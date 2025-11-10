"""
Report Generator for DataComPy Results
Saves comparison results to text and Excel files
"""
import pandas as pd
import datacompy
from pathlib import Path
from datetime import datetime
from typing import Dict
import glob
import os
from .config import OUTPUT_FOLDER, REPORT_SETTINGS


class DataComPyReportGenerator:
    """
    Generate reports from datacompy comparison results
    """
    
    def __init__(self, output_folder: Path = OUTPUT_FOLDER, clean_old_reports: bool = True):
        self.output_folder = output_folder
        self.output_folder.mkdir(parents=True, exist_ok=True)
        
        # Clean old reports on initialization
        if clean_old_reports:
            self.clean_old_reports()
    
    def clean_old_reports(self):
        """Remove all old DataComPy reports from output folder"""
        if not self.output_folder.exists():
            return
        
        # Remove all .txt and .xlsx files
        txt_files = list(self.output_folder.glob("datacompy_*.txt"))
        xlsx_files = list(self.output_folder.glob("datacompy_*.xlsx"))
        
        total_removed = 0
        for file in txt_files + xlsx_files:
            try:
                file.unlink()
                total_removed += 1
            except Exception as e:
                print(f"⚠ Could not remove {file.name}: {e}")
        
        if total_removed > 0:
            print(f"🗑️  Cleaned {total_removed} old report(s) from output folder\n")
    
    def save_text_report(self, compare: datacompy.Compare, table_name: str) -> Path:
        """
        Save text comparison report
        
        Args:
            compare: datacompy.Compare object
            table_name: Name of the table
            
        Returns:
            Path to saved file
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"datacompy_report_{table_name}_{timestamp}.txt"
        filepath = self.output_folder / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"DataComPy Comparison Report\n")
            f.write(f"{'='*80}\n\n")
            f.write(f"Table: {table_name}\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"\n{'='*80}\n\n")
            f.write(compare.report())
        
        print(f"✅ Text report saved: {filepath.name}")
        return filepath
    
    def save_excel_report(
        self, 
        compare: datacompy.Compare, 
        table_name: str,
        include_summary: bool = True,
        include_mismatches: bool = True,
        include_excel_only: bool = True,
        include_csv_only: bool = True,
        include_stats: bool = True
    ) -> Path:
        """
        Save detailed Excel report with multiple sheets
        
        Args:
            compare: datacompy.Compare object
            table_name: Name of the table
            include_summary: Include summary sheet
            include_mismatches: Include mismatches sheet
            include_excel_only: Include Excel-only rows
            include_csv_only: Include CSV-only rows
            include_stats: Include column statistics
            
        Returns:
            Path to saved file
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"datacompy_details_{table_name}_{timestamp}.xlsx"
        filepath = self.output_folder / filename
        
        with pd.ExcelWriter(filepath, engine='xlsxwriter') as writer:
            workbook = writer.book
            
            # Define formats
            header_format = workbook.add_format({
                'bold': True,
                'bg_color': '#4472C4',
                'font_color': 'white',
                'border': 1
            })
            
            success_format = workbook.add_format({
                'bg_color': '#C6EFCE',
                'font_color': '#006100'
            })
            
            warning_format = workbook.add_format({
                'bg_color': '#FFEB9C',
                'font_color': '#9C5700'
            })
            
            # 1. Summary Sheet
            if include_summary:
                summary_data = self._create_summary_data(compare, table_name)
                summary_df = pd.DataFrame(summary_data)
                summary_df.to_excel(writer, sheet_name='Summary', index=False)
                
                worksheet = writer.sheets['Summary']
                worksheet.set_column('A:A', 35)
                worksheet.set_column('B:B', 50)
            
            # 2. All Mismatches
            if include_mismatches:
                mismatches = compare.all_mismatch()
                if not mismatches.empty:
                    mismatches.to_excel(writer, sheet_name='Mismatches', index=False)
                    worksheet = writer.sheets['Mismatches']
                    for col_num, column in enumerate(mismatches.columns):
                        worksheet.write(0, col_num, column, header_format)
            
            # 3. Rows only in Excel
            if include_excel_only:
                excel_only = compare.df1_unq_rows
                if not excel_only.empty:
                    excel_only.to_excel(writer, sheet_name='Only_in_Excel', index=False)
                    worksheet = writer.sheets['Only_in_Excel']
                    for col_num, column in enumerate(excel_only.columns):
                        worksheet.write(0, col_num, column, header_format)
            
            # 4. Rows only in CSV
            if include_csv_only:
                csv_only = compare.df2_unq_rows
                if not csv_only.empty:
                    csv_only.to_excel(writer, sheet_name='Only_in_CSV', index=False)
                    worksheet = writer.sheets['Only_in_CSV']
                    for col_num, column in enumerate(csv_only.columns):
                        worksheet.write(0, col_num, column, header_format)
            
            # 5. Column Statistics
            if include_stats:
                stats = compare.column_stats
                if stats:
                    stats_df = pd.DataFrame(stats)
                    stats_df.to_excel(writer, sheet_name='Column_Statistics', index=False)
                    worksheet = writer.sheets['Column_Statistics']
                    for col_num, column in enumerate(stats_df.columns):
                        worksheet.write(0, col_num, column, header_format)
        
        print(f"✅ Excel report saved: {filepath.name}")
        return filepath
    
    def _create_summary_data(self, compare: datacompy.Compare, table_name: str) -> Dict:
        """Create summary data for report"""
        return {
            'Metric': [
                'Table Name',
                'Comparison Status',
                'Comparison Date',
                '',
                'Excel Rows',
                'CSV Rows',
                'Rows Match',
                '',
                'Common Columns',
                'Columns Only in Excel',
                'Columns Only in CSV',
                '',
                'Rows Only in Excel',
                'Rows Only in CSV',
                'Matching Rows',
                'Rows with Differences',
                '',
                'Match Percentage',
                '',
                'Excel Data Source',
                'CSV Data Source'
            ],
            'Value': [
                table_name,
                '✅ PERFECT MATCH' if compare.matches() else '⚠ DIFFERENCES FOUND',
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                '',
                len(compare.df1),
                len(compare.df2),
                'Yes' if len(compare.df1) == len(compare.df2) else 'No',
                '',
                len(compare.intersect_columns()),
                len(compare.df1_unq_columns()),
                len(compare.df2_unq_columns()),
                '',
                len(compare.df1_unq_rows),
                len(compare.df2_unq_rows),
                compare.count_matching_rows(),
                len(compare.all_mismatch()),
                '',
                f"{(compare.count_matching_rows() / max(len(compare.df1), 1) * 100):.2f}%",
                '',
                'power bi actual report',
                'data/downloads (CSV export)'
            ]
        }
    
    def save_all_reports(
        self, 
        results: Dict[str, datacompy.Compare],
        save_text: bool = True,
        save_excel: bool = True
    ):
        """
        Save reports for all comparison results
        
        Args:
            results: Dictionary of table_name -> datacompy.Compare
            save_text: Save text reports
            save_excel: Save Excel reports
        """
        print(f"\n{'='*80}")
        print(f"💾 SAVING REPORTS")
        print(f"{'='*80}\n")
        
        for table_name, compare in results.items():
            print(f"\n📁 {table_name}:")
            
            if save_text:
                self.save_text_report(compare, table_name)
            
            if save_excel:
                self.save_excel_report(compare, table_name)
        
        print(f"\n{'='*80}")
        print(f"✅ All reports saved to: {self.output_folder}")
        print(f"{'='*80}\n")
