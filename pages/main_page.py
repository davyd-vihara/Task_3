from pages.base_page import BasePage
from locators.main_locators import MainPageLocators
from utils.config import Config
from selenium.webdriver.common.by import By

class MainPage(BasePage):
    """Главная страница"""
    
    def __init__(self, driver):
        super().__init__(driver, Config.BASE_URL)
        self.locators = MainPageLocators()
    
    def click_constructor_button(self):
        """Кликает по кнопке 'Конструктор'"""
        self.click(self.locators.CONSTRUCTOR_BUTTON)
    
    def click_order_feed_button(self):
        """Кликает по кнопке 'Лента заказов'"""
        self.click(self.locators.ORDER_FEED_BUTTON)
    
    def click_personal_account_button(self):
        """Кликает по кнопке 'Личный кабинет'"""
        self.click(self.locators.PERSONAL_ACCOUNT_BUTTON)
    
    def click_first_bun_ingredient(self):
        """Кликает по первому ингредиенту из булок (Флюоресцентная булка R2-D3)"""
        import time
        from pages.base_page import _log_debug
        
        # #region agent log
        _log_debug("debug-session", "run1", "A", "main_page.py:click_first_bun_ingredient", "Начало поиска ингредиента", {
            "locator": str(self.locators.FIRST_BUN_INGREDIENT),
            "url": self.driver.current_url
        })
        # #endregion
        
        time.sleep(2)  # Ждем загрузки страницы
        
        # #region agent log
        # Проверяем наличие всех ингредиентов на странице
        all_ingredients = self.driver.find_elements("xpath", "//a[contains(@class, 'BurgerIngredient_ingredient')]")
        bun_texts = []
        for ing in all_ingredients[:5]:  # Первые 5 для проверки
            try:
                p_elements = ing.find_elements("xpath", ".//p")
                for p in p_elements:
                    if p.text:
                        bun_texts.append(p.text)
            except:
                pass
        _log_debug("debug-session", "run1", "A", "main_page.py:click_first_bun_ingredient", "Найдено ингредиентов на странице", {
            "total_ingredients": len(all_ingredients),
            "first_5_texts": bun_texts
        })
        # #endregion
        
        # Пробуем найти ингредиент по точному тексту, если не найдем - используем первый из булок
        try:
            ingredient = self.find_visible_element(self.locators.FIRST_BUN_INGREDIENT, timeout=5)
        except:
            # Если не нашли по точному тексту, ищем первый ингредиент из булок
            # #region agent log
            _log_debug("debug-session", "run1", "A", "main_page.py:click_first_bun_ingredient", "Не найден по точному тексту, ищем первый ингредиент", {
                "fallback_locator": "(//a[contains(@class, 'BurgerIngredient_ingredient')])[1]"
            })
            # #endregion
            ingredient = self.find_visible_element((By.XPATH, "(//a[contains(@class, 'BurgerIngredient_ingredient')])[1]"), timeout=10)
        # Прокручиваем к ингредиенту и кликаем
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", ingredient)
        time.sleep(0.5)
        ingredient.click()
    
    def click_first_sauce_ingredient(self):
        """Кликает по первому ингредиенту из соусов"""
        self.click(self.locators.FIRST_SAUCE_INGREDIENT)
    
    def click_first_filling_ingredient(self):
        """Кликает по первому ингредиенту из начинок"""
        self.click(self.locators.FIRST_FILLING_INGREDIENT)
    
    def close_modal(self):
        """Закрывает модальное окно"""
        self.click(self.locators.MODAL_CLOSE_BUTTON)
    
    def is_modal_visible(self):
        """Проверяет видимость модального окна"""
        return self.is_element_visible(self.locators.MODAL)
    
    def get_modal_title(self):
        """Получает заголовок модального окна"""
        return self.get_text(self.locators.MODAL_TITLE)
    
    def drag_ingredient_to_constructor(self, ingredient_locator):
        """Перетаскивает ингредиент в конструктор"""
        from selenium.webdriver.common.action_chains import ActionChains
        from pages.base_page import _log_debug
        
        # #region agent log
        _log_debug("debug-session", "run1", "A", "main_page.py:drag_ingredient_to_constructor", "Начало перетаскивания", {
            "ingredient_locator": str(ingredient_locator),
            "constructor_locator": str(self.locators.CONSTRUCTOR_AREA)
        })
        # #endregion
        
        ingredient = self.find_visible_element(ingredient_locator)
        constructor = self.find_visible_element(self.locators.CONSTRUCTOR_AREA)
        
        # #region agent log
        _log_debug("debug-session", "run1", "A", "main_page.py:drag_ingredient_to_constructor", "Элементы найдены, выполнение drag_and_drop", {
            "ingredient_tag": ingredient.tag_name,
            "constructor_tag": constructor.tag_name
        })
        # #endregion
        
        ActionChains(self.driver).drag_and_drop(ingredient, constructor).perform()
    
    def get_ingredient_counter(self, ingredient_locator):
        """Получает счетчик ингредиента"""
        try:
            ingredient = self.find_element(ingredient_locator)
            counter = ingredient.find_element(*self.locators.INGREDIENT_COUNTER)
            return int(counter.text)
        except:
            return 0
    
    def click_order_button(self):
        """Кликает по кнопке 'Оформить заказ'"""
        self.click(self.locators.ORDER_BUTTON)
    
    def is_order_success_visible(self):
        """Проверяет видимость сообщения об успешном заказе"""
        # Ищем модальное окно с номером заказа
        try:
            from locators.order_feed_locators import OrderFeedPageLocators
            return self.is_element_visible(OrderFeedPageLocators.ORDER_NUMBER)
        except:
            return False
    
    def click_recover_password_link(self):
        """Кликает по ссылке восстановления пароля"""
        self.click(self.locators.RECOVER_PASSWORD_LINK)

