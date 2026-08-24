variable "project_id" {
  description = "The GCP project ID"
  type        = string
}

variable "region" {
  description = "The GCP region"
  type        = string
}

variable "artifact_repo" {
  description = "The GCP Artifact Registry name"
  type        = string
  default     = "ml-platform-v2"
}

variable "cluster_name" {
  description = "The GKE Autopilot cluster name"
  type        = string
}

variable "model_bucket_name" {
  description = "The GCP bucket name for storing ML models"
  type        = string
}