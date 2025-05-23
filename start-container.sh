#!/bin/sh

# Nazwa kontenera do monitorowania
CONTAINER_NAME="photo-indexer-job"

# Sprawdź, czy kontener już działa
if docker ps --filter "name=$CONTAINER_NAME" --format '{{.Names}}' | grep -q "$CONTAINER_NAME"; then
    echo "[INFO] Container already running. Skipping launch."
    exit 0
fi

# Uruchom kontener (w tle, z nazwą)
docker run \
  --name $CONTAINER_NAME \
  -e SOURCE_DIR=/data/photos \
  -e TARGET_DIR=/data/output \
  -e TZ=Europe/Warsaw \
  -v /volume1/photos:/data/photos \
  -v /volume1/output:/data/output \
  -u 1026:100 \
  photo-indexer

echo "[INFO] Container started."

# Opcjonalnie: usuwaj kontener po zakończeniu
# Można dodać np. do innego crona:
# docker rm -f $CONTAINER_NAME
