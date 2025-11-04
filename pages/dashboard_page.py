"""
PowerBI Dashboard Page Object Model
Handles dashboard interactions and navigation
"""

from pages.base_page import BasePage
from config.config import SELECTORS, TIMEOUTS
import allure


class DashboardPage(BasePage):
 """Page Object for PowerBI Dashboard"""
 
 def __init__(self, page):
 super().__init__(page)
 self.grid_role = SELECTORS['dashboard']['grid']
 self.grid_text = SELECTORS['dashboard']['grid_text']
 
 def wait_for_dashboard(self):
 """Wait for PowerBI dashboard to load"""
 with allure.step('Wait for PowerBI Dashboard to Load'):
 print("[INFO] Waiting for PowerBI dashboard to load...")
 self.wait(8000) # Keep 8s to handle prompts
 
 # Check multiple times for redirect to PowerBI
 max_attempts = 10
 for i in range(max_attempts):
 dashboard_url = self.get_current_url()
 if "app.powerbi.com/groups" in dashboard_url:
 break
 print(f"[INFO] Waiting for PowerBI... ({i+1}/{max_attempts})")
 self.wait(2000)
 
 dashboard_url = self.get_current_url()
 print(f"[INFO] Current URL: {dashboard_url}")
 
 if "app.powerbi.com/groups" in dashboard_url:
 print("[SUCCESS] Successfully loaded PowerBI dashboard!")
 self.attach_text(dashboard_url, 'Dashboard URL')
 self.take_screenshot('PowerBI Dashboard Loaded')
 else:
 raise Exception(f"Did not reach PowerBI dashboard. Current URL: {dashboard_url}")
 
 try:
 self.wait_for_load_state("networkidle", timeout=30000) # Reduced from 60s to 30s
 self.attach_text('Dashboard fully loaded', 'Dashboard Status')
 except:
 self.attach_text('Dashboard loaded with some pending requests', 'Dashboard Status')
 
 self.wait(2000) # Wait for interactions to be ready
 print("[INFO] Dashboard ready for interaction")
 return self
 
 def verify_dashboard_loaded(self) -> bool:
 """Verify if dashboard is loaded"""
 current_url = self.get_current_url()
 return "app.powerbi.com/groups" in current_url
