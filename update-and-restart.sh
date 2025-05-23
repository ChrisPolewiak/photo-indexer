#!/bin/sh

# Project directory where docker-compose.yml and git repo are located
PROJECT_DIR="/volume1/docker/photo-indexer"

# Name of the Docker Compose service/container
CONTAINER_NAME="photo-indexer"

# Navigate to the project directory
cd "$PROJECT_DIR" || {
  echo "[ERROR] Failed to access project directory: $PROJECT_DIR"
  exit 1
}

# Check if the container is already running
if docker ps --filter "name=${CONTAINER_NAME}" --format '{{.Names}}' | grep -q "$CONTAINER_NAME"; then
  echo "[INFO] Container '${CONTAINER_NAME}' is already running. Skipping update."
  exit 0
fi

# Perform a git pull and capture the output
echo "[INFO] Checking for git updates..."
GIT_OUTPUT=$(git pull)
echo "$GIT_OUTPUT"

# Exit if no updates were pulled
if echo "$GIT_OUTPUT" | grep -q "Already up to date"; then
  echo "[INFO] No changes detected. Skipping build and deploy."
  exit 0
fi

# Build and start the updated container
echo "[INFO] Updates detected. Rebuilding and starting container..."
docker-compose build && docker-compose up
