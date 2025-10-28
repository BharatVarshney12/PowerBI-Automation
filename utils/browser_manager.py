"""
Browser Manager
Handles browser initialization and configuration
"""

from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page
from config.config import BROWSER_CONFIG
import allure
from allure_commons.types import AttachmentType


class BrowserManager:
    """Manages browser lifecycle"""
    
    def __init__(self):
        self.playwright = None
        self.browser: Browser = None
        self.context: BrowserContext = None
        self.page: Page = None
    
    def launch_browser(self):
        """Launch browser with configured settings"""
        with allure.step('Launch Browser in Incognito Mode'):
            self.playwright = sync_playwright().start()
            
            browser_type = getattr(self.playwright, BROWSER_CONFIG['browser_type'])
            
            self.browser = browser_type.launch(
                headless=BROWSER_CONFIG['headless'],
                args=BROWSER_CONFIG['args']
            )
            
            print(f"[BROWSER] Launched {BROWSER_CONFIG['browser_type']} browser")
            allure.attach('Browser launched in incognito mode', 'Browser Setup', AttachmentType.TEXT)
            
            return self
    
    def create_context(self):
        """Create fresh browser context"""
        with allure.step('Create Fresh Browser Context'):
            self.context = self.browser.new_context(
                accept_downloads=BROWSER_CONFIG['accept_downloads'],
                ignore_https_errors=BROWSER_CONFIG['ignore_https_errors'],
                viewport=BROWSER_CONFIG['viewport'],
                storage_state=None  # Fresh session, no cache
            )
            
            self.page = self.context.new_page()
            
            print("[BROWSER] Created fresh context with no cache")
            allure.attach('Fresh context created with no cache', 'Context Setup', AttachmentType.TEXT)
            
            return self.page
    
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
