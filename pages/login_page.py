from pages.base_page import BasePage
from locators.login_locators import LoginPageLocators
from config.urls import Urls
from config.constants import Constants
import allure
from selenium.webdriver.support import expected_conditions as EC

class LoginPage(BasePage):
    """Страница входа"""
    
    def __init__(self, driver):
        super().__init__(driver, f"{Urls.BASE_URL}{Urls.LOGIN_PAGE.lstrip('/')}")
        self.locators = LoginPageLocators()
    
    @allure.step("Ввести email")
    def input_email(self, email):
        """Вводит email"""
        self.input_text(self.locators.EMAIL_INPUT, email)
    
    @allure.step("Ввести пароль")
    def input_password(self, password):
        """Вводит пароль"""
        self.input_text(self.locators.PASSWORD_INPUT, password)
    
    @allure.step("Кликнуть по кнопке входа")
    def click_login_button(self):
        """Кликает по кнопке входа"""
        self.click_by_js(self.locators.LOGIN_BUTTON)
    
    @allure.step("Кликнуть по ссылке восстановления пароля")
    def click_recover_password_link(self):
        """Кликает по ссылке восстановления пароля"""
        self.click_by_js(self.locators.RECOVER_PASSWORD_LINK)
    
    @allure.step("Выполнить вход")
    def login(self, email, password):
        """Выполняет вход"""
        # Проверяем, что мы на странице логина
        current_url = self.get_current_url()
        if "/login" not in current_url:
            self.open()
        
        # Вводим данные
        self.input_email(email)
        self.input_password(password)
        
        # Сохраняем текущий URL перед кликом
        url_before = self.get_current_url()
        
        # Кликаем по кнопке входа
        self.click_login_button()
        
        # Ждем перехода на главную страницу после успешного входа
        wait = self.get_wait(Constants.TIMEOUT_LONG)
        
        # Ждем, пока URL изменится (уйдет со страницы логина)
        # Используем expected_conditions для проверки изменения URL
        try:
            # Проверяем, что URL изменился (не равен исходному) через явное ожидание
            wait.until(lambda d: d.current_url != url_before)
        except Exception:
            # Если не перешли, проверяем, что хотя бы URL не содержит "/login"
            try:
                wait.until(EC.not_(EC.url_contains("/login")))
            except Exception:
                url_after = self.get_current_url()
                if url_before == url_after:
                    raise Exception(
                        f"Авторизация не прошла. URL не изменился. "
                        f"Было: {url_before}, Стало: {url_after}. "
                        f"Возможно, неверные данные: email={email}"
                    )
        
        # Ждем сохранения токена в cookies/localStorage через проверку наличия токена
        try:
            wait.until(lambda d: self.execute_script("return localStorage.getItem('accessToken') || document.cookie.includes('token')"))
        except Exception:
            # Если токен не найден, это не критично - продолжаем
            pass
    
    @allure.step("Проверить видимость формы входа")
    def is_login_form_visible(self):
        """Проверяет видимость формы входа"""
        return self.is_element_visible(self.locators.LOGIN_BUTTON)
    
    @allure.step("Проверить наличие заголовка 'Вход'")
    def is_login_title_visible(self):
        """Проверяет наличие заголовка 'Вход'"""
        return self.is_element_visible(self.locators.LOGIN_TITLE, timeout=Constants.TIMEOUT_DEFAULT)
    
    @allure.step("Проверить доступность полей входа")
    def are_login_fields_available(self):
        """Проверяет доступность полей email и пароля"""
        email_visible = self.is_element_visible(self.locators.EMAIL_INPUT, timeout=Constants.TIMEOUT_DEFAULT)
        password_visible = self.is_element_visible(self.locators.PASSWORD_INPUT, timeout=Constants.TIMEOUT_DEFAULT)
        return email_visible and password_visible


