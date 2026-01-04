from pages.base_page import BasePage
from locators.profile_locators import ProfilePageLocators
from config.urls import Urls
from config.constants import Constants
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import allure

class ProfilePage(BasePage):
    """Страница личного кабинета"""
    
    def __init__(self, driver):
        super().__init__(driver, f"{Urls.BASE_URL}account/profile")
        self.locators = ProfilePageLocators()
    
    @allure.step("Кликнуть по ссылке 'История заказов'")
    def click_order_history_link(self):
        """Кликает по ссылке 'История заказов'"""
        self.click_by_js(self.locators.ORDER_HISTORY_LINK)
    
    @allure.step("Кликнуть по кнопке 'Выход'")
    def click_logout_button(self):
        """Кликает по кнопке 'Выход'"""
        self.click_by_js(self.locators.LOGOUT_BUTTON)
    
    @allure.step("Проверить видимость страницы профиля")
    def is_profile_page_visible(self):
        """Проверяет видимость страницы профиля"""
        current_url = self.get_current_url()
        is_profile_url = "account/profile" in current_url or "account" in current_url
        try:
            has_profile_elements = self.is_element_visible(self.locators.PROFILE_PAGE_TITLE, timeout=Constants.TIMEOUT_MODAL_LOAD)
        except (TimeoutException, NoSuchElementException):
            has_profile_elements = False
        return is_profile_url or has_profile_elements
    
    @allure.step("Проверить видимость истории заказов")
    def is_order_history_visible(self):
        """Проверяет видимость истории заказов"""
        # Проверяем, что мы на странице истории заказов
        return "account/orders" in self.get_current_url()
    
    @allure.step("Проверить наличие кнопки 'Профиль'")
    def is_profile_button_visible(self):
        """Проверяет наличие кнопки 'Профиль' в меню личного кабинета"""
        return self.is_element_visible(self.locators.PROFILE_BUTTON, timeout=Constants.TIMEOUT_DEFAULT)
    
    @allure.step("Проверить наличие кнопки 'Выход'")
    def is_logout_button_visible(self):
        """Проверяет наличие кнопки 'Выход' в меню личного кабинета"""
        return self.is_element_visible(self.locators.LOGOUT_BUTTON, timeout=Constants.TIMEOUT_DEFAULT)

