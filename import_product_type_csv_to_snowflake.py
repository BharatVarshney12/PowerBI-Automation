"""
Import CSV Data to Snowflake - Spend by Product Type
Imports Spend by product type.csv into PowerBI_learning.TRAINING_POWERBI.SPEND_BY_PRODUCT_TYPE table
"""

import pandas as pd
from pathlib import Path
import sys
from utils.snowflake_connector import SnowflakeConnector
from utils.logger import (
 log_test_start, log_test_end, log_step, log_action,
 log_verification, log_data, log_error, log_info
)


def import_product_type_csv_to_snowflake():
 """Import Spend by Product Type CSV data to Snowflake table and verify"""
 
 test_name = "Import Product Type CSV to Snowflake"
 log_test_start(test_name)
 
 print("\n" + "="*80)
 print("IMPORTING SPEND BY PRODUCT TYPE CSV TO SNOWFLAKE")
 print("="*80)
 
 try:
 # Step 1: Load CSV file
 log_step("Load CSV File")
 csv_file = Path(__file__).parent / 'Spend by product type.csv'
 
 if not csv_file.exists():
 log_error(f"CSV file not found: {csv_file}")
 raise FileNotFoundError(f"CSV file not found: {csv_file}")
 
 log_action("Reading CSV file", str(csv_file))
 
 # Read CSV, skip the filter rows at the bottom
 df = pd.read_csv(csv_file)
 
 # Remove empty rows
 df = df.dropna(how='all')
 
 # Remove filter description rows (rows where first column starts with "Applied filters")
 df = df[~df.iloc[:, 0].astype(str).str.contains('Applied filters', na=False)]
 
 log_data("CSV Data Loaded", {
 "File": csv_file.name,
 "Rows": len(df),
 "Columns": len(df.columns),
 "Column Names": ', '.join(df.columns)
 })
 
 print(f"\n[CSV] Loaded {len(df)} rows from {csv_file.name}")
 print(f"[CSV] Columns: {list(df.columns)}")
 print(f"\n[CSV] Sample Data (RAW):")
 print(df.head())
 
 # Step 1.5: Clean and transform CSV data
 log_step("Clean and transform CSV data")
 
 # Map CSV column names to Snowflake column names
 column_mapping = {
 'Claim Form Type': 'CLAIM_FORM_TYPE',
 'Product': 'PRODUCT',
 'PMPM Prev Year': 'PMPM_PREV_YEAR',
 'PMPM': 'PMPM',
 'PMPM YoY%': 'PMPM_YOY_PERCENT',
 'Total Paid Prev Year': 'TOTAL_PAID_PREV_YEAR',
 'Total Paid': 'TOTAL_PAID',
 'Total Paid YoY%': 'TOTAL_PAID_YOY_PERCENT',
 'Cost Per Claim Prev year ': 'COST_PER_CLAIM_PREV_YEAR', # Note: extra space in CSV
 'Cost Per Claim': 'COST_PER_CLAIM',
 'Cost Per Claim YoY%': 'COST_PER_CLAIM_YOY_PERCENT'
 }
 
 # Rename columns
 df = df.rename(columns=column_mapping)
 
 log_action("Renamed columns to match Snowflake table", str(list(df.columns)))
 print(f"\n[TRANSFORM] Renamed columns to: {list(df.columns)}")
 
 # Clean numeric columns (remove $, commas, and convert percentages)
 numeric_columns = [
 'PMPM_PREV_YEAR', 'PMPM', 'TOTAL_PAID_PREV_YEAR', 'TOTAL_PAID',
 'COST_PER_CLAIM_PREV_YEAR', 'COST_PER_CLAIM'
 ]
 
 percent_columns = [
 'PMPM_YOY_PERCENT', 'TOTAL_PAID_YOY_PERCENT', 'COST_PER_CLAIM_YOY_PERCENT'
 ]
 
 print(f"\n[TRANSFORM] Cleaning numeric columns...")
 
 # Clean dollar amount columns
 for col in numeric_columns:
 # Remove $ and all commas, then convert to float
 df[col] = df[col].astype(str).str.replace('$', '').str.replace(',', '').astype(float)
 
 # Clean percentage columns (remove % and convert to decimal)
 for col in percent_columns:
 # Remove % and convert to float (keep as percentage, e.g., 0.6% becomes 0.6)
 df[col] = df[col].astype(str).str.replace('%', '').astype(float)
 
 # Handle NULL values in Product column (Total row has empty Product)
 df['PRODUCT'] = df['PRODUCT'].fillna('Total')
 
 log_action("Cleaned numeric data", f"{len(numeric_columns)} dollar columns, {len(percent_columns)} percent columns")
 
 print(f"\n[CSV] Sample Data (CLEANED):")
 print(df.head())
 
 # Step 2: Connect to Snowflake
 log_step("Connect to Snowflake")
 
 with SnowflakeConnector() as sf_conn:
 
 # Switch to PowerBI_learning database and TRAINING_POWERBI schema
 log_action("Switching to PowerBI_learning database")
 sf_conn.cursor.execute("USE WAREHOUSE PowerBI")
 sf_conn.cursor.execute("USE DATABASE PowerBI_learning")
 sf_conn.cursor.execute("USE SCHEMA TRAINING_POWERBI")
 
 print(f"\n[SNOWFLAKE] Using warehouse: PowerBI")
 print(f"[SNOWFLAKE] Using database: PowerBI_learning")
 print(f"[SNOWFLAKE] Using schema: TRAINING_POWERBI")
 
 # Step 3: Check if table exists
 log_step("Check if table SPEND_BY_PRODUCT_TYPE exists")
 
 check_table_query = """
 SELECT COUNT(*) as TABLE_EXISTS
 FROM INFORMATION_SCHEMA.TABLES 
 WHERE TABLE_SCHEMA = 'TRAINING_POWERBI' 
 AND TABLE_NAME = 'SPEND_BY_PRODUCT_TYPE'
 """
 
 result = sf_conn.execute_query(check_table_query)
 table_exists = result.iloc[0]['TABLE_EXISTS'] > 0
 
 log_verification("Table exists", table_exists)
 
 if not table_exists:
 log_error("Table SPEND_BY_PRODUCT_TYPE does not exist")
 raise Exception("Table SPEND_BY_PRODUCT_TYPE does not exist in PowerBI_learning.TRAINING_POWERBI schema")
 
 print(f"[SNOWFLAKE] Table SPEND_BY_PRODUCT_TYPE exists")
 
 # Step 4: Get table structure
 log_step("Get table structure")
 
 describe_query = "DESCRIBE TABLE SPEND_BY_PRODUCT_TYPE"
 table_structure = sf_conn.execute_query(describe_query)
 
 print(f"\n[SNOWFLAKE] Table Structure:")
 print(table_structure[['name', 'type', 'null?']])
 
 # Step 5: Clear existing data (optional - uncomment if needed)
 log_step("Clear existing data from table")
 log_action("Truncating table SPEND_BY_PRODUCT_TYPE")
 sf_conn.cursor.execute("TRUNCATE TABLE SPEND_BY_PRODUCT_TYPE")
 print(f"[SNOWFLAKE] Table truncated")
 
 # Step 6: Insert data from CSV
 log_step("Insert CSV data into Snowflake table")
 
 # Prepare insert statement with proper column names (no quotes needed for uppercase columns)
 columns = ', '.join(df.columns)
 placeholders = ', '.join(['%s'] * len(df.columns))
 insert_query = f"INSERT INTO SPEND_BY_PRODUCT_TYPE ({columns}) VALUES ({placeholders})"
 
 log_action("Inserting data", f"{len(df)} rows")
 print(f"\n[SNOWFLAKE] Inserting {len(df)} rows...")
 print(f"[SNOWFLAKE] Insert query: {insert_query}")
 
 # Insert data row by row
 inserted_count = 0
 for index, row in df.iterrows():
 try:
 values = tuple(row)
 print(f"[DEBUG] Row {index}: {values}")
 sf_conn.cursor.execute(insert_query, values)
 inserted_count += 1
 print(f"[SNOWFLAKE] Inserted row {index + 1}/{len(df)}")
 except Exception as e:
 log_error(f"Failed to insert row {index}: {str(e)}")
 print(f"[ERROR] Row {index}: {e}")
 print(f"[ERROR] Values: {tuple(row)}")
 
 log_data("Insert Results", {
 "Total Rows": len(df),
 "Inserted": inserted_count,
 "Failed": len(df) - inserted_count
 })
 
 print(f"[SNOWFLAKE] Inserted {inserted_count}/{len(df)} rows")
 
 # Step 7: Verify data was inserted
 log_step("Verify data was imported successfully")
 
 verify_query = "SELECT COUNT(*) as ROW_COUNT FROM SPEND_BY_PRODUCT_TYPE"
 verify_result = sf_conn.execute_query(verify_query)
 snowflake_row_count = verify_result.iloc[0]['ROW_COUNT']
 
 log_verification("Row count matches", snowflake_row_count == len(df))
 
 print(f"\n[VERIFICATION] CSV rows: {len(df)}")
 print(f"[VERIFICATION] Snowflake rows: {snowflake_row_count}")
 
 if snowflake_row_count == len(df):
 print(f"[VERIFICATION] Row count MATCHES!")
 else:
 print(f"[VERIFICATION] Row count MISMATCH!")
 
 # Step 8: Show sample data from Snowflake
 log_step("Retrieve sample data from Snowflake")
 
 sample_query = "SELECT * FROM SPEND_BY_PRODUCT_TYPE LIMIT 10"
 sample_data = sf_conn.execute_query(sample_query)
 
 print(f"\n[SNOWFLAKE] Sample Data (first 10 rows):")
 print(sample_data)
 
 log_data("Sample Data", {
 "Rows Retrieved": len(sample_data),
 "Columns": len(sample_data.columns)
 })
 
 # Step 9: Compare CSV vs Snowflake data
 log_step("Compare CSV data vs Snowflake data")
 
 full_query = "SELECT * FROM SPEND_BY_PRODUCT_TYPE ORDER BY CLAIM_FORM_TYPE, PRODUCT"
 snowflake_full_data = sf_conn.execute_query(full_query)
 
 # Sort CSV data the same way
 df_sorted = df.sort_values(by=['CLAIM_FORM_TYPE', 'PRODUCT']).reset_index(drop=True)
 
 print(f"\n[COMPARISON] Comparing data...")
 
 # Compare column names
 csv_cols = set(df.columns)
 sf_cols = set(snowflake_full_data.columns)
 
 cols_match = csv_cols == sf_cols
 log_verification("Column names match", cols_match)
 
 if cols_match:
 print(f"[COMPARISON] Column names MATCH")
 else:
 print(f"[COMPARISON] Column names MISMATCH")
 print(f" CSV only: {csv_cols - sf_cols}")
 print(f" Snowflake only: {sf_cols - csv_cols}")
 
 # Final summary
 print("\n" + "="*80)
 print("IMPORT VERIFICATION SUMMARY")
 print("="*80)
 print(f" CSV file loaded: {len(df)} rows")
 print(f" Snowflake table exists: SPEND_BY_PRODUCT_TYPE")
 print(f" Data inserted: {inserted_count} rows")
 print(f" Verification query: {snowflake_row_count} rows in table")
 
 if snowflake_row_count == len(df) and cols_match:
 print(f"\n SUCCESS! Data imported and verified successfully!")
 log_test_end(test_name, "PASSED")
 else:
 print(f"\n WARNING! Some verification checks failed")
 log_test_end(test_name, "COMPLETED WITH WARNINGS")
 
 print("="*80)
 
 return {
 'csv_rows': len(df),
 'inserted_rows': inserted_count,
 'snowflake_rows': snowflake_row_count,
 'columns_match': cols_match,
 'success': snowflake_row_count == len(df) and cols_match
 }
 
 except Exception as e:
 log_error(f"Import failed: {str(e)}", exc_info=True)
 log_test_end(test_name, "FAILED")
 print(f"\n IMPORT FAILED: {e}")
 raise


if __name__ == "__main__":
 import_product_type_csv_to_snowflake()
