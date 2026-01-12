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
app.config['UPLOAD_FOLDER'] = '/tmp/uploads'

# Ensure directories exist
os.makedirs(app.config['CERTIFICATE_DIR'], exist_ok=True)
os.makedirs(app.config['EXCEL_DIR'], exist_ok=True)
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

CORS(app)

# Initialize final perfect PDF generator
pdf_generator = FinalPDFCertificateGenerator()

# Global students data
students_data = []

# Load students data
def load_students_data():
    global students_data
    try:
        # Try multiple possible paths
        possible_paths = [
            'aws-final-deployment/excel-samples/student-data.xlsx',
            'excel-samples/student-data.xlsx',
            'data/excel-samples/student-data.xlsx',
            'aws-final-deployment/production/data/excel-samples/student-data.xlsx'
        ]
        
        for excel_path in possible_paths:
            if os.path.exists(excel_path):
                df = pd.read_excel(excel_path)
                students_data = df.to_dict('records')
                logger.info(f"✅ Loaded {len(students_data)} students from {excel_path}")
                return students_data
        
        # If no file found, create sample data
        logger.warning("❌ No Excel file found, creating sample data")
        students_data = create_sample_data()
        return students_data
        
    except Exception as e:
        logger.error(f"❌ Error loading students data: {e}")
        students_data = create_sample_data()
        return students_data

def create_sample_data():
    """Create sample student data"""
    sample_data = [
        {
            'student_name': 'Rahul Sharma',
            'batch_number': 'AWS-2024-001',
            'batch_start_date': '2024-01-15',
            'batch_end_date': '2024-04-15',
            'sixerclass_id': 'SIX001'
        },
        {
            'student_name': 'Priya Patel',
            'batch_number': 'AWS-2024-001',
            'batch_start_date': '2024-01-15',
            'batch_end_date': '2024-04-15',
            'sixerclass_id': 'SIX002'
        },
        {
            'student_name': 'Amit Kumar',
            'batch_number': 'AWS-2024-002',
            'batch_start_date': '2024-02-01',
            'batch_end_date': '2024-05-01',
            'sixerclass_id': 'SIX003'
        }
    ]
    
    # Save sample data to Excel
    df = pd.DataFrame(sample_data)
    os.makedirs('excel-samples', exist_ok=True)
    df.to_excel('excel-samples/student-data.xlsx', index=False)
    logger.info("✅ Created sample Excel data with 3 students")
    
    return sample_data

# Load initial data
load_students_data()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/check-status')
def check_status():
    return jsonify({
        "status": "operational",
        "students_loaded": len(students_data),
        "timestamp": datetime.now().isoformat(),
        "version": "4.0.0-Production-Ready"
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

# ADMIN ROUTES
@app.route('/admin')
def admin_redirect():
    return redirect('/admin/students')

@app.route('/admin/students')
def admin_students():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Student Management - AWS Certificate System</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 0; background: #f5f5f5; }
            .header { background: #007bff; color: white; padding: 1rem; text-align: center; }
            .container { max-width: 1200px; margin: 2rem auto; padding: 2rem; background: white; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            .actions { display: flex; gap: 1rem; margin-bottom: 2rem; flex-wrap: wrap; }
            .btn { padding: 0.75rem 1.5rem; background: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer; text-decoration: none; display: inline-block; }
            .btn:hover { background: #0056b3; }
            .btn-success { background: #28a745; }
            .btn-success:hover { background: #1e7e34; }
            .btn-danger { background: #dc3545; }
            .btn-danger:hover { background: #c82333; }
            .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-bottom: 2rem; }
            .stat-card { background: #f8f9fa; padding: 1.5rem; border-radius: 8px; text-align: center; border-left: 4px solid #007bff; }
            .stat-card h3 { margin: 0; font-size: 2rem; color: #007bff; }
            .stat-card p { margin: 0.5rem 0 0 0; color: #666; }
            .table-container { overflow-x: auto; }
            table { width: 100%; border-collapse: collapse; margin-top: 1rem; }
            th, td { padding: 0.75rem; text-align: left; border-bottom: 1px solid #ddd; }
            th { background: #f8f9fa; font-weight: bold; }
            tr:hover { background: #f8f9fa; }
            .search-box { width: 100%; padding: 0.75rem; border: 1px solid #ddd; border-radius: 5px; margin-bottom: 1rem; }
            .upload-area { border: 2px dashed #007bff; border-radius: 10px; padding: 2rem; text-align: center; margin: 1rem 0; background: #f8f9fa; }
            .upload-area.dragover { background: #e3f2fd; border-color: #0056b3; }
            #fileInput { display: none; }
            .progress { width: 100%; height: 20px; background: #f0f0f0; border-radius: 10px; overflow: hidden; margin: 1rem 0; display: none; }
            .progress-bar { height: 100%; background: #007bff; transition: width 0.3s; }
            .alert { padding: 1rem; border-radius: 5px; margin: 1rem 0; }
            .alert-success { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
            .alert-error { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>📊 Student Management</h1>
            <p>AWS Training Certificate System</p>
        </div>
        
        <div class="container">
            <div class="stats" id="stats">
                <div class="stat-card">
                    <h3 id="totalStudents">0</h3>
                    <p>Total Students</p>
                </div>
                <div class="stat-card">
                    <h3 id="totalBatches">0</h3>
                    <p>Total Batches</p>
                </div>
                <div class="stat-card">
                    <h3 id="recentStudents">0</h3>
                    <p>Recent Additions</p>
                </div>
            </div>
            
            <div class="actions">
                <button class="btn btn-success" onclick="exportStudents()">📥 Export Excel</button>
                <button class="btn btn-success" onclick="document.getElementById('fileInput').click()">📤 Import Excel</button>
                <button class="btn" onclick="refreshData()">🔄 Refresh</button>
                <a href="/" class="btn">← Back to Main</a>
            </div>
            
            <div class="upload-area" id="uploadArea">
                <h3>📤 Import Students from Excel</h3>
                <p>Drag and drop an Excel file here, or click "Import Excel" to select a file</p>
                <p><small>Supported formats: .xlsx, .xls</small></p>
                <input type="file" id="fileInput" accept=".xlsx,.xls" onchange="handleFileSelect(event)">
            </div>
            
            <div class="progress" id="progressContainer">
                <div class="progress-bar" id="progressBar"></div>
            </div>
            
            <div id="alertContainer"></div>
            
            <input type="text" class="search-box" id="searchBox" placeholder="🔍 Search students by name, batch, or ID..." onkeyup="filterStudents()">
            
            <div class="table-container">
                <table id="studentsTable">
                    <thead>
                        <tr>
                            <th>SixerClass ID</th>
                            <th>Student Name</th>
                            <th>Batch Number</th>
                            <th>Start Date</th>
                            <th>End Date</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody id="studentsTableBody">
                        <tr>
                            <td colspan="6" style="text-align: center; padding: 2rem;">Loading students...</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
        
        <script>
            let allStudents = [];
            
            // Load students data
            async function loadStudents() {
                try {
                    const response = await fetch('/admin/api/students');
                    const data = await response.json();
                    
                    if (data.success) {
                        allStudents = data.students;
                        displayStudents(allStudents);
                        updateStats();
                    } else {
                        showAlert('Failed to load students', 'error');
                    }
                } catch (error) {
                    console.error('Error loading students:', error);
                    showAlert('Error loading students', 'error');
                }
            }
            
            // Display students in table
            function displayStudents(students) {
                const tbody = document.getElementById('studentsTableBody');
                
                if (students.length === 0) {
                    tbody.innerHTML = '<tr><td colspan="6" style="text-align: center; padding: 2rem;">No students found</td></tr>';
                    return;
                }
                
                tbody.innerHTML = students.map(student => `
                    <tr>
                        <td>${student.sixerclass_id}</td>
                        <td>${student.student_name}</td>
                        <td>${student.batch_number}</td>
                        <td>${student.batch_start_date}</td>
                        <td>${student.batch_end_date}</td>
                        <td>
                            <button class="btn" onclick="generateCertificate('${student.sixerclass_id}')">📄 Certificate</button>
                        </td>
                    </tr>
                `).join('');
            }
            
            // Update statistics
            function updateStats() {
                document.getElementById('totalStudents').textContent = allStudents.length;
                
                const batches = new Set(allStudents.map(s => s.batch_number));
                document.getElementById('totalBatches').textContent = batches.size;
                
                // Recent students (assuming last 10% are recent)
                const recentCount = Math.ceil(allStudents.length * 0.1);
                document.getElementById('recentStudents').textContent = recentCount;
            }
            
            // Filter students
            function filterStudents() {
                const searchTerm = document.getElementById('searchBox').value.toLowerCase();
                const filtered = allStudents.filter(student => 
                    student.student_name.toLowerCase().includes(searchTerm) ||
                    student.batch_number.toLowerCase().includes(searchTerm) ||
                    student.sixerclass_id.toLowerCase().includes(searchTerm)
                );
                displayStudents(filtered);
            }
            
            // Export students to Excel
            async function exportStudents() {
                try {
                    const response = await fetch('/admin/api/students/export');
                    if (response.ok) {
                        const blob = await response.blob();
                        const url = window.URL.createObjectURL(blob);
                        const a = document.createElement('a');
                        a.href = url;
                        a.download = `students_export_${new Date().toISOString().split('T')[0]}.xlsx`;
                        document.body.appendChild(a);
                        a.click();
                        document.body.removeChild(a);
                        window.URL.revokeObjectURL(url);
                        showAlert('Students exported successfully!', 'success');
                    } else {
                        showAlert('Export failed', 'error');
                    }
                } catch (error) {
                    console.error('Export error:', error);
                    showAlert('Export error', 'error');
                }
            }
            
            // Handle file selection
            function handleFileSelect(event) {
                const file = event.target.files[0];
                if (file) {
                    uploadFile(file);
                }
            }
            
            // Upload file
            async function uploadFile(file) {
                const formData = new FormData();
                formData.append('file', file);
                
                try {
                    showProgress(0);
                    showAlert('Uploading and processing file...', 'success');
                    
                    const response = await fetch('/admin/api/students/import', {
                        method: 'POST',
                        body: formData
                    });
                    
                    const result = await response.json();
                    hideProgress();
                    
                    if (result.success) {
                        showAlert(`Import successful! ${result.imported_count} students imported.`, 'success');
                        loadStudents(); // Refresh the table
                    } else {
                        showAlert(`Import failed: ${result.error}`, 'error');
                    }
                } catch (error) {
                    hideProgress();
                    console.error('Upload error:', error);
                    showAlert('Upload failed', 'error');
                }
            }
            
            // Show alert
            function showAlert(message, type) {
                const container = document.getElementById('alertContainer');
                const alert = document.createElement('div');
                alert.className = `alert alert-${type}`;
                alert.textContent = message;
                container.innerHTML = '';
                container.appendChild(alert);
                
                setTimeout(() => {
                    container.innerHTML = '';
                }, 5000);
            }
            
            // Show/hide progress
            function showProgress(percent) {
                document.getElementById('progressContainer').style.display = 'block';
                document.getElementById('progressBar').style.width = percent + '%';
            }
            
            function hideProgress() {
                document.getElementById('progressContainer').style.display = 'none';
            }
            
            // Refresh data
            function refreshData() {
                loadStudents();
                showAlert('Data refreshed!', 'success');
            }
            
            // Generate certificate (placeholder)
            function generateCertificate(sixerclassId) {
                showAlert(`Certificate generation for ${sixerclassId} - Feature coming soon!`, 'success');
            }
            
            // Drag and drop functionality
            const uploadArea = document.getElementById('uploadArea');
            
            uploadArea.addEventListener('dragover', (e) => {
                e.preventDefault();
                uploadArea.classList.add('dragover');
            });
            
            uploadArea.addEventListener('dragleave', () => {
                uploadArea.classList.remove('dragover');
            });
            
            uploadArea.addEventListener('drop', (e) => {
                e.preventDefault();
                uploadArea.classList.remove('dragover');
                
                const files = e.dataTransfer.files;
                if (files.length > 0) {
                    uploadFile(files[0]);
                }
            });
            
            // Load data on page load
            loadStudents();
        </script>
    </body>
    </html>
    '''

# ADMIN API ROUTES
@app.route('/admin/api/students')
def admin_api_students():
    """Get all students with optional search"""
    try:
        search = request.args.get('search', '').lower()
        
        if search:
            filtered_students = [
                s for s in students_data 
                if search in s['student_name'].lower() or 
                   search in s['batch_number'].lower() or 
                   search in s['sixerclass_id'].lower()
            ]
        else:
            filtered_students = students_data
        
        return jsonify({
            "success": True,
            "total": len(filtered_students),
            "students": filtered_students
        })
    except Exception as e:
        logger.error(f"❌ Error getting students: {e}")
        return jsonify({"error": "Failed to get students"}), 500

@app.route('/admin/api/students/export')
def admin_export_students():
    """Export students to Excel"""
    try:
        df = pd.DataFrame(students_data)
        
        # Create filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"students_export_{timestamp}.xlsx"
        filepath = os.path.join(app.config['EXCEL_DIR'], filename)
        
        # Export to Excel
        df.to_excel(filepath, index=False, engine='openpyxl')
        
        logger.info(f"✅ Students exported to: {filename}")
        return send_file(filepath, as_attachment=True, download_name=filename)
        
    except Exception as e:
        logger.error(f"❌ Error exporting students: {e}")
        return jsonify({"error": "Export failed"}), 500

@app.route('/admin/api/students/import', methods=['POST'])
def admin_import_students():
    """Import students from Excel file"""
    global students_data
    
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        if not file.filename.lower().endswith(('.xlsx', '.xls')):
            return jsonify({"error": "Invalid file format. Please upload Excel file (.xlsx or .xls)"}), 400
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Read Excel file
        df = pd.read_excel(filepath)
        
        # Validate required columns
        required_columns = ['student_name', 'batch_number', 'batch_start_date', 'batch_end_date', 'sixerclass_id']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            return jsonify({
                "error": f"Missing required columns: {', '.join(missing_columns)}"
            }), 400
        
        # Convert to records
        new_students = df.to_dict('records')
        
        # Validate and add students
        imported_count = 0
        errors = []
        
        for student in new_students:
            # Check for duplicates
            if any(s['sixerclass_id'] == student['sixerclass_id'] for s in students_data):
                errors.append(f"Duplicate SixerClass ID: {student['sixerclass_id']}")
                continue
            
            # Add to students_data
            students_data.append(student)
            imported_count += 1
        
        # Save updated data to Excel
        updated_df = pd.DataFrame(students_data)
        updated_df.to_excel('excel-samples/student-data.xlsx', index=False)
        
        logger.info(f"✅ Imported {imported_count} students from {filename}")
        
        return jsonify({
            "success": True,
            "message": f"Successfully imported {imported_count} students",
            "imported_count": imported_count,
            "errors": errors[:5]  # Return first 5 errors
        })
        
    except Exception as e:
        logger.error(f"❌ Error importing students: {e}")
        return jsonify({"error": "Import failed"}), 500

if __name__ == '__main__':
    logger.info("🚀 Starting AWS Training Certificate System - Production Ready")
    logger.info(f"📊 Loaded {len(students_data)} students")
    app.run(host='0.0.0.0', port=5000, debug=False)