import allure
from pages.login_page import LoginPage
from pages.password_recovery_page import PasswordRecoveryPage
from config.urls import Urls
from config.constants import Constants

@allure.feature("Восстановление пароля")
@allure.story("Функциональность восстановления пароля")
class TestPasswordRecovery:
    
    @allure.title("Переход на страницу восстановления пароля")
    def test_go_to_password_recovery(self, driver):
        """Проверяет переход на страницу восстановления пароля"""
        login_page = LoginPage(driver)
        
        with allure.step("Открываем страницу входа"):
            login_page.open()
        
        with allure.step("Кликаем по ссылке 'Восстановить пароль'"):
            login_page.click_recover_password_link()
        
        with allure.step("Проверяем, что открылась страница восстановления пароля"):
            recovery_page = PasswordRecoveryPage(driver)
            assert Urls.FORGOT_PASSWORD_PAGE in recovery_page.get_current_url(), "Страница восстановления пароля не открылась"
    
    @allure.title("Ввод почты для восстановления пароля")
    def test_input_email_for_recovery(self, driver, registered_user):
        """Проверяет ввод почты и клик по кнопке восстановления"""
        recovery_page = PasswordRecoveryPage(driver)
        
        with allure.step("Открываем страницу восстановления пароля"):
            recovery_page.open()
        
        test_email = registered_user["email"]
        
        with allure.step("Вводим email и кликаем по кнопке 'Восстановить'"):
            recovery_page.input_email(test_email)
            recovery_page.click_recover_button()
            recovery_page.wait_for_url_contains("/reset-password", timeout=Constants.TIMEOUT_MEDIUM)
        
        with allure.step("Проверяем, что открылась страница ввода кода"):
            assert Urls.RESET_PASSWORD_PAGE in recovery_page.get_current_url(), "Страница ввода кода не открылась"
    
    @allure.title("Показать/скрыть пароль подсвечивает поле")
    def test_password_visibility_toggle(self, driver, registered_user):
        """Проверяет подсветку поля при клике на иконку глаза"""
        recovery_page = PasswordRecoveryPage(driver)
        
        with allure.step("Открываем страницу восстановления пароля"):
            recovery_page.open()
        
        test_email = registered_user["email"]
        
        with allure.step("Вводим email и переходим на страницу ввода нового пароля"):
            recovery_page.input_email(test_email)
            recovery_page.click_recover_button()
            recovery_page.wait_for_url_contains("/reset-password", timeout=Constants.TIMEOUT_MEDIUM)
        
        with allure.step("Кликаем на иконку показать/скрыть пароль"):
            recovery_page.click_show_password_button()
        
        with allure.step("Проверяем, что поле пароля подсвечено или тип поля изменился на text"):
            is_highlighted = recovery_page.is_password_field_highlighted()
            field_type = recovery_page.get_password_field_type()
            assert is_highlighted or field_type == "text", \
                "Поле пароля не подсвечено после клика на иконку"

