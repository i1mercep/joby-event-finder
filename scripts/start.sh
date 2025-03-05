#!/bin/bash
BIND=${BIND-0.0.0.0:8000}

HOST=$(echo $BIND | cut -f1 -d:)
PORT=$(echo $BIND | cut -f2 -d:)

uvicorn src.main:app --reload --host $HOST --port $PORT --log-level ${LOG_LEVEL:-info}
