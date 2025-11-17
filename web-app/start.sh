#!/bin/bash

echo "🚀 Starting AWS Training Certificate Web Application"
echo "📍 URL: http://localhost:5000"
echo "✨ Features: Student login, certificate generation, download"
echo ""

# Navigate to web app directory
cd "$(dirname "$0")"

# Start Flask application
python app.py
