#!/bin/bash

# AWS Training Certificate System - Production Startup
echo "🚀 Starting AWS Training Certificate System (Production)..."

# Set production environment
export FLASK_ENV=production
export PORT=5001
export CERTIFICATE_DIR=/tmp/certificates
export EXCEL_DIR=/tmp/excel-data

# Create directories
mkdir -p $CERTIFICATE_DIR $EXCEL_DIR

# Start with gunicorn
echo "📊 Starting Gunicorn on port $PORT..."
exec gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 120 --access-logfile - --error-logfile - app_aws:application
