#!/bin/bash

# AWS Training Certificate System - Deployment Script
echo "🚀 Deploying AWS Training Certificate System..."

# Kill any existing processes on port 5001
pkill -f "gunicorn.*5001" 2>/dev/null

# Install dependencies
pip install -r requirements.txt --quiet

# Copy application files from parent directory
cp ../app_aws.py .
cp -r ../templates .
cp -r ../static .
cp -r ../data .

# Create directories
mkdir -p /tmp/certificates /tmp/excel-data

# Start the application on different port to avoid conflicts
echo "📊 Starting with Gunicorn on port 5001..."
gunicorn --bind 0.0.0.0:5001 --workers 2 --timeout 120 app_aws:application
