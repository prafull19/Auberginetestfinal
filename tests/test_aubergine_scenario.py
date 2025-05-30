import sys
import os
import pytest
import time # Used for small delays where necessary for UI stability

# Adjust sys.path to enable imports from the project root.
# This ensures that modules like 'pages.aubergine_page' and 'config.config' can be found.
# The path goes up two levels from 'SeleniumAutomationProject/tests/' to 'SeleniumAutomationProject/'.
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import the necessary Page Object and Config class
from pages.aubergine_page import AuberginePage
from config.config import Config # Import Config from config/config.py


# The 'browser_setup' fixture is defined in tests/conftest.py and automatically discovered by pytest.
def test_scenario_3_aubergine_solutions(browser_setup):
    """
    Test Scenario 3: Aubergine Solutions Navigation
    1. Hit the URL- https://auberginesolutions.com/
    2. Navigate to expertise > python.
    3. Verify the first image present on the page is displayed using assertion.
    4. Verify the carousel displayed.
    5. Open “Talk to our python experts now” button link in the new tab.
    6. Switch to the main tab.
    7. Close the browser. (Handled by Pytest fixture)
    """
    driver = browser_setup # Get the WebDriver instance from the Pytest fixture
    page = AuberginePage(driver)

    print("\n--- Running Test Scenario 3: Aubergine Solutions ---")

    # 1. Hit the URL & 2. Navigate to expertise > python.
    # The navigate_to_python_expertise method in AuberginePage handles loading the URL.
    page.navigate_to_python_expertise()

    # Verify that the page title contains "Python"
    # This acts as an assertion for successful navigation to the Python expertise page.
    assert "Python" in driver.title, \
        f"Page title does not contain 'Python' after navigation. Actual title: {driver.title}"
    print(f"Navigated to Python expertise page. Title: {driver.title}")

    # 3. Verify the first image present on the page is displayed using assertion.
    first_image_element = page.get_first_image_element()
    assert first_image_element.is_displayed(), \
        "First image on Python expertise page is not displayed."
    print("Verification: First image on page is displayed.")

    # 4. Verify the carousel displayed.
    # This method checks for visibility based on its locator
    assert page.is_carousel_displayed(), \
        "Carousel element is not displayed on the Python expertise page."
    print("Verification: Carousel is displayed.")

    # 5. Open “Talk to our python experts now” button link in the new tab.
    # We store the main window handle before opening a new tab
    main_window_handle = driver.current_window_handle
    page.open_talk_to_experts_link_in_new_tab()
    time.sleep(2) # Give a short delay for the new tab to fully open and load content

    # Switch to the newly opened tab
    page.switch_to_new_tab()
    # Verify that the URL of the new tab contains "contact"
    assert "contact" in driver.current_url, \
        f"New tab URL does not contain 'contact'. Actual URL: {driver.current_url}"
    print(f"Switched to new tab. Current URL: {driver.current_url}")

    # 6. Switch back to the main tab.
    page.switch_to_main_tab()
    # Verify that we are back on the original Python expertise page by checking its URL.
    # The URL should still contain "/python-development-company/"
    assert "/python-development-company/" in driver.current_url, \
        f"Did not switch back to original Python page URL. Actual URL: {driver.current_url}"
    print(f"Switched back to main tab. Current URL: {driver.current_url}")

    print("Test Scenario 3 Completed Successfully.")

    # 7. Close the browser. (Handled by the 'browser_setup' fixture's teardown in conftest.py)