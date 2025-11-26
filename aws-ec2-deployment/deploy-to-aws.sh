#!/bin/bash
# AWS Training Certificate System - EC2 Deployment Script

echo "🚀 Deploying to AWS EC2..."

# Update system
sudo yum update -y

# Install Python and pip
sudo yum install python3 python3-pip -y

# Install dependencies
pip3 install -r requirements.txt

# Create AWS directories
sudo mkdir -p /var/log/aws-certificate-system
sudo mkdir -p /opt/aws-certificate-system

# Copy application files
sudo cp -r . /opt/aws-certificate-system/
cd /opt/aws-certificate-system

# Set permissions
sudo chmod +x start_production.sh

# Create systemd service
sudo tee /etc/systemd/system/aws-certificate.service << 'SERVICE'
[Unit]
Description=AWS Training Certificate System
After=network.target

[Service]
Type=simple
User=ec2-user
WorkingDirectory=/opt/aws-certificate-system
ExecStart=/usr/bin/python3 app_aws.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
SERVICE

# Enable and start service
sudo systemctl enable aws-certificate.service
sudo systemctl start aws-certificate.service

echo "✅ AWS deployment complete!"
echo "🌐 Application should be running on port 5001"
