"""
Centralized Logger Utility
Provides structured logging for PowerBI automation framework
"""

import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional


class PowerBILogger:
 """Custom logger for PowerBI automation"""
 
 _instance = None
 
 def __new__(cls):
 if cls._instance is None:
 cls._instance = super().__new__(cls)
 cls._instance._initialized = False
 return cls._instance
 
 def __init__(self):
 if self._initialized:
 return
 
 self._initialized = True
 self.logger = None
 self._setup_logger()
 
 def _setup_logger(self):
 """Setup logger with file and console handlers"""
 
 # Create logs directory
 log_dir = Path(__file__).parent.parent / 'logs'
 log_dir.mkdir(exist_ok=True)
 
 # Create logger
 self.logger = logging.getLogger('PowerBIAutomation')
 self.logger.setLevel(logging.DEBUG)
 
 # Remove existing handlers
 if self.logger.handlers:
 self.logger.handlers.clear()
 
 # Create formatters
 detailed_formatter = logging.Formatter(
 '%(asctime)s | %(levelname)-8s | %(name)s | %(filename)s:%(lineno)d | %(message)s',
 datefmt='%Y-%m-%d %H:%M:%S'
 )
 
 simple_formatter = logging.Formatter(
 '%(asctime)s | %(levelname)-8s | %(message)s',
 datefmt='%H:%M:%S'
 )
 
 # File Handler - Detailed logs with rotation
 timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
 log_file = log_dir / f'powerbi_automation_{timestamp}.log'
 
 file_handler = logging.FileHandler(log_file, encoding='utf-8')
 file_handler.setLevel(logging.DEBUG)
 file_handler.setFormatter(detailed_formatter)
 
 # Console Handler - Simple logs
 console_handler = logging.StreamHandler(sys.stdout)
 console_handler.setLevel(logging.INFO)
 console_handler.setFormatter(simple_formatter)
 
 # Add handlers
 self.logger.addHandler(file_handler)
 self.logger.addHandler(console_handler)
 
 self.logger.info(f"Logger initialized. Log file: {log_file}")
 
 def get_logger(self, name: Optional[str] = None) -> logging.Logger:
 """Get logger instance"""
 if name:
 return logging.getLogger(f'PowerBIAutomation.{name}')
 return self.logger
 
 def debug(self, message: str):
 """Log debug message"""
 self.logger.debug(message)
 
 def info(self, message: str):
 """Log info message"""
 self.logger.info(message)
 
 def warning(self, message: str):
 """Log warning message"""
 self.logger.warning(message)
 
 def error(self, message: str, exc_info: bool = False):
 """Log error message"""
 self.logger.error(message, exc_info=exc_info)
 
 def critical(self, message: str, exc_info: bool = False):
 """Log critical message"""
 self.logger.critical(message, exc_info=exc_info)
 
 def exception(self, message: str):
 """Log exception with traceback"""
 self.logger.exception(message)
 
 def log_test_start(self, test_name: str):
 """Log test start"""
 self.logger.info("=" * 80)
 self.logger.info(f"TEST STARTED: {test_name}")
 self.logger.info("=" * 80)
 
 def log_test_end(self, test_name: str, status: str):
 """Log test end"""
 self.logger.info("=" * 80)
 self.logger.info(f"TEST {status.upper()}: {test_name}")
 self.logger.info("=" * 80)
 
 def log_step(self, step_name: str):
 """Log test step"""
 self.logger.info(f"STEP: {step_name}")
 
 def log_action(self, action: str, details: str = ""):
 """Log action"""
 if details:
 self.logger.info(f"ACTION: {action} | {details}")
 else:
 self.logger.info(f"ACTION: {action}")
 
 def log_verification(self, item: str, status: bool, details: str = ""):
 """Log verification"""
 status_str = " PASS" if status else " FAIL"
 if details:
 self.logger.info(f"VERIFY: {item} | {status_str} | {details}")
 else:
 self.logger.info(f"VERIFY: {item} | {status_str}")
 
 def log_data(self, data_type: str, details: dict):
 """Log data details"""
 self.logger.info(f"DATA: {data_type}")
 for key, value in details.items():
 self.logger.info(f" - {key}: {value}")
 
 def log_performance(self, operation: str, duration: float):
 """Log performance metrics"""
 self.logger.info(f"PERFORMANCE: {operation} | Duration: {duration:.2f}s")


# Singleton instance
_logger_instance = PowerBILogger()


def get_logger(name: Optional[str] = None) -> logging.Logger:
 """
 Get logger instance
 
 Args:
 name: Optional logger name for sub-modules
 
 Returns:
 Logger instance
 """
 return _logger_instance.get_logger(name)


def log_debug(message: str):
 """Log debug message"""
 _logger_instance.debug(message)


def log_info(message: str):
 """Log info message"""
 _logger_instance.info(message)


def log_warning(message: str):
 """Log warning message"""
 _logger_instance.warning(message)


def log_error(message: str, exc_info: bool = False):
 """Log error message"""
 _logger_instance.error(message, exc_info=exc_info)


def log_critical(message: str, exc_info: bool = False):
 """Log critical message"""
 _logger_instance.critical(message, exc_info=exc_info)


def log_exception(message: str):
 """Log exception with traceback"""
 _logger_instance.exception(message)


def log_test_start(test_name: str):
 """Log test start"""
 _logger_instance.log_test_start(test_name)


def log_test_end(test_name: str, status: str):
 """Log test end"""
 _logger_instance.log_test_end(test_name, status)


def log_step(step_name: str):
 """Log test step"""
 _logger_instance.log_step(step_name)


def log_action(action: str, details: str = ""):
 """Log action"""
 _logger_instance.log_action(action, details)


def log_verification(item: str, status: bool, details: str = ""):
 """Log verification"""
 _logger_instance.log_verification(item, status, details)


def log_data(data_type: str, details: dict):
 """Log data details"""
 _logger_instance.log_data(data_type, details)


def log_performance(operation: str, duration: float):
 """Log performance metrics"""
 _logger_instance.log_performance(operation, duration)
