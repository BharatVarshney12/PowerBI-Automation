"""
Data Profiling Utility
Generates Sweetviz and YData-Profiling reports
"""

import pandas as pd
import sweetviz as sv
from ydata_profiling import ProfileReport
from datetime import datetime
import os
import allure
from allure_commons.types import AttachmentType
from config.config import SWEETVIZ_DIR, YDATA_DIR, PROFILING_CONFIG


class DataProfiler:
 """Handles data profiling with Sweetviz and YData-Profiling"""
 
 def __init__(self, excel_path: str):
 self.excel_path = excel_path
 self.df = None
 self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
 
 def load_data(self):
 """Load Excel data into pandas DataFrame"""
 self.df = pd.read_excel(self.excel_path)
 print(f"[DATA] Loaded {len(self.df)} rows, {len(self.df.columns)} columns")
 return self
 
 def generate_sweetviz_report(self) -> str:
 """Generate Sweetviz analysis report"""
 if not PROFILING_CONFIG['sweetviz']['enabled']:
 print("[SWEETVIZ] Disabled in config")
 return None
 
 with allure.step('Generate Sweetviz Data Analysis Report'):
 try:
 print("\n[SWEETVIZ] Analyzing downloaded data...")
 
 if self.df is None:
 self.load_data()
 
 print(f"[SWEETVIZ] Loaded {len(self.df)} rows, {len(self.df.columns)} columns")
 
 # Generate Sweetviz report
 report = sv.analyze(self.df)
 
 # Save report
 os.makedirs(SWEETVIZ_DIR, exist_ok=True)
 sweetviz_filename = f"sweetviz_analysis_{self.timestamp}.html"
 sweetviz_path = os.path.join(SWEETVIZ_DIR, sweetviz_filename)
 
 report.show_html(sweetviz_path, open_browser=False)
 
 sweetviz_size = os.path.getsize(sweetviz_path)
 print(f"[SWEETVIZ] Analysis report generated!")
 print(f"[SWEETVIZ] Location: {sweetviz_path}")
 print(f"[SWEETVIZ] File size: {sweetviz_size} bytes")
 
 # Attach to Allure
 allure.attach(
 f'Sweetviz Report: {sweetviz_filename}\nPath: {sweetviz_path}\nSize: {sweetviz_size} bytes\nRows: {len(self.df)}\nColumns: {len(self.df.columns)}',
 'Sweetviz Analysis Details',
 AttachmentType.TEXT
 )
 
 with open(sweetviz_path, 'rb') as sv_file:
 allure.attach(sv_file.read(), sweetviz_filename, attachment_type='text/html', extension='.html')
 
 return sweetviz_path
 
 except Exception as e:
 print(f"[SWEETVIZ] Warning: Could not generate report - {e}")
 allure.attach(f'Sweetviz generation failed: {str(e)}', 'Sweetviz Warning', AttachmentType.TEXT)
 return None
 
 def generate_ydata_report(self) -> str:
 """Generate YData-Profiling report"""
 if not PROFILING_CONFIG['ydata']['enabled']:
 print("[YDATA] Disabled in config")
 return None
 
 with allure.step('Generate YData-Profiling Comprehensive Report'):
 try:
 print("\n[YDATA] Generating comprehensive data profile...")
 
 if self.df is None:
 self.load_data()
 
 # Create profiling report
 profile = ProfileReport(
 self.df,
 title=f"PowerBI Data Profile - {self.timestamp}",
 explorative=PROFILING_CONFIG['ydata']['explorative'],
 minimal=PROFILING_CONFIG['ydata']['minimal']
 )
 
 # Save report
 os.makedirs(YDATA_DIR, exist_ok=True)
 ydata_filename = f"ydata_profile_{self.timestamp}.html"
 ydata_path = os.path.join(YDATA_DIR, ydata_filename)
 
 profile.to_file(ydata_path)
 
 ydata_size = os.path.getsize(ydata_path)
 print(f"[YDATA] Profiling report generated!")
 print(f"[YDATA] Location: {ydata_path}")
 print(f"[YDATA] File size: {ydata_size} bytes")
 
 # Attach to Allure
 allure.attach(
 f'YData-Profiling Report: {ydata_filename}\nPath: {ydata_path}\nSize: {ydata_size} bytes\nRows: {len(self.df)}\nColumns: {len(self.df.columns)}\n\nReport includes:\n- Overview statistics\n- Variable analysis\n- Interactions\n- Correlations\n- Missing values\n- Sample data\n- Duplicate rows',
 'YData-Profiling Details',
 AttachmentType.TEXT
 )
 
 with open(ydata_path, 'rb') as ydata_file:
 allure.attach(ydata_file.read(), ydata_filename, attachment_type='text/html', extension='.html')
 
 print(f"[YDATA] Report attached to Allure successfully")
 
 return ydata_path
 
 except Exception as e:
 print(f"[YDATA] Warning: Could not generate report - {e}")
 allure.attach(f'YData-Profiling generation failed: {str(e)}', 'YData-Profiling Warning', AttachmentType.TEXT)
 return None
 
 def generate_all_reports(self):
 """Generate both Sweetviz and YData reports"""
 sweetviz_path = self.generate_sweetviz_report()
 ydata_path = self.generate_ydata_report()
 
 return {
 'sweetviz': sweetviz_path,
 'ydata': ydata_path
 }
