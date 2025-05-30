from pages.base_page import BasePage
from locators.upload_locators import UploadLocators
from config.config import Config
import os
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time


class UploadPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.locators = UploadLocators

    def load(self):
        """Loads the file upload URL and waits for the main page elements to be visible."""
        self.go_to_url(Config.UPLOAD_URL)

        # Add a short sleep for initial page rendering, especially in headless mode or on slow networks.
        # This is a temporary measure if other waits fail, usually indicative of deeper issues.
        time.sleep(1)

        # Wait for the main content div to be visible, as it encapsulates the whole page.
        # From your HTML: <div id="content" class="large-12 columns">
        self.wait.until(EC.visibility_of_element_located((By.ID, "content")),
                        message="Main content div (#content) not visible on upload page within default wait time.")

        # Now, wait for the specific 'File Uploader' heading (h3) to confirm the page is fully loaded and structured.
        # Using the locator defined in upload_locators.py (MAIN_HEADING)
        self.wait.until(EC.visibility_of_element_located(self.locators.MAIN_HEADING),
                        message="Main 'File Uploader' heading not visible on upload page within default wait time.")
        print("Upload page loaded successfully and 'File Uploader' heading is visible.")

    def upload_file_by_drag_drop_area(self, file_path):
        """
        Uploads a file by sending its path to the file input element.
        On the-internet.herokuapp.com, the 'drag and drop' area is directly linked
        to a hidden input field, so sending keys to that input is the mechanism.
        """
        # Ensure the file input element is present and interactive before sending keys
        file_input = self.wait.until(EC.presence_of_element_located(self.locators.FILE_INPUT),
                                     message="File input element not found within default wait time.")
        file_input.send_keys(file_path)
        print(f"File '{os.path.basename(file_path)}' sent to upload input.")
        # Give a small pause to allow the browser's JavaScript to process the upload
        # and display the file name in the preview area.
        time.sleep(1.5)  # Increased slightly for more reliability with JS updates.

    def get_displayed_file_name(self):
        """
        Waits for the uploaded file name to appear in the display element
        and returns its text.
        """
        # Wait until the dynamically created file display element is visible.
        self.wait.until(EC.visibility_of_element_located(self.locators.UPLOADED_FILES_DISPLAY),
                        message="Uploaded file name display element (.dz-filename [data-dz-name]) not visible within default wait time.")

        # Then, wait for the actual file name (Config.TEST_FILE_NAME) to be present in that element's text.
        self.wait.until(EC.text_to_be_present_in_element(self.locators.UPLOADED_FILES_DISPLAY, Config.TEST_FILE_NAME),
                        message=f"Expected filename '{Config.TEST_FILE_NAME}' not found in uploaded file display within default wait time.")

        # Once confirmed, get and return the text.
        return self.get_element_text(self.locators.UPLOADED_FILES_DISPLAY)

    def click_upload_button(self):
        """Clicks the 'Upload' button."""
        self.click_element(self.locators.UPLOAD_BUTTON)

    def get_upload_success_message(self):
        """
        Gets the text of the success message header after file upload.
        """
        # After clicking upload, the page navigates to a new URL with a success message.
        # This message is an H2 tag (e.g., "File Uploaded!").
        self.wait.until(EC.visibility_of_element_located(self.locators.SUCCESS_MESSAGE_HEADER),
                        message="Upload success message header not visible after navigation.")
        return self.get_element_text(self.locators.SUCCESS_MESSAGE_HEADER)