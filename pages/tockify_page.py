from pages.base_page import BasePage
from locators.tockify_locators import TockifyLocators
from config.config import Config
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time


class TockifyPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.locators = TockifyLocators

    def load(self):
        """Loads the Tockify URL."""
        self.go_to_url(Config.TOCKIFY_URL)
        # Wait for the main page title to be present
        self.wait.until(EC.title_contains("Tockify"),
                        message=f"Page title does not contain 'Tockify' on main page. Actual: {self.driver.title}")
        print("Tockify main page seems loaded and title verified.")

    def switch_to_calendar_iframe(self):
        """Switches to the Tockify calendar iframe."""
        # Wait for the iframe to be present and switch to it
        self.wait.until(EC.frame_to_be_available_and_switch_to_it(self.locators.CALENDAR_IFRAME),
                        message="Tockify calendar iframe not available or could not be switched to.")
        print("Switched to Tockify calendar iframe.")

        # Wait for the loading spinner inside the iframe to become invisible
        try:
            self.wait.until(EC.invisibility_of_element_located(self.locators.IFRAME_LOADING_SPINNER),
                            message="Tockify iframe loading spinner did not become invisible.")
            print("Waited for element ('css selector', '.spinner.spinner__double-circles') to become invisible.")
        except Exception as e:
            # This catch is for cases where the spinner might not always appear or disappear quickly
            print(f"Warning: Spinner invisibility check failed or timed out: {e}. Proceeding anyway.")

        # --- CRITICAL CHANGE: INCREASED SLEEP AFTER SPINNER DISAPPEARS ---
        # Give more time for the calendar UI to fully render after the spinner is gone.
        time.sleep(10)  # Increased from 1 second to 2 seconds for added stability.

    def load_and_switch_to_calendar_iframe(self):
        """Loads the main Tockify page and then switches to the calendar iframe."""
        self.load()
        self.switch_to_calendar_iframe()

        # After switching and waiting for spinner, ensure a core calendar element is visible.
        self.wait.until(EC.visibility_of_element_located(self.locators.MONTH_YEAR_NAV),
                        message='Calendar navigation inside iframe not visible after loading.')
        print("Calendar navigation element inside iframe is visible.")

    def select_date(self, target_date_str):
        """
        Selects a date on the calendar.
        target_date_str example: "28 Feb 2040"
        """
        # Parse the target date
        from datetime import datetime
        target_date = datetime.strptime(target_date_str, "%d %b %Y")

        # Navigate to the correct month and year first
        # It's better to get the text, parse it, and then check against target_date.
        # Adding a loop to robustly read the month/year
        max_attempts = 10  # Prevent infinite loops for far-off dates
        attempts = 0
        while attempts < max_attempts:
            try:
                current_month_year_text = self.wait.until(
                    EC.visibility_of_element_located(self.locators.MONTH_YEAR_NAV)
                ).text.strip()
                current_month_year = datetime.strptime(current_month_year_text, "%B %Y")
                break
            except Exception as e:
                time.sleep(0.5)  # Wait a bit if element not visible immediately
                attempts += 1
        if attempts == max_attempts:
            raise TimeoutError("Could not get current month/year text from calendar navigation.")

        # Navigate to future/past months if needed
        while current_month_year.year < target_date.year or \
                (current_month_year.year == target_date.year and current_month_year.month < target_date.month):
            self.click_element(self.locators.NEXT_MONTH_BUTTON)
            time.sleep(0.5)  # Give UI time to update
            current_month_year_text = self.get_element_text(self.locators.MONTH_YEAR_NAV)
            current_month_year = datetime.strptime(current_month_year_text, "%B %Y")
            print(f"Navigated to: {current_month_year_text}")

        while current_month_year.year > target_date.year or \
                (current_month_year.year == target_date.year and current_month_year.month > target_date.month):
            self.click_element(self.locators.PREV_MONTH_BUTTON)
            time.sleep(0.5)  # Give UI time to update
            current_month_year_text = self.get_element_text(self.locators.MONTH_YEAR_NAV)
            current_month_year = datetime.strptime(current_month_year_text, "%B %Y")
            print(f"Navigated to: {current_month_year_text}")

        # Click the day
        day_locator = (By.XPATH, self.locators.DAY_IN_CALENDAR_XPATH_TEMPLATE.format(day=target_date.day))
        self.wait.until(EC.element_to_be_clickable(day_locator),
                        message=f"Date '{target_date.day}' not clickable.")
        self.click_element(day_locator)
        print(f"Selected date: {target_date_str}")
        time.sleep(1)  # Small pause after clicking a date for event details to load.

    def get_selected_date_display(self):
        """
        Gets the text of the displayed selected date (e.g., '28/02/40').
        This is usually in the event details view.
        """
        # Wait for the event details to appear after selecting a date.
        self.wait.until(EC.visibility_of_element_located(self.locators.EVENT_DATE_DISPLAY),
                        message="Event date display element not visible after selecting date.")

        return self.get_element_text(self.locators.EVENT_DATE_DISPLAY)

    def click_monthly_tab(self):
        """Clicks the 'Monthly' tab."""
        self.click_element(self.locators.MONTHLY_TAB)
        # Wait for the monthly view to load, e.g., by waiting for the calendar grid to be visible again
        self.wait.until(EC.visibility_of_element_located(self.locators.CALENDAR_GRID),
                        message="Calendar grid not visible after switching to Monthly tab.")
        print("Clicked 'Monthly' tab and calendar grid is visible.")

    def is_calendar_grid_displayed(self):
        """Checks if the main calendar grid is displayed."""
        return self.is_element_displayed(self.locators.CALENDAR_GRID)

    def get_page_title(self):
        """Gets the title of the current page."""
        return self.driver.title

    def get_calendar_title(self):
        """Gets the title displayed on the calendar itself (e.g., "Demo Calendar")."""
        self.wait.until(EC.visibility_of_element_located(self.locators.CALENDAR_TITLE_DISPLAY),
                        message="Calendar title display element not visible.")
        return self.get_element_text(self.locators.CALENDAR_TITLE_DISPLAY)