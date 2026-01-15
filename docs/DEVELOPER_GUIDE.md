# 🔧 AWS Training Certificate System - Developer Guide

## 📚 Table of Contents
1. [System Architecture](#system-architecture)
2. [File Structure](#file-structure)
3. [Database Schema](#database-schema)
4. [API Reference](#api-reference)
5. [Configuration](#configuration)
6. [AWS Deployment](#aws-deployment)
7. [Troubleshooting](#troubleshooting)

## 🏗️ System Architecture

**Technology Stack:**
- Backend: Flask (Python)
- Frontend: HTML5, CSS3, JavaScript
- Storage: Excel files (xlsx)
- PDF: ReportLab + Pillow
- Deployment: AWS (Elastic Beanstalk, EC2, ECS)

**Application Flow:**
```
Student Portal → Authentication → Certificate Generation → PDF Download
Admin Panel → Login → Student Management → CRUD Operations → Excel I/O
```

## 📁 File Structure

**Core Application:**
```
src/app.py                    # Main Flask application (1500+ lines)
src/certificate_generator.py # PDF certificate generation
application.py               # AWS Elastic Beanstalk entry point
```

**Data Storage:**
```
data/excel/student-data.xlsx  # Primary student database
data/templates/               # Certificate templates
data/certificates/            # Generated PDFs
data/uploads/                 # Temporary uploads
```

**Deployment:**
```
Dockerfile                    # Container deployment
docker-compose.yml           # Local development
deploy.sh                    # Deployment automation
.env.example                 # Environment template
```

## 🗃️ Database Schema

**Student Record:**
```python
{
    'student_name': str,      # Full name
    'batch_number': str,      # Format: AWS-YYYY-XXX
    'batch_start_date': str,  # YYYY-MM-DD
    'batch_end_date': str,    # YYYY-MM-DD
    'sixerclass_id': str      # Unique ID: SIXNNN
}
```

**Download Log:**
```python
{
    'student_name': str,
    'sixerclass_id': str,
    'batch_number': str,
    'download_time': str,     # ISO timestamp
    'filename': str
}
```

## 🔌 API Reference

**Public Endpoints:**
- `GET /` - Student portal homepage
- `POST /api/authenticate` - Student authentication
- `POST /api/download-certificate` - Generate and download certificate
- `GET /api/check-status` - System health check
- `GET /static/<filename>` - Static assets

**Admin Endpoints:**
- `GET /admin/login` - Admin login page
- `POST /admin/login` - Admin authentication
- `GET /admin/students` - Admin panel
- `GET /admin/api/students` - List students
- `POST /admin/api/students/add` - Add student
- `POST /admin/api/students/update` - Update student
- `POST /admin/api/students/delete` - Delete student
- `GET /admin/api/students/export` - Export Excel
- `POST /admin/api/students/import` - Import Excel
- `GET /admin/api/reports` - Download analytics
- `GET /admin/api/reports/export` - Export reports

## ⚙️ Configuration

**AWS-Compatible Paths:**
```python
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
app.config['BASE_DIR'] = base_dir
app.config['ASSETS_DIR'] = os.path.join(base_dir, 'assets')
app.config['DATA_DIR'] = os.path.join(base_dir, 'data')
app.config['CERTIFICATE_DIR'] = os.path.join(base_dir, 'data', 'certificates')
app.config['EXCEL_DIR'] = os.path.join(base_dir, 'data', 'excel')
app.config['UPLOAD_FOLDER'] = os.path.join(base_dir, 'data', 'uploads')
app.config['TEMPLATE_DIR'] = os.path.join(base_dir, 'data', 'templates')
```

**Environment Variables:**
```bash
SECRET_KEY=your-production-secret-key
ADMIN_USERNAME=admin
ADMIN_PASSWORD=secure-password
FLASK_ENV=production
FLASK_DEBUG=False
```

## 🚀 AWS Deployment

**Deployment Options:**
1. **AWS Elastic Beanstalk** (Recommended)
2. **AWS EC2 with Docker**
3. **AWS ECS with Fargate**

**Quick Deploy:**
```bash
./deploy.sh
```

**Environment Setup:**
```python
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'fallback-key')
app.config['ADMIN_USERNAME'] = os.environ.get('ADMIN_USERNAME', 'admin')
app.config['ADMIN_PASSWORD'] = os.environ.get('ADMIN_PASSWORD', 'admin123')
```

**Requirements:**
- All paths must be absolute and configurable
- Assets accessible via static routes
- Data directories must be writable
- No hardcoded dependencies

## 🐛 Troubleshooting

**Common Issues:**

1. **Static Files Not Loading**
   ```python
   # Check asset paths
   logo_path = os.path.join(app.config['ASSETS_DIR'], 'Magicbus_logo.png')
   if not os.path.exists(logo_path):
       logger.error(f"Logo not found at: {logo_path}")
   ```

2. **Template Not Found**
   ```python
   # Verify template path
   template_path = os.path.join(app.config['TEMPLATE_DIR'], 'certificate-template.png')
   if not os.path.exists(template_path):
       logger.error(f"Certificate template not found at: {template_path}")
   ```

3. **Permission Issues**
   ```bash
   chmod -R 755 data/
   chown -R app:app data/
   ```

4. **Environment Variables**
   ```bash
   echo $SECRET_KEY
   echo $ADMIN_USERNAME
   echo $ADMIN_PASSWORD
   ```

**Debug Mode:**
```python
import logging
logging.basicConfig(level=logging.DEBUG)

logger.info(f"Base directory: {app.config['BASE_DIR']}")
logger.info(f"Assets directory: {app.config['ASSETS_DIR']}")
logger.info(f"Data directory: {app.config['DATA_DIR']}")
```

**Development Workflow:**
```bash
# Local setup
cp .env.example .env
pip install -r requirements.txt
python src/app.py

# Docker testing
docker-compose up
docker build -t certificate-system .
docker run -p 5000:5000 certificate-system
```

---

**For complete deployment instructions, see `AWS_DEPLOYMENT_INSTRUCTIONS.md`** 📖