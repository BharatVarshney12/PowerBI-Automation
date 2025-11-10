"""
Main Entry Point for DataComPy Validation
Run Excel vs CSV comparisons with report generation
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from datacompy_validation.excel_csv_comparator import ExcelCSVComparator
from datacompy_validation.report_generator import DataComPyReportGenerator
from datacompy_validation.config import COMPARISON_CONFIG, OUTPUT_FOLDER


def run_single_comparison(table_key: str):
    """
    Run comparison for a single table
    
    Args:
        table_key: Table name from COMPARISON_CONFIG
    """
    print(f"\n{'='*100}")
    print(f" RUNNING DATACOMPY VALIDATION: {table_key}")
    print(f"{'='*100}\n")
    
    # Create comparator
    comparator = ExcelCSVComparator()
    
    try:
        # Run comparison
        compare = comparator.compare(table_key)
        
        # Generate reports
        report_gen = DataComPyReportGenerator()
        
        print(f"\n📄 Generating reports...")
        report_gen.save_text_report(compare, table_key)
        report_gen.save_excel_report(compare, table_key)
        
        return compare
        
    except FileNotFoundError as e:
        print(f"\n❌ ERROR: {e}")
        print(f"\n💡 Make sure you have:")
        config = COMPARISON_CONFIG[table_key]
        print(f"   - Excel file: power bi actual report/{config['excel_file']}")
        print(f"   - CSV file: data/downloads/{config['csv_file']}")
        print(f"\nTo create CSV file, export Snowflake table to CSV format.")
        return None
    
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()
        return None


def run_all_comparisons():
    """Run comparisons for all configured tables"""
    print(f"\n{'='*100}")
    print(f" RUNNING ALL DATACOMPY VALIDATIONS")
    print(f"{'='*100}\n")
    
    # Create comparator
    comparator = ExcelCSVComparator()
    
    # Run all comparisons
    results = comparator.compare_all_tables()
    
    # Generate all reports
    if results:
        report_gen = DataComPyReportGenerator()
        report_gen.save_all_reports(results)
    
    return results


def interactive_menu():
    """Interactive menu for choosing what to compare"""
    print(f"\n{'='*100}")
    print(f" DATACOMPY EXCEL vs CSV VALIDATION")
    print(f"{'='*100}\n")
    
    print("Available tables:")
    tables = list(COMPARISON_CONFIG.keys())
    for i, table in enumerate(tables, 1):
        print(f"  {i}. {table}")
    print(f"  {len(tables) + 1}. Compare ALL tables")
    print(f"  0. Exit")
    
    print()
    choice = input("Select option (0-{}): ".format(len(tables) + 1))
    
    try:
        choice = int(choice)
        
        if choice == 0:
            print("\n👋 Goodbye!")
            return
        
        elif choice == len(tables) + 1:
            run_all_comparisons()
        
        elif 1 <= choice <= len(tables):
            table_key = tables[choice - 1]
            run_single_comparison(table_key)
        
        else:
            print(f"\n❌ Invalid choice. Please select 0-{len(tables) + 1}")
            
    except ValueError:
        print("\n❌ Invalid input. Please enter a number.")


def show_instructions():
    """Show setup instructions"""
    print(f"\n{'='*100}")
    print(f" SETUP INSTRUCTIONS")
    print(f"{'='*100}\n")
    
    print("Before running comparisons, you need CSV files from Snowflake:")
    print()
    
    print("METHOD 1: Export from Snowflake UI")
    print("  1. Login to Snowflake")
    print("  2. Run: SELECT * FROM POWERBI_LEARNING.TRAINING_POWERBI.SPEND_BY_CODE")
    print("  3. Click 'Download Results' → Choose 'CSV'")
    print("  4. Save to: data/downloads/spend_by_code.csv")
    print("  5. Repeat for other tables")
    print()
    
    print("METHOD 2: Use Python script (if you have one)")
    print("  - Use your existing Snowflake connector")
    print("  - Export queries to CSV format")
    print("  - Save in data/downloads/ folder")
    print()
    
    print("Required CSV files:")
    for table_key, config in COMPARISON_CONFIG.items():
        print(f"  ✓ data/downloads/{config['csv_file']}")
    print()
    
    print("Excel files (already available):")
    for table_key, config in COMPARISON_CONFIG.items():
        print(f"  ✓ power bi actual report/{config['excel_file']}")
    print()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='DataComPy Excel vs CSV Validation')
    parser.add_argument('--table', type=str, help='Specific table to compare')
    parser.add_argument('--all', action='store_true', help='Compare all tables')
    parser.add_argument('--instructions', action='store_true', help='Show setup instructions')
    
    args = parser.parse_args()
    
    if args.instructions:
        show_instructions()
    
    elif args.table:
        if args.table in COMPARISON_CONFIG:
            run_single_comparison(args.table)
        else:
            print(f"❌ Unknown table: {args.table}")
            print(f"Available tables: {', '.join(COMPARISON_CONFIG.keys())}")
    
    elif args.all:
        run_all_comparisons()
    
    else:
        # Interactive mode
        interactive_menu()
    
    print(f"\n{'='*100}")
    print(f"📁 Reports saved in: {OUTPUT_FOLDER}")
    print(f"{'='*100}\n")
