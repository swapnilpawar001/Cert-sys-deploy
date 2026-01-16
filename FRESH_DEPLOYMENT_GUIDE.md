# Fresh Deployment Instructions - AWS Certificate System

## Prerequisites
- AWS CLI configured
- EB CLI installed
- Domain: awsmagicbus.me
- SSL Certificate ARN: arn:aws:acm:ap-northeast-2:903578657649:certificate/6754f66a-088a-4540-bad0-ee9c6d03bde0

---

## Step 1: Verify S3 Bucket Configuration (One-Time Setup)

```bash
# Check if bucket exists
aws s3 ls s3://elasticbeanstalk-ap-northeast-2-903578657649

# If bucket doesn't exist, create it
aws s3 mb s3://elasticbeanstalk-ap-northeast-2-903578657649

# Configure bucket permissions
aws s3api put-public-access-block \
  --bucket elasticbeanstalk-ap-northeast-2-903578657649 \
  --public-access-block-configuration "BlockPublicAcls=false,IgnorePublicAcls=false,BlockPublicPolicy=false,RestrictPublicBuckets=false"

aws s3api put-bucket-ownership-controls \
  --bucket elasticbeanstalk-ap-northeast-2-903578657649 \
  --ownership-controls Rules=[{ObjectOwnership=BucketOwnerPreferred}]
```

---

## Step 2: Initialize Elastic Beanstalk Application

```bash
# Navigate to project directory
cd /workspaces/Cert-sys-deploy

# Initialize EB application
eb init certificate-system --platform python-3.9 --region ap-northeast-2
```

---

## Step 3: Create Production Environment with Load Balancer

```bash
# Create environment with Application Load Balancer
eb create production --instance-type t3.small --elb-type application

# Wait for environment to be created (3-5 minutes)
# Monitor status
eb status
```

**Expected Output:**
- Status: Ready
- Health: Green
- CNAME: production.eba-XXXXXXX.ap-northeast-2.elasticbeanstalk.com

---

## Step 4: Get Load Balancer DNS Name

```bash
# Get load balancer ARN
LB_ARN=$(aws elasticbeanstalk describe-environment-resources \
  --environment-name production \
  --query 'EnvironmentResources.LoadBalancers[0].Name' \
  --output text)

# Get load balancer DNS name
LB_DNS=$(aws elbv2 describe-load-balancers \
  --load-balancer-arns $LB_ARN \
  --query 'LoadBalancers[0].DNSName' \
  --output text)

echo "Load Balancer DNS: $LB_DNS"
```

**Save this DNS name for Step 5!**

---

## Step 5: Update DNS Records at Domain Registrar

Go to your domain registrar and update the CNAME record:

```
Type: CNAME
Name: @ (or awsmagicbus.me)
Value: <Load Balancer DNS from Step 4>
Example: awseb--AWSEB-XXXXXXXXX-XXXXXXXXXX.ap-northeast-2.elb.amazonaws.com
```

**Note:** DNS propagation takes 5-30 minutes

---

## Step 6: Verify SSL Certificate (Already Created)

```bash
# Check certificate status
aws acm describe-certificate \
  --certificate-arn arn:aws:acm:ap-northeast-2:903578657649:certificate/6754f66a-088a-4540-bad0-ee9c6d03bde0 \
  --region ap-northeast-2 \
  --query 'Certificate.Status'
```

**Expected:** "ISSUED"

**If certificate doesn't exist or expired, create new one:**
```bash
aws acm request-certificate \
  --domain-name awsmagicbus.me \
  --validation-method DNS \
  --region ap-northeast-2
```

---

## Step 7: HTTPS Configuration (Automatic via .ebextensions)

The `.ebextensions/https-instance.config` file automatically configures:
- HTTPS listener on port 443
- SSL certificate attachment
- Security group rule for port 443

**No manual configuration needed!**

To verify:
```bash
# Check listeners
aws elbv2 describe-listeners \
  --load-balancer-arn $LB_ARN \
  --query 'Listeners[*].[Port,Protocol]' \
  --output table
```

**Expected Output:**
```
-------------------
|DescribeListeners|
+------+----------+
|  80  |  HTTP    |
|  443 |  HTTPS   |
+------+----------+
```

---

## Step 8: Verify Deployment

```bash
# Check environment status
eb status

# Test HTTP
curl -I http://awsmagicbus.me

# Test HTTPS (after DNS propagates)
curl -I https://awsmagicbus.me

# Check DNS propagation
curl -s "https://dns.google/resolve?name=awsmagicbus.me&type=CNAME" | python3 -m json.tool
```

---

## Step 9: Verify Application Access

**URLs:**
- HTTPS: https://awsmagicbus.me
- HTTP: http://awsmagicbus.me
- Admin: https://awsmagicbus.me/admin/login

**Default Credentials:**
- Username: admin
- Password: admin123

---

## Quick Reference Commands

### Deploy Updates
```bash
eb deploy
```

### Check Status
```bash
eb status
```

### View Logs
```bash
eb logs
```

### SSH to Instance
```bash
eb ssh
```

### Terminate Environment
```bash
eb terminate production --force
```

### Delete Application
```bash
aws elasticbeanstalk delete-application --application-name certificate-system
```

---

## Troubleshooting

### Issue: HTTPS Not Working

**Check 1: Verify HTTPS listener exists**
```bash
aws elbv2 describe-listeners --load-balancer-arn $LB_ARN
```

**Check 2: Verify port 443 is open**
```bash
SG_ID=$(aws elbv2 describe-load-balancers \
  --load-balancer-arns $LB_ARN \
  --query 'LoadBalancers[0].SecurityGroups[0]' \
  --output text)

aws ec2 describe-security-groups \
  --group-ids $SG_ID \
  --query 'SecurityGroups[0].IpPermissions[*].[FromPort,ToPort,IpProtocol]'
```

**Fix: Open port 443 manually if needed**
```bash
aws ec2 authorize-security-group-ingress \
  --group-id $SG_ID \
  --protocol tcp \
  --port 443 \
  --cidr 0.0.0.0/0
```

### Issue: DNS Not Resolving

**Wait 5-30 minutes for propagation**

**Check propagation:**
- https://dnschecker.org
- https://www.whatsmydns.net

**Verify CNAME record points to Load Balancer DNS (not EB environment URL)**

### Issue: Deployment Fails

**Check logs:**
```bash
eb logs
```

**Common fixes:**
- Verify S3 bucket permissions
- Check all dependencies in requirements.txt
- Ensure .ebextensions/https-instance.config exists

---

## Important Files

### .ebextensions/https-instance.config
Automatically configures HTTPS on deployment. **Do not delete!**

### requirements.txt
Must include:
- Flask==2.3.3
- reportlab==4.0.4
- pandas==2.1.1
- (and other dependencies)

### application.py
Entry point for Elastic Beanstalk

---

## Cost Estimate

**Continuous Operation (~30 days):**
- t3.small instance: ~$15/month
- Application Load Balancer: ~$18/month
- SSL Certificate: FREE
- Total: ~$33/month

**48-Hour Event (300 users):**
- 4x t3.medium instances: ~$1.60
- Load Balancer: ~$0.50
- Total: ~$2.30

---

## Summary Checklist

- [ ] S3 bucket configured
- [ ] EB application initialized
- [ ] Production environment created
- [ ] Load balancer DNS obtained
- [ ] DNS CNAME record updated
- [ ] SSL certificate verified
- [ ] HTTPS listener configured (automatic)
- [ ] Port 443 opened (automatic)
- [ ] Application accessible via HTTPS
- [ ] Admin panel working

---

**Last Updated:** January 16, 2026
**Domain:** awsmagicbus.me
**Region:** ap-northeast-2 (Seoul)
**SSL Certificate:** arn:aws:acm:ap-northeast-2:903578657649:certificate/6754f66a-088a-4540-bad0-ee9c6d03bde0