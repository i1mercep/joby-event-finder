#!/bin/bash

# Exit immediately if a pipeline exits with a non-zero status.
set -e

export PYTHONUNBUFFERED=1

# This only exists in development because(mounted from local filesystem)
set -a # make next variables exported
if [ -d "envs/" ]; then
    # Load all the envs
    source <(cat envs/*.env 2> /dev/null)
fi

source /venv/bin/activate
echo "Making migrations..."
alembic upgrade head

# Path to the Alembic versions directory
VERSIONS_DIR="src/migrations/versions"

# Ensure the versions directory exists
if [ ! -d "$VERSIONS_DIR" ]; then
    echo "Error: Versions directory not found: $VERSIONS_DIR"
    exit 1
fi

# Check if a migration message is provided as an argument
if [ -z "$1" ]; then
    echo "Usage: $0 \"Migration message\""
    exit 1
fi

# Use the first argument as the migration message
MIGRATION_MESSAGE="$1"

# Find the latest version number by looking for files starting with digits
LATEST_VERSION=$(ls "$VERSIONS_DIR" | grep -E '^[0-9]{4}_' | sort -n | tail -1 | awk -F'_' '{print $1}')

# If no version exists, start with 0001
if [ -z "$LATEST_VERSION" ]; then
    NEXT_VERSION="0001"
else
    NEXT_VERSION=$(printf "%04d" $((10#$LATEST_VERSION + 1)))
fi

# Generate the Alembic revision with the new sequential version ID and message
alembic revision --rev-id="$NEXT_VERSION" -m "$MIGRATION_MESSAGE" --autogenerate

echo "Migration $NEXT_VERSION created successfully: \"$MIGRATION_MESSAGE\""
