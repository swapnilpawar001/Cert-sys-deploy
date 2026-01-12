import requests

def test_full_flow():
    base_url = "http://localhost:5000"
    
    print("🧪 Testing Full Certificate Flow")
    print("=" * 40)
    
    # Create session to maintain cookies
    session = requests.Session()
    
    # Test student data
    student_data = {
        "student_name": "Rahul Sharma",
        "batch_number": "AWS-2024-001",
        "sixerclass_id": "SIX001"
    }
    
    print("1️⃣ Authenticating student...")
    try:
        auth_response = session.post(f"{base_url}/api/authenticate", json=student_data)
        print(f"Auth Status: {auth_response.status_code}")
        
        if auth_response.status_code == 200:
            result = auth_response.json()
            print(f"✅ Authentication: {result.get('success')}")
            
            print("\n2️⃣ Downloading certificate...")
            cert_response = session.post(f"{base_url}/api/download-certificate")
            print(f"Certificate Status: {cert_response.status_code}")
            
            if cert_response.status_code == 200:
                result = cert_response.json()
                print(f"✅ Certificate: {result}")
            else:
                print(f"❌ Certificate Error: {cert_response.text}")
        else:
            print(f"❌ Auth Error: {auth_response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_full_flow()