# Snowflake Configuration
SNOWFLAKE_CONFIG = {
 'account': 'po54025.central-india.azure',
 'user': 'BHARATAARETE',
 'password': 'Parthkalka2609@1234',
 'warehouse': 'COMPUTE_WH',
 'database': 'SNOWFLAKELEARNING',
 'schema': 'TRAINING_SCHEMA',
 'role': 'ACCOUNTADMIN'
}

# Tables available for validation
SNOWFLAKE_TABLES = {
 'customers': 'CUSTOMERS',
 'orders': 'ORDERS',
 'order_items': 'ORDER_ITEMS'
}

# Validation Configuration
VALIDATION_CONFIG = {
 'default_table': 'CUSTOMERS', # Default table for validation
 'table_name': 'CUSTOMERS', # Add table_name key for backward compatibility
 'comparison_rules': {
 'validate_row_count': True,
 'validate_columns': True,
 'validate_data_types': True,
 'validate_nulls': True,
 'validate_duplicates': True,
 'tolerance': 0.01 # 1% tolerance for numeric comparisons
 },
 'generate_report': True,
 'save_results': True
}
