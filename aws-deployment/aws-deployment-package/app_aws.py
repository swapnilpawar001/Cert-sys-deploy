import os
import sys
from flask import Flask
from flask_cors import CORS
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging for AWS CloudWatch
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add parent directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# Import our production app
from app_production import app as application

# AWS-specific configurations
application.config.update(
    SECRET_KEY=os.environ.get('SECRET_KEY', 'aws-production-secret-key'),
    CERTIFICATE_DIR=os.environ.get('CERTIFICATE_DIR', '/tmp/certificates'),
    EXCEL_DIR=os.environ.get('EXCEL_DIR', '/tmp/excel-data')
)

# Ensure AWS directories exist
os.makedirs(application.config['CERTIFICATE_DIR'], exist_ok=True)
os.makedirs(application.config['EXCEL_DIR'], exist_ok=True)

logger.info("🚀 AWS Training Certificate System - AWS Deployment Ready")

if __name__ == '__main__':
    # For local testing only
    port = int(os.environ.get('PORT', 5000))
    application.run(host='0.0.0.0', port=port, debug=False)
