#!/bin/bash

# --- ENVIRONMENT VARIABLES CHECK ---

# Environment variable for login (your GitHub username)
if [ -z "$DOCKER_USERNAME" ]; then
    echo "Error: Environment variable DOCKER_USERNAME is not set (expected: your GitHub login)."
    exit 1
fi

# Environment variable for token (your Personal Access Token with write:packages)
if [ -z "$DOCKER_PASSWORD" ]; then
    echo "Error: Environment variable DOCKER_PASSWORD is not set (expected: PAT with write:packages permission)."
    exit 1
fi

# Get the current commit hash
COMMIT_HASH=$(git rev-parse --short HEAD)
REPO="ghcr.io/$DOCKER_USERNAME/vvpreo--forpedro"

# 1. Authenticate with GitHub Container Registry (GHCR)
echo "Authenticating with GitHub Container Registry (GHCR) using $DOCKER_USERNAME..."
# Login: DOCKER_USERNAME, Password: DOCKER_PASSWORD (via stdin for security)
echo $DOCKER_PASSWORD | docker login ghcr.io -u $DOCKER_USERNAME --password-stdin

if [ $? -ne 0 ]; then
    echo "❌ GHCR authentication error. Check DOCKER_PASSWORD (PAT) and permissions (write:packages)."
    exit 1
fi

# 2. Push the images to GitHub Registry
echo "Pushing Docker image to $REPO..."

# Push with unique tag (Commit Hash)
echo "Pushing $REPO:$COMMIT_HASH"
docker push $REPO:$COMMIT_HASH

# Push with :latest tag
echo "Pushing $REPO:latest"
docker push $REPO:latest

echo "✅ Push complete."