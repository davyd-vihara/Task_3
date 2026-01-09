from pages.base_page import BasePage
from locators.order_feed_locators import OrderFeedPageLocators
from locators.base_locators import BaseLocators
from config.urls import Urls
from config.constants import Constants
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
import re
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
    def is_order_modal_visible(self, timeout=None):
        """Проверяет видимость модального окна заказа"""
        if timeout is None:
            timeout = Constants.TIMEOUT_MEDIUM
        return self.is_element_visible(self.locators.ORDER_MODAL, timeout=timeout)
    
    @allure.step("Ожидать появления модального окна заказа")
    def wait_for_order_modal(self, timeout=None):
        """Ожидает появления модального окна заказа"""
        if timeout is None:
            timeout = Constants.TIMEOUT_LONG
        
        self.wait_for_element_to_be_visible(self.locators.ORDER_MODAL, timeout=timeout)
    
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
            self.wait_for_element_to_be_visible(self.locators.TOTAL_ORDERS_COUNTER, timeout=Constants.TIMEOUT_DEFAULT)
            # Пробуем получить значение через локатор
            count_text = self.get_text(self.locators.TOTAL_ORDERS_COUNTER)
            # Убираем пробелы и преобразуем в число
            count = int(count_text.strip().replace(' ', ''))
            return count
        except (TimeoutException, NoSuchElementException, ValueError, AttributeError) as e:
            # Если не получилось, пробуем альтернативный способ
            try:
                # Используем JavaScript селектор напрямую
                count_text = self.execute_script(
                    "return document.querySelector('#root > div > main > div > div > div > div.undefined.mb-15 > p.OrderFeed_number__2MbrQ.text.text_type_digits-large')?.textContent || '';"
                )
                if count_text:
                    return int(count_text.strip().replace(' ', ''))
            except (ValueError, AttributeError):
                pass
            return 0
    
    @allure.step("Ожидать увеличения счетчика 'Выполнено за всё время'")
    def wait_for_total_orders_increase(self, initial_value, timeout=None):
        """Ожидает, пока счетчик 'Выполнено за всё время' станет больше начального значения"""
        if timeout is None:
            timeout = Constants.TIMEOUT_VERY_LONG
        wait = self.get_wait(timeout)
        # Используем lambda с self вместо driver
        return wait.until(lambda _: self.get_total_orders_count() > initial_value)
    
    @allure.step("Получить счетчик 'Выполнено за сегодня'")
    def get_today_orders_count(self):
        """Получает счетчик 'Выполнено за сегодня'"""
        try:
            return int(self.get_text(self.locators.TODAY_ORDERS_COUNTER))
        except (TimeoutException, NoSuchElementException, ValueError, AttributeError):
            return 0
    
    @allure.step("Ожидать увеличения счетчика 'Выполнено за сегодня'")
    def wait_for_today_orders_increase(self, initial_value, timeout=None):
        """Ожидает, пока счетчик 'Выполнено за сегодня' станет больше начального значения"""
        if timeout is None:
            timeout = Constants.TIMEOUT_VERY_LONG
        wait = self.get_wait(timeout)
        # Используем lambda с self вместо driver
        return wait.until(lambda _: self.get_today_orders_count() > initial_value)
    
    @allure.step("Получить список заказов в работе")
    def get_in_progress_orders(self):
        """Получает список заказов в работе"""
        try:
            # Сначала проверяем, что раздел "В работе" существует с коротким таймаутом
            if not self.is_element_visible(self.locators.IN_PROGRESS_SECTION, timeout=Constants.TIMEOUT_SHORT):
                return []
            
            # Получаем список заказов с коротким таймаутом
            orders = self.find_elements(self.locators.IN_PROGRESS_ORDERS, timeout=Constants.TIMEOUT_SHORT)
            return [order.text for order in orders if order.text]
        except (TimeoutException, NoSuchElementException, WebDriverException) as e:
            # Пробуем альтернативный способ поиска
            try:
                # Ищем все элементы li в разделе "В работе" с коротким таймаутом
                section = self.find_element(self.locators.IN_PROGRESS_SECTION, timeout=Constants.TIMEOUT_SHORT)
                orders = section.find_elements(By.TAG_NAME, "li")
                return [order.text for order in orders if order.text]
            except (TimeoutException, NoSuchElementException, WebDriverException):
                return []
    
    @allure.step("Ожидать появления заказа в разделе 'В работе'")
    def wait_for_order_in_progress(self, order_number, timeout=None):
        """Ожидает, пока заказ появится в разделе 'В работе'"""
        if timeout is None:
            timeout = Constants.TIMEOUT_VERY_LONG
        wait = self.get_wait(timeout)
        # Используем lambda с self вместо driver
        return wait.until(lambda _: self.is_order_in_progress(order_number))
    
    @allure.step("Проверить, есть ли заказ в разделе 'В работе'")
    def is_order_in_progress(self, order_number):
        """Проверяет, есть ли заказ в разделе 'В работе'"""
        order_num_normalized = re.sub(r'\D', '', str(order_number))
        
        # Сначала пробуем найти через текст раздела "В работе"
        try:
            section = self.find_element(self.locators.IN_PROGRESS_SECTION, timeout=Constants.TIMEOUT_SHORT)
            section_text_normalized = re.sub(r'\D', '', section.text)
            if order_num_normalized in section_text_normalized:
                return True
        except (TimeoutException, NoSuchElementException, WebDriverException):
            pass
        
        # Пробуем найти через элементы списка
        try:
            in_progress_elements = self.find_elements(self.locators.IN_PROGRESS_ORDERS, timeout=Constants.TIMEOUT_SHORT)
            for element in in_progress_elements:
                try:
                    element_text_normalized = re.sub(r'\D', '', str(element.text))
                    if order_num_normalized in element_text_normalized or element_text_normalized in order_num_normalized:
                        return True
                except (AttributeError, ValueError):
                    continue
        except (TimeoutException, NoSuchElementException, WebDriverException):
            pass
        
        # Если не нашли, пробуем через get_in_progress_orders
        try:
            orders = self.get_in_progress_orders()
            for order_text in orders:
                order_text_normalized = re.sub(r'\D', '', str(order_text))
                if order_num_normalized in order_text_normalized or order_text_normalized in order_num_normalized:
                    return True
        except (TimeoutException, NoSuchElementException, WebDriverException):
            pass
        
        return False
    
    @allure.step("Проверить наличие номера заказа в модальном окне")
    def is_order_number_visible(self):
        """Проверяет наличие номера заказа в модальном окне"""
        return self.is_element_visible(self.locators.ORDER_NUMBER, timeout=Constants.TIMEOUT_DEFAULT)
    
    @allure.step("Проверить наличие заголовка заказа в модальном окне")
    def is_order_title_visible(self):
        """Проверяет наличие заголовка заказа в модальном окне"""
        return self.is_element_visible(self.locators.ORDER_TITLE, timeout=Constants.TIMEOUT_DEFAULT)
    
    @allure.step("Проверить наличие статуса заказа в модальном окне")
    def is_order_status_visible(self):
        """Проверяет наличие статуса заказа в модальном окне"""
        return self.is_element_visible(self.locators.ORDER_STATUS, timeout=Constants.TIMEOUT_DEFAULT)
    
    @allure.step("Проверить наличие раздела 'Состав' в модальном окне")
    def is_order_composition_visible(self):
        """Проверяет наличие раздела 'Состав' в модальном окне"""
        # Упрощенная проверка: если элемент виден - true, если нет - false
        return self.is_element_visible(self.locators.ORDER_COMPOSITION_TITLE, timeout=Constants.TIMEOUT_MODAL_LOAD)


