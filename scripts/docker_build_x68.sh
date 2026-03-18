#!/bin/sh

#!/bin/bash

# Прерывать выполнение при любой ошибке
set -e

IMAGE_NAME="contract-risk-analyzer"
TAG="latest-x86"

COMMIT_HASH=$(git rev-parse --short HEAD)

# Сборка образа с явным указанием целевой платформы
echo "Building Docker image for linux/amd64 with tag: $COMMIT_HASH"
docker build --platform linux/amd64 \
  -t ghcr.io/vvpreo/vvpreo--forpedro:$COMMIT_HASH \
  -t ghcr.io/vvpreo/vvpreo--forpedro:latest \
  .

echo "DONE"