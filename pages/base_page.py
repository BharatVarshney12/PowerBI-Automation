"""
Base Page Object Model
Contains common methods used across all pages
"""

from playwright.sync_api import Page, expect
import allure
from allure_commons.types import AttachmentType
from typing import List, Optional
import time


class BasePage:
    """Base class for all page objects"""
    
    def __init__(self, page: Page):
        self.page = page
    
    def navigate(self, url: str, timeout: int = 60000):
        """Navigate to a URL"""
        with allure.step(f'Navigate to {url}'):
            self.page.goto(url, timeout=timeout)
            self.wait(3000)
            self.take_screenshot('Page Loaded')
    
    def fill_input(self, selector: str, text: str, description: str = ""):
        """Fill an input field"""
        step_name = description or f'Fill input: {selector}'
        with allure.step(step_name):
            self.page.fill(selector, text)
            print(f"[INPUT] Filled: {selector}")
            allure.attach(f'Filled: {selector}', 'Input Action', AttachmentType.TEXT)
    
    def click_element(self, selector: str, description: str = ""):
        """Click an element"""
        step_name = description or f'Click: {selector}'
        with allure.step(step_name):
            self.page.click(selector)
            print(f"[CLICK] Clicked: {selector}")
            allure.attach(f'Clicked: {selector}', 'Click Action', AttachmentType.TEXT)
    
    def wait_for_selector(self, selector: str, timeout: int = 30000, state: str = 'visible'):
        """Wait for selector to be in a specific state"""
        self.page.wait_for_selector(selector, timeout=timeout, state=state)
    
    def is_visible(self, selector: str, timeout: int = 5000) -> bool:
        """Check if element is visible"""
        try:
            return self.page.locator(selector).is_visible(timeout=timeout)
        except:
            return False
    
    def wait(self, milliseconds: int):
        """Wait for specified milliseconds"""
        self.page.wait_for_timeout(milliseconds)
    
    def wait_for_load_state(self, state: str = 'networkidle', timeout: int = 30000):
        """Wait for page load state"""
        try:
            self.page.wait_for_load_state(state, timeout=timeout)
        except:
            print(f"[WARNING] Load state '{state}' not reached within timeout")
    
    def get_current_url(self) -> str:
        """Get current page URL"""
        return self.page.url
    
    def take_screenshot(self, name: str = "Screenshot"):
        """Take and attach screenshot to Allure report"""
        screenshot = self.page.screenshot()
        allure.attach(screenshot, name, AttachmentType.PNG)
    
    def try_selectors(self, selectors: List[str], action: str = 'fill', value: str = None) -> bool:
        """Try multiple selectors until one works"""
        for selector in selectors:
            try:
                if self.is_visible(selector):
                    if action == 'fill' and value:
                        self.page.fill(selector, value)
                    elif action == 'click':
                        self.page.click(selector)
                    print(f"[SUCCESS] Used selector: {selector}")
                    return True
            except:
                continue
        return False
    
    def get_by_role(self, role: str, name: str = None):
        """Get element by role"""
        if name:
            return self.page.get_by_role(role, name=name)
        return self.page.get_by_role(role)
    
    def get_by_test_id(self, test_id: str):
        """Get element by test ID"""
        return self.page.get_by_test_id(test_id)
    
    def get_by_text(self, text: str):
        """Get element by text"""
        return self.page.get_by_text(text)
    
    def attach_text(self, text: str, name: str):
        """Attach text to Allure report"""
        allure.attach(text, name, AttachmentType.TEXT)
