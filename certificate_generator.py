from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os
from datetime import datetime
from PIL import Image

class CertificateGenerator:
    def __init__(self):
        # Try multiple template paths
        possible_paths = [
            'aws-final-deployment/certificate-templates/raw/certificate-template.png',
            'certificate-templates/raw/certificate-template.png',
            'aws-final-deployment/production/data/certificate-templates/raw/certificate-template.png'
        ]
        
        self.template_path = None
        for path in possible_paths:
            if os.path.exists(path):
                self.template_path = path
                break
        
        if not self.template_path:
            print("❌ Certificate template not found!")
        else:
            print(f"✅ Using template: {self.template_path}")
        
    def get_image_dimensions(self):
        """Get original image dimensions"""
        if self.template_path and os.path.exists(self.template_path):
            with Image.open(self.template_path) as img:
                return img.size  # (width, height)
        return (1056, 816)  # Default dimensions
        
    def create_certificate(self, student_data, output_path):
        """Create PDF certificate with template overlay"""
        try:
            if not self.template_path:
                print("❌ No template available")
                return False
                
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Get image dimensions
            img_width, img_height = self.get_image_dimensions()
            
            # Create PDF with exact image dimensions
            custom_page_size = (img_width, img_height)
            c = canvas.Canvas(output_path, pagesize=custom_page_size)
            
            # Draw template image at exact size
            c.drawImage(self.template_path, 0, 0, width=img_width, height=img_height)
            
            # Add text with perfect coordinates (from your conversation)
            c.setFont("Helvetica-Bold", 28)
            c.setFillColorRGB(0, 0, 0)  # Black text
            
            # Student name at perfect position
            c.drawString(405, 400, student_data['student_name'].upper())
            
            # Dates at perfect positions
            c.setFont("Helvetica", 18)
            c.drawString(345, 277, str(student_data['batch_start_date']))
            c.drawString(625, 277, str(student_data['batch_end_date']))
            
            # Additional info
            c.setFont("Helvetica", 12)
            c.drawString(50, 50, f"Batch: {student_data['batch_number']}")
            c.drawString(50, 35, f"ID: {student_data['sixerclass_id']}")
            c.drawString(400, 35, f"Issued: {datetime.now().strftime('%B %d, %Y')}")
            
            c.save()
            print(f"✅ Template-based certificate created: {output_path}")
            return True
            
        except Exception as e:
            print(f"❌ Certificate generation error: {e}")
            return False