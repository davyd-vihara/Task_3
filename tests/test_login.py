import allure
from pages.login_page import LoginPage
from pages.main_page import MainPage
from pages.profile_page import ProfilePage
from config.urls import Urls
from config.constants import Constants
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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

        with allure.step("Проверяем, что открылась главная страница"):
            main_page.open()
            main_page.wait_for_page_load()
            wait = WebDriverWait(driver, Constants.TIMEOUT_MEDIUM)
            wait.until(lambda d: Urls.BASE_URL.rstrip('/') in d.current_url or d.current_url.startswith(Urls.BASE_URL))
        
        assert Urls.BASE_URL.rstrip('/') in driver.current_url or driver.current_url.startswith(Urls.BASE_URL), \
            "Главная страница не открылась после входа"
        wait = WebDriverWait(driver, Constants.TIMEOUT_MEDIUM)
        wait.until(lambda d: main_page.is_user_logged_in())
        assert main_page.is_user_logged_in(), "Пользователь не авторизован после входа"
        
        with allure.step("Проверяем авторизацию через переход в личный кабинет"):
            main_page.click_personal_account_button()
            profile_page = ProfilePage(driver)
            wait = WebDriverWait(driver, Constants.TIMEOUT_MEDIUM)
            wait.until(lambda d: Urls.PROFILE_PAGE in d.current_url or "account" in d.current_url)
        
        assert profile_page.is_profile_page_visible(), "Страница профиля не открылась"
        assert profile_page.is_profile_button_visible(), \
            "Кнопка 'Профиль' не найдена в личном кабинете. Авторизация не прошла."
        assert profile_page.is_logout_button_visible(), \
            "Кнопка 'Выход' не найдена в личном кабинете. Авторизация не прошла."
