# Claude Code Instructions

## Before Committing

Always run full lint checks before committing to ensure CI will pass:

```bash
uv run ruff check .
uv run ruff format --check .
```

Pre-commit hooks only run on changed files, but CI runs on all files. Running the full check locally catches issues that pre-commit might miss.

## Running Tests

```bash
uv run pytest trips/tests/ -v
```

## Development Setup

```bash
uv sync --all-extras
```
