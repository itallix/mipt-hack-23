#!/usr/bin/env bash
set -eu

default_token=$(gcloud secrets versions access latest --secret=telegram-token)

if [ "$1" = "set" ]; then    
    default_url=$(gcloud run services describe city-bot --format="value(status.url)")
    url=${2:-$default_url}
    token=${3:-$default_token}
    curl "https://api.telegram.org/bot${token}/setWebhook?url=${url}"
elif [ "$1" = "delete" ]; then
    token={$2:-$default_token}
    curl "https://api.telegram.org/bot${token}/deleteWebhook"
else
    echo "Unsupported command."
fi
