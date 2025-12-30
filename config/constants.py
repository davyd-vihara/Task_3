"""Константы для тестов"""
import os
from dotenv import load_dotenv

load_dotenv()


class Constants:
    """Константы тестов"""
    # Браузер по умолчанию
    BROWSER = os.getenv("BROWSER", "chrome")
    
    # Пути к драйверам (приоритет у локальных путей)
    CHROME_DRIVER_PATH = os.getenv("CHROME_DRIVER_PATH", r"C:\WebDriver\chromedriver-win64\chromedriver.exe")
    FIREFOX_DRIVER_PATH = os.getenv("FIREFOX_DRIVER_PATH", r"C:\WebDriver\geckodriver-v0.36.0-win64\geckodriver.exe")
    
    # Режим запуска браузера
    FULLSCREEN = os.getenv("FULLSCREEN", "true").lower() == "true"
    
    # Тестовые данные
    TEST_EMAIL = os.getenv("TEST_EMAIL", "test@example.com")
    TEST_PASSWORD = os.getenv("TEST_PASSWORD", "password123")
    TEST_USER_PREFIX = "test_"
    TEST_USER_NAME_PREFIX = "TestUser"
    DEFAULT_PASSWORD = "123456"  # Фиксированный пароль для тестовых пользователей
    
    # Текстовые константы UI
    CONSTRUCTOR_TITLE = "Соберите бургер"
    ORDER_FEED_TITLE = "Лента заказов"
    INGREDIENT_DETAILS_TITLE = "Детали ингредиента"
    FIRST_BUN_NAME = "Флюоресцентная булка R2-D3"
    ORDER_COOKING_TEXT = "Ваш заказ начали готовить"
    ORDER_WAIT_TEXT = "Дождитесь готовности на орбитальной станции"
    LOGIN_TITLE = "Вход"
    
    # Таймауты (в секундах)
    TIMEOUT = 1
    TIMEOUT_MODAL_LOAD = 3
    
    # Оптимизация: переиспользование браузера (true/false)
    REUSE_BROWSER = os.getenv("REUSE_BROWSER", "false").lower() == "true"

