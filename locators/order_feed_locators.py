from selenium.webdriver.common.by import By

class OrderFeedPageLocators:
    """Локаторы для страницы ленты заказов"""
    ORDER_FEED_TITLE = (By.XPATH, "//h1[contains(text(), 'Лента заказов')]")
    # Первый заказ в списке на странице ленты заказов
    FIRST_ORDER = (By.XPATH, "//a[contains(@class, 'OrderHistory_link')]")
    ORDER_MODAL = (By.XPATH, "//div[contains(@class, 'Modal_modal__container__Wo2l_')]")
    ORDER_NUMBER = (By.XPATH, "//p[contains(@class, 'OrderDetails_id')] | //p[contains(text(), '#')]")
    
    # Счетчики
    TOTAL_ORDERS_COUNTER = (By.XPATH, "//p[contains(text(), 'Выполнено за всё время')]/following-sibling::p")
    TODAY_ORDERS_COUNTER = (By.XPATH, "//p[contains(text(), 'Выполнено за сегодня')]/following-sibling::p")
    
    # Раздел "В работе"
    IN_PROGRESS_SECTION = (By.XPATH, "//div[contains(@class, 'OrderFeed_orderListReady__')]")
    IN_PROGRESS_ORDERS = (By.XPATH, "//div[contains(@class, 'OrderFeed_orderListReady__')]//li")

