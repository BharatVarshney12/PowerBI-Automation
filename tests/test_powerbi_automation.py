"""
PowerBI End-to-End Test Suite
Tests PowerBI login, export, and data profiling using Page Object Model
"""

import pytest
import allure
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.export_page import ExportPage
from utils.profiling import DataProfiler


@allure.feature('PowerBI Automation')
@allure.story('Report Download with POM')
@allure.title('PowerBI Report Export with Fresh Login (Page Object Model)')
@allure.description('Automates login to PowerBI and exports report data using industry-standard Page Object Model pattern')
class TestPowerBIAutomation:
    """Test suite for PowerBI automation with POM pattern"""
    
    def test_powerbi_login_and_export(self, browser_page, powerbi_url, credentials):
        """
        Test complete PowerBI workflow: Login -> Navigate -> Export -> Profile
        
        Args:
            browser_page: Browser page fixture
            powerbi_url: PowerBI dashboard URL
            credentials: Login credentials
        """
        
        # Initialize page objects
        login_page = LoginPage(browser_page)
        dashboard_page = DashboardPage(browser_page)
        export_page = ExportPage(browser_page)
        
        try:
            # Step 1: Navigate to PowerBI
            with allure.step('Navigate to PowerBI Application'):
                login_page.navigate(powerbi_url)
                print(f"[INFO] Starting FRESH login session (incognito mode)")
                print(f"[INFO] Current URL: {browser_page.url}")
            
            # Step 2: Complete Login Flow
            with allure.step('Complete Authentication'):
                login_page.login(
                    email=credentials['username'],
                    password=credentials['password']
                )
                print("[AUTH] Login completed successfully")
            
            # Step 3: Wait for Dashboard
            dashboard_page.wait_for_dashboard()
            
            # Verify dashboard loaded
            assert dashboard_page.verify_dashboard_loaded(), "Dashboard did not load properly"
            print("[SUCCESS] Successfully logged into PowerBI dashboard!")
            
            # Step 4: Export Report
            with allure.step('Export Report Data'):
                file_path = export_page.export_report()
                print(f"[EXPORT] Report downloaded to: {file_path}")
            
            # Step 5: Generate Data Profiling Reports
            with allure.step('Generate Data Profiling Reports'):
                profiler = DataProfiler(file_path)
                reports = profiler.generate_all_reports()
                
                print("\n[PROFILING] Generated reports:")
                if reports['sweetviz']:
                    print(f"  - Sweetviz: {reports['sweetviz']}")
                if reports['ydata']:
                    print(f"  - YData: {reports['ydata']}")
            
            print("\n[SUCCESS] ✅ All tests passed successfully!")
            
        except Exception as e:
            print(f"[ERROR] Test failed: {e}")
            browser_page.screenshot()
            allure.attach(
                browser_page.screenshot(),
                'Error Screenshot',
                allure.attachment_type.PNG
            )
            raise


@allure.feature('PowerBI Automation')
@allure.story('Login Only')
class TestPowerBILogin:
    """Test suite for PowerBI login functionality only"""
    
    def test_powerbi_login_only(self, browser_page, powerbi_url, credentials):
        """Test PowerBI login flow only"""
        
        login_page = LoginPage(browser_page)
        dashboard_page = DashboardPage(browser_page)
        
        # Navigate and login
        login_page.navigate(powerbi_url)
        login_page.login(
            email=credentials['username'],
            password=credentials['password']
        )
        
        # Verify dashboard
        dashboard_page.wait_for_dashboard()
        assert dashboard_page.verify_dashboard_loaded(), "Login failed - Dashboard not loaded"
        
        print("[SUCCESS] Login test passed!")


@allure.feature('PowerBI Automation')
@allure.story('Export Only')
class TestPowerBIExport:
    """Test suite for PowerBI export functionality (assumes logged in)"""
    
    def test_powerbi_export_only(self, browser_page, powerbi_url, credentials):
        """Test PowerBI export flow after login"""
        
        # Login first
        login_page = LoginPage(browser_page)
        dashboard_page = DashboardPage(browser_page)
        export_page = ExportPage(browser_page)
        
        login_page.navigate(powerbi_url)
        login_page.login(credentials['username'], credentials['password'])
        dashboard_page.wait_for_dashboard()
        
        # Test export
        file_path = export_page.export_report()
        
        import os
        assert os.path.exists(file_path), "Export file was not created"
        assert os.path.getsize(file_path) > 0, "Export file is empty"
        
        print(f"[SUCCESS] Export test passed! File: {file_path}")
