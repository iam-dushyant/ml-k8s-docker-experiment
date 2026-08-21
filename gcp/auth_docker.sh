#!/bin/bash

gcloud auth configure-docker "$REGION-docker.pkg.dev"

docker buildx build \
    --platform linux/amd64 \
    -t "$REGION-docker.pkg.dev/$PROJECT_ID/$REPO/$IMAGE:v1" \
    --push .