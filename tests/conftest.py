import pytest
import allure
import uuid
from utils.driver_factory import DriverFactory
from utils.api_client import ApiClient
from config.constants import Constants
from config.urls import Urls
from pages.login_page import LoginPage
from pages.main_page import MainPage
from pages.constructor_page import ConstructorPage
from pages.order_feed_page import OrderFeedPage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Глобальное хранилище для браузеров (для оптимизированного режима)
_browser_instances = {}


# Режим переиспользования браузера (можно включить через переменную окружения REUSE_BROWSER=true)
REUSE_BROWSER = Constants.REUSE_BROWSER


if REUSE_BROWSER:
    # ОПТИМИЗИРОВАННЫЙ РЕЖИМ: переиспользование браузера с изоляцией через вкладки
    
    @pytest.fixture(scope="session", params=["chrome", "firefox"])
    def browser_session(request):
        """Фикстура сессии браузера - создается один раз на всю сессию тестов.
        
        Браузер создается один раз и переиспользуется для всех тестов.
        Закрывается только в конце всей сессии тестов.
        """
        browser_name = request.param
        
        if browser_name not in _browser_instances:
            driver = DriverFactory.create_driver(browser_name)
            _browser_instances[browser_name] = driver
        
        yield _browser_instances[browser_name]
    
    @pytest.fixture(scope="function")
    def driver(browser_session):
        """Фикстура для каждого теста - открывает новую вкладку и обеспечивает изоляцию.
        
        Для каждого теста:
        1. Открывает новую вкладку
        2. Очищает cookies и localStorage
        3. После теста закрывает вкладку
        """
        # Сохраняем исходную вкладку
        original_window = browser_session.current_window_handle
        original_windows = browser_session.window_handles
        
        # Открываем новую вкладку для теста
        browser_session.execute_script("window.open('about:blank', '_blank');")
        
        # Переключаемся на новую вкладку
        new_windows = browser_session.window_handles
        new_window = [w for w in new_windows if w not in original_windows][0]
        browser_session.switch_to.window(new_window)
        
        # Очищаем состояние браузера для изоляции теста
        browser_session.delete_all_cookies()
        browser_session.execute_script("localStorage.clear();")
        browser_session.execute_script("sessionStorage.clear();")
        
        yield browser_session
        
        # После теста закрываем вкладку и возвращаемся к исходной
        browser_session.close()
        browser_session.switch_to.window(original_window)
    
    def pytest_sessionfinish(session, exitstatus):
        """Закрываем все браузеры в конце сессии"""
        for browser_name, driver in _browser_instances.items():
            driver.quit()
        _browser_instances.clear()

else:
    # СТАНДАРТНЫЙ РЕЖИМ: новый браузер для каждого теста
    
    @pytest.fixture(scope="function", params=["chrome", "firefox"])
    def driver(request):
        """Фикстура для создания драйвера.
        
        Автоматически запускает тесты в обоих браузерах.
        Создает новый браузер для каждого теста (максимальная изоляция).
        """
        driver = DriverFactory.create_driver(request.param)
        
        yield driver
        
        driver.quit()


@pytest.fixture(scope="function")
def api_client():
    """Фикстура для API клиента"""
    return ApiClient()


@pytest.fixture(scope="function")
def registered_user(api_client):
    """Создает тестового пользователя через API и возвращает его данные"""
    email = f"test_{uuid.uuid4()}@mail.ru"
    password = Constants.DEFAULT_PASSWORD
    name = "Test User"

    response = api_client.register_user(email, password, name)
    access_token = response.get("accessToken")
    
    if not access_token:
        raise Exception(f"Токен не получен при регистрации. Ответ: {response}")

    user_data = {
        "email": email,
        "password": password,
        "name": name,
        "access_token": access_token
    }
    
    yield user_data
    
    # Очистка: удаляем пользователя после теста
    api_client.delete_user(access_token)


@pytest.fixture(scope="function")
def logged_in_user(driver, registered_user, api_client):
    """Фикстура для залогиненного пользователя"""
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(registered_user["email"], registered_user["password"])
    
    wait = WebDriverWait(driver, Constants.TIMEOUT_LONG)
    
    # Линейный сценарий: ждем выхода из страницы логина
    wait.until(lambda d: "/login" not in d.current_url or Urls.BASE_URL.rstrip('/') in d.current_url)
    
    main_page = MainPage(driver)
    main_page.open()
    main_page.wait_for_page_load()
    
    # Линейный сценарий: ждем появления кнопки заказа
    wait.until(EC.presence_of_element_located(main_page.locators.ORDER_BUTTON))
    wait.until(EC.invisibility_of_element_located(main_page.locators.LOGIN_BUTTON))
    
    yield {
        "driver": driver,
        "user": registered_user,
        "api_client": api_client,
        "main_page": main_page
    }


@pytest.fixture(scope="function")
def main_page(driver):
    """Фикстура для главной страницы"""
    page = MainPage(driver, Urls.BASE_URL)
    page.open()
    return page


@pytest.fixture(scope="function")
def opened_main_page(driver):
    """Фикстура для открытой главной страницы с проверкой загрузки"""
    main_page = MainPage(driver)
    main_page.open()
    main_page.wait_for_page_load()
    return main_page


@pytest.fixture(scope="function")
def constructor_page(driver, opened_main_page):
    """Фикстура для страницы конструктора"""
    opened_main_page.click_constructor_button()
    constructor_page = ConstructorPage(driver)
    return constructor_page


@pytest.fixture(scope="function")
def order_feed_page(driver, opened_main_page):
    """Фикстура для страницы ленты заказов"""
    opened_main_page.click_order_feed_button()
    order_feed_page = OrderFeedPage(driver)
    return order_feed_page


def pytest_collection_modifyitems(config, items):
    """Изменяет порядок выполнения тестов: сначала все на Chrome, потом на Firefox"""
    chrome_tests = []
    firefox_tests = []
    other_tests = []
    
    for item in items:
        test_id = item.nodeid
        if '[chrome]' in test_id:
            chrome_tests.append(item)
        elif '[firefox]' in test_id:
            firefox_tests.append(item)
        else:
            other_tests.append(item)
    
    items[:] = chrome_tests + firefox_tests + other_tests


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Хук для создания скриншотов при падении теста в Allure"""
    outcome = yield
    rep = outcome.get_result()
    
    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get("driver")
        if driver:
            allure.attach(
                driver.get_screenshot_as_png(),
                name="screenshot",
                attachment_type=allure.attachment_type.PNG
            )
