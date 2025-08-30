#!/bin/bash
# Script to start the Uvicorn server for the backend

cd "$(dirname "$0")/.."  # Move to project root

# Read only API_HOST and API_PORT from config/.env
API_HOST=$(grep '^API_HOST=' src/config/.env | cut -d '=' -f2-)
API_PORT=$(grep '^API_PORT=' src/config/.env | cut -d '=' -f2-)

# Start Uvicorn server using API_HOST and API_PORT from .env
uv run uvicorn main:app --host "$API_HOST" --port "$API_PORT" --reload
