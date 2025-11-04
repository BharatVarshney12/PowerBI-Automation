"""
Login Page Object Model
Handles Microsoft/PowerBI authentication
"""

from pages.base_page import BasePage
from config.config import SELECTORS, TIMEOUTS
import allure
from allure_commons.types import AttachmentType


class LoginPage(BasePage):
 """Page Object for Login/Authentication"""
 
 def __init__(self, page):
 super().__init__(page)
 self.email_selectors = SELECTORS['email']['input']
 self.email_submit = SELECTORS['email']['submit']
 self.password_input = SELECTORS['password']['input']
 self.password_submit = SELECTORS['password']['submit']
 
 def enter_email(self, email: str):
 """Enter email address"""
 with allure.step('Enter Email Address'):
 email_filled = False
 
 for selector in self.email_selectors:
 try:
 if self.is_visible(selector, timeout=5000):
 self.fill_input(selector, email, f'Fill email using: {selector}')
 email_filled = True
 break
 except:
 continue
 
 if not email_filled:
 self.take_screenshot('Email Field Not Found')
 raise Exception("Could not find email field")
 
 self.take_screenshot('Email Entered')
 return self
 
 def click_email_submit(self):
 """Click email submit button"""
 with allure.step('Click Submit Button'):
 self.wait(1000)
 self.click_element(self.email_submit, 'Click Email Submit')
 self.attach_text('Submit button clicked successfully', 'Submit Action')
 return self
 
 def wait_for_redirect(self):
 """Wait for Microsoft login redirect"""
 with allure.step('Wait for Microsoft Login Redirect'):
 self.wait_for_load_state("networkidle", timeout=TIMEOUTS['navigation'])
 self.wait(3000)
 redirect_url = self.get_current_url()
 print(f"[INFO] Redirected to: {redirect_url}")
 self.attach_text(redirect_url, 'Redirect URL')
 self.take_screenshot('Microsoft Login Page')
 return self
 
 def enter_password(self, password: str):
 """Enter password"""
 with allure.step('Enter Password'):
 self.wait_for_load_state("networkidle", timeout=TIMEOUTS['navigation'])
 self.wait(2000)
 
 # Wait for password field and fill
 self.wait_for_selector(self.password_input, timeout=10000)
 self.fill_input(self.password_input, password, 'Enter Password')
 
 print("[AUTH] Password entered")
 self.attach_text('Password entered successfully', 'Password Entry')
 self.take_screenshot('Password Entered')
 return self
 
 def click_sign_in(self):
 """Click sign in button"""
 with allure.step('Click Sign In'):
 self.wait(1000)
 self.click_element(self.password_submit, 'Click Sign In Button')
 self.attach_text('Sign in button clicked', 'Sign In Action')
 return self
 
 def handle_stay_signed_in(self):
 """Handle 'Stay signed in' prompt if appears"""
 with allure.step('Handle "Stay Signed In" Prompt'):
 self.wait(3000)
 try:
 if self.get_by_text("Stay signed in?").is_visible(timeout=5000):
 self.click_element('input[type="submit"]', 'Click Yes on Stay Signed In')
 print("[AUTH] Clicked 'Yes' on stay signed in prompt")
 self.attach_text('Clicked Yes on Stay signed in', 'Prompt Handling')
 else:
 self.attach_text('No Stay signed in prompt found', 'Prompt Handling')
 except:
 print("[AUTH] No 'Stay signed in' prompt")
 pass
 
 self.wait(2000)
 return self
 
 def login(self, email: str, password: str):
 """Complete login flow"""
 with allure.step('Complete Login Flow'):
 self.enter_email(email)
 self.click_email_submit()
 self.wait_for_redirect()
 self.enter_password(password)
 self.click_sign_in()
 self.handle_stay_signed_in()
 return self
