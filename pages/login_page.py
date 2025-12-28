from pages.base_page import BasePage
from locators.login_locators import LoginPageLocators
from utils.config import Config

class LoginPage(BasePage):
    """Страница входа"""
    
    def __init__(self, driver):
        super().__init__(driver, f"{Config.BASE_URL}login")
        self.locators = LoginPageLocators()
    
    def input_email(self, email):
        """Вводит email"""
        self.input_text(self.locators.EMAIL_INPUT, email)
    
    def input_password(self, password):
        """Вводит пароль"""
        self.input_text(self.locators.PASSWORD_INPUT, password)
    
    def click_login_button(self):
        """Кликает по кнопке входа"""
        self.click(self.locators.LOGIN_BUTTON)
    
    def click_recover_password_link(self):
        """Кликает по ссылке восстановления пароля"""
        self.click(self.locators.RECOVER_PASSWORD_LINK)
    
    def login(self, email, password):
        """Выполняет вход"""
        self.input_email(email)
        self.input_password(password)
        self.click_login_button()
    
    def is_login_form_visible(self):
        """Проверяет видимость формы входа"""
        return self.is_element_visible(self.locators.LOGIN_BUTTON)

