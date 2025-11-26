#!/bin/bash
# AWS Training Certificate System - AWS Deployment Script

echo "�� Deploying AWS Training Certificate System to AWS..."

# Install dependencies
pip install -r requirements.txt

# Create AWS directories
mkdir -p /tmp/certificates /tmp/excel-data

# Start production server
echo "📊 Starting production server..."
gunicorn --bind 0.0.0.0:5000 --workers 4 --timeout 120 app_aws:application
