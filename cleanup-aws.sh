#!/bin/bash

# AWS Certificate System - Complete Cleanup Script
echo "🗑️  AWS Certificate System Cleanup"
echo "=================================="

# Function to confirm deletion
confirm_deletion() {
    read -p "⚠️  This will DELETE all resources. Are you sure? (yes/no): " confirm
    if [ "$confirm" != "yes" ]; then
        echo "❌ Cleanup cancelled"
        exit 1
    fi
}

# Method selection
echo "Select deployment method to cleanup:"
echo "1) Elastic Beanstalk"
echo "2) ECS Fargate"
echo "3) EC2"
echo "4) All methods"
read -p "Enter choice (1-4): " method

case $method in
    1)
        echo "🧹 Cleaning up Elastic Beanstalk..."
        confirm_deletion
        
        # Terminate EB environment
        eb terminate production --force
        
        # Delete application
        aws elasticbeanstalk delete-application --application-name certificate-system
        
        echo "✅ Elastic Beanstalk cleanup complete"
        ;;
        
    2)
        echo "🧹 Cleaning up ECS Fargate..."
        confirm_deletion
        
        # Delete ECS service
        aws ecs update-service --cluster certificate-cluster --service certificate-service --desired-count 0
        aws ecs delete-service --cluster certificate-cluster --service certificate-service --force
        
        # Delete cluster
        aws ecs delete-cluster --cluster certificate-cluster
        
        # Delete ECR repository
        aws ecr delete-repository --repository-name certificate-system --force
        
        # Deregister task definitions
        aws ecs list-task-definitions --family-prefix certificate-task --query 'taskDefinitionArns[]' --output text | xargs -I {} aws ecs deregister-task-definition --task-definition {}
        
        echo "✅ ECS Fargate cleanup complete"
        ;;
        
    3)
        echo "🧹 Cleaning up EC2..."
        confirm_deletion
        
        # Get instance ID
        read -p "Enter EC2 instance ID (i-xxxxx): " instance_id
        
        # Stop and remove Docker container
        echo "Stopping Docker container..."
        ssh -i certificate-key.pem ec2-user@$(aws ec2 describe-instances --instance-ids $instance_id --query 'Reservations[0].Instances[0].PublicIpAddress' --output text) "sudo docker stop cert-app; sudo docker rm cert-app; sudo docker rmi certificate-system"
        
        # Terminate instance
        aws ec2 terminate-instances --instance-ids $instance_id
        
        # Delete key pair
        aws ec2 delete-key-pair --key-name certificate-key
        rm -f certificate-key.pem
        
        echo "✅ EC2 cleanup complete"
        ;;
        
    4)
        echo "🧹 Cleaning up ALL resources..."
        confirm_deletion
        
        # Cleanup Elastic Beanstalk
        echo "Cleaning Elastic Beanstalk..."
        eb terminate production --force 2>/dev/null || true
        aws elasticbeanstalk delete-application --application-name certificate-system 2>/dev/null || true
        
        # Cleanup ECS
        echo "Cleaning ECS..."
        aws ecs update-service --cluster certificate-cluster --service certificate-service --desired-count 0 2>/dev/null || true
        aws ecs delete-service --cluster certificate-cluster --service certificate-service --force 2>/dev/null || true
        aws ecs delete-cluster --cluster certificate-cluster 2>/dev/null || true
        aws ecr delete-repository --repository-name certificate-system --force 2>/dev/null || true
        
        # Cleanup EC2 (requires manual instance ID input)
        echo "For EC2 cleanup, run this script again with option 3"
        
        echo "✅ Bulk cleanup complete"
        ;;
        
    *)
        echo "❌ Invalid choice"
        exit 1
        ;;
esac

# Additional cleanup
echo ""
echo "🧹 Additional cleanup recommendations:"
echo "- Check CloudWatch logs and delete log groups"
echo "- Remove any custom security groups"
echo "- Delete unused EBS volumes"
echo "- Remove Route 53 records if configured"
echo "- Delete SSL certificates from ACM if not needed"
echo "- Check S3 buckets for any stored data"

echo ""
echo "✅ Cleanup script completed!"