from selenium.webdriver.common.by import By

class OrderFeedPageLocators:
    """Локаторы для страницы ленты заказов"""
    ORDER_FEED_TITLE = (By.XPATH, "//h1[contains(text(), 'Лента заказов')]")
    # Первый заказ в списке на странице ленты заказов
    FIRST_ORDER = (By.XPATH, "//a[contains(@class, 'OrderHistory_link')]")
    # Модальное окно заказа
    # XPath: /html/body/div/div/section[2]/div[1]/div
    # XPath с id: //*[@id="root"]/div/section[2]/div[1]/div
    # Используем более точный путь через section[2]
    ORDER_MODAL = (By.XPATH, "//section[2]/div[1]/div")
    # Статус заказа в модальном окне
    # XPath: /html/body/div/div/section[2]/div[1]/div/p[2]
    ORDER_STATUS = (By.XPATH, "//section[2]/div[1]/div//p[contains(text(), 'Выполнен')]")
    # Номер заказа в модальном окне (в <p> с классами text text_type_digits-default)
    # Из скриншота: <p class="text text_type_digits-default mb-10 mt-5">#0<br>338801</p>
    ORDER_NUMBER = (By.XPATH, "//section[2]/div[1]/div//p[contains(@class, 'text_type_digits-default')]")
    # Заголовок заказа (название бургера) в <h2>
    # Из скриншота: <h2 class="text text_type_main-medium mb-2">Флюоресцентный бургер</h2>
    ORDER_TITLE = (By.XPATH, "//section[2]/div[1]/div//h2[contains(@class, 'text_type_main-medium')]")
    # Раздел "Состав" в модальном окне
    # Из скриншота: <p class="text text_type_main-medium mb-8">Состав</p>
    ORDER_COMPOSITION_TITLE = (By.XPATH, "//section[2]/div[1]/div//p[contains(text(), 'Состав')]")
    # Текст "идентификатор заказа"
    ORDER_IDENTIFIER_TEXT = (By.XPATH, "//p[contains(text(), 'идентификатор заказа')]")
    # Текст в модальном окне успешного заказа
    ORDER_SUCCESS_TEXT = (By.XPATH, "//p[contains(text(), 'Ваш заказ начали готовить')]")
    ORDER_WAIT_TEXT = (By.XPATH, "//p[contains(text(), 'Дождитесь готовности на орбитальной станции')]")
    
    # Счетчики
    # Счетчик "Выполнено за всё время"
    # XPath: /html/body/div/div/main/div/div/div/div[2]/p[2]
    # CSS: #root > div > main > div > div > div > div.undefined.mb-15 > p.OrderFeed_number__2MbrQ.text.text_type_digits-large
    TOTAL_ORDERS_COUNTER = (By.XPATH, "//main/div/div/div/div[2]/p[2] | //p[contains(@class, 'OrderFeed_number__') and contains(@class, 'text_type_digits-large')]")
    # Счетчик "Выполнено за сегодня"
    TODAY_ORDERS_COUNTER = (By.XPATH, "//p[contains(text(), 'Выполнено за сегодня')]/following-sibling::p")
    
    # Раздел "В работе"
    IN_PROGRESS_SECTION = (By.XPATH, "//div[contains(@class, 'OrderFeed_orderListReady__')]")
    IN_PROGRESS_ORDERS = (By.XPATH, "//div[contains(@class, 'OrderFeed_orderListReady__')]//li")

