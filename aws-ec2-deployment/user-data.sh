#!/bin/bash
# EC2 Instance User Data - Runs on instance launch

# Update system
yum update -y

# Install Python and dependencies
yum install python3 python3-pip git -y

# Create application directory
mkdir -p /opt/aws-certificate-system
cd /opt/aws-certificate-system

# Install Python packages
pip3 install flask flask-cors pandas pillow openpyxl gunicorn python-dotenv

# Create placeholder files (will be replaced by deployment)
cat > app_aws.py << 'PLACEHOLDER'
# AWS app will be deployed here
PLACEHOLDER

# Create systemd service
cat > /etc/systemd/system/aws-certificate.service << 'SERVICE'
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

# Enable service
systemctl enable aws-certificate.service
systemctl start aws-certificate.service

# Install CloudWatch agent (optional)
wget https://s3.amazonaws.com/amazoncloudwatch-agent/amazon_linux/amd64/latest/amazon-cloudwatch-agent.rpm
rpm -U ./amazon-cloudwatch-agent.rpm

echo "✅ EC2 instance configured and ready for deployment"
