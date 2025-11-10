# DataComPy Quick Start Guide

## What You Get

A **completely separate** validation approach for comparing Excel and CSV files using the `datacompy` library.

## Installation

```bash
pip install datacompy
```

## Folder Structure

```
datacompy_validation/          ← NEW! Separate from your existing code
├── __init__.py
├── README.md                   ← Full documentation
├── config.py                   ← Configuration
├── excel_csv_comparator.py     ← Main comparison logic
├── report_generator.py         ← Report generation
├── demo_basic_usage.py         ← Learn datacompy basics
├── demo_excel_csv.py           ← Excel vs CSV examples
└── run_comparison.py           ← Main entry point
```

**Your existing code is 100% untouched!**

## Quick Start (3 Steps)

### Step 1: Install datacompy

```bash
pip install datacompy
```

### Step 2: See demos

```bash
# Learn datacompy basics
python datacompy_validation/demo_basic_usage.py

# See Excel vs CSV comparison examples
python datacompy_validation/demo_excel_csv.py
```

### Step 3: Run on your data

```bash
# Interactive menu
python datacompy_validation/run_comparison.py

# Compare specific table
python datacompy_validation/run_comparison.py --table SPEND_BY_CODE

# Compare all tables
python datacompy_validation/run_comparison.py --all
```

## What DataComPy Does

```python
import datacompy

# Load your data
excel_df = pd.read_excel('file.xlsx')
csv_df = pd.read_csv('file.csv')

# Compare in ONE line!
compare = datacompy.Compare(
    df1=excel_df,
    df2=csv_df,
    join_columns=['ID'],
    abs_tol=0.01  # 1 cent tolerance
)

# Get detailed report
print(compare.report())
```

Output:
```
DataFrame Comparison
====================

DataFrame Summary
-----------------
  DataFrame  Columns  Rows
0     Excel       10     3
1       CSV       10     3

Row Summary
-----------
Matched on: CLAIM_FORM_TYPE
Number of rows in common: 3
Number of rows with differences: 2

Column Comparison
-----------------
Number of columns compared: 10
Number of columns with differences: 2
```

## How It Helps Your Project

### Current Approach (Your existing code)
```python
# Your complete_data_comparison.py (100+ lines)
- Manual row-by-row comparison
- Custom color coding
- Manual tolerance handling
- Works great! Keep using it!
```

### DataComPy Approach (This new folder)
```python
# datacompy_validation (10 lines for same result)
comparator = ExcelCSVComparator()
compare = comparator.compare('SPEND_BY_CODE')
report_gen = DataComPyReportGenerator()
report_gen.save_excel_report(compare, 'SPEND_BY_CODE')
```

## Benefits

✅ **Automatic schema comparison** - Detects missing/extra columns  
✅ **Built-in tolerance** - Handles floating-point precision  
✅ **Row-level matching** - Finds missing rows in either file  
✅ **Detailed statistics** - Match rate per column  
✅ **Less code** - 10 lines vs 100+ lines  
✅ **Industry standard** - Well-tested library  

## Output Location

```
validation_reports/
├── datacompy_output/              ← DataComPy reports (NEW)
│   ├── datacompy_report_*.txt     ← Text reports
│   └── datacompy_details_*.xlsx   ← Excel reports
│
└── (your existing reports)        ← Unchanged!
```

## Usage Examples

### Example 1: Compare one table

```bash
python datacompy_validation/run_comparison.py --table SPEND_BY_CODE
```

### Example 2: Compare all tables

```bash
python datacompy_validation/run_comparison.py --all
```

### Example 3: Interactive menu

```bash
python datacompy_validation/run_comparison.py
```

### Example 4: In your own script

```python
from datacompy_validation.excel_csv_comparator import quick_compare

compare = quick_compare(
    excel_file='spend by code.xlsx',
    csv_file='spend_by_code.csv',
    join_columns=['CLAIM_FORM_TYPE'],
    abs_tol=0.01
)

if compare.matches():
    print("✅ Perfect match!")
else:
    print(f"⚠ {len(compare.all_mismatch())} differences found")
```

## Prerequisites

You need CSV files from Snowflake:

```bash
# Required files in data/downloads/
spend_by_code.csv
spend_by_product_type.csv
spend_by_bill_type.csv
```

**How to get CSV files:**

1. **Option 1:** Export from Snowflake UI
   - Run query: `SELECT * FROM table_name`
   - Download as CSV
   - Save to `data/downloads/`

2. **Option 2:** Use Python
   ```python
   import snowflake.connector
   import pandas as pd
   
   # Connect to Snowflake
   conn = snowflake.connector.connect(...)
   
   # Export to CSV
   df = pd.read_sql("SELECT * FROM table_name", conn)
   df.to_csv('data/downloads/table_name.csv', index=False)
   ```

## No Changes to Your Code

✅ Your existing scripts work exactly as before  
✅ No imports changed  
✅ No dependencies broken  
✅ Completely independent  

## Sample Output

### Text Report
```
DataFrame Comparison
====================

DataFrame Summary
-----------------
  DataFrame  Columns  Rows
0     Excel        9     3
1       CSV        9     3

Column Summary
--------------
Number of columns in common: 9
Number of columns in Excel only: 0
Number of columns in CSV only: 0

Row Summary
-----------
Matched on: CLAIM_FORM_TYPE
Number of rows in common: 3
Number of rows in Excel only: 0
Number of rows in CSV only: 0

*** DataFrames are identical! ***
```

### Excel Report Sheets

1. **Summary** - Overall statistics
2. **Mismatches** - Rows with differences
3. **Only_in_Excel** - Missing from CSV
4. **Only_in_CSV** - Missing from Excel
5. **Column_Statistics** - Per-column match rates

## Comparison Matrix

| Feature | Your Current Code | DataComPy |
|---------|------------------|-----------|
| Row comparison | ✅ Manual loops | ✅ Automatic |
| Column schema check | ❌ Manual | ✅ Automatic |
| Numeric tolerance | ✅ Custom | ✅ Built-in |
| Missing rows detection | ❌ Manual | ✅ Automatic |
| Statistics | ❌ Manual | ✅ Built-in |
| Code lines | 100+ | 10 |
| Customization | ✅ Full control | ⚠ Limited |

## When to Use Each

### Use Your Current Code When:
- You need custom Excel formatting
- You want full control over logic
- You need specific color schemes
- It's already working perfectly

### Use DataComPy When:
- You want quick validation
- You need detailed statistics
- You want less code to maintain
- You need industry-standard reports

## Both Can Coexist!

```bash
# Run your existing validation
python complete_data_comparison.py

# ALSO run datacompy validation
python datacompy_validation/run_comparison.py

# Compare outputs and choose what works best!
```

## Troubleshooting

**Problem:** `FileNotFoundError: CSV file not found`  
**Solution:** Export Snowflake tables to CSV first (see Prerequisites)

**Problem:** `ModuleNotFoundError: No module named 'datacompy'`  
**Solution:** `pip install datacompy`

**Problem:** Column name mismatches  
**Solution:** DataComPy auto-detects this! Check the report for details.

## Next Steps

1. ✅ Install: `pip install datacompy`
2. ✅ Run demos: `python datacompy_validation/demo_basic_usage.py`
3. ✅ Export CSV files from Snowflake
4. ✅ Run comparison: `python datacompy_validation/run_comparison.py`
5. ✅ Review reports in `validation_reports/datacompy_output/`

## Questions?

- Check `datacompy_validation/README.md` for full documentation
- Run demos to see examples
- DataComPy docs: https://github.com/capitalone/datacompy

---

**Remember:** Your existing validation code continues to work perfectly!  
This is just an additional tool you can use alongside it.
