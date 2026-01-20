#!/bin/bash
set -euo pipefail

# Rollback to a previous version
# Usage: ./rollback.sh <version>

IMAGE="${IMAGE:-ghcr.io/dgrant/carlog}"

if [ -z "${1:-}" ]; then
    echo "Usage: ./rollback.sh <version>"
    echo ""
    echo "Available local images:"
    docker images "${IMAGE}" --format "table {{.Tag}}\t{{.CreatedAt}}\t{{.Size}}"
    exit 1
fi

VERSION="$1"

echo "=== Rolling back to version: $VERSION ==="

# Use the same deploy script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
"${SCRIPT_DIR}/deploy.sh" "$VERSION"
