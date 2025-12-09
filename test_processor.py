"""
Test script to verify the data processor works with the example file.
"""

from data_processor import OvertimeProcessor

def test_processor():
    """Test the overtime processor with the example file."""
    print("Testing Overtime Processor...")
    print("=" * 50)
    
    processor = OvertimeProcessor()
    
    try:
        # Process the example file
        file_path = "OCTOBER OVERTIME - CN V3 - 27 NOV 2025.xlsx"
        print(f"\nProcessing file: {file_path}")
        data = processor.process_all_sheets(file_path)
        
        print(f"\n✓ Successfully processed {len(data)} records")
        print(f"  Columns: {list(data.columns)}")
        
        # Get summaries
        print("\n" + "=" * 50)
        print("Employee Summary (Top 5):")
        print("=" * 50)
        emp_summary = processor.get_summary_by_employee()
        print(emp_summary.head().to_string())
        
        print("\n" + "=" * 50)
        print("Monthly Summary:")
        print("=" * 50)
        month_summary = processor.get_summary_by_month()
        print(month_summary.to_string())
        
        print("\n" + "=" * 50)
        print("Overall Statistics:")
        print("=" * 50)
        total_overtime = data['OVERTIME_HOURS_DECIMAL'].sum()
        total_hours = data['HOURS_WORKED_DECIMAL'].sum()
        unique_employees = data['PIN CODE'].nunique()
        
        print(f"Total Overtime Hours: {total_overtime:.2f}")
        print(f"Total Hours Worked: {total_hours:.2f}")
        print(f"Unique Employees: {unique_employees}")
        print(f"Total Records: {len(data)}")
        
        print("\n" + "=" * 50)
        print("✓ All tests passed!")
        
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_processor()


