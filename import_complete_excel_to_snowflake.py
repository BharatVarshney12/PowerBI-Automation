"""
Import Complete Excel Data to Snowflake (including Total rows)
This script imports ALL rows from Excel files to match exactly with Excel structure
"""

import pandas as pd
import numpy as np
import snowflake.connector
from pathlib import Path
from datetime import datetime

# Snowflake connection
SNOWFLAKE_CONFIG = {
    'user': 'BHARATAARETE',
    'password': 'Parthkalka2609@1234',
    'account': 'po54025.central-india.azure',
    'warehouse': 'POWERBI',
    'database': 'POWERBI_LEARNING',
    'schema': 'TRAINING_POWERBI'
}

def clean_value(value):
    """Clean Excel values for Snowflake import"""
    if pd.isna(value) or value is None or value == '':
        return None
    
    if isinstance(value, str):
        value = value.strip()
        
        # Remove dollar signs and commas
        if '$' in value or ',' in value:
            value = value.replace('$', '').replace(',', '')
        
        # Remove percentage signs
        if '%' in value:
            value = value.replace('%', '')
        
        # Try to convert to number - always use float for consistency
        try:
            return float(value)
        except:
            return value
    
    if isinstance(value, (int, float)):
        return float(value)  # Convert to float
    
    return value

def import_excel_to_snowflake(excel_file, table_name, column_mapping):
    """Import complete Excel data to Snowflake table"""
    
    print(f"\n{'='*100}")
    print(f"IMPORTING: {excel_file} -> {table_name}")
    print(f"{'='*100}")
    
    # Load Excel
    print(f"\n Loading Excel file...")
    df = pd.read_excel(excel_file, engine='openpyxl')
    
    # Clean column names
    df.columns = [str(col).strip() for col in df.columns]
    
    print(f"    Loaded {len(df)} rows from Excel")
    print(f"    Columns: {list(df.columns)}")
    print(f"\n   First few rows:")
    print(df.head())
    
    # Clean all values
    for col in df.columns:
        df[col] = df[col].apply(clean_value)
    
    # Replace NaN with None
    df = df.replace({pd.NA: None, np.nan: None})
    
    # Remove rows where ALL values are None (blank rows)
    df = df.dropna(how='all')
    
    # Remove filter information rows (rows that start with "Applied filters:")
    first_col = df.columns[0]
    df = df[~df[first_col].astype(str).str.contains('Applied filters', case=False, na=False)]
    
    # Reset index after filtering
    df = df.reset_index(drop=True)
    
    # Rename columns to match Snowflake
    df = df.rename(columns=column_mapping)
    
    print(f"\n    Data cleaned and columns mapped")
    print(f"    Snowflake columns: {list(df.columns)}")
    
    # Connect to Snowflake
    print(f"\n[SNOWFLAKE] Connecting to Snowflake...")
    conn = snowflake.connector.connect(**SNOWFLAKE_CONFIG)
    cursor = conn.cursor()
    
    try:
        # Use database and schema
        cursor.execute(f"USE DATABASE {SNOWFLAKE_CONFIG['database']}")
        cursor.execute(f"USE SCHEMA {SNOWFLAKE_CONFIG['schema']}")
        
        # Clear existing data
        print(f"\n🗑️  Clearing existing data from {table_name}...")
        cursor.execute(f"TRUNCATE TABLE IF EXISTS {table_name}")
        
        # Insert all rows (including Total and blank rows)
        print(f"\n📥 Inserting {len(df)} rows into Snowflake...")
        
        inserted = 0
        failed = 0
        
        for idx, row in df.iterrows():
            try:
                # Build column names and values
                columns = ', '.join(df.columns)
                placeholders = ', '.join(['%s'] * len(df.columns))
                
                # Get values
                values = [row[col] for col in df.columns]
                
                # Insert query
                insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
                
                cursor.execute(insert_query, values)
                inserted += 1
                
                if (idx + 1) % 10 == 0:
                    print(f"   Progress: {idx + 1}/{len(df)} rows inserted...")
                    
            except Exception as e:
                print(f"     Row {idx} failed: {str(e)}")
                failed += 1
        
        print(f"\n    Insert complete: {inserted} rows inserted, {failed} failed")
        
        # Verify row count
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        sf_count = cursor.fetchone()[0]
        
        print(f"\n Verification:")
        print(f"   Excel rows: {len(df)}")
        print(f"   Snowflake rows: {sf_count}")
        
        if sf_count == len(df):
            print(f"    SUCCESS! Row counts MATCH!")
        else:
            print(f"     WARNING! Row count mismatch: Difference = {sf_count - len(df)}")
        
        # Show sample data
        print(f"\n Sample data from Snowflake:")
        cursor.execute(f"SELECT * FROM {table_name} LIMIT 5")
        sample = cursor.fetchall()
        for row in sample:
            print(f"   {row}")
        
    except Exception as e:
        print(f"\n Error: {str(e)}")
        import traceback
        traceback.print_exc()
        
    finally:
        cursor.close()
        conn.close()
        print(f"\n Connection closed")

def main():
    """Main execution"""
    
    print("\n" + "="*100)
    print("IMPORT COMPLETE EXCEL DATA TO SNOWFLAKE (INCLUDING TOTAL ROWS)")
    print("="*100)
    
    # Table 1: Spend by Code
    import_excel_to_snowflake(
        excel_file='power bi actual report/Spend by code.xlsx',
        table_name='SPEND_BY_CODE',
        column_mapping={
            'Claim Form Type': 'CLAIM_FORM_TYPE',
            'PMPM Prev Year': 'PMPM_PREV_YEAR',
            'PMPM': 'PMPM',
            'PMPM YoY%': 'PMPM_YOY_PERCENT',
            'Total Paid Prev Year': 'TOTAL_PAID_PREV_YEAR',
            'Total Paid': 'TOTAL_PAID',
            'Total Paid YoY%': 'TOTAL_PAID_YOY_PERCENT',
            'Cost Per Claim Prev Year': 'COST_PER_CLAIM_PREV_YEAR',
            'Cost Per Claim': 'COST_PER_CLAIM',
            'Cost Per Claim YoY%': 'COST_PER_CLAIM_YOY_PERCENT'
        }
    )
    
    # Table 2: Spend by Product Type
    import_excel_to_snowflake(
        excel_file='power bi actual report/Spend by product type.xlsx',
        table_name='SPEND_BY_PRODUCT_TYPE',
        column_mapping={
            'Claim Form Type': 'CLAIM_FORM_TYPE',
            'Product': 'PRODUCT',
            'PMPM Prev Year': 'PMPM_PREV_YEAR',
            'PMPM': 'PMPM',
            'PMPM YoY%': 'PMPM_YOY_PERCENT',
            'Total Paid Prev Year': 'TOTAL_PAID_PREV_YEAR',
            'Total Paid': 'TOTAL_PAID',
            'Total Paid YoY%': 'TOTAL_PAID_YOY_PERCENT',
            'Cost Per Claim Prev year': 'COST_PER_CLAIM_PREV_YEAR',
            'Cost Per Claim': 'COST_PER_CLAIM',
            'Cost Per Claim YoY%': 'COST_PER_CLAIM_YOY_PERCENT'
        }
    )
    
    # Table 3: Spend by Bill Type
    import_excel_to_snowflake(
        excel_file='power bi actual report/Spend by  bill type.xlsx',
        table_name='SPEND_BY_BILL_TYPE',
        column_mapping={
            'Claim Form Type': 'CLAIM_FORM_TYPE',
            'Bill Type Code': 'BILL_TYPE',
            'PMPM Prev Year': 'PMPM_PREV_YEAR',
            'PMPM': 'PMPM',
            'PMPM YoY%': 'PMPM_YOY_PERCENT',
            'Total Paid Prev Year': 'TOTAL_PAID_PREV_YEAR',
            'Total Paid': 'TOTAL_PAID',
            'Total Paid YoY%': 'TOTAL_PAID_YOY_PERCENT',
            'Cost Per Claim Prev Year': 'COST_PER_CLAIM_PREV_YEAR',
            'Cost Per Claim': 'COST_PER_CLAIM',
            'Cost Per Claim YoY%': 'COST_PER_CLAIM_YOY_PERCENT'
        }
    )
    
    print("\n" + "="*100)
    print(" ALL TABLES IMPORTED SUCCESSFULLY")
    print("="*100)
    print("\nNext step: Run the validation script again to verify all data matches!")
    print("Command: python compare_excel_snowflake_reports.py")
    print("="*100 + "\n")

if __name__ == "__main__":
    main()
