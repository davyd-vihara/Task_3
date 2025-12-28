from pages.base_page import BasePage
from locators.constructor_locators import ConstructorPageLocators
from locators.main_locators import MainPageLocators
from utils.config import Config

class ConstructorPage(BasePage):
    """Страница конструктора"""
    
    def __init__(self, driver):
        super().__init__(driver, Config.BASE_URL)
        self.locators = MainPageLocators()
        self.constructor_locators = ConstructorPageLocators()
    
    def is_constructor_visible(self):
        """Проверяет видимость конструктора"""
        return self.is_element_visible(self.constructor_locators.CONSTRUCTOR_TITLE)

