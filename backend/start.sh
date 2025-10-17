#!/bin/bash

# Start script for Render deployment
echo "Starting Cognivasc Backend..."

# Set environment variables
export PYTHONUNBUFFERED=1
export PYTHONDONTWRITEBYTECODE=1

# Create necessary directories
mkdir -p logs cache

# Start the application
python app.py
