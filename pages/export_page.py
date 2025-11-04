"""
Export Page Object Model
Handles report export functionality
"""

from pages.base_page import BasePage
from config.config import SELECTORS, TIMEOUTS, DOWNLOADS_DIR
import allure
from datetime import datetime
import os


class ExportPage(BasePage):
    """Page Object for Report Export Operations"""
    
    def __init__(self, page):
        super().__init__(page)
        self.more_options_btn = SELECTORS['export']['more_options']
        self.export_data_item = SELECTORS['export']['export_data']
        self.export_type_role = SELECTORS['export']['export_type']
        self.export_type_name = SELECTORS['export']['export_type_name']
        self.export_button = SELECTORS['export']['export_button']
        self.grid_role = SELECTORS['dashboard']['grid']
        self.grid_text = SELECTORS['dashboard']['grid_text']
    
    def select_visual_grid(self):
        """Select the visual grid for export - click on white space"""
        with allure.step('Select Visual Grid'):
            print("\n[EXPORT] Starting report export process...")
            
            try:
                # Click on the interactive grid white space
                grid_selector = self.page.locator('div.interactive-grid.innerContainer')
                
                if grid_selector.count() > 0:
                    grid_selector.first.click()
                    print("[EXPORT] Clicked on grid visual (white space)")
                    self.wait(800)
                    
                    self.attach_text('Grid visual selected successfully', 'Visual Selection')
                    self.take_screenshot('Visual Selected')
                else:
                    self.take_screenshot('Grid Not Found')
                    raise Exception("Could not find interactive grid")
                    
            except Exception as e:
                self.take_screenshot('Grid Click Error')
                raise Exception(f"Failed to select grid: {str(e)}")
            
            return self
    
    def click_more_options(self):
        """Click more options button (three dots)"""
        with allure.step('Click More Options (Three Dots)'):
            print("[EXPORT] Waiting for 'More options' button (three dots)...")
            self.wait(1000)
            
            # Click on three dots icon
            more_options = self.page.locator('i.glyphicon.pbi-glyph-more.glyph-small')
            
            if more_options.count() > 0:
                more_options.first.click()
                print("[EXPORT] Clicked 'More options' button (three dots)")
                self.wait(1000)
                
                self.attach_text('More options menu opened', 'Menu Action')
                self.take_screenshot('More Options Menu')
            else:
                self.take_screenshot('More Options Not Found')
                raise Exception("More options button (three dots) not visible")
            
            return self
    
    def click_export_data(self):
        """Click export data menu item"""
        with allure.step('Click Export Data'):
            export_data = self.page.get_by_text('Export data', exact=True)
            
            if export_data.count() > 0:
                export_data.first.click()
                print("[EXPORT] Clicked 'Export data'")
                self.wait(2000)
                
                self.attach_text('Export data menu item clicked', 'Menu Action')
                self.take_screenshot('Export Dialog')
            else:
                self.take_screenshot('Export Menu Not Found')
                raise Exception("Export data menu item not visible")
            
            return self
    
    def select_export_type(self):
        """Select export type (Data with current layout)"""
        with allure.step('Select Export Type'):
            try:
                # Click on "Data with current layout" radio button
                layout_radio = self.page.locator("//label[@for='pbi-radio-button-3-input']//div[@class='pbi-radio-button-circle']")
                
                if layout_radio.count() > 0:
                    layout_radio.first.click()
                    print(f"[EXPORT] Selected 'Data with current layout'")
                    self.attach_text(f'Selected: Data with current layout', 'Export Type')
                else:
                    self.take_screenshot('Radio Button Not Found')
                    raise Exception("Could not find 'Data with current layout' radio button")
                
                self.wait(1000)
                self.take_screenshot('Export Type Selected')
                
            except Exception as e:
                self.take_screenshot('Export Type Selection Error')
                raise Exception(f"Failed to select export type: {str(e)}")
            
            return self
    
    def download_report(self) -> str:
        """Download the report file"""
        with allure.step('Download Report File'):
            os.makedirs(DOWNLOADS_DIR, exist_ok=True)
            
            # Click on Export button
            export_btn = self.page.get_by_role('button', name='Export')
            
            if export_btn.count() > 0:
                print("[EXPORT] Found export button")
                
                with self.page.expect_download(timeout=TIMEOUTS['download']) as download_info:
                    export_btn.first.click()
                    print("[EXPORT] Clicked 'Export' button")
                
                download = download_info.value
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                
                # Use unique filename with timestamp to avoid file locks
                original_filename = download.suggested_filename or "powerbi_export.xlsx"
                filename = f"powerbi_export_{timestamp}.xlsx"
                save_path = os.path.join(DOWNLOADS_DIR, filename)
                
                # Try to save, if file is locked, add retry logic
                max_retries = 3
                for attempt in range(max_retries):
                    try:
                        download.save_as(save_path)
                        break
                    except PermissionError:
                        if attempt < max_retries - 1:
                            print(f"[WARNING] File locked, retrying... (attempt {attempt + 1}/{max_retries})")
                            self.wait(1000)
                            # Try alternative filename
                            filename = f"powerbi_export_{timestamp}_{attempt + 1}.xlsx"
                            save_path = os.path.join(DOWNLOADS_DIR, filename)
                        else:
                            raise Exception(f"Cannot save file - it may be open in another program. Please close {filename} and try again.")
                
                file_size = os.path.getsize(save_path)
                
                print(f"\n[SUCCESS]  Report exported successfully!")
                print(f"[FILE] Location: {save_path}")
                print(f"[SIZE] File size: {file_size} bytes")
                
                # Attach download details to report
                self.attach_text(
                    f'File: {filename}\nPath: {save_path}\nSize: {file_size} bytes',
                    'Download Details'
                )
                
                # Attach file to Allure
                with open(save_path, 'rb') as f:
                    allure.attach(
                        f.read(),
                        filename,
                        attachment_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                        extension='.xlsx'
                    )
                
                return save_path
            else:
                self.take_screenshot('Export Button Not Visible')
                raise Exception("Export button not visible")
    
    def export_report(self) -> str:
        """Complete export flow"""
        with allure.step('Complete Report Export'):
            self.select_visual_grid()
            self.click_more_options()
            self.click_export_data()
            self.select_export_type()
            file_path = self.download_report()
            return file_path
