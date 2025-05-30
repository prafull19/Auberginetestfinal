from pages.base_page import BasePage
from locators.dnd_locators import DragAndDropLocators
from config.config import Config # Import correct for nested config
from selenium.webdriver.common.action_chains import ActionChains

class DragAndDropPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.locators = DragAndDropLocators

    def load(self):
        """Loads the drag and drop URL."""
        self.go_to_url(Config.DRAG_AND_DROP_URL)

    def drag_a_to_b(self):
        """
        Performs a drag and drop action from Column A to Column B.
        """
        column_a = self.find_element(self.locators.COLUMN_A)
        column_b = self.find_element(self.locators.COLUMN_B)
        actions = ActionChains(self.driver)
        # The drag_and_drop method directly drags one element to another
        actions.drag_and_drop(column_a, column_b).perform()
        print("Performed drag and drop of 'A' to 'B'.")

    def get_column_a_header_text(self):
        """Gets the text from Column A's header."""
        return self.get_element_text(self.locators.HEADER_A)

    def get_column_b_header_text(self):
        """Gets the text from Column B's header."""
        return self.get_element_text(self.locators.HEADER_B)