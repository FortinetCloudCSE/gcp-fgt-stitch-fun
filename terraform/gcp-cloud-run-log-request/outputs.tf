# Output the function details
output "function_name" {
  description = "Name of the deployed Cloud Function"
  value       = module.request_logger.function_name
}

output "function_url" {
  description = "HTTPS URL of the deployed Cloud Function"
  value       = module.request_logger.function_url
}

output "function_region" {
  description = "Region where the Cloud Function is deployed"
  value       = module.request_logger.function_region
}

output "function_project" {
  description = "Project ID where the Cloud Function is deployed"
  value       = module.request_logger.function_project
}

output "source_bucket_name" {
  description = "Name of the Cloud Storage bucket containing the function source"
  value       = module.request_logger.source_bucket_name
}

output "curl_test_command" {
  description = "Example curl command to test the function"
  value = <<-EOT
    # Test with GET request
    curl "${module.request_logger.function_url}?test=true&user=demo"
    
    # Test with POST request and JSON data
    curl -X POST "${module.request_logger.function_url}" \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer test-token" \
      -H "X-Custom-Header: demo-value" \
      -d '{"message": "Hello from test", "timestamp": "2025-12-10", "data": {"key": "value"}}'
  EOT
}

output "logs_command" {
  description = "Command to view the function logs"
  value       = "gcloud functions logs read ${module.request_logger.function_name} --region=${module.request_logger.function_region} --limit=50"
}