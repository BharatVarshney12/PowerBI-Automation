"""
Excel vs CSV Comparator using DataComPy
Completely separate from your existing comparison code
"""
import pandas as pd
import datacompy
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime
from .config import EXCEL_FOLDER, CSV_FOLDER, COMPARISON_CONFIG, DATACOMPY_SETTINGS


class ExcelCSVComparator:
    """
    Compare Excel and CSV files using datacompy library
    """
    
    def __init__(self):
        self.excel_folder = EXCEL_FOLDER
        self.csv_folder = CSV_FOLDER
        self.comparison_results = {}
    
    def load_excel(self, filename: str) -> pd.DataFrame:
        """
        Load and clean Excel file
        
        Args:
            filename: Excel file name
            
        Returns:
            Cleaned DataFrame
        """
        filepath = self.excel_folder / filename
        
        if not filepath.exists():
            raise FileNotFoundError(f"Excel file not found: {filepath}")
        
        print(f"📊 Loading Excel: {filename}")
        
        # Load Excel
        df = pd.read_excel(filepath, engine='openpyxl')
        
        # Clean data
        df = self._clean_dataframe(df, "Excel")
        
        print(f"   ✓ Loaded {len(df)} rows, {len(df.columns)} columns")
        
        return df
    
    def load_csv(self, filename: str) -> pd.DataFrame:
        """
        Load and clean CSV file
        
        Args:
            filename: CSV file name
            
        Returns:
            Cleaned DataFrame
        """
        filepath = self.csv_folder / filename
        
        if not filepath.exists():
            raise FileNotFoundError(f"CSV file not found: {filepath}")
        
        print(f"📄 Loading CSV: {filename}")
        
        # Load CSV
        df = pd.read_csv(filepath)
        
        # Clean data
        df = self._clean_dataframe(df, "CSV")
        
        print(f"   ✓ Loaded {len(df)} rows, {len(df.columns)} columns")
        
        return df
    
    def _clean_dataframe(self, df: pd.DataFrame, source: str) -> pd.DataFrame:
        """
        Clean DataFrame - remove blanks, standardize columns
        
        Args:
            df: DataFrame to clean
            source: Source name (for logging)
            
        Returns:
            Cleaned DataFrame
        """
        original_rows = len(df)
        
        # Remove completely blank rows
        df = df.dropna(how='all')
        
        # Remove filter description rows (if any)
        if len(df) > 0:
            df = df[~df.iloc[:, 0].astype(str).str.contains('Applied filters:', na=False)]
        
        # Clean column names - strip whitespace and convert to uppercase
        df.columns = df.columns.str.strip().str.upper()
        
        # Clean numeric values in CSV files (remove $, %, commas)
        if source == "CSV":
            df = self._clean_csv_numeric_values(df)
        
        # Reset index
        df = df.reset_index(drop=True)
        
        removed = original_rows - len(df)
        if removed > 0:
            print(f"   ⚠ Removed {removed} blank/filter rows from {source}")
        
        return df
    
    def _clean_csv_numeric_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean numeric values in CSV that have formatting like $, %, commas
        
        Args:
            df: DataFrame to clean
            
        Returns:
            DataFrame with cleaned numeric values
        """
        for col in df.columns:
            # Skip the first column (usually the key column with text)
            if col == df.columns[0]:
                continue
            
            # Check if column has string values that look like numbers
            if df[col].dtype == 'object':
                try:
                    # Check if values contain % before cleaning
                    has_percent = df[col].astype(str).str.contains('%', na=False).any()
                    
                    # Remove $, %, commas and convert to float
                    cleaned = df[col].astype(str).str.replace('$', '', regex=False)
                    cleaned = cleaned.str.replace(',', '', regex=False)
                    cleaned = cleaned.str.replace('%', '', regex=False)
                    cleaned = cleaned.str.strip()
                    
                    # Try to convert to numeric
                    numeric_series = pd.to_numeric(cleaned, errors='coerce')
                    
                    # If successful conversion, use cleaned values
                    if not numeric_series.isna().all():
                        # If original had %, divide by 100 to match Excel decimal format
                        if has_percent:
                            numeric_series = numeric_series / 100
                        
                        df[col] = numeric_series
                            
                except Exception as e:
                    # If cleaning fails, keep original values
                    pass
        
        return df
        df = df.reset_index(drop=True)
        
        removed = original_rows - len(df)
        if removed > 0:
            print(f"   ⚠ Removed {removed} blank/filter rows from {source}")
        
        return df
    
    def compare(
        self, 
        table_key: str,
        excel_df: Optional[pd.DataFrame] = None,
        csv_df: Optional[pd.DataFrame] = None
    ) -> datacompy.Compare:
        """
        Compare Excel and CSV using datacompy
        
        Args:
            table_key: Key from COMPARISON_CONFIG
            excel_df: Optional pre-loaded Excel DataFrame
            csv_df: Optional pre-loaded CSV DataFrame
            
        Returns:
            datacompy.Compare object with results
        """
        if table_key not in COMPARISON_CONFIG:
            raise ValueError(f"Unknown table: {table_key}")
        
        config = COMPARISON_CONFIG[table_key]
        
        print(f"\n{'='*80}")
        print(f"🔍 Comparing: {table_key}")
        print(f"{'='*80}\n")
        
        # Load data if not provided
        if excel_df is None:
            excel_df = self.load_excel(config['excel_file'])
        
        if csv_df is None:
            csv_df = self.load_csv(config['csv_file'])
        
        print(f"\n⚙ Running DataComPy comparison...")
        print(f"   Join columns: {config['join_columns']}")
        print(f"   Numeric tolerance: {config['abs_tol']}")
        
        # Create datacompy comparison
        compare = datacompy.Compare(
            df1=excel_df,
            df2=csv_df,
            join_columns=config['join_columns'],
            abs_tol=config['abs_tol'],
            rel_tol=config.get('rel_tol', 0),
            df1_name='Excel',
            df2_name='CSV',
            **DATACOMPY_SETTINGS
        )
        
        # Store results
        self.comparison_results[table_key] = {
            'compare_object': compare,
            'matches': compare.matches(),
            'timestamp': datetime.now()
        }
        
        # Print summary
        self._print_summary(compare, table_key)
        
        return compare
    
    def _print_summary(self, compare: datacompy.Compare, table_key: str):
        """Print comparison summary"""
        print(f"\n{'='*80}")
        print(f"📊 COMPARISON SUMMARY: {table_key}")
        print(f"{'='*80}\n")
        
        if compare.matches():
            print("✅ SUCCESS: Excel and CSV data are IDENTICAL!")
        else:
            print("⚠ DIFFERENCES FOUND:")
            print(f"   • Rows with differences: {len(compare.all_mismatch())}")
            print(f"   • Rows only in Excel: {len(compare.df1_unq_rows)}")
            print(f"   • Rows only in CSV: {len(compare.df2_unq_rows)}")
            
            # Column differences
            col_stats = compare.column_stats
            if col_stats:
                diff_cols = [stat for stat in col_stats if stat.get('unequal_cnt', 0) > 0]
                if diff_cols:
                    print(f"\n   Columns with differences:")
                    for stat in diff_cols:
                        col_name = stat.get('column', 'Unknown')
                        unequal = stat.get('unequal_cnt', 0)
                        total = stat.get('all_cnt', 1)
                        match_rate = ((total - unequal) / total * 100) if total > 0 else 0
                        print(f"      • {col_name}: {match_rate:.1f}% match ({unequal} mismatches)")
        
        print(f"\n{'='*80}\n")
    
    def get_detailed_report(self, compare: datacompy.Compare) -> str:
        """
        Get detailed text report from datacompy
        
        Args:
            compare: datacompy.Compare object
            
        Returns:
            Full text report
        """
        return compare.report()
    
    def get_mismatches(self, compare: datacompy.Compare) -> pd.DataFrame:
        """
        Get all rows with mismatches
        
        Args:
            compare: datacompy.Compare object
            
        Returns:
            DataFrame with mismatched rows
        """
        return compare.all_mismatch()
    
    def get_excel_only_rows(self, compare: datacompy.Compare) -> pd.DataFrame:
        """Get rows that exist only in Excel"""
        return compare.df1_unq_rows
    
    def get_csv_only_rows(self, compare: datacompy.Compare) -> pd.DataFrame:
        """Get rows that exist only in CSV"""
        return compare.df2_unq_rows
    
    def get_column_stats(self, compare: datacompy.Compare) -> pd.DataFrame:
        """
        Get detailed column statistics
        
        Args:
            compare: datacompy.Compare object
            
        Returns:
            DataFrame with column-level statistics
        """
        stats = compare.column_stats
        if stats:
            return pd.DataFrame(stats)
        return pd.DataFrame()
    
    def compare_all_tables(self) -> Dict[str, datacompy.Compare]:
        """
        Compare all configured tables
        
        Returns:
            Dictionary of comparison results
        """
        results = {}
        
        print("\n" + "="*80)
        print("🚀 COMPARING ALL TABLES")
        print("="*80)
        
        for table_key in COMPARISON_CONFIG.keys():
            try:
                compare = self.compare(table_key)
                results[table_key] = compare
            except FileNotFoundError as e:
                print(f"❌ Error: {e}")
                print(f"   Skipping {table_key}")
            except Exception as e:
                print(f"❌ Unexpected error for {table_key}: {e}")
        
        # Overall summary
        self._print_overall_summary(results)
        
        return results
    
    def _print_overall_summary(self, results: Dict[str, datacompy.Compare]):
        """Print summary for all comparisons"""
        print("\n" + "="*80)
        print("📈 OVERALL SUMMARY")
        print("="*80 + "\n")
        
        total_tables = len(results)
        matching_tables = sum(1 for comp in results.values() if comp.matches())
        
        print(f"Total tables compared: {total_tables}")
        print(f"Perfect matches: {matching_tables}")
        print(f"Tables with differences: {total_tables - matching_tables}")
        
        if matching_tables < total_tables:
            print(f"\n⚠ Tables needing review:")
            for table_key, compare in results.items():
                if not compare.matches():
                    mismatches = len(compare.all_mismatch())
                    print(f"   • {table_key}: {mismatches} rows with differences")
        else:
            print(f"\n✅ All tables match perfectly!")
        
        print(f"\n" + "="*80 + "\n")


# Convenience function
def quick_compare(excel_file: str, csv_file: str, join_columns: list, abs_tol: float = 0.01):
    """
    Quick comparison without configuration
    
    Args:
        excel_file: Excel file name
        csv_file: CSV file name
        join_columns: Columns to join on
        abs_tol: Numeric tolerance
        
    Returns:
        datacompy.Compare object
    """
    comparator = ExcelCSVComparator()
    
    excel_df = comparator.load_excel(excel_file)
    csv_df = comparator.load_csv(csv_file)
    
    compare = datacompy.Compare(
        df1=excel_df,
        df2=csv_df,
        join_columns=join_columns,
        abs_tol=abs_tol,
        df1_name='Excel',
        df2_name='CSV',
        **DATACOMPY_SETTINGS
    )
    
    print(compare.report())
    
    return compare
