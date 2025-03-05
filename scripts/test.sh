#!/bin/bash
dirs="src"

# Exit immediately if a pipeline exits with a non-zero status.
set -e

# No buffering of log messages, all goes straight to stdout
export PYTHONUNBUFFERED=1

echo "===== format check ====="
ruff format $dirs --config pyproject.toml --preview --check

echo "====== lint check ======"
ruff check $dirs --config pyproject.toml --preview

# Run pytest with coverage report
coverage run --rcfile=pyproject.toml --source=$dirs -m pytest "${@:1}"
coverage report -m --rcfile=pyproject.toml
