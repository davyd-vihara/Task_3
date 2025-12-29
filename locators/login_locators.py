from selenium.webdriver.common.by import By

class LoginPageLocators:
    """Локаторы для страницы входа"""
    # Заголовок "Вход"
    LOGIN_TITLE = (By.XPATH, "//h2[contains(text(), 'Вход')] | //h1[contains(text(), 'Вход')]")
    EMAIL_INPUT = (By.XPATH, "//input[@name='name' and @type='text']")
    PASSWORD_INPUT = (By.XPATH, "//input[@name='Пароль' and @type='password']")
    LOGIN_BUTTON = (By.XPATH, "//button[contains(@class, 'button_button') and contains(text(), 'Войти')]")
    REGISTER_LINK = (By.XPATH, "//a[contains(@class, 'Auth_link') and contains(text(), 'Зарегистрироваться')]")
    RECOVER_PASSWORD_LINK = (By.XPATH, "//a[contains(@class, 'Auth_link') and contains(text(), 'Восстановить пароль')]")

