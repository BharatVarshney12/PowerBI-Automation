"""
Generate Sample Excel Data for Testing
Creates an Excel file with multiple sheets containing sample Snowflake data
"""

import pandas as pd
from pathlib import Path
import sys

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from utils.logger import log_info, log_step, log_action, log_data, log_error


def create_sample_excel():
    """Create sample Excel file with test data"""
    
    try:
        log_step("Creating Sample Excel Data")
        
        # --- CUSTOMERS TABLE ---
        log_action("Creating CUSTOMERS data")
        customers_data = {
            "CUSTOMER_ID": [1, 2, 3, 4, 5],
            "FIRST_NAME": ["Amit", "Neha", "Rohit", "Priya", "Anjali"],
            "LAST_NAME": ["Sharma", "Patel", "Kumar", "Singh", "Verma"],
            "EMAIL": [
                "amit.sharma@example.com",
                "neha.patel@example.com",
                "rohit.kumar@example.com",
                "priya.singh@example.com",
                "anjali.verma@example.com"
            ],
            "PHONE": ["9876543210", "9988776655", "9876512345", "9998877665", "9812345678"],
            "CREATED_AT": ["2025-10-29 00:00:00"] * 5
        }

        # --- ORDERS TABLE ---
        log_action("Creating ORDERS data")
        orders_data = {
            "ORDER_ID": [1, 2, 3, 4, 5],
            "CUSTOMER_ID": [1, 2, 3, 4, 5],
            "ORDER_DATE": ["2025-10-10", "2025-10-09", "2025-10-08", "2025-10-07", "2025-10-06"],
            "ORDER_STATUS": ["Completed", "Pending", "Shipped", "Cancelled", "Completed"],
            "TOTAL_AMOUNT": [2500.00, 1500.00, 3200.00, 800.00, 1800.00]
        }

        # --- ORDER_ITEMS TABLE ---
        log_action("Creating ORDER_ITEMS data")
        order_items_data = {
            "ITEM_ID": [1, 2, 3, 4, 5, 6, 7],
            "ORDER_ID": [1, 1, 2, 3, 3, 4, 5],
            "PRODUCT_NAME": ["Laptop Bag", "Mouse", "Keyboard", "Monitor", "HDMI Cable", "USB Cable", "Charger"],
            "QUANTITY": [1, 2, 1, 1, 1, 2, 1],
            "PRICE": [1200.00, 650.00, 1500.00, 3000.00, 200.00, 400.00, 1800.00]
        }

        # --- VALIDATION QUERY RESULT ---
        log_action("Creating VALIDATION_QUERY_RESULT data")
        validation_data = {
            "CUSTOMER_NAME": ["Amit Sharma", "Neha Patel", "Rohit Kumar", "Priya Singh", "Anjali Verma"],
            "ORDER_ID": [1, 2, 3, 4, 5],
            "ORDER_STATUS": ["Completed", "Pending", "Shipped", "Cancelled", "Completed"],
            "CALCULATED_TOTAL": [2500.00, 1500.00, 3200.00, 800.00, 1800.00]
        }

        # --- Convert to DataFrames ---
        log_step("Converting data to DataFrames")
        df_customers = pd.DataFrame(customers_data)
        df_orders = pd.DataFrame(orders_data)
        df_order_items = pd.DataFrame(order_items_data)
        df_validation = pd.DataFrame(validation_data)

        log_data("DataFrame Summary", {
            "CUSTOMERS": f"{len(df_customers)} rows, {len(df_customers.columns)} columns",
            "ORDERS": f"{len(df_orders)} rows, {len(df_orders.columns)} columns",
            "ORDER_ITEMS": f"{len(df_order_items)} rows, {len(df_order_items.columns)} columns",
            "VALIDATION": f"{len(df_validation)} rows, {len(df_validation.columns)} columns"
        })

        # --- Save to Excel ---
        log_step("Saving to Excel file")
        
        # Determine output path
        output_dir = Path(__file__).parent.parent / 'data' / 'downloads'
        output_dir.mkdir(parents=True, exist_ok=True)
        file_path = output_dir / "snowflake_validation_data.xlsx"
        
        log_action("Writing Excel file", str(file_path))
        
        with pd.ExcelWriter(file_path, engine="xlsxwriter") as writer:
            df_customers.to_excel(writer, sheet_name="CUSTOMERS", index=False)
            df_orders.to_excel(writer, sheet_name="ORDERS", index=False)
            df_order_items.to_excel(writer, sheet_name="ORDER_ITEMS", index=False)
            df_validation.to_excel(writer, sheet_name="VALIDATION_QUERY_RESULT", index=False)

        log_info(f" Excel file created successfully: {file_path}")
        log_data("File Details", {
            "Path": str(file_path),
            "Size": f"{file_path.stat().st_size} bytes",
            "Sheets": "CUSTOMERS, ORDERS, ORDER_ITEMS, VALIDATION_QUERY_RESULT"
        })
        
        return str(file_path)
        
    except Exception as e:
        log_error(f"Failed to create Excel file: {str(e)}", exc_info=True)
        raise


if __name__ == "__main__":
    """Run directly to create the Excel file"""
    print("\n" + "="*80)
    print("CREATING SAMPLE EXCEL DATA FOR TESTING")
    print("="*80 + "\n")
    
    file_path = create_sample_excel()
    
    print("\n" + "="*80)
    print(f"SUCCESS! File created at: {file_path}")
    print("="*80 + "\n")
