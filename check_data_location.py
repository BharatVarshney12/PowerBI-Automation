"""
Check where data is actually loaded in both schemas
"""

from utils.snowflake_connector import SnowflakeConnector

def check_all_schemas():
    print("\n" + "="*80)
    print("CHECKING DATA LOCATION IN ALL SCHEMAS")
    print("="*80)
    
    with SnowflakeConnector() as sf_conn:
        
        sf_conn.cursor.execute("USE WAREHOUSE PowerBI")
        sf_conn.cursor.execute("USE DATABASE PowerBI_learning")
        
        print(f"\n[DATABASE] Using: PowerBI_learning")
        
        # Check PUBLIC schema
        print(f"\n{'='*80}")
        print("CHECKING PUBLIC SCHEMA")
        print(f"{'='*80}")
        
        sf_conn.cursor.execute("USE SCHEMA PUBLIC")
        
        for table in ['SPEND_BY_CODE', 'SPEND_BY_PRODUCT_TYPE', 'SPEND_BY_BILL_TYPE']:
            try:
                query = f"SELECT COUNT(*) as ROW_COUNT FROM {table}"
                result = sf_conn.execute_query(query)
                count = result.iloc[0]['ROW_COUNT']
                print(f"✅ PUBLIC.{table}: {count} rows")
            except Exception as e:
                print(f"❌ PUBLIC.{table}: Error - {e}")
        
        # Check TRAINING_POWERBI schema
        print(f"\n{'='*80}")
        print("CHECKING TRAINING_POWERBI SCHEMA")
        print(f"{'='*80}")
        
        sf_conn.cursor.execute("USE SCHEMA TRAINING_POWERBI")
        
        for table in ['SPEND_BY_CODE', 'SPEND_BY_PRODUCT_TYPE', 'SPEND_BY_BILL_TYPE']:
            try:
                query = f"SELECT COUNT(*) as ROW_COUNT FROM {table}"
                result = sf_conn.execute_query(query)
                count = result.iloc[0]['ROW_COUNT']
                print(f"✅ TRAINING_POWERBI.{table}: {count} rows")
            except Exception as e:
                print(f"❌ TRAINING_POWERBI.{table}: Error - {e}")
        
        print(f"\n{'='*80}")
        print("SUMMARY")
        print(f"{'='*80}")

if __name__ == "__main__":
    check_all_schemas()
