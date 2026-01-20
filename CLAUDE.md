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

## GitHub PR Workflow

After addressing PR review comments, always resolve the conversation on GitHub. Use the GitHub API to mark comments as resolved:

```bash
gh api graphql -f query='mutation { resolveReviewThread(input: {threadId: "THREAD_ID"}) { thread { isResolved } } }'
```

To find thread IDs, fetch PR review threads first:

```bash
gh api graphql -f query='query { repository(owner: "dgrant", name: "carlog") { pullRequest(number: PR_NUMBER) { reviewThreads(first: 50) { nodes { id isResolved comments(first: 1) { nodes { body } } } } } } }'
```
