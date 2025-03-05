#!/bin/bash

# Exit immediately if a pipeline exits with a non-zero status.
set -e

export PYTHONUNBUFFERED=1

# if theres a virtual env activate it
if [ -d "/venv/" ]; then
    source /venv/bin/activate
fi

echo "Applying migrations..."
alembic upgrade head
echo "Migrations applied!"

echo "Initiating db..."
python -m src.init_db
echo "Initiating db done!"

if [ -n "$DEVELOPMENT" ]; then
    export PYTHONDONTWRITEBYTECODE=1
    export PYTHONASYNCIODEBUG=true

    # Extensions to watch for changes (source code and environment)
    WE_EXT=py,env

    # Start watching file extensions and run 'start.sh' which writes to stdout what filed changed
    watchexec -n -e $WE_EXT -r -- "$@"
else
    # eval $(aws-env)
    exec "$@"
fi
