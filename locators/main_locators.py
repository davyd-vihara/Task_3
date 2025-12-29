from selenium.webdriver.common.by import By

class MainPageLocators:
    """Локаторы для главной страницы"""
    
    # Шапка - используем href для более надежного поиска
    CONSTRUCTOR_BUTTON = (By.XPATH, "//a[contains(@class, 'AppHeader_header__link') and (@href='/' or @href='https://stellarburgers.education-services.ru/')]")
    ORDER_FEED_BUTTON = (By.XPATH, "//a[contains(@class, 'AppHeader_header__link') and contains(@href, '/feed')]")
    PERSONAL_ACCOUNT_BUTTON = (By.XPATH, "//a[contains(@class, 'AppHeader_header__link') and contains(@href, '/account')]")
    
    # Ингредиенты - используем класс BurgerIngredient_ingredient
    BUN_SECTION = (By.XPATH, "//h2[text()='Булки']/parent::div")
    SAUCE_SECTION = (By.XPATH, "//h2[text()='Соусы']/parent::div")
    FILLING_SECTION = (By.XPATH, "//h2[text()='Начинки']/parent::div")
    
    # Первый ингредиент из секции "Булки"
    FIRST_BUN_INGREDIENT = (By.XPATH, "//a[contains(@class, 'BurgerIngredient_ingredient')]//p[text()='Флюоресцентная булка R2-D3']/parent::a")
    FIRST_SAUCE_INGREDIENT = (By.XPATH, "(//a[contains(@class, 'BurgerIngredient_ingredient')])[6]")
    FIRST_FILLING_INGREDIENT = (By.XPATH, "(//a[contains(@class, 'BurgerIngredient_ingredient')])[11]")
    
    # Счетчик ингредиента (цифра, показывающая количество добавленных ингредиентов)
    # Относительный путь для поиска внутри элемента ингредиента
    INGREDIENT_COUNTER = (By.XPATH, ".//p[contains(@class, 'counter_counter__num')]")
    # Глобальный локатор для счетчика (используется для ожидания)
    INGREDIENT_COUNTER_VALUE = (By.XPATH, "//p[contains(@class, 'counter_counter__num')]")
    
    # Overlay (загрузка/модальное окно)
    OVERLAY = (By.XPATH, "//div[contains(@class, 'Modal_modal_overlay')]")
    
    # Модальные окна
    MODAL = (By.XPATH, "//div[contains(@class, 'Modal_modal__container')]")
    MODAL_CLOSE_BUTTON = (By.XPATH, "//button[contains(@class, 'Modal_modal__close')]")
    MODAL_TITLE = (By.XPATH, "//h2[contains(@class, 'Modal_modal__title')] | //h2[contains(text(), 'Детали ингредиента')]")
    # Название ингредиента в модальном окне (обычно это текст в параграфе или заголовке)
    MODAL_INGREDIENT_NAME = (By.XPATH, "//div[contains(@class, 'Modal_modal__container')]//p[contains(@class, 'text_type_main-medium')] | //div[contains(@class, 'Modal_modal__container')]//h3")
    
    # Конструктор - область конструктора (куда перетаскиваются ингредиенты)
    CONSTRUCTOR_AREA = (By.XPATH, "//ul[contains(@class, 'BurgerConstructor_basket__list__l9dp_')]")
    # Кнопка "Оформить заказ" (видна только для авторизованных пользователей)
    ORDER_BUTTON = (By.XPATH, "//button[contains(@class, 'button_button__33qZ0') and contains(text(), 'Оформить заказ')]")
    # Кнопка "Войти в аккаунт" (видна только для неавторизованных пользователей)
    LOGIN_BUTTON = (By.XPATH, "//button[contains(@class, 'button_button') and contains(text(), 'Войти в аккаунт')]")
    
    # Восстановление пароля
    RECOVER_PASSWORD_LINK = (By.XPATH, "//a[contains(text(), 'Восстановить пароль')]")

