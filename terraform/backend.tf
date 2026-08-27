terraform {
    backend "gcs" {
        bucket = "k8s-docker-ml-dev-tfstate"
        prefix = "dev"      
    }
}