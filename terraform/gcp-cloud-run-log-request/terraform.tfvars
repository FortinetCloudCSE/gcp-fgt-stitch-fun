# Example terraform.tfvars file
# Copy this to terraform.tfvars and customize the values

# Required: Your GCP Project ID

# Optional: Customize these values as needed
function_name = "my-request-logger"
region       = "us-central1"
memory_mb    = 512
timeout_seconds = 120

# Security settings
allow_unauthenticated = true  # Set to false for production

# Environment variables for the function
environment_variables = {
  LOG_LEVEL     = "DEBUG"
  ENVIRONMENT   = "development"
  CUSTOM_HEADER = "X-My-App"
}

# Labels for resource organization
labels = {
  environment = "development"
  team        = "platform"
  purpose     = "debugging"
  cost-center = "engineering"
}