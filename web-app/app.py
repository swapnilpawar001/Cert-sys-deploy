from flask import Flask, render_template, request, jsonify, send_file, session
import pandas as pd
import os
import sys
from datetime import datetime
import json

# Add parent directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# Import PIL for image processing
try:
    from PIL import Image, ImageDraw, ImageFont
    PIL_AVAILABLE = True
    print("✅ PIL (Pillow) available for image processing")
except ImportError:
    PIL_AVAILABLE = False
    print("❌ PIL not available, will use text fallback")

# Create Flask app first (globally)
app = Flask(__name__)
app.secret_key = 'aws-training-certificate-system-2024'

# Define the web app class with better error handling
class CertificateWebApp:
    def __init__(self):
        print("🔄 Initializing CertificateWebApp...")
        self.excel_processor = None
        self.student_data = None
        self.template_path = None
        self.output_dir = None
        self.initialize_components()
    
    def initialize_components(self):
        """Initialize components with detailed error handling"""
        try:
            print("📂 Setting up directories...")
            # Set up directories with ABSOLUTE paths
            self.output_dir = os.path.join(parent_dir, 'data', 'certificate-templates', 'processed')
            self.template_path = os.path.join(parent_dir, 'data', 'certificate-templates', 'raw', 'certificate-template.png')
            
            print(f"📄 Template path: {self.template_path}")
            print(f"📁 Output directory: {self.output_dir}")
            
            # Check if template exists with detailed info
            if os.path.exists(self.template_path):
                template_size = os.path.getsize(self.template_path)
                print(f"✅ Template found: {template_size} bytes")
                
                try:
                    with Image.open(self.template_path) as img:
                        print(f"📊 Template dimensions: {img.size}")
                        print(f"🎨 Template mode: {img.mode}")
                except Exception as e:
                    print(f"⚠️ Could not open template: {e}")
            else:
                print("❌ Template not found")
                # Check what's actually there
                template_dir = os.path.join(parent_dir, 'data', 'certificate-templates', 'raw')
                if os.path.exists(template_dir):
                    files = os.listdir(template_dir)
                    print(f"📋 Files in template directory: {files}")
                    # Try to use whatever PNG file is there
                    for file in files:
                        if file.endswith('.png'):
                            self.template_path = os.path.join(template_dir, file)
                            print(f"🎯 Using alternative template: {file}")
                            break
            
            # Create output directory
            os.makedirs(self.output_dir, exist_ok=True)
            print(f"✅ Output directory created/verified")
            
            # Initialize Excel processor
            self.initialize_excel_processor()
            
        except Exception as e:
            print(f"❌ Error in initialize_components: {e}")
            self.create_fallback_components()
    
    def initialize_excel_processor(self):
        """Initialize Excel processor with detailed logging"""
        try:
            print("🔧 Initializing Excel processor...")
            
            # Simple Excel processor
            class ExcelProcessor:
                def __init__(self):
                    pass
                
                def load_student_data(self, file_path):
                    try:
                        print(f"📊 Attempting to load: {file_path}")
                        if os.path.exists(file_path):
                            print(f"✅ File exists, loading...")
                            df = pd.read_excel(file_path)
                            print(f"✅ Excel loaded: {len(df)} rows, columns: {list(df.columns)}")
                            return df
                        else:
                            print(f"❌ File not found: {file_path}")
                        return None
                    except Exception as e:
                        print(f"❌ Excel loading error: {e}")
                        return None
                
                def validate_excel_structure(self, file_path):
                    return True
            
            self.excel_processor = ExcelProcessor()
            print("✅ Excel processor initialized")
            
        except Exception as e:
            print(f"❌ Error initializing Excel processor: {e}")
    
    def load_student_data(self):
        """Load student data with comprehensive path checking"""
        try:
            print("📊 Loading student data...")
            
            possible_paths = [
                os.path.join(parent_dir, 'data', 'excel-samples', 'student-data.xlsx'),
                os.path.join(current_dir, 'data', 'excel-samples', 'student-data.xlsx'),
                os.path.join(parent_dir, 'web-app', 'data', 'excel-samples', 'student-data.xlsx'),
                '/workspaces/aws-training-certificate-system/data/excel-samples/student-data.xlsx'
            ]
            
            excel_file = None
            for i, path in enumerate(possible_paths):
                print(f"🔍 Checking path {i+1}: {path}")
                if os.path.exists(path):
                    excel_file = path
                    print(f"✅ Found Excel file: {excel_file}")
                    break
                else:
                    print(f"❌ Not found: {path}")
            
            if excel_file:
                print(f"📊 Loading from: {excel_file}")
                df = self.excel_processor.load_student_data(excel_file)
                if df is not None:
                    self.student_data = df
                    print(f"✅ Loaded {len(self.student_data)} students")
                    print(f"📋 Columns: {list(self.student_data.columns)}")
                    if len(self.student_data) > 0:
                        print(f"🔍 First student: {self.student_data.iloc[0].to_dict()}")
                else:
                    print("❌ Failed to load Excel data")
                    self.create_sample_data()
            else:
                print("❌ Excel file not found in any location")
                self.create_sample_data()
                
        except Exception as e:
            print(f"❌ Error loading student data: {e}")
            self.create_sample_data()
    
    def create_sample_data(self):
        """Create sample data for testing"""
        try:
            print("📝 Creating sample data...")
            sample_data = [
                {
                    'sixerclass_id': 'SIX001',
                    'student_name': 'John Doe Smith',
                    'batch_number': 'AWS-2024-001',
                    'batch_start_date': '2024-01-15',
                    'batch_end_date': '2024-04-15'
                },
                {
                    'sixerclass_id': 'SIX002',
                    'student_name': 'Jane Doe Wilson',
                    'batch_number': 'AWS-2024-001',
                    'batch_start_date': '2024-01-15',
                    'batch_end_date': '2024-04-15'
                }
            ]
            
            self.student_data = pd.DataFrame(sample_data)
            print("✅ Sample data created")
            
        except Exception as e:
            print(f"❌ Error creating sample data: {e}")
            # Create empty DataFrame as final fallback
            self.student_data = pd.DataFrame(columns=['sixerclass_id', 'student_name', 'batch_number', 'batch_start_date', 'batch_end_date'])

    def authenticate_student(self, student_name, batch_number, sixerclass_id):
        """Authenticate student against data"""
        try:
            if self.student_data is None or self.student_data.empty:
                print("❌ No student data available")
                return None
            
            print(f"🔍 Authenticating: {student_name}, {batch_number}, {sixerclass_id}")
            print(f"📊 Available students: {len(self.student_data)}")
            
            # Look for matching student
            for index, row in self.student_data.iterrows():
                student_name_clean = str(row.get('student_name', '')).lower().strip()
                batch_number_clean = str(row.get('batch_number', '')).lower().strip()
                sixerclass_id_clean = str(row.get('sixerclass_id', '')).lower().strip()
                
                print(f"📋 Checking: {student_name_clean} vs {student_name.lower().strip()}")
                print(f"📋 Checking: {batch_number_clean} vs {batch_number.lower().strip()}")
                print(f"📋 Checking: {sixerclass_id_clean} vs {sixerclass_id.lower().strip()}")
                
                if (student_name_clean == student_name.lower().strip() and
                    batch_number_clean == batch_number.lower().strip() and
                    sixerclass_id_clean == sixerclass_id.lower().strip()):
                    print(f"✅ Found matching student: {row['student_name']}")
                    return row.to_dict()
            
            print("❌ No matching student found")
            return None
            
        except Exception as e:
            print(f"❌ Authentication error: {e}")
            return None
    
    def generate_certificate(self, student_data):
        """Generate certificate using your actual template"""
        try:
            if not PIL_AVAILABLE:
                print("⚠️ PIL not available, using text fallback")
                return self.generate_text_certificate(student_data)
            
            if not os.path.exists(self.template_path):
                print("❌ Template not found, creating placeholder")
                return self.generate_placeholder_certificate(student_data)
            
            print("🎨 Generating JPEG certificate with template...")
            
            # Load the actual template
            with Image.open(self.template_path) as template:
                certificate = template.copy()
                draw = ImageDraw.Draw(certificate)
                
                # Load fonts
                fonts = self.load_fonts()
                
                # Your exact positions (final positions)
                text_positions = {
                    "student_name": (550, 400),      # X: 550, Y: 400
                    "start_date": (420, 530),        # X: 420, Y: 530
                    "end_date": (680, 530),          # X: 680, Y: 530
                }
                
                # Prepare text data
                texts_to_draw = [
                    {
                        'text': student_data['student_name'].upper(),
                        'position': text_positions['student_name'],
                        'font': fonts['name'],
                        'color': '#1a365d',  # Rich dark blue
                        'label': 'Student Name'
                    },
                    {
                        'text': self.format_date(student_data['batch_start_date']),
                        'position': text_positions['start_date'],
                        'font': fonts['date'],
                        'color': '#2d3748',  # Rich dark gray
                        'label': 'Start Date'
                    },
                    {
                        'text': self.format_date(student_data['batch_end_date']),
                        'position': text_positions['end_date'],
                        'font': fonts['date'],
                        'color': '#2d3748',  # Rich dark gray
                        'label': 'End Date'
                    }
                ]
                
                # Add each text element to the certificate
                for text_config in texts_to_draw:
                    x, y = text_config['position']
                    
                    # Draw text with center alignment
                    draw.text(
                        (x, y), 
                        text_config['text'], 
                        fill=text_config['color'], 
                        font=text_config['font'], 
                        anchor='mm'
                    )
                    
                    print(f"📍 {text_config['label']}: Position ({x}, {y}) - Text: '{text_config['text']}'")
                
                # Generate high-quality output filename
                safe_name = "".join(c for c in student_data['student_name'] if c.isalnum() or c in (' ', '-', '_'))
                output_filename = f"certificate_{student_data['sixerclass_id']}_{safe_name.replace(' ', '_')}.png"
                output_path = os.path.join(self.output_dir, output_filename)
                
                # Save with HIGH QUALITY settings
                certificate.save(
                    output_path,
                    'PNG',
                    quality=100,
                    optimize=False,
                    dpi=(300, 300)
                )
                
                print(f"✅ High-quality JPEG certificate generated: {output_filename}")
                return output_path
                
        except Exception as e:
            print(f"❌ JPEG certificate generation error: {e}")
            return self.generate_text_certificate(student_data)
    
    def load_fonts(self):
        """Load fonts for certificate text"""
        fonts = {}
        try:
            # Try different font sources
            font_candidates = [
                "arial.ttf", "Arial.ttf", "Helvetica.ttf", 
                "DejaVuSans.ttf", "FreeSans.ttf", "LiberationSans.ttf"
            ]
            
            # Find available font
            available_font = None
            for font_name in font_candidates:
                try:
                    fonts["name"] = ImageFont.truetype(font_name, 36)
                    available_font = font_name
                    break
                except:
                    continue
            
            if available_font:
                fonts["date"] = ImageFont.truetype(available_font, 28)
                print(f"✅ Using font: {available_font}")
            else:
                raise Exception("No suitable font found")
                
        except Exception as e:
            # Fallback to default font
            fonts["name"] = ImageFont.load_default()
            fonts["date"] = ImageFont.load_default()
            print("⚠️ Using default fonts")
        
        return fonts
    
    def format_date(self, date_str):
        """Format date nicely for certificate"""
        try:
            if isinstance(date_str, str):
                date_obj = pd.to_datetime(date_str)
            else:
                date_obj = date_str
            return date_obj.strftime("%B %d, %Y")  # e.g., "January 15, 2024"
        except:
            return str(date_str)

# Create the web app instance with error handling
try:
    web_app = CertificateWebApp()
    print("✅ Web application initialized successfully")
    
    if web_app.student_data is not None:
        student_count = len(web_app.student_data)
        print(f"📊 Students loaded: {student_count}")
        if student_count > 0:
            print(f"🔍 First student: {web_app.student_data.iloc[0].to_dict()}")
    else:
        print("❌ Student data is None")
        
except Exception as e:
    print(f"❌ Failed to initialize web application: {e}")
    web_app = None

# Define routes (same as before)
@app.route('/')
def index():
    """Main login page"""
    return render_template('enhanced.html')

# ... (rest of the routes remain the same)
@app.route('/api/authenticate', methods=['POST'])
def authenticate():
    """Authenticate student and return certificate info"""
    try:
        if web_app is None:
            return jsonify({"error": "Web application not initialized"}), 500
        
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        student_name = data.get('student_name', '').strip()
        batch_number = data.get('batch_number', '').strip()
        sixerclass_id = data.get('sixerclass_id', '').strip()
        
        # Validate input
        if not all([student_name, batch_number, sixerclass_id]):
            return jsonify({"error": "All fields are required"}), 400
        
        # Authenticate student
        student = web_app.authenticate_student(student_name, batch_number, sixerclass_id)
        
        if student:
            # Store in session for certificate generation
            session['student_data'] = student
            
            return jsonify({
                "success": True,
                "student": {
                    "sixerclass_id": student['sixerclass_id'],
                    "student_name": student['student_name'],
                    "batch_number": student['batch_number'],
                    "batch_start_date": str(student['batch_start_date']),
                    "batch_end_date": str(student['batch_end_date'])
                }
            })
        else:
            return jsonify({"error": "Student not found. Please check your details."}), 404
            
    except Exception as e:
        return jsonify({"error": f"Authentication failed: {str(e)}"}), 500

@app.route('/api/download-certificate', methods=['POST'])
def download_certificate():
    """Generate and download student certificate (JPEG with template)"""
    try:
        if web_app is None:
            return jsonify({"error": "Web application not initialized"}), 500
        
        # Check if student is authenticated
        if 'student_data' not in session:
            return jsonify({"error": "Please authenticate first"}), 401
        
        student_data = session['student_data']
        
        # Generate certificate (JPEG with template)
        certificate_path = web_app.generate_certificate(student_data)
        
        if certificate_path and os.path.exists(certificate_path):
            # Return download URL
            filename = os.path.basename(certificate_path)
            return jsonify({
                "success": True,
                "download_url": f"/api/serve-certificate/{filename}",
                "filename": filename
            })
        else:
            return jsonify({"error": "Certificate generation failed"}), 500
            
    except Exception as e:
        return jsonify({"error": f"Download failed: {str(e)}"}), 500

@app.route('/api/serve-certificate/<filename>')
def serve_certificate(filename):
    """Serve generated certificate file"""
    try:
        if web_app is None:
            return jsonify({"error": "Web application not initialized"}), 500
        
        # Security: only serve files from our certificate directory
        certificate_dir = "../data/certificate-templates/processed"
        file_path = os.path.join(certificate_dir, filename)
        
        if os.path.exists(file_path) and filename.startswith('certificate_'):
            return send_file(file_path, as_attachment=True, download_name=filename)
        else:
            return jsonify({"error": "Certificate not found"}), 404
            
    except Exception as e:
        return jsonify({"error": f"File serving failed: {str(e)}"}), 500

@app.route('/api/check-status')
def check_status():
    """Check system status"""
    if web_app is None:
        return jsonify({"status": "error", "message": "Web application not initialized"}), 500
    
    student_count = len(web_app.student_data) if web_app.student_data is not None else 0
    return jsonify({
        "status": "operational",
        "students_loaded": student_count,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/logout')
def logout():
    """Clear session"""
    session.clear()
    return jsonify({"success": True})

if __name__ == '__main__':
    print("🚀 Starting AWS Training Certificate Web Application")
    print("📍 URL: http://localhost:5000")
    print("✨ Features: Student authentication, JPEG certificate generation with template, download")
    
    if web_app is not None and web_app.student_data is not None:
        print(f"📊 Students loaded: {len(web_app.student_data)}")
        print("📄 Certificate template positions:")
        print("   Name: (550, 400)")
        print("   Start Date: (420, 530)")
        print("   End Date: (680, 530)")
    else:
        print("❌ Web application or student data not properly initialized")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
