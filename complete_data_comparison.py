"""
Complete Data Comparison: Snowflake vs Excel
Shows actual values from both sources for all tables
"""
import pandas as pd
import snowflake.connector
from pathlib import Path
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Snowflake connection
SNOWFLAKE_CONFIG = {
    'user': 'BHARATAARETE',
    'password': 'Parthkalka2609@1234',
    'account': 'po54025.central-india.azure',
    'warehouse': 'POWERBI',
    'database': 'POWERBI_LEARNING',
    'schema': 'TRAINING_POWERBI'
}

# Tables to compare
TABLES = {
    'SPEND_BY_CODE': {
        'excel_file': 'power bi actual report/Spend by code.xlsx',
        'description': 'Spend by Code Analysis'
    },
    'SPEND_BY_PRODUCT_TYPE': {
        'excel_file': 'power bi actual report/Spend by product type.xlsx',
        'description': 'Spend by Product Type Analysis'
    },
    'SPEND_BY_BILL_TYPE': {
        'excel_file': 'power bi actual report/Spend by  bill type.xlsx',
        'description': 'Spend by Bill Type Analysis'
    }
}

def connect_snowflake():
    """Create Snowflake connection"""
    return snowflake.connector.connect(**SNOWFLAKE_CONFIG)

def get_snowflake_data(table_name):
    """Get all data from Snowflake table"""
    print(f"\n[SNOWFLAKE] Loading table: {table_name}")
    
    conn = connect_snowflake()
    cursor = conn.cursor()
    
    try:
        query = f"""
        SELECT * 
        FROM {SNOWFLAKE_CONFIG['database']}.{SNOWFLAKE_CONFIG['schema']}.{table_name}
        """
        
        cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
        
        df = pd.DataFrame(rows, columns=columns)
        print(f"   Retrieved {len(df)} rows, {len(df.columns)} columns")
        
        return df
        
    except Exception as e:
        print(f"   Error: {str(e)}")
        return None
        
    finally:
        cursor.close()
        conn.close()

def get_excel_data(excel_file):
    """Get all data from Excel file"""
    print(f"\n[EXCEL] Loading file: {excel_file}")
    
    try:
        excel_path = Path(excel_file)
        
        if not excel_path.exists():
            print(f"   Error: File not found")
            return None
        
        # Read Excel file
        df = pd.read_excel(excel_file, engine='openpyxl', sheet_name=0)
        
        # Clean column names
        df.columns = [str(col).strip() for col in df.columns]
        
        # Remove blank rows
        df = df.dropna(how='all')
        
        # Remove filter rows
        first_col = df.columns[0]
        df = df[~df[first_col].astype(str).str.contains('Applied filters', case=False, na=False)]
        
        df = df.reset_index(drop=True)
        
        print(f"   Retrieved {len(df)} rows, {len(df.columns)} columns")
        
        return df
        
    except Exception as e:
        print(f"   Error: {str(e)}")
        return None

def create_comparison_report():
    """Create comprehensive comparison report"""
    print("="*100)
    print("COMPLETE DATA COMPARISON: SNOWFLAKE vs EXCEL")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*100)
    
    output_dir = Path('validation_reports')
    output_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = output_dir / f'Complete_Data_Comparison_{timestamp}.xlsx'
    
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        
        summary_data = []
        
        for table_name, config in TABLES.items():
            print(f"\n{'='*100}")
            print(f"PROCESSING: {table_name}")
            print(f"{'='*100}")
            
            # Get Snowflake data
            sf_df = get_snowflake_data(table_name)
            
            # Get Excel data
            excel_df = get_excel_data(config['excel_file'])
            
            if sf_df is None or excel_df is None:
                print(f"   Skipping {table_name} due to data load error")
                continue
            
            # Summary
            summary_data.append({
                'Table': table_name,
                'Snowflake_Rows': len(sf_df),
                'Excel_Rows': len(excel_df),
                'Row_Difference': len(sf_df) - len(excel_df),
                'Snowflake_Columns': len(sf_df.columns),
                'Excel_Columns': len(excel_df.columns),
                'Column_Difference': len(sf_df.columns) - len(excel_df.columns)
            })
            
            # Export Snowflake data
            sheet_name = f'{table_name}_Snowflake'[:31]
            sf_df.to_excel(writer, sheet_name=sheet_name, index=False)
            print(f"   Exported Snowflake data to sheet: {sheet_name}")
            
            # Export Excel data
            sheet_name = f'{table_name}_Excel'[:31]
            excel_df.to_excel(writer, sheet_name=sheet_name, index=False)
            print(f"   Exported Excel data to sheet: {sheet_name}")
            
            # Create side-by-side comparison for first 50 rows
            comparison_rows = min(50, len(sf_df), len(excel_df))
            
            if comparison_rows > 0:
                comparison_data = []
                
                # Get common columns (first 5 for readability)
                sf_cols = list(sf_df.columns)[:5]
                excel_cols = list(excel_df.columns)[:5]
                
                for idx in range(comparison_rows):
                    row_data = {'Row': idx + 1}
                    
                    # Add Snowflake values
                    for col in sf_cols:
                        if col in sf_df.columns:
                            row_data[f'SF_{col}'] = sf_df.iloc[idx][col]
                    
                    # Add Excel values
                    for col in excel_cols:
                        if col in excel_df.columns:
                            row_data[f'Excel_{col}'] = excel_df.iloc[idx][col]
                    
                    comparison_data.append(row_data)
                
                comparison_df = pd.DataFrame(comparison_data)
                sheet_name = f'{table_name}_Compare'[:31]
                comparison_df.to_excel(writer, sheet_name=sheet_name, index=False)
                print(f"   Created comparison sheet: {sheet_name}")
        
        # Create summary sheet
        if summary_data:
            summary_df = pd.DataFrame(summary_data)
            summary_df.to_excel(writer, sheet_name='Summary', index=False)
            print(f"\n   Created summary sheet")
    
    print(f"\n{'='*100}")
    print(f"REPORT GENERATED SUCCESSFULLY")
    print(f"{'='*100}")
    print(f"\nFile: {output_file}")
    print(f"\nThis report contains:")
    print(f"  - Summary: Overview of all tables")
    print(f"  - {table_name}_Snowflake: Complete data from Snowflake")
    print(f"  - {table_name}_Excel: Complete data from Excel files")
    print(f"  - {table_name}_Compare: Side-by-side comparison (first 50 rows)")
    print(f"\nYou can now see ACTUAL values from both sources!\n")

if __name__ == "__main__":
    create_comparison_report()
