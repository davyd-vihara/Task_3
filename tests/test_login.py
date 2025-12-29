import allure
import time
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

        with allure.step("Вводим учетные данные"):
            login_page.input_email(registered_user["email"])
            login_page.input_password(registered_user["password"])

        with allure.step("Кликаем по кнопке входа"):
            login_page.click_login_button()

        main_page = MainPage(driver)

        with allure.step("Проверяем, что открылась главная страница"):
            # Ждем загрузки главной страницы
            time.sleep(Constants.TIMEOUT_SHORT)
            main_page.open()
            main_page.wait_for_page_load()
            assert Urls.BASE_URL.rstrip('/') in driver.current_url or driver.current_url.startswith(Urls.BASE_URL), \
                "Главная страница не открылась после входа"
        
        with allure.step("Проверяем авторизацию через переход в личный кабинет"):
            # Кликаем на кнопку "Личный кабинет"
            main_page.click_personal_account_button()
            
            # Ждем загрузки страницы профиля
            time.sleep(Constants.TIMEOUT_SHORT)
            
            # Проверяем, что открылась страница профиля
            profile_page = ProfilePage(driver)
            assert profile_page.is_profile_page_visible(), "Страница профиля не открылась"
            
            # Проверяем наличие кнопки "Профиль"
            assert profile_page.is_profile_button_visible(), \
                "Кнопка 'Профиль' не найдена в личном кабинете. Авторизация не прошла."
            
            # Проверяем наличие кнопки "Выход"
            assert profile_page.is_logout_button_visible(), \
                "Кнопка 'Выход' не найдена в личном кабинете. Авторизация не прошла."
