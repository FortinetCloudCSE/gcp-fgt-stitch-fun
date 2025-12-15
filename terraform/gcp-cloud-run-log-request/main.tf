# Configure the Terraform providers
terraform {
  required_version = ">= 1.0"
  
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 4.0, < 6.0"
    }
  }
}

# Configure the Google Cloud Provider
provider "google" {
  project = var.project_id
  region  = var.region
}

# Enable required APIs
resource "google_project_service" "firestore" {
  project = var.project_id
  service = "firestore.googleapis.com"
  
  disable_dependent_services = true
  disable_on_destroy        = false
}

resource "google_project_service" "cloudfunctions" {
  project = var.project_id
  service = "cloudfunctions.googleapis.com"
  
  disable_dependent_services = true
  disable_on_destroy        = false
}

resource "google_project_service" "cloudbuild" {
  project = var.project_id
  service = "cloudbuild.googleapis.com"
  
  disable_dependent_services = true
  disable_on_destroy        = false
}

resource "google_project_service" "compute" {
  project = var.project_id
  service = "compute.googleapis.com"
  
  disable_dependent_services = true
  disable_on_destroy        = false
}

# Call the Cloud Function logging module
module "request_logger" {
  source = "./terraform-gcp-cloud-function"
  
  # Pass the project ID to the module
  project_id          = var.project_id
  function_name        = var.function_name
  function_description = "Cloud Function for logging all incoming HTTP requests with Firestore tracking"
  region              = var.region
  memory_mb           = var.memory_mb
  timeout_seconds     = var.timeout_seconds
  
  # Security configuration
  allow_unauthenticated = var.allow_unauthenticated
  
  # Environment variables for the function
  environment_variables = merge(var.environment_variables, {
    GCP_PROJECT = var.project_id
  })
  
  # Labels for resource organization
  labels = merge(var.labels, {
    managed-by = "terraform"
    module     = "gcp-cloud-function-logger"
    created    = formatdate("YYYY-MM-DD", timestamp())
  })
  
  # Ensure APIs are enabled before creating the function
  depends_on = [
    google_project_service.firestore,
    google_project_service.cloudfunctions,
    google_project_service.cloudbuild,
    google_project_service.compute
  ]
}