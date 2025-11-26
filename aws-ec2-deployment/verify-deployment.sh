#!/bin/bash
# Verify AWS Deployment

echo "🔍 Verifying AWS Certificate System Deployment..."

# Check if instance is running
if [ -f instance-info.txt ]; then
    source instance-info.txt
    
    echo "📋 Instance ID: $INSTANCE_ID"
    echo "🌐 Public IP: $PUBLIC_IP"
    
    # Check instance status
    aws ec2 describe-instances --instance-ids $INSTANCE_ID --query 'Reservations[0].Instances[0].State.Name' --output text
    
    # Test application
    echo "🧪 Testing application..."
    curl -s http://$PUBLIC_IP:5001/api/check-status && echo "✅ Application responding" || echo "❌ Application not responding"
    
else
    echo "❌ Instance info not found. Run launch-ec2.sh first."
fi
