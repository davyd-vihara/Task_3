from selenium.webdriver.common.by import By

class PasswordRecoveryPageLocators:
    """Локаторы для страницы восстановления пароля"""
    EMAIL_INPUT = (By.XPATH, "//input[@type='text' and contains(@class, 'input__textfield')]")
    RECOVER_BUTTON = (By.XPATH, "//button[contains(@class, 'button_button') and contains(text(), 'Восстановить')]")
    SHOW_PASSWORD_BUTTON = (By.XPATH, "//div[contains(@class, 'input__icon')]")
    PASSWORD_INPUT = (By.XPATH, "//input[@type='password' or @type='text'][contains(@class, 'input__textfield')]")
    # Поле ввода кода (появляется после ввода email и клика "Восстановить")
    # На странице reset-password есть label с текстом "Введите код из письма"
    CODE_INPUT = (By.XPATH, "//label[contains(@class, 'input_placeholder') and contains(text(), 'Введите код')]")
    RECOVERY_FORM = (By.XPATH, "//form[contains(@class, 'Auth_form')]")

