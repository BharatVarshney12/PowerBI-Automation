"""
QUICK REFERENCE - PowerBI Validation Workflow
==============================================

EASIEST WAY TO RUN EVERYTHING:
-------------------------------
    python run_complete_validation.py

OR use VS Code Task:
    Ctrl+Shift+P → Tasks: Run Task → "RUN COMPLETE VALIDATION WORKFLOW"


MANUAL WORKFLOW (Step by Step):
================================

┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  STEP 1: Import Excel to Snowflake                                     │
│  ═══════════════════════════════════                                   │
│                                                                         │
│  Command: python import_complete_excel_to_snowflake.py                 │
│                                                                         │
│  Purpose: Loads Excel files into Snowflake database                    │
│                                                                         │
│  Input:  power bi actual report/Spend by code.xlsx                     │
│          power bi actual report/Spend by product type.xlsx             │
│          power bi actual report/Spend by  bill type.xlsx               │
│                                                                         │
│  Output: Snowflake tables created/updated                              │
│          - SPEND_BY_CODE                                               │
│          - SPEND_BY_PRODUCT_TYPE                                       │
│          - SPEND_BY_BILL_TYPE                                          │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  STEP 2: Quick Validation (Optional)                                   │
│  ════════════════════════════════                                      │
│                                                                         │
│  Command: python quick_validation.py                                   │
│                                                                         │
│  Purpose: Fast sanity check - row counts only                          │
│                                                                         │
│  Output: Console output showing row count comparison                   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  STEP 3: Comprehensive Validation (MAIN STEP)                          │
│  ═════════════════════════════════════════════                         │
│                                                                         │
│  Command: python compare_excel_snowflake_reports.py                    │
│                                                                         │
│  Purpose: Complete cell-by-cell Excel vs Snowflake comparison          │
│                                                                         │
│  Output Files (in validation_reports/):                                │
│    1. Excel_vs_Snowflake_Validation_TIMESTAMP.xlsx                     │
│       - Summary sheet                                                  │
│       - Detailed comparison for each table                             │
│       - Row/column counts                                              │
│       - NULL value analysis                                            │
│       - Data type validation                                           │
│       - Cell-by-cell mismatches                                        │
│                                                                         │
│    2. Snowflake_Validation_Queries_TIMESTAMP.xlsx                      │
│       - Sample data (20 rows) from each table                          │
│       - Full data from each table                                      │
│                                                                         │
│    3. Validation_Report_TIMESTAMP.txt                                  │
│       - Text summary of validation results                             │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  STEP 4: Export SQL Queries (Optional)                                 │
│  ══════════════════════════════════════                                │
│                                                                         │
│  Command: python snowflake_queries_to_excel.py                         │
│                                                                         │
│  Purpose: Document all SQL queries executed on Snowflake               │
│                                                                         │
│  Output File (in validation_reports/):                                 │
│    Snowflake_SQL_Results_TIMESTAMP.xlsx                                │
│      - 24 sheets with different SQL query results                      │
│      - 108 total queries executed                                      │
│      - SQL_Queries_List sheet with all queries                         │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  STEP 5: CSV vs Excel Comparison (Only if CSV files edited)            │
│  ═══════════════════════════════════════════════════════               │
│                                                                         │
│  Command: python complete_data_comparison.py                           │
│                                                                         │
│  Purpose: Show differences between CSV and Excel with color coding     │
│                                                                         │
│  Input:  spend by code.csv                                             │
│          Spend by product type.csv                                     │
│          Spend by  bill type.csv                                       │
│          +                                                             │
│          power bi actual report/*.xlsx files                           │
│                                                                         │
│  Output File (in validation_reports/):                                 │
│    CSV_vs_Excel_Comparison_ColorCoded_TIMESTAMP.xlsx                   │
│      - Summary sheet with match percentages                            │
│      - Side-by-side comparison for each table                          │
│      - COLOR CODED:                                                    │
│        🔴 RED (Pink) = CSV value (different from Excel)                │
│        🟢 GREEN = Excel value (original from Power BI)                 │
│        ⚪ No color = Values match                                       │
│      - Legend sheet explaining colors                                  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘


COMMON USE CASES:
=================

1. FIRST TIME SETUP:
   → Run: python run_complete_validation.py
   → This runs all steps automatically

2. DAILY VALIDATION:
   → Run: python compare_excel_snowflake_reports.py
   → Only need Step 3 if Snowflake data already loaded

3. DATA CHANGED IN EXCEL:
   → Run: python import_complete_excel_to_snowflake.py
   → Then: python compare_excel_snowflake_reports.py

4. CSV FILES EDITED MANUALLY:
   → Run: python complete_data_comparison.py
   → See exactly what changed with color highlighting

5. NEED SQL DOCUMENTATION:
   → Run: python snowflake_queries_to_excel.py
   → Get all 108 SQL queries in Excel format


VS CODE TASKS AVAILABLE:
=========================
Press Ctrl+Shift+P → Tasks: Run Task → Choose from:

  ★ RUN COMPLETE VALIDATION WORKFLOW      ← Use this to run everything!
  - Import Complete Excel to Snowflake
  - Quick Validation Check
  - Compare Excel vs Snowflake Reports
  - Export Snowflake Queries to Excel
  - Complete Data Comparison (Snowflake vs Excel)
  - Detect CSV vs Excel Mismatches


OUTPUT FILES LOCATION:
======================
All validation reports are saved in:
    validation_reports/

Files are timestamped so they never overwrite previous reports.


TROUBLESHOOTING:
================

Error: "Snowflake connection failed"
  → Check config/config.py credentials
  → Verify Snowflake warehouse is running

Error: "Excel file not found"
  → Check files exist in "power bi actual report/" folder
  → Verify exact file names (including spaces)

Error: "ModuleNotFoundError"
  → Run: pip install -r requirements.txt

Low match percentage
  → Expected if CSV files were manually edited
  → Run complete_data_comparison.py to see changes


QUICK CHEAT SHEET:
==================

Task                        | Command                                  | Output
----------------------------|------------------------------------------|------------------
Run everything             | python run_complete_validation.py         | Multiple files
Import to Snowflake        | python import_complete_excel_to_snowflake.py | Console
Quick check                | python quick_validation.py                | Console
Main validation            | python compare_excel_snowflake_reports.py | 3 Excel files
Export SQL                 | python snowflake_queries_to_excel.py      | 1 Excel file
CSV comparison             | python complete_data_comparison.py        | 1 Excel file


NEED HELP?
==========
Read the detailed guide: VALIDATION_GUIDE.md
Or ask Bharat Varshney (bvarshney@aarete.com)


Last Updated: November 4, 2025
"""

if __name__ == "__main__":
    print(__doc__)
