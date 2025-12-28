from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import json
import os

# #region agent log
def _log_debug(session_id, run_id, hypothesis_id, location, message, data):
    """Логирование для отладки"""
    log_path = r"c:\Git\master\perfect-project\.cursor\debug.log"
    try:
        log_entry = {
            "sessionId": session_id,
            "runId": run_id,
            "hypothesisId": hypothesis_id,
            "location": location,
            "message": message,
            "data": data,
            "timestamp": int(__import__("time").time() * 1000)
        }
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
    except Exception:
        pass
# #endregion

class BasePage:
    """Базовый класс для всех страниц"""
    
    def __init__(self, driver, url=None):
        self.driver = driver
        self.url = url
        self.wait = WebDriverWait(driver, 10)
    
    def open(self):
        """Открывает страницу"""
        if self.url:
            self.driver.get(self.url)
    
    def find_element(self, locator, timeout=10):
        """Находит элемент с ожиданием"""
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_element_located(locator))
    
    def find_elements(self, locator, timeout=10):
        """Находит все элементы с ожиданием"""
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_all_elements_located(locator))
    
    def find_visible_element(self, locator, timeout=10):
        """Находит видимый элемент"""
        # #region agent log
        _log_debug("debug-session", "run1", "A", "base_page.py:find_visible_element", "Поиск видимого элемента", {
            "locator": str(locator),
            "timeout": timeout,
            "url": self.driver.current_url if hasattr(self, "driver") else "unknown"
        })
        # #endregion
        try:
            wait = WebDriverWait(self.driver, timeout)
            element = wait.until(EC.visibility_of_element_located(locator))
            # #region agent log
            _log_debug("debug-session", "run1", "A", "base_page.py:find_visible_element", "Элемент найден", {
                "locator": str(locator),
                "tag": element.tag_name,
                "text": element.text[:50] if element.text else "",
                "is_displayed": element.is_displayed()
            })
            # #endregion
            return element
        except TimeoutException as e:
            # #region agent log
            _log_debug("debug-session", "run1", "A", "base_page.py:find_visible_element", "Элемент не найден", {
                "locator": str(locator),
                "timeout": timeout,
                "url": self.driver.current_url,
                "page_source_length": len(self.driver.page_source) if hasattr(self.driver, "page_source") else 0
            })
            # #endregion
            raise
    
    def click(self, locator):
        """Кликает по элементу"""
        element = self.find_visible_element(locator)
        element.click()
    
    def input_text(self, locator, text):
        """Вводит текст в поле"""
        element = self.find_visible_element(locator)
        element.clear()
        element.send_keys(text)
    
    def get_text(self, locator):
        """Получает текст элемента"""
        element = self.find_visible_element(locator)
        return element.text
    
    def is_element_visible(self, locator, timeout=5):
        """Проверяет видимость элемента"""
        # #region agent log
        _log_debug("debug-session", "run1", "B", "base_page.py:is_element_visible", "Проверка видимости элемента", {
            "locator": str(locator),
            "timeout": timeout,
            "url": self.driver.current_url if hasattr(self, "driver") else "unknown"
        })
        # #endregion
        try:
            wait = WebDriverWait(self.driver, timeout)
            element = wait.until(EC.visibility_of_element_located(locator))
            is_visible = element.is_displayed()
            # #region agent log
            _log_debug("debug-session", "run1", "B", "base_page.py:is_element_visible", "Элемент видим" if is_visible else "Элемент не видим", {
                "locator": str(locator),
                "is_visible": is_visible,
                "tag": element.tag_name if element else None
            })
            # #endregion
            return is_visible
        except TimeoutException:
            # #region agent log
            _log_debug("debug-session", "run1", "B", "base_page.py:is_element_visible", "Элемент не найден (TimeoutException)", {
                "locator": str(locator),
                "timeout": timeout
            })
            # #endregion
            return False
    
    def wait_for_element_to_disappear(self, locator, timeout=10):
        """Ожидает исчезновения элемента"""
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.invisibility_of_element_located(locator))
    
    def get_current_url(self):
        """Возвращает текущий URL"""
        return self.driver.current_url

