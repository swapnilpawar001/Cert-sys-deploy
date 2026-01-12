import pandas as pd
from datetime import datetime

def create_excel_template():
    """Create an Excel template for student data import"""
    
    # Define the required columns
    columns = [
        'student_name',
        'batch_number', 
        'batch_start_date',
        'batch_end_date',
        'sixerclass_id'
    ]
    
    # Create sample data to show the format
    sample_data = [
        {
            'student_name': 'John Doe',
            'batch_number': 'AWS-2024-003',
            'batch_start_date': '2024-03-01',
            'batch_end_date': '2024-06-01',
            'sixerclass_id': 'SIX007'
        },
        {
            'student_name': 'Jane Smith',
            'batch_number': 'AWS-2024-003',
            'batch_start_date': '2024-03-01',
            'batch_end_date': '2024-06-01',
            'sixerclass_id': 'SIX008'
        },
        {
            'student_name': 'Mike Johnson',
            'batch_number': 'AWS-2024-004',
            'batch_start_date': '2024-04-01',
            'batch_end_date': '2024-07-01',
            'sixerclass_id': 'SIX009'
        }
    ]
    
    # Create DataFrame
    df = pd.DataFrame(sample_data)
    
    # Save to Excel with formatting
    filename = 'student_import_template.xlsx'
    
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        # Write sample data
        df.to_excel(writer, sheet_name='Sample Data', index=False)
        
        # Create empty template sheet
        empty_df = pd.DataFrame(columns=columns)
        empty_df.to_excel(writer, sheet_name='Import Template', index=False)
        
        # Create instructions sheet
        instructions = pd.DataFrame({
            'Instructions': [
                '1. Use the "Import Template" sheet to add your student data',
                '2. Required columns (do not change column names):',
                '   - student_name: Full name of the student',
                '   - batch_number: Training batch identifier (e.g., AWS-2024-003)',
                '   - batch_start_date: Start date in YYYY-MM-DD format',
                '   - batch_end_date: End date in YYYY-MM-DD format', 
                '   - sixerclass_id: Unique student ID (e.g., SIX007)',
                '',
                '3. Date format must be YYYY-MM-DD (e.g., 2024-03-01)',
                '4. SixerClass ID must be unique for each student',
                '5. Batch numbers should follow format: AWS-YYYY-XXX',
                '6. See "Sample Data" sheet for examples',
                '',
                '7. After filling data, upload this file to the admin panel',
                '8. The system will validate and import your students'
            ]
        })
        instructions.to_excel(writer, sheet_name='Instructions', index=False)
    
    print(f"✅ Excel template created: {filename}")
    print("📋 Template includes:")
    print("   - Sample Data sheet (with examples)")
    print("   - Import Template sheet (empty, ready for your data)")
    print("   - Instructions sheet (detailed guide)")
    print("\n📊 Required columns:")
    for i, col in enumerate(columns, 1):
        print(f"   {i}. {col}")
    
    return filename

if __name__ == "__main__":
    template_file = create_excel_template()
    print(f"\n🎯 Template ready: {template_file}")
    print("📤 Upload this file to: http://localhost:5000/admin/students")