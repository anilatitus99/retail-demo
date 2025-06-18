variable "project_id" {
  type        = string
  description = "GCP project ID"
}

variable "image_tag" {
  type        = string
  description = "Docker image tag to deploy"
  default     = "latest"  # fallback default
}
