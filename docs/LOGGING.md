# Logger Documentation

## Overview
The PowerBI Automation framework includes comprehensive logging functionality to track test execution, debug issues, and monitor performance.

## Features

### 1. **Dual Output**
- **Console**: INFO level and above (simplified format)
- **Log File**: DEBUG level and above (detailed format with timestamps, file locations, line numbers)

### 2. **Log Levels**
- **DEBUG**: Detailed diagnostic information
- **INFO**: General informational messages
- **WARNING**: Warning messages for potentially problematic situations
- **ERROR**: Error messages with optional exception tracebacks
- **CRITICAL**: Critical errors that may cause test failures

### 3. **Structured Logging**
The logger provides specialized methods for common test activities:

#### Test Lifecycle
```python
log_test_start("Test Name")  # Marks test start
log_test_end("Test Name", "PASSED")  # Marks test completion
```

#### Test Steps
```python
log_step("Navigate to Login Page")  # Logs a test step
```

#### Actions
```python
log_action("Click Button", "Submit")  # Logs an action with details
```

#### Verifications
```python
log_verification("Login Successful", True, "User authenticated")
log_verification("Element Visible", False, "Element not found")
```

#### Data Logging
```python
log_data("User Info", {
    "Username": "test@example.com",
    "Role": "Admin",
    "Login Time": "2025-10-29 20:00:00"
})
```

#### Performance Tracking
```python
log_performance("Page Load", 2.45)  # Logs operation duration in seconds
```

## Usage Examples

### Basic Usage
```python
from utils.logger import log_info, log_error, log_debug

log_debug("Debug message for troubleshooting")
log_info("Information message")
log_error("Error occurred", exc_info=True)  # Includes traceback
```

### Test Integration
```python
import time
from utils.logger import (
    log_test_start, log_test_end, log_step, 
    log_action, log_verification, log_performance
)

def test_example():
    test_name = "Example Test"
    log_test_start(test_name)
    start_time = time.time()
    
    try:
        log_step("Step 1: Login")
        log_action("Enter username", "test@example.com")
        log_action("Click login button")
        
        # Perform login...
        login_success = True
        log_verification("Login successful", login_success)
        
        duration = time.time() - start_time
        log_performance("Login", duration)
        
        log_test_end(test_name, "PASSED")
        
    except Exception as e:
        log_error(f"Test failed: {str(e)}", exc_info=True)
        log_test_end(test_name, "FAILED")
        raise
```

### Advanced Logger Usage
```python
from utils.logger import get_logger

# Get a named logger for a specific module
logger = get_logger("MyModule")

logger.info("Module-specific log message")
logger.debug("Detailed debug info")
logger.error("Error in module", exc_info=True)
```

## Log File Location

Log files are automatically created in the `logs/` directory with timestamp:
```
logs/powerbi_automation_20251029_200000.log
```

## Log File Format

### Console Output (Simple)
```
20:00:01 | INFO     | Logger initialized
20:00:02 | INFO     | TEST STARTED: PowerBI Login Test
20:00:03 | INFO     | STEP: Navigate to PowerBI
```

### File Output (Detailed)
```
2025-10-29 20:00:01 | INFO     | PowerBIAutomation | logger.py:75 | Logger initialized. Log file: logs/powerbi_automation_20251029_200000.log
2025-10-29 20:00:02 | INFO     | PowerBIAutomation | logger.py:125 | ================================================================================
2025-10-29 20:00:02 | INFO     | PowerBIAutomation | logger.py:126 | TEST STARTED: PowerBI Login Test
2025-10-29 20:00:03 | INFO     | PowerBIAutomation | logger.py:136 | STEP: Navigate to PowerBI
```

## Integration with Existing Tests

The logging is already integrated into:
1. **PowerBI Automation Tests** (`test_powerbi_automation.py`)
2. **Snowflake Validation Tests** (`test_snowflake_validation.py`)

## Benefits

1. **Debugging**: Detailed logs help identify issues quickly
2. **Performance Monitoring**: Track execution times for each operation
3. **Audit Trail**: Complete record of test execution
4. **Test Analysis**: Review logs to understand test behavior
5. **Troubleshooting**: Exception tracebacks with context

## Best Practices

1. **Use appropriate log levels**: DEBUG for detailed info, INFO for general flow
2. **Log test steps**: Make logs readable by clearly marking test phases
3. **Include context**: Add relevant details to log messages
4. **Performance logging**: Track timing for critical operations
5. **Structured data**: Use `log_data()` for complex information

## Configuration

The logger is configured in `utils/logger.py` and uses a singleton pattern. You can modify:
- Log levels
- Output format
- File naming convention
- Handler configuration

## Viewing Logs

### During Test Execution
Logs appear in the console in real-time during test execution.

### After Test Execution
1. Navigate to the `logs/` directory
2. Open the latest log file
3. Search for specific test names, errors, or timestamps

### Example Log Analysis
```bash
# Find all errors
grep "ERROR" logs/powerbi_automation_20251029_200000.log

# Find performance metrics
grep "PERFORMANCE" logs/powerbi_automation_20251029_200000.log

# Find specific test
grep "TEST STARTED: PowerBI Login" logs/powerbi_automation_20251029_200000.log
```

## Troubleshooting

### No log file created
- Check that `logs/` directory exists (auto-created)
- Verify write permissions

### Logs not appearing
- Check log level settings
- Ensure logger is imported correctly

### Too verbose logs
- Increase console handler level to WARNING
- Keep file handler at DEBUG for detailed records
