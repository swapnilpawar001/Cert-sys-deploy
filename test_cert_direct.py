from certificate_generator import CertificateGenerator
import os

# Test certificate generation directly
cert_gen = CertificateGenerator()

test_student = {
    'student_name': 'Test Student',
    'batch_number': 'AWS-2024-001',
    'batch_start_date': '2024-01-15',
    'batch_end_date': '2024-04-15',
    'sixerclass_id': 'TEST001'
}

output_path = '/tmp/certificates/test_certificate.pdf'
os.makedirs('/tmp/certificates', exist_ok=True)

print("Testing certificate generation...")
success = cert_gen.create_certificate(test_student, output_path)

if success:
    print(f"✅ Certificate created: {output_path}")
    print(f"File exists: {os.path.exists(output_path)}")
    if os.path.exists(output_path):
        print(f"File size: {os.path.getsize(output_path)} bytes")
else:
    print("❌ Certificate generation failed")