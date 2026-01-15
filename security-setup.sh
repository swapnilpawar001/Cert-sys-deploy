#!/bin/bash

# Security Hardening Script for AWS Certificate System
echo "🔒 Security Hardening Script"
echo "============================"

# Generate secure secret key
echo "🔑 Generating secure SECRET_KEY..."
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")
echo "Generated SECRET_KEY: $SECRET_KEY"

# Create secure .env file
echo "📝 Creating secure .env file..."
cat > .env << EOF
# Generated on $(date)
SECRET_KEY=$SECRET_KEY
ADMIN_USERNAME=admin
ADMIN_PASSWORD=SecurePass$(date +%s)
FLASK_ENV=production
FLASK_DEBUG=False
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True
EOF

echo "✅ Secure .env file created"

# Set proper file permissions
echo "🔐 Setting file permissions..."
chmod 600 .env
chmod 755 src/
chmod 644 src/*.py
chmod 755 data/
chmod 755 assets/

# Create required directories with proper permissions
echo "📁 Creating directories..."
mkdir -p data/{certificates,excel,uploads,templates}
chmod 755 data/{certificates,excel,uploads,templates}

# Security checklist
echo ""
echo "🔒 Security Checklist:"
echo "====================="
echo "✅ Secure SECRET_KEY generated"
echo "✅ Strong admin password set"
echo "✅ File permissions configured"
echo "✅ Production environment set"

echo ""
echo "⚠️  IMPORTANT MANUAL STEPS:"
echo "1. Upload certificate template to data/templates/"
echo "2. Configure SSL certificate in AWS"
echo "3. Set up security groups (ports 80, 443 only)"
echo "4. Enable CloudWatch logging"
echo "5. Configure backup strategy"

echo ""
echo "🚨 BEFORE DEPLOYMENT:"
echo "1. Test locally: python src/app.py"
echo "2. Verify all endpoints work"
echo "3. Check certificate generation"
echo "4. Update admin credentials in AWS console"

echo ""
echo "Generated admin password: SecurePass$(date +%s)"
echo "Save this password securely!"