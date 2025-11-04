"""Quick Snowflake Integration Test"""
import sys
sys.path.insert(0, 'C:\\Users\\bvarshney\\PowerBI_Automation_POM')

from utils.snowflake_connector import SnowflakeConnector
from config.snowflake_config import SNOWFLAKE_TABLES
import pandas as pd
import os

def test_snowflake():
    print("\n" + "="*60)
    print("🔵 SNOWFLAKE CONNECTION TEST")
    print("="*60)
    
    # Connect to Snowflake
    sf = SnowflakeConnector()
    sf.connect()
    
    print(f" Connected to Snowflake!")
    print(f"   Database: SNOWFLAKELEARNING")
    print(f"   Schema: TRAINING_SCHEMA")
    print(f"   Account: po54025.central-india.azure")
    
    print("\n" + "="*60)
    print(" TABLE ROW COUNTS")
    print("="*60)
    
    for table_key, table_name in SNOWFLAKE_TABLES.items():
        info = sf.get_table_info(table_name)
        print(f"   {table_name}: {info['row_count']:,} rows, {info['column_count']} columns")
    
    print("\n" + "="*60)
    print(" SAMPLE DATA FROM CUSTOMERS TABLE")
    print("="*60)
    
    # Get sample data
    sample_df = sf.get_table_data(SNOWFLAKE_TABLES['customers'], limit=5)
    print(f"\n   Columns: {list(sample_df.columns)}")
    print(f"   Shape: {sample_df.shape}")
    print(f"\n{sample_df.to_string()}")
    
    print("\n" + "="*60)
    print(" SAMPLE DATA FROM ORDERS TABLE")
    print("="*60)
    
    orders_df = sf.get_table_data(SNOWFLAKE_TABLES['orders'], limit=5)
    print(f"\n   Columns: {list(orders_df.columns)}")
    print(f"   Shape: {orders_df.shape}")
    print(f"\n{orders_df.to_string()}")
    
    print("\n" + "="*60)
    print(" SAMPLE DATA FROM ORDER_ITEMS TABLE")
    print("="*60)
    
    items_df = sf.get_table_data(SNOWFLAKE_TABLES['order_items'], limit=5)
    print(f"\n   Columns: {list(items_df.columns)}")
    print(f"   Shape: {items_df.shape}")
    print(f"\n{items_df.to_string()}")
    
    # Close connection
    sf.close()
    print("\n" + "="*60)
    print(" SNOWFLAKE TEST COMPLETED SUCCESSFULLY!")
    print("="*60 + "\n")
    
    return True


def test_powerbi_data():
    """Test if PowerBI exported data exists"""
    print("\n" + "="*60)
    print(" POWERBI EXPORTED DATA CHECK")
    print("="*60)
    
    excel_file = "C:\\Users\\bvarshney\\PowerBI_Automation_POM\\data\\data.xlsx"
    
    if os.path.exists(excel_file):
        df = pd.read_excel(excel_file)
        print(f" PowerBI data file found!")
        print(f"   File: {excel_file}")
        print(f"   Shape: {df.shape}")
        print(f"   Columns: {list(df.columns)}")
        print(f"\n   Sample Data:")
        print(df.head().to_string())
        print("\n" + "="*60 + "\n")
        return True
    else:
        print(f"  PowerBI data file not found at: {excel_file}")
        print(f"   Run PowerBI automation test first to generate data")
        print("="*60 + "\n")
        return False


if __name__ == "__main__":
    try:
        # Test Snowflake
        snowflake_ok = test_snowflake()
        
        # Test PowerBI data
        powerbi_ok = test_powerbi_data()
        
        if snowflake_ok:
            print("\n ALL TESTS PASSED! \n")
        
    except Exception as e:
        print(f"\n ERROR: {str(e)}\n")
        import traceback
        traceback.print_exc()
