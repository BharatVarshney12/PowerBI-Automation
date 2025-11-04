"""
Data Validator
Compares PowerBI export data with Snowflake table data
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
import allure
from allure_commons.types import AttachmentType
from config.snowflake_config import VALIDATION_CONFIG


class DataValidator:
 """Validate data between PowerBI export and Snowflake"""
 
 def __init__(self, powerbi_df: pd.DataFrame, snowflake_df: pd.DataFrame):
 self.powerbi_df = powerbi_df
 self.snowflake_df = snowflake_df
 self.validation_results = {}
 
 def validate_row_count(self) -> Dict:
 """Compare row counts between datasets"""
 with allure.step('Validate Row Count'):
 powerbi_rows = len(self.powerbi_df)
 snowflake_rows = len(self.snowflake_df)
 
 match = powerbi_rows == snowflake_rows
 
 result = {
 'test': 'Row Count Validation',
 'powerbi_count': powerbi_rows,
 'snowflake_count': snowflake_rows,
 'match': match,
 'difference': abs(powerbi_rows - snowflake_rows)
 }
 
 status = " PASSED" if match else " FAILED"
 print(f"[VALIDATION] Row Count: {status}")
 print(f" PowerBI: {powerbi_rows} rows")
 print(f" Snowflake: {snowflake_rows} rows")
 
 allure.attach(
 f"PowerBI Rows: {powerbi_rows}\n"
 f"Snowflake Rows: {snowflake_rows}\n"
 f"Match: {match}\n"
 f"Difference: {result['difference']}",
 'Row Count Validation',
 AttachmentType.TEXT
 )
 
 self.validation_results['row_count'] = result
 return result
 
 def validate_columns(self) -> Dict:
 """Compare column names and count"""
 with allure.step('Validate Column Names'):
 powerbi_cols = set(self.powerbi_df.columns)
 snowflake_cols = set(self.snowflake_df.columns)
 
 common_cols = powerbi_cols.intersection(snowflake_cols)
 powerbi_only = powerbi_cols - snowflake_cols
 snowflake_only = snowflake_cols - powerbi_cols
 
 match = powerbi_cols == snowflake_cols
 
 result = {
 'test': 'Column Validation',
 'powerbi_columns': list(powerbi_cols),
 'snowflake_columns': list(snowflake_cols),
 'common_columns': list(common_cols),
 'powerbi_only': list(powerbi_only),
 'snowflake_only': list(snowflake_only),
 'match': match
 }
 
 status = " PASSED" if match else " FAILED"
 print(f"[VALIDATION] Column Names: {status}")
 print(f" Common: {len(common_cols)} columns")
 if powerbi_only:
 print(f" PowerBI only: {powerbi_only}")
 if snowflake_only:
 print(f" Snowflake only: {snowflake_only}")
 
 allure.attach(
 f"Common Columns: {', '.join(common_cols)}\n"
 f"PowerBI Only: {', '.join(powerbi_only) if powerbi_only else 'None'}\n"
 f"Snowflake Only: {', '.join(snowflake_only) if snowflake_only else 'None'}\n"
 f"Match: {match}",
 'Column Validation',
 AttachmentType.TEXT
 )
 
 self.validation_results['columns'] = result
 return result
 
 def validate_data_types(self) -> Dict:
 """Compare data types of common columns"""
 with allure.step('Validate Data Types'):
 powerbi_types = self.powerbi_df.dtypes.to_dict()
 snowflake_types = self.snowflake_df.dtypes.to_dict()
 
 common_cols = set(powerbi_types.keys()).intersection(set(snowflake_types.keys()))
 
 type_mismatches = []
 for col in common_cols:
 pb_type = str(powerbi_types[col])
 sf_type = str(snowflake_types[col])
 if pb_type != sf_type:
 type_mismatches.append({
 'column': col,
 'powerbi_type': pb_type,
 'snowflake_type': sf_type
 })
 
 match = len(type_mismatches) == 0
 
 result = {
 'test': 'Data Type Validation',
 'mismatches': type_mismatches,
 'match': match
 }
 
 status = " PASSED" if match else " WARNING"
 print(f"[VALIDATION] Data Types: {status}")
 if type_mismatches:
 for mismatch in type_mismatches:
 print(f" {mismatch['column']}: PB={mismatch['powerbi_type']}, SF={mismatch['snowflake_type']}")
 
 allure.attach(
 f"Type Mismatches: {len(type_mismatches)}\n"
 f"Details: {type_mismatches}",
 'Data Type Validation',
 AttachmentType.TEXT
 )
 
 self.validation_results['data_types'] = result
 return result
 
 def validate_null_values(self) -> Dict:
 """Compare null value counts"""
 with allure.step('Validate Null Values'):
 common_cols = set(self.powerbi_df.columns).intersection(set(self.snowflake_df.columns))
 
 null_comparison = []
 for col in common_cols:
 pb_nulls = self.powerbi_df[col].isnull().sum()
 sf_nulls = self.snowflake_df[col].isnull().sum()
 
 if pb_nulls != sf_nulls:
 null_comparison.append({
 'column': col,
 'powerbi_nulls': int(pb_nulls),
 'snowflake_nulls': int(sf_nulls),
 'difference': int(abs(pb_nulls - sf_nulls))
 })
 
 match = len(null_comparison) == 0
 
 result = {
 'test': 'Null Value Validation',
 'discrepancies': null_comparison,
 'match': match
 }
 
 status = " PASSED" if match else " WARNING"
 print(f"[VALIDATION] Null Values: {status}")
 for disc in null_comparison:
 print(f" {disc['column']}: PB={disc['powerbi_nulls']}, SF={disc['snowflake_nulls']}")
 
 allure.attach(
 f"Null Value Discrepancies: {len(null_comparison)}\n"
 f"Details: {null_comparison}",
 'Null Value Validation',
 AttachmentType.TEXT
 )
 
 self.validation_results['null_values'] = result
 return result
 
 def validate_duplicates(self) -> Dict:
 """Check for duplicate rows"""
 with allure.step('Validate Duplicate Rows'):
 powerbi_duplicates = self.powerbi_df.duplicated().sum()
 snowflake_duplicates = self.snowflake_df.duplicated().sum()
 
 result = {
 'test': 'Duplicate Row Validation',
 'powerbi_duplicates': int(powerbi_duplicates),
 'snowflake_duplicates': int(snowflake_duplicates),
 'match': powerbi_duplicates == snowflake_duplicates
 }
 
 status = " PASSED" if result['match'] else " WARNING"
 print(f"[VALIDATION] Duplicates: {status}")
 print(f" PowerBI: {powerbi_duplicates} duplicates")
 print(f" Snowflake: {snowflake_duplicates} duplicates")
 
 allure.attach(
 f"PowerBI Duplicates: {powerbi_duplicates}\n"
 f"Snowflake Duplicates: {snowflake_duplicates}\n"
 f"Match: {result['match']}",
 'Duplicate Validation',
 AttachmentType.TEXT
 )
 
 self.validation_results['duplicates'] = result
 return result
 
 def validate_numeric_values(self, tolerance: float = 0.01) -> Dict:
 """Compare numeric column values with tolerance"""
 with allure.step('Validate Numeric Values'):
 numeric_cols = self.powerbi_df.select_dtypes(include=[np.number]).columns
 common_numeric = set(numeric_cols).intersection(set(self.snowflake_df.columns))
 
 value_comparisons = []
 for col in common_numeric:
 try:
 pb_values = self.powerbi_df[col].dropna()
 sf_values = self.snowflake_df[col].dropna()
 
 # Compare statistics
 pb_mean = pb_values.mean()
 sf_mean = sf_values.mean()
 
 diff_pct = abs(pb_mean - sf_mean) / pb_mean if pb_mean != 0 else 0
 
 value_comparisons.append({
 'column': col,
 'powerbi_mean': float(pb_mean),
 'snowflake_mean': float(sf_mean),
 'difference_pct': float(diff_pct * 100),
 'within_tolerance': diff_pct <= tolerance
 })
 except Exception as e:
 print(f" Warning: Could not compare {col}: {e}")
 
 all_within_tolerance = all(comp['within_tolerance'] for comp in value_comparisons)
 
 result = {
 'test': 'Numeric Value Validation',
 'tolerance': tolerance * 100,
 'comparisons': value_comparisons,
 'match': all_within_tolerance
 }
 
 status = " PASSED" if all_within_tolerance else " WARNING"
 print(f"[VALIDATION] Numeric Values: {status}")
 for comp in value_comparisons:
 print(f" {comp['column']}: Diff={comp['difference_pct']:.2f}%")
 
 allure.attach(
 f"Tolerance: {tolerance * 100}%\n"
 f"Columns Compared: {len(value_comparisons)}\n"
 f"All Within Tolerance: {all_within_tolerance}\n\n"
 + "\n".join([f"{c['column']}: {c['difference_pct']:.2f}%" for c in value_comparisons]),
 'Numeric Value Validation',
 AttachmentType.TEXT
 )
 
 self.validation_results['numeric_values'] = result
 return result
 
 def run_all_validations(self) -> Dict:
 """Run all validation checks"""
 with allure.step('Run Complete Data Validation'):
 print("\n" + "="*70)
 print("STARTING DATA VALIDATION")
 print("="*70)
 
 config = VALIDATION_CONFIG['comparison_rules']
 
 if config.get('validate_row_count', True):
 self.validate_row_count()
 
 if config.get('validate_columns', True):
 self.validate_columns()
 
 if config.get('validate_data_types', True):
 self.validate_data_types()
 
 if config.get('validate_nulls', True):
 self.validate_null_values()
 
 if config.get('validate_duplicates', True):
 self.validate_duplicates()
 
 self.validate_numeric_values(tolerance=config.get('tolerance', 0.01))
 
 # Generate summary
 total_tests = len(self.validation_results)
 passed_tests = sum(1 for r in self.validation_results.values() if r.get('match', False))
 
 summary = {
 'total_tests': total_tests,
 'passed': passed_tests,
 'failed': total_tests - passed_tests,
 'pass_rate': (passed_tests / total_tests * 100) if total_tests > 0 else 0,
 'details': self.validation_results
 }
 
 print("\n" + "="*70)
 print(f"VALIDATION SUMMARY: {passed_tests}/{total_tests} tests passed ({summary['pass_rate']:.1f}%)")
 print("="*70 + "\n")
 
 allure.attach(
 f"Total Tests: {total_tests}\n"
 f"Passed: {passed_tests}\n"
 f"Failed: {total_tests - passed_tests}\n"
 f"Pass Rate: {summary['pass_rate']:.1f}%",
 'Validation Summary',
 AttachmentType.TEXT
 )
 
 return summary
