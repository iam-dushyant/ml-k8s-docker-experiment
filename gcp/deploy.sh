#!/bin/bash

gcloud run deploy iris-api \
    --image "$REGION-docker.pkg.dev/$PROJECT_ID/$REPO/$IMAGE:v1" \
    --region "$REGION" \
    --platform managed \
    --allow-unauthenticated \
    --min 0 \
    --max 1 \
    --memory 512Mi \
    --cpu 1