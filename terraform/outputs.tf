output "artifact_registry" {
  value = google_artifact_registry_repository.docker.repository_id
}

output "model_bucket_name" {
  value = google_storage_bucket.model_artifacts.name
}

output "cluster_name" {
  value = google_container_cluster.autopilot.name
}

output "cluster_region" {
  value = var.region
}