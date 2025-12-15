variable "project_id" {
  description = "The GCP project ID where resources will be created"
  type        = string
  default     = "cse-us-341516"
}

variable "function_name" {
  description = "Name of the Cloud Function"
  type        = string
}

variable "function_description" {
  description = "Description of the Cloud Function"
  type        = string
  default     = "Cloud Function that logs all incoming request headers and body data"
}

variable "region" {
  description = "GCP region where the function will be deployed"
  type        = string
  default     = "us-central1"
}

variable "memory_mb" {
  description = "Memory allocation for the Cloud Function in MB"
  type        = number
  default     = 256
  
  validation {
    condition = contains([128, 256, 512, 1024, 2048, 4096, 8192], var.memory_mb)
    error_message = "Memory must be one of: 128, 256, 512, 1024, 2048, 4096, 8192."
  }
}

variable "timeout_seconds" {
  description = "Timeout for the Cloud Function in seconds"
  type        = number
  default     = 60
  
  validation {
    condition = var.timeout_seconds >= 1 && var.timeout_seconds <= 540
    error_message = "Timeout must be between 1 and 540 seconds."
  }
}

variable "entry_point" {
  description = "The name of the function to execute"
  type        = string
  default     = "log_request"
}



variable "allow_unauthenticated" {
  description = "Whether to allow unauthenticated access to the function"
  type        = bool
  default     = false
}

variable "environment_variables" {
  description = "Environment variables for the Cloud Function"
  type        = map(string)
  default     = {}
}

variable "labels" {
  description = "Labels to apply to the Cloud Function"
  type        = map(string)
  default     = {}
}