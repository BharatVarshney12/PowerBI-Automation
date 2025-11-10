"""
Demo: Excel vs CSV Comparison using DataComPy
Shows how to compare your actual Excel and CSV files
"""
import pandas as pd
import datacompy
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from datacompy_validation.excel_csv_comparator import ExcelCSVComparator, quick_compare
from datacompy_validation.report_generator import DataComPyReportGenerator


def demo_simple_excel_csv_comparison():
    """Simple Excel vs CSV comparison example"""
    print("\n" + "="*80)
    print("DEMO: Simple Excel vs CSV Comparison")
    print("="*80 + "\n")
    
    # Create sample Excel data
    excel_data = pd.DataFrame({
        'CLAIM_FORM_TYPE': ['DENTAL', 'OPTICAL', 'MEDICAL'],
        'NET_SPEND': [5000.50, 3500.75, 12000.25],
        'GROSS_SPEND': [6000.00, 4000.00, 14000.00]
    })
    
    # Create sample CSV data (with small differences)
    csv_data = pd.DataFrame({
        'CLAIM_FORM_TYPE': ['DENTAL', 'OPTICAL', 'MEDICAL'],
        'NET_SPEND': [5000.52, 3500.75, 12000.30],  # Slightly different
        'GROSS_SPEND': [6000.00, 4000.00, 14000.00]
    })
    
    print("Sample Excel Data:")
    print(excel_data)
    print("\nSample CSV Data:")
    print(csv_data)
    
    # Compare using datacompy
    compare = datacompy.Compare(
        df1=excel_data,
        df2=csv_data,
        join_columns=['CLAIM_FORM_TYPE'],
        abs_tol=0.01,  # 1 cent tolerance
        df1_name='Excel',
        df2_name='CSV'
    )
    
    print("\n" + "-"*80)
    print("DataComPy Report:")
    print("-"*80)
    print(compare.report())
    
    # Show mismatches
    if not compare.matches():
        print("\n" + "-"*80)
        print("Detailed Mismatches:")
        print("-"*80)
        print(compare.all_mismatch())


def demo_with_actual_files():
    """
    Demo with actual Excel and CSV files
    NOTE: This requires CSV files to exist in data/downloads/
    """
    print("\n" + "="*80)
    print("DEMO: Comparing Actual Excel and CSV Files")
    print("="*80 + "\n")
    
    print("⚠ NOTE: This demo requires CSV files exported from Snowflake")
    print("   Expected location: data/downloads/")
    print("   Files needed:")
    print("     - spend_by_code.csv")
    print("     - spend_by_product_type.csv")
    print("     - spend_by_bill_type.csv")
    print()
    
    comparator = ExcelCSVComparator()
    
    # Try to compare SPEND_BY_CODE
    try:
        print("Attempting to compare SPEND_BY_CODE...")
        compare = comparator.compare('SPEND_BY_CODE')
        
        # Generate reports
        print("\nGenerating reports...")
        report_gen = DataComPyReportGenerator()
        report_gen.save_text_report(compare, 'SPEND_BY_CODE')
        report_gen.save_excel_report(compare, 'SPEND_BY_CODE')
        
    except FileNotFoundError as e:
        print(f"❌ {e}")
        print("\n💡 To run this demo:")
        print("   1. Export Snowflake tables to CSV format")
        print("   2. Save them in data/downloads/ folder")
        print("   3. Run this demo again")


def demo_quick_compare():
    """Demo the quick_compare convenience function"""
    print("\n" + "="*80)
    print("DEMO: Quick Compare Function")
    print("="*80 + "\n")
    
    print("The quick_compare() function allows one-line comparisons:")
    print()
    print("Example code:")
    print("-" * 80)
    print("""
    from datacompy_validation.excel_csv_comparator import quick_compare
    
    compare = quick_compare(
        excel_file='spend by code.xlsx',
        csv_file='spend_by_code.csv',
        join_columns=['CLAIM_FORM_TYPE'],
        abs_tol=0.01
    )
    """)
    print("-" * 80)


def show_comparison_workflow():
    """Show the complete comparison workflow"""
    print("\n" + "="*80)
    print("COMPLETE EXCEL vs CSV COMPARISON WORKFLOW")
    print("="*80 + "\n")
    
    print("Step-by-step workflow:")
    print()
    
    print("1️⃣ PREPARE DATA")
    print("   - Excel files: Already in 'power bi actual report' folder")
    print("   - CSV files: Export from Snowflake to 'data/downloads' folder")
    print()
    
    print("2️⃣ LOAD DATA")
    print("   comparator = ExcelCSVComparator()")
    print("   compare = comparator.compare('SPEND_BY_CODE')")
    print()
    
    print("3️⃣ REVIEW RESULTS")
    print("   - DataComPy automatically:")
    print("     • Compares row counts")
    print("     • Checks column schemas")
    print("     • Identifies missing rows")
    print("     • Finds value mismatches")
    print("     • Calculates match percentages")
    print()
    
    print("4️⃣ GENERATE REPORTS")
    print("   report_gen = DataComPyReportGenerator()")
    print("   report_gen.save_text_report(compare, 'table_name')")
    print("   report_gen.save_excel_report(compare, 'table_name')")
    print()
    
    print("5️⃣ ANALYZE OUTPUT")
    print("   - Text report: Quick overview")
    print("   - Excel report: Detailed analysis with multiple sheets:")
    print("     • Summary: Overall statistics")
    print("     • Mismatches: Rows with differences")
    print("     • Only_in_Excel: Missing from CSV")
    print("     • Only_in_CSV: Missing from Excel")
    print("     • Column_Statistics: Per-column match rates")
    print()


def show_benefits():
    """Show benefits of datacompy approach"""
    print("\n" + "="*80)
    print("WHY USE DATACOMPY FOR EXCEL VS CSV COMPARISON?")
    print("="*80 + "\n")
    
    print("✅ BENEFITS:")
    print()
    
    print("1. Automatic Schema Comparison")
    print("   - Detects missing/extra columns")
    print("   - No manual column checking needed")
    print()
    
    print("2. Smart Numeric Tolerance")
    print("   - Handles floating-point precision issues")
    print("   - Configurable tolerance (e.g., 0.01 for 1 cent)")
    print()
    
    print("3. Row-Level Matching")
    print("   - Joins on key columns")
    print("   - Identifies missing rows in either file")
    print()
    
    print("4. Detailed Statistics")
    print("   - Match rate per column")
    print("   - Overall comparison summary")
    print("   - Mismatch counts")
    print()
    
    print("5. Less Code to Write")
    print("   - 10 lines vs 100+ lines manual comparison")
    print("   - Built-in report generation")
    print()
    
    print("6. Industry Standard")
    print("   - Well-tested library")
    print("   - Used by Capital One and others")
    print("   - Maintained and documented")
    print()
    
    print("\n📊 COMPARISON:")
    print()
    print("Manual Approach:")
    print("  - Load Excel → Load CSV → Clean both → Loop rows →")
    print("    Loop columns → Check each value → Track differences →")
    print("    Format output → Generate Excel → Add colors → Save")
    print()
    print("DataComPy Approach:")
    print("  - Load Excel → Load CSV → datacompy.Compare() → Done!")
    print()


if __name__ == "__main__":
    print("\n" + "="*100)
    print(" EXCEL vs CSV COMPARISON DEMOS")
    print("="*100)
    
    demo_simple_excel_csv_comparison()
    demo_quick_compare()
    show_comparison_workflow()
    show_benefits()
    demo_with_actual_files()
    
    print("\n" + "="*100)
    print(" DEMOS COMPLETE!")
    print("="*100)
    print("\nNext step: Run run_comparison.py with your actual data!")
