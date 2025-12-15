# Example Usage of the Cloud Function Logging Module

This file demonstrates how to use the Cloud Function logging module in different scenarios.

## Basic Usage

```hcl
module "basic_logging_function" {
  source = "./terraform-gcp-cloud-function"
  
  function_name = "basic-request-logger"
}
```

## Advanced Usage

```hcl
module "advanced_logging_function" {
  source = "./terraform-gcp-cloud-function"
  
  function_name        = "advanced-request-logger"
  function_description = "Advanced request logging with custom settings"
  region              = "us-east1"
  memory_mb           = 512
  timeout_seconds     = 120
  
  # Allow public access (use with caution in production)
  allow_unauthenticated = true
  
  # Custom environment variables
  environment_variables = {
    LOG_LEVEL     = "INFO"
    ENVIRONMENT   = "production"
    CUSTOM_HEADER = "X-Custom-App"
  }
  
  # Labels for resource organization
  labels = {
    environment = "production"
    team        = "platform"
    purpose     = "request-logging"
    cost-center = "engineering"
  }
}
```

## Required Provider Configuration

```hcl
provider "google" {
  project = "your-project-id"
  region  = "us-central1"
}
```