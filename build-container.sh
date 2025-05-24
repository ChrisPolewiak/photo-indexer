#!/bin/bash

# Project directory where docker-compose.yml and git repo are located
PROJECT_DIR="/volume1/docker/photo-indexer"

# Name of the Docker Compose service/container
CONTAINER_NAME="photo-indexer"

# Navigate to the project directory
cd "$PROJECT_DIR" || {
  echo "[ERROR] Failed to access project directory: $PROJECT_DIR"
  exit 1
}

# Check if container exists (running or not)
if docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
  echo "[INFO] Stopping and removing existing container: ${CONTAINER_NAME}"
  docker stop "$CONTAINER_NAME" >/dev/null 2>&1
  docker rm "$CONTAINER_NAME" >/dev/null 2>&1
fi

echo "[INFO] Building and starting container: ${CONTAINER_NAME}"
docker-compose build
docker-compose up -d
