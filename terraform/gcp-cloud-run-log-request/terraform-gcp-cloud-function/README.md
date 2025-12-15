# Google Cloud Function Terraform Module

This Terraform module creates a Google Cloud Function (2nd generation) that logs all incoming HTTP request headers and body data, with specialized handling for FortiGate traffic violation events. The function provides automated incident response by detecting compromised devices and tagging them in GCP.

## Features

- 🔍 **Comprehensive Logging**: Logs all request headers, query parameters, and body data
- 🚨 **Traffic Violation Detection**: Automatically detects FortiGate traffic violation events
- 🔥 **Firestore Integration**: Persistent tracking of processed source IPs to prevent duplicates
- 🏷️ **Automatic Instance Tagging**: Finds and tags compromised GCP instances with "compromised" network tag
- 🛡️ **Security Automation**: Complete incident response workflow for compromised devices
- 📊 **Multiple Content Types**: Handles JSON, form data, multipart uploads, and raw data
- 🔧 **2nd Generation**: Uses Cloud Functions 2nd gen running on Cloud Run for better performance
- ⚙️ **Configurable**: Customizable memory, timeout, and other settings

## Usage

### Basic Example

```hcl
module "logging_function" {
  source = "./terraform-gcp-cloud-function"
  
  project_id    = "your-gcp-project-id"
  function_name = "request-logger"
}
```

### Advanced Example

```hcl
module "logging_function" {
  source = "./terraform-gcp-cloud-function"
  
  project_id           = "your-gcp-project-id"
  function_name        = "fortigate-incident-response"
  function_description = "FortiGate traffic violation processor with automated incident response"
  region              = "us-central1"
  memory_mb           = 512
  timeout_seconds     = 120
  
  allow_unauthenticated = true
  
  environment_variables = {
    LOG_LEVEL = "DEBUG"
    APP_ENV   = "production"
  }
  
  labels = {
    environment = "production"
    team        = "security"
    purpose     = "incident-response"
  }
}
```

## Traffic Violation Processing

The Cloud Function includes specialized handling for FortiGate traffic violation events:

### Automated Incident Response Workflow
1. **Detection**: Identifies requests with `eventtype: "traffic violation"`
2. **IP Extraction**: Extracts source IP from `rawlog.srcip` field
3. **Duplicate Prevention**: Checks Firestore database for previously processed IPs
4. **Instance Discovery**: Searches all GCP zones for compute instances matching the source IP
5. **Automatic Tagging**: Adds "compromised" network tag to matching instances
6. **Audit Logging**: Records all actions in both Cloud Logging and Firestore

### FortiGate Log Structure
The function expects FortiGate logs in this format:
```json
{
  "data": {
    "eventtype": "traffic violation",
    "rawlog": {
      "srcip": "10.128.0.11",
      "dstip": "8.8.8.8",
      "action": "deny",
      "service": "HTTPS",
      "policyname": "block-compromised"
    }
  }
}
```

## What Gets Logged

The Cloud Function logs the following information for each request:

### Request Metadata
- HTTP method (GET, POST, etc.)
- Request path and full URL
- Content type and content length
- Remote IP address
- User agent

### Headers
- All HTTP headers as key-value pairs

### Query Parameters
- All URL query parameters

### Request Body
- **JSON**: Parsed as structured data
- **Form Data**: Parsed form fields
- **Multipart**: Form fields and file metadata
- **Raw Data**: Text representation for other content types

### Example Response for Traffic Violations

**New Traffic Violation (First Time):**
```json
{
  "status": "success",
  "message": "Request logged successfully",
  "logged_at": "check Cloud Logging for details",
  "request_summary": {
    "method": "POST",
    "path": "/",
    "headers_count": 11,
    "query_params_count": 0,
    "has_body": true
  },
  "traffic_violation": {
    "detected": true,
    "source_ip": "10.128.0.11",
    "database": "firestore",
    "processed_ips_count": 4
  }
}
```

**Duplicate Traffic Violation (Already Processed):**
```json
{
  "status": "ignored",
  "message": "Source IP 10.128.0.11 already processed - ignoring duplicate traffic violation",
  "source_ip": "10.128.0.11",
  "processed_ips_count": 4,
  "database": "firestore"
}
```

## Requirements

### Prerequisites
- Google Cloud Project with billing enabled
- Cloud Functions API enabled (automatically enabled by module)
- Cloud Storage API enabled (automatically enabled by module)
- Firestore API enabled (automatically enabled by module)
- Compute Engine API enabled (automatically enabled by module)
- Appropriate IAM permissions for instance tagging

### Terraform Requirements
```hcl
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 4.0"
    }
    archive = {
      source  = "hashicorp/archive"
      version = ">= 2.0"
    }
    random = {
      source  = "hashicorp/random"
      version = ">= 3.0"
    }
  }
}
```

## Variables

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| `project_id` | The GCP project ID where resources will be created | `string` | n/a | yes |
| `function_name` | Name of the Cloud Function | `string` | n/a | yes |
| `function_description` | Description of the Cloud Function | `string` | `"Cloud Function that logs all incoming request headers and body data"` | no |
| `region` | GCP region where the function will be deployed | `string` | `"us-central1"` | no |
| `memory_mb` | Memory allocation for the Cloud Function in MB | `number` | `256` | no |
| `timeout_seconds` | Timeout for the Cloud Function in seconds | `number` | `60` | no |
| `entry_point` | The name of the function to execute | `string` | `"log_request"` | no |
| `allow_unauthenticated` | Whether to allow unauthenticated access to the function | `bool` | `false` | no |
| `environment_variables` | Environment variables for the Cloud Function | `map(string)` | `{}` | no |
| `labels` | Labels to apply to the Cloud Function | `map(string)` | `{}` | no |

## Outputs

| Name | Description |
|------|-------------|
| `function_name` | Name of the deployed Cloud Function |
| `function_url` | URL of the deployed Cloud Function |
| `function_region` | Region where the Cloud Function is deployed |
| `function_project` | Project ID where the Cloud Function is deployed |
| `source_bucket_name` | Name of the Cloud Storage bucket containing the function source |
| `source_bucket_url` | URL of the Cloud Storage bucket containing the function source |

## Deployment Steps

1. **Configure Terraform**:
   ```bash
   # Set your project ID in terraform.tfvars
   echo 'project_id = "your-gcp-project-id"' > terraform.tfvars
   echo 'function_name = "fortigate-incident-response"' >> terraform.tfvars
   
   terraform init
   terraform plan
   terraform apply
   ```

2. **Test with Traffic Violation**:
   ```bash
   # Get the function URL from Terraform outputs
   FUNCTION_URL=$(terraform output -raw function_url)
   
   # Test FortiGate traffic violation
   curl -X POST "$FUNCTION_URL" \
     -H "Content-Type: application/json" \
     -d '{
       "data": {
         "eventtype": "traffic violation",
         "rawlog": {
           "srcip": "10.128.0.11",
           "dstip": "8.8.8.8",
           "action": "deny",
           "service": "HTTPS",
           "policyname": "block-compromised"
         }
       }
     }'
   ```

3. **Verify Instance Tagging**:
   ```bash
   # Check if instance was tagged (replace with actual instance name and zone)
   gcloud compute instances describe INSTANCE_NAME --zone=ZONE --format="value(tags.items)"
   ```

4. **View Logs**:
   ```bash
   gcloud functions logs read fortigate-incident-response --region=us-central1
   ```

## Security Considerations

- **Authentication**: By default, the function requires authentication. Set `allow_unauthenticated = true` only if needed.
- **IAM Permissions**: The function requires `compute.instanceAdmin.v1` and `compute.viewer` roles for instance tagging.
- **Network Tags**: The "compromised" tag should be used in firewall rules to isolate affected instances.
- **Data Sensitivity**: Be cautious when logging requests that may contain sensitive data.
- **Firestore Security**: Processed IPs are stored in Firestore - ensure proper access controls.
- **False Positives**: Review tagged instances regularly to prevent blocking legitimate traffic.
- **Log Retention**: Configure appropriate log retention policies for audit trails.
- **Access Control**: Restrict access to Cloud Logging and Firestore to authorized security personnel only.

## Monitoring

The function provides comprehensive monitoring capabilities:

### Cloud Logging
1. **View logs in Cloud Console**: Navigate to Cloud Functions → Your Function → Logs
2. **Use gcloud CLI**: `gcloud functions logs read <function-name>`
3. **Set up log-based alerts**: Create alerting policies for traffic violations
4. **Export logs**: Set up log sinks to BigQuery, Pub/Sub, or Cloud Storage

### Firestore Collections
- **processed_source_ips**: Tracks all processed violation source IPs
- **compromised_instances**: Records all instances that have been tagged

### Recommended Alerts
1. **Traffic Violation Detection**: Alert on "TRAFFIC VIOLATION DETECTED" log messages
2. **Instance Tagging**: Alert when instances are tagged as compromised
3. **Function Errors**: Alert on function execution failures
4. **High Volume**: Alert on unusual volumes of traffic violations

### Dashboard Queries
```sql
-- Count traffic violations by source IP
SELECT srcip, COUNT(*) as violation_count
FROM your_project.your_dataset.firestore_processed_source_ips
GROUP BY srcip
ORDER BY violation_count DESC
```

## Troubleshooting

### Common Issues

1. **Function not receiving requests**:
   - Check if `allow_unauthenticated` is set correctly
   - Verify IAM permissions
   - Ensure the function URL is correct

2. **Deployment failures**:
   - Ensure `project_id` is correctly set in variables
   - Verify required APIs are enabled (done automatically by module)
   - Check IAM permissions for Cloud Functions, Storage, Firestore, and Compute Engine
   - Ensure the source code is valid

3. **Instance tagging not working**:
   - Verify the function has `compute.instanceAdmin.v1` permissions
   - Check if the source IP matches any actual GCP instance internal/external IPs
   - Ensure Compute Engine API is enabled
   - Check function logs for "Instance found" messages

4. **Firestore connection issues**:
   - Verify Firestore API is enabled
   - Check if Firestore database is initialized in your project
   - Ensure proper IAM permissions for Firestore access

5. **Traffic violations not detected**:
   - Verify the JSON payload contains `data.eventtype: "traffic violation"`
   - Check that `data.rawlog.srcip` field exists in the request
   - Review function logs for parsing errors

6. **Missing logs**:
   - Check Cloud Logging quotas and limits
   - Verify log retention settings
   - Ensure the function is actually being invoked
   - Look for logs in both stdout and error streams

## License

This module is provided under the MIT License. See LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request