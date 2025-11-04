# 📊 PowerBI Automation - Complete Validation Guide

## 🚀 Quick Start - Run Everything Automatically

### **Option 1: Master Script (RECOMMENDED)**
Run the complete workflow with one command:

```bash
python run_complete_validation.py
```

This will automatically:
1. Import Excel data to Snowflake
2. Run quick validation check
3. Perform comprehensive Excel vs Snowflake comparison
4. Export all Snowflake SQL queries
5. Optionally compare CSV vs Excel (if you edited CSV files)

---

### **Option 2: VS Code Tasks**
Press **Ctrl+Shift+P** → Type `Tasks: Run Task` → Select task

---

### **Option 3: Run Individual Scripts**

For more control, run scripts manually in this order:

#### **STEP 1: Import Data** (Required)
```bash
python import_complete_excel_to_snowflake.py
```
**What it does:** Imports Excel files from `power bi actual report/` into Snowflake database

---

#### **STEP 2: Quick Check** (Optional)
```bash
python quick_validation.py
```
**What it does:** Fast row count comparison (console output only)

---

#### **STEP 3: Main Validation** (Required)
```bash
python compare_excel_snowflake_reports.py
```
**What it does:** Comprehensive cell-by-cell Excel vs Snowflake validation

**Output files:**
- `Excel_vs_Snowflake_Validation_*.xlsx` - Detailed comparison
- `Snowflake_Validation_Queries_*.xlsx` - Sample data from Snowflake
- `Validation_Report_*.txt` - Text summary

---

#### **STEP 4: Export SQL** (Optional)
```bash
python snowflake_queries_to_excel.py
```
**What it does:** Exports all 108 SQL queries and results to Excel

**Output file:**
- `Snowflake_SQL_Results_*.xlsx` (24 sheets)

---

#### **STEP 5: CSV Comparison** (Only if you edited CSV files)
```bash
python complete_data_comparison.py
```
**What it does:** Compares CSV files with Excel Power BI reports using color coding

**Output file:**
- `CSV_vs_Excel_Comparison_ColorCoded_*.xlsx`
- Red = CSV value (different)
- Green = Excel value (original)

---

## 📁 File Structure

```
PowerBI_Automation_POM/
│
├── run_complete_validation.py          # Master script - runs all steps
│
├── import_complete_excel_to_snowflake.py   # Step 1: Import to Snowflake
├── quick_validation.py                     # Step 2: Quick check
├── compare_excel_snowflake_reports.py      # Step 3: Main validation
├── snowflake_queries_to_excel.py           # Step 4: Export SQL
├── complete_data_comparison.py             # Step 5: CSV comparison
│
├── validation_reports/                 # All output files saved here
│   ├── Excel_vs_Snowflake_Validation_*.xlsx
│   ├── Snowflake_Validation_Queries_*.xlsx
│   ├── Validation_Report_*.txt
│   ├── Snowflake_SQL_Results_*.xlsx
│   └── CSV_vs_Excel_Comparison_ColorCoded_*.xlsx
│
├── power bi actual report/            # Excel source files
│   ├── Spend by code.xlsx
│   ├── Spend by product type.xlsx
│   └── Spend by  bill type.xlsx
│
├── CSV files (if you exported them):
│   ├── spend by code.csv
│   ├── Spend by product type.csv
│   └── Spend by  bill type.csv
│
└── config/
    └── config.py                      # Snowflake configuration
```

---

## 🎯 What Each Script Does

| Script | Purpose | When to Use | Output Type |
|--------|---------|-------------|-------------|
| `run_complete_validation.py` | Run all steps automatically | **Use this first!** | Console + Multiple Excel files |
| `import_complete_excel_to_snowflake.py` | Import Excel → Snowflake | Before any validation | Console |
| `quick_validation.py` | Fast row count check | Quick sanity check | Console |
| `compare_excel_snowflake_reports.py` | **Main validation** Excel ↔ Snowflake | Primary validation | 3 Excel files |
| `snowflake_queries_to_excel.py` | Export all SQL queries | Document SQL details | 1 Excel file |
| `complete_data_comparison.py` | CSV ↔ Excel comparison | Only if CSV edited | 1 Excel file (color coded) |
| `detect_csv_excel_mismatches.py` | Detect CSV mismatches | Detailed mismatch report | 1 Excel file |

---

## ✅ Validation Workflow Sequence

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  1. Import Excel to Snowflake                               │
│     └─> Creates tables: SPEND_BY_CODE, SPEND_BY_PRODUCT_   │
│         TYPE, SPEND_BY_BILL_TYPE                            │
│                                                             │
│  2. Quick Validation (Optional)                             │
│     └─> Fast check: Row counts match?                       │
│                                                             │
│  3. Comprehensive Validation (MAIN)                         │
│     └─> Cell-by-cell comparison                            │
│     └─> Output: 3 Excel files in validation_reports/       │
│                                                             │
│  4. Export SQL Queries (Optional)                           │
│     └─> Document all 108 SQL queries                        │
│     └─> Output: 1 Excel file with 24 sheets                │
│                                                             │
│  5. CSV vs Excel Comparison (Only if CSV edited)            │
│     └─> Color-coded difference highlighting                │
│     └─> Output: 1 Excel file with color formatting         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔧 Configuration

Edit `config/config.py` for Snowflake connection:

```python
SNOWFLAKE_CONFIG = {
    'account': 'po54025.central-india.azure',
    'user': 'BHARATAARETE',
    'password': 'your_password',
    'warehouse': 'POWERBI',
    'database': 'POWERBI_LEARNING',
    'schema': 'TRAINING_POWERBI'
}
```

---

## 📊 Understanding Output Files

### **Excel_vs_Snowflake_Validation_*.xlsx**
- **Sheet 1:** Summary - Overview of all validations
- **Sheet 2:** SPEND_BY_CODE - Detailed comparison
- **Sheet 3:** SPEND_BY_PRODUCT_TYPE - Detailed comparison
- **Sheet 4:** SPEND_BY_BILL_TYPE - Detailed comparison

Each sheet shows:
- Row count comparison
- Column count comparison
- NULL value counts
- Data type validation
- Cell-by-cell mismatches

---

### **Snowflake_Validation_Queries_*.xlsx**
- **Sample data** from each Snowflake table (20 rows)
- **Full data** from each table (all rows)
- Used to verify Snowflake content

---

### **CSV_vs_Excel_Comparison_ColorCoded_*.xlsx**
- **Summary:** Match percentages for all tables
- **Table sheets:** Side-by-side CSV vs Excel comparison
- **Legend:** Color coding explanation

**Color Coding:**
- 🔴 **Red (Pink)** = CSV value (different from Excel)
- 🟢 **Green** = Excel value (original Power BI data)
- ⚪ **No color** = Values match

---

## 🐛 Troubleshooting

### **Error: Snowflake connection failed**
- Check `config/config.py` credentials
- Verify Snowflake warehouse is running
- Test connection: `python -c "from config.config import test_snowflake_connection; test_snowflake_connection()"`

### **Error: Excel file not found**
- Ensure files exist in `power bi actual report/` folder
- Check file names match exactly (including spaces)

### **Error: ModuleNotFoundError**
```bash
pip install -r requirements.txt
```

### **Low match percentage in validation**
- This is expected if CSV files were manually edited
- Use `complete_data_comparison.py` to see exactly what changed

---

## 💡 Tips

1. **First time setup:** Run `python run_complete_validation.py` to execute all steps
2. **Daily validation:** Just run Step 3 (`compare_excel_snowflake_reports.py`)
3. **CSV edited?** Run Step 5 (`complete_data_comparison.py`) to see changes
4. **Check output:** All reports saved in `validation_reports/` folder
5. **VS Code:** Use built-in tasks (Ctrl+Shift+P → Tasks: Run Task)

---

## 📝 Notes

- All output files are timestamped (won't overwrite previous reports)
- Validation reports are saved in `validation_reports/` folder
- CSV comparison only needed if you manually edited CSV files
- Master script (`run_complete_validation.py`) includes interactive prompts

---

## 🎉 Success Criteria

After running validation, you should see:

✅ All imports completed successfully  
✅ Row counts match between Excel and Snowflake  
✅ High match percentage (>95%) in cell comparison  
✅ Minimal NULL value differences  
✅ All data types validated  
✅ Validation report files generated  

If any step fails, check error messages in console output.

---

**Author:** Bharat Varshney  
**Date:** November 4, 2025  
**Version:** 1.0
