#!/bin/bash
dirs="src tests"

# Exit immediately if a pipeline exits with a non-zero status.
set -e

# no buffering of log messages, all goes straight to stdout
export PYTHONUNBUFFERED=1

echo "===== format ====="
ruff format $dirs --config pyproject.toml --preview
echo "===== lint ====="
ruff check $dirs --config pyproject.toml --preview --fix --show-fixes 
