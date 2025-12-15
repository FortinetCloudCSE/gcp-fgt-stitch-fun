# Generate a unique suffix for the bucket name
resource "random_id" "bucket_suffix" {
  byte_length = 4
}

# Create a Cloud Storage bucket for the function source code
resource "google_storage_bucket" "function_bucket" {
  project                     = var.project_id
  name                        = "${var.function_name}-source-${random_id.bucket_suffix.hex}"
  location                    = var.region
  uniform_bucket_level_access = true
  
  # Optional: Add lifecycle rule to clean up old versions
  lifecycle_rule {
    condition {
      age = 30
    }
    action {
      type = "Delete"
    }
  }
}

# Create a zip file of the function source code
data "archive_file" "function_source" {
  type        = "zip"
  source_dir  = "${path.module}/src"
  output_path = "${path.module}/function-source.zip"
}

# Upload the function source code to the bucket
resource "google_storage_bucket_object" "function_source" {
  name   = "function-source-${data.archive_file.function_source.output_md5}.zip"
  bucket = google_storage_bucket.function_bucket.name
  source = data.archive_file.function_source.output_path
}

# Create the Cloud Function (2nd generation)
resource "google_cloudfunctions2_function" "function" {
  project     = var.project_id
  name        = var.function_name
  location    = var.region
  description = var.function_description

  build_config {
    runtime     = "python311"
    entry_point = var.entry_point
    source {
      storage_source {
        bucket = google_storage_bucket.function_bucket.name
        object = google_storage_bucket_object.function_source.name
      }
    }
  }

  service_config {
    max_instance_count    = 100
    available_memory      = "${var.memory_mb}Mi"
    timeout_seconds       = var.timeout_seconds
    environment_variables = var.environment_variables
    
    ingress_settings               = "ALLOW_ALL"
    all_traffic_on_latest_revision = true
  }

  labels = var.labels
}

# Get the Cloud Function service account
data "google_compute_default_service_account" "default" {
  project = var.project_id
}

# Grant Compute Engine permissions to the function's service account
resource "google_project_iam_member" "function_compute_admin" {
  project = var.project_id
  role    = "roles/compute.instanceAdmin.v1"
  member  = "serviceAccount:${google_cloudfunctions2_function.function.service_config[0].service_account_email}"

  depends_on = [google_cloudfunctions2_function.function]
}

resource "google_project_iam_member" "function_compute_viewer" {
  project = var.project_id
  role    = "roles/compute.viewer"
  member  = "serviceAccount:${google_cloudfunctions2_function.function.service_config[0].service_account_email}"

  depends_on = [google_cloudfunctions2_function.function]
}

# IAM binding to make the function publicly accessible (optional)
resource "google_cloud_run_service_iam_member" "invoker" {
  count    = var.allow_unauthenticated ? 1 : 0
  project  = google_cloudfunctions2_function.function.project
  location = google_cloudfunctions2_function.function.location
  service  = google_cloudfunctions2_function.function.name

  role   = "roles/run.invoker"
  member = "allUsers"
}