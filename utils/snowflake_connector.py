"""
Snowflake Connector
Manages Snowflake database connections and queries
"""

import snowflake.connector
import pandas as pd
from config.snowflake_config import SNOWFLAKE_CONFIG
import allure
from allure_commons.types import AttachmentType
from contextlib import contextmanager


class SnowflakeConnector:
    """Handle Snowflake database connections"""
    
    def __init__(self):
        self.connection = None
        self.cursor = None
    
    def connect(self):
        """Establish connection to Snowflake"""
        with allure.step('Connect to Snowflake Database'):
            try:
                self.connection = snowflake.connector.connect(
                    account=SNOWFLAKE_CONFIG['account'],
                    user=SNOWFLAKE_CONFIG['user'],
                    password=SNOWFLAKE_CONFIG['password'],
                    warehouse=SNOWFLAKE_CONFIG['warehouse'],
                    database=SNOWFLAKE_CONFIG['database'],
                    schema=SNOWFLAKE_CONFIG['schema'],
                    role=SNOWFLAKE_CONFIG.get('role', 'ACCOUNTADMIN'),
                    # Disable result caching and JSON parsing issues
                    session_parameters={
                        'QUERY_TAG': 'PowerBI_Automation',
                    }
                )
                
                # Don't use DictCursor to avoid JSON parsing issues
                self.cursor = self.connection.cursor()
                
                print(f"[SNOWFLAKE] ✅ Connected successfully")
                print(f"[SNOWFLAKE] Database: {SNOWFLAKE_CONFIG['database']}")
                print(f"[SNOWFLAKE] Schema: {SNOWFLAKE_CONFIG['schema']}")
                
                allure.attach(
                    f"Account: {SNOWFLAKE_CONFIG['account']}\n"
                    f"Database: {SNOWFLAKE_CONFIG['database']}\n"
                    f"Schema: {SNOWFLAKE_CONFIG['schema']}\n"
                    f"Warehouse: {SNOWFLAKE_CONFIG['warehouse']}",
                    'Snowflake Connection Details',
                    AttachmentType.TEXT
                )
                
                return self
                
            except Exception as e:
                print(f"[SNOWFLAKE] ❌ Connection failed: {e}")
                allure.attach(f'Connection failed: {str(e)}', 'Snowflake Error', AttachmentType.TEXT)
                raise
    
    def execute_query(self, query: str) -> pd.DataFrame:
        """Execute SQL query and return results as DataFrame"""
        with allure.step(f'Execute Snowflake Query'):
            try:
                print(f"[SNOWFLAKE] Executing query...")
                
                # Use default cursor instead of DictCursor to avoid JSON parsing issues
                cursor = self.connection.cursor()
                cursor.execute(query)
                
                # Get column names
                columns = [desc[0] for desc in cursor.description] if cursor.description else []
                
                # Fetch all results
                results = cursor.fetchall()
                cursor.close()
                
                # Convert to DataFrame with explicit column names
                if results:
                    df = pd.DataFrame(results, columns=columns)
                    
                    # Clean up any problematic data types
                    for col in df.columns:
                        # Convert bytes to string if needed
                        if df[col].dtype == 'object':
                            df[col] = df[col].apply(lambda x: str(x) if isinstance(x, bytes) else x)
                    
                    print(f"[SNOWFLAKE] ✅ Query returned {len(df)} rows")
                    
                    allure.attach(
                        f"Query: {query}\n\n"
                        f"Rows returned: {len(df)}\n"
                        f"Columns: {', '.join(df.columns.tolist())}",
                        'Query Execution',
                        AttachmentType.TEXT
                    )
                    
                    return df
                else:
                    print(f"[SNOWFLAKE] Query returned no results")
                    return pd.DataFrame()
                    
            except Exception as e:
                print(f"[SNOWFLAKE] ❌ Query failed: {e}")
                allure.attach(
                    f'Query: {query}\n\nError: {str(e)}',
                    'Query Error',
                    AttachmentType.TEXT
                )
                raise
    
    def get_table_data(self, table_name: str, limit: int = None) -> pd.DataFrame:
        """Fetch all data from a table"""
        with allure.step(f'Fetch data from table: {table_name}'):
            query = f"SELECT * FROM {table_name}"
            if limit:
                query += f" LIMIT {limit}"
            
            return self.execute_query(query)
    
    def get_table_info(self, table_name: str) -> dict:
        """Get table metadata (row count, columns, etc.)"""
        with allure.step(f'Get table info: {table_name}'):
            try:
                # Get row count
                count_query = f"SELECT COUNT(*) as row_count FROM {table_name}"
                count_result = self.execute_query(count_query)
                row_count = count_result['ROW_COUNT'].iloc[0] if not count_result.empty else 0
                
                # Get column information
                columns_query = f"""
                SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_SCHEMA = '{SNOWFLAKE_CONFIG['schema']}'
                AND TABLE_NAME = '{table_name}'
                ORDER BY ORDINAL_POSITION
                """
                columns_info = self.execute_query(columns_query)
                
                info = {
                    'row_count': row_count,
                    'column_count': len(columns_info),
                    'columns': columns_info.to_dict('records') if not columns_info.empty else []
                }
                
                print(f"[SNOWFLAKE] Table {table_name}:")
                print(f"  - Rows: {row_count}")
                print(f"  - Columns: {len(columns_info)}")
                
                allure.attach(
                    f"Table: {table_name}\n"
                    f"Row Count: {row_count}\n"
                    f"Column Count: {len(columns_info)}\n"
                    f"Columns: {', '.join([col['COLUMN_NAME'] for col in info['columns']])}",
                    'Table Information',
                    AttachmentType.TEXT
                )
                
                return info
                
            except Exception as e:
                print(f"[SNOWFLAKE] ❌ Failed to get table info: {e}")
                raise
    
    def close(self):
        """Close Snowflake connection"""
        with allure.step('Close Snowflake Connection'):
            if self.cursor:
                self.cursor.close()
            if self.connection:
                self.connection.close()
            
            print("[SNOWFLAKE] Connection closed")
            allure.attach('Connection closed successfully', 'Snowflake Cleanup', AttachmentType.TEXT)
    
    def __enter__(self):
        """Context manager entry"""
        return self.connect()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()


@contextmanager
def snowflake_connection():
    """Context manager for Snowflake connections"""
    connector = SnowflakeConnector()
    try:
        yield connector.connect()
    finally:
        connector.close()
