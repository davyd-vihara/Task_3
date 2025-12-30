import pytest
import allure
import uuid
from utils.driver_factory import DriverFactory
from utils.api_client import ApiClient
from pages.main_page import MainPage
from config.constants import Constants

@pytest.fixture(scope="function", params=["chrome", "firefox"])
def driver(request):
    """Фикстура для создания драйвера.
    
    Автоматически запускает тесты в обоих браузерах.
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
    # Создаем уникальные данные пользователя (используем uuid как в референсе)
    email = f"test_{uuid.uuid4()}@mail.ru"
    password = Constants.DEFAULT_PASSWORD
    name = "Test User"
    access_token = None

    try:
        # Регистрация пользователя через API
        response = api_client.register_user(email, password, name)
        access_token = response.get("accessToken")
        
        # Проверяем, что токен получен
        if not access_token:
            raise Exception(f"Токен не получен при регистрации. Ответ: {response}")

        user_data = {
            "email": email,
            "password": password,
            "name": name,
            "access_token": access_token
        }
        
        # Проверяем, что данные корректны
        assert user_data["email"] == email, "Email не совпадает"
        assert user_data["password"] == password, "Пароль не совпадает"
        assert user_data["access_token"], "Access token отсутствует"
        
        yield user_data
    except Exception as e:
        # Если регистрация не удалась, пробуем войти (возможно пользователь уже существует)
        try:
            response = api_client.login_user(email, password)
            access_token = response.get("accessToken")
            if not access_token:
                raise Exception(f"Токен не получен при входе. Ответ: {response}")
            
            user_data = {
                "email": email,
                "password": password,
                "name": name,
                "access_token": access_token
            }
            yield user_data
        except Exception as login_error:
            # Если и вход не удался, выбрасываем исключение с информацией
            raise Exception(
                f"Не удалось зарегистрировать или войти пользователя. "
                f"Email: {email}, Ошибка регистрации: {str(e)}, "
                f"Ошибка входа: {str(login_error)}"
            )
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
    
    # Проверяем, что пользователь зарегистрирован
    assert registered_user.get("email"), "Пользователь не зарегистрирован"
    assert registered_user.get("password"), "Пароль пользователя отсутствует"
    
    login_page = LoginPage(driver)
    login_page.open()
    
    # Выполняем авторизацию
    login_page.login(registered_user["email"], registered_user["password"])
    
    # Проверяем, что произошел переход с страницы логина (авторизация успешна)
    from config.urls import Urls
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    wait = WebDriverWait(driver, 15)
    
    # Ждем перехода на главную страницу
    try:
        wait.until(lambda d: "/login" not in d.current_url or Urls.BASE_URL.rstrip('/') in d.current_url)
    except Exception:
        pass
    
    # Явно открываем главную страницу после логина
    main_page = MainPage(driver)
    main_page.open()
    
    # Ждем исчезновения overlay (модального окна загрузки)
    main_page.wait_for_page_load()
    
    # Ждем загрузки ингредиентов
    from selenium.webdriver.common.by import By
    try:
        wait.until(EC.presence_of_element_located(
            (By.XPATH, "//a[contains(@class, 'BurgerIngredient_ingredient')]")
        ))
    except Exception:
        pass  # Игнорируем, если не загрузились
    
    # Проверяем, что пользователь авторизован - кнопка "Оформить заказ" должна быть видна
    max_retries = 3
    for attempt in range(max_retries):
        try:
            # Проверяем, что кнопка "Оформить заказ" видна
            wait.until(EC.presence_of_element_located(main_page.locators.ORDER_BUTTON))
            # Дополнительно проверяем, что кнопка "Войти в аккаунт" не видна
            try:
                wait.until(EC.invisibility_of_element_located(main_page.locators.LOGIN_BUTTON))
            except Exception:
                pass
            break  # Если все проверки прошли, выходим из цикла
        except Exception:
            if attempt < max_retries - 1:
                # Пробуем еще раз открыть главную страницу
                main_page.open()
                time.sleep(2)
                main_page.wait_for_page_load()
            else:
                # Если после всех попыток не удалось, продолжаем (может быть проблема с авторизацией)
                pass
    
    yield {
        "driver": driver,
        "user": registered_user,
        "api_client": api_client,
        "main_page": main_page
    }

@pytest.fixture(scope="function")
def main_page(driver):
    """Фикстура для главной страницы"""
    from config.urls import Urls
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
    from pages.constructor_page import ConstructorPage
    opened_main_page.click_constructor_button()
    constructor_page = ConstructorPage(driver)
    return constructor_page


@pytest.fixture(scope="function")
def order_feed_page(driver, opened_main_page):
    """Фикстура для страницы ленты заказов"""
    from pages.order_feed_page import OrderFeedPage
    opened_main_page.click_order_feed_button()
    order_feed_page = OrderFeedPage(driver)
    return order_feed_page


def pytest_collection_modifyitems(config, items):
    """Изменяет порядок выполнения тестов: сначала все на Chrome, потом на Firefox"""
    # Группируем тесты по браузеру
    chrome_tests = []
    firefox_tests = []
    other_tests = []
    
    for item in items:
        # Проверяем id теста - для параметризованных фикстур формат: test_name[param_value]
        test_id = item.nodeid
        
        if '[chrome]' in test_id:
            chrome_tests.append(item)
        elif '[firefox]' in test_id:
            firefox_tests.append(item)
        else:
            other_tests.append(item)
    
    # Переупорядочиваем: сначала все Chrome тесты, потом все Firefox тесты, затем остальные
    items[:] = chrome_tests + firefox_tests + other_tests
    
    # Отладочный вывод (можно убрать после проверки)
    if config.option.verbose >= 1:
        print(f"\n[DEBUG] Переупорядочивание тестов: Chrome={len(chrome_tests)}, Firefox={len(firefox_tests)}, Other={len(other_tests)}")


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

