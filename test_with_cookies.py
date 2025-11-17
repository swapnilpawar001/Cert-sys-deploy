#!/usr/bin/env python3
import requests
import json

def test_with_cookies():
    print("🎯 Testing Complete System with Cookie Support")
    print("="*50)
    
    # Create a session (handles cookies automatically)
    session = requests.Session()
    
    # Test data
    student = {
        'student_name': 'Rahul Sharma',
        'batch_number': 'AWS-2024-001',
        'sixerclass_id': 'SIX001'
    }
    
    print("Step 1: Authentication...")
    try:
        auth_response = session.post(
            'http://localhost:5000/api/authenticate',
            json=student,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if auth_response.status_code == 200:
            auth_data = auth_response.json()
            if auth_data.get('success'):
                print("✅ Authentication successful")
                print(f"Student: {auth_data['student']['student_name']}")
                
                print("\nStep 2: Certificate download (with cookies)...")
                download_response = session.post(
                    'http://localhost:5000/api/download-certificate',
                    headers={'Content-Type': 'application/json'},
                    timeout=15
                )
                
                if download_response.status_code == 200:
                    download_data = download_response.json()
                    if download_data.get('success'):
                        print("✅ Certificate generation successful")
                        
                        # Extract and test download URL
                        download_url = download_data['download_url']
                        print(f"Download URL: {download_url}")
                        
                        # Download the certificate
                        cert_response = session.get(f'http://localhost:5000{download_url}')
                        
                        if cert_response.status_code == 200:
                            print("✅ Certificate download successful")
                            
                            # Save certificate
                            with open('rahul_certificate_final.txt', 'w') as f:
                                f.write(cert_response.text)
                            
                            print("📄 Certificate saved as: rahul_certificate_final.txt")
                            print("Certificate content:")
                            print("="*30)
                            print(cert_response.text)
                            print("="*30)
                            print("🏆 Complete system test PASSED!")
                        else:
                            print(f"❌ Certificate download failed: {cert_response.status_code}")
                    else:
                        print(f"❌ Certificate generation failed: {download_data.get('error', 'Unknown error')}")
                else:
                    print(f"❌ Certificate generation HTTP error: {download_response.status_code}")
            else:
                print(f"❌ Authentication failed: {auth_data.get('error', 'Unknown error')}")
        else:
            print(f"❌ Authentication HTTP error: {auth_response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Flask server - is it running?")
    except Exception as e:
        print(f"❌ Test error: {e}")

if __name__ == "__main__":
    test_with_cookies()
