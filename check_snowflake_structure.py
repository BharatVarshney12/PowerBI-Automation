"""
Check Snowflake database structure to find the correct schema for SPEND_BY_CODE table
"""

from utils.snowflake_connector import SnowflakeConnector

def check_snowflake_structure():
    print("\n" + "="*80)
    print("CHECKING SNOWFLAKE STRUCTURE")
    print("="*80)
    
    with SnowflakeConnector() as sf_conn:
        
        # Check all databases
        print("\n[1] Checking available databases...")
        sf_conn.cursor.execute("SHOW DATABASES")
        databases = sf_conn.cursor.fetchall()
        print(f"\nDatabases found: {len(databases)}")
        for db in databases:
            print(f"  - {db[1]}")  # Database name is in column 1
        
        # Switch to PowerBI_learning database
        print("\n[2] Switching to PowerBI_learning database...")
        try:
            sf_conn.cursor.execute("USE DATABASE PowerBI_learning")
            print(" Successfully switched to PowerBI_learning")
        except Exception as e:
            print(f" Failed: {e}")
            return
        
        # Check all schemas in PowerBI_learning
        print("\n[3] Checking schemas in PowerBI_learning...")
        sf_conn.cursor.execute("SHOW SCHEMAS IN DATABASE PowerBI_learning")
        schemas = sf_conn.cursor.fetchall()
        print(f"\nSchemas found: {len(schemas)}")
        for schema in schemas:
            print(f"  - {schema[1]}")  # Schema name is in column 1
        
        # Check for SPEND_BY_CODE table in each schema
        print("\n[4] Searching for SPEND_BY_CODE table in all schemas...")
        for schema in schemas:
            schema_name = schema[1]
            try:
                query = f"""
                SELECT TABLE_NAME, TABLE_SCHEMA 
                FROM PowerBI_learning.INFORMATION_SCHEMA.TABLES 
                WHERE TABLE_SCHEMA = '{schema_name}' 
                AND TABLE_NAME = 'SPEND_BY_CODE'
                """
                result = sf_conn.execute_query(query)
                if len(result) > 0:
                    print(f"\n FOUND! Table SPEND_BY_CODE exists in schema: {schema_name}")
                    print(f"   Full path: PowerBI_learning.{schema_name}.SPEND_BY_CODE")
            except Exception as e:
                pass
        
        # List all tables in TRAINING_PowerBI schema
        print("\n[5] Checking tables in TRAINING_POWERBI schema...")
        try:
            sf_conn.cursor.execute("USE SCHEMA TRAINING_POWERBI")
            sf_conn.cursor.execute("SHOW TABLES IN SCHEMA TRAINING_POWERBI")
            tables = sf_conn.cursor.fetchall()
            print(f"\nTables in TRAINING_POWERBI: {len(tables)}")
            for table in tables:
                print(f"  - {table[1]}")  # Table name is in column 1
        except Exception as e:
            print(f" Schema TRAINING_POWERBI not found or error: {e}")
        
        print("\n" + "="*80)
        print("STRUCTURE CHECK COMPLETE")
        print("="*80)

if __name__ == "__main__":
    check_snowflake_structure()
