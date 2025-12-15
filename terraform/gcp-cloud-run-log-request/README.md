# Terraform GCP Cloud Function Deployment

This Terraform configuration deploys a Google Cloud Function that logs all incoming HTTP request data using the custom module in the `terraform-gcp-cloud-function` directory.

## Quick Start

1. **Set up your GCP project**:
   ```bash
   # Enable required APIs
   gcloud services enable cloudfunctions.googleapis.com
   gcloud services enable cloudbuild.googleapis.com
   gcloud services enable storage-api.googleapis.com
   ```

2. **Configure variables**:
   ```bash
   # Copy the example variables file
   cp terraform.tfvars.example terraform.tfvars
   
   # Edit terraform.tfvars and set your project ID
   vim terraform.tfvars
   ```

3. **Deploy the infrastructure**:
   ```bash
   # Initialize Terraform
   terraform init
   
   # Plan the deployment
   terraform plan
   
   # Apply the configuration
   terraform apply
   ```

4. **Test the function**:
   ```bash
   # Get the function URL
   FUNCTION_URL=$(terraform output -raw function_url)
   
   # Test with curl (commands will be shown in terraform output)
   terraform output curl_test_command
   ```

5. **View logs**:
   ```bash
   # Use the command from terraform output
   terraform output logs_command
   ```

## Configuration Options

### Required Variables
- `project_id`: Your GCP project ID

### Optional Variables
- `function_name`: Name of the Cloud Function (default: "http-request-logger")
- `region`: GCP region (default: "us-central1")
- `memory_mb`: Memory allocation in MB (default: 256)
- `timeout_seconds`: Function timeout in seconds (default: 60)
- `allow_unauthenticated`: Allow public access (default: false)
- `security_level`: HTTPS security level (default: "SECURE_ALWAYS")
- `environment_variables`: Custom environment variables (map)
- `labels`: Resource labels (map)

## Example Usage

### Basic deployment:
```bash
# Set only the required variable
export TF_VAR_project_id="your-project-id"
terraform apply
```

### Advanced deployment with custom settings:
```hcl
# In terraform.tfvars
project_id = "my-gcp-project"
function_name = "production-logger"
region = "us-east1"
memory_mb = 1024
allow_unauthenticated = true

environment_variables = {
  LOG_LEVEL = "INFO"
  APP_ENV = "production"
}

labels = {
  environment = "production"
  team = "platform"
}
```

## Outputs

After deployment, Terraform will output:
- Function name and URL
- Example curl commands for testing
- Command to view function logs
- Source bucket information

## Clean Up

To destroy all resources:
```bash
terraform destroy
```

## Security Notes

- By default, the function requires authentication
- Set `allow_unauthenticated = true` only if you need public access
- Be cautious about logging sensitive data in production
- Configure appropriate log retention policies