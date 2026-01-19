#!/bin/bash
# Script to create a new git worktree with full local development setup
# Usage: source new_worktree.sh <branch_name>
#
# This script must be SOURCED (not executed) to allow cd into the new worktree.

# Store the source directory
SOURCE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_NAME="carlog"

# Check if branch name is provided
if [ -z "$1" ]; then
    echo "Error: Branch name is required"
    echo "Usage: source new_worktree.sh <branch_name>"
    return 1 2>/dev/null || exit 1
fi

BRANCH_NAME="$1"
WORKTREE_DIR="../${REPO_NAME}_${BRANCH_NAME}"

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "Error: Not in a git repository"
    return 1 2>/dev/null || exit 1
fi

# Check if local.py exists (required)
if [ ! -f "$SOURCE_DIR/django_carlog/settings/local.py" ]; then
    echo "Error: django_carlog/settings/local.py does not exist"
    echo "Please create it from local.py.example first"
    return 1 2>/dev/null || exit 1
fi

# Check if worktree directory already exists
if [ -d "$SOURCE_DIR/$WORKTREE_DIR" ]; then
    echo "Error: Worktree directory already exists: $WORKTREE_DIR"
    return 1 2>/dev/null || exit 1
fi

# Check if branch already exists
if git show-ref --verify --quiet "refs/heads/$BRANCH_NAME"; then
    echo "Branch '$BRANCH_NAME' already exists. Using existing branch."
    git worktree add "$WORKTREE_DIR" "$BRANCH_NAME"
else
    echo "Creating new branch '$BRANCH_NAME' and worktree..."
    git worktree add -b "$BRANCH_NAME" "$WORKTREE_DIR"
fi

if [ $? -ne 0 ]; then
    echo "Error: Failed to create worktree"
    return 1 2>/dev/null || exit 1
fi

# Get absolute path to worktree
WORKTREE_ABS="$(cd "$SOURCE_DIR/$WORKTREE_DIR" && pwd)"

echo "Copying local.py to new worktree..."
cp "$SOURCE_DIR/django_carlog/settings/local.py" "$WORKTREE_ABS/django_carlog/settings/local.py"

echo "Changing to new worktree directory..."
cd "$WORKTREE_ABS"

# Unset VIRTUAL_ENV to avoid conflicts with any active environment from the source repo
unset VIRTUAL_ENV

echo "Installing dependencies with uv..."
uv sync

echo "Installing pre-commit hooks..."
uv run pre-commit install

echo "Creating .env file..."
echo 'DJANGO_SETTINGS_MODULE=django_carlog.settings.local' > .env

echo ""
echo "====================================="
echo "Worktree setup complete!"
echo "====================================="
echo "Location: $WORKTREE_ABS"
echo "Branch: $BRANCH_NAME"
echo ""
echo "You can now run:"
echo "  uv run ./manage.py runserver"
echo ""
echo "Or activate the virtualenv:"
echo "  source .venv/bin/activate"
echo "  ./manage.py runserver"
echo ""
