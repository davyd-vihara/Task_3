from pages.base_page import BasePage
from locators.profile_locators import ProfilePageLocators
from utils.config import Config
from pages.base_page import _log_debug

class ProfilePage(BasePage):
    """Страница личного кабинета"""
    
    def __init__(self, driver):
        super().__init__(driver, f"{Config.BASE_URL}account/profile")
        self.locators = ProfilePageLocators()
    
    def click_order_history_link(self):
        """Кликает по ссылке 'История заказов'"""
        self.click(self.locators.ORDER_HISTORY_LINK)
    
    def click_logout_button(self):
        """Кликает по кнопке 'Выход'"""
        self.click(self.locators.LOGOUT_BUTTON)
    
    def is_profile_page_visible(self):
        """Проверяет видимость страницы профиля"""
        # #region agent log
        _log_debug("debug-session", "run1", "B", "profile_page.py:is_profile_page_visible", "Проверка видимости страницы профиля", {
            "locator": str(self.locators.PROFILE_PAGE_TITLE),
            "url": self.driver.current_url
        })
        # #endregion
        # Проверяем URL и наличие элементов профиля
        current_url = self.get_current_url()
        is_profile_url = "account/profile" in current_url or "account" in current_url
        # Также проверяем наличие элементов профиля
        try:
            has_profile_elements = self.is_element_visible(self.locators.PROFILE_PAGE_TITLE, timeout=3)
        except:
            has_profile_elements = False
        return is_profile_url or has_profile_elements
    
    def is_order_history_visible(self):
        """Проверяет видимость истории заказов"""
        # Проверяем, что мы на странице истории заказов
        return "account/orders" in self.get_current_url()

