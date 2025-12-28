import pytest
import allure
import random
from utils.driver_factory import DriverFactory
from utils.config import Config
from utils.api_client import ApiClient
from pages.main_page import MainPage

def pytest_addoption(parser):
    """Добавляет опцию командной строки для выбора браузера"""
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Браузер для тестов: chrome или firefox"
    )

@pytest.fixture(scope="function")
def browser(request):
    """Фикстура для получения браузера из параметров"""
    return request.config.getoption("--browser")

@pytest.fixture(scope="function")
def driver(browser):
    """Фикстура для создания драйвера"""
    driver = DriverFactory.create_driver(browser)
    
    yield driver
    
    driver.quit()

@pytest.fixture(scope="function")
def api_client():
    """Фикстура для API клиента"""
    return ApiClient()

@pytest.fixture(scope="function")
def registered_user(api_client):
    """Создает тестового пользователя через API"""
    email = f"{Config.TEST_USER_PREFIX}{random.randint(10000, 99999)}@example.com"
    password = Config.TEST_PASSWORD
    name = f"{Config.TEST_USER_NAME_PREFIX}{random.randint(1000, 9999)}"
    access_token = None

    try:
        # Регистрация пользователя
        response = api_client.register_user(email, password, name)
        access_token = response.get("accessToken")

        yield {
            "email": email,
            "password": password,
            "name": name,
            "access_token": access_token
        }
    except Exception:
        # Если регистрация не удалась, пробуем войти
        try:
            response = api_client.login_user(email, password)
            access_token = response.get("accessToken")
            yield {
                "email": email,
                "password": password,
                "name": name,
                "access_token": access_token
            }
        except Exception:
            yield {
                "email": email,
                "password": password,
                "name": name,
                "access_token": None
            }
    finally:
        # Удаление пользователя после теста
        if access_token:
            try:
                api_client.delete_user(access_token)
            except Exception:
                pass

@pytest.fixture(scope="function")
def logged_in_user(driver, registered_user, api_client):
    """Фикстура для залогиненного пользователя"""
    import time
    from pages.login_page import LoginPage
    from pages.main_page import MainPage
    
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(registered_user["email"], registered_user["password"])
    
    # Ждем, пока загрузится главная страница и ингредиенты
    time.sleep(3)
    
    # Явно открываем главную страницу после логина
    main_page = MainPage(driver)
    main_page.open()
    
    # Ждем загрузки ингредиентов
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    wait = WebDriverWait(driver, 15)
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(@class, 'BurgerIngredient_ingredient')]")))
    except:
        pass  # Игнорируем, если не загрузились
    
    yield {
        "driver": driver,
        "user": registered_user,
        "api_client": api_client,
        "main_page": main_page
    }

@pytest.fixture(scope="function")
def main_page(driver):
    """Фикстура для главной страницы"""
    page = MainPage(driver, Config.BASE_URL)
    page.open()
    return page

# Хуки для Allure
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Хук для создания скриншотов при падении теста"""
    outcome = yield
    rep = outcome.get_result()
    
    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get("driver")
        if driver:
            try:
                allure.attach(
                    driver.get_screenshot_as_png(),
                    name="screenshot",
                    attachment_type=allure.attachment_type.PNG
                )
            except Exception:
                pass

