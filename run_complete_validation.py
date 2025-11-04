"""
MASTER VALIDATION SCRIPT
Runs complete Excel to Snowflake validation workflow in correct sequence

This script automates all validation steps:
1. Import Excel data to Snowflake
2. Quick validation check
3. Comprehensive Excel vs Snowflake comparison
4. Export Snowflake SQL queries
5. Optional: CSV vs Excel comparison (if CSV files edited)

Author: Bharat Varshney
Date: November 4, 2025
"""

import subprocess
import sys
from pathlib import Path
from datetime import datetime
import time

class ValidationWorkflow:
    """Complete validation workflow orchestrator"""
    
    def __init__(self):
        self.python_exe = sys.executable
        self.start_time = datetime.now()
        self.steps_completed = []
        self.steps_failed = []
        
    def print_header(self, step_number, title):
        """Print formatted step header"""
        print("\n" + "="*100)
        print(f"STEP {step_number}: {title}")
        print("="*100)
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("-"*100)
    
    def print_step_result(self, step_name, success, duration):
        """Print step completion status"""
        status = "SUCCESS" if success else "FAILED"
        symbol = "[+]" if success else "[X]"
        print(f"\n{symbol} {step_name}: {status} (Duration: {duration:.2f}s)")
        print("-"*100)
        
        if success:
            self.steps_completed.append(step_name)
        else:
            self.steps_failed.append(step_name)
    
    def run_script(self, script_name, step_name):
        """Run a Python script and return success status"""
        start = time.time()
        
        try:
            result = subprocess.run(
                [self.python_exe, script_name],
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            # Print script output
            if result.stdout:
                print(result.stdout)
            
            if result.stderr and result.returncode != 0:
                print(f"ERROR: {result.stderr}")
            
            duration = time.time() - start
            success = result.returncode == 0
            
            self.print_step_result(step_name, success, duration)
            
            return success
            
        except subprocess.TimeoutExpired:
            duration = time.time() - start
            print(f"ERROR: Script timed out after {duration:.2f}s")
            self.print_step_result(step_name, False, duration)
            return False
            
        except Exception as e:
            duration = time.time() - start
            print(f"ERROR: {str(e)}")
            self.print_step_result(step_name, False, duration)
            return False
    
    def check_file_exists(self, filename):
        """Check if required file exists"""
        return Path(filename).exists()
    
    def run_complete_workflow(self, include_csv_comparison=False):
        """Run complete validation workflow"""
        
        print("\n" + "="*100)
        print(" "*35 + "COMPLETE VALIDATION WORKFLOW")
        print(" "*30 + "Excel → Snowflake → Validation")
        print("="*100)
        print(f"Started: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*100)
        
        # ========================================
        # STEP 1: Import Excel to Snowflake
        # ========================================
        self.print_header(1, "IMPORT EXCEL DATA TO SNOWFLAKE")
        
        if not self.check_file_exists('import_complete_excel_to_snowflake.py'):
            print("[X] ERROR: import_complete_excel_to_snowflake.py not found!")
            self.print_step_result("Import Excel to Snowflake", False, 0)
        else:
            success = self.run_script(
                'import_complete_excel_to_snowflake.py',
                'Import Excel to Snowflake'
            )
            
            if not success:
                print("\n[!] WARNING: Import failed. Continuing with validation anyway...")
                print("[!] Validation will use existing Snowflake data if available.")
        
        # ========================================
        # STEP 2: Quick Validation Check
        # ========================================
        self.print_header(2, "QUICK VALIDATION CHECK (Row Counts)")
        
        if not self.check_file_exists('quick_validation.py'):
            print("[!] Skipping: quick_validation.py not found")
            print("[!] This is optional - continuing to next step...")
        else:
            self.run_script('quick_validation.py', 'Quick Validation Check')
        
        # ========================================
        # STEP 3: Comprehensive Excel vs Snowflake Comparison
        # ========================================
        self.print_header(3, "COMPREHENSIVE EXCEL vs SNOWFLAKE VALIDATION")
        
        if not self.check_file_exists('compare_excel_snowflake_reports.py'):
            print("[X] ERROR: compare_excel_snowflake_reports.py not found!")
            self.print_step_result("Excel vs Snowflake Validation", False, 0)
        else:
            self.run_script(
                'compare_excel_snowflake_reports.py',
                'Excel vs Snowflake Validation'
            )
        
        # ========================================
        # STEP 4: Export Snowflake SQL Queries
        # ========================================
        self.print_header(4, "EXPORT SNOWFLAKE SQL QUERIES TO EXCEL")
        
        if not self.check_file_exists('snowflake_queries_to_excel.py'):
            print("[!] Skipping: snowflake_queries_to_excel.py not found")
            print("[!] This is optional - continuing...")
        else:
            self.run_script(
                'snowflake_queries_to_excel.py',
                'Export Snowflake SQL Queries'
            )
        
        # ========================================
        # STEP 5: CSV vs Excel Comparison (Optional)
        # ========================================
        if include_csv_comparison:
            self.print_header(5, "CSV vs EXCEL COMPARISON (Color Coded)")
            
            if not self.check_file_exists('complete_data_comparison.py'):
                print("[!] Skipping: complete_data_comparison.py not found")
            else:
                self.run_script(
                    'complete_data_comparison.py',
                    'CSV vs Excel Comparison'
                )
        
        # ========================================
        # FINAL SUMMARY
        # ========================================
        self.print_final_summary()
    
    def print_final_summary(self):
        """Print final workflow summary"""
        end_time = datetime.now()
        total_duration = (end_time - self.start_time).total_seconds()
        
        print("\n\n" + "="*100)
        print(" "*40 + "WORKFLOW SUMMARY")
        print("="*100)
        
        print(f"\nStart Time: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"End Time:   {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Total Duration: {total_duration:.2f} seconds ({total_duration/60:.2f} minutes)")
        
        print(f"\n{'='*100}")
        print(f"COMPLETED STEPS ({len(self.steps_completed)}):")
        print(f"{'='*100}")
        
        if self.steps_completed:
            for i, step in enumerate(self.steps_completed, 1):
                print(f"  {i}. [+] {step}")
        else:
            print("  None")
        
        if self.steps_failed:
            print(f"\n{'='*100}")
            print(f"FAILED STEPS ({len(self.steps_failed)}):")
            print(f"{'='*100}")
            
            for i, step in enumerate(self.steps_failed, 1):
                print(f"  {i}. [X] {step}")
        
        print(f"\n{'='*100}")
        print("OUTPUT FILES LOCATION:")
        print(f"{'='*100}")
        print("  Folder: validation_reports/")
        print("\n  Expected files:")
        print("    - Excel_vs_Snowflake_Validation_*.xlsx")
        print("    - Snowflake_Validation_Queries_*.xlsx")
        print("    - Validation_Report_*.txt")
        print("    - Snowflake_SQL_Results_*.xlsx")
        print("    - CSV_vs_Excel_Comparison_ColorCoded_*.xlsx (if CSV comparison enabled)")
        
        print(f"\n{'='*100}")
        
        if not self.steps_failed:
            print("STATUS: ALL VALIDATIONS COMPLETED SUCCESSFULLY!")
            print(f"{'='*100}\n")
        else:
            print(f"STATUS: COMPLETED WITH {len(self.steps_failed)} FAILED STEP(S)")
            print(f"{'='*100}\n")
            print("Please review the failed steps above and check error messages.")
            print("You can run individual scripts manually if needed.\n")


def main():
    """Main entry point"""
    
    print("\n" + "="*100)
    print(" "*25 + "POWERBI AUTOMATION - COMPLETE VALIDATION WORKFLOW")
    print("="*100)
    
    # Ask user if they want CSV comparison
    print("\nDo you want to include CSV vs Excel comparison? (only if you edited CSV files)")
    print("  1. No - Standard workflow (Excel → Snowflake validation only)")
    print("  2. Yes - Include CSV vs Excel comparison with color coding")
    
    choice = input("\nEnter choice (1 or 2) [Default: 1]: ").strip()
    
    include_csv = False
    if choice == '2':
        include_csv = True
        print("\n[+] CSV comparison will be included in workflow")
    else:
        print("\n[+] Running standard Excel → Snowflake validation workflow")
    
    # Confirm before proceeding
    print("\n" + "-"*100)
    print("This will run the following steps in sequence:")
    print("  1. Import Excel data to Snowflake")
    print("  2. Quick validation check")
    print("  3. Comprehensive Excel vs Snowflake comparison")
    print("  4. Export Snowflake SQL queries")
    if include_csv:
        print("  5. CSV vs Excel comparison (color coded)")
    print("-"*100)
    
    proceed = input("\nProceed? (y/n) [Default: y]: ").strip().lower()
    
    if proceed and proceed != 'y':
        print("\n[!] Workflow cancelled by user.")
        return
    
    # Run workflow
    workflow = ValidationWorkflow()
    workflow.run_complete_workflow(include_csv_comparison=include_csv)


if __name__ == "__main__":
    main()
