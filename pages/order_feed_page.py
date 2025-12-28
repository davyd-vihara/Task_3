from pages.base_page import BasePage
from locators.order_feed_locators import OrderFeedPageLocators
from locators.base_locators import BaseLocators
from utils.config import Config

class OrderFeedPage(BasePage):
    """Страница ленты заказов"""
    
    def __init__(self, driver):
        super().__init__(driver, f"{Config.BASE_URL}feed")
        self.locators = OrderFeedPageLocators()
        self.base_locators = BaseLocators()
    
    def click_first_order(self):
        """Кликает по первому заказу"""
        self.click(self.locators.FIRST_ORDER)
    
    def is_order_modal_visible(self):
        """Проверяет видимость модального окна заказа"""
        return self.is_element_visible(self.locators.ORDER_MODAL)
    
    def close_order_modal(self):
        """Закрывает модальное окно заказа"""
        self.click(self.base_locators.MODAL_CLOSE_BUTTON)
    
    def get_order_number(self):
        """Получает номер заказа из модального окна"""
        return self.get_text(self.locators.ORDER_NUMBER)
    
    def get_total_orders_count(self):
        """Получает счетчик 'Выполнено за всё время'"""
        try:
            return int(self.get_text(self.locators.TOTAL_ORDERS_COUNTER))
        except:
            return 0
    
    def get_today_orders_count(self):
        """Получает счетчик 'Выполнено за сегодня'"""
        try:
            return int(self.get_text(self.locators.TODAY_ORDERS_COUNTER))
        except:
            return 0
    
    def get_in_progress_orders(self):
        """Получает список заказов в работе"""
        try:
            orders = self.find_elements(self.locators.IN_PROGRESS_ORDERS)
            return [order.text for order in orders]
        except:
            return []
    
    def is_order_in_progress(self, order_number):
        """Проверяет, есть ли заказ в разделе 'В работе'"""
        orders = self.get_in_progress_orders()
        return any(order_number in order for order in orders)

