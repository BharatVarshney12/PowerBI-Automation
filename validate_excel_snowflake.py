"""
Excel vs Snowflake Data Validation Script
Compares three CSV files with their corresponding Snowflake tables:
1. SPEND_BY_CODE
2. SPEND_BY_PRODUCT_TYPE
3. SPEND_BY_BILL_TYPE

Validation checks:
- Row count match
- Column count match
- Column names match
- Data types comparison
- Null value counts
- Data validation (sample records)
- Header checks
- Detailed discrepancy reporting
"""

import pandas as pd
import numpy as np
import snowflake.connector
from pathlib import Path
from datetime import datetime
import json

# Snowflake connection parameters
SNOWFLAKE_CONFIG = {
    'user': 'bvarshney',
    'password': 'Bharat@12345',
    'account': 'gfb73272.ca-central-1.aws',
    'warehouse': 'PowerBI',
    'database': 'PowerBI_learning',
    'schema': 'TRAINING_POWERBI'
}

# Table configurations
TABLES_CONFIG = [
    {
        'csv_file': 'data/spend by code.csv',
        'table_name': 'SPEND_BY_CODE',
        'column_mapping': {
            'Claim Form Type': 'CLAIM_FORM_TYPE',
            'Bill Type Code': 'BILL_TYPE_CODE',
            'PMPM Prior Year': 'PMPM_PREV_YEAR',
            'PMPM': 'PMPM',
            'PMPM YOY%': 'PMPM_YOY_PERCENT',
            'Total Paid Prior Year': 'TOTAL_PAID_PREV_YEAR',
            'Total Paid': 'TOTAL_PAID',
            'Total Paid YOY%': 'TOTAL_PAID_YOY_PERCENT',
            'Cost per Claim Prior Year': 'COST_PER_CLAIM_PREV_YEAR',
            'Cost per Claim': 'COST_PER_CLAIM'
        }
    },
    {
        'csv_file': 'data/Spend by product type.csv',
        'table_name': 'SPEND_BY_PRODUCT_TYPE',
        'column_mapping': {
            'Claim Form Type': 'CLAIM_FORM_TYPE',
            'Product': 'PRODUCT',
            'PMPM Prior Year': 'PMPM_PREV_YEAR',
            'PMPM': 'PMPM',
            'PMPM YOY%': 'PMPM_YOY_PERCENT',
            'Total Paid Prior Year': 'TOTAL_PAID_PREV_YEAR',
            'Total Paid': 'TOTAL_PAID',
            'Total Paid YOY%': 'TOTAL_PAID_YOY_PERCENT',
            'Cost per Claim Prior Year': 'COST_PER_CLAIM_PREV_YEAR',
            'Cost per Claim': 'COST_PER_CLAIM',
            'Cost per Claim YOY%': 'COST_PER_CLAIM_YOY_PERCENT'
        }
    },
    {
        'csv_file': 'data/Spend by bill type.csv',
        'table_name': 'SPEND_BY_BILL_TYPE',
        'column_mapping': {
            'Claim Form Type': 'CLAIM_FORM_TYPE',
            'Bill Type Code': 'BILL_TYPE',
            'PMPM Prior Year': 'PMPM_PREV_YEAR',
            'PMPM': 'PMPM',
            'PMPM YOY%': 'PMPM_YOY_PERCENT',
            'Total Paid Prior Year': 'TOTAL_PAID_PREV_YEAR',
            'Total Paid': 'TOTAL_PAID',
            'Total Paid YOY%': 'TOTAL_PAID_YOY_PERCENT',
            'Cost per Claim Prior Year': 'COST_PER_CLAIM_PREV_YEAR',
            'Cost per Claim': 'COST_PER_CLAIM',
            'Cost per Claim YOY%': 'COST_PER_CLAIM_YOY_PERCENT'
        }
    }
]

def clean_value(value):
    """Clean dollar and percentage values from CSV"""
    if pd.isna(value) or value is None:
        return None
    if isinstance(value, str):
        # Remove dollar signs and commas
        value = value.replace('$', '').replace(',', '')
        # Remove percentage signs
        value = value.replace('%', '')
        try:
            return float(value)  # Always use float for consistency
        except:
            return value
    if isinstance(value, (int, float)):
        return float(value)  # Convert to float
    return value

def load_csv_data(csv_file, column_mapping):
    """Load and clean CSV data"""
    print(f"\n📂 Loading CSV: {csv_file}")
    df = pd.read_csv(csv_file)
    
    # Clean data
    for col in df.columns:
        df[col] = df[col].apply(clean_value)
    
    # Handle NaN values
    df = df.replace({pd.NA: None, np.nan: None})
    
    # Rename columns to match Snowflake
    df = df.rename(columns=column_mapping)
    
    # Fill empty Product values with 'Total' for product type table
    if 'PRODUCT' in df.columns:
        df['PRODUCT'] = df['PRODUCT'].fillna('Total')
    
    print(f"    Loaded {len(df)} rows, {len(df.columns)} columns")
    return df

def load_snowflake_data(table_name):
    """Load data from Snowflake table"""
    print(f"\n❄️  Loading Snowflake table: {table_name}")
    
    conn = snowflake.connector.connect(**SNOWFLAKE_CONFIG)
    cursor = conn.cursor()
    
    try:
        query = f"SELECT * FROM {SNOWFLAKE_CONFIG['database']}.{SNOWFLAKE_CONFIG['schema']}.{table_name}"
        cursor.execute(query)
        
        # Get column names
        columns = [col[0] for col in cursor.description]
        
        # Fetch all data
        data = cursor.fetchall()
        
        # Create DataFrame
        df = pd.DataFrame(data, columns=columns)
        
        print(f"    Loaded {len(df)} rows, {len(df.columns)} columns")
        return df
        
    finally:
        cursor.close()
        conn.close()

def compare_data_types(csv_df, sf_df, table_name):
    """Compare data types between CSV and Snowflake"""
    results = {
        'table': table_name,
        'csv_dtypes': {},
        'snowflake_dtypes': {},
        'mismatches': []
    }
    
    for col in csv_df.columns:
        csv_type = str(csv_df[col].dtype)
        sf_type = str(sf_df[col].dtype) if col in sf_df.columns else 'NOT FOUND'
        
        results['csv_dtypes'][col] = csv_type
        results['snowflake_dtypes'][col] = sf_type
        
        # Check for type compatibility
        if sf_type == 'NOT FOUND':
            results['mismatches'].append({
                'column': col,
                'issue': 'Column not found in Snowflake table'
            })
        elif (csv_type.startswith('float') or csv_type.startswith('int')) and \
             not (sf_type.startswith('float') or sf_type.startswith('int')):
            results['mismatches'].append({
                'column': col,
                'issue': f'Type mismatch: CSV={csv_type}, Snowflake={sf_type}'
            })
    
    return results

def compare_null_counts(csv_df, sf_df, table_name):
    """Compare null value counts"""
    results = {
        'table': table_name,
        'csv_nulls': {},
        'snowflake_nulls': {},
        'differences': []
    }
    
    for col in csv_df.columns:
        csv_null_count = csv_df[col].isna().sum()
        sf_null_count = sf_df[col].isna().sum() if col in sf_df.columns else -1
        
        results['csv_nulls'][col] = int(csv_null_count)
        results['snowflake_nulls'][col] = int(sf_null_count)
        
        if sf_null_count >= 0 and csv_null_count != sf_null_count:
            results['differences'].append({
                'column': col,
                'csv_nulls': int(csv_null_count),
                'snowflake_nulls': int(sf_null_count),
                'difference': int(sf_null_count - csv_null_count)
            })
    
    return results

def validate_data_samples(csv_df, sf_df, table_name, sample_size=5):
    """Validate sample data records"""
    results = {
        'table': table_name,
        'sample_size': min(sample_size, len(csv_df)),
        'mismatches': []
    }
    
    sample_size = min(sample_size, len(csv_df))
    
    for idx in range(sample_size):
        for col in csv_df.columns:
            if col not in sf_df.columns:
                continue
                
            csv_val = csv_df.iloc[idx][col]
            sf_val = sf_df.iloc[idx][col]
            
            # Handle None/NaN comparison
            if pd.isna(csv_val) and pd.isna(sf_val):
                continue
            
            # Compare numeric values with tolerance
            if isinstance(csv_val, (int, float)) and isinstance(sf_val, (int, float)):
                if not np.isclose(csv_val, sf_val, rtol=1e-5, equal_nan=True):
                    results['mismatches'].append({
                        'row': idx,
                        'column': col,
                        'csv_value': float(csv_val) if csv_val is not None else None,
                        'snowflake_value': float(sf_val) if sf_val is not None else None
                    })
            else:
                # String comparison
                if str(csv_val) != str(sf_val):
                    results['mismatches'].append({
                        'row': idx,
                        'column': col,
                        'csv_value': str(csv_val),
                        'snowflake_value': str(sf_val)
                    })
    
    return results

def generate_validation_report(table_config):
    """Generate comprehensive validation report for a table"""
    print(f"\n{'='*80}")
    print(f" VALIDATING: {table_config['table_name']}")
    print(f"{'='*80}")
    
    # Load data
    csv_df = load_csv_data(table_config['csv_file'], table_config['column_mapping'])
    sf_df = load_snowflake_data(table_config['table_name'])
    
    report = {
        'table_name': table_config['table_name'],
        'csv_file': table_config['csv_file'],
        'timestamp': datetime.now().isoformat(),
        'validations': {}
    }
    
    # 1. Row Count Check
    print("\n Row Count Validation:")
    csv_rows = len(csv_df)
    sf_rows = len(sf_df)
    row_match = csv_rows == sf_rows
    
    report['validations']['row_count'] = {
        'csv_rows': csv_rows,
        'snowflake_rows': sf_rows,
        'match': row_match,
        'difference': sf_rows - csv_rows
    }
    
    if row_match:
        print(f"    Row count MATCHES: {csv_rows} rows")
    else:
        print(f"    Row count MISMATCH: CSV={csv_rows}, Snowflake={sf_rows}, Diff={sf_rows - csv_rows}")
    
    # 2. Column Count Check
    print("\n Column Count Validation:")
    csv_cols = len(csv_df.columns)
    sf_cols = len(sf_df.columns)
    col_match = csv_cols == sf_cols
    
    report['validations']['column_count'] = {
        'csv_columns': csv_cols,
        'snowflake_columns': sf_cols,
        'match': col_match,
        'difference': sf_cols - csv_cols
    }
    
    if col_match:
        print(f"    Column count MATCHES: {csv_cols} columns")
    else:
        print(f"    Column count MISMATCH: CSV={csv_cols}, Snowflake={sf_cols}")
    
    # 3. Column Names Check
    print("\n🏷️  Column Names Validation:")
    csv_columns = set(csv_df.columns)
    sf_columns = set(sf_df.columns)
    
    missing_in_sf = csv_columns - sf_columns
    extra_in_sf = sf_columns - csv_columns
    matching_columns = csv_columns & sf_columns
    
    report['validations']['column_names'] = {
        'csv_columns': list(csv_df.columns),
        'snowflake_columns': list(sf_df.columns),
        'matching': list(matching_columns),
        'missing_in_snowflake': list(missing_in_sf),
        'extra_in_snowflake': list(extra_in_sf)
    }
    
    if not missing_in_sf and not extra_in_sf:
        print(f"    All column names MATCH ({len(matching_columns)} columns)")
    else:
        if missing_in_sf:
            print(f"    Columns in CSV but NOT in Snowflake: {missing_in_sf}")
        if extra_in_sf:
            print(f"     Extra columns in Snowflake: {extra_in_sf}")
    
    # 4. Data Types Comparison
    print("\n🔤 Data Types Validation:")
    dtype_results = compare_data_types(csv_df, sf_df, table_config['table_name'])
    report['validations']['data_types'] = dtype_results
    
    if dtype_results['mismatches']:
        print(f"     Found {len(dtype_results['mismatches'])} data type issues:")
        for mismatch in dtype_results['mismatches']:
            print(f"      - {mismatch['column']}: {mismatch['issue']}")
    else:
        print("    Data types are compatible")
    
    # 5. Null Values Check
    print("\n Null Values Validation:")
    null_results = compare_null_counts(csv_df, sf_df, table_config['table_name'])
    report['validations']['null_counts'] = null_results
    
    if null_results['differences']:
        print(f"     Found null count differences in {len(null_results['differences'])} columns:")
        for diff in null_results['differences']:
            print(f"      - {diff['column']}: CSV={diff['csv_nulls']}, Snowflake={diff['snowflake_nulls']}, Diff={diff['difference']}")
    else:
        print("    Null counts MATCH across all columns")
    
    # 6. Data Validation (Sample Records)
    print("\n Data Validation (Sample Records):")
    sample_results = validate_data_samples(csv_df, sf_df, table_config['table_name'], sample_size=5)
    report['validations']['data_samples'] = sample_results
    
    if sample_results['mismatches']:
        print(f"     Found {len(sample_results['mismatches'])} data mismatches in sample:")
        for mismatch in sample_results['mismatches'][:10]:  # Show first 10
            print(f"      - Row {mismatch['row']}, Column {mismatch['column']}: CSV={mismatch['csv_value']}, SF={mismatch['snowflake_value']}")
    else:
        print(f"    Sample data MATCHES ({sample_results['sample_size']} rows validated)")
    
    # 7. Header Check Summary
    print("\n📑 Header Validation Summary:")
    header_issues = []
    
    for col in csv_df.columns:
        if col not in sf_df.columns:
            header_issues.append(f"Column '{col}' missing in Snowflake")
    
    report['validations']['header_check'] = {
        'issues': header_issues,
        'passed': len(header_issues) == 0
    }
    
    if header_issues:
        print("    Header issues found:")
        for issue in header_issues:
            print(f"      - {issue}")
    else:
        print("    All headers validated successfully")
    
    # Overall Status
    print("\n" + "="*80)
    all_passed = (
        row_match and 
        col_match and 
        not missing_in_sf and 
        not extra_in_sf and 
        not dtype_results['mismatches'] and 
        not null_results['differences'] and 
        not sample_results['mismatches'] and
        not header_issues
    )
    
    report['overall_status'] = 'PASSED' if all_passed else 'FAILED'
    
    if all_passed:
        print(" OVERALL STATUS:  ALL VALIDATIONS PASSED")
    else:
        print("  OVERALL STATUS:  SOME VALIDATIONS FAILED - Review details above")
    
    print("="*80)
    
    return report

def save_reports(reports):
    """Save validation reports to files"""
    output_dir = Path('data/validation_results')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Save individual JSON reports
    for report in reports:
        table_name = report['table_name']
        json_file = output_dir / f'{table_name}_validation_{timestamp}.json'
        
        with open(json_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n💾 Saved JSON report: {json_file}")
    
    # Save consolidated summary report
    summary_file = output_dir / f'validation_summary_{timestamp}.txt'
    
    with open(summary_file, 'w') as f:
        f.write("="*100 + "\n")
        f.write("EXCEL vs SNOWFLAKE DATA VALIDATION SUMMARY\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("="*100 + "\n\n")
        
        for report in reports:
            f.write(f"\nTABLE: {report['table_name']}\n")
            f.write("-"*100 + "\n")
            f.write(f"CSV File: {report['csv_file']}\n")
            f.write(f"Overall Status: {report['overall_status']}\n\n")
            
            # Row count
            rc = report['validations']['row_count']
            f.write(f"Row Count: CSV={rc['csv_rows']}, Snowflake={rc['snowflake_rows']}, Match={rc['match']}\n")
            
            # Column count
            cc = report['validations']['column_count']
            f.write(f"Column Count: CSV={cc['csv_columns']}, Snowflake={cc['snowflake_columns']}, Match={cc['match']}\n")
            
            # Column names
            cn = report['validations']['column_names']
            f.write(f"Matching Columns: {len(cn['matching'])}\n")
            if cn['missing_in_snowflake']:
                f.write(f"Missing in Snowflake: {cn['missing_in_snowflake']}\n")
            if cn['extra_in_snowflake']:
                f.write(f"Extra in Snowflake: {cn['extra_in_snowflake']}\n")
            
            # Data type issues
            dt = report['validations']['data_types']
            if dt['mismatches']:
                f.write(f"Data Type Issues: {len(dt['mismatches'])}\n")
                for issue in dt['mismatches']:
                    f.write(f"  - {issue['column']}: {issue['issue']}\n")
            
            # Null count differences
            nc = report['validations']['null_counts']
            if nc['differences']:
                f.write(f"Null Count Differences: {len(nc['differences'])}\n")
                for diff in nc['differences']:
                    f.write(f"  - {diff['column']}: CSV={diff['csv_nulls']}, SF={diff['snowflake_nulls']}\n")
            
            # Data mismatches
            ds = report['validations']['data_samples']
            if ds['mismatches']:
                f.write(f"Data Mismatches in Sample: {len(ds['mismatches'])}\n")
            
            f.write("\n")
        
        f.write("="*100 + "\n")
    
    print(f"💾 Saved summary report: {summary_file}")
    
    # Save Excel comparison report
    excel_file = output_dir / f'validation_comparison_{timestamp}.xlsx'
    
    with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
        for report in reports:
            table_name = report['table_name']
            
            # Create summary sheet for each table
            summary_data = {
                'Validation Check': [
                    'Row Count',
                    'Column Count',
                    'Column Names Match',
                    'Data Types Compatible',
                    'Null Counts Match',
                    'Sample Data Match',
                    'Overall Status'
                ],
                'CSV Value': [
                    report['validations']['row_count']['csv_rows'],
                    report['validations']['column_count']['csv_columns'],
                    len(report['validations']['column_names']['csv_columns']),
                    'N/A',
                    'N/A',
                    'N/A',
                    report['csv_file']
                ],
                'Snowflake Value': [
                    report['validations']['row_count']['snowflake_rows'],
                    report['validations']['column_count']['snowflake_columns'],
                    len(report['validations']['column_names']['snowflake_columns']),
                    'N/A',
                    'N/A',
                    'N/A',
                    report['overall_status']
                ],
                'Status': [
                    ' PASS' if report['validations']['row_count']['match'] else ' FAIL',
                    ' PASS' if report['validations']['column_count']['match'] else ' FAIL',
                    ' PASS' if not report['validations']['column_names']['missing_in_snowflake'] else ' FAIL',
                    ' PASS' if not report['validations']['data_types']['mismatches'] else ' WARN',
                    ' PASS' if not report['validations']['null_counts']['differences'] else ' WARN',
                    ' PASS' if not report['validations']['data_samples']['mismatches'] else ' FAIL',
                    ' PASS' if report['overall_status'] == 'PASSED' else ' FAIL'
                ]
            }
            
            summary_df = pd.DataFrame(summary_data)
            summary_df.to_excel(writer, sheet_name=f'{table_name}_Summary', index=False)
    
    print(f"💾 Saved Excel report: {excel_file}")
    
    return summary_file, excel_file

def main():
    """Main execution function"""
    print("\n" + "="*100)
    print("EXCEL vs SNOWFLAKE DATA VALIDATION")
    print("="*100)
    
    all_reports = []
    
    # Validate each table
    for table_config in TABLES_CONFIG:
        try:
            report = generate_validation_report(table_config)
            all_reports.append(report)
        except Exception as e:
            print(f"\n ERROR validating {table_config['table_name']}: {str(e)}")
            import traceback
            traceback.print_exc()
    
    # Save all reports
    if all_reports:
        print("\n" + "="*100)
        print("SAVING VALIDATION REPORTS")
        print("="*100)
        
        summary_file, excel_file = save_reports(all_reports)
        
        print("\n" + "="*100)
        print(" VALIDATION COMPLETE")
        print("="*100)
        print(f"\nGenerated {len(all_reports)} validation reports:")
        print(f"  📄 Summary Report: {summary_file}")
        print(f"   Excel Report: {excel_file}")
        print(f"   All reports in: data/validation_results/")
        print("\n")

if __name__ == "__main__":
    main()
