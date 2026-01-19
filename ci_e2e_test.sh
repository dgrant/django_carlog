#!/bin/sh
set -e

# Install Playwright browser (--with-deps installs system dependencies, needs sudo in CI)
if [ "$CI" = "true" ]; then
    uv run playwright install --with-deps chromium
else
    uv run playwright install chromium
fi

uv run pytest e2e/ --browser chromium -v
