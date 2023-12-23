#!/usr/bin/env bash
set -eu

# # Building docker image
docker build -t us-central1-docker.pkg.dev/mipt-hack-01/cloud-run/city-bot .

# # Pushing to Artifactory Registry
docker push us-central1-docker.pkg.dev/mipt-hack-01/cloud-run/city-bot

# Redeploying the new revision from the image
gcloud run deploy city-bot \
    --image us-central1-docker.pkg.dev/mipt-hack-01/cloud-run/city-bot \
    --set-secrets=TELEGRAM_TOKEN=telegram-token:latest \
    --set-env-vars=PROJECT_ID=mipt-hack-01 \
    --memory 1Gi \
    --region us-central1 \
    --allow-unauthenticated
