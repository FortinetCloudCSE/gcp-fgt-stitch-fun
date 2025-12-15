output "function_name" {
  description = "Name of the deployed Cloud Function"
  value       = google_cloudfunctions2_function.function.name
}

output "function_url" {
  description = "URL of the deployed Cloud Function"
  value       = google_cloudfunctions2_function.function.service_config[0].uri
}

output "function_region" {
  description = "Region where the Cloud Function is deployed"
  value       = google_cloudfunctions2_function.function.location
}

output "function_project" {
  description = "Project ID where the Cloud Function is deployed"
  value       = google_cloudfunctions2_function.function.project
}

output "source_bucket_name" {
  description = "Name of the Cloud Storage bucket containing the function source"
  value       = google_storage_bucket.function_bucket.name
}

output "source_bucket_url" {
  description = "URL of the Cloud Storage bucket containing the function source"
  value       = google_storage_bucket.function_bucket.url
}