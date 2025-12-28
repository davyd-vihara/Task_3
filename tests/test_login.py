import allure
import time
from pages.login_page import LoginPage
from pages.main_page import MainPage


@allure.feature("Вход в систему")
@allure.story("Функциональность входа")
class TestLogin:

    @allure.title("Успешный вход в систему")
    def test_successful_login(self, driver, registered_user):
        """Проверяет успешный вход в систему"""
        login_page = LoginPage(driver)
        login_page.open()

        with allure.step("Вводим учетные данные"):
            login_page.input_email(registered_user["email"])
            login_page.input_password(registered_user["password"])

        with allure.step("Кликаем по кнопке входа"):
            login_page.click_login_button()

        main_page = MainPage(driver)

        with allure.step("Проверяем, что открылась главная страница"):
            # Ждем загрузки главной страницы
            time.sleep(2)
            assert main_page.is_element_visible(
                main_page.locators.CONSTRUCTOR_BUTTON
            ), "Главная страница не открылась после входа"
