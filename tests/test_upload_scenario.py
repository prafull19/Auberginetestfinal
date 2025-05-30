import sys
import os
import pytest
import time

# Adjust sys.path to enable imports from the project root.
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from pages.upload_page import UploadPage
from config.config import Config


def test_scenario_1_file_upload(browser_setup):
    """
    Test Scenario 1: File Upload (CSS Selectors)
    1. Hit the URL- https://the-internet.herokuapp.com/upload
    2. Drag and drop the pdf file to upload in the area.
    3. Verify the name of the pdf file displayed using Assertions.
    4. Click on the upload button.
    5. Verify the file uploaded message displayed using Assertions.
    6. Close the browser. (Handled by Pytest fixture)
    """
    driver = browser_setup  # Get the driver instance from the fixture
    page = UploadPage(driver)

    print("\n--- Running Test Scenario 1: File Upload ---")

    # Pre-check: Ensure the dummy file exists
    full_file_path = Config.TEST_FILE_PATH
    if not os.path.exists(full_file_path):
        pytest.fail(
            f"Test file not found: {full_file_path}. Please create '{Config.TEST_FILE_NAME}' in your project root.")

    print(f"Attempting to upload file from: {full_file_path}")

    # 1. Hit the URL
    page.load()  # This is where the TimeoutException is occurring

    # 2. Drag and drop the pdf file to upload in the area (using send_keys to file input)
    page.upload_file_by_drag_drop_area(full_file_path)

    # 3. Verify the name of the pdf file displayed using Assertions.
    displayed_file_name = page.get_displayed_file_name()
    assert Config.TEST_FILE_NAME in displayed_file_name, \
        f"Displayed file name '{displayed_file_name}' does not contain expected file name '{Config.TEST_FILE_NAME}'"
    print(f"Verification: File name '{displayed_file_name}' displayed as expected.")

    # 4. Click on the upload button.
    page.click_upload_button()

    # 5. Verify the file uploaded message displayed using Assertions.
    success_message = page.get_upload_success_message()
    assert "File Uploaded!" in success_message, \
        f"Success message expected 'File Uploaded!', but got '{success_message}'"
    print(f"Verification: Success message '{success_message}' displayed as expected.")

    print("Test Scenario 1 Completed Successfully.")

    # 6. Close the browser. (Handled by the 'browser_setup' fixture's teardown)