import requests

# Test admin certificate generation (doesn't need session)
def test_admin_cert():
    print("🧪 Testing Admin Certificate Generation")
    
    student_data = {
        "student": {
            "student_name": "Rahul Sharma",
            "batch_number": "AWS-2024-001",
            "batch_start_date": "2024-01-15", 
            "batch_end_date": "2024-04-15",
            "sixerclass_id": "SIX001"
        }
    }
    
    try:
        response = requests.post(
            "http://localhost:5000/admin/api/generate-certificate",
            json=student_data
        )
        
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print(f"✅ Certificate generated: {result['filename']}")
                print(f"📄 Download URL: {result['download_url']}")
                return True
        
        return False
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_admin_cert()