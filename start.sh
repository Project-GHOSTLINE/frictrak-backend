#!/bin/bash
echo "Starting FRICTRAK API..."
echo "PORT: ${PORT:-8080}"
exec gunicorn app:app --bind "0.0.0.0:${PORT:-8080}"
