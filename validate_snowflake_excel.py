"""
Snowflake Data Validation Script
Validates Excel data against Snowflake database and generates detailed report
"""

import pandas as pd
from pathlib import Path
import time
from datetime import datetime
from utils.snowflake_connector import SnowflakeConnector
from utils.logger import (
    log_test_start, log_test_end, log_step, log_action,
    log_verification, log_data, log_error, log_performance
)


class SnowflakeExcelValidator:
    """Validates Excel data against Snowflake database"""
    
    def __init__(self, excel_path: str):
        self.excel_path = Path(excel_path)
        self.results = []
        self.summary = {}
        
    def load_excel_data(self):
        """Load all sheets from Excel file"""
        log_step("Loading Excel file")
        log_action("Reading Excel", str(self.excel_path))
        
        excel_data = {}
        with pd.ExcelFile(self.excel_path) as xls:
            for sheet_name in xls.sheet_names:
                df = pd.read_excel(xls, sheet_name=sheet_name)
                excel_data[sheet_name] = df
                log_action(f"Loaded sheet: {sheet_name}", f"{len(df)} rows, {len(df.columns)} columns")
                print(f"   ✅ {sheet_name}: {len(df)} rows, {len(df.columns)} columns")
        
        return excel_data
    
    def validate_table(self, table_name: str, excel_df: pd.DataFrame, snowflake_df: pd.DataFrame):
        """Validate single table data"""
        log_step(f"Validating table: {table_name}")
        
        validation_result = {
            'table_name': table_name,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'validations': []
        }
        
        print(f"\n{'='*80}")
        print(f"VALIDATING: {table_name}")
        print(f"{'='*80}")
        
        # 1. Row Count Validation
        excel_rows = len(excel_df)
        sf_rows = len(snowflake_df)
        row_match = excel_rows == sf_rows
        
        validation_result['validations'].append({
            'check': 'Row Count',
            'excel_value': excel_rows,
            'snowflake_value': sf_rows,
            'match': row_match,
            'status': 'PASS' if row_match else 'FAIL'
        })
        
        log_verification("Row Count Match", row_match, f"Excel: {excel_rows}, Snowflake: {sf_rows}")
        print(f"   Row Count: Excel={excel_rows}, Snowflake={sf_rows} {'✅ MATCH' if row_match else '❌ MISMATCH'}")
        
        # 2. Column Count Validation
        excel_cols = len(excel_df.columns)
        sf_cols = len(snowflake_df.columns)
        col_count_match = excel_cols == sf_cols
        
        validation_result['validations'].append({
            'check': 'Column Count',
            'excel_value': excel_cols,
            'snowflake_value': sf_cols,
            'match': col_count_match,
            'status': 'PASS' if col_count_match else 'FAIL'
        })
        
        log_verification("Column Count Match", col_count_match, f"Excel: {excel_cols}, Snowflake: {sf_cols}")
        print(f"   Column Count: Excel={excel_cols}, Snowflake={sf_cols} {'✅ MATCH' if col_count_match else '❌ MISMATCH'}")
        
        # 3. Column Names Validation
        excel_columns = set(excel_df.columns.str.upper())
        sf_columns = set(snowflake_df.columns.str.upper())
        
        common_cols = excel_columns & sf_columns
        excel_only = excel_columns - sf_columns
        sf_only = sf_columns - excel_columns
        
        col_names_match = excel_columns == sf_columns
        
        validation_result['validations'].append({
            'check': 'Column Names',
            'excel_value': ', '.join(sorted(excel_columns)),
            'snowflake_value': ', '.join(sorted(sf_columns)),
            'match': col_names_match,
            'status': 'PASS' if col_names_match else 'FAIL',
            'common_columns': ', '.join(sorted(common_cols)),
            'excel_only': ', '.join(sorted(excel_only)) if excel_only else 'None',
            'snowflake_only': ', '.join(sorted(sf_only)) if sf_only else 'None'
        })
        
        log_verification("Column Names Match", col_names_match)
        print(f"   Column Names: {'✅ MATCH' if col_names_match else '❌ MISMATCH'}")
        if not col_names_match:
            if excel_only:
                print(f"      Excel Only: {', '.join(sorted(excel_only))}")
            if sf_only:
                print(f"      Snowflake Only: {', '.join(sorted(sf_only))}")
        
        # 4. Data Type Validation (for common columns)
        dtype_matches = 0
        dtype_mismatches = 0
        
        for col in common_cols:
            excel_col = excel_df.columns[excel_df.columns.str.upper() == col][0]
            sf_col = snowflake_df.columns[snowflake_df.columns.str.upper() == col][0]
            
            excel_dtype = str(excel_df[excel_col].dtype)
            sf_dtype = str(snowflake_df[sf_col].dtype)
            
            # Simplified type matching (object/string compatibility)
            match = (excel_dtype == sf_dtype or 
                    (excel_dtype == 'object' and sf_dtype == 'object'))
            
            if match:
                dtype_matches += 1
            else:
                dtype_mismatches += 1
        
        validation_result['validations'].append({
            'check': 'Data Types',
            'excel_value': f'{dtype_matches} matching types',
            'snowflake_value': f'{dtype_mismatches} mismatches',
            'match': dtype_mismatches == 0,
            'status': 'PASS' if dtype_mismatches == 0 else 'PARTIAL'
        })
        
        print(f"   Data Types: {dtype_matches} matches, {dtype_mismatches} mismatches")
        
        # 5. Data Content Validation (for common columns and matching rows)
        if row_match and len(common_cols) > 0:
            content_matches = 0
            content_mismatches = 0
            
            for col in common_cols:
                excel_col = excel_df.columns[excel_df.columns.str.upper() == col][0]
                sf_col = snowflake_df.columns[snowflake_df.columns.str.upper() == col][0]
                
                # Compare values (convert to string for comparison)
                excel_values = excel_df[excel_col].astype(str).str.strip()
                sf_values = snowflake_df[sf_col].astype(str).str.strip()
                
                matches = (excel_values == sf_values).sum()
                total = len(excel_values)
                
                if matches == total:
                    content_matches += 1
                else:
                    content_mismatches += 1
                    print(f"      Column '{col}': {matches}/{total} values match")
            
            validation_result['validations'].append({
                'check': 'Data Content',
                'excel_value': f'{len(common_cols)} columns checked',
                'snowflake_value': f'{content_matches} fully matching columns',
                'match': content_mismatches == 0,
                'status': 'PASS' if content_mismatches == 0 else 'FAIL',
                'details': f'{content_matches} exact matches, {content_mismatches} with differences'
            })
            
            print(f"   Data Content: {content_matches}/{len(common_cols)} columns match exactly")
        
        # Calculate overall status
        passed = sum(1 for v in validation_result['validations'] if v['status'] == 'PASS')
        total = len(validation_result['validations'])
        validation_result['pass_rate'] = (passed / total * 100) if total > 0 else 0
        validation_result['overall_status'] = 'PASS' if passed == total else 'FAIL'
        
        print(f"\n   Overall: {passed}/{total} checks passed ({validation_result['pass_rate']:.1f}%)")
        
        return validation_result
    
    def run_validation(self):
        """Run complete validation"""
        test_name = "Snowflake Excel Validation"
        log_test_start(test_name)
        start_time = time.time()
        
        print("\n" + "="*80)
        print("SNOWFLAKE EXCEL VALIDATION")
        print("="*80)
        
        try:
            # Load Excel data
            excel_data = self.load_excel_data()
            
            # Connect to Snowflake
            log_step("Connect to Snowflake")
            
            with SnowflakeConnector() as sf_conn:
                
                # Map sheet names to Snowflake tables
                table_mapping = {
                    'CUSTOMERS': 'CUSTOMERS',
                    'ORDERS': 'ORDERS',
                    'ORDER_ITEMS': 'ORDER_ITEMS',
                    'VALIDATION_QUERY_RESULT': None  # Custom query result
                }
                
                # Validate each table
                for sheet_name, table_name in table_mapping.items():
                    if sheet_name not in excel_data:
                        print(f"\n⚠️  Sheet '{sheet_name}' not found in Excel file, skipping...")
                        continue
                    
                    excel_df = excel_data[sheet_name]
                    
                    if table_name:
                        # Standard table validation
                        log_action(f"Fetching Snowflake table: {table_name}")
                        sf_df = sf_conn.get_table_data(table_name)
                        
                        result = self.validate_table(sheet_name, excel_df, sf_df)
                        self.results.append(result)
                    
                    elif sheet_name == 'VALIDATION_QUERY_RESULT':
                        # Special validation query
                        log_step("Validating VALIDATION_QUERY_RESULT")
                        
                        query = """
                        SELECT 
                            CONCAT(c.FIRST_NAME, ' ', c.LAST_NAME) AS CUSTOMER_NAME,
                            o.ORDER_ID,
                            o.ORDER_STATUS,
                            o.TOTAL_AMOUNT AS CALCULATED_TOTAL
                        FROM CUSTOMERS c
                        JOIN ORDERS o ON c.CUSTOMER_ID = o.CUSTOMER_ID
                        ORDER BY o.ORDER_ID
                        """
                        
                        log_action("Executing validation query", query[:100] + "...")
                        sf_df = sf_conn.execute_query(query)
                        
                        result = self.validate_table(sheet_name, excel_df, sf_df)
                        result['query'] = query
                        self.results.append(result)
                
                # Generate summary
                self.generate_summary()
                
                # Save results
                output_path = self.save_results()
                
                duration = time.time() - start_time
                log_performance("Total Validation", duration)
                log_test_end(test_name, "COMPLETED")
                
                print("\n" + "="*80)
                print(f"✅ VALIDATION COMPLETED in {duration:.2f}s")
                print(f"📊 Results saved to: {output_path}")
                print("="*80)
                
                return output_path
                
        except Exception as e:
            log_error(f"Validation failed: {str(e)}", exc_info=True)
            log_test_end(test_name, "FAILED")
            raise
    
    def generate_summary(self):
        """Generate validation summary"""
        log_step("Generating summary")
        
        total_tables = len(self.results)
        passed_tables = sum(1 for r in self.results if r['overall_status'] == 'PASS')
        
        total_checks = sum(len(r['validations']) for r in self.results)
        passed_checks = sum(
            sum(1 for v in r['validations'] if v['status'] == 'PASS')
            for r in self.results
        )
        
        self.summary = {
            'total_tables': total_tables,
            'passed_tables': passed_tables,
            'failed_tables': total_tables - passed_tables,
            'total_checks': total_checks,
            'passed_checks': passed_checks,
            'failed_checks': total_checks - passed_checks,
            'pass_rate': (passed_checks / total_checks * 100) if total_checks > 0 else 0
        }
        
        print("\n" + "="*80)
        print("VALIDATION SUMMARY")
        print("="*80)
        print(f"Tables Validated: {total_tables}")
        print(f"Tables Passed: {passed_tables}")
        print(f"Tables Failed: {self.summary['failed_tables']}")
        print(f"Total Checks: {total_checks}")
        print(f"Checks Passed: {passed_checks}")
        print(f"Checks Failed: {self.summary['failed_checks']}")
        print(f"Overall Pass Rate: {self.summary['pass_rate']:.1f}%")
        
        log_data("Validation Summary", self.summary)
    
    def save_results(self):
        """Save validation results to Excel"""
        log_step("Saving results to Excel")
        
        output_dir = Path(__file__).parent / 'data' / 'downloads'
        output_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = output_dir / f'validation_results_{timestamp}.xlsx'
        
        with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
            # Summary sheet
            summary_df = pd.DataFrame([self.summary])
            summary_df.to_excel(writer, sheet_name='Summary', index=False)
            
            # Detailed results for each table
            for result in self.results:
                sheet_name = result['table_name'][:31]  # Excel sheet name limit
                
                # Create detailed validation dataframe
                validations_df = pd.DataFrame(result['validations'])
                
                # Add metadata
                metadata = {
                    'Table': [result['table_name']],
                    'Timestamp': [result['timestamp']],
                    'Overall Status': [result['overall_status']],
                    'Pass Rate': [f"{result['pass_rate']:.1f}%"]
                }
                metadata_df = pd.DataFrame(metadata)
                
                # Write to sheet
                metadata_df.to_excel(writer, sheet_name=sheet_name, index=False, startrow=0)
                validations_df.to_excel(writer, sheet_name=sheet_name, index=False, startrow=len(metadata_df) + 2)
            
            # All checks combined
            all_checks = []
            for result in self.results:
                for validation in result['validations']:
                    all_checks.append({
                        'Table': result['table_name'],
                        'Check': validation['check'],
                        'Excel Value': validation.get('excel_value', ''),
                        'Snowflake Value': validation.get('snowflake_value', ''),
                        'Match': validation['match'],
                        'Status': validation['status']
                    })
            
            all_checks_df = pd.DataFrame(all_checks)
            all_checks_df.to_excel(writer, sheet_name='All_Checks', index=False)
        
        log_action("Results saved", str(output_path))
        print(f"\n📊 Results saved to: {output_path}")
        
        return output_path


def main():
    """Main execution"""
    # Path to Excel file
    excel_path = Path(__file__).parent / 'data' / 'downloads' / 'snowflake_validation_data.xlsx'
    
    if not excel_path.exists():
        print(f"❌ Error: Excel file not found at {excel_path}")
        print("Please run: python utils/create_sample_data.py")
        return
    
    # Run validation
    validator = SnowflakeExcelValidator(excel_path)
    output_path = validator.run_validation()
    
    print(f"\n✅ Validation complete! Results saved to:")
    print(f"   {output_path}")


if __name__ == "__main__":
    main()
