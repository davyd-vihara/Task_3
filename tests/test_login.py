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

        with allure.step("Проверяем, что открылась главная страница"):
            main_page.open()
            main_page.wait_for_page_load()
            # Проверяем URL через метод из Page Object
            current_url = main_page.get_current_url()
            assert Urls.BASE_URL.rstrip('/') in current_url or current_url.startswith(Urls.BASE_URL), \
                "Главная страница не открылась после входа"
            # Ждем авторизации через метод из Page Object
            main_page.wait_until_user_logged_in(timeout=Constants.TIMEOUT_MEDIUM)
            assert main_page.is_user_logged_in(), "Пользователь не авторизован после входа"
        
        with allure.step("Проверяем авторизацию через переход в личный кабинет"):
            main_page.click_personal_account_button()
            profile_page = ProfilePage(driver)
            # Ждем перехода на страницу профиля через метод из Page Object
            profile_page.wait_for_url_contains(Urls.PROFILE_PAGE, timeout=Constants.TIMEOUT_MEDIUM)
        
        assert profile_page.is_profile_page_visible(), "Страница профиля не открылась"
        assert profile_page.is_profile_button_visible(), \
            "Кнопка 'Профиль' не найдена в личном кабинете. Авторизация не прошла."
        assert profile_page.is_logout_button_visible(), \
            "Кнопка 'Выход' не найдена в личном кабинете. Авторизация не прошла."
