#!/bin/bash
set -euo pipefail

# Configuration
IMAGE="${IMAGE:-ghcr.io/dgrant/carlog}"
CONTAINER_NAME="${CONTAINER_NAME:-carlog_prod}"
ENV_FILE="${ENV_FILE:-/home/david/.env.carlog.prod}"
STATIC_DIR="${STATIC_DIR:-/home/david/carlog_prod/static}"
PORT="${PORT:-8002}"

# Get version from argument or default to latest
VERSION="${1:-latest}"

echo "=== Deploying Carlog version: $VERSION ==="
echo "Container: $CONTAINER_NAME"
echo "Port: $PORT"

# Pull new image
echo ">>> Pulling image ${IMAGE}:${VERSION}..."
docker pull "${IMAGE}:${VERSION}"

# Collect static files (one-off container with volume mount)
echo ">>> Collecting static files..."
docker run --rm \
    -v "${STATIC_DIR}:/app/static" \
    --env-file "${ENV_FILE}" \
    -e DJANGO_SETTINGS_MODULE=django_carlog.settings.docker \
    "${IMAGE}:${VERSION}" \
    python manage.py collectstatic --noinput

# Run migrations (one-off container)
echo ">>> Running migrations..."
docker run --rm \
    --network host \
    --env-file "${ENV_FILE}" \
    -e DJANGO_SETTINGS_MODULE=django_carlog.settings.docker \
    "${IMAGE}:${VERSION}" \
    python manage.py migrate --noinput

# Stop old container
echo ">>> Stopping old container..."
docker stop "${CONTAINER_NAME}" 2>/dev/null || true
docker rm "${CONTAINER_NAME}" 2>/dev/null || true

# App version for display
APP_VERSION="${VERSION}"

# Start new container
echo ">>> Starting new container..."
docker run -d \
    --name "${CONTAINER_NAME}" \
    --restart unless-stopped \
    --network host \
    --env-file "${ENV_FILE}" \
    -e DJANGO_SETTINGS_MODULE=django_carlog.settings.docker \
    -e APP_VERSION="${APP_VERSION}" \
    "${IMAGE}:${VERSION}" \
    python -m gunicorn --bind "127.0.0.1:${PORT}" --workers 3 --threads 2 django_carlog.wsgi:application

# Check health
echo ">>> Checking application health..."
MAX_ATTEMPTS=12
SLEEP_BETWEEN=5

for attempt in $(seq 1 $MAX_ATTEMPTS); do
    if curl -fsS "http://127.0.0.1:${PORT}/health/" > /dev/null 2>&1; then
        echo "=== Deployment successful! Application is healthy. ==="
        docker ps --filter "name=${CONTAINER_NAME}"
        echo ">>> Cleaning up old Docker images..."
        docker image prune -af
        exit 0
    fi
    echo ">>> Health check attempt $attempt/$MAX_ATTEMPTS failed. Retrying in ${SLEEP_BETWEEN}s..."
    sleep "$SLEEP_BETWEEN"
done

echo "=== ERROR: Application did not become healthy ==="
docker logs "${CONTAINER_NAME}" --tail 50
exit 1
