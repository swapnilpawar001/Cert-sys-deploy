from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas
import os

def calibrate_positions():
    template_path = 'aws-final-deployment/certificate-templates/raw/certificate-template.png'
    
    if not os.path.exists(template_path):
        print("❌ Template not found")
        return
    
    # Get new template dimensions
    with Image.open(template_path) as img:
        width, height = img.size
        print(f"📐 New template dimensions: {width} x {height}")
    
    # Create calibration PDF with grid
    output_path = '/tmp/certificates/calibration_grid.pdf'
    os.makedirs('/tmp/certificates', exist_ok=True)
    
    c = canvas.Canvas(output_path, pagesize=(width, height))
    
    # Draw template
    c.drawImage(template_path, 0, 0, width=width, height=height)
    
    # Add grid lines every 50 pixels
    c.setStrokeColorRGB(1, 0, 0)  # Red lines
    c.setLineWidth(1)
    
    # Vertical lines
    for x in range(0, width, 50):
        c.line(x, 0, x, height)
        if x % 100 == 0:
            c.setFont("Helvetica", 8)
            c.setFillColorRGB(1, 0, 0)
            c.drawString(x+2, height-15, str(x))
    
    # Horizontal lines  
    for y in range(0, height, 50):
        c.line(0, y, width, y)
        if y % 100 == 0:
            c.setFont("Helvetica", 8)
            c.setFillColorRGB(1, 0, 0)
            c.drawString(5, y+2, str(y))
    
    # Add sample text at old positions to see offset
    c.setFont("Helvetica-Bold", 28)
    c.setFillColorRGB(0, 0, 1)  # Blue text
    c.drawString(405, 400, "SAMPLE NAME (405,400)")
    
    c.setFont("Helvetica", 18)
    c.drawString(345, 277, "START DATE (345,277)")
    c.drawString(625, 277, "END DATE (625,277)")
    
    c.save()
    print(f"✅ Calibration grid created: {output_path}")
    print("📋 Instructions:")
    print("1. Open the PDF to see where text appears on your template")
    print("2. Note the correct X,Y coordinates from the grid")
    print("3. Update the positions in certificate_generator.py")

if __name__ == "__main__":
    calibrate_positions()