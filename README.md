# PowerBI Automation Framework (Page Object Model)

## 🎯 Project Overview
Industry-standard automation framework for PowerBI using **Page Object Model (POM)** pattern with Playwright, Pytest, and comprehensive reporting.

## 📁 Project Structure
```
PowerBI_Automation_POM/
├── config/
│   └── config.py              # Centralized configuration
├── pages/
│   ├── base_page.py           # Base page with common methods
│   ├── login_page.py          # Login page object
│   ├── dashboard_page.py      # Dashboard page object
│   └── export_page.py         # Export functionality page object
├── utils/
│   ├── browser_manager.py     # Browser lifecycle management
│   └── profiling.py           # Data profiling utilities
├── tests/
│   ├── conftest.py            # Pytest fixtures
│   └── test_powerbi_automation.py  # Test suite
├── data/
│   ├── downloads/             # Downloaded Excel files
│   ├── sweetviz_reports/      # Sweetviz HTML reports
│   └── ydata_reports/         # YData-Profiling reports
├── reports/
│   └── allure-results/        # Allure test results
├── pytest.ini                 # Pytest configuration
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## 🚀 Features
- ✅ **Page Object Model (POM)** - Industry-standard design pattern
- ✅ **Pytest Fixtures** - Reusable test components
- ✅ **Allure Reporting** - Beautiful HTML test reports with screenshots
- ✅ **Sweetviz Integration** - Quick visual EDA reports
- ✅ **YData-Profiling** - Comprehensive data profiling
- ✅ **Fresh Session** - Incognito mode for each test
- ✅ **Configuration Management** - Centralized settings
- ✅ **Error Handling** - Screenshots on failure
- ✅ **Modular Design** - Easy to maintain and extend

## 📦 Installation

### Step 1: Install Python Dependencies
```bash
cd C:\Users\bvarshney\PowerBI_Automation_POM
pip install -r requirements.txt
```

### Step 2: Install Playwright Browsers
```bash
playwright install chromium
```

## ▶️ Running Tests

### Run All Tests
```bash
pytest
```

### Run Specific Test Class
```bash
pytest tests/test_powerbi_automation.py::TestPowerBIAutomation
```

### Run Login Test Only
```bash
pytest tests/test_powerbi_automation.py::TestPowerBILogin
```

### Run Export Test Only
```bash
pytest tests/test_powerbi_automation.py::TestPowerBIExport
```

### Run with Custom Allure Directory
```bash
pytest --alluredir=reports/allure-results
```

## 📊 View Allure Report
```bash
allure serve reports/allure-results
```

## 🏗️ Architecture

### Page Object Model Pattern
Each page is represented as a Python class with methods for user actions:

```python
# Login Page
login_page = LoginPage(page)
login_page.enter_email("user@example.com")
login_page.click_submit()

# Dashboard Page  
dashboard = DashboardPage(page)
dashboard.wait_for_dashboard()

# Export Page
export = ExportPage(page)
export.export_report()
```

### Benefits of This Pattern
1. **Separation of Concerns** - Test logic separated from page interactions
2. **Reusability** - Page objects can be used across multiple tests
3. **Maintainability** - Changes to UI only require updates in one place
4. **Readability** - Tests read like natural language
5. **Scalability** - Easy to add new pages and tests

## 🔧 Configuration

Edit `config/config.py` to change:
- PowerBI URL and credentials
- Browser settings
- Timeouts
- Selectors
- Profiling options

## 📈 Generated Reports

After test execution, you'll find:
- **Excel Data**: `data/downloads/`
- **Sweetviz Reports**: `data/sweetviz_reports/`
- **YData Reports**: `data/ydata_reports/`
- **Allure Results**: `reports/allure-results/`

## 🧪 Test Coverage

- ✅ PowerBI Authentication Flow
- ✅ Dashboard Navigation
- ✅ Report Export
- ✅ Data Profiling (Sweetviz + YData)
- ✅ Error Handling
- ✅ Screenshot Capture

## 📝 Adding New Tests

1. Create page object in `pages/` if needed
2. Add test in `tests/test_powerbi_automation.py`
3. Use fixtures from `conftest.py`
4. Run and verify with Allure report

## 🎓 Example Usage

```python
def test_example(browser_page, powerbi_url, credentials):
    # Use page objects
    login = LoginPage(browser_page)
    login.navigate(powerbi_url)
    login.login(credentials['username'], credentials['password'])
    
    # Verify
    dashboard = DashboardPage(browser_page)
    assert dashboard.verify_dashboard_loaded()
```

## 🔍 Troubleshooting

- **Import errors**: Make sure you're in project root directory
- **Browser not found**: Run `playwright install chromium`
- **Allure not found**: Install Allure CLI via Scoop (Windows)

## 📞 Support

For issues or questions, review the generated Allure reports for detailed execution logs and screenshots.
