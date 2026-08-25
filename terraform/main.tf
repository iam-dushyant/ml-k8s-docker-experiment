locals {
  required_apis = toset([
    "artifactregistry.googleapis.com",
    "container.googleapis.com",
    "storage.googleapis.com",
    "aiplatform.googleapis.com",
    "monitoring.googleapis.com",
    "logging.googleapis.com",
  ])
}

resource "google_project_service" "required" {
  for_each = local.required_apis

  project            = var.project_id
  service            = each.value
  disable_on_destroy = false
}

resource "google_artifact_registry_repository" "docker" {
  project       = var.project_id
  location      = var.region
  repository_id = var.artifact_repo
  description   = "Docker images for the MLOps experiment"
  format        = "DOCKER"

  depends_on = [
    google_project_service.required["artifactregistry.googleapis.com"]
  ]
}

resource "google_storage_bucket" "model_artifacts" {
  project                     = var.project_id
  name                        = var.model_bucket_name
  location                    = var.region
  uniform_bucket_level_access = true
  force_destroy               = true

  versioning {
    enabled = true
  }

  depends_on = [
    google_project_service.required["storage.googleapis.com"]
  ]
}

resource "google_container_cluster" "autopilot" {
  project             = var.project_id
  name                = var.cluster_name
  location            = var.region
  enable_autopilot    = true
  deletion_protection = false

  depends_on = [
    google_project_service.required["container.googleapis.com"]
  ]
}