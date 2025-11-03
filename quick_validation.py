"""
Quick Validation - Check if Excel and Snowflake row counts match
"""

import pandas as pd
import snowflake.connector

# Snowflake connection
SNOWFLAKE_CONFIG = {
    'user': 'BHARATAARETE',
    'password': 'Parthkalka2609@1234',
    'account': 'po54025.central-india.azure',
    'warehouse': 'POWERBI',
    'database': 'POWERBI_LEARNING',
    'schema': 'TRAINING_POWERBI'
}

def quick_check():
    """Quick validation check"""
    
    print("\n" + "="*80)
    print("QUICK VALIDATION - ROW COUNT CHECK")
    print("="*80)
    
    tables = [
        ('power bi actual report/Spend by code.xlsx', 'SPEND_BY_CODE'),
        ('power bi actual report/Spend by product type.xlsx', 'SPEND_BY_PRODUCT_TYPE'),
        ('power bi actual report/Spend by  bill type.xlsx', 'SPEND_BY_BILL_TYPE')
    ]
    
    conn = snowflake.connector.connect(**SNOWFLAKE_CONFIG)
    cursor = conn.cursor()
    
    all_match = True
    
    for excel_file, table_name in tables:
        print(f"\n📊 {table_name}:")
        
        # Excel count
        df = pd.read_excel(excel_file)
        excel_count = len(df)
        
        # Snowflake count
        cursor.execute(f"SELECT COUNT(*) FROM {SNOWFLAKE_CONFIG['database']}.{SNOWFLAKE_CONFIG['schema']}.{table_name}")
        sf_count = cursor.fetchone()[0]
        
        match = excel_count == sf_count
        status = "✅ MATCH" if match else "❌ MISMATCH"
        
        print(f"   Excel rows: {excel_count}")
        print(f"   Snowflake rows: {sf_count}")
        print(f"   Status: {status}")
        
        if not match:
            all_match = False
    
    cursor.close()
    conn.close()
    
    print(f"\n" + "="*80)
    if all_match:
        print("🎉 SUCCESS! All tables have matching row counts!")
    else:
        print("⚠️  Some tables have mismatches")
    print("="*80 + "\n")

if __name__ == "__main__":
    quick_check()
