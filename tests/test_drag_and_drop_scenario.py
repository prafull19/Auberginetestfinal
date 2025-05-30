import sys
import os
import pytest
import time # For time.sleep

# Adjust sys.path to import modules from the project root
# This assumes the test file is at SeleniumAutomationProject/tests/test_drag_and_drop_scenario.py
# So, we need to go up two directories (../..) to reach SeleniumAutomationProject/
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from pages.drag_and_drop_page import DragAndDropPage
from config.config import Config # Import Config from config/config.py

# The 'browser_setup' fixture is defined in tests/conftest.py and automatically discovered by pytest.
def test_scenario_2_drag_and_drop(browser_setup):
    """
    Test Scenario 2: Drag and Drop 'A' and 'B' using XPATH locators.
    1. Hit the URL - https://the-internet.herokuapp.com/drag_and_drop
    2. Switch the position of ‘A’ and ‘B’ using the offset method.
    3. Verify using assertion.
    4. Close the browser. (Handled by Pytest fixture)
    """
    driver = browser_setup # Get the WebDriver instance from the Pytest fixture
    page = DragAndDropPage(driver)

    print("\n--- Running Test Scenario 2: Drag and Drop ---")

    # 1. Hit the URL - https://the-internet.herokuapp.com/drag_and_drop
    page.load()

    # Verify initial positions before drag and drop
    initial_header_a = page.get_column_a_header_text()
    initial_header_b = page.get_column_b_header_text()
    assert initial_header_a == "A", f"Initial Column A header expected 'A', but was '{initial_header_a}'"
    assert initial_header_b == "B", f"Initial Column B header expected 'B', but was '{initial_header_b}'"
    print(f"Initial positions verified: Column A: '{initial_header_a}', Column B: '{initial_header_b}'")

    # 2. Switch the position of ‘A’ and ‘B’ using the offset method.
    # Selenium's `ActionChains.drag_and_drop(source_element, target_element)`
    # implicitly uses offsets to drop the source element at the center of the target element.
    page.drag_a_to_b()
    time.sleep(1) # Small pause to allow the UI to visually update after drag-and-drop

    # 3. Verify using assertion.
    # After dragging A to B, Column A should now contain 'B' and Column B should contain 'A'.
    final_header_a = page.get_column_a_header_text()
    final_header_b = page.get_column_b_header_text()
    assert final_header_a == "B", f"After drag and drop, Column A header expected 'B', but was '{final_header_a}'"
    assert final_header_b == "A", f"After drag and drop, Column B header expected 'A', but was '{final_header_b}'"
    print(f"Final positions verified: Column A: '{final_header_a}', Column B: '{final_header_b}'")

    print("Test Scenario 2 Completed Successfully.")

    # 4. Close the browser. (Handled by the 'browser_setup' fixture's teardown)