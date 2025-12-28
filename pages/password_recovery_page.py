from pages.base_page import BasePage
from locators.password_recovery_locators import PasswordRecoveryPageLocators
from utils.config import Config
from pages.base_page import _log_debug
from selenium.webdriver.common.by import By

class PasswordRecoveryPage(BasePage):
    """Страница восстановления пароля"""
    
    def __init__(self, driver):
        super().__init__(driver, f"{Config.BASE_URL}forgot-password")
        self.locators = PasswordRecoveryPageLocators()
    
    def input_email(self, email):
        """Вводит email для восстановления"""
        self.input_text(self.locators.EMAIL_INPUT, email)
    
    def click_recover_button(self):
        """Кликает по кнопке 'Восстановить'"""
        self.click(self.locators.RECOVER_BUTTON)
    
    def click_show_password_button(self):
        """Кликает по кнопке показать/скрыть пароль"""
        self.click(self.locators.SHOW_PASSWORD_BUTTON)
    
    def is_recovery_form_visible(self):
        """Проверяет видимость формы восстановления"""
        return self.is_element_visible(self.locators.RECOVERY_FORM)
    
    def is_code_input_visible(self):
        """Проверяет видимость поля ввода кода"""
        # #region agent log
        _log_debug("debug-session", "run1", "C", "password_recovery_page.py:is_code_input_visible", "Проверка видимости поля ввода кода", {
            "locator": str(self.locators.CODE_INPUT),
            "url": self.driver.current_url
        })
        # #endregion
        # Проверяем, что мы на странице reset-password
        current_url = self.get_current_url()
        if "reset-password" not in current_url:
            # #region agent log
            _log_debug("debug-session", "run1", "C", "password_recovery_page.py:is_code_input_visible", "Не на странице reset-password", {
                "current_url": current_url
            })
            # #endregion
            return False
        
        # Ищем label с текстом "Введите код"
        try:
            return self.is_element_visible(self.locators.CODE_INPUT, timeout=5)
        except:
            # Альтернативный поиск - ищем по тексту
            try:
                code_label = self.driver.find_element(By.XPATH, "//label[contains(text(), 'Введите код')]")
                return code_label.is_displayed()
            except:
                return False
    
    def is_password_field_highlighted(self):
        """Проверяет подсветку поля пароля"""
        try:
            password_field = self.find_visible_element(self.locators.PASSWORD_INPUT)
            # Проверяем наличие класса или стиля, указывающего на активное состояние
            classes = password_field.get_attribute("class")
            return "input_status_active" in classes or "input__status_active" in classes
        except:
            return False
    
    def get_password_field_type(self):
        """Получает тип поля пароля (password или text)"""
        password_field = self.find_element(self.locators.PASSWORD_INPUT)
        return password_field.get_attribute("type")

