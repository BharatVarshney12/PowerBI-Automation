"""
Browser Manager
Handles browser initialization and configuration with session persistence
"""

from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page
from config.config import BROWSER_CONFIG
import allure
from allure_commons.types import AttachmentType
import os
from pathlib import Path


class BrowserManager:
 """Manages browser lifecycle with optional session persistence"""
 
 def __init__(self):
 self.playwright = None
 self.browser: Browser = None
 self.context: BrowserContext = None
 self.page: Page = None
 self.storage_state_path = Path(__file__).parent.parent / 'data' / 'auth_state.json'
 
 def launch_browser(self):
 """Launch browser with configured settings"""
 with allure.step('Launch Browser'):
 self.playwright = sync_playwright().start()
 
 browser_type = getattr(self.playwright, BROWSER_CONFIG['browser_type'])
 
 self.browser = browser_type.launch(
 headless=BROWSER_CONFIG['headless'],
 args=BROWSER_CONFIG['args']
 )
 
 print(f"[BROWSER] Launched {BROWSER_CONFIG['browser_type']} browser in maximized mode")
 allure.attach('Browser launched in maximized mode', 'Browser Setup', AttachmentType.TEXT)
 
 return self
 
 def create_context(self):
 """Create fresh browser context (always fresh login)"""
 with allure.step('Create Fresh Browser Context'):
 # Always create fresh context - no session persistence
 print("[BROWSER] Creating fresh session - fresh login required")
 allure.attach('Fresh session - always login', 'Context Setup', AttachmentType.TEXT)
 
 # Build context options
 context_options = {
 'accept_downloads': BROWSER_CONFIG['accept_downloads'],
 'ignore_https_errors': BROWSER_CONFIG['ignore_https_errors'],
 'no_viewport': True # Use full screen size
 }
 
 # Only add viewport if it's explicitly set (not None)
 if BROWSER_CONFIG.get('viewport'):
 context_options['viewport'] = BROWSER_CONFIG['viewport']
 context_options['no_viewport'] = False
 
 self.context = self.browser.new_context(**context_options)
 self.page = self.context.new_page()
 
 # Maximize the page
 self.page.set_viewport_size({'width': 1920, 'height': 1080})
 
 return self.page
 
 def save_session(self):
 """Save authentication session for reuse - DISABLED (always fresh login)"""
 # Session persistence is disabled - no saving
 print("[BROWSER] Session persistence disabled - will login fresh next time")
 allure.attach('Session not saved - fresh login always required', 'Session Persistence', AttachmentType.TEXT)
 
 def close(self):
 """Close browser and cleanup"""
 with allure.step('Close Browser'):
 if self.page:
 self.page.wait_for_timeout(3000)
 
 if self.browser:
 self.browser.close()
 print("[BROWSER] Browser closed")
 allure.attach('Browser closed successfully', 'Cleanup', AttachmentType.TEXT)
 
 if self.playwright:
 self.playwright.stop()
 
 def __enter__(self):
 """Context manager entry"""
 self.launch_browser()
 return self.create_context()
 
 def __exit__(self, exc_type, exc_val, exc_tb):
 """Context manager exit"""
 self.close()
