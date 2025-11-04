"""
Quick Test - Run all validation steps without user prompts
"""
import subprocess
import sys
from pathlib import Path

python_exe = sys.executable
scripts = [
    ('import_complete_excel_to_snowflake.py', 'Import Excel to Snowflake'),
    ('quick_validation.py', 'Quick Validation'),
    ('compare_excel_snowflake_reports.py', 'Excel vs Snowflake Validation'),
    ('snowflake_queries_to_excel.py', 'Export SQL Queries'),
]

print("="*100)
print(" "*30 + "TESTING ALL VALIDATION SCRIPTS")
print("="*100)

results = []

for script, name in scripts:
    print(f"\n{'='*100}")
    print(f"Running: {name}")
    print(f"Script: {script}")
    print(f"{'='*100}\n")
    
    try:
        result = subprocess.run(
            [python_exe, script],
            capture_output=True,
            text=True,
            timeout=300,
            encoding='utf-8',
            errors='replace'
        )
        
        # Show last 20 lines of output
        if result.stdout:
            lines = result.stdout.split('\n')
            print('\n'.join(lines[-20:]))
        
        success = result.returncode == 0
        results.append({
            'script': name,
            'success': success,
            'exit_code': result.returncode
        })
        
        print(f"\n{'[+]' if success else '[X]'} {name}: {'SUCCESS' if success else 'FAILED'}")
        
        if not success and result.stderr:
            print(f"Error: {result.stderr[:500]}")
            
    except Exception as e:
        print(f"[X] {name}: EXCEPTION - {str(e)}")
        results.append({
            'script': name,
            'success': False,
            'exit_code': -1
        })

# Summary
print(f"\n\n{'='*100}")
print(" "*40 + "TEST SUMMARY")
print(f"{'='*100}\n")

passed = sum(1 for r in results if r['success'])
failed = len(results) - passed

for r in results:
    status = '[+] PASSED' if r['success'] else '[X] FAILED'
    print(f"{status:12} - {r['script']}")

print(f"\n{'='*100}")
print(f"Total: {len(results)} | Passed: {passed} | Failed: {failed}")
print(f"{'='*100}\n")

# Check validation_reports folder
reports_dir = Path('validation_reports')
if reports_dir.exists():
    files = list(reports_dir.glob('*.xlsx'))
    print(f"\nFiles in validation_reports/: {len(files)}")
    for f in sorted(files, key=lambda x: x.stat().st_mtime, reverse=True)[:5]:
        print(f"  - {f.name}")
