"""
Pytest Fixtures for PowerBI Automation
Provides reusable fixtures for browser, pages, and configuration
"""

import pytest
from utils.browser_manager import BrowserManager
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.export_page import ExportPage
from config.config import POWERBI_CONFIG
import allure


@pytest.fixture(scope="function")
def browser_page():
    """Fixture to provide browser page"""
    with BrowserManager() as page:
        yield page


@pytest.fixture(scope="function")
def login_page(browser_page):
    """Fixture to provide LoginPage instance"""
    return LoginPage(browser_page)


@pytest.fixture(scope="function")
def dashboard_page(browser_page):
    """Fixture to provide DashboardPage instance"""
    return DashboardPage(browser_page)


@pytest.fixture(scope="function")
def export_page(browser_page):
    """Fixture to provide ExportPage instance"""
    return ExportPage(browser_page)


@pytest.fixture(scope="function")
def credentials():
    """Fixture to provide login credentials"""
    return {
        'username': POWERBI_CONFIG['username'],
        'password': POWERBI_CONFIG['password']
    }


@pytest.fixture(scope="function")
def powerbi_url():
    """Fixture to provide PowerBI URL"""
    return POWERBI_CONFIG['url']


@pytest.fixture(autouse=True)
def setup_allure_environment():
    """Setup Allure environment info"""
    # Allure environment is set via allure-results/environment.properties
    pass
