# Sample Data Generator

## Overview
This utility creates sample Excel data for testing the PowerBI automation and Snowflake validation workflows.

## What It Does

Creates an Excel file (`snowflake_validation_data.xlsx`) with 4 sheets:

### 1. CUSTOMERS Sheet
- **Columns**: CUSTOMER_ID, FIRST_NAME, LAST_NAME, EMAIL, PHONE, CREATED_AT
- **Rows**: 5 customer records
- Sample data includes Indian names and contact information

### 2. ORDERS Sheet
- **Columns**: ORDER_ID, CUSTOMER_ID, ORDER_DATE, ORDER_STATUS, TOTAL_AMOUNT
- **Rows**: 5 order records
- Statuses: Completed, Pending, Shipped, Cancelled
- Amounts ranging from ₹800 to ₹3,200

### 3. ORDER_ITEMS Sheet
- **Columns**: ITEM_ID, ORDER_ID, PRODUCT_NAME, QUANTITY, PRICE
- **Rows**: 7 order items
- Products: Laptop Bag, Mouse, Keyboard, Monitor, HDMI Cable, USB Cable, Charger

### 4. VALIDATION_QUERY_RESULT Sheet
- **Columns**: CUSTOMER_NAME, ORDER_ID, ORDER_STATUS, CALCULATED_TOTAL
- **Rows**: 5 validation records
- Represents SQL query results for validation testing

## Usage

### Method 1: Run the Script Directly
```bash
python utils/create_sample_data.py
```

### Method 2: Use VS Code Task
1. Press `Ctrl+Shift+P`
2. Type "Tasks: Run Task"
3. Select "Create Sample Excel Data"

### Method 3: Import as Module
```python
from utils.create_sample_data import create_sample_excel

file_path = create_sample_excel()
print(f"File created at: {file_path}")
```

## Output

**File Location**: `data/downloads/snowflake_validation_data.xlsx`

**File Size**: ~8 KB

**Sheets**:
- CUSTOMERS (5 rows × 6 columns)
- ORDERS (5 rows × 5 columns)  
- ORDER_ITEMS (7 rows × 5 columns)
- VALIDATION_QUERY_RESULT (5 rows × 4 columns)

## Logging

The script uses the PowerBI automation logger to track:
- Each step of data creation
- DataFrame summaries
- File creation details
- Any errors that occur

Logs are saved to: `logs/powerbi_automation_YYYYMMDD_HHMMSS.log`

## Use Cases

1. **Testing PowerBI Export**: Use as reference data to compare against PowerBI exports
2. **Snowflake Validation**: Compare with actual Snowflake database data
3. **Data Profiling**: Test data profiling tools (Sweetviz, YData)
4. **Schema Validation**: Verify column names and data types
5. **Sample Data**: Demo data for presentations or training

## Requirements

- pandas
- xlsxwriter (automatically installed)

## Features

✅ Comprehensive logging  
✅ Error handling  
✅ Auto-creates directories  
✅ Standardized output location  
✅ VS Code task integration  
✅ Reusable as module  

## Example Output

```
================================================================================
CREATING SAMPLE EXCEL DATA FOR TESTING
================================================================================

20:18:08 | INFO     | STEP: Creating Sample Excel Data
20:18:08 | INFO     | ACTION: Creating CUSTOMERS data
20:18:08 | INFO     | ACTION: Creating ORDERS data
20:18:08 | INFO     | ACTION: Creating ORDER_ITEMS data
20:18:08 | INFO     | ACTION: Creating VALIDATION_QUERY_RESULT data
20:18:08 | INFO     | STEP: Converting data to DataFrames
20:18:08 | INFO     | DATA: DataFrame Summary
20:18:08 | INFO     |   - CUSTOMERS: 5 rows, 6 columns
20:18:08 | INFO     |   - ORDERS: 5 rows, 5 columns
20:18:08 | INFO     |   - ORDER_ITEMS: 7 rows, 5 columns
20:18:08 | INFO     |   - VALIDATION: 5 rows, 4 columns
20:18:08 | INFO     | STEP: Saving to Excel file
20:18:08 | INFO     | ✅ Excel file created successfully
20:18:08 | INFO     | DATA: File Details
20:18:08 | INFO     |   - Path: C:\...\data\downloads\snowflake_validation_data.xlsx
20:18:08 | INFO     |   - Size: 7957 bytes
20:18:08 | INFO     |   - Sheets: CUSTOMERS, ORDERS, ORDER_ITEMS, VALIDATION_QUERY_RESULT

================================================================================
SUCCESS! File created at: C:\...\data\downloads\snowflake_validation_data.xlsx
================================================================================
```

## Data Schema

### CUSTOMERS
```
CUSTOMER_ID (int) | FIRST_NAME (str) | LAST_NAME (str) | EMAIL (str) | PHONE (str) | CREATED_AT (str)
```

### ORDERS
```
ORDER_ID (int) | CUSTOMER_ID (int) | ORDER_DATE (str) | ORDER_STATUS (str) | TOTAL_AMOUNT (float)
```

### ORDER_ITEMS
```
ITEM_ID (int) | ORDER_ID (int) | PRODUCT_NAME (str) | QUANTITY (int) | PRICE (float)
```

### VALIDATION_QUERY_RESULT
```
CUSTOMER_NAME (str) | ORDER_ID (int) | ORDER_STATUS (str) | CALCULATED_TOTAL (float)
```
