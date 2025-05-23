#!/bin/sh

# Container name to monitor
CONTAINER_NAME="photo-indexer-job"

# Check if the container is already running
if docker ps --filter "name=$CONTAINER_NAME" --format '{{.Names}}' | grep -q "$CONTAINER_NAME"; then
    echo "[INFO] Container already running. Skipping launch."
    exit 0
fi

# Start the container (in background, with name)
docker run --rm \
  --name $CONTAINER_NAME \
  -e SOURCE_DIR=/data/photos \
  -e TARGET_DIR=/data/output \
  -e TZ=Europe/Warsaw \
  -v /volume1/photos:/data/photos \
  -v /volume1/output:/data/output \
  -u 1026:100 \
  photo-indexer

echo "[INFO] Container started."
