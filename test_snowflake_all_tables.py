"""
Quick Test: Verify Snowflake Connector Reads All Tables
Tests connection to CUSTOMERS, ORDERS, and ORDER_ITEMS tables
"""

from utils.snowflake_connector import SnowflakeConnector
from config.snowflake_config import SNOWFLAKE_TABLES, SNOWFLAKE_CONFIG
from utils.logger import log_info, log_step, log_data, log_error, log_test_start, log_test_end
import time


def test_all_tables():
 """Test reading all three tables from Snowflake"""
 
 test_name = "Snowflake All Tables Test"
 log_test_start(test_name)
 start_time = time.time()
 
 print("\n" + "="*80)
 print("TESTING SNOWFLAKE CONNECTOR - ALL TABLES")
 print("="*80)
 
 print(f"\n Database: {SNOWFLAKE_CONFIG['database']}")
 print(f" Schema: {SNOWFLAKE_CONFIG['schema']}")
 print(f"\n Tables to verify:")
 for key, table_name in SNOWFLAKE_TABLES.items():
 print(f" - {table_name}")
 
 try:
 log_step("Connect to Snowflake")
 
 with SnowflakeConnector() as sf_conn:
 results = {}
 
 print("\n" + "="*80)
 print("READING ALL TABLES")
 print("="*80 + "\n")
 
 # Test each table
 for key, table_name in SNOWFLAKE_TABLES.items():
 log_step(f"Reading table: {table_name}")
 print(f"\n Table: {table_name}")
 print("-" * 80)
 
 try:
 # Get table info
 table_info = sf_conn.get_table_info(table_name)
 
 # Get actual data
 df = sf_conn.get_table_data(table_name)
 
 results[table_name] = {
 'success': True,
 'rows': len(df),
 'columns': len(df.columns),
 'column_names': list(df.columns),
 'sample_data': df.head(3).to_dict('records') if len(df) > 0 else []
 }
 
 print(f" SUCCESS")
 print(f" Rows: {len(df)}")
 print(f" Columns: {len(df.columns)}")
 print(f" Column Names: {', '.join(df.columns)}")
 
 if len(df) > 0:
 print(f"\n Sample Data (first 3 rows):")
 print(df.head(3).to_string(index=False))
 
 log_data(f"Table: {table_name}", {
 "Status": "SUCCESS",
 "Rows": len(df),
 "Columns": len(df.columns),
 "Column Names": ', '.join(df.columns)
 })
 
 except Exception as e:
 results[table_name] = {
 'success': False,
 'error': str(e)
 }
 print(f" FAILED: {e}")
 log_error(f"Failed to read {table_name}: {str(e)}")
 
 # Summary
 print("\n" + "="*80)
 print("SUMMARY")
 print("="*80)
 
 success_count = sum(1 for r in results.values() if r.get('success', False))
 total_count = len(results)
 
 print(f"\n Successfully read: {success_count}/{total_count} tables")
 
 for table_name, result in results.items():
 if result.get('success'):
 print(f" {table_name}: {result['rows']} rows, {result['columns']} columns")
 else:
 print(f" {table_name}: {result.get('error', 'Unknown error')}")
 
 # Detailed summary
 print("\n" + "="*80)
 print("DETAILED SUMMARY")
 print("="*80 + "\n")
 
 total_rows = sum(r.get('rows', 0) for r in results.values() if r.get('success'))
 
 summary_data = {
 "Database": SNOWFLAKE_CONFIG['database'],
 "Schema": SNOWFLAKE_CONFIG['schema'],
 "Tables Tested": total_count,
 "Tables Readable": success_count,
 "Total Rows": total_rows
 }
 
 for key, value in summary_data.items():
 print(f"{key}: {value}")
 
 log_data("Final Summary", summary_data)
 
 # Verification
 assert success_count == total_count, f"Only {success_count}/{total_count} tables readable"
 
 duration = time.time() - start_time
 log_test_end(test_name, "PASSED")
 
 print("\n" + "="*80)
 print(f" ALL TESTS PASSED in {duration:.2f}s")
 print("="*80 + "\n")
 
 print(" CONFIRMATION: Your Snowflake connector CAN read all 3 tables:")
 print(f" CUSTOMERS: {results['CUSTOMERS']['rows']} rows")
 print(f" ORDERS: {results['ORDERS']['rows']} rows")
 print(f" ORDER_ITEMS: {results['ORDER_ITEMS']['rows']} rows")
 
 return results
 
 except Exception as e:
 log_error(f"Test failed: {str(e)}", exc_info=True)
 log_test_end(test_name, "FAILED")
 print(f"\n TEST FAILED: {e}")
 raise


if __name__ == "__main__":
 test_all_tables()
