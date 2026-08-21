#!/bin/bash

set -e

export PROJECT_ID="k8s-docker-ml-dev"
export REGION="europe-west1"
export REPO="k8-docker-ml-dev"
export IMAGE="iris-api"

echo "Using project: $PROJECT_ID"
echo "Using region:  $REGION"

gcloud auth login
gcloud config set project "$PROJECT_ID"

gcloud services enable \
  artifactregistry.googleapis.com \
  run.googleapis.com