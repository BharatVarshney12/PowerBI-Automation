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
        """Select the visual grid for export"""
        with allure.step('Select Visual Grid'):
            print("\n[EXPORT] Starting report export process...")
            
            try:
                # Try to find specific grid with text
                grid_selector = self.get_by_role(self.grid_role).filter(has_text=self.grid_text)
                
                if grid_selector.count() > 0:
                    grid_selector.click()
                    print("[EXPORT] Clicked on grid visual (first click)")
                    self.wait(1000)
                    
                    grid_selector.click()
                    print("[EXPORT] Clicked grid visual again (second click)")
                    self.wait(1500)
                    
                    self.attach_text('Grid visual selected successfully', 'Visual Selection')
                    self.take_screenshot('Visual Selected')
                else:
                    # Fallback to first available grid
                    self.get_by_role(self.grid_role).first.click()
                    self.wait(1000)
                    self.get_by_role(self.grid_role).first.click()
                    self.wait(1500)
                    self.attach_text('First available grid selected', 'Visual Selection')
                    
            except Exception as e:
                self.take_screenshot('Grid Click Error')
                raise Exception(f"Failed to select grid: {str(e)}")
            
            return self
    
    def click_more_options(self):
        """Click more options button"""
        with allure.step('Click More Options'):
            more_options = self.get_by_test_id('visual-more-options-btn')
            
            if more_options.is_visible(timeout=5000):
                more_options.click()
                print("[EXPORT] Clicked 'More options' button")
                self.wait(2000)
                
                self.attach_text('More options menu opened', 'Menu Action')
                self.take_screenshot('More Options Menu')
            else:
                self.take_screenshot('More Options Not Found')
                raise Exception("More options button not visible")
            
            return self
    
    def click_export_data(self):
        """Click export data menu item"""
        with allure.step('Click Export Data'):
            export_data = self.get_by_test_id('pbimenu-item.Export data')
            
            if export_data.is_visible(timeout=5000):
                export_data.click()
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
                layout_radio = self.get_by_role(self.export_type_role, name=self.export_type_name)
                
                if layout_radio.is_visible(timeout=3000):
                    layout_radio.click()
                    print(f"[EXPORT] Selected '{self.export_type_name}'")
                    self.attach_text(f'Selected: {self.export_type_name}', 'Export Type')
                else:
                    # Fallback to first radio option
                    self.page.locator('.exportTypeRadioButtonIcon').first.click()
                    self.attach_text('Selected: First export type option', 'Export Type')
                
                self.wait(1000)
                self.take_screenshot('Export Type Selected')
                
            except Exception as e:
                self.attach_text(f'Using default export type: {str(e)}', 'Export Type')
            
            return self
    
    def download_report(self) -> str:
        """Download the report file"""
        with allure.step('Download Report File'):
            os.makedirs(DOWNLOADS_DIR, exist_ok=True)
            
            export_btn = self.get_by_test_id('export-btn')
            
            if export_btn.is_visible(timeout=5000):
                print("[EXPORT] Found export button")
                
                with self.page.expect_download(timeout=TIMEOUTS['download']) as download_info:
                    export_btn.click()
                    print("[EXPORT] Clicked 'Export' button")
                
                download = download_info.value
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = download.suggested_filename or f"powerbi_export_{timestamp}.xlsx"
                save_path = os.path.join(DOWNLOADS_DIR, filename)
                
                download.save_as(save_path)
                
                file_size = os.path.getsize(save_path)
                
                print(f"\n[SUCCESS] ✅ Report exported successfully!")
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
