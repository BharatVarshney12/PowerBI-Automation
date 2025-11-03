"""
Detect Data Mismatches between CSV files and Actual Excel Reports
Compares CSV files with Excel reports to detect any value changes
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime

# File mappings
FILE_MAPPINGS = [
    {
        'name': 'SPEND_BY_CODE',
        'csv_file': 'spend by code.csv',
        'excel_file': 'power bi actual report/Spend by code.xlsx'
    },
    {
        'name': 'SPEND_BY_PRODUCT_TYPE',
        'csv_file': 'Spend by product type.csv',
        'excel_file': 'power bi actual report/Spend by product type.xlsx'
    },
    {
        'name': 'SPEND_BY_BILL_TYPE',
        'csv_file': 'Spend by  bill type.csv',
        'excel_file': 'power bi actual report/Spend by  bill type.xlsx'
    }
]

def clean_value(value):
    """Clean and normalize values for comparison"""
    if pd.isna(value) or value is None:
        return None
    
    if isinstance(value, str):
        # Remove currency symbols, commas, percentage signs
        value = value.replace('$', '').replace(',', '').replace('%', '').strip()
        
        # Try to convert to number
        try:
            if '.' in value:
                return float(value)
            else:
                return int(value)
        except (ValueError, AttributeError):
            return value
    
    return value

def load_and_clean_csv(csv_file):
    """Load and clean CSV file"""
    try:
        df = pd.read_csv(csv_file)
        
        # Clean column names
        df.columns = [str(col).strip() for col in df.columns]
        
        # Remove completely blank rows
        df = df.dropna(how='all')
        
        # Remove filter information rows
        if len(df) > 0:
            first_col = df.columns[0]
            df = df[~df[first_col].astype(str).str.contains('Applied filters', case=False, na=False)]
        
        # Reset index
        df = df.reset_index(drop=True)
        
        # Clean all values
        for col in df.columns:
            df[col] = df[col].apply(clean_value)
        
        return df
    except Exception as e:
        print(f"Error loading CSV {csv_file}: {e}")
        return None

def load_and_clean_excel(excel_file):
    """Load and clean Excel file"""
    try:
        df = pd.read_excel(excel_file, engine='openpyxl')
        
        # Clean column names
        df.columns = [str(col).strip() for col in df.columns]
        
        # Remove completely blank rows
        df = df.dropna(how='all')
        
        # Remove filter information rows
        if len(df) > 0:
            first_col = df.columns[0]
            df = df[~df[first_col].astype(str).str.contains('Applied filters', case=False, na=False)]
        
        # Reset index
        df = df.reset_index(drop=True)
        
        # Clean all values
        for col in df.columns:
            df[col] = df[col].apply(clean_value)
        
        return df
    except Exception as e:
        print(f"Error loading Excel {excel_file}: {e}")
        return None

def compare_values(val1, val2):
    """Compare two values considering numeric precision"""
    # Both None/NaN
    if (val1 is None or pd.isna(val1)) and (val2 is None or pd.isna(val2)):
        return True
    
    # One is None/NaN
    if (val1 is None or pd.isna(val1)) or (val2 is None or pd.isna(val2)):
        return False
    
    # Both numeric
    if isinstance(val1, (int, float)) and isinstance(val2, (int, float)):
        return abs(float(val1) - float(val2)) < 0.0001
    
    # String comparison
    return str(val1).strip().lower() == str(val2).strip().lower()

def detect_mismatches():
    """Detect all mismatches between CSV and Excel files"""
    
    print("\n" + "="*100)
    print("CSV vs EXCEL MISMATCH DETECTION")
    print("="*100)
    
    all_mismatches = []
    summary_data = []
    
    for mapping in FILE_MAPPINGS:
        table_name = mapping['name']
        csv_file = mapping['csv_file']
        excel_file = mapping['excel_file']
        
        print(f"\n{'='*100}")
        print(f"PROCESSING: {table_name}")
        print(f"{'='*100}")
        print(f"CSV File: {csv_file}")
        print(f"Excel File: {excel_file}")
        
        # Load files
        print(f"\n📂 Loading files...")
        df_csv = load_and_clean_csv(csv_file)
        df_excel = load_and_clean_excel(excel_file)
        
        if df_csv is None or df_excel is None:
            print(f"❌ Error loading files for {table_name}")
            continue
        
        print(f"   ✅ CSV loaded: {len(df_csv)} rows, {len(df_csv.columns)} columns")
        print(f"   ✅ Excel loaded: {len(df_excel)} rows, {len(df_excel.columns)} columns")
        
        table_mismatches = 0
        
        # Check 1: Row count
        print(f"\n1️⃣ Checking row counts...")
        if len(df_csv) != len(df_excel):
            mismatch = {
                'Table_Name': table_name,
                'Mismatch_Type': 'Row_Count',
                'Excel_Value': len(df_excel),
                'CSV_Value': len(df_csv),
                'Row_Index': 'N/A',
                'Column_Name': 'N/A',
                'Details': f'Row count mismatch: Excel has {len(df_excel)} rows, CSV has {len(df_csv)} rows'
            }
            all_mismatches.append(mismatch)
            table_mismatches += 1
            print(f"   ❌ MISMATCH: Excel={len(df_excel)}, CSV={len(df_csv)}")
        else:
            print(f"   ✅ MATCH: {len(df_csv)} rows")
        
        # Check 2: Column count
        print(f"\n2️⃣ Checking column counts...")
        if len(df_csv.columns) != len(df_excel.columns):
            mismatch = {
                'Table_Name': table_name,
                'Mismatch_Type': 'Column_Count',
                'Excel_Value': len(df_excel.columns),
                'CSV_Value': len(df_csv.columns),
                'Row_Index': 'N/A',
                'Column_Name': 'N/A',
                'Details': f'Column count mismatch: Excel has {len(df_excel.columns)} columns, CSV has {len(df_csv.columns)} columns'
            }
            all_mismatches.append(mismatch)
            table_mismatches += 1
            print(f"   ❌ MISMATCH: Excel={len(df_excel.columns)}, CSV={len(df_csv.columns)}")
        else:
            print(f"   ✅ MATCH: {len(df_csv.columns)} columns")
        
        # Check 3: Column names
        print(f"\n3️⃣ Checking column names...")
        csv_cols = set(df_csv.columns)
        excel_cols = set(df_excel.columns)
        
        missing_in_excel = csv_cols - excel_cols
        missing_in_csv = excel_cols - csv_cols
        
        if missing_in_excel or missing_in_csv:
            details = []
            if missing_in_excel:
                details.append(f"Missing in Excel: {', '.join(missing_in_excel)}")
            if missing_in_csv:
                details.append(f"Missing in CSV: {', '.join(missing_in_csv)}")
            
            mismatch = {
                'Table_Name': table_name,
                'Mismatch_Type': 'Column_Names',
                'Excel_Value': ', '.join(excel_cols),
                'CSV_Value': ', '.join(csv_cols),
                'Row_Index': 'N/A',
                'Column_Name': 'N/A',
                'Details': '; '.join(details)
            }
            all_mismatches.append(mismatch)
            table_mismatches += 1
            print(f"   ❌ MISMATCH: {'; '.join(details)}")
        else:
            print(f"   ✅ MATCH: All column names match")
        
        # Check 4: Cell-by-cell comparison
        print(f"\n4️⃣ Comparing cell values...")
        
        # Only compare if same shape
        if len(df_csv) == len(df_excel) and len(df_csv.columns) == len(df_excel.columns):
            value_mismatches = 0
            
            # Compare each cell
            for row_idx in range(len(df_csv)):
                for col in df_csv.columns:
                    if col in df_excel.columns:
                        csv_val = df_csv.loc[row_idx, col]
                        excel_val = df_excel.loc[row_idx, col]
                        
                        if not compare_values(csv_val, excel_val):
                            mismatch = {
                                'Table_Name': table_name,
                                'Mismatch_Type': 'Data_Value',
                                'Excel_Value': excel_val,
                                'CSV_Value': csv_val,
                                'Row_Index': row_idx,
                                'Column_Name': col,
                                'Details': f'Value mismatch at row {row_idx}, column "{col}": Excel="{excel_val}", CSV="{csv_val}"'
                            }
                            all_mismatches.append(mismatch)
                            value_mismatches += 1
                            table_mismatches += 1
            
            if value_mismatches == 0:
                print(f"   ✅ MATCH: All cell values match ({len(df_csv) * len(df_csv.columns)} cells checked)")
            else:
                print(f"   ❌ MISMATCH: {value_mismatches} cells have different values")
        else:
            print(f"   ⚠️  SKIPPED: Cannot compare values due to shape mismatch")
        
        # Summary for this table
        status = "✅ PASS" if table_mismatches == 0 else f"❌ FAIL ({table_mismatches} mismatches)"
        summary_data.append({
            'Table_Name': table_name,
            'Total_Mismatches': table_mismatches,
            'Status': status
        })
        
        print(f"\n{'='*100}")
        print(f"TABLE SUMMARY: {table_name} - {status}")
        print(f"{'='*100}")
    
    # Generate report
    print(f"\n{'='*100}")
    print(f"GENERATING EXCEL REPORT")
    print(f"{'='*100}")
    
    output_dir = Path('validation_reports')
    output_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = output_dir / f'Data_Mismatches_{timestamp}.xlsx'
    
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        # All mismatches in one tab
        if all_mismatches:
            df_mismatches = pd.DataFrame(all_mismatches)
            df_mismatches.to_excel(writer, sheet_name='All_Mismatches', index=False)
            print(f"   ✅ All_Mismatches sheet created with {len(all_mismatches)} mismatches")
        else:
            # Create empty sheet with message
            df_empty = pd.DataFrame([{
                'Message': 'No mismatches found! All CSV files match Excel reports perfectly.',
                'Total_Files_Checked': len(FILE_MAPPINGS),
                'Check_Date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }])
            df_empty.to_excel(writer, sheet_name='All_Mismatches', index=False)
            print(f"   ✅ No mismatches found!")
        
        # Summary sheet
        df_summary = pd.DataFrame(summary_data)
        df_summary.to_excel(writer, sheet_name='Summary', index=False)
        print(f"   ✅ Summary sheet created")
    
    print(f"\n{'='*100}")
    print(f"✅ REPORT GENERATED SUCCESSFULLY")
    print(f"{'='*100}")
    print(f"\n📁 File saved: {output_file}")
    print(f"\n📊 Results:")
    print(f"   • Total mismatches found: {len(all_mismatches)}")
    print(f"   • Tables checked: {len(FILE_MAPPINGS)}")
    
    for summary in summary_data:
        print(f"   • {summary['Table_Name']}: {summary['Status']}")
    
    print(f"\n{'='*100}\n")

if __name__ == "__main__":
    detect_mismatches()
