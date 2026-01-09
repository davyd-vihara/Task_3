from selenium.webdriver.common.by import By

class OrderFeedPageLocators:
    """Локаторы для страницы ленты заказов"""
    ORDER_FEED_TITLE = (By.XPATH, "//h1[contains(text(), 'Лента заказов')]")
    FIRST_ORDER = (By.XPATH, "//a[contains(@class, 'OrderHistory_link')]")
    ORDER_MODAL = (By.XPATH, "//section[2]/div[1]/div")
    ORDER_MODAL_ALTERNATIVE_1 = (By.XPATH, "//*[@id='root']/div/section[2]/div[1]/div")
    ORDER_MODAL_ALTERNATIVE_2 = (By.XPATH, "//div[contains(@class, 'Modal_modal_container')]")
    ORDER_MODAL_ALTERNATIVE_3 = (By.XPATH, "//div[contains(@class, 'Modal_modal__container')]")
    ORDER_STATUS = (By.XPATH, "//section[2]/div[1]/div//p[contains(text(), 'Выполнен')]")
    ORDER_NUMBER = (By.XPATH, "//section[2]/div[1]/div//p[contains(@class, 'text_type_digits-default')]")
    ORDER_TITLE = (By.XPATH, "//section[2]/div[1]/div//h2[contains(@class, 'text_type_main-medium')]")
    ORDER_COMPOSITION_TITLE = (By.XPATH, "//section[2]/div[1]/div//p[contains(text(), 'Состав')]")
    ORDER_COMPOSITION_TITLE_ALTERNATIVE = (By.XPATH, ".//p[contains(text(), 'Состав')]")
    ORDER_COMPOSITION_TITLE_GLOBAL = (By.XPATH, "//p[contains(text(), 'Состав')]")
    ORDER_IDENTIFIER_TEXT = (By.XPATH, "//p[contains(text(), 'идентификатор заказа')]")
    ORDER_SUCCESS_TEXT = (By.XPATH, "//p[contains(text(), 'Ваш заказ начали готовить')]")
    ORDER_WAIT_TEXT = (By.XPATH, "//p[contains(text(), 'Дождитесь готовности на орбитальной станции')]")
    TOTAL_ORDERS_COUNTER = (By.XPATH, "//main/div/div/div/div[2]/p[2] | //p[contains(@class, 'OrderFeed_number__') and contains(@class, 'text_type_digits-large')]")
    TODAY_ORDERS_COUNTER = (By.XPATH, "//p[contains(text(), 'Выполнено за сегодня')]/following-sibling::p")
    IN_PROGRESS_SECTION = (By.XPATH, "//div[contains(@class, 'OrderFeed_ordersData__')] | //div[contains(text(), 'В работе:')]")
    IN_PROGRESS_ORDERS = (By.XPATH, "//div[contains(@class, 'OrderFeed_ordersData__')]//li | //div[contains(text(), 'В работе:')]//li")

