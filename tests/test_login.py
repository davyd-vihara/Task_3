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
            # Используем метод login(), который содержит логику ожидания авторизации
            login_page.login(registered_user["email"], registered_user["password"])

        main_page = MainPage(driver)

        with allure.step("Проверяем, что открылась главная страница"):
            # Ждем загрузки главной страницы через expected_conditions
            main_page.open()
            main_page.wait_for_page_load()
            wait = WebDriverWait(driver, Constants.TIMEOUT_MEDIUM)
            wait.until(lambda d: Urls.BASE_URL.rstrip('/') in d.current_url or d.current_url.startswith(Urls.BASE_URL))
            assert Urls.BASE_URL.rstrip('/') in driver.current_url or driver.current_url.startswith(Urls.BASE_URL), \
                "Главная страница не открылась после входа"
        
        with allure.step("Проверяем, что пользователь авторизован"):
            # Проверяем авторизацию через наличие кнопки "Оформить заказ" или отсутствие кнопки "Войти в аккаунт"
            wait = WebDriverWait(driver, Constants.TIMEOUT_MEDIUM)
            wait.until(lambda d: main_page.is_user_logged_in())
            assert main_page.is_user_logged_in(), "Пользователь не авторизован после входа"
        
        with allure.step("Проверяем авторизацию через переход в личный кабинет"):
            # Кликаем на кнопку "Личный кабинет"
            main_page.click_personal_account_button()
            
            # Ждем загрузки страницы профиля через expected_conditions
            profile_page = ProfilePage(driver)
            # Ожидаем изменения URL на страницу профиля
            wait = WebDriverWait(driver, Constants.TIMEOUT_MEDIUM)
            wait.until(lambda d: Urls.PROFILE_PAGE in d.current_url or "account" in d.current_url)
            
            # Проверяем, что открылась страница профиля
            assert profile_page.is_profile_page_visible(), "Страница профиля не открылась"
            
            # Проверяем наличие кнопки "Профиль"
            assert profile_page.is_profile_button_visible(), \
                "Кнопка 'Профиль' не найдена в личном кабинете. Авторизация не прошла."
            
            # Проверяем наличие кнопки "Выход"
            assert profile_page.is_logout_button_visible(), \
                "Кнопка 'Выход' не найдена в личном кабинете. Авторизация не прошла."
