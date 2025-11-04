"""
PowerBI Validation Workflow with Allure Reporting
=================================================
Runs complete validation workflow and generates beautiful Allure reports for stakeholders.

Features:
- Step-by-step validation execution tracking
- Rich HTML reports with screenshots and attachments
- Pass/Fail status for each validation step
- Execution time tracking
- Export validation files as report attachments
- Stakeholder-friendly presentation

Author: Bharat Varshney
Date: November 2025
"""

import subprocess
import sys
import time
from pathlib import Path
from datetime import datetime
import json
import shutil

class AllureValidationRunner:
    def __init__(self):
        self.python_exe = sys.executable
        self.project_root = Path(__file__).parent
        self.allure_results = self.project_root / "reports" / "allure-results"
        self.allure_report = self.project_root / "reports" / "allure-report"
        self.validation_reports = self.project_root / "validation_reports"
        
        # Clear old Allure results
        if self.allure_results.exists():
            shutil.rmtree(self.allure_results)
        self.allure_results.mkdir(parents=True, exist_ok=True)
        
        self.results = []
        self.start_time = None
        self.end_time = None
        
    def print_header(self):
        print("=" * 100)
        print("POWERBI VALIDATION WORKFLOW WITH ALLURE REPORTING".center(100))
        print("=" * 100)
        print(f"\nStarted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
    def run_validation_step(self, step_name, script_name, description):
        """Run a single validation step and track results"""
        print(f"\n{'='*100}")
        print(f"STEP: {step_name}")
        print(f"{'='*100}")
        print(f"Description: {description}")
        print(f"Script: {script_name}")
        print(f"{'-'*100}")
        
        start_time = time.time()
        
        try:
            result = subprocess.run(
                [self.python_exe, script_name],
                capture_output=True,
                text=True,
                timeout=300,
                encoding='utf-8',
                errors='replace'
            )
            
            duration = time.time() - start_time
            
            # Check if script succeeded
            success = result.returncode == 0
            
            step_result = {
                'name': step_name,
                'script': script_name,
                'description': description,
                'status': 'passed' if success else 'failed',
                'duration': duration,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode
            }
            
            self.results.append(step_result)
            
            if success:
                print(f"\n[✓] {step_name}: SUCCESS (Duration: {duration:.2f}s)")
            else:
                print(f"\n[✗] {step_name}: FAILED (Duration: {duration:.2f}s)")
                print(f"Error: {result.stderr[:500]}")
            
            print(f"{'-'*100}")
            
            return step_result
            
        except subprocess.TimeoutExpired:
            duration = time.time() - start_time
            step_result = {
                'name': step_name,
                'script': script_name,
                'description': description,
                'status': 'failed',
                'duration': duration,
                'stdout': '',
                'stderr': 'Script timeout (exceeded 300 seconds)',
                'returncode': -1
            }
            self.results.append(step_result)
            print(f"\n[✗] {step_name}: TIMEOUT (Duration: {duration:.2f}s)")
            return step_result
            
        except Exception as e:
            duration = time.time() - start_time
            step_result = {
                'name': step_name,
                'script': script_name,
                'description': description,
                'status': 'failed',
                'duration': duration,
                'stdout': '',
                'stderr': str(e),
                'returncode': -1
            }
            self.results.append(step_result)
            print(f"\n[✗] {step_name}: ERROR - {str(e)}")
            return step_result
    
    def create_allure_test_case(self, step_result):
        """Create Allure test case JSON for a validation step"""
        test_uuid = f"test-{step_result['name'].lower().replace(' ', '-')}"
        
        # Determine status
        status = "passed" if step_result['status'] == 'passed' else "failed"
        
        # Create test result
        test_result = {
            "uuid": test_uuid,
            "historyId": step_result['name'],
            "fullName": f"Validation.{step_result['name']}",
            "labels": [
                {"name": "suite", "value": "PowerBI Validation Workflow"},
                {"name": "feature", "value": "Data Validation"},
                {"name": "story", "value": step_result['name']},
                {"name": "severity", "value": "critical"}
            ],
            "links": [],
            "name": step_result['name'],
            "status": status,
            "statusDetails": {
                "message": step_result['description'],
                "trace": step_result['stderr'] if status == "failed" else ""
            },
            "stage": "finished",
            "steps": [],
            "attachments": [],
            "start": int(self.start_time * 1000),
            "stop": int((self.start_time + step_result['duration']) * 1000)
        }
        
        # Save test result to Allure results
        result_file = self.allure_results / f"{test_uuid}-result.json"
        with open(result_file, 'w') as f:
            json.dump(test_result, f, indent=2)
        
        # Save output as attachment if available
        if step_result['stdout']:
            attachment_file = self.allure_results / f"{test_uuid}-output.txt"
            with open(attachment_file, 'w', encoding='utf-8', errors='replace') as f:
                f.write(step_result['stdout'])
            
            # Update test result with attachment
            test_result['attachments'].append({
                "name": "Console Output",
                "source": f"{test_uuid}-output.txt",
                "type": "text/plain"
            })
            
            with open(result_file, 'w') as f:
                json.dump(test_result, f, indent=2)
    
    def attach_validation_reports(self):
        """Attach validation report files to Allure"""
        if not self.validation_reports.exists():
            return
            
        print(f"\n{'='*100}")
        print("ATTACHING VALIDATION REPORTS TO ALLURE".center(100))
        print(f"{'='*100}\n")
        
        # Find latest validation files
        excel_files = list(self.validation_reports.glob("*.xlsx"))
        txt_files = list(self.validation_reports.glob("*.txt"))
        
        attached_count = 0
        
        for file in excel_files + txt_files:
            if file.name.startswith('~$'):  # Skip Excel temp files
                continue
                
            # Copy to allure-results
            dest = self.allure_results / file.name
            try:
                shutil.copy2(file, dest)
                attached_count += 1
                print(f"  ✓ Attached: {file.name}")
            except Exception as e:
                print(f"  ✗ Failed to attach {file.name}: {e}")
        
        print(f"\nTotal files attached: {attached_count}")
    
    def generate_allure_report(self):
        """Generate Allure HTML report"""
        print(f"\n{'='*100}")
        print("GENERATING ALLURE REPORT".center(100))
        print(f"{'='*100}\n")
        
        try:
            # Check if allure command is available
            result = subprocess.run(
                ["allure", "--version"],
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                print("⚠ Allure CLI not found!")
                print("\nTo install Allure CLI:")
                print("  1. Download from: https://github.com/allure-framework/allure2/releases")
                print("  2. Or install via Scoop: scoop install allure")
                print("  3. Or install via npm: npm install -g allure-commandline")
                print(f"\nAllure results saved in: {self.allure_results}")
                print("You can generate report manually: allure serve reports/allure-results")
                return False
            
            # Generate report
            print("Generating Allure HTML report...")
            result = subprocess.run(
                ["allure", "generate", str(self.allure_results), "-o", str(self.allure_report), "--clean"],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print(f"\n✓ Allure report generated successfully!")
                print(f"Report location: {self.allure_report}")
                print(f"\nTo view report, run: allure open {self.allure_report}")
                return True
            else:
                print(f"✗ Failed to generate report: {result.stderr}")
                return False
                
        except FileNotFoundError:
            print("⚠ Allure CLI not found!")
            print("\nTo install Allure CLI:")
            print("  1. Download from: https://github.com/allure-framework/allure2/releases")
            print("  2. Or install via Scoop: scoop install allure")
            print("  3. Or install via npm: npm install -g allure-commandline")
            print(f"\nAllure results saved in: {self.allure_results}")
            print("You can generate report manually: allure serve reports/allure-results")
            return False
    
    def run_complete_workflow(self, include_csv_comparison=False):
        """Run complete validation workflow with Allure reporting"""
        self.print_header()
        self.start_time = time.time()
        
        # Define validation steps
        steps = [
            {
                'name': 'Import Excel to Snowflake',
                'script': 'import_complete_excel_to_snowflake.py',
                'description': 'Import Power BI Excel reports into Snowflake database tables'
            },
            {
                'name': 'Quick Row Count Validation',
                'script': 'quick_validation.py',
                'description': 'Fast validation comparing row counts between Excel and Snowflake'
            },
            {
                'name': 'Comprehensive Excel vs Snowflake Validation',
                'script': 'compare_excel_snowflake_reports.py',
                'description': 'Cell-by-cell comparison of Excel reports against Snowflake data'
            },
            {
                'name': 'Export Snowflake SQL Queries',
                'script': 'snowflake_queries_to_excel.py',
                'description': 'Export all SQL queries and results from Snowflake to Excel'
            }
        ]
        
        if include_csv_comparison:
            steps.append({
                'name': 'CSV vs Excel Comparison',
                'script': 'complete_data_comparison.py',
                'description': 'Color-coded comparison between CSV exports and Excel reports'
            })
        
        # Run each validation step
        for step in steps:
            step_result = self.run_validation_step(
                step['name'],
                step['script'],
                step['description']
            )
            self.create_allure_test_case(step_result)
        
        self.end_time = time.time()
        
        # Attach validation reports
        self.attach_validation_reports()
        
        # Print summary
        self.print_summary()
        
        # Generate Allure report
        self.generate_allure_report()
    
    def print_summary(self):
        """Print execution summary"""
        print(f"\n{'='*100}")
        print("VALIDATION WORKFLOW SUMMARY".center(100))
        print(f"{'='*100}\n")
        
        total_duration = self.end_time - self.start_time
        passed = sum(1 for r in self.results if r['status'] == 'passed')
        failed = sum(1 for r in self.results if r['status'] == 'failed')
        
        print(f"Start Time: {datetime.fromtimestamp(self.start_time).strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"End Time:   {datetime.fromtimestamp(self.end_time).strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Total Duration: {total_duration:.2f} seconds ({total_duration/60:.2f} minutes)\n")
        
        print(f"{'='*100}")
        print(f"RESULTS: {passed} PASSED | {failed} FAILED")
        print(f"{'='*100}\n")
        
        for result in self.results:
            status_icon = "✓" if result['status'] == 'passed' else "✗"
            status_text = "PASSED" if result['status'] == 'passed' else "FAILED"
            print(f"  [{status_icon}] {result['name']}: {status_text} ({result['duration']:.2f}s)")
        
        print(f"\n{'='*100}")
        if failed == 0:
            print("STATUS: ALL VALIDATIONS PASSED ✓".center(100))
        else:
            print(f"STATUS: {failed} VALIDATION(S) FAILED ✗".center(100))
        print(f"{'='*100}\n")


def main():
    """Main execution function"""
    print("\n" + "="*100)
    print("POWERBI VALIDATION WITH ALLURE REPORTING".center(100))
    print("="*100 + "\n")
    
    # Ask user for workflow options
    print("Do you want to include CSV vs Excel comparison?")
    print("  1. No - Standard workflow (Excel → Snowflake validation only)")
    print("  2. Yes - Include CSV vs Excel comparison with color coding")
    
    choice = input("\nEnter choice (1 or 2) [Default: 1]: ").strip()
    include_csv = choice == "2"
    
    if include_csv:
        print("\n[+] CSV comparison will be included in workflow")
    
    # Confirm execution
    print("\n" + "-"*100)
    print("\nThis will run the complete validation workflow and generate Allure report")
    print("for stakeholder review.\n")
    
    proceed = input("Proceed? (y/n) [Default: y]: ").strip().lower()
    if proceed and proceed != 'y':
        print("\n[!] Workflow cancelled by user")
        return
    
    # Run workflow
    runner = AllureValidationRunner()
    runner.run_complete_workflow(include_csv_comparison=include_csv)
    
    print("\n" + "="*100)
    print("WORKFLOW COMPLETED".center(100))
    print("="*100)
    print("\nNext Steps:")
    print("  1. Review Allure report for stakeholder presentation")
    print("  2. Check validation_reports/ folder for detailed Excel reports")
    print("  3. Share Allure HTML report with stakeholders")
    print("\n")


if __name__ == "__main__":
    main()
