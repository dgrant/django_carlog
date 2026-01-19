#!/bin/bash
# Run the Django app locally in Docker with SQLite for testing
#
# Usage:
#   ./run-local-docker.sh          # Build and run
#   ./run-local-docker.sh --no-build   # Run without rebuilding

set -e

IMAGE_NAME="django-carlog"
CONTAINER_NAME="carlog-test"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DATA_DIR="$SCRIPT_DIR/data"
PORT=8000
DJANGO_SETTINGS_MODULE=django_carlog.settings.production

# Create data directory for persistent SQLite database
mkdir -p "$DATA_DIR"

# Stop existing container if running
docker stop "$CONTAINER_NAME" 2>/dev/null || true

# Build the image unless --no-build is passed
if [[ "$1" != "--no-build" ]]; then
  echo "Building Docker image..."
  docker build -t "$IMAGE_NAME" .
fi

# Run the container
echo "Starting container..."
docker run --rm -d --name "$CONTAINER_NAME" \
  -e SECRET_KEY="local-testing-secret-key-not-for-production" \
  -e DATABASE_URL="sqlite:////app/data/db.sqlite3" \
  -e ALLOWED_HOSTS="localhost,127.0.0.1" \
  -e DEBUG=true \
  -e DJANGO_SETTINGS_MODULE="$DJANGO_SETTINGS_MODULE" \
  -e PORT="$PORT" \
  -v "$DATA_DIR:/app/data" \
  -p "$PORT:$PORT" \
  "$IMAGE_NAME" \
  sh -c "uv run python manage.py migrate && uv run gunicorn --bind 0.0.0.0:\$PORT django_carlog.wsgi:application"

echo ""
echo "Container started! View logs with: docker logs -f $CONTAINER_NAME"
echo "API available at: http://localhost:$PORT/trips/api/"
echo "Stop with: docker stop $CONTAINER_NAME"
