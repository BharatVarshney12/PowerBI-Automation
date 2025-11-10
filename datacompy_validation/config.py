"""
Configuration for DataComPy Validation
Separate from your existing config files
"""
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
EXCEL_FOLDER = PROJECT_ROOT / "power bi actual report"
CSV_FOLDER = PROJECT_ROOT  # CSV files are in project root
OUTPUT_FOLDER = PROJECT_ROOT / "validation_reports" / "datacompy_output"

# Create output folder
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

# Comparison configurations
COMPARISON_CONFIG = {
    'SPEND_BY_CODE': {
        'excel_file': 'Spend by code.xlsx',  # Note: Capital 'S'
        'csv_file': 'spend by code.csv',
        'join_columns': ['CLAIM FORM TYPE'],  # Uppercase after cleaning
        'abs_tol': 0.01,  # Absolute tolerance for numeric columns (0.01 = 1 cent)
        'rel_tol': 0,     # Relative tolerance (0 = exact match required)
    },
    'SPEND_BY_PRODUCT_TYPE': {
        'excel_file': 'Spend by product type.xlsx',  # Note: Capital 'S'
        'csv_file': 'Spend by product type.csv',
        'join_columns': ['CLAIM FORM TYPE', 'PRODUCT'],  # Multi-column join
        'abs_tol': 0.01,
        'rel_tol': 0,
    },
    'SPEND_BY_BILL_TYPE': {
        'excel_file': 'Spend by  bill type.xlsx',  # Note: Two spaces
        'csv_file': 'Spend by  bill type.csv',
        'join_columns': ['CLAIM FORM TYPE'],
        'abs_tol': 0.01,
        'rel_tol': 0,
    }
}

# DataComPy settings
DATACOMPY_SETTINGS = {
    'ignore_spaces': True,      # Ignore leading/trailing spaces
    'ignore_case': True,        # Case-insensitive string comparison
    'cast_column_names_lower': False,  # Keep original column names
}

# Report settings
REPORT_SETTINGS = {
    'save_text_report': True,   # Save .txt comparison reports
    'save_excel_report': True,  # Save .xlsx detailed reports
    'include_summary': True,    # Include summary sheet
    'include_mismatches': True, # Include mismatch details
    'include_stats': True,      # Include column statistics
}
