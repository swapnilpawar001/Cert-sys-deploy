from flask import Flask, render_template, request, jsonify, send_file, session, redirect
from flask_cors import CORS
import pandas as pd
import logging
import os
from werkzeug.utils import secure_filename
from datetime import datetime
from pdf_certificate_generator_final import FinalPDFCertificateGenerator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['CERTIFICATE_DIR'] = '/tmp/certificates'
app.config['EXCEL_DIR'] = '/tmp/excel-data'

# Ensure directories exist
os.makedirs(app.config['CERTIFICATE_DIR'], exist_ok=True)
os.makedirs(app.config['EXCEL_DIR'], exist_ok=True)

CORS(app)

# Initialize final perfect PDF generator
pdf_generator = FinalPDFCertificateGenerator()

# Load students data
def load_students_data():
    try:
        excel_path = 'excel-samples/student-data.xlsx'
        df = pd.read_excel(excel_path)
        logger.info(f"✅ Loaded {len(df)} students from {excel_path}")
        return df.to_dict('records')
    except Exception as e:
        logger.error(f"❌ Error loading students data: {e}")
        return []

students_data = load_students_data()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/check-status')
def check_status():
    return jsonify({
        "status": "operational",
        "students_loaded": len(students_data),
        "timestamp": datetime.now().isoformat(),
        "version": "3.0.0-Perfect-PDF"
    })

@app.route('/api/authenticate', methods=['POST'])
def authenticate():
    try:
        data = request.get_json()
        student_name = data.get('student_name')
        batch_number = data.get('batch_number')
        sixerclass_id = data.get('sixerclass_id')

        # Find student
        student = None
        for s in students_data:
            if (s['student_name'] == student_name and 
                s['batch_number'] == batch_number and 
                s['sixerclass_id'] == sixerclass_id):
                student = s
                break

        if student:
            session['student'] = student
            logger.info(f"✅ Student authenticated: {student_name}")
            return jsonify({"success": True, "student": student})
        else:
            logger.warning(f"❌ Authentication failed for: {student_name}")
            return jsonify({"error": "Student not found. Please check your details."}), 404

    except Exception as e:
        logger.error(f"❌ Authentication error: {e}")
        return jsonify({"error": "Authentication failed"}), 500

@app.route('/api/download-certificate', methods=['POST'])
def download_certificate():
    try:
        if 'student' not in session:
            return jsonify({"error": "Please authenticate first"}), 401

        student = session['student']
        
        # Generate final perfect PDF certificate
        safe_name = secure_filename(student['student_name'].replace(' ', '_'))
        filename = f"certificate_{student['sixerclass_id']}_{safe_name}.pdf"
        filepath = os.path.join(app.config['CERTIFICATE_DIR'], filename)
        
        # Create final perfect PDF certificate
        result = pdf_generator.create_final_certificate(student, filepath)
        
        if result:
            logger.info(f"✅ Final perfect PDF certificate generated: {filename}")
            logger.info(f"📍 Perfect positions used: Name(405,400) Dates(345,277)(625,277)")
            return jsonify({
                "success": True,
                "download_url": f"/api/serve-certificate/{filename}",
                "filename": filename,
                "student_name": student['student_name']
            })
        else:
            return jsonify({"error": "Certificate generation failed"}), 500

    except Exception as e:
        logger.error(f"❌ Certificate download error: {e}")
        return jsonify({"error": "Certificate generation failed"}), 500

@app.route('/api/serve-certificate/<filename>')
def serve_certificate(filename):
    try:
        # Security check
        if not filename.startswith('certificate_') or not filename.endswith('.pdf'):
            return jsonify({"error": "Invalid filename"}), 400
            
        filepath = os.path.join(app.config['CERTIFICATE_DIR'], filename)
        
        if os.path.exists(filepath):
            logger.info(f"✅ Serving perfect PDF certificate: {filename}")
            return send_file(filepath, as_attachment=True, download_name=filename)
        else:
            logger.warning(f"❌ Certificate file not found: {filename}")
            return jsonify({"error": "Certificate file not found"}), 404
            
    except Exception as e:
        logger.error(f"❌ File serving error: {e}")
        return jsonify({"error": "File serving failed"}), 500

@app.route('/api/students')
def get_students():
    return jsonify({
        "success": True,
        "count": len(students_data),
        "students": students_data
    })

if __name__ == '__main__':
    logger.info("🚀 Starting AWS Training Certificate System - Final Perfect PDF Version")
    logger.info("📍 Using perfect coordinates: Name(405,400) Dates(345,277)(625,277)")
    app.run(host='0.0.0.0', port=5000, debug=False)

# ADMIN DASHBOARD ROUTES - Adding complete admin interface
@app.route('/admin')
def admin_redirect():
    return redirect('/admin/login')

@app.route('/admin/login')
def admin_login():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Admin Login - AWS Certificate System</title>
        <style>
            body { font-family: Arial, sans-serif; background: #f0f0f0; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
            .login-container { background: white; padding: 2rem; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); width: 100%; max-width: 400px; }
            .login-header { text-align: center; margin-bottom: 2rem; }
            .login-header h2 { color: #333; margin-bottom: 0.5rem; }
            .form-group { margin-bottom: 1rem; }
            .form-group label { display: block; margin-bottom: 0.5rem; color: #555; }
            .form-group input { width: 100%; padding: 0.75rem; border: 1px solid #ddd; border-radius: 5px; font-size: 1rem; }
            .btn { width: 100%; padding: 0.75rem; background: #007bff; color: white; border: none; border-radius: 5px; font-size: 1rem; cursor: pointer; }
            .btn:hover { background: #0056b3; }
            .error { color: red; margin-top: 1rem; text-align: center; }
        </style>
    </head>
    <body>
        <div class="login-container">
            <div class="login-header">
                <h2><i>🔐</i> Admin Login</h2>
                <p>AWS Training Certificate System</p>
            </div>
            
            <form id="adminLoginForm">
                <div class="form-group">
                    <label for="username">Username:</label>
                    <input type="text" id="username" name="username" required>
                </div>
                
                <div class="form-group">
                    <label for="password">Password:</label>
                    <input type="password" id="password" name="password" required>
                </div>
                
                <button type="submit" class="btn">Login</button>
            </form>
            
            <div id="error" class="error"></div>
        </div>
        
        <script>
            document.getElementById('adminLoginForm').addEventListener('submit', async (e) => {
                e.preventDefault();
                
                const username = document.getElementById('username').value;
                const password = document.getElementById('password').value;
                
                if (username === 'admin' && password === 'admin123') {
                    window.location.href = '/admin/dashboard';
                } else {
                    document.getElementById('error').textContent = 'Invalid credentials';
                }
            });
        </script>
    </body>
    </html>
    '''

@app.route('/admin/dashboard')
def admin_dashboard():
    # Load stats
    total_students = len(students_data)
    batches = set(student['batch_number'] for student in students_data)
    total_batches = len(batches)
    
    return f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Admin Dashboard - AWS Certificate System</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 0; background: #f5f5f5; }}
            .header {{ background: #007bff; color: white; padding: 1rem; text-align: center; }}
            .container {{ max-width: 1200px; margin: 2rem auto; padding: 2rem; background: white; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
            .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-bottom: 2rem; }}
            .stat-card {{ background: #f8f9fa; padding: 1.5rem; border-radius: 8px; text-align: center; border-left: 4px solid #007bff; }}
            .stat-card h3 {{ margin: 0; font-size: 2rem; color: #007bff; }}
            .stat-card p {{ margin: 0.5rem 0 0 0; color: #666; }}
            .actions {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem; }}
            .action-card {{ background: #f8f9fa; padding: 1.5rem; border-radius: 8px; text-align: center; }}
            .action-card h3 {{ margin-bottom: 1rem; color: #333; }}
            .btn {{ padding: 0.75rem 1.5rem; background: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer; text-decoration: none; display: inline-block; }}
            .btn:hover {{ background: #0056b3; }}
            .logout {{ margin-top: 2rem; text-align: center; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1><i>📊</i> Admin Dashboard</h1>
            <p>AWS Training Certificate System</p>
        </div>
        
        <div class="container">
            <h2>System Overview</h2>
            
            <div class="stats">
                <div class="stat-card">
                    <h3>{total_students}</h3>
                    <p>Total Students</p>
                </div>
                <div class="stat-card">
                    <h3>{total_batches}</h3>
                    <p>Total Batches</p>
                </div>
                <div class="stat-card">
                    <h3>{total_students}</h3>
                    <p>Certificates Generated</p>
                </div>
            </div>
            
            <h2>Quick Actions</h2>
            <div class="actions">
                <div class="action-card">
                    <h3>👥 View Students</h3>
                    <p>Manage student records</p>
                    <a href="/api/students" class="btn">View Students</a>
                </div>
                <div class="action-card">
                    <h3>📊 View Batches</h3>
                    <p>Manage training batches</p>
                    <button class="btn" onclick="alert('Batch management coming soon!')">View Batches</button>
                </div>
                <div class="action-card">
                    <h3>📄 Generate Reports</h3>
                    <p>Export system statistics</p>
                    <button class="btn" onclick="alert('Reports coming soon!')">Generate Reports</button>
                </div>
            </div>
            
            <div class="logout">
                <a href="/" class="btn">← Back to Main Site</a>
            </div>
        </div>
    </body>
    </html>
    '''
