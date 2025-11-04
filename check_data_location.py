"""
Check data location in TRAINING_POWERBI schema
"""

from utils.snowflake_connector import SnowflakeConnector

def check_data_location():
 print("\n" + "="*80)
 print("CHECKING DATA LOCATION IN TRAINING_POWERBI SCHEMA")
 print("="*80)
 
 with SnowflakeConnector() as sf_conn:
 
 sf_conn.cursor.execute("USE WAREHOUSE POWERBI")
 sf_conn.cursor.execute("USE DATABASE POWERBI_LEARNING")
 sf_conn.cursor.execute("USE SCHEMA TRAINING_POWERBI")
 
 print(f"\n[DATABASE] Using: POWERBI_LEARNING")
 print(f"[SCHEMA] Using: TRAINING_POWERBI")
 
 # Check TRAINING_POWERBI schema
 print(f"\n{'='*80}")
 print("CHECKING TABLES")
 print(f"{'='*80}")
 
 for table in ['SPEND_BY_CODE', 'SPEND_BY_PRODUCT_TYPE', 'SPEND_BY_BILL_TYPE']:
 try:
 query = f"SELECT COUNT(*) as ROW_COUNT FROM {table}"
 result = sf_conn.execute_query(query)
 count = result.iloc[0]['ROW_COUNT']
 print(f" {table}: {count} rows")
 except Exception as e:
 print(f" {table}: Error - {e}")
 
 print(f"\n{'='*80}")
 print("DATA LOCATION CHECK COMPLETE")
 print(f"{'='*80}")

if __name__ == "__main__":
 check_data_location()
