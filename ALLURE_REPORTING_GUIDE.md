# PowerBI Validation - Allure Reporting for Stakeholders

## 📊 Overview

This project provides **comprehensive validation reporting** for PowerBI data pipeline using **Allure Framework** - a beautiful, interactive HTML report perfect for stakeholder presentations.

### What is Allure?

Allure is a flexible, lightweight test report framework that generates beautiful HTML reports with:
- ✅ Visual pass/fail indicators
- 📈 Execution trends and statistics
- 📎 File attachments (Excel reports, SQL queries)
- 📝 Detailed step-by-step execution logs
- ⏱️ Performance metrics and timing
- 🎨 Clean, professional presentation

---

## 🚀 Quick Start (For Stakeholders)

### Option 1: View Existing Report (Fastest)

If validation has already been run:

```batch
view_allure_report.bat
```

This opens the Allure report in your browser instantly.

### Option 2: Run New Validation + Generate Report

To run fresh validation and generate a new report:

```batch
generate_allure_report.bat
```

This will:
1. Run all validation tests
2. Generate Allure HTML report
3. Open report in your browser automatically

---

## 📋 Prerequisites

### 1. Install Allure CLI

Choose one installation method:

#### **Option A: Using Scoop (Recommended for Windows)**
```powershell
# Install Scoop if not already installed
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
irm get.scoop.sh | iex

# Install Allure
scoop install allure
```

#### **Option B: Manual Download**
1. Download from: https://github.com/allure-framework/allure2/releases
2. Extract to a folder (e.g., `C:\allure`)
3. Add to System PATH:
   - Windows Key → Search "Environment Variables"
   - Edit System Environment Variables
   - Add `C:\allure\bin` to PATH

#### **Option C: Using npm**
```bash
npm install -g allure-commandline
```

### 2. Verify Installation

```batch
allure --version
```

Should display version like: `2.x.x`

---

## 📂 Report Contents

The Allure report includes:

### 🧪 Test Results
- **Import Excel to Snowflake** - Data import validation
- **Quick Row Count Validation** - Fast sanity check
- **Comprehensive Excel vs Snowflake** - Cell-by-cell comparison
- **SQL Queries Export** - Complete SQL documentation
- **CSV vs Excel Comparison** - Visual difference highlighting

### 📎 Attachments (Auto-included)
- Excel validation reports
- SQL query results
- Text summary reports
- Console output logs
- Error traces (if any)

### 📊 Visual Elements
- Execution timeline
- Pass/fail statistics
- Duration metrics
- Trend graphs (across multiple runs)

---

## 💼 For Stakeholders

### Viewing the Report

1. **Double-click** `view_allure_report.bat`
2. Your browser opens automatically
3. Navigate through:
   - **Overview** - Summary statistics
   - **Suites** - Detailed test results
   - **Graphs** - Visual analytics
   - **Timeline** - Execution timeline
   - **Behaviors** - Grouped by features

### Understanding Results

| Icon | Meaning |
|------|---------|
| ✅ Green Check | Test Passed - Data Valid |
| ❌ Red X | Test Failed - Issues Found |
| ⚠️ Yellow Warning | Test Skipped/Incomplete |

### Sharing Reports

**To share with team:**

1. Navigate to `reports/allure-report/` folder
2. Copy entire folder
3. Share via:
   - Email (zip the folder)
   - SharePoint/OneDrive
   - Internal file server
   - Web hosting

Recipients can open `index.html` in any browser (no server needed).

---

## 🔧 For Developers

### Manual Execution

#### Run Tests Only (No Report)
```bash
pytest test_validation_allure.py -v
```

#### Run Tests + Generate Allure Results
```bash
pytest test_validation_allure.py --alluredir=reports/allure-results -v
```

#### Generate HTML Report from Results
```bash
allure generate reports/allure-results -o reports/allure-report --clean
```

#### Serve Report Locally
```bash
allure serve reports/allure-results
```

#### Open Existing Report
```bash
allure open reports/allure-report
```

### Customization

Edit `test_validation_allure.py` to:
- Add/remove validation steps
- Customize descriptions
- Modify severity levels
- Add custom attachments

---

## 📁 Project Structure

```
PowerBI_Automation_POM/
│
├── test_validation_allure.py          # Pytest test suite with Allure
├── run_validation_with_allure.py      # Standalone runner (alternative)
├── generate_allure_report.bat         # Windows: Generate report
├── view_allure_report.bat             # Windows: View existing report
│
├── reports/
│   ├── allure-results/                # Raw test results (JSON)
│   └── allure-report/                 # Generated HTML report
│       └── index.html                 # Main report page
│
├── validation_reports/                # Validation output files
│   ├── Excel_vs_Snowflake_Validation_*.xlsx
│   ├── Snowflake_SQL_Results_*.xlsx
│   ├── CSV_vs_Excel_Comparison_*.xlsx
│   └── Validation_Report_*.txt
│
└── [validation scripts...]            # Core validation Python files
```

---

## 🎯 Validation Workflow

```
┌─────────────────────────────────────┐
│  1. Import Excel → Snowflake        │
│     • Load Power BI reports         │
│     • Create Snowflake tables       │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│  2. Quick Row Count Check           │
│     • Verify row counts match       │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│  3. Comprehensive Validation        │
│     • Cell-by-cell comparison       │
│     • Identify all mismatches       │
│     • Generate detailed reports     │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│  4. SQL Documentation               │
│     • Export 108 SQL queries        │
│     • Document data sources         │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│  5. CSV Comparison (Optional)       │
│     • Color-coded differences       │
│     • Visual mismatch highlighting  │
└──────────────┬──────────────────────┘
               ↓
         📊 Allure Report
```

---

## 📞 Support

### Common Issues

**1. "Allure command not found"**
- Solution: Install Allure CLI (see Prerequisites section)

**2. "No tests found"**
- Solution: Ensure you're in project root directory
- Run: `pytest test_validation_allure.py --collect-only`

**3. "Report not opening"**
- Solution: Manually open `reports/allure-report/index.html` in browser

**4. "Some tests failed"**
- Solution: Check Allure report for detailed error messages
- Review `validation_reports/` folder for output files

### Contact

For technical support, contact:
- **Developer**: Bharat Varshney
- **Email**: bvarshney@aarete.com

---

## 📝 Version History

| Date | Version | Changes |
|------|---------|---------|
| Nov 2025 | 1.0 | Initial Allure reporting implementation |

---

## 🏆 Best Practices

### For Regular Validation
1. Run `generate_allure_report.bat` weekly/monthly
2. Archive old reports (with timestamps)
3. Share with stakeholders via email/SharePoint

### For Stakeholder Presentations
1. Open Allure report in browser
2. Navigate to **Overview** for summary
3. Show **Graphs** for visual impact
4. Drill into specific tests for details
5. Highlight **Attachments** (Excel reports)

### For Data Quality Meetings
1. Compare trends across multiple runs
2. Focus on failed tests (if any)
3. Review attached validation reports
4. Export specific test results as needed

---

## 📄 License

Internal use - Aarete Corporation

---

**Last Updated**: November 4, 2025  
**Maintained By**: Bharat Varshney
