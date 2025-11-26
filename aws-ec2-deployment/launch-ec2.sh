#!/bin/bash
# AWS EC2 Instance Launch Script

echo "🚀 Launching AWS EC2 Instance for Certificate System..."

# Configuration
INSTANCE_NAME="aws-certificate-system"
INSTANCE_TYPE="t3.micro"
AMI_ID="ami-0c02fb55956c7d316"  # Amazon Linux 2
KEY_NAME="aws-certificate-key"
SECURITY_GROUP="aws-certificate-sg"

# Create key pair (if not exists)
aws ec2 create-key-pair --key-name $KEY_NAME --query 'KeyMaterial' --output text > $KEY_NAME.pem
chmod 400 $KEY_NAME.pem

# Create security group
SECURITY_GROUP_ID=$(aws ec2 create-security-group \
    --group-name $SECURITY_GROUP \
    --description "Security group for AWS Certificate System" \
    --query 'GroupId' --output text)

# Configure security group rules
aws ec2 authorize-security-group-ingress \
    --group-id $SECURITY_GROUP_ID \
    --protocol tcp \
    --port 5001 \
    --cidr 0.0.0.0/0

aws ec2 authorize-security-group-ingress \
    --group-id $SECURITY_GROUP_ID \
    --protocol tcp \
    --port 22 \
    --cidr 0.0.0.0/0

# Launch EC2 instance
INSTANCE_ID=$(aws ec2 run-instances \
    --image-id $AMI_ID \
    --instance-type $INSTANCE_TYPE \
    --key-name $KEY_NAME \
    --security-group-ids $SECURITY_GROUP_ID \
    --tag-specifications "ResourceType=instance,Tags=[{Key=Name,Value=$INSTANCE_NAME}]" \
    --user-data file://user-data.sh \
    --query 'Instances[0].InstanceId' --output text)

echo "✅ EC2 Instance launched: $INSTANCE_ID"
echo "⏳ Waiting for instance to be running..."

# Wait for instance to be running
aws ec2 wait instance-running --instance-ids $INSTANCE_ID

# Get public IP
PUBLIC_IP=$(aws ec2 describe-instances \
    --instance-ids $INSTANCE_ID \
    --query 'Reservations[0].Instances[0].PublicIpAddress' \
    --output text)

echo "🌐 Instance Public IP: $PUBLIC_IP"
echo "🔗 Application will be available at: http://$PUBLIC_IP:5001"

# Save instance info
echo "INSTANCE_ID=$INSTANCE_ID" > instance-info.txt
echo "PUBLIC_IP=$PUBLIC_IP" >> instance-info.txt
echo "SECURITY_GROUP_ID=$SECURITY_GROUP_ID" >> instance-info.txt

echo "✅ Instance info saved to instance-info.txt"
