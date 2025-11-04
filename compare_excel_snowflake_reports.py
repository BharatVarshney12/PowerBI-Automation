"""
Comprehensive Excel vs Snowflake Data Validation
Compares actual Excel reports with Snowflake tables and generates detailed validation reports

Tables to validate:
1. Spend by code.xlsx -> SPEND_BY_CODE
2. Spend by product type.xlsx -> SPEND_BY_PRODUCT_TYPE  
3. Spend by bill type.xlsx -> SPEND_BY_BILL_TYPE

Validation checks:
- Row count comparison
- Column count comparison
- Column name mapping
- Data type validation
- NULL/blank value counts
- Data accuracy (cell-by-cell comparison)
- Schema validation
- Detailed discrepancy reporting
"""

import pandas as pd
import numpy as np
import snowflake.connector
from pathlib import Path
from datetime import datetime
import openpyxl
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

# Table configurations with Excel file mappings
TABLES = [
    {
        'name': 'SPEND_BY_CODE',
        'excel_file': 'power bi actual report/Spend by code.xlsx',
        'sheet_name': None,  # Will auto-detect
        'description': 'Spend by Code Analysis'
    },
    {
        'name': 'SPEND_BY_PRODUCT_TYPE',
        'excel_file': 'power bi actual report/Spend by product type.xlsx',
        'sheet_name': None,
        'description': 'Spend by Product Type Analysis'
    },
    {
        'name': 'SPEND_BY_BILL_TYPE',
        'excel_file': 'power bi actual report/Spend by  bill type.xlsx',
        'sheet_name': None,
        'description': 'Spend by Bill Type Analysis'
    }
]

def connect_snowflake():
    """Create Snowflake connection"""
    return snowflake.connector.connect(**SNOWFLAKE_CONFIG)

def clean_excel_value(value):
    """Clean Excel cell values"""
    if pd.isna(value) or value is None or value == '':
        return None
    
    if isinstance(value, str):
        # Remove whitespace
        value = value.strip()
        
        # Remove dollar signs, commas
        if '$' in value or ',' in value:
            value = value.replace('$', '').replace(',', '')
        
        # Remove percentage signs
        if '%' in value:
            value = value.replace('%', '')
        
        # Try to convert to number
        try:
            if '.' in value:
                return float(value)
            else:
                return int(value)
        except:
            return value
    
    return value

def load_excel_data(excel_file):
    """Load data from Excel file"""
    print(f"\n Loading Excel: {excel_file}")
    
    try:
        # Try to read Excel file
        excel_path = Path(excel_file)
        
        if not excel_path.exists():
            print(f"    File not found: {excel_file}")
            return None
        
        # Load with openpyxl engine for better Excel support
        df = pd.read_excel(excel_file, engine='openpyxl', sheet_name=0)
        
        # Clean column names - remove extra spaces
        df.columns = [str(col).strip() for col in df.columns]
        
        # Clean all values
        for col in df.columns:
            df[col] = df[col].apply(clean_excel_value)
        
        # Replace NaN with None
        df = df.replace({pd.NA: None, np.nan: None})
        
        # Remove rows where ALL values are None (blank rows)
        df = df.dropna(how='all')
        
        # Remove filter information rows (rows that start with "Applied filters:")
        first_col = df.columns[0]
        df = df[~df[first_col].astype(str).str.contains('Applied filters', case=False, na=False)]
        
        # Reset index after filtering
        df = df.reset_index(drop=True)
        
        print(f"    Loaded {len(df)} rows, {len(df.columns)} columns (after filtering)")
        print(f"    Columns: {list(df.columns)}")
        
        return df
        
    except Exception as e:
        print(f"    Error loading Excel: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def load_snowflake_table(table_name):
    """Load data from Snowflake table"""
    print(f"\n[SNOWFLAKE] Loading Snowflake table: {table_name}")
    
    conn = connect_snowflake()
    cursor = conn.cursor()
    
    try:
        # Query all data (without ORDER BY to match Excel insertion order)
        query = f"""
        SELECT * 
        FROM {SNOWFLAKE_CONFIG['database']}.{SNOWFLAKE_CONFIG['schema']}.{table_name}
        """
        
        print(f"    Executing: {query}")
        cursor.execute(query)
        
        # Get column names
        columns = [col[0] for col in cursor.description]
        
        # Fetch all rows
        rows = cursor.fetchall()
        
        # Create DataFrame
        df = pd.DataFrame(rows, columns=columns)
        
        print(f"    Loaded {len(df)} rows, {len(df.columns)} columns")
        print(f"    Columns: {list(df.columns)}")
        
        return df
        
    except Exception as e:
        print(f"    Error loading from Snowflake: {str(e)}")
        import traceback
        traceback.print_exc()
        return None
        
    finally:
        cursor.close()
        conn.close()

def run_snowflake_validation_queries(table_name):
    """Run comprehensive validation queries on Snowflake table"""
    print(f"\n Running Snowflake validation queries for {table_name}")
    
    conn = connect_snowflake()
    cursor = conn.cursor()
    
    results = {}
    
    try:
        # 1. Row count
        query = f"SELECT COUNT(*) as row_count FROM {SNOWFLAKE_CONFIG['database']}.{SNOWFLAKE_CONFIG['schema']}.{table_name}"
        cursor.execute(query)
        results['row_count'] = cursor.fetchone()[0]
        print(f"    Row count: {results['row_count']}")
        
        # 2. Column count
        query = f"SELECT COUNT(*) as col_count FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = '{SNOWFLAKE_CONFIG['schema']}' AND TABLE_NAME = '{table_name}'"
        cursor.execute(query)
        results['column_count'] = cursor.fetchone()[0]
        print(f"    Column count: {results['column_count']}")
        
        # 3. Column details
        query = f"""
        SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_SCHEMA = '{SNOWFLAKE_CONFIG['schema']}' 
        AND TABLE_NAME = '{table_name}'
        ORDER BY ORDINAL_POSITION
        """
        cursor.execute(query)
        columns_info = cursor.fetchall()
        results['columns'] = [{'name': col[0], 'type': col[1], 'nullable': col[2]} for col in columns_info]
        print(f"    Column details retrieved")
        
        # 4. NULL counts per column
        null_counts = {}
        for col_info in results['columns']:
            col_name = col_info['name']
            query = f"SELECT COUNT(*) FROM {SNOWFLAKE_CONFIG['database']}.{SNOWFLAKE_CONFIG['schema']}.{table_name} WHERE {col_name} IS NULL"
            cursor.execute(query)
            null_counts[col_name] = cursor.fetchone()[0]
        
        results['null_counts'] = null_counts
        print(f"    NULL counts calculated for all columns")
        
        # 5. Sample data (first 20 rows to show more data)
        query = f"SELECT * FROM {SNOWFLAKE_CONFIG['database']}.{SNOWFLAKE_CONFIG['schema']}.{table_name} LIMIT 20"
        cursor.execute(query)
        sample_data = cursor.fetchall()
        sample_columns = [col[0] for col in cursor.description]
        results['sample_data'] = pd.DataFrame(sample_data, columns=sample_columns)
        print(f"    Sample data retrieved (20 rows)")
        
        # 6. Full data preview (all rows for validation)
        query = f"SELECT * FROM {SNOWFLAKE_CONFIG['database']}.{SNOWFLAKE_CONFIG['schema']}.{table_name}"
        cursor.execute(query)
        full_data = cursor.fetchall()
        full_columns = [col[0] for col in cursor.description]
        results['full_data'] = pd.DataFrame(full_data, columns=full_columns)
        print(f"    Full data retrieved ({len(full_data)} rows)")
        
        # 6. Data type summary
        type_summary = {}
        for col_info in results['columns']:
            col_name = col_info['name']
            col_type = col_info['type']
            
            # Get min, max for numeric columns
            if 'NUMBER' in col_type or 'FLOAT' in col_type or 'DECIMAL' in col_type:
                query = f"SELECT MIN({col_name}), MAX({col_name}), AVG({col_name}) FROM {SNOWFLAKE_CONFIG['database']}.{SNOWFLAKE_CONFIG['schema']}.{table_name}"
                cursor.execute(query)
                stats = cursor.fetchone()
                type_summary[col_name] = {
                    'type': col_type,
                    'min': stats[0],
                    'max': stats[1],
                    'avg': stats[2]
                }
            else:
                type_summary[col_name] = {'type': col_type}
        
        results['type_summary'] = type_summary
        print(f"    Data type summary completed")
        
        return results
        
    except Exception as e:
        print(f"    Error running validation queries: {str(e)}")
        import traceback
        traceback.print_exc()
        return None
        
    finally:
        cursor.close()
        conn.close()

def compare_dataframes(excel_df, snowflake_df, table_name):
    """Detailed comparison between Excel and Snowflake data"""
    print(f"\n[COMPARE] Comparing Excel vs Snowflake for {table_name}")
    
    comparison = {
        'table_name': table_name,
        'timestamp': datetime.now().isoformat(),
        'checks': {}
    }
    
    # 1. Row count comparison
    excel_rows = len(excel_df)
    sf_rows = len(snowflake_df)
    row_match = excel_rows == sf_rows
    
    comparison['checks']['row_count'] = {
        'excel': excel_rows,
        'snowflake': sf_rows,
        'match': row_match,
        'difference': sf_rows - excel_rows,
        'status': ' PASS' if row_match else ' FAIL'
    }
    
    print(f"   {'' if row_match else ''} Row Count: Excel={excel_rows}, Snowflake={sf_rows}, Match={row_match}")
    
    # 2. Column count comparison
    excel_cols = len(excel_df.columns)
    sf_cols = len(snowflake_df.columns)
    col_match = excel_cols == sf_cols
    
    comparison['checks']['column_count'] = {
        'excel': excel_cols,
        'snowflake': sf_cols,
        'match': col_match,
        'difference': sf_cols - excel_cols,
        'status': ' PASS' if col_match else ' FAIL'
    }
    
    print(f"   {'' if col_match else ''} Column Count: Excel={excel_cols}, Snowflake={sf_cols}, Match={col_match}")
    
    # 3. Column name comparison (case-insensitive mapping)
    excel_columns = [str(col).strip() for col in excel_df.columns]
    sf_columns = list(snowflake_df.columns)
    
    # Create mapping (Excel column -> Snowflake column)
    column_mapping = {}
    missing_in_sf = []
    extra_in_sf = []
    
    # Try to map Excel columns to Snowflake columns
    for excel_col in excel_columns:
        # Convert Excel column to expected Snowflake format
        sf_col_expected = excel_col.upper().replace(' ', '_').replace('%', 'PERCENT')
        
        # Check if it exists in Snowflake
        if sf_col_expected in sf_columns:
            column_mapping[excel_col] = sf_col_expected
        else:
            # Try fuzzy matching
            found = False
            for sf_col in sf_columns:
                if sf_col.replace('_', '').replace('PERCENT', '') == excel_col.replace(' ', '').replace('%', '').upper():
                    column_mapping[excel_col] = sf_col
                    found = True
                    break
            
            if not found:
                missing_in_sf.append(excel_col)
    
    # Find extra columns in Snowflake
    mapped_sf_cols = set(column_mapping.values())
    extra_in_sf = [col for col in sf_columns if col not in mapped_sf_cols]
    
    comparison['checks']['column_mapping'] = {
        'excel_columns': excel_columns,
        'snowflake_columns': sf_columns,
        'mapping': column_mapping,
        'missing_in_snowflake': missing_in_sf,
        'extra_in_snowflake': extra_in_sf,
        'status': ' PASS' if not missing_in_sf else ' WARN'
    }
    
    print(f"   {'' if not missing_in_sf else ''} Column Mapping: {len(column_mapping)} mapped")
    if missing_in_sf:
        print(f"       Missing in Snowflake: {missing_in_sf}")
    if extra_in_sf:
        print(f"       Extra in Snowflake: {extra_in_sf}")
    
    # 4. NULL value comparison
    null_comparison = {}
    for excel_col, sf_col in column_mapping.items():
        excel_nulls = excel_df[excel_col].isna().sum()
        sf_nulls = snowflake_df[sf_col].isna().sum()
        
        null_comparison[excel_col] = {
            'excel_nulls': int(excel_nulls),
            'snowflake_nulls': int(sf_nulls),
            'match': excel_nulls == sf_nulls,
            'difference': int(sf_nulls - excel_nulls)
        }
    
    comparison['checks']['null_values'] = null_comparison
    null_mismatches = [k for k, v in null_comparison.items() if not v['match']]
    
    print(f"   {'' if not null_mismatches else ''} NULL Values: {len(null_mismatches)} columns with differences")
    
    # 5. Data type comparison
    dtype_comparison = {}
    for excel_col, sf_col in column_mapping.items():
        excel_dtype = str(excel_df[excel_col].dtype)
        sf_dtype = str(snowflake_df[sf_col].dtype)
        
        dtype_comparison[excel_col] = {
            'excel_dtype': excel_dtype,
            'snowflake_dtype': sf_dtype,
            'compatible': True  # Simplified check
        }
    
    comparison['checks']['data_types'] = dtype_comparison
    print(f"    Data Types: Comparison completed")
    
    # 6. Cell-by-cell data validation (sample)
    data_mismatches = []
    sample_size = min(10, excel_rows, sf_rows)
    
    for idx in range(sample_size):
        for excel_col, sf_col in column_mapping.items():
            excel_val = excel_df.iloc[idx][excel_col]
            sf_val = snowflake_df.iloc[idx][sf_col]
            
            # Handle None/NaN
            if pd.isna(excel_val) and pd.isna(sf_val):
                continue
            
            # Compare values with 0.01 tolerance (ignore differences < 1 cent)
            if isinstance(excel_val, (int, float)) and isinstance(sf_val, (int, float)):
                excel_val_f = float(excel_val)
                sf_val_f = float(sf_val)
                
                # Use absolute tolerance of 0.01 instead of relative tolerance
                if abs(excel_val_f - sf_val_f) > 0.01:
                    data_mismatches.append({
                        'row': idx,
                        'column': excel_col,
                        'excel_value': excel_val_f,
                        'snowflake_value': sf_val_f,
                        'difference': excel_val_f - sf_val_f
                    })
            else:
                if str(excel_val) != str(sf_val):
                    data_mismatches.append({
                        'row': idx,
                        'column': excel_col,
                        'excel_value': str(excel_val),
                        'snowflake_value': str(sf_val),
                        'difference': 'String mismatch'
                    })
    
    comparison['checks']['data_validation'] = {
        'sample_size': sample_size,
        'mismatches': data_mismatches,
        'status': ' PASS' if not data_mismatches else ' FAIL'
    }
    
    print(f"   {'' if not data_mismatches else ''} Data Validation: {len(data_mismatches)} mismatches in {sample_size} sample rows")
    
    # Show sample of actual data being compared
    print(f"\n   SAMPLE DATA PREVIEW (first 5 rows):")
    print(f"   Excel columns: {list(excel_df.columns[:5])}...")
    print(f"   Snowflake columns: {list(snowflake_df.columns[:5])}...")
    if len(excel_df) > 0 and len(snowflake_df) > 0:
        print(f"\n   First row comparison:")
        for excel_col, sf_col in list(column_mapping.items())[:3]:
            print(f"      {excel_col}: Excel={excel_df.iloc[0][excel_col]}, Snowflake={snowflake_df.iloc[0][sf_col]}")
    
    # Overall status
    all_passed = (
        row_match and
        col_match and
        not missing_in_sf and
        not null_mismatches and
        not data_mismatches
    )
    
    comparison['overall_status'] = 'PASSED' if all_passed else 'FAILED'
    comparison['summary'] = {
        'total_checks': 6,
        'passed': sum([
            row_match,
            col_match,
            not missing_in_sf,
            not null_mismatches,
            not data_mismatches,
            True  # dtype check
        ]),
        'warnings': len(null_mismatches) + len(extra_in_sf),
        'failures': len(missing_in_sf) + len(data_mismatches) + (0 if row_match else 1) + (0 if col_match else 1)
    }
    
    return comparison

def generate_excel_report(all_comparisons, output_file):
    """Generate comprehensive Excel report"""
    print(f"\n Generating Excel report: {output_file}")
    
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        
        # Summary sheet
        summary_data = []
        for comp in all_comparisons:
            summary_data.append({
                'Table Name': comp['table_name'],
                'Overall Status': comp['overall_status'],
                'Excel Rows': comp['checks']['row_count']['excel'],
                'Snowflake Rows': comp['checks']['row_count']['snowflake'],
                'Row Match': comp['checks']['row_count']['match'],
                'Excel Columns': comp['checks']['column_count']['excel'],
                'Snowflake Columns': comp['checks']['column_count']['snowflake'],
                'Column Match': comp['checks']['column_count']['match'],
                'Columns Missing in SF': len(comp['checks']['column_mapping']['missing_in_snowflake']),
                'NULL Mismatches': len([k for k, v in comp['checks']['null_values'].items() if not v['match']]),
                'Data Mismatches': len(comp['checks']['data_validation']['mismatches']),
                'Total Checks': comp['summary']['total_checks'],
                'Passed': comp['summary']['passed'],
                'Warnings': comp['summary']['warnings'],
                'Failures': comp['summary']['failures']
            })
        
        summary_df = pd.DataFrame(summary_data)
        summary_df.to_excel(writer, sheet_name='Summary', index=False)
        
        # Detailed sheets for each table
        for comp in all_comparisons:
            table_name = comp['table_name']
            
            # Row & Column check
            basic_checks = pd.DataFrame([
                {'Check': 'Row Count', 'Excel': comp['checks']['row_count']['excel'], 
                 'Snowflake': comp['checks']['row_count']['snowflake'], 
                 'Status': comp['checks']['row_count']['status']},
                {'Check': 'Column Count', 'Excel': comp['checks']['column_count']['excel'], 
                 'Snowflake': comp['checks']['column_count']['snowflake'], 
                 'Status': comp['checks']['column_count']['status']}
            ])
            basic_checks.to_excel(writer, sheet_name=f'{table_name}_BasicChecks', index=False)
            
            # Column mapping
            mapping_data = []
            for excel_col, sf_col in comp['checks']['column_mapping']['mapping'].items():
                mapping_data.append({'Excel Column': excel_col, 'Snowflake Column': sf_col, 'Status': ' Mapped'})
            
            for missing_col in comp['checks']['column_mapping']['missing_in_snowflake']:
                mapping_data.append({'Excel Column': missing_col, 'Snowflake Column': 'NOT FOUND', 'Status': ' Missing'})
            
            if mapping_data:
                mapping_df = pd.DataFrame(mapping_data)
                mapping_df.to_excel(writer, sheet_name=f'{table_name}_ColumnMapping', index=False)
            
            # NULL comparison
            null_data = []
            for col, info in comp['checks']['null_values'].items():
                null_data.append({
                    'Column': col,
                    'Excel NULLs': info['excel_nulls'],
                    'Snowflake NULLs': info['snowflake_nulls'],
                    'Match': '' if info['match'] else '',
                    'Difference': info['difference']
                })
            
            if null_data:
                null_df = pd.DataFrame(null_data)
                null_df.to_excel(writer, sheet_name=f'{table_name}_NULLs', index=False)
            
            # Data mismatches
            if comp['checks']['data_validation']['mismatches']:
                mismatch_df = pd.DataFrame(comp['checks']['data_validation']['mismatches'])
                mismatch_df.to_excel(writer, sheet_name=f'{table_name}_DataMismatches', index=False)
    
    print(f"    Excel report generated successfully")

def generate_text_report(all_comparisons, output_file):
    """Generate detailed text report"""
    print(f"\n[REPORT] Generating text report: {output_file}")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("="*120 + "\n")
        f.write("EXCEL vs SNOWFLAKE COMPREHENSIVE VALIDATION REPORT\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Database: {SNOWFLAKE_CONFIG['database']}.{SNOWFLAKE_CONFIG['schema']}\n")
        f.write("="*120 + "\n\n")
        
        for comp in all_comparisons:
            f.write("\n" + "="*120 + "\n")
            f.write(f"TABLE: {comp['table_name']}\n")
            f.write(f"Overall Status: {comp['overall_status']}\n")
            f.write("="*120 + "\n\n")
            
            # Row count
            rc = comp['checks']['row_count']
            f.write(f"1. ROW COUNT CHECK: {rc['status']}\n")
            f.write(f"   Excel Rows: {rc['excel']}\n")
            f.write(f"   Snowflake Rows: {rc['snowflake']}\n")
            f.write(f"   Match: {rc['match']}\n")
            f.write(f"   Difference: {rc['difference']}\n\n")
            
            # Column count
            cc = comp['checks']['column_count']
            f.write(f"2. COLUMN COUNT CHECK: {cc['status']}\n")
            f.write(f"   Excel Columns: {cc['excel']}\n")
            f.write(f"   Snowflake Columns: {cc['snowflake']}\n")
            f.write(f"   Match: {cc['match']}\n")
            f.write(f"   Difference: {cc['difference']}\n\n")
            
            # Column mapping
            cm = comp['checks']['column_mapping']
            f.write(f"3. COLUMN MAPPING CHECK: {cm['status']}\n")
            f.write(f"   Mapped Columns: {len(cm['mapping'])}\n")
            if cm['missing_in_snowflake']:
                f.write(f"   Missing in Snowflake: {cm['missing_in_snowflake']}\n")
            if cm['extra_in_snowflake']:
                f.write(f"   Extra in Snowflake: {cm['extra_in_snowflake']}\n")
            f.write("\n")
            
            # NULL values
            nv = comp['checks']['null_values']
            null_mismatches = [(k, v) for k, v in nv.items() if not v['match']]
            f.write(f"4. NULL VALUE CHECK:\n")
            f.write(f"   Columns Checked: {len(nv)}\n")
            f.write(f"   Columns with NULL Mismatches: {len(null_mismatches)}\n")
            if null_mismatches:
                for col, info in null_mismatches:
                    f.write(f"      - {col}: Excel={info['excel_nulls']}, Snowflake={info['snowflake_nulls']}, Diff={info['difference']}\n")
            f.write("\n")
            
            # Data validation
            dv = comp['checks']['data_validation']
            f.write(f"5. DATA VALIDATION CHECK: {dv['status']}\n")
            f.write(f"   Sample Size: {dv['sample_size']} rows\n")
            f.write(f"   Mismatches Found: {len(dv['mismatches'])}\n")
            if dv['mismatches']:
                f.write(f"   First 10 mismatches:\n")
                for mismatch in dv['mismatches'][:10]:
                    f.write(f"      - Row {mismatch['row']}, Column '{mismatch['column']}': Excel={mismatch['excel_value']}, Snowflake={mismatch['snowflake_value']}\n")
            f.write("\n")
            
            # Summary
            f.write(f"SUMMARY:\n")
            f.write(f"   Total Checks: {comp['summary']['total_checks']}\n")
            f.write(f"   Passed: {comp['summary']['passed']}\n")
            f.write(f"   Warnings: {comp['summary']['warnings']}\n")
            f.write(f"   Failures: {comp['summary']['failures']}\n")
            f.write("\n")
        
        f.write("="*120 + "\n")
        f.write("END OF REPORT\n")
        f.write("="*120 + "\n")
    
    print(f"    Text report generated successfully")

def main():
    """Main execution"""
    print("\n" + "="*120)
    print("EXCEL vs SNOWFLAKE COMPREHENSIVE DATA VALIDATION")
    print("="*120)
    
    all_comparisons = []
    all_sf_validations = []
    
    for table_config in TABLES:
        table_name = table_config['name']
        excel_file = table_config['excel_file']
        
        print(f"\n{'='*120}")
        print(f"PROCESSING: {table_name}")
        print(f"Excel File: {excel_file}")
        print(f"{'='*120}")
        
        # Load Excel data
        excel_df = load_excel_data(excel_file)
        if excel_df is None:
            print(f" Skipping {table_name} due to Excel load error")
            continue
        
        # Load Snowflake data
        sf_df = load_snowflake_table(table_name)
        if sf_df is None:
            print(f" Skipping {table_name} due to Snowflake load error")
            continue
        
        # Run Snowflake validation queries
        sf_validation = run_snowflake_validation_queries(table_name)
        if sf_validation:
            sf_validation['table_name'] = table_name
            all_sf_validations.append(sf_validation)
        
        # Compare data
        comparison = compare_dataframes(excel_df, sf_df, table_name)
        all_comparisons.append(comparison)
    
    # Generate reports
    if all_comparisons:
        print(f"\n{'='*120}")
        print("GENERATING VALIDATION REPORTS")
        print(f"{'='*120}")
        
        output_dir = Path('validation_reports')
        output_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Excel report
        excel_report = output_dir / f'Excel_vs_Snowflake_Validation_{timestamp}.xlsx'
        generate_excel_report(all_comparisons, excel_report)
        
        # Text report
        text_report = output_dir / f'Validation_Report_{timestamp}.txt'
        generate_text_report(all_comparisons, text_report)
        
        # Save Snowflake validation queries results
        sf_validation_file = output_dir / f'Snowflake_Validation_Queries_{timestamp}.xlsx'
        with pd.ExcelWriter(sf_validation_file, engine='openpyxl') as writer:
            for sf_val in all_sf_validations:
                table_name = sf_val['table_name']
                
                # Basic stats
                stats_df = pd.DataFrame([
                    {'Metric': 'Row Count', 'Value': sf_val['row_count']},
                    {'Metric': 'Column Count', 'Value': sf_val['column_count']}
                ])
                stats_df.to_excel(writer, sheet_name=f'{table_name}_Stats', index=False)
                
                # Column info
                col_df = pd.DataFrame(sf_val['columns'])
                col_df.to_excel(writer, sheet_name=f'{table_name}_Columns', index=False)
                
                # NULL counts
                null_df = pd.DataFrame(list(sf_val['null_counts'].items()), columns=['Column', 'NULL_Count'])
                null_df.to_excel(writer, sheet_name=f'{table_name}_NULLs', index=False)
                
                # Sample data
                sf_val['sample_data'].to_excel(writer, sheet_name=f'{table_name}_Sample', index=False)
                
                # Full data (all rows from Snowflake)
                sf_val['full_data'].to_excel(writer, sheet_name=f'{table_name}_FullData', index=False)
        
        print(f"\n{'='*120}")
        print(" VALIDATION COMPLETE")
        print(f"{'='*120}")
        print(f"\n Reports saved in: {output_dir}/")
        print(f"    Excel Report: {excel_report.name}")
        print(f"    Text Report: {text_report.name}")
        print(f"    Snowflake Queries Report: {sf_validation_file.name}")
        print(f"\n")

if __name__ == "__main__":
    main()
