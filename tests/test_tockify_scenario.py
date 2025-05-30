import sys
import os
import pytest
import time  # Used for small delays for UI stability, consider replacing with explicit waits if flakiness occurs

# Adjust sys.path to enable imports from the project root.
# This ensures that modules like 'pages.tockify_page' and 'config.config' can be found.
# The path goes up two levels from 'SeleniumAutomationProject/tests/' to 'SeleniumAutomationProject/'.
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import the necessary Page Object and Config class
from pages.tockify_page import TockifyPage
from config.config import Config  # Import Config from config/config.py


# The 'browser_setup' fixture is defined in tests/conftest.py and automatically discovered by pytest.
def test_scenario_4_tockify_calendar(browser_setup):
    """
    Test Scenario 4: Tockify Calendar Interaction
    1. Hit the URL-https://tockify.com/
    2. Select “28 Feb 2040” from the calendar displayed.
    3. Verify the date displayed as ‘28/02/40’ in the calendar using assertion.
    4. Select the ‘Monthly’ tab.
    5. Verify the calendar grid and title of the page displayed using assertion.
    6. Close the browser. (Handled by Pytest fixture)
    """
    driver = browser_setup  # Get the WebDriver instance from the Pytest fixture
    page = TockifyPage(driver)

    print("\n--- Running Test Scenario 4: Tockify Calendar ---")

    # 1. Hit the URL-https://tockify.com/ and switch to calendar iframe
    # The load_and_switch_to_calendar_iframe method handles navigation and iframe switching.
    page.load_and_switch_to_calendar_iframe()

    # 2. Select “28 Feb 2040” from the calendar displayed.
    target_day = 28
    target_month_num = 2  # February is the 2nd month
    target_year = 2040
    page.select_date_from_calendar(target_day, target_month_num, target_year)
    time.sleep(1)  # Small delay to allow date selection to visually reflect on the page

    # 3. Verify the date displayed as ‘28/02/40’ in the calendar using assertion.
    # The get_selected_date_display method will switch back to iframe, get text, then switch to default content.
    displayed_date_text = page.get_selected_date_display()
    assert displayed_date_text == Config.TOCKIFY_EXPECTED_DATE_FORMAT, \
        f"Displayed date mismatch. Expected: '{Config.TOCKIFY_EXPECTED_DATE_FORMAT}', Actual: '{displayed_date_text}'"
    print(f"Verification: Date '{displayed_date_text}' displayed as expected.")

    # 4. Select the ‘Monthly’ tab.
    # The select_monthly_tab method handles switching to iframe, clicking, then switching back.
    page.select_monthly_tab()
    time.sleep(1)  # Small delay to allow view to change to monthly grid

    # 5. Verify the calendar grid and title of the page displayed using assertion.
    # The is_calendar_grid_displayed method handles switching to iframe, checking, then switching back.
    assert page.is_calendar_grid_displayed(), \
        "Calendar grid is not displayed in monthly view."
    print("Verification: Calendar grid is displayed in monthly view.")

    # Verify the title of the main page (driver is currently in default content after previous step)
    assert Config.TOCKIFY_CALENDAR_TITLE_PART in driver.title, \
        f"Page title '{driver.title}' does not contain '{Config.TOCKIFY_CALENDAR_TITLE_PART}'."
    print(f"Verification: Page title '{driver.title}' contains '{Config.TOCKIFY_CALENDAR_TITLE_PART}'.")

    print("Test Scenario 4 Completed Successfully.")

    # 6. Close the browser. (Handled automatically by the 'browser_setup' fixture's teardown in conftest.py)