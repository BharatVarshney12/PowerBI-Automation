# DataComPy Validation - Separate Approach

## Overview

This folder contains a **completely separate** validation approach using the **datacompy** library for comparing Excel and CSV files.

**YOUR EXISTING CODE IS UNTOUCHED!**

## What is DataComPy?

DataComPy is a powerful Python library that:
- Compares two Pandas DataFrames
- Automatically detects schema differences
- Identifies row-level mismatches
- Provides detailed statistical reports
- Handles numeric tolerances
- Generates comprehensive comparison reports

## Installation

```bash
pip install datacompy
```

## Folder Structure

```
datacompy_validation/
├── __init__.py                    # Package initialization
├── README.md                      # This file
├── config.py                      # Configuration
├── excel_csv_comparator.py        # Main comparison logic
├── report_generator.py            # Report generation
├── demo_basic_usage.py            # Basic examples
├── demo_excel_csv.py              # Excel vs CSV comparison demo
└── run_comparison.py              # Main entry point
```

## Quick Start

### Option 1: Run Demo Examples

```bash
# See basic datacompy usage
python datacompy_validation/demo_basic_usage.py

# Run Excel vs CSV comparison
python datacompy_validation/demo_excel_csv.py
```

### Option 2: Run on Your Actual Data

```bash
python datacompy_validation/run_comparison.py
```

## How It Works

### 1. Load Excel File
```python
excel_df = pd.read_excel('power bi actual report/spend by code.xlsx')
```

### 2. Load CSV File
```python
csv_df = pd.read_csv('data/downloads/spend_by_code.csv')
```

### 3. Compare with DataComPy
```python
import datacompy

compare = datacompy.Compare(
    df1=excel_df,
    df2=csv_df,
    join_columns=['CLAIM_FORM_TYPE'],  # Key column
    abs_tol=0.01,  # Numeric tolerance (1 cent)
    df1_name='Excel',
    df2_name='CSV'
)

# Print detailed report
print(compare.report())
```

### 4. Get Detailed Results
```python
# Check if data matches
if compare.matches():
    print("✅ Data is identical!")
else:
    print("❌ Differences found!")
    
    # Show all mismatches
    print(compare.all_mismatch())
    
    # Rows only in Excel
    print(compare.df1_unq_rows)
    
    # Rows only in CSV
    print(compare.df2_unq_rows)
```

## Sample Output

```
DataFrame Comparison
====================

DataFrame Summary
-----------------
  DataFrame  Columns  Rows
0     Excel       10     3
1       CSV       10     3

Column Summary
--------------
Number of columns in common: 10
Number of columns in Excel only: 0
Number of columns in CSV only: 0

Row Summary
-----------
Matched on: CLAIM_FORM_TYPE
Number of rows in common: 3
Number of rows in Excel only: 0
Number of rows in CSV only: 0
Number of rows with differences: 2

Column Comparison
-----------------
Number of columns compared: 10
Number of columns with differences: 2

Column Differences
------------------
Column: NET_SPEND
  Match rate: 66.67%
  Mismatches: 1
  
Column: GROSS_SPEND
  Match rate: 66.67%
  Mismatches: 1
```

## Benefits Over Manual Comparison

### Your Current Approach
- ✅ Full control
- ✅ Custom formatting
- ❌ More code to maintain
- ❌ Manual tolerance handling
- ❌ Limited statistics

### DataComPy Approach
- ✅ Automatic schema comparison
- ✅ Built-in tolerance handling
- ✅ Rich statistics
- ✅ Less code
- ✅ Industry-standard tool
- ❌ Less customization

## Integration Options

### Option 1: Keep Separate (Recommended)
Run both your existing validation AND datacompy side-by-side.

```bash
# Your existing validation
python complete_data_comparison.py

# DataComPy validation (separate)
python datacompy_validation/run_comparison.py
```

### Option 2: Use for Specific Cases
Use datacompy for quick checks, your existing code for detailed reports.

### Option 3: Gradual Migration
Slowly adopt datacompy for new validations while keeping existing code.

## Output Location

All datacompy reports are saved in:
```
validation_reports/datacompy_output/
├── comparison_report_*.txt         # Text reports
└── comparison_details_*.xlsx       # Excel reports
```

**Separate from your existing validation_reports/ files!**

## No Changes to Your Code

✅ Your existing scripts work exactly as before
✅ No imports changed
✅ No dependencies broken
✅ Completely independent module

## Questions?

Check the demo files:
- `demo_basic_usage.py` - Learn datacompy basics
- `demo_excel_csv.py` - See Excel vs CSV comparison
- `run_comparison.py` - Full validation workflow
