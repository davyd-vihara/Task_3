from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from config.constants import Constants
import os

class DriverFactory:
    """Фабрика для создания драйверов разных браузеров"""
    
    @staticmethod
    def _get_chrome_driver_path():
        """Получает путь к ChromeDriver (приоритет у локального пути)"""
        # Сначала проверяем локальный путь из конфига
        if Constants.CHROME_DRIVER_PATH and os.path.exists(Constants.CHROME_DRIVER_PATH):
            return Constants.CHROME_DRIVER_PATH
        
        # Если локального нет, используем webdriver-manager
        try:
            driver_path = ChromeDriverManager().install()
            
            # Исправление: webdriver-manager может вернуть неправильный файл
            if driver_path and not driver_path.lower().endswith('.exe'):
                driver_dir = os.path.dirname(driver_path)
                exe_path = None
                
                # Ищем chromedriver.exe в текущей директории
                test_path = os.path.join(driver_dir, 'chromedriver.exe')
                if os.path.exists(test_path):
                    exe_path = test_path
                else:
                    # Ищем в поддиректориях
                    for root, dirs, files in os.walk(driver_dir):
                        for file in files:
                            if file.lower() == 'chromedriver.exe':
                                exe_path = os.path.join(root, file)
                                break
                        if exe_path:
                            break
                
                if exe_path:
                    driver_path = exe_path
            
            return driver_path
        except Exception:
            raise Exception("Не удалось найти или скачать ChromeDriver")
    
    @staticmethod
    def _get_firefox_driver_path():
        """Получает путь к GeckoDriver (приоритет у локального пути)"""
        # Сначала проверяем локальный путь из конфига
        if Constants.FIREFOX_DRIVER_PATH and os.path.exists(Constants.FIREFOX_DRIVER_PATH):
            return Constants.FIREFOX_DRIVER_PATH
        
        # Если локального нет, используем webdriver-manager
        try:
            # Пробуем использовать кэшированную версию, если есть
            manager = GeckoDriverManager()
            # Проверяем кэш перед попыткой скачать
            try:
                driver_path = manager.install()
            except ValueError as e:
                # Если ошибка связана с rate limit, пробуем найти в кэше
                if "rate limit" in str(e).lower() or "API rate limit" in str(e):
                    # Ищем geckodriver в стандартных местах кэша webdriver-manager
                    import tempfile
                    cache_dir = os.path.join(tempfile.gettempdir(), ".wdm")
                    # Ищем geckodriver.exe в кэше
                    for root, dirs, files in os.walk(cache_dir):
                        for file in files:
                            if file.lower() == 'geckodriver.exe':
                                driver_path = os.path.join(root, file)
                                if os.path.exists(driver_path):
                                    return driver_path
                    raise Exception(
                        f"Превышен лимит GitHub API для загрузки GeckoDriver. "
                        f"Подождите несколько минут или установите GeckoDriver вручную. "
                        f"Ошибка: {str(e)}"
                    )
                raise
            
            # Исправление для Firefox: ищем geckodriver.exe
            if driver_path and not driver_path.lower().endswith('.exe'):
                driver_dir = os.path.dirname(driver_path)
                exe_path = os.path.join(driver_dir, 'geckodriver.exe')
                if os.path.exists(exe_path):
                    driver_path = exe_path
            
            return driver_path
        except Exception as e:
            error_msg = str(e)
            if "rate limit" in error_msg.lower() or "API rate limit" in error_msg:
                raise Exception(
                    f"Превышен лимит GitHub API для загрузки GeckoDriver. "
                    f"Подождите несколько минут или установите GeckoDriver вручную. "
                    f"Ошибка: {error_msg}"
                )
            raise Exception(f"Не удалось найти или скачать GeckoDriver: {error_msg}")
    
    @staticmethod
    def create_driver(browser_name="chrome"):
        """Создает и возвращает драйвер для указанного браузера"""
        browser_name = browser_name.lower()
        
        if browser_name == "chrome":
            options = webdriver.ChromeOptions()
            
            # Полноэкранный режим
            if Constants.FULLSCREEN:
                options.add_argument("--start-maximized")
            else:
                options.add_argument("--window-size=1920,1080")
            
            # Дополнительные параметры для стабильности
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
            options.add_experimental_option('useAutomationExtension', False)
            
            # Получаем путь к драйверу
            driver_path = DriverFactory._get_chrome_driver_path()
            
            # Создаем драйвер
            driver = webdriver.Chrome(
                service=ChromeService(driver_path),
                options=options
            )
            
            # Если полноэкранный режим не сработал через аргумент, делаем через maximize_window
            if Constants.FULLSCREEN:
                try:
                    driver.maximize_window()
                except Exception:
                    pass
            
        elif browser_name == "firefox":
            options = webdriver.FirefoxOptions()
            
            # Полноэкранный режим для Firefox
            if Constants.FULLSCREEN:
                options.add_argument("--start-maximized")
            else:
                options.add_argument("--width=1920")
                options.add_argument("--height=1080")
            
            # Получаем путь к драйверу
            driver_path = DriverFactory._get_firefox_driver_path()
            
            # Создаем драйвер
            driver = webdriver.Firefox(
                service=FirefoxService(driver_path),
                options=options
            )
            
            # Если полноэкранный режим не сработал через аргумент, делаем через maximize_window
            if Constants.FULLSCREEN:
                try:
                    driver.maximize_window()
                except Exception:
                    pass
            
        else:
            raise ValueError(f"Неподдерживаемый браузер: {browser_name}. "
                           f"Поддерживаются: chrome, firefox")
        
        # Не используем неявные ожидания - только явные через WebDriverWait и expected_conditions
        return driver

