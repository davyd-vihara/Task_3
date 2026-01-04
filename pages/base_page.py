from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from config.constants import Constants
import allure

class BasePage:
    """Базовый класс для всех страниц"""
    
    def __init__(self, driver, url=None):
        self.driver = driver
        self.url = url
        self.wait = WebDriverWait(driver, Constants.TIMEOUT_MEDIUM)
    
    @allure.step("Открыть страницу")
    def open(self):
        """Открывает страницу"""
        if self.url:
            self.driver.get(self.url)
    
    @allure.step("Найти элемент")
    def find_element(self, locator, timeout=None):
        """Находит элемент с ожиданием"""
        if timeout is None:
            timeout = Constants.TIMEOUT_MEDIUM
        wait = self.get_wait(timeout)
        return wait.until(EC.presence_of_element_located(locator))
    
    @allure.step("Найти все элементы")
    def find_elements(self, locator, timeout=None):
        """Находит все элементы с ожиданием"""
        if timeout is None:
            timeout = Constants.TIMEOUT_MEDIUM
        try:
            wait = self.get_wait(timeout)
            return wait.until(EC.presence_of_all_elements_located(locator))
        except (TimeoutException, WebDriverException):
            return []
        except Exception:
            return []
    
    @allure.step("Найти видимый элемент")
    def find_visible_element(self, locator, timeout=None):
        """Находит видимый элемент"""
        if timeout is None:
            timeout = Constants.TIMEOUT_MEDIUM
        wait = self.get_wait(timeout)
        return wait.until(EC.visibility_of_element_located(locator))
    
    @allure.step("Кликнуть по элементу")
    def click(self, locator):
        """Кликает по элементу"""
        element = self.find_visible_element(locator)
        try:
            element.click()
        except Exception:
            # Если обычный клик не работает (например, элемент перекрыт overlay), используем JavaScript
            self.execute_script("arguments[0].click();", element)
    
    @allure.step("Кликнуть по элементу через JavaScript")
    def click_by_js(self, locator):
        """Кликает по элементу через JavaScript (обходит проблемы с перекрытием элементов)"""
        element = self.find_visible_element(locator)
        self.execute_script("arguments[0].click();", element)
    
    @allure.step("Перетащить элемент")
    def drag_and_drop_element(self, source, target):
        """Перетаскивает элемент из source в target (использует seletools для надежной работы в Firefox)"""
        from seletools.actions import drag_and_drop
        drag_and_drop(self.driver, source, target)
    
    @allure.step("Ввести текст в поле")
    def input_text(self, locator, text):
        """Вводит текст в поле"""
        element = self.find_visible_element(locator)
        element.clear()
        element.send_keys(text)
    
    @allure.step("Получить текст элемента")
    def get_text(self, locator):
        """Получает текст элемента"""
        element = self.find_visible_element(locator)
        return element.text
    
    @allure.step("Проверить видимость элемента")
    def is_element_visible(self, locator, timeout=None):
        """Проверяет видимость элемента"""
        if timeout is None:
            timeout = Constants.TIMEOUT_DEFAULT
        try:
            wait = self.get_wait(timeout)
            element = wait.until(EC.visibility_of_element_located(locator))
            return element.is_displayed()
        except (TimeoutException, WebDriverException):
            return False
        except Exception:
            return False
    
    @allure.step("Ожидать исчезновения элемента")
    def wait_for_element_to_disappear(self, locator, timeout=None):
        """Ожидает исчезновения элемента"""
        if timeout is None:
            timeout = Constants.TIMEOUT_MEDIUM
        wait = self.get_wait(timeout)
        return wait.until(EC.invisibility_of_element_located(locator))
    
    @allure.step("Ожидать появления видимого элемента")
    def wait_for_element_to_be_visible(self, locator, timeout=None):
        """Ожидает появления видимого элемента"""
        return self.find_visible_element(locator, timeout=timeout)
    
    @allure.step("Получить текущий URL")
    def get_current_url(self):
        """Возвращает текущий URL"""
        return self.driver.current_url
    
    @allure.step("Проверить, что URL содержит часть")
    def wait_for_url_contains(self, url_part, timeout=None):
        """Ожидает, что URL содержит указанную часть"""
        if timeout is None:
            timeout = Constants.TIMEOUT_MEDIUM
        wait = self.get_wait(timeout)
        return wait.until(lambda d: url_part in d.current_url)
    
    @allure.step("Проверить, что URL не содержит часть")
    def wait_for_url_not_contains(self, url_part, timeout=None):
        """Ожидает, что URL не содержит указанную часть"""
        if timeout is None:
            timeout = Constants.TIMEOUT_MEDIUM
        wait = self.get_wait(timeout)
        return wait.until(lambda d: url_part not in d.current_url)
    
    @allure.step("Получить WebDriverWait")
    def get_wait(self, timeout=None):
        """Возвращает объект WebDriverWait с указанным таймаутом"""
        if timeout is None:
            timeout = Constants.TIMEOUT_MEDIUM
        return WebDriverWait(self.driver, timeout)
    
    @allure.step("Выполнить JavaScript")
    def execute_script(self, script, *args):
        """Выполняет JavaScript код"""
        return self.driver.execute_script(script, *args)
    
    @allure.step("Найти элемент напрямую (без ожидания)")
    def find_element_direct(self, by, value):
        """Находит элемент напрямую без ожидания (для поиска внутри других элементов)"""
        return self.driver.find_element(by, value)

