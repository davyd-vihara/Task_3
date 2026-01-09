from pages.base_page import BasePage
from locators.main_locators import MainPageLocators
from locators.order_feed_locators import OrderFeedPageLocators
from config.urls import Urls
from config.constants import Constants
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import allure

class MainPage(BasePage):
    """Главная страница"""
    
    def __init__(self, driver):
        super().__init__(driver, Urls.BASE_URL)
        self.locators = MainPageLocators()
    
    @allure.step("Ожидать загрузки главной страницы")
    def wait_for_page_load(self):
        """Ожидает исчезновения overlay перед взаимодействием с элементами"""
        self.wait_for_element_to_disappear(self.locators.OVERLAY, timeout=Constants.TIMEOUT_DEFAULT)
    
    @allure.step("Кликнуть по кнопке 'Конструктор'")
    def click_constructor_button(self):
        """Кликает по кнопке 'Конструктор'"""
        self.wait_for_page_load()
        self.click_by_js(self.locators.CONSTRUCTOR_BUTTON)
    
    @allure.step("Кликнуть по кнопке 'Лента заказов'")
    def click_order_feed_button(self):
        """Кликает по кнопке 'Лента заказов'"""
        self.wait_for_page_load()
        self.click_by_js(self.locators.ORDER_FEED_BUTTON)
    
    @allure.step("Кликнуть по кнопке 'Личный кабинет'")
    def click_personal_account_button(self):
        """Кликает по кнопке 'Личный кабинет'"""
        self.wait_for_page_load()
        self.click_by_js(self.locators.PERSONAL_ACCOUNT_BUTTON)
    
    @allure.step("Кликнуть по первому ингредиенту из булок")
    def click_first_bun_ingredient(self):
        """Кликает по первому ингредиенту из булок"""
        ingredient = self.find_visible_element(self.locators.FIRST_BUN_INGREDIENT, timeout=Constants.TIMEOUT_DEFAULT)
        
        # Прокручиваем элемент в видимую область
        self.execute_script("arguments[0].scrollIntoView({block: 'center'});", ingredient)
        # Ждем, пока элемент станет кликабельным после прокрутки
        wait = self.get_wait(Constants.TIMEOUT_SHORT)
        wait.until(EC.element_to_be_clickable(self.locators.FIRST_BUN_INGREDIENT))
        self.execute_script("arguments[0].click();", ingredient)
    
    @allure.step("Кликнуть по первому ингредиенту из соусов")
    def click_first_sauce_ingredient(self):
        """Кликает по первому ингредиенту из соусов"""
        self.click_by_js(self.locators.FIRST_SAUCE_INGREDIENT)
    
    @allure.step("Кликнуть по первому ингредиенту из начинок")
    def click_first_filling_ingredient(self):
        """Кликает по первому ингредиенту из начинок"""
        self.click_by_js(self.locators.FIRST_FILLING_INGREDIENT)
    
    @allure.step("Закрыть модальное окно")
    def close_modal(self):
        """Закрывает модальное окно"""
        self.click_by_js(self.locators.MODAL_CLOSE_BUTTON)
    
    @allure.step("Проверить видимость модального окна")
    def is_modal_visible(self):
        """Проверяет видимость модального окна"""
        return self.is_element_visible(self.locators.MODAL)
    
    @allure.step("Получить заголовок модального окна")
    def get_modal_title(self):
        """Получает заголовок модального окна"""
        return self.get_text(self.locators.MODAL_TITLE)
    
    @allure.step("Получить название ингредиента из модального окна")
    def get_modal_ingredient_name(self):
        """Получает название ингредиента из модального окна"""
        # Линейный сценарий без ветвлений - просто получаем текст по локатору
        return self.get_text(self.locators.MODAL_INGREDIENT_NAME)
    
    @allure.step("Перетащить ингредиент в конструктор")
    def drag_ingredient_to_constructor(self, ingredient_locator):
        """Перетаскивает ингредиент в конструктор"""
        ingredient = self.find_visible_element(ingredient_locator)
        constructor = self.find_visible_element(self.locators.CONSTRUCTOR_AREA)
        
        # Используем метод из base_page, который использует seletools для надежной работы в Firefox
        self.drag_and_drop_element(ingredient, constructor)
    
    @allure.step("Ожидать появления счетчика ингредиента")
    def wait_for_ingredient_counter_not_zero(self, timeout=None):
        """Ожидает, пока счетчик ингредиента станет больше 0"""
        if timeout is None:
            timeout = Constants.TIMEOUT_MEDIUM
        # Линейный сценарий без ветвлений - просто ждем появления счетчика
        self.get_wait(timeout).until(
            lambda d: int(
                d.find_element(*self.locators.INGREDIENT_COUNTER_VALUE).text or 0
            ) > 0
        )
    
    @allure.step("Получить счетчик ингредиента")
    def get_ingredient_counter(self, ingredient_locator):
        """Получает счетчик ингредиента"""
        ingredient = self.find_element(ingredient_locator)
        counter = ingredient.find_element(*self.locators.INGREDIENT_COUNTER)
        return int(counter.text) if counter.text else 0
    
    @allure.step("Проверить, что пользователь авторизован")
    def is_user_logged_in(self):
        """Проверяет, что пользователь авторизован (кнопка 'Оформить заказ' видна)"""
        # Упрощенная проверка: если кнопка видна - true, если нет - false
        return self.is_element_visible(self.locators.ORDER_BUTTON, timeout=Constants.TIMEOUT_MODAL_LOAD)
    
    @allure.step("Ожидать авторизации пользователя")
    def wait_until_user_logged_in(self, timeout=None):
        """Ожидает, пока пользователь станет авторизованным"""
        if timeout is None:
            timeout = Constants.TIMEOUT_MEDIUM
        wait = self.get_wait(timeout)
        return wait.until(lambda d: self.is_user_logged_in())
    
    @allure.step("Кликнуть по кнопке 'Оформить заказ'")
    def click_order_button(self):
        """Кликает по кнопке 'Оформить заказ'"""
        # Проверяем, что пользователь авторизован
        if not self.is_user_logged_in():
            raise Exception("Пользователь не авторизован. Кнопка 'Оформить заказ' не найдена.")
        self.click_by_js(self.locators.ORDER_BUTTON)
    
    @allure.step("Проверить видимость сообщения об успешном заказе")
    def is_order_success_visible(self):
        """Проверяет видимость сообщения об успешном заказе по наличию текста 'идентификатор заказа'"""
        return self.is_element_visible(OrderFeedPageLocators.ORDER_IDENTIFIER_TEXT, timeout=Constants.TIMEOUT_DEFAULT)
    
    @allure.step("Получить текст модального окна заказа")
    def get_order_modal_text(self):
        """Получает весь текст из модального окна заказа"""
        modal = self.find_element(self.locators.MODAL, timeout=Constants.TIMEOUT_DEFAULT)
        return modal.text
    
    @allure.step("Проверить наличие текста 'Ваш заказ начали готовить'")
    def is_order_cooking_text_visible(self):
        """Проверяет наличие текста 'Ваш заказ начали готовить'"""
        # Упрощенная проверка: если элемент виден - true, если нет - false
        return self.is_element_visible(OrderFeedPageLocators.ORDER_SUCCESS_TEXT)
    
    @allure.step("Проверить наличие текста 'Дождитесь готовности на орбитальной станции'")
    def is_order_wait_text_visible(self):
        """Проверяет наличие текста 'Дождитесь готовности на орбитальной станции'"""
        # Упрощенная проверка: если элемент виден - true, если нет - false
        return self.is_element_visible(OrderFeedPageLocators.ORDER_WAIT_TEXT)
    
    @allure.step("Ожидать появления и загрузки номера заказа в модальном окне")
    def wait_for_order_number(self, timeout=None):
        """Ожидает появления номера заказа в модальном окне"""
        if timeout is None:
            timeout = Constants.TIMEOUT_VERY_LONG
        
        # Ждем появления модального окна
        self.wait_for_element_to_be_visible(self.locators.MODAL, timeout=timeout)
        
        # Ждем появления текста "идентификатор заказа" (надежный маркер)
        wait = self.get_wait(timeout)
        wait.until(EC.presence_of_element_located(OrderFeedPageLocators.ORDER_IDENTIFIER_TEXT))
        
        # Ждем появления номера заказа (может появиться не сразу)
        try:
            short_wait = self.get_wait(Constants.TIMEOUT_SHORT)
            short_wait.until(EC.presence_of_element_located(OrderFeedPageLocators.ORDER_NUMBER))
        except TimeoutException:
            # Если номер не появился сразу, это не критично, так как идентификатор уже найден
            pass
    
    @allure.step("Получить номер заказа из модального окна")
    def get_order_number_from_modal(self, timeout=None):
        """Получает номер заказа из модального окна"""
        if timeout is None:
            timeout = Constants.TIMEOUT_VERY_LONG
        
        try:
            element = self.find_visible_element(OrderFeedPageLocators.ORDER_NUMBER, timeout=timeout)
            return element.text.strip() or None
        except (TimeoutException, NoSuchElementException, AttributeError):
            return None
    
    @allure.step("Кликнуть по ссылке восстановления пароля")
    def click_recover_password_link(self):
        """Кликает по ссылке восстановления пароля"""
        self.click_by_js(self.locators.RECOVER_PASSWORD_LINK)

