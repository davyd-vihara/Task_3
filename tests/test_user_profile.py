import allure
from pages.profile_page import ProfilePage
from pages.login_page import LoginPage
from config.urls import Urls
from config.constants import Constants


@allure.feature("Личный кабинет")
@allure.story("Функциональность личного кабинета")
class TestUserProfile:
    
    @allure.title("Переход по клику на 'Личный кабинет'")
    def test_go_to_personal_account(self, driver, logged_in_user):
        """Проверяет переход по клику на 'Личный кабинет'"""
        main_page = logged_in_user["main_page"]
        
        with allure.step("Кликаем по кнопке 'Личный кабинет'"):
            main_page.click_personal_account_button()
        
        with allure.step("Проверяем, что открылась страница профиля"):
            profile_page = ProfilePage(driver)
            assert Urls.PROFILE_PAGE in profile_page.get_current_url(), "Страница профиля не открылась"
    
    @allure.title("Переход в раздел 'История заказов'")
    def test_go_to_order_history(self, driver, logged_in_user):
        """Проверяет переход в раздел 'История заказов'"""
        main_page = logged_in_user["main_page"]
        
        with allure.step("Переходим в личный кабинет"):
            main_page.click_personal_account_button()
        
        profile_page = ProfilePage(driver)
        
        with allure.step("Кликаем по ссылке 'История заказов'"):
            profile_page.click_order_history_link()
        
        with allure.step("Проверяем, что открылась страница истории заказов"):
            assert Urls.ORDER_HISTORY_PAGE in profile_page.get_current_url(), "Страница истории заказов не открылась"
    
    @allure.title("Выход из аккаунта")
    def test_logout(self, driver, logged_in_user):
        """Проверяет выход из аккаунта"""
        main_page = logged_in_user["main_page"]
        
        with allure.step("Переходим в личный кабинет"):
            main_page.click_personal_account_button()
        
        profile_page = ProfilePage(driver)
        
        with allure.step("Кликаем по кнопке 'Выход'"):
            profile_page.click_logout_button()
        
        with allure.step("Ожидаем появления формы входа"):
            login_page = LoginPage(driver)
            login_page.wait_for_element_to_be_visible(login_page.locators.LOGIN_TITLE, timeout=Constants.TIMEOUT_MEDIUM)
        
        with allure.step("Проверяем, что открылась страница входа"):
            assert login_page.is_login_title_visible(), f"Заголовок '{Constants.LOGIN_TITLE}' не найден на странице"
            assert login_page.are_login_fields_available(), \
                "Поля логин и пароль не доступны на странице входа"

