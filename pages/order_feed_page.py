from pages.base_page import BasePage
from locators.order_feed_locators import OrderFeedPageLocators
from locators.base_locators import BaseLocators
from config.urls import Urls
from selenium.webdriver.common.by import By
import allure

class OrderFeedPage(BasePage):
    """Страница ленты заказов"""
    
    def __init__(self, driver):
        super().__init__(driver, f"{Urls.BASE_URL}feed")
        self.locators = OrderFeedPageLocators()
        self.base_locators = BaseLocators()
    
    @allure.step("Проверить видимость заголовка 'Лента заказов'")
    def is_order_feed_title_visible(self):
        """Проверяет видимость заголовка 'Лента заказов'"""
        return self.is_element_visible(self.locators.ORDER_FEED_TITLE)
    
    @allure.step("Кликнуть по первому заказу")
    def click_first_order(self):
        """Кликает по первому заказу"""
        self.click_by_js(self.locators.FIRST_ORDER)
    
    @allure.step("Проверить видимость модального окна заказа")
    def is_order_modal_visible(self, timeout=10):
        """Проверяет видимость модального окна заказа"""
        return self.is_element_visible(self.locators.ORDER_MODAL, timeout=timeout)
    
    @allure.step("Ожидать появления модального окна заказа")
    def wait_for_order_modal(self, timeout=15):
        """Ожидает появления модального окна заказа"""
        import time
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        
        # Небольшая задержка для начала анимации
        time.sleep(0.5)
        
        # Пробуем найти модальное окно разными способами
        wait = WebDriverWait(self.driver, timeout)
        
        def modal_appeared(driver):
            # Пробуем разные варианты локаторов
            locators_to_try = [
                (By.XPATH, "//section[2]/div[1]/div"),
                (By.XPATH, "//*[@id='root']/div/section[2]/div[1]/div"),
                (By.XPATH, "//div[contains(@class, 'Modal_modal_container')]"),
                (By.XPATH, "//div[contains(@class, 'Modal_modal__container')]"),
            ]
            
            for by, locator in locators_to_try:
                try:
                    element = driver.find_element(by, locator)
                    if element and element.is_displayed():
                        return True
                except:
                    continue
            return False
        
        try:
            wait.until(modal_appeared)
        except Exception:
            # Если не удалось найти, пробуем еще раз с базовым локатором
            self.wait_for_element_to_be_visible(self.locators.ORDER_MODAL, timeout=5)
    
    @allure.step("Закрыть модальное окно заказа")
    def close_order_modal(self):
        """Закрывает модальное окно заказа"""
        self.click_by_js(self.base_locators.MODAL_CLOSE_BUTTON)
    
    @allure.step("Получить номер заказа из модального окна")
    def get_order_number(self):
        """Получает номер заказа из модального окна"""
        return self.get_text(self.locators.ORDER_NUMBER)
    
    @allure.step("Получить счетчик 'Выполнено за всё время'")
    def get_total_orders_count(self):
        """Получает счетчик 'Выполнено за всё время'"""
        try:
            # Ждем появления элемента счетчика
            self.wait_for_element_to_be_visible(self.locators.TOTAL_ORDERS_COUNTER, timeout=5)
            # Пробуем получить значение через локатор
            count_text = self.get_text(self.locators.TOTAL_ORDERS_COUNTER)
            # Убираем пробелы и преобразуем в число
            count = int(count_text.strip().replace(' ', ''))
            return count
        except Exception as e:
            # Если не получилось, пробуем альтернативный способ
            try:
                # Используем JavaScript селектор напрямую
                count_text = self.driver.execute_script(
                    "return document.querySelector('#root > div > main > div > div > div > div.undefined.mb-15 > p.OrderFeed_number__2MbrQ.text.text_type_digits-large')?.textContent || '';"
                )
                if count_text:
                    return int(count_text.strip().replace(' ', ''))
            except:
                pass
            return 0
    
    @allure.step("Получить счетчик 'Выполнено за сегодня'")
    def get_today_orders_count(self):
        """Получает счетчик 'Выполнено за сегодня'"""
        try:
            return int(self.get_text(self.locators.TODAY_ORDERS_COUNTER))
        except:
            return 0
    
    @allure.step("Получить список заказов в работе")
    def get_in_progress_orders(self):
        """Получает список заказов в работе"""
        try:
            # Сначала проверяем, что раздел "В работе" существует
            if not self.is_element_visible(self.locators.IN_PROGRESS_SECTION, timeout=5):
                return []
            
            # Получаем список заказов
            orders = self.find_elements(self.locators.IN_PROGRESS_ORDERS, timeout=5)
            return [order.text for order in orders if order.text]
        except Exception:
            # Пробуем альтернативный способ поиска
            try:
                # Ищем все элементы li в разделе "В работе"
                from selenium.webdriver.common.by import By
                section = self.find_element(self.locators.IN_PROGRESS_SECTION, timeout=3)
                orders = section.find_elements(By.TAG_NAME, "li")
                return [order.text for order in orders if order.text]
            except Exception:
                return []
    
    @allure.step("Проверить, есть ли заказ в разделе 'В работе'")
    def is_order_in_progress(self, order_number):
        """Проверяет, есть ли заказ в разделе 'В работе'"""
        import re
        # Нормализуем номер заказа - оставляем только цифры
        order_num_normalized = re.sub(r'\D', '', str(order_number))
        
        try:
            # Получаем список заказов в работе
            orders = self.get_in_progress_orders()
            
            # Проверяем каждый заказ
            for order_text in orders:
                # Нормализуем текст заказа - оставляем только цифры
                order_text_normalized = re.sub(r'\D', '', str(order_text))
                # Проверяем, содержится ли номер заказа в тексте
                if order_num_normalized in order_text_normalized or order_text_normalized in order_num_normalized:
                    return True
            
            # Также пробуем найти напрямую через локатор
            try:
                in_progress_elements = self.find_elements(self.locators.IN_PROGRESS_ORDERS)
                for element in in_progress_elements:
                    element_text = element.text
                    element_text_normalized = re.sub(r'\D', '', str(element_text))
                    if order_num_normalized in element_text_normalized or element_text_normalized in order_num_normalized:
                        return True
            except Exception:
                pass
            
            return False
        except Exception:
            return False
    
    @allure.step("Проверить наличие номера заказа в модальном окне")
    def is_order_number_visible(self):
        """Проверяет наличие номера заказа в модальном окне"""
        return self.is_element_visible(self.locators.ORDER_NUMBER, timeout=5)
    
    @allure.step("Проверить наличие заголовка заказа в модальном окне")
    def is_order_title_visible(self):
        """Проверяет наличие заголовка заказа в модальном окне"""
        return self.is_element_visible(self.locators.ORDER_TITLE, timeout=5)
    
    @allure.step("Проверить наличие статуса заказа в модальном окне")
    def is_order_status_visible(self):
        """Проверяет наличие статуса заказа в модальном окне"""
        return self.is_element_visible(self.locators.ORDER_STATUS, timeout=5)
    
    @allure.step("Проверить наличие раздела 'Состав' в модальном окне")
    def is_order_composition_visible(self):
        """Проверяет наличие раздела 'Состав' в модальном окне"""
        # Пробуем найти элемент разными способами
        try:
            # Сначала пробуем через локатор
            if self.is_element_visible(self.locators.ORDER_COMPOSITION_TITLE, timeout=3):
                return True
        except:
            pass
        
        # Если не нашли по локатору, пробуем найти по тексту напрямую в модальном окне
        try:
            # Ищем внутри модального окна
            modal = self.find_element(self.locators.ORDER_MODAL, timeout=3)
            composition = modal.find_element(By.XPATH, ".//p[contains(text(), 'Состав')]")
            return composition and composition.is_displayed()
        except:
            pass
        
        # Пробуем глобальный поиск
        try:
            composition = self.driver.find_element(By.XPATH, "//p[contains(text(), 'Состав')]")
            return composition and composition.is_displayed()
        except:
            return False


