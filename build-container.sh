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

# Build and start the updated container
echo "[INFO] Updates detected. Rebuilding and starting container..."
docker-compose build && docker-compose up
