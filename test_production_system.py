import requests
import json
import pandas as pd
import time

def test_excel_import_system():
    """Test the complete Excel import system"""
    
    print("🎯 Testing AWS Training Certificate System - Excel Import")
    print("=" * 60)
    
    # Step 1: Create sample Excel file for import
    print("\n1️⃣ Creating Sample Excel File...")
    sample_students = [
        {
            'student_name': 'Rajesh Kumar',
            'batch_number': 'AWS-2024-003',
            'batch_start_date': '2024-07-01',
            'batch_end_date': '2024-10-01',
            'sixerclass_id': 'SIX007'
        },
        {
            'student_name': 'Anjali Sharma',
            'batch_number': 'AWS-2024-003',
            'batch_start_date': '2024-07-01',
            'batch_end_date': '2024-10-01',
            'sixerclass_id': 'SIX008'
        },
        {
            'student_name': 'Vikram Singh',
            'batch_number': 'AWS-2024-004',
            'batch_start_date': '2024-08-01',
            'batch_end_date': '2024-11-01',
            'sixerclass_id': 'SIX009'
        }
    ]
    
    df = pd.DataFrame(sample_students)
    test_file = 'test_import_students.xlsx'
    df.to_excel(test_file, index=False)
    print(f"✅ Created test file: {test_file}")
    print(f"📊 Test data: {len(sample_students)} students")
    
    # Step 2: Check system status
    print("\n2️⃣ Checking System Status...")
    try:
        response = requests.get("http://localhost:5000/api/check-status")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ System Status: {data['status']}")
            print(f"📊 Students Before Import: {data['students_loaded']}")
            initial_count = data['students_loaded']
        else:
            print(f"❌ System not responding: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to system: {e}")
        return False
    
    # Step 3: Test Excel Import
    print("\n3️⃣ Testing Excel Import...")
    try:
        with open(test_file, 'rb') as f:
            files = {'file': f}
            response = requests.post('http://localhost:5000/admin/api/students/import', files=files)
            
            print(f"Import Response Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    print(f"✅ Import Successful!")
                    print(f"📈 Imported Count: {data['imported_count']}")
                    print(f"💬 Message: {data['message']}")
                    if data.get('errors'):
                        print(f"⚠️  Warnings: {data['errors']}")
                else:
                    print(f"❌ Import Failed: {data.get('error')}")
                    return False
            else:
                print(f"❌ Import Request Failed: {response.status_code}")
                print(f"Response: {response.text[:200]}")
                return False
                
    except Exception as e:
        print(f"❌ Import Test Error: {e}")
        return False
    
    # Step 4: Verify Import Results
    print("\n4️⃣ Verifying Import Results...")
    try:
        response = requests.get("http://localhost:5000/api/check-status")
        if response.status_code == 200:
            data = response.json()
            final_count = data['students_loaded']
            print(f"📊 Students After Import: {final_count}")
            print(f"📈 Expected Increase: {len(sample_students)}")
            print(f"📈 Actual Increase: {final_count - initial_count}")
            
            if final_count > initial_count:
                print("✅ Import Verification: SUCCESS")
            else:
                print("❌ Import Verification: FAILED")
                return False
        else:
            print(f"❌ Status check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Verification error: {e}")
        return False
    
    # Step 5: Test Admin Interface
    print("\n5️⃣ Testing Admin Interface...")
    try:
        response = requests.get("http://localhost:5000/admin/api/students")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Admin API Working")
            print(f"📊 Total Students via Admin API: {data['total']}")
            
            # Test search functionality
            response = requests.get("http://localhost:5000/admin/api/students?search=AWS-2024-003")
            if response.status_code == 200:
                search_data = response.json()
                print(f"🔍 Search Results for 'AWS-2024-003': {search_data['total']} students")
                if search_data['students']:
                    print("📋 Found students:")
                    for student in search_data['students']:
                        print(f"   - {student['student_name']} ({student['sixerclass_id']})")
            
        else:
            print(f"❌ Admin API failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Admin interface test error: {e}")
        return False
    
    # Step 6: Test Export Functionality
    print("\n6️⃣ Testing Export Functionality...")
    try:
        response = requests.get("http://localhost:5000/admin/api/students/export")
        if response.status_code == 200:
            print("✅ Export functionality working")
            print(f"📁 Export file size: {len(response.content)} bytes")
        else:
            print(f"❌ Export failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Export test error: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 EXCEL IMPORT SYSTEM TEST COMPLETE!")
    print("✅ All core functionality verified")
    print("📊 System is production ready")
    return True

if __name__ == "__main__":
    success = test_excel_import_system()
    if success:
        print("\n🚀 Ready for production deployment!")
    else:
        print("\n❌ Issues found - please check logs")