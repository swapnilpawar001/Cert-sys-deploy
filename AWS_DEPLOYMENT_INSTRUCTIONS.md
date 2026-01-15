# AWS Deployment Instructions - Certificate System

## 🚀 Method 1: AWS Elastic Beanstalk (CLI)

### Prerequisites
```bash
# Install AWS CLI and EB CLI
pip install awsebcli
aws configure
```

### Deployment Steps
```bash
# 1. Initialize EB application
eb init certificate-system --platform python-3.9 --region us-east-1

# 2. Create environment
eb create production --instance-type t3.small

# 3. Set environment variables
eb setenv SECRET_KEY="your-super-secret-key-$(date +%s)" \
         ADMIN_USERNAME="admin" \
         ADMIN_PASSWORD="SecurePass123!" \
         FLASK_ENV="production" \
         FLASK_DEBUG="False"

# 4. Deploy
eb deploy

# 5. Open application
eb open
```

### Deletion Steps
```bash
# 1. Terminate environment
eb terminate production

# 2. Delete application (optional)
aws elasticbeanstalk delete-application --application-name certificate-system
```

## 🖥️ Method 1: AWS Elastic Beanstalk (Console)

### Step 1: Prepare Application
1. Create deployment package:
```bash
zip -r certificate-system.zip . -x "*.git*" "__pycache__/*" "*.pyc" ".env"
```

### Step 2: Console Deployment
1. Go to **AWS Elastic Beanstalk Console**
2. Click **Create Application**
3. Application name: `certificate-system`
4. Platform: **Python 3.9**
5. Upload `certificate-system.zip`
6. Click **Create Application**

### Step 3: Configure Environment
1. Go to **Configuration** → **Software**
2. Add environment variables:
   - `SECRET_KEY`: Generate strong key
   - `ADMIN_USERNAME`: Your admin username
   - `ADMIN_PASSWORD`: Strong password
   - `FLASK_ENV`: production
   - `FLASK_DEBUG`: False

### Deletion Steps (Console)
1. Go to **Elastic Beanstalk Console**
2. Select your application
3. Click **Actions** → **Terminate Environment**
4. Confirm termination
5. Delete application if no longer needed

## 🐳 Method 2: AWS ECS with Fargate (CLI)

### Prerequisites
```bash
# Install Docker and AWS CLI
aws configure
```

### Deployment Steps
```bash
# 1. Create ECR repository
aws ecr create-repository --repository-name certificate-system

# 2. Get login token
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

# 3. Build and push image
docker build -t certificate-system .
docker tag certificate-system:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/certificate-system:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/certificate-system:latest

# 4. Create ECS cluster
aws ecs create-cluster --cluster-name certificate-cluster

# 5. Create task definition (see task-definition.json below)
aws ecs register-task-definition --cli-input-json file://task-definition.json

# 6. Create service
aws ecs create-service --cluster certificate-cluster --service-name certificate-service --task-definition certificate-task --desired-count 1 --launch-type FARGATE --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx],securityGroups=[sg-xxx],assignPublicIp=ENABLED}"
```

### Deletion Steps
```bash
# 1. Delete service
aws ecs update-service --cluster certificate-cluster --service certificate-service --desired-count 0
aws ecs delete-service --cluster certificate-cluster --service certificate-service

# 2. Delete cluster
aws ecs delete-cluster --cluster certificate-cluster

# 3. Delete ECR repository
aws ecr delete-repository --repository-name certificate-system --force

# 4. Deregister task definitions
aws ecs list-task-definitions --family-prefix certificate-task --query 'taskDefinitionArns[]' --output text | xargs -I {} aws ecs deregister-task-definition --task-definition {}
```

## 🖥️ Method 2: AWS ECS (Console)

### Step 1: Create ECR Repository
1. Go to **Amazon ECR Console**
2. Click **Create repository**
3. Name: `certificate-system`
4. Click **Create repository**

### Step 2: Push Docker Image
```bash
# Follow push commands from ECR console
```

### Step 3: Create ECS Service
1. Go to **Amazon ECS Console**
2. Create **Cluster** → **Fargate**
3. Create **Task Definition**:
   - Family: `certificate-task`
   - CPU: 512, Memory: 1024
   - Container image: Your ECR URI
   - Port: 5000
4. Create **Service** using the task definition

### Deletion Steps (Console)
1. Go to **ECS Console**
2. Select cluster → **Services**
3. Select service → **Delete**
4. Go to **Clusters** → **Delete cluster**
5. Go to **ECR** → Select repository → **Delete**
6. Go to **Task Definitions** → Deregister all revisions

## ☁️ Method 3: AWS EC2 (CLI)

### Launch Instance
```bash
# 1. Create key pair
aws ec2 create-key-pair --key-name certificate-key --query 'KeyMaterial' --output text > certificate-key.pem
chmod 400 certificate-key.pem

# 2. Launch instance
aws ec2 run-instances --image-id ami-0abcdef1234567890 --count 1 --instance-type t3.small --key-name certificate-key --security-group-ids sg-xxx --subnet-id subnet-xxx

# 3. Get instance IP
aws ec2 describe-instances --query 'Reservations[*].Instances[*].PublicIpAddress'
```

### Deploy Application
```bash
# 1. Copy files to EC2
scp -i certificate-key.pem -r . ec2-user@<instance-ip>:/home/ec2-user/certificate-system/

# 2. SSH and setup
ssh -i certificate-key.pem ec2-user@<instance-ip>
sudo yum update -y
sudo yum install docker -y
sudo service docker start
sudo usermod -a -G docker ec2-user

# 3. Run application
cd certificate-system
sudo docker build -t certificate-system .
sudo docker run -d -p 80:5000 --name cert-app certificate-system
```

### Deletion Steps
```bash
# 1. Stop and remove container
sudo docker stop cert-app
sudo docker rm cert-app

# 2. Remove image
sudo docker rmi certificate-system

# 3. Terminate EC2 instance
aws ec2 terminate-instances --instance-ids i-1234567890abcdef0

# 4. Delete key pair
aws ec2 delete-key-pair --key-name certificate-key
rm certificate-key.pem
```

## 🖥️ Method 3: AWS EC2 (Console)

### Step 1: Launch Instance
1. Go to **EC2 Console**
2. Click **Launch Instance**
3. Choose **Amazon Linux 2 AMI**
4. Instance type: **t3.small**
5. Configure security group (ports 22, 80, 443)
6. Launch with key pair

### Step 2: Setup Application
```bash
# SSH to instance and run setup commands above
```

### Deletion Steps (Console)
1. Go to **EC2 Console**
2. Select instance → **Instance State** → **Terminate**
3. Go to **Key Pairs** → Select → **Delete**
4. Go to **Security Groups** → Delete custom security group
5. Clean up any associated resources (EBS volumes, Elastic IPs)

## 🔧 Required Configurations

### Environment Variables (All Methods)
```bash
SECRET_KEY=your-super-secret-key-change-this
ADMIN_USERNAME=your-admin-username
ADMIN_PASSWORD=your-secure-password
FLASK_ENV=production
FLASK_DEBUG=False
```

### Security Groups
- **Inbound Rules**:
  - HTTP (80) from 0.0.0.0/0
  - HTTPS (443) from 0.0.0.0/0
  - SSH (22) from your IP only

### SSL Certificate
1. **AWS Certificate Manager**:
   - Request certificate for your domain
   - Validate via DNS/Email
2. **Application Load Balancer**:
   - Create ALB
   - Add SSL certificate
   - Forward HTTP to HTTPS

## 📊 Monitoring Setup

### CloudWatch Logs
```bash
# Install CloudWatch agent on EC2
sudo yum install amazon-cloudwatch-agent -y
```

### Health Checks
- **Endpoint**: `/api/check-status`
- **Expected**: 200 status code
- **Interval**: 30 seconds

## 🔒 Security Hardening

### 1. Update Default Credentials
```bash
# Generate strong secret key
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 2. Enable HTTPS Only
```python
# Add to app.py
from flask_talisman import Talisman
Talisman(app, force_https=True)
```

### 3. Database Migration (Recommended)
- Replace file-based storage with RDS
- Use Redis for session management
- Implement proper user authentication

## 🚨 Critical Precautions

### Before Deployment
- [ ] Change all default passwords
- [ ] Set strong SECRET_KEY
- [ ] Upload certificate template to `data/templates/`
- [ ] Test locally with production settings
- [ ] Backup existing data

### After Deployment
- [ ] Configure SSL certificate
- [ ] Set up monitoring and alerts
- [ ] Configure automated backups
- [ ] Test all functionality
- [ ] Set up log rotation

### Ongoing Maintenance
- [ ] Regular security updates
- [ ] Monitor disk usage
- [ ] Backup certificate data
- [ ] Review access logs
- [ ] Update dependencies

## 🔄 Backup Strategy

### Data Backup
```bash
# Backup data directory
aws s3 sync /app/data s3://your-backup-bucket/data/$(date +%Y%m%d)/
```

### Database Backup (if migrated)
```bash
# RDS automated backups
aws rds create-db-snapshot --db-instance-identifier mydb --db-snapshot-identifier mydb-snapshot-$(date +%Y%m%d)
```

## 🆘 Troubleshooting

### Common Issues
1. **Template not found**: Ensure `certificate-template.png` exists
2. **Permission denied**: Check file permissions and IAM roles
3. **Memory issues**: Increase instance size or optimize code
4. **SSL errors**: Verify certificate configuration

### Debug Commands
```bash
# Check application logs
eb logs
docker logs cert-app
tail -f /var/log/application.log

# Test endpoints
curl http://your-domain/api/check-status
curl -X POST http://your-domain/api/authenticate
```

## 📞 Support Checklist

Before seeking help:
- [ ] Check application logs
- [ ] Verify all environment variables
- [ ] Test with minimal configuration
- [ ] Check AWS service limits
- [ ] Verify IAM permissions