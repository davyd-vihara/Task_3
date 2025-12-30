import allure
import time
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
        # #region agent log
        import json
        log_path = r"c:\Git\master\perfect-project\.cursor\debug.log"
        try:
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(json.dumps({"sessionId": "debug-session", "runId": "run1", "hypothesisId": "C", "location": "test_user_profile.py:14", "message": "test_go_to_personal_account started", "data": {"test": "test_go_to_personal_account"}, "timestamp": int(time.time() * 1000)}) + "\n")
        except: pass
        # #endregion
        
        main_page = logged_in_user["main_page"]
        
        with allure.step("Кликаем по кнопке 'Личный кабинет'"):
            # #region agent log
            try:
                with open(log_path, "a", encoding="utf-8") as f:
                    f.write(json.dumps({"sessionId": "debug-session", "runId": "run1", "hypothesisId": "C", "location": "test_user_profile.py:22", "message": "Before clicking personal account button", "data": {"current_url": driver.current_url}, "timestamp": int(time.time() * 1000)}) + "\n")
            except: pass
            # #endregion
            main_page.click_personal_account_button()
            # #region agent log
            try:
                with open(log_path, "a", encoding="utf-8") as f:
                    f.write(json.dumps({"sessionId": "debug-session", "runId": "run1", "hypothesisId": "C", "location": "test_user_profile.py:26", "message": "After clicking personal account button", "data": {"current_url": driver.current_url}, "timestamp": int(time.time() * 1000)}) + "\n")
            except: pass
            # #endregion
        
        with allure.step("Проверяем, что открылась страница профиля"):
            current_url = driver.current_url
            # #region agent log
            try:
                with open(log_path, "a", encoding="utf-8") as f:
                    f.write(json.dumps({"sessionId": "debug-session", "runId": "run1", "hypothesisId": "C", "location": "test_user_profile.py:32", "message": "Checking profile page URL", "data": {"current_url": current_url, "expected_url": Urls.PROFILE_PAGE, "url_match": Urls.PROFILE_PAGE in current_url}, "timestamp": int(time.time() * 1000)}) + "\n")
            except: pass
            # #endregion
            assert Urls.PROFILE_PAGE in current_url, "Страница профиля не открылась"
    
    @allure.title("Переход в раздел 'История заказов'")
    def test_go_to_order_history(self, driver, logged_in_user):
        """Проверяет переход в раздел 'История заказов'"""
        main_page = logged_in_user["main_page"]
        main_page.click_personal_account_button()
        
        profile_page = ProfilePage(driver)
        
        with allure.step("Кликаем по ссылке 'История заказов'"):
            profile_page.click_order_history_link()
        
        with allure.step("Проверяем, что открылась страница истории заказов"):
            assert Urls.ORDER_HISTORY_PAGE in driver.current_url, "Страница истории заказов не открылась"
    
    @allure.title("Выход из аккаунта")
    def test_logout(self, driver, logged_in_user):
        """Проверяет выход из аккаунта"""
        main_page = logged_in_user["main_page"]
        main_page.click_personal_account_button()
        
        profile_page = ProfilePage(driver)
        
        with allure.step("Кликаем по кнопке 'Выход'"):
            profile_page.click_logout_button()
        
        with allure.step("Ожидаем появления формы входа"):
            time.sleep(Constants.TIMEOUT_SHORT)
            login_page = LoginPage(driver)
        
        with allure.step(f"Проверяем, что отображается страница входа с заголовком '{Constants.LOGIN_TITLE}'"):
            assert login_page.is_login_title_visible(), f"Заголовок '{Constants.LOGIN_TITLE}' не найден на странице"
        
        with allure.step("Проверяем, что поля логин и пароль доступны"):
            assert login_page.are_login_fields_available(), \
                "Поля логин и пароль не доступны на странице входа"

