import requests
import time

def test_certificate_system():
    base_url = "http://localhost:5000"
    
    print("🧪 Testing Certificate Generation System")
    print("=" * 50)
    
    # Test 1: Check system status
    print("\n1️⃣ System Status Check...")
    try:
        response = requests.get(f"{base_url}/api/check-status")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Status: {data['status']}")
            print(f"📊 Students: {data['students_loaded']}")
        else:
            print(f"❌ Status check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect: {e}")
        return False
    
    # Test 2: Student authentication and certificate download
    print("\n2️⃣ Testing Student Authentication & Certificate...")
    test_student = {
        "student_name": "Rahul Sharma",
        "batch_number": "AWS-2024-001", 
        "sixerclass_id": "SIX001"
    }
    
    try:
        # Authenticate
        auth_response = requests.post(f"{base_url}/api/authenticate", 
                                    json=test_student)
        
        if auth_response.status_code == 200:
            print("✅ Authentication successful")
            
            # Get session cookies
            session = requests.Session()
            session.post(f"{base_url}/api/authenticate", json=test_student)
            
            # Download certificate
            cert_response = session.post(f"{base_url}/api/download-certificate")
            
            if cert_response.status_code == 200:
                result = cert_response.json()
                if result.get('success'):
                    print(f"✅ Certificate generated: {result['filename']}")
                    print(f"📄 Download URL: {result['download_url']}")
                else:
                    print(f"❌ Certificate failed: {result.get('error')}")
            else:
                print(f"❌ Certificate request failed: {cert_response.status_code}")
        else:
            print(f"❌ Authentication failed: {auth_response.status_code}")
    except Exception as e:
        print(f"❌ Certificate test error: {e}")
    
    # Test 3: Admin certificate generation
    print("\n3️⃣ Testing Admin Certificate Generation...")
    try:
        admin_data = {"student": test_student}
        admin_response = requests.post(f"{base_url}/admin/api/generate-certificate",
                                     json=admin_data)
        
        if admin_response.status_code == 200:
            result = admin_response.json()
            if result.get('success'):
                print(f"✅ Admin certificate generated: {result['filename']}")
            else:
                print(f"❌ Admin certificate failed: {result.get('error')}")
        else:
            print(f"❌ Admin request failed: {admin_response.status_code}")
    except Exception as e:
        print(f"❌ Admin test error: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 Test Complete!")
    print("Visit http://localhost:5000 to test manually")

if __name__ == "__main__":
    test_certificate_system()