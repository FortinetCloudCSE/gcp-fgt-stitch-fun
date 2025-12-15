import functions_framework
import json
import logging
from flask import Request
from google.cloud import firestore
from google.cloud import compute_v1
from datetime import datetime
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize clients
db = firestore.Client()
compute_client = compute_v1.InstancesClient()
COLLECTION_NAME = 'processed_source_ips'

# Get project ID from environment or metadata
PROJECT_ID = os.environ.get('GCP_PROJECT', os.environ.get('GOOGLE_CLOUD_PROJECT'))

def is_ip_processed(srcip):
    """Check if source IP has already been processed."""
    try:
        doc_ref = db.collection(COLLECTION_NAME).document(srcip)
        doc = doc_ref.get()
        return doc.exists
    except Exception as e:
        logger.error(f"Error checking IP in Firestore: {e}")
        return False

def add_processed_ip(srcip):
    """Add source IP to processed database."""
    try:
        doc_ref = db.collection(COLLECTION_NAME).document(srcip)
        doc_ref.set({
            'ip_address': srcip,
            'first_seen': datetime.utcnow(),
            'processed_at': firestore.SERVER_TIMESTAMP
        })
        logger.info(f"Successfully added IP {srcip} to Firestore")
        return True
    except Exception as e:
        logger.error(f"Error adding IP to Firestore: {e}")
        return False

def get_processed_ips_count():
    """Get count of processed IPs from Firestore."""
    try:
        docs = db.collection(COLLECTION_NAME).stream()
        return len(list(docs))
    except Exception as e:
        logger.error(f"Error counting processed IPs: {e}")
        return 0

def find_instance_by_ip(srcip):
    """Find GCP compute instance by internal or external IP address."""
    try:
        print(f"🔍 Searching for GCP instance with IP: {srcip}")
        
        # List all zones in the project
        zones_client = compute_v1.ZonesClient()
        zones = zones_client.list(project=PROJECT_ID)
        
        for zone in zones:
            try:
                # List instances in this zone
                instances = compute_client.list(project=PROJECT_ID, zone=zone.name)
                
                for instance in instances:
                    # Check network interfaces for matching IPs
                    for interface in instance.network_interfaces:
                        # Check internal IP
                        if interface.network_i_p == srcip:
                            print(f"✅ Found instance '{instance.name}' in zone '{zone.name}' with internal IP: {srcip}")
                            return instance.name, zone.name
                        
                        # Check external IP (access configs)
                        if interface.access_configs:
                            for access_config in interface.access_configs:
                                if access_config.nat_i_p == srcip:
                                    print(f"✅ Found instance '{instance.name}' in zone '{zone.name}' with external IP: {srcip}")
                                    return instance.name, zone.name
            
            except Exception as zone_error:
                logger.warning(f"Error checking zone {zone.name}: {zone_error}")
                continue
        
        print(f"❌ No GCP instance found with IP: {srcip}")
        return None, None
        
    except Exception as e:
        logger.error(f"Error searching for instance by IP: {e}")
        return None, None

def add_compromised_tag(instance_name, zone_name, srcip):
    """Add 'compromised' network tag to the specified instance."""
    try:
        print(f"🏷️  Adding 'compromised' tag to instance: {instance_name} in zone: {zone_name}")
        
        # Get current instance details
        instance = compute_client.get(project=PROJECT_ID, zone=zone_name, instance=instance_name)
        
        # Get current tags
        current_tags = list(instance.tags.items) if instance.tags and instance.tags.items else []
        
        # Check if 'compromised' tag already exists
        if 'compromised' in current_tags:
            print(f"⚠️  Instance {instance_name} already has 'compromised' tag")
            return True
        
        # Add 'compromised' tag
        new_tags = current_tags + ['compromised']
        
        # Create tags object
        tags_body = compute_v1.Tags()
        tags_body.items = new_tags
        tags_body.fingerprint = instance.tags.fingerprint if instance.tags else None
        
        # Update instance tags
        operation = compute_client.set_tags(
            project=PROJECT_ID,
            zone=zone_name,
            instance=instance_name,
            tags_resource=tags_body
        )
        
        print(f"🔄 Tag update operation started for {instance_name}: {operation.name}")
        print(f"✅ Successfully added 'compromised' tag to instance {instance_name}")
        
        # Log the action to Firestore
        doc_ref = db.collection('compromised_instances').document(f"{instance_name}_{zone_name}")
        doc_ref.set({
            'instance_name': instance_name,
            'zone': zone_name,
            'source_ip': srcip,
            'tagged_at': firestore.SERVER_TIMESTAMP,
            'operation_id': operation.name,
            'previous_tags': current_tags,
            'new_tags': new_tags
        })
        
        return True
        
    except Exception as e:
        logger.error(f"Error adding compromised tag to instance {instance_name}: {e}")
        return False

@functions_framework.http
def log_request(request: Request):
    """
    Cloud Function that logs all incoming request headers and body data.
    
    Args:
        request: The HTTP request object
        
    Returns:
        A JSON response indicating the request was logged
    """
    
    print("🚀 Cloud Function log_request() called!")
    print("Function execution started - processing incoming request...")
    
    # Initialize variables for traffic violation processing
    srcip = None
    is_traffic_violation = False
    
    # Extract request method and path
    method = request.method
    path = request.path
    url = request.url
    
    # Extract all headers
    headers = dict(request.headers)
    
    # Extract query parameters
    query_params = dict(request.args)
    
    # Extract request body
    body_data = None
    content_type = request.content_type or "unknown"
    
    try:
        if request.content_length and request.content_length > 0:
            if content_type.startswith('application/json'):
                # Try to parse JSON body
                try:
                    body_data = request.get_json()
                except Exception as e:
                    # If JSON parsing fails, get raw data
                    body_data = request.get_data(as_text=True)
                    logger.warning(f"Failed to parse JSON body: {e}")
            elif content_type.startswith('application/x-www-form-urlencoded'):
                # Parse form data
                body_data = dict(request.form)
            elif content_type.startswith('multipart/form-data'):
                # Parse multipart form data
                form_data = {}
                for key, value in request.form.items():
                    form_data[key] = value
                
                # Handle files
                files_data = {}
                for key, file in request.files.items():
                    files_data[key] = {
                        'filename': file.filename,
                        'content_type': file.content_type,
                        'size': len(file.read())
                    }
                    file.seek(0)  # Reset file pointer
                
                body_data = {
                    'form': form_data,
                    'files': files_data
                }
            else:
                # For other content types, get raw data as text
                body_data = request.get_data(as_text=True)
        else:
            body_data = "No body data"
    except Exception as e:
        logger.error(f"Error extracting body data: {e}")
        body_data = f"Error reading body: {str(e)}"
    
    # Check for traffic violation events and extract srcip
    if isinstance(body_data, dict):
        try:
            # Check if this is a traffic violation event
            eventtype = None
            
            # Navigate through the nested structure to find eventtype
            if 'data' in body_data:
                if 'eventtype' in body_data['data']:
                    eventtype = body_data['data']['eventtype']
                elif 'rawlog' in body_data['data'] and 'eventtype' in body_data['data']['rawlog']:
                    eventtype = body_data['data']['rawlog']['eventtype']
            
            # Check if it's a traffic violation
            if eventtype == "traffic violation":
                is_traffic_violation = True
                print("🚨 TRAFFIC VIOLATION DETECTED!")
                
                # Extract srcip from rawlog
                if ('data' in body_data and 
                    'rawlog' in body_data['data'] and 
                    'srcip' in body_data['data']['rawlog']):
                    srcip = body_data['data']['rawlog']['srcip']
                    print(f"📍 Source IP extracted: {srcip}")
                    
                    # Check if this IP has already been processed using Firestore
                    if is_ip_processed(srcip):
                        print(f"🔄 IP {srcip} already processed in Firestore - IGNORING future logs")
                        
                        # Return early response for ignored IPs
                        response_data = {
                            'status': 'ignored',
                            'message': f'Source IP {srcip} already processed - ignoring duplicate traffic violation',
                            'source_ip': srcip,
                            'processed_ips_count': get_processed_ips_count(),
                            'database': 'firestore'
                        }
                        return json.dumps(response_data, indent=2), 200, {'Content-Type': 'application/json'}
                    
                    else:
                        # Add IP to Firestore
                        if add_processed_ip(srcip):
                            print(f"✅ IP {srcip} added to Firestore database")
                            
                            # Find and tag the compromised instance
                            instance_name, zone_name = find_instance_by_ip(srcip)
                            if instance_name and zone_name:
                                tag_success = add_compromised_tag(instance_name, zone_name, srcip)
                                if tag_success:
                                    print(f"🎯 Successfully tagged instance {instance_name} as compromised")
                                else:
                                    print(f"❌ Failed to tag instance {instance_name}")
                            else:
                                print(f"🤷 No matching GCP instance found for IP {srcip}")
                        else:
                            print(f"❌ Failed to add IP {srcip} to Firestore")
                        
                else:
                    print("⚠️  Could not find srcip in rawlog data")
            
        except Exception as e:
            logger.warning(f"Error processing traffic violation data: {e}")
    
    # Create comprehensive log entry
    log_entry = {
        'timestamp': None,  # Cloud Logging will add timestamp
        'request_info': {
            'method': method,
            'path': path,
            'url': url,
            'content_type': content_type,
            'content_length': request.content_length
        },
        'headers': headers,
        'query_parameters': query_params,
        'body': body_data,
        'remote_addr': request.environ.get('REMOTE_ADDR', 'unknown'),
        'user_agent': headers.get('User-Agent', 'unknown')
    }
    
    # Log the complete request information using print for better Cloud Run visibility
    print("=== INCOMING REQUEST LOGGED ===")
    print(f"Method: {method}")
    print(f"URL: {url}")
    print(f"Path: {path}")
    print(f"Content-Type: {content_type}")
    print(f"Content-Length: {request.content_length}")
    print(f"Remote Address: {request.environ.get('REMOTE_ADDR', 'unknown')}")
    
    print("\n--- REQUEST HEADERS ---")
    for key, value in headers.items():
        print(f"{key}: {value}")
    
    print(f"\n--- QUERY PARAMETERS ---")
    for key, value in query_params.items():
        print(f"{key}: {value}")
    
    print(f"\n--- REQUEST BODY ---")
    print(f"Body Type: {type(body_data).__name__}")
    if isinstance(body_data, dict):
        print("Body Content (JSON):")
        print(json.dumps(body_data, indent=2, default=str))
    else:
        print(f"Body Content: {body_data}")
    
    # Traffic violation specific logging
    if is_traffic_violation:
        print(f"\n--- TRAFFIC VIOLATION ANALYSIS ---")
        print(f"Event Type: traffic violation")
        print(f"Source IP: {srcip if srcip else 'NOT FOUND'}")
        if srcip:
            print(f"🔍 Processing NEW traffic violation from source: {srcip}")
            print(f"📊 Total processed IPs in Firestore: {get_processed_ips_count()}")
            print(f"🔥 Database: Google Cloud Firestore")
    
    print("\n--- COMPLETE REQUEST DATA (JSON) ---")
    print(json.dumps(log_entry, indent=2, default=str))
    print("=== END REQUEST LOG ===\n")
    
    # Also use logger for structured logging
    logger.info("Request processed", extra={'request_data': log_entry})
    
    # Prepare response
    response_data = {
        'status': 'success',
        'message': 'Request logged successfully',
        'logged_at': 'check Cloud Logging for details',
        'request_summary': {
            'method': method,
            'path': path,
            'headers_count': len(headers),
            'query_params_count': len(query_params),
            'has_body': body_data != "No body data"
        },
        'traffic_violation': {
            'detected': is_traffic_violation,
            'source_ip': srcip,
            'database': 'firestore',
            'processed_ips_count': get_processed_ips_count() if is_traffic_violation else 0
        } if is_traffic_violation else None
    }
    
    return json.dumps(response_data, indent=2), 200, {'Content-Type': 'application/json'}