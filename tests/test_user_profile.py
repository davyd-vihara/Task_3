import allure
from pages.profile_page import ProfilePage
from pages.login_page import LoginPage


@allure.feature("Личный кабинет")
@allure.story("Функциональность личного кабинета")
class TestUserProfile:
    
    @allure.title("Переход по клику на 'Личный кабинет'")
    def test_go_to_personal_account(self, driver, logged_in_user):
        """Проверяет переход по клику на 'Личный кабинет'"""
        import time
        main_page = logged_in_user["main_page"]
        
        with allure.step("Кликаем по кнопке 'Личный кабинет'"):
            main_page.click_personal_account_button()
        
        # Ждем загрузки страницы профиля
        time.sleep(2)
        
        profile_page = ProfilePage(driver)
        
        with allure.step("Проверяем, что открылась страница профиля"):
            assert profile_page.is_profile_page_visible(), "Страница профиля не открылась"
    
    @allure.title("Переход в раздел 'История заказов'")
    def test_go_to_order_history(self, driver, logged_in_user):
        """Проверяет переход в раздел 'История заказов'"""
        import time
        main_page = logged_in_user["main_page"]
        main_page.click_personal_account_button()
        
        # Ждем загрузки страницы профиля
        time.sleep(2)
        
        profile_page = ProfilePage(driver)
        
        with allure.step("Кликаем по ссылке 'История заказов'"):
            profile_page.click_order_history_link()
        
        with allure.step("Проверяем, что открылась страница истории заказов"):
            assert profile_page.is_order_history_visible(), "Страница истории заказов не открылась"
    
    @allure.title("Выход из аккаунта")
    def test_logout(self, driver, logged_in_user):
        """Проверяет выход из аккаунта"""
        import time
        main_page = logged_in_user["main_page"]
        main_page.click_personal_account_button()
        
        # Ждем загрузки страницы профиля
        time.sleep(2)
        
        profile_page = ProfilePage(driver)
        
        with allure.step("Кликаем по кнопке 'Выход'"):
            profile_page.click_logout_button()
        
        login_page = LoginPage(driver)
        
        with allure.step("Проверяем, что открылась страница входа"):
            assert login_page.is_login_form_visible(), "Страница входа не открылась после выхода"

