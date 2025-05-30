from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from config.config import Config  # Import the Config class from your config.py
import os


class DriverManager:
    _driver = None  # A class-level variable to store the single WebDriver instance (singleton pattern)

    @classmethod
    def get_driver(cls):
        """
        Initializes and returns a Chrome WebDriver instance.
        It uses a singleton pattern, meaning it will create the driver only once.
        Configures headless mode and suppresses logging based on settings in config.py.
        """
        if cls._driver is None:
            options = Options()

            # Configure headless mode if enabled in config.py
            if Config.HEADLESS_MODE:
                options.add_argument("--headless")
                options.add_argument("--disable-gpu")  # Recommended for headless on some OS
                options.add_argument("--no-sandbox")  # Necessary for some CI/CD environments
                options.add_argument("--window-size=1920,1080")  # Set a consistent window size for headless

            # Suppress "DevTools listening on ws://..." and other console logs
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            options.add_argument("--log-level=3")  # Suppress INFO/WARNING logs from ChromeDriver

            try:
                # Determine the correct chromedriver executable name based on OS
                driver_executable_name = "chromedriver.exe" if os.name == 'nt' else "chromedriver"
                # Construct the absolute path to the chromedriver executable
                driver_path = os.path.join(Config.PROJECT_ROOT, "drivers", driver_executable_name)

                # Check if the chromedriver exists at the specified path
                if not os.path.exists(driver_path):
                    raise FileNotFoundError(
                        f"Chromedriver not found at: {driver_path}. "
                        "Please download the compatible ChromeDriver and place it in the 'drivers' folder."
                    )

                # Initialize the Chrome WebDriver
                cls._driver = webdriver.Chrome(options=options)

                # Set page load timeout (time to wait for page to load)
                cls._driver.set_page_load_timeout(Config.DEFAULT_WAIT_TIME)

                # Set implicit wait (time to wait for an element to be present)
                # While explicit waits are preferred, implicit can be a fallback
                # for basic element presence checks.
                cls._driver.implicitly_wait(Config.DEFAULT_WAIT_TIME)

                print("WebDriver initialized successfully.")
            except Exception as e:
                print(f"Error initializing WebDriver: {e}")
                # Re-raise the exception to propagate the error up the call stack
                raise e
        return cls._driver

    @classmethod
    def quit_driver(cls):
        """
        Quits the WebDriver instance if it's running.
        Resets the _driver variable to None.
        """
        if cls._driver:
            cls._driver.quit()
            cls._driver = None
            print("WebDriver closed.")