# Claude Code Guidelines

## Before Committing

**Always run tests and lint checks before committing changes.**

```bash
# Run all tests
uv run pytest

# Run unit tests only (faster)
uv run pytest trips/tests/

# Run E2E tests only
uv run pytest e2e/
```

Tests must pass before any PR can be merged.

## Linting

Run pre-commit hooks and mypy before committing:

```bash
uv run pre-commit run --all-files
uv run mypy trips/ django_carlog/
```

Pre-commit hooks only run on changed files, but CI runs on all files. Running the full check locally catches issues that pre-commit might miss.

## Development Setup

```bash
uv sync --all-extras
```

## Deployment

The app deploys to Linode via Docker when changes are pushed to `master`. The CI/CD pipeline:

1. Runs lint checks (pre-commit + mypy)
2. Runs unit tests
3. Runs E2E tests
4. Builds and pushes Docker image to ghcr.io
5. Deploys to Linode via SSH
