import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Конфигурация тестов"""
    BASE_URL = "https://stellarburgers.education-services.ru/"
    
    # Браузер по умолчанию (можно переопределить через переменную окружения)
    BROWSER = os.getenv("BROWSER", "chrome")
    
    # Пути к драйверам (приоритет у локальных путей)
    CHROME_DRIVER_PATH = os.getenv("CHROME_DRIVER_PATH", r"C:\WebDriver\chromedriver-win64\chromedriver.exe")
    FIREFOX_DRIVER_PATH = os.getenv("FIREFOX_DRIVER_PATH", "")
    
    # Режим запуска браузера
    FULLSCREEN = os.getenv("FULLSCREEN", "true").lower() == "true"
    
    # Тестовые данные
    TEST_EMAIL = os.getenv("TEST_EMAIL", "test@example.com")
    TEST_PASSWORD = os.getenv("TEST_PASSWORD", "password123")
    TEST_USER_PREFIX = "test_"
    TEST_USER_NAME_PREFIX = "TestUser"
    
    # API
    API_URL = "https://stellarburgers.nomoreparties.site/api"

