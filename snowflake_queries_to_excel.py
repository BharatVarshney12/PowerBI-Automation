"""
Run Snowflake Validation Queries and Export to Excel
Executes comprehensive SQL queries on all three tables and saves results to Excel
"""

import pandas as pd
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

# Tables to query
TABLES = ['SPEND_BY_CODE', 'SPEND_BY_PRODUCT_TYPE', 'SPEND_BY_BILL_TYPE']

def run_query(cursor, query, description, executed_queries=None):
 """Execute a query and return results as DataFrame"""
 print(f" {description}")
 cursor.execute(query)
 columns = [col[0] for col in cursor.description]
 data = cursor.fetchall()
 df = pd.DataFrame(data, columns=columns)
 
 # Track the query
 if executed_queries is not None:
 executed_queries.append({
 'Query_Number': len(executed_queries) + 1,
 'Description': description,
 'SQL_Query': query.strip(),
 'Rows_Retrieved': len(df)
 })
 
 # Convert timezone-aware datetime columns to timezone-naive
 for col in df.columns:
 if pd.api.types.is_datetime64_any_dtype(df[col]):
 df[col] = df[col].dt.tz_localize(None)
 
 print(f" Retrieved {len(df)} rows")
 return df

def generate_snowflake_queries_excel():
 """Generate comprehensive Excel file with all Snowflake query results"""
 
 print("\n" + "="*100)
 print("SNOWFLAKE SQL QUERIES - EXPORT TO EXCEL")
 print("="*100)
 
 # Create output directory
 output_dir = Path('validation_reports')
 output_dir.mkdir(exist_ok=True)
 
 timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
 excel_file = output_dir / f'Snowflake_SQL_Results_{timestamp}.xlsx'
 
 print(f"\n Connecting to Snowflake...")
 conn = snowflake.connector.connect(**SNOWFLAKE_CONFIG)
 cursor = conn.cursor()
 
 # Track all executed queries
 executed_queries = []
 
 try:
 with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
 
 # Sheet 1: Database and Schema Info
 print(f"\n Database Information:")
 
 db_info_query = f"""
 SELECT 
 CURRENT_DATABASE() as DATABASE_NAME,
 CURRENT_SCHEMA() as SCHEMA_NAME,
 CURRENT_WAREHOUSE() as WAREHOUSE_NAME,
 CURRENT_USER() as USER_NAME,
 CURRENT_TIMESTAMP() as QUERY_TIMESTAMP
 """
 df_db_info = run_query(cursor, db_info_query, "Database Information", executed_queries)
 df_db_info.to_excel(writer, sheet_name='Database_Info', index=False)
 
 # Sheet 2: All Tables List
 print(f"\n Tables in Schema:")
 
 tables_query = f"""
 SELECT 
 TABLE_NAME,
 TABLE_TYPE,
 ROW_COUNT,
 CREATED,
 LAST_ALTERED
 FROM INFORMATION_SCHEMA.TABLES
 WHERE TABLE_SCHEMA = '{SNOWFLAKE_CONFIG['schema']}'
 ORDER BY TABLE_NAME
 """
 df_tables = run_query(cursor, tables_query, "Tables List", executed_queries)
 df_tables.to_excel(writer, sheet_name='All_Tables', index=False)
 
 # Process each table
 for table_name in TABLES:
 print(f"\n{'='*100}")
 print(f"PROCESSING TABLE: {table_name}")
 print(f"{'='*100}")
 
 # Query 1: Full Data
 print(f"\n1⃣ Full Table Data:")
 query_full = f"SELECT * FROM {table_name}"
 df_full = run_query(cursor, query_full, f"All data from {table_name}", executed_queries)
 df_full.to_excel(writer, sheet_name=f'{table_name}_Data', index=False)
 
 # Query 2: Row Count
 print(f"\n2⃣ Row Count:")
 query_count = f"SELECT COUNT(*) as ROW_COUNT FROM {table_name}"
 df_count = run_query(cursor, query_count, f"Row count for {table_name}", executed_queries)
 df_count.to_excel(writer, sheet_name=f'{table_name}_RowCount', index=False)
 
 # Query 3: Column Information
 print(f"\n3⃣ Column Information:")
 query_columns = f"""
 SELECT 
 ORDINAL_POSITION,
 COLUMN_NAME,
 DATA_TYPE,
 IS_NULLABLE,
 CHARACTER_MAXIMUM_LENGTH,
 NUMERIC_PRECISION,
 NUMERIC_SCALE
 FROM INFORMATION_SCHEMA.COLUMNS
 WHERE TABLE_SCHEMA = '{SNOWFLAKE_CONFIG['schema']}'
 AND TABLE_NAME = '{table_name}'
 ORDER BY ORDINAL_POSITION
 """
 df_columns = run_query(cursor, query_columns, f"Column details for {table_name}", executed_queries)
 df_columns.to_excel(writer, sheet_name=f'{table_name}_Columns', index=False)
 
 # Query 4: NULL Counts per Column
 print(f"\n4⃣ NULL Value Counts:")
 
 # Get column names
 cursor.execute(f"SELECT * FROM {table_name} LIMIT 1")
 columns = [col[0] for col in cursor.description]
 
 null_counts = []
 for col in columns:
 query_null = f"SELECT COUNT(*) as NULL_COUNT FROM {table_name} WHERE {col} IS NULL"
 cursor.execute(query_null)
 null_count = cursor.fetchone()[0]
 null_counts.append({
 'COLUMN_NAME': col,
 'NULL_COUNT': null_count,
 'TOTAL_ROWS': len(df_full),
 'NULL_PERCENTAGE': round((null_count / len(df_full) * 100), 2) if len(df_full) > 0 else 0
 })
 
 # Track NULL count query
 executed_queries.append({
 'Query_Number': len(executed_queries) + 1,
 'Description': f"NULL count for {table_name}.{col}",
 'SQL_Query': query_null.strip(),
 'Rows_Retrieved': 1
 })
 
 df_nulls = pd.DataFrame(null_counts)
 print(f" NULL counts calculated for {len(columns)} columns")
 df_nulls.to_excel(writer, sheet_name=f'{table_name}_NULLs', index=False)
 
 # Query 5: Data Summary Statistics (for numeric columns)
 print(f"\n5⃣ Data Summary Statistics:")
 
 numeric_stats = []
 for col in columns:
 # Try to get stats for numeric columns
 try:
 query_stats = f"""
 SELECT 
 '{col}' as COLUMN_NAME,
 MIN({col}) as MIN_VALUE,
 MAX({col}) as MAX_VALUE,
 AVG({col}) as AVG_VALUE,
 COUNT(DISTINCT {col}) as DISTINCT_COUNT
 FROM {table_name}
 WHERE {col} IS NOT NULL
 """
 cursor.execute(query_stats)
 result = cursor.fetchone()
 if result:
 numeric_stats.append({
 'COLUMN_NAME': result[0],
 'MIN_VALUE': result[1],
 'MAX_VALUE': result[2],
 'AVG_VALUE': result[3],
 'DISTINCT_COUNT': result[4]
 })
 
 # Track stats query
 executed_queries.append({
 'Query_Number': len(executed_queries) + 1,
 'Description': f"Statistics for {table_name}.{col}",
 'SQL_Query': query_stats.strip(),
 'Rows_Retrieved': 1
 })
 except:
 # Skip non-numeric columns
 pass
 
 if numeric_stats:
 df_stats = pd.DataFrame(numeric_stats)
 print(f" Statistics calculated for {len(numeric_stats)} numeric columns")
 df_stats.to_excel(writer, sheet_name=f'{table_name}_Stats', index=False)
 
 # Query 6: Distinct Values Count
 print(f"\n6⃣ Distinct Values Count:")
 
 distinct_counts = []
 for col in columns:
 query_distinct = f"SELECT COUNT(DISTINCT {col}) as DISTINCT_COUNT FROM {table_name}"
 cursor.execute(query_distinct)
 distinct_count = cursor.fetchone()[0]
 distinct_counts.append({
 'COLUMN_NAME': col,
 'DISTINCT_COUNT': distinct_count,
 'TOTAL_ROWS': len(df_full),
 'UNIQUENESS_PERCENTAGE': round((distinct_count / len(df_full) * 100), 2) if len(df_full) > 0 else 0
 })
 
 # Track distinct count query
 executed_queries.append({
 'Query_Number': len(executed_queries) + 1,
 'Description': f"Distinct count for {table_name}.{col}",
 'SQL_Query': query_distinct.strip(),
 'Rows_Retrieved': 1
 })
 
 df_distinct = pd.DataFrame(distinct_counts)
 print(f" Distinct counts calculated for {len(columns)} columns")
 df_distinct.to_excel(writer, sheet_name=f'{table_name}_Distinct', index=False)
 
 # Query 7: Sample Data (First 10 rows)
 print(f"\n7⃣ Sample Data (First 10 rows):")
 query_sample = f"SELECT * FROM {table_name} LIMIT 10"
 df_sample = run_query(cursor, query_sample, f"Sample data from {table_name}", executed_queries)
 df_sample.to_excel(writer, sheet_name=f'{table_name}_Sample', index=False)
 
 # Final Summary Sheet
 print(f"\n{'='*100}")
 print(f"GENERATING SUMMARY")
 print(f"{'='*100}")
 
 summary_data = []
 for table_name in TABLES:
 query_summary = f"""
 SELECT 
 '{table_name}' as TABLE_NAME,
 COUNT(*) as ROW_COUNT,
 (SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS 
 WHERE TABLE_SCHEMA = '{SNOWFLAKE_CONFIG['schema']}' 
 AND TABLE_NAME = '{table_name}') as COLUMN_COUNT
 FROM {table_name}
 """
 cursor.execute(query_summary)
 result = cursor.fetchone()
 summary_data.append({
 'TABLE_NAME': result[0],
 'ROW_COUNT': result[1],
 'COLUMN_COUNT': result[2]
 })
 
 # Track summary query
 executed_queries.append({
 'Query_Number': len(executed_queries) + 1,
 'Description': f"Summary for {table_name}",
 'SQL_Query': query_summary.strip(),
 'Rows_Retrieved': 1
 })
 
 df_summary = pd.DataFrame(summary_data)
 df_summary.to_excel(writer, sheet_name='Summary', index=False)
 print(f" Summary sheet created")
 
 # NEW: SQL Queries List Sheet
 print(f"\n Creating SQL Queries List...")
 df_queries = pd.DataFrame(executed_queries)
 df_queries.to_excel(writer, sheet_name='SQL_Queries_List', index=False)
 print(f" SQL Queries List sheet created with {len(executed_queries)} queries")
 
 print(f"\n{'='*100}")
 print(f" EXCEL FILE GENERATED SUCCESSFULLY")
 print(f"{'='*100}")
 print(f"\n File saved: {excel_file}")
 print(f"\n Sheets created:")
 print(f" • Database_Info - Database and connection details")
 print(f" • All_Tables - List of all tables in schema")
 print(f" • Summary - Quick summary of all three tables")
 print(f" • SQL_Queries_List - ALL {len(executed_queries)} SQL QUERIES EXECUTED ")
 
 for table_name in TABLES:
 print(f"\n {table_name}:")
 print(f" • {table_name}_Data - Full table data")
 print(f" • {table_name}_RowCount - Total row count")
 print(f" • {table_name}_Columns - Column information")
 print(f" • {table_name}_NULLs - NULL value counts")
 print(f" • {table_name}_Stats - Numeric statistics")
 print(f" • {table_name}_Distinct - Distinct value counts")
 print(f" • {table_name}_Sample - Sample data (10 rows)")
 
 print(f"\n{'='*100}\n")
 
 except Exception as e:
 print(f"\n Error: {str(e)}")
 import traceback
 traceback.print_exc()
 
 finally:
 cursor.close()
 conn.close()
 print(f" Connection closed")

if __name__ == "__main__":
 generate_snowflake_queries_excel()
