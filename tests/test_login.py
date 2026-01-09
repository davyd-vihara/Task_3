import allure
from pages.login_page import LoginPage
from pages.main_page import MainPage
from pages.profile_page import ProfilePage
from config.urls import Urls
from config.constants import Constants


@allure.feature("Вход в систему")
@allure.story("Функциональность входа")
class TestLogin:

    @allure.title("Успешный вход в систему")
    def test_successful_login(self, driver, registered_user):
        """Проверяет успешный вход в систему"""
        login_page = LoginPage(driver)
        login_page.open()

        with allure.step("Выполняем вход через метод login()"):
            login_page.login(registered_user["email"], registered_user["password"])

        main_page = MainPage(driver)

        with allure.step("Проверяем, что пользователь авторизован"):
            main_page.open()
            main_page.wait_for_page_load()
            main_page.wait_until_user_logged_in(timeout=Constants.TIMEOUT_MEDIUM)
            assert main_page.is_user_logged_in(), "Пользователь не авторизован после входа"
