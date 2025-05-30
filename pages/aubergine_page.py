from pages.base_page import BasePage
from locators.aubergine_locators import AubergineLocators
from config.config import Config
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException  # Ensure TimeoutException is imported
import time


class AuberginePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.locators = AubergineLocators

    def _dismiss_cookie_popup(self):
        """
        Attempts to find and click the cookie accept button based on provided outerHTML.
        This method is designed to be robust.
        """
        # Prioritize the "Accept" button first, then a generic "close" button
        cookie_accept_locators = [
            (By.ID, "hs-eu-confirmation-button"),  # Specific 'Accept' button from the provided HTML
            (By.ID, "hs-eu-close-button"),  # Specific 'Dismiss' button from the provided HTML
            (By.ID, "cn-accept-cookie"),  # Fallback from previous common locators
            (By.CSS_SELECTOR, ".cli_action_button.wt-cli-accept-btn"),  # Fallback from previous common locators
            (By.CSS_SELECTOR, "a.cky-btn.cky-btn-accept"),  # Fallback for Complianz type banners
            (By.XPATH, "//button[contains(., 'Accept') or contains(., 'Got it')]"),  # Generic text-based fallback
        ]

        print("Attempting to dismiss cookie consent popup...")
        for locator in cookie_accept_locators:
            try:
                # Use a short explicit wait for the cookie button itself to appear and be clickable
                accept_button = self.wait.until(EC.element_to_be_clickable(locator), timeout=5)

                # If found, click it. Using JavaScript click can sometimes be more reliable
                # if the element is covered by another transparent layer.
                try:
                    accept_button.click()
                except Exception:
                    self.execute_script("arguments[0].click();", accept_button)

                print(f"Cookie consent popup dismissed using locator: {locator}")
                time.sleep(1)  # Give a moment for the popup to disappear and page to settle
                return True  # Cookie dismissed successfully
            except TimeoutException:
                pass  # This locator didn't work, try the next one
            except Exception as e:
                print(f"Error clicking cookie button with {locator}: {e}")
                pass  # Continue to next locator if an unexpected error occurs during click

        print("No cookie consent popup found or could not be dismissed using known locators.")
        return False  # Cookie not dismissed

    def load(self):
        """Loads the Aubergine Solutions URL and dismisses cookie popup."""
        self.go_to_url(Config.AUBERGINE_URL)

        # --- IMPORTANT: Call the cookie dismissal method immediately after loading ---
        self._dismiss_cookie_popup()

        # --- ROBUST PAGE LOAD WAIT for Aubergine Homepage ---
        # 1. Wait for the page title to contain 'Aubergine Solutions'. This is usually very stable.
        self.wait.until(EC.title_contains("Aubergine Solutions"),
                        message=f"Page title does not contain 'Aubergine Solutions' on homepage. Actual: {self.driver.title}")
        print("Aubergine Solutions homepage title verified.")

        # 2. Wait for the 'Expertise' menu item to be clickable, as it's the first interaction point.
        # This confirms the main navigation is ready.
        self.wait.until(EC.element_to_be_clickable(self.locators.EXPERTISE_MENU_ITEM),
                        message="Expertise menu item not clickable after homepage load. Locator: " + str(
                            self.locators.EXPERTISE_MENU_ITEM))

        print("Aubergine Solutions homepage seems loaded and stable, Expertise menu is clickable.")

    def navigate_to_python_expertise(self):
        """
        Navigates to the Python Expertise page by hovering over 'Expertise'
        and clicking 'Python Development Company' submenu.
        """
        self.load()  # This now handles loading and initial stability, including cookies.

        expertise_menu = self.find_element(self.locators.EXPERTISE_MENU_ITEM)  # Should be quick as waited for in load()
        ActionChains(self.driver).move_to_element(expertise_menu).perform()
        print("Hovered over 'Expertise' menu.")

        # Ensure the submenu is visible AND clickable BEFORE clicking
        self.wait.until(EC.visibility_of_element_located(self.locators.PYTHON_SUBMENU_ITEM),
                        message="Python submenu did not become visible after hovering over Expertise.")

        self.wait.until(EC.element_to_be_clickable(self.locators.PYTHON_SUBMENU_ITEM),
                        message="Python submenu is visible but not clickable.")

        self.click_element(self.locators.PYTHON_SUBMENU_ITEM)
        print("Clicked on 'Python' submenu.")

        # Wait for URL and title to reflect navigation
        self.wait.until(EC.url_contains("/python-development-company"),
                        message="URL did not change to Python expertise page.")
        self.wait.until(EC.title_contains("Python"),
                        message="Page title did not contain 'Python' after navigation.")

    def get_first_image_element(self):
        return self.find_element(self.locators.FIRST_IMAGE_ON_PAGE)

    def is_carousel_displayed(self):
        return self.is_element_displayed(self.locators.CAROUSEL_CONTAINER)

    def open_talk_to_experts_link_in_new_tab(self):
        button = self.find_element(self.locators.TALK_TO_EXPERTS_BUTTON)
        self.execute_script("window.open(arguments[0].href, '_blank');", button)
        print("Opened 'Talk to our python experts now' button link in a new tab via JS.")