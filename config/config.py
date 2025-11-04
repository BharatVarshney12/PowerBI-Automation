"""
Configuration file for PowerBI Automation
Contains all environment-specific settings
"""

import os
from pathlib import Path

# Project Paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
REPORTS_DIR = BASE_DIR / "reports"
ALLURE_RESULTS_DIR = BASE_DIR / "reports" / "allure-results"
SWEETVIZ_DIR = DATA_DIR / "sweetviz_reports"
YDATA_DIR = DATA_DIR / "ydata_reports"
DOWNLOADS_DIR = DATA_DIR / "downloads"

# Create directories if they don't exist
for directory in [DATA_DIR, REPORTS_DIR, ALLURE_RESULTS_DIR, SWEETVIZ_DIR, YDATA_DIR, DOWNLOADS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# PowerBI Configuration
POWERBI_CONFIG = {
    'url': 'https://app.powerbi.com/groups/me/apps/ecadb76d-ccf2-4fdc-b9db-3d3383beac62/reports/5502e4cd-040c-46c7-9224-0cda87688847/d786f02be7f25e623edf?experience=power-bi',
    'username': 'bvarshney@aarete.com',
    'password': 'Twenty!Aug@2025'
}

# Browser Configuration
BROWSER_CONFIG = {
    'headless': False,
    'browser_type': 'chromium',
    'args': [
        '--disable-blink-features=AutomationControlled',
        '--start-maximized'  # Open browser in maximized mode
    ],
    'viewport': None,  # Use full screen instead of fixed viewport
    'accept_downloads': True,
    'ignore_https_errors': True,
    'persist_session': False  # Always force fresh login (disabled session persistence)
}

# Timeout Configuration (in milliseconds)
TIMEOUTS = {
    'default': 30000,
    'navigation': 60000,
    'download': 90000,
    'short': 5000,
    'long': 120000
}

# Selectors Configuration
SELECTORS = {
    'email': {
        'input': [
            'input[placeholder="Enter email"]',
            'input[type="email"]',
            'input[name="loginfmt"]'
        ],
        'submit': '#submitBtn'
    },
    'password': {
        'input': 'input[type="password"]',
        'submit': 'input[type="submit"]'
    },
    'dashboard': {
        'grid': 'grid',
        'grid_text': 'Claim Type PMPM Prev Year'
    },
    'export': {
        'more_options': '[data-testid="visual-more-options-btn"]',
        'export_data': '[data-testid="pbimenu-item.Export data"]',
        'export_type': 'radio',
        'export_type_name': 'Data with current layout',
        'export_button': '[data-testid="export-btn"]'
    }
}

# Profiling Configuration
PROFILING_CONFIG = {
    'sweetviz': {
        'enabled': True,
        'explorative': True
    },
    'ydata': {
        'enabled': True,
        'explorative': True,
        'minimal': False
    }
}

# Logging Configuration
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file': str(BASE_DIR / 'logs' / 'automation.log')
}
