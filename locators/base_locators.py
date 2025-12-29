from selenium.webdriver.common.by import By

class BaseLocators:
    """Базовые локаторы, общие для всех страниц"""
    MODAL = (By.CLASS_NAME, "Modal_modal__")
    MODAL_CLOSE_BUTTON = (By.XPATH, "//button[contains(@class, 'Modal_modal__close')]")


