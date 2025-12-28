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
    INGREDIENT_COUNTER = (By.XPATH, ".//div[contains(@class, 'counter_counter')]")
    
    # Модальные окна
    MODAL = (By.XPATH, "//div[contains(@class, 'Modal_modal__container')]")
    MODAL_CLOSE_BUTTON = (By.XPATH, "//button[contains(@class, 'Modal_modal__close')]")
    MODAL_TITLE = (By.XPATH, "//h2[contains(@class, 'Modal_modal__title')] | //h2[contains(text(), 'Детали ингредиента')]")
    
    # Конструктор - область конструктора (куда перетаскиваются ингредиенты)
    CONSTRUCTOR_AREA = (By.XPATH, "//ul[contains(@class, 'BurgerConstructor_basket__list__l9dp_')]")
    # Кнопка "Оформить заказ"
    ORDER_BUTTON = (By.XPATH, "//button[contains(@class, 'button_button__33qZ0') and contains(text(), 'Оформить заказ')]")
    
    # Восстановление пароля
    RECOVER_PASSWORD_LINK = (By.XPATH, "//a[contains(text(), 'Восстановить пароль')]")

