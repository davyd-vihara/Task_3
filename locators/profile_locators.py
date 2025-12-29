from selenium.webdriver.common.by import By

class ProfilePageLocators:
    """Локаторы для страницы личного кабинета"""
    PROFILE_LINK = (By.XPATH, "//a[contains(@href, '/account/profile')]")
    # Заголовок или элемент, указывающий что это страница профиля
    # Проверяем по URL или наличию элементов профиля
    PROFILE_PAGE_TITLE = (By.XPATH, "//a[contains(@href, '/account/profile')] | //a[contains(@href, '/account/order-history')] | //button[contains(text(), 'Выход')]")
    # Кнопка "Профиль" в меню личного кабинета
    PROFILE_BUTTON = (By.XPATH, "//a[contains(@href, '/account/profile')] | //*[contains(text(), 'Профиль')]")
    # Ссылка "История заказов" в меню профиля
    ORDER_HISTORY_LINK = (By.XPATH, "//a[contains(@href, '/account/order-history')] | //a[contains(@href, '/account/orders')] | //*[contains(text(), 'История заказов')]")
    # Кнопка "Выход" в профиле
    LOGOUT_BUTTON = (By.XPATH, "//button[contains(text(), 'Выход')]")

