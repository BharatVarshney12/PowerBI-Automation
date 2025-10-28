"""
Snowflake Data Validation Tests
Validates PowerBI export data against Snowflake database
"""

import pytest
import allure
import pandas as pd
from utils.snowflake_connector import SnowflakeConnector
from utils.data_validator import DataValidator
from config.snowflake_config import VALIDATION_CONFIG
import os


@allure.feature('Data Validation')
@allure.story('PowerBI vs Snowflake Comparison')
@allure.title('Validate PowerBI Export Against Snowflake Table')
class TestSnowflakeValidation:
    """Test suite for Snowflake data validation"""
    
    def test_validate_powerbi_vs_snowflake(self, powerbi_url, credentials):
        """
        Complete test: Download from PowerBI, fetch from Snowflake, validate
        
        This test:
        1. Logs into PowerBI
        2. Downloads report data
        3. Connects to Snowflake
        4. Fetches corresponding table data
        5. Validates data integrity and consistency
        """
        
        # Import page objects here to avoid circular imports
        from pages.login_page import LoginPage
        from pages.dashboard_page import DashboardPage
        from pages.export_page import ExportPage
        from utils.browser_manager import BrowserManager
        
        powerbi_file_path = None
        
        try:
            # Step 1: Get PowerBI Data
            with allure.step('Download PowerBI Report'):
                with BrowserManager() as page:
                    # Login to PowerBI
                    login = LoginPage(page)
                    login.navigate(powerbi_url)
                    login.login(credentials['username'], credentials['password'])
                    
                    # Wait for dashboard
                    dashboard = DashboardPage(page)
                    dashboard.wait_for_dashboard()
                    
                    # Export report
                    export = ExportPage(page)
                    powerbi_file_path = export.export_report()
                    
                    print(f"[POWERBI] Downloaded: {powerbi_file_path}")
            
            # Step 2: Load PowerBI Data
            with allure.step('Load PowerBI Excel Data'):
                powerbi_df = pd.read_excel(powerbi_file_path)
                print(f"[POWERBI] Loaded {len(powerbi_df)} rows, {len(powerbi_df.columns)} columns")
                
                allure.attach(
                    f"Rows: {len(powerbi_df)}\n"
                    f"Columns: {len(powerbi_df.columns)}\n"
                    f"Column Names: {', '.join(powerbi_df.columns.tolist())}",
                    'PowerBI Data Summary',
                    allure.attachment_type.TEXT
                )
            
            # Step 3: Connect to Snowflake and Fetch Data
            with allure.step('Fetch Snowflake Table Data'):
                with SnowflakeConnector() as sf_conn:
                    # Get table information
                    table_name = VALIDATION_CONFIG['table_name']
                    table_info = sf_conn.get_table_info(table_name)
                    
                    # Fetch table data
                    snowflake_df = sf_conn.get_table_data(table_name)
                    
                    print(f"[SNOWFLAKE] Loaded {len(snowflake_df)} rows, {len(snowflake_df.columns)} columns")
                    
                    allure.attach(
                        f"Table: {table_name}\n"
                        f"Rows: {len(snowflake_df)}\n"
                        f"Columns: {len(snowflake_df.columns)}\n"
                        f"Column Names: {', '.join(snowflake_df.columns.tolist())}",
                        'Snowflake Data Summary',
                        allure.attachment_type.TEXT
                    )
            
            # Step 4: Validate Data
            with allure.step('Validate PowerBI vs Snowflake Data'):
                validator = DataValidator(powerbi_df, snowflake_df)
                validation_summary = validator.run_all_validations()
                
                # Assert validation passed
                assert validation_summary['pass_rate'] >= 80, \
                    f"Data validation failed: Only {validation_summary['pass_rate']:.1f}% tests passed"
                
                print(f"\n[SUCCESS] ✅ Data validation completed!")
                print(f"Pass Rate: {validation_summary['pass_rate']:.1f}%")
            
        except Exception as e:
            print(f"[ERROR] Test failed: {e}")
            allure.attach(
                str(e),
                'Test Error',
                allure.attachment_type.TEXT
            )
            raise
    
    def test_snowflake_connection_only(self):
        """Test Snowflake connection without PowerBI"""
        
        with allure.step('Test Snowflake Connection'):
            with SnowflakeConnector() as sf_conn:
                # Get table info
                table_name = VALIDATION_CONFIG['table_name']
                table_info = sf_conn.get_table_info(table_name)
                
                assert table_info['row_count'] > 0, "Table is empty"
                assert table_info['column_count'] > 0, "Table has no columns"
                
                print(f"[SUCCESS] ✅ Snowflake connection test passed!")
                print(f"Table: {table_name}")
                print(f"Rows: {table_info['row_count']}")
                print(f"Columns: {table_info['column_count']}")
    
    def test_validate_existing_files(self):
        """Validate using existing PowerBI Excel file (no download)"""
        
        # Find most recent PowerBI download
        from config.config import DOWNLOADS_DIR
        
        excel_files = list(DOWNLOADS_DIR.glob('*.xlsx'))
        if not excel_files:
            pytest.skip("No Excel files found in downloads directory")
        
        # Use most recent file
        powerbi_file = max(excel_files, key=lambda x: x.stat().st_mtime)
        
        with allure.step(f'Load PowerBI File: {powerbi_file.name}'):
            powerbi_df = pd.read_excel(powerbi_file)
            print(f"[POWERBI] Loaded {len(powerbi_df)} rows from {powerbi_file.name}")
        
        with allure.step('Fetch Snowflake Data'):
            with SnowflakeConnector() as sf_conn:
                table_name = VALIDATION_CONFIG['table_name']
                snowflake_df = sf_conn.get_table_data(table_name)
                print(f"[SNOWFLAKE] Loaded {len(snowflake_df)} rows")
        
        with allure.step('Validate Data'):
            validator = DataValidator(powerbi_df, snowflake_df)
            validation_summary = validator.run_all_validations()
            
            assert validation_summary['pass_rate'] >= 80, \
                f"Validation failed: {validation_summary['pass_rate']:.1f}% pass rate"
            
            print(f"[SUCCESS] ✅ Validation passed: {validation_summary['pass_rate']:.1f}%")


@allure.feature('Snowflake Queries')
@allure.story('Custom Query Execution')
class TestSnowflakeQueries:
    """Test custom Snowflake queries"""
    
    def test_custom_query(self):
        """Execute custom SQL query"""
        
        with SnowflakeConnector() as sf_conn:
            # Simple query to get row count
            query = f"""
            SELECT COUNT(*) as total_rows
            FROM {VALIDATION_CONFIG['table_name']}
            """
            
            result = sf_conn.execute_query(query)
            
            print(f"[SNOWFLAKE] Query results:")
            print(result)
            
            assert not result.empty, "Query returned no results"
            assert result['TOTAL_ROWS'].iloc[0] >= 0, "Row count should be non-negative"
