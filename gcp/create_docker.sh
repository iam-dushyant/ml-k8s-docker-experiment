# !/bin/bash

gcloud artifact-registry repositories create "$REPO" \
  --repository-format=docker \
  --location="$REGION" \
  --description="Docker repository for ML Lab"