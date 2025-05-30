from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from config.config import Config # Import Config for default wait time

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, Config.DEFAULT_WAIT_TIME)

    def go_to_url(self, url):
        """Navigates the browser to the specified URL."""
        self.driver.get(url)
        print(f"Navigated to URL: {url}")

    def find_element(self, locator):
        """
        Waits for and finds a single element using its locator.
        Raises NoSuchElementException if the element is not found within the default wait time.
        """
        try:
            # EC.presence_of_element_located ensures the element is in the DOM
            return self.wait.until(EC.presence_of_element_located(locator),
                                  message=f"Element not found using {locator} within {Config.DEFAULT_WAIT_TIME} seconds.")
        except TimeoutException:
            raise NoSuchElementException(f"Element not found after {Config.DEFAULT_WAIT_TIME} seconds: {locator}")

    def click_element(self, locator):
        """
        Waits for an element to be clickable and then clicks it.
        """
        element = self.wait.until(EC.element_to_be_clickable(locator),
                                  message=f"Element not clickable using {locator} within {Config.DEFAULT_WAIT_TIME} seconds.")
        element.click()
        print(f"Clicked element: {locator}")

    def type_into_element(self, locator, text):
        """
        Finds an element, clears its content, and then sends text to it.
        """
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
        print(f"Typed '{text}' into element: {locator}")

    def get_element_text(self, locator):
        """
        Finds an element and returns its visible text, stripped of leading/trailing whitespace.
        """
        element = self.find_element(locator)
        return element.text.strip()

    def is_element_displayed(self, locator):
        """
        Checks if an element is present in the DOM and visible on the page.
        Returns True if displayed, False otherwise.
        """
        try:
            # EC.visibility_of_element_located ensures it's in DOM and visible
            element = self.wait.until(EC.visibility_of_element_located(locator),
                                     message=f"Element {locator} is not visible.")
            return element.is_displayed()
        except (TimeoutException, NoSuchElementException):
            return False # Element not found or not visible

    def execute_script(self, script, *args):
        """
        Executes JavaScript in the browser.
        """
        return self.driver.execute_script(script, *args)

    def switch_to_new_tab(self):
        """
        Waits for a new tab to open and switches WebDriver focus to it.
        Assumes there will be exactly two windows after the new tab opens.
        """
        self.wait.until(EC.number_of_windows_to_be(2))
        # Find the handle of the new tab (which is not the current one)
        new_tab_handle = [handle for handle in self.driver.window_handles if handle != self.driver.current_window_handle][0]
        self.driver.switch_to.window(new_tab_handle)
        print("Switched to new tab.")

    def switch_to_main_tab(self):
        """
        Switches WebDriver focus back to the first (main) browser tab/window.
        """
        main_tab_handle = self.driver.window_handles[0]
        self.driver.switch_to.window(main_tab_handle)
        print("Switched back to main tab.")

    def wait_for_invisibility(self, locator):
        """
        Waits for an element to become invisible or not present in the DOM.
        Useful for waiting for loading spinners to disappear.
        """
        self.wait.until(EC.invisibility_of_element_located(locator))
        print(f"Waited for element {locator} to become invisible.")