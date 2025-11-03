"""
Check what data is actually in the SPEND_BY_BILL_TYPE table
"""

from utils.snowflake_connector import SnowflakeConnector

def check_bill_type_table():
    print("\n" + "="*80)
    print("CHECKING SPEND_BY_BILL_TYPE TABLE DATA")
    print("="*80)
    
    with SnowflakeConnector() as sf_conn:
        
        # Switch to PowerBI_learning database
        sf_conn.cursor.execute("USE WAREHOUSE PowerBI")
        sf_conn.cursor.execute("USE DATABASE PowerBI_learning")
        sf_conn.cursor.execute("USE SCHEMA PUBLIC")
        
        print(f"\n[SNOWFLAKE] Using database: PowerBI_learning")
        print(f"[SNOWFLAKE] Using schema: PUBLIC")
        
        # Check row count
        count_query = "SELECT COUNT(*) as ROW_COUNT FROM SPEND_BY_BILL_TYPE"
        count_result = sf_conn.execute_query(count_query)
        row_count = count_result.iloc[0]['ROW_COUNT']
        
        print(f"\n[INFO] Total rows in table: {row_count}")
        
        # Get all data
        query = "SELECT * FROM SPEND_BY_BILL_TYPE ORDER BY CLAIM_FORM_TYPE, BILL_TYPE LIMIT 20"
        data = sf_conn.execute_query(query)
        
        print(f"\n[DATA] First 20 rows:")
        print(data)
        
        print(f"\n[INFO] Columns: {list(data.columns)}")
        print(f"[INFO] Data types:")
        print(data.dtypes)
        
        # Check for any NULL or unusual values
        print(f"\n[INFO] Checking for NULL values:")
        print(data.isnull().sum())

if __name__ == "__main__":
    check_bill_type_table()
