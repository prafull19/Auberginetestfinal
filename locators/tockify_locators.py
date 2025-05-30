from selenium.webdriver.common.by import By

class TockifyLocators:
    # --- CORRECTED IFRAME LOCATOR ---
    # The iframe containing the Tockify calendar
    # Using By.NAME is very reliable for iframes.
    # Alternatively, By.CSS_SELECTOR, 'iframe[name="tkf-client-window-embed-1"]'
    CALENDAR_IFRAME = (By.NAME, "tkf-client-window-embed-1")

    # --- CORRECTED LOADING SPINNER LOCATOR ---
    # The loading spinner that appears while the calendar content loads
    # Based on the outerHTML: <div class="spinner spinner__double-circles ng-hide">
    LOADING_SPINNER = (By.CSS_SELECTOR, ".spinner.spinner__double-circles")

    # The button/element to click to open the month/year date picker
    MONTH_YEAR_NAV = (By.CSS_SELECTOR, ".tic-nav-month-year")

    # The container for the date picker (month/year selection overlay)
    DATE_PICKER_CONTAINER = (By.CSS_SELECTOR, ".tic-month-picker.tic-show")

    # The element displaying the current year in the date picker
    YEAR_DISPLAY = (By.CSS_SELECTOR, ".tic-year-display")

    # The arrow to navigate to the next year in the date picker
    NEXT_YEAR_ARROW = (By.CSS_SELECTOR, ".tic-year-arrow.tic-next")

    # A template for month buttons in the date picker (format with month number 1-12)
    # Example: "button.tic-month-btn[data-month='2']" for February
    MONTH_BUTTON_TEMPLATE = "button.tic-month-btn[data-month='{}']"

    # A template for day buttons in the date picker (format with day number)
    # Example: "//div[contains(@class, 'tic-day') and normalize-space(text())='28']" for day 28
    DAY_BUTTON_TEMPLATE = (By.XPATH, "//div[contains(@class, 'tic-day') and normalize-space(text())='{}']")

    # The element displaying the selected date or current view's date in the calendar header
    DATE_DISPLAY = (By.CSS_SELECTOR, ".tic-date-display")

    # The "Monthly" view tab button
    MONTHLY_TAB = (By.CSS_SELECTOR, "button[data-view='month']")

    # The main grid container for the calendar when in monthly view
    CALENDAR_GRID = (By.CSS_SELECTOR, ".tic-grid-view")