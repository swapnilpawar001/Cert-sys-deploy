# 🎓 AWS Training Certificate System

A production-ready web-based certificate management system for AWS training programs with student authentication, admin panel, and automated certificate generation.

## ✨ Key Features

- **Student Portal** - Secure authentication and certificate download
- **Admin Panel** - Complete student management with Excel import/export
- **Certificate Generation** - Automated PDF generation with custom templates
- **Download Analytics** - Track and report certificate downloads
- **AWS Ready** - Optimized for AWS deployment with multiple deployment options

## 🚀 Quick Start

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Run application
python src/app.py
```

### Access Points
- **Student Portal**: http://localhost:5000
- **Admin Panel**: http://localhost:5000/admin/login

### Default Admin Credentials
- Username: `admin` | Password: `admin123`
- **⚠️ Change these in production via environment variables**

## 📁 Project Structure

```
Cert-sys-deploy/
├── src/                    # Application source code
├── data/                   # Data storage (Excel, templates, certificates)
├── assets/                 # Static assets (logos, images)
├── docs/                   # Documentation
├── application.py          # AWS Elastic Beanstalk entry point
├── Dockerfile             # Container deployment
├── requirements.txt       # Python dependencies
└── AWS_DEPLOYMENT_INSTRUCTIONS.md  # Complete deployment guide
```

## 📊 Data Format

**Excel Import Columns:**
- `student_name`, `batch_number`, `batch_start_date`, `batch_end_date`, `sixerclass_id`

**Sample Data:** 6 pre-loaded students (SIX001-SIX006) for testing

## ⚙️ Configuration

**Environment Variables:**
```bash
SECRET_KEY=your-production-secret-key
ADMIN_USERNAME=your_admin
ADMIN_PASSWORD=secure_password
FLASK_ENV=production
FLASK_DEBUG=False
```

**Certificate Template:** Place your template at `data/templates/certificate-template.png`

## 🔌 API Endpoints

**Public:** `/`, `/api/authenticate`, `/api/download-certificate`, `/api/check-status`

**Admin:** `/admin/*` - Complete admin panel with student management, Excel operations, and reporting

## 🛡️ Security

- Environment-based configuration
- Session authentication
- File validation and secure handling
- Input sanitization and error handling

## 🚀 AWS Deployment

**Quick Deploy:**
```bash
./deploy.sh
```

**Deployment Options:**
1. AWS Elastic Beanstalk (Recommended)
2. AWS EC2 with Docker
3. AWS ECS with Fargate

📖 **See `AWS_DEPLOYMENT_INSTRUCTIONS.md` for complete deployment guide**

## 🐳 Docker

```bash
# Development
docker-compose up

# Production
docker build -t certificate-system .
docker run -d -p 5000:5000 certificate-system
```

## 📊 Features

- **Download Tracking** - Monitor certificate downloads
- **Analytics & Reports** - Export download statistics
- **Health Monitoring** - System status endpoint

## 📚 Documentation

- **Technical Details:** `docs/DEVELOPER_GUIDE.md`
- **AWS Deployment:** `AWS_DEPLOYMENT_INSTRUCTIONS.md`
- **Sample Data:** 6 test students included

## 🆘 Troubleshooting

1. Ensure certificate template exists at `data/templates/certificate-template.png`
2. Check environment variables are properly set
3. Verify file permissions for data directories
4. Review application logs for errors

---

**Built for AWS Training Programs by Magic Bus India Foundation** 🚌