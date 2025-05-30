import os

# Get the absolute path to the directory containing this config.py file
# Then navigate up one level to get the project root.
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Config:
    # URLs for each test scenario
    UPLOAD_URL = "https://the-internet.herokuapp.com/upload"
    DRAG_AND_DROP_URL = "https://the-internet.herokuapp.com/drag_and_drop" # <-- ENSURE THIS LINE IS PRESENT AND CORRECT
    AUBERGINE_URL = "https://auberginesolutions.com/"
    TOCKIFY_URL = "https://tockify.com/"

    # Browser settings
    HEADLESS_MODE = False
    DEFAULT_WAIT_TIME = 10

    # Test data paths
    TEST_FILE_NAME = "test_file.pdf"
    TEST_FILE_PATH = os.path.join(PROJECT_ROOT, TEST_FILE_NAME)

    # Expected values for assertions
    # AUBERGINE_PYTHON_TITLE = "Python | Aubergine Solutions"
    TOCKIFY_EXPECTED_DATE_FORMAT = "28/02/40"
    TOCKIFY_CALENDAR_TITLE_PART = "Tockify"