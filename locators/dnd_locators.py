from selenium.webdriver.common.by import By

class DragAndDropLocators:
    # The div element representing Column A
    COLUMN_A = (By.XPATH, "//div[@id='column-a']")

    # The div element representing Column B
    COLUMN_B = (By.XPATH, "//div[@id='column-b']")

    # The header element inside Column A (to verify text after drag)
    HEADER_A = (By.XPATH, "//div[@id='column-a']/header")

    # The header element inside Column B (to verify text after drag)
    HEADER_B = (By.XPATH, "//div[@id='column-b']/header")