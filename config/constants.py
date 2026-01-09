"""Константы для тестов"""
import os
from dotenv import load_dotenv

load_dotenv()


class BrowserConfig:
    """Настройки браузера"""
    BROWSER = os.getenv("BROWSER", "chrome")
    CHROME_DRIVER_PATH = os.getenv("CHROME_DRIVER_PATH", r"C:\WebDriver\chromedriver-win64\chromedriver.exe")
    FIREFOX_DRIVER_PATH = os.getenv("FIREFOX_DRIVER_PATH", r"C:\WebDriver\geckodriver-v0.36.0-win64\geckodriver.exe")
    FULLSCREEN = os.getenv("FULLSCREEN", "true").lower() == "true"
    REUSE_BROWSER = os.getenv("REUSE_BROWSER", "false").lower() == "true"

    
class TestData:
    """Тестовые данные"""
    TEST_EMAIL = os.getenv("TEST_EMAIL", "test@example.com")
    TEST_PASSWORD = os.getenv("TEST_PASSWORD", "password123")
    TEST_USER_PREFIX = "test_"
    TEST_USER_NAME_PREFIX = "TestUser"
    DEFAULT_PASSWORD = "123456"  # Фиксированный пароль для тестовых пользователей
    

class UITexts:
    """Текстовые константы UI"""
    CONSTRUCTOR_TITLE = "Соберите бургер"
    ORDER_FEED_TITLE = "Лента заказов"
    INGREDIENT_DETAILS_TITLE = "Детали ингредиента"
    FIRST_BUN_NAME = "Флюоресцентная булка R2-D3"
    ORDER_COOKING_TEXT = "Ваш заказ начали готовить"
    ORDER_WAIT_TEXT = "Дождитесь готовности на орбитальной станции"
    LOGIN_TITLE = "Вход"
    

class Timeouts:
    """Таймауты (в секундах)"""
    TIMEOUT = 1
    TIMEOUT_MODAL_LOAD = 3
    TIMEOUT_SHORT = 2  # Короткое ожидание (для быстрых операций)
    TIMEOUT_DEFAULT = 5  # Стандартное ожидание (для обычных операций)
    TIMEOUT_MEDIUM = 10  # Среднее ожидание (для загрузки страниц)
    TIMEOUT_LONG = 15  # Длинное ожидание (для авторизации, сложных операций)
    TIMEOUT_VERY_LONG = 30  # Очень длинное ожидание (для обработки на сервере)


# Для обратной совместимости - оставляем класс Constants, который объединяет все
class Constants:
    """Константы тестов (объединяет все классы для обратной совместимости)"""
    # Настройки браузера
    BROWSER = BrowserConfig.BROWSER
    CHROME_DRIVER_PATH = BrowserConfig.CHROME_DRIVER_PATH
    FIREFOX_DRIVER_PATH = BrowserConfig.FIREFOX_DRIVER_PATH
    FULLSCREEN = BrowserConfig.FULLSCREEN
    REUSE_BROWSER = BrowserConfig.REUSE_BROWSER
    
    # Тестовые данные
    TEST_EMAIL = TestData.TEST_EMAIL
    TEST_PASSWORD = TestData.TEST_PASSWORD
    TEST_USER_PREFIX = TestData.TEST_USER_PREFIX
    TEST_USER_NAME_PREFIX = TestData.TEST_USER_NAME_PREFIX
    DEFAULT_PASSWORD = TestData.DEFAULT_PASSWORD
    
    # Текстовые константы UI
    CONSTRUCTOR_TITLE = UITexts.CONSTRUCTOR_TITLE
    ORDER_FEED_TITLE = UITexts.ORDER_FEED_TITLE
    INGREDIENT_DETAILS_TITLE = UITexts.INGREDIENT_DETAILS_TITLE
    FIRST_BUN_NAME = UITexts.FIRST_BUN_NAME
    ORDER_COOKING_TEXT = UITexts.ORDER_COOKING_TEXT
    ORDER_WAIT_TEXT = UITexts.ORDER_WAIT_TEXT
    LOGIN_TITLE = UITexts.LOGIN_TITLE
    
    # Таймауты
    TIMEOUT = Timeouts.TIMEOUT
    TIMEOUT_MODAL_LOAD = Timeouts.TIMEOUT_MODAL_LOAD
    TIMEOUT_SHORT = Timeouts.TIMEOUT_SHORT
    TIMEOUT_DEFAULT = Timeouts.TIMEOUT_DEFAULT
    TIMEOUT_MEDIUM = Timeouts.TIMEOUT_MEDIUM
    TIMEOUT_LONG = Timeouts.TIMEOUT_LONG
    TIMEOUT_VERY_LONG = Timeouts.TIMEOUT_VERY_LONG
