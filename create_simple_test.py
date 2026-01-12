import pandas as pd

# Create simple test data
test_data = [
    {
        'student_name': 'Test Student',
        'batch_number': 'AWS-2024-TEST',
        'batch_start_date': '2024-12-01',
        'batch_end_date': '2025-03-01',
        'sixerclass_id': 'TEST999'
    }
]

df = pd.DataFrame(test_data)
df.to_excel('simple_test.xlsx', index=False)
print("✅ Simple test file created: simple_test.xlsx")