from selenium.webdriver.common.by import By

class AubergineLocators:
    # The "Expertise" menu item, which has children (sub-menus)
    EXPERTISE_MENU_ITEM = (By.CSS_SELECTOR, "li.menu-item-has-children > a[href*='/expertise']")

    # The "Python Development Company" submenu item under Expertise
    PYTHON_SUBMENU_ITEM = (By.CSS_SELECTOR, "li.menu-item-has-children a[href*='/python-development-company']")

    # The first image found within the main content area of the page
    FIRST_IMAGE_ON_PAGE = (By.CSS_SELECTOR, ".entry-content img:first-of-type")

    # The container for the Owl Carousel (check if it's displayed)
    CAROUSEL_CONTAINER = (By.CSS_SELECTOR, ".owl-carousel.wp-block-aubergine-owl-carousel")

    # The "Talk to our python experts now" button link
    TALK_TO_EXPERTS_BUTTON = (By.CSS_SELECTOR, "a.wp-block-button__link[href*='contact']")