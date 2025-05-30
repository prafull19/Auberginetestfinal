import pytest
import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# --- IMPORTANT PATH ADJUSTMENT ---
# Calculate project_root relative to conftest.py's location.
# conftest.py is in 'SeleniumAutomationProject/tests/'
# We need to go up two levels to reach 'SeleniumAutomationProject/'
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import Config after sys.path is set
from config.config import Config


@pytest.fixture(scope="module")
def browser_setup():
    """
    Pytest fixture to set up and tear down the WebDriver.
    Yields the WebDriver instance to the tests.
    """
    options = Options()

    if Config.HEADLESS_MODE:
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--window-size=1920,1080")

    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument("--log-level=3")

    # Determine the correct chromedriver executable name based on OS
    driver_executable_name = "chromedriver.exe" if os.name == 'nt' else "chromedriver"

    # --- ADD DEBUG PRINT STATEMENTS HERE ---
    print(f"\n--- DEBUGGING PATH ---")
    print(f"Current script (__file__): {os.path.abspath(__file__)}")
    print(f"Calculated project_root: {project_root}")
    print(f"Expected driver_executable_name: {driver_executable_name}")
    # --- END DEBUG PRINT STATEMENTS ---

    # Use the 'project_root' calculated at the top of this conftest.py file
    driver_path = os.path.join(project_root, "drivers", driver_executable_name)

    print(f"Attempting to find Chromedriver at: {driver_path}") # More specific print
    print(f"Does the path exist? {os.path.exists(driver_path)}")
    print(f"Is it a file? {os.path.isfile(driver_path)}")


    if not os.path.exists(driver_path):
        pytest.fail(f"Chromedriver not found at: {driver_path}. Please download the compatible ChromeDriver and place it in the 'drivers' folder.")

    driver = None
    try:
        service = Service(executable_path=driver_path)
        driver = webdriver.Chrome(service=service, options=options)

        driver.set_page_load_timeout(Config.DEFAULT_WAIT_TIME)
        driver.implicitly_wait(Config.DEFAULT_WAIT_TIME)

        print("\nWebDriver initialized successfully.")
        yield driver
    except Exception as e:
        pytest.fail(f"Error initializing WebDriver: {e}")
    finally:
        if driver:
            driver.quit()
            print("WebDriver closed.")

@pytest.fixture(autouse=True)
def reset_browser_state(browser_setup):
    driver = browser_setup
    driver.get("about:blank")
    yield