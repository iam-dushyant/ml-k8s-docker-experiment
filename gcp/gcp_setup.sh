#!/bin/bash

#source "$(dirname "$0")/config.sh"

echo "Using project: $PROJECT_ID"
echo "Using region:  $REGION"

gcloud auth list
gcloud config set project "$PROJECT_ID"

gcloud services enable \
  artifactregistry.googleapis.com \
  run.googleapis.com