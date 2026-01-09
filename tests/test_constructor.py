import allure
from pages.constructor_page import ConstructorPage
from pages.order_feed_page import OrderFeedPage
from pages.main_page import MainPage
from pages.login_page import LoginPage
from config.constants import Constants


@allure.feature("Основной функционал")
@allure.story("Проверка основного функционала приложения")
class TestConstructor:
    
    @allure.title("Переход по клику на 'Конструктор'")
    def test_go_to_constructor(self, driver):
        """Проверяет переход по клику на 'Конструктор'"""
        main_page = MainPage(driver)
        
        with allure.step("Загружаем главную страницу"):
            main_page.open()
            main_page.wait_for_page_load()
        
        with allure.step("Кликаем по кнопке 'Конструктор'"):
            main_page.click_constructor_button()
        
        with allure.step("Проверяем, что открылась страница конструктора"):
            constructor_page = ConstructorPage(driver)
            assert constructor_page.is_constructor_visible(), \
                f"Заголовок '{Constants.CONSTRUCTOR_TITLE}' не найден на странице конструктора"
    
    @allure.title("Переход по клику на 'Лента заказов'")
    def test_go_to_order_feed(self, driver):
        """Проверяет переход по клику на 'Лента заказов'"""
        main_page = MainPage(driver)
        
        with allure.step("Загружаем главную страницу"):
            main_page.open()
            main_page.wait_for_page_load()
        
        with allure.step("Кликаем по кнопке 'Лента заказов'"):
            main_page.click_order_feed_button()
        
        with allure.step("Проверяем, что открылась страница ленты заказов"):
            order_feed_page = OrderFeedPage(driver)
            assert order_feed_page.is_order_feed_title_visible(), \
                f"Заголовок '{Constants.ORDER_FEED_TITLE}' не найден на странице"
    
    @allure.title("Всплывающее окно с деталями ингредиента")
    def test_ingredient_modal(self, driver):
        """Проверяет открытие модального окна с деталями ингредиента"""
        main_page = MainPage(driver)
        
        with allure.step("Загружаем главную страницу"):
            main_page.open()
            main_page.wait_for_page_load()
        
        with allure.step("Переходим в конструктор"):
            main_page.click_constructor_button()
        
        with allure.step("Проверяем, что открылась страница конструктора"):
            constructor_page = ConstructorPage(driver)
            assert constructor_page.is_constructor_visible(), \
                "Заголовок 'Соберите бургер' не найден на странице конструктора"
        
        with allure.step("Кликаем на первый ингредиент из списка 'Булки'"):
            main_page.click_first_bun_ingredient()
            main_page.wait_for_element_to_be_visible(main_page.locators.MODAL, timeout=Constants.TIMEOUT_DEFAULT)
        
        with allure.step("Проверяем, что модальное окно открылось с правильными данными"):
            assert main_page.is_modal_visible(), "Модальное окно с деталями ингредиента не появилось"
            modal_title = main_page.get_modal_title()
            assert modal_title and "Детали ингредиента" in modal_title, \
                f"Заголовок 'Детали ингредиента' не найден. Найден: {modal_title}"
            ingredient_name = main_page.get_modal_ingredient_name()
            assert ingredient_name and "Флюоресцентная булка R2-D3" in ingredient_name, \
                f"Название булки 'Флюоресцентная булка R2-D3' не найдено. Найдено: {ingredient_name}"
    
    @allure.title("Закрытие модального окна крестиком")
    def test_close_modal(self, driver):
        """Проверяет закрытие модального окна кликом по крестику"""
        main_page = MainPage(driver)
        
        with allure.step("Загружаем главную страницу"):
            main_page.open()
            main_page.wait_for_page_load()
        
        with allure.step("Переходим в конструктор"):
            main_page.click_constructor_button()
        
        with allure.step("Проверяем, что открылась страница конструктора"):
            constructor_page = ConstructorPage(driver)
            assert constructor_page.is_constructor_visible(), \
                f"Заголовок '{Constants.CONSTRUCTOR_TITLE}' не найден на странице конструктора"
        
        with allure.step("Открываем модальное окно с деталями ингредиента"):
            main_page.click_first_bun_ingredient()
            main_page.wait_for_element_to_be_visible(main_page.locators.MODAL, timeout=Constants.TIMEOUT_DEFAULT)
        
        with allure.step("Проверяем, что модальное окно открылось"):
            assert main_page.is_modal_visible(), "Модальное окно с деталями ингредиента не появилось"
            modal_title = main_page.get_modal_title()
            assert modal_title and Constants.INGREDIENT_DETAILS_TITLE in modal_title, \
                f"Заголовок '{Constants.INGREDIENT_DETAILS_TITLE}' не найден. Найден: {modal_title}"
            ingredient_name = main_page.get_modal_ingredient_name()
            assert ingredient_name and Constants.FIRST_BUN_NAME in ingredient_name, \
                f"Название булки '{Constants.FIRST_BUN_NAME}' не найдено. Найдено: {ingredient_name}"
        
        with allure.step("Закрываем модальное окно кликом по крестику"):
            main_page.close_modal()
            main_page.wait_for_element_to_disappear(main_page.locators.MODAL)
        
        with allure.step("Проверяем, что модальное окно закрылось"):
            assert not main_page.is_modal_visible(), "Модальное окно не закрылось"
    
    @allure.title("Увеличение счетчика ингредиента при добавлении")
    def test_ingredient_counter_increase(self, driver):
        """Проверяет увеличение счетчика ингредиента при добавлении в заказ"""
        main_page = MainPage(driver)
        
        with allure.step("Загружаем главную страницу"):
            main_page.open()
            main_page.wait_for_page_load()
        
        with allure.step("Переходим в конструктор"):
            main_page.click_constructor_button()
        
        with allure.step("Проверяем, что открылась страница конструктора"):
            constructor_page = ConstructorPage(driver)
            assert constructor_page.is_constructor_visible(), \
                "Заголовок 'Соберите бургер' не найден на странице конструктора"
        
        with allure.step("Проверяем начальное значение счетчика"):
            initial_counter = main_page.get_ingredient_counter(main_page.locators.FIRST_BUN_INGREDIENT)
            assert initial_counter == 0, \
                f"Начальный счетчик должен быть равен нулю, но равен {initial_counter}"
        
        with allure.step("Перетаскиваем ингредиент в конструктор"):
            main_page.drag_ingredient_to_constructor(main_page.locators.FIRST_BUN_INGREDIENT)
            main_page.wait_for_ingredient_counter_not_zero(timeout=Constants.TIMEOUT_MEDIUM)
        
        with allure.step("Проверяем, что счетчик увеличился"):
            new_counter = main_page.get_ingredient_counter(main_page.locators.FIRST_BUN_INGREDIENT)
            assert new_counter > 0, \
                f"Счетчик должен быть больше нуля, но равен {new_counter}"
            assert new_counter == 2, \
                f"Счетчик должен быть равен 2 (булка добавляется дважды - верх и низ), но равен {new_counter}"
    
    @allure.title("Оформление заказа залогиненным пользователем")
    def test_create_order(self, driver, registered_user):
        """Проверяет оформление заказа залогиненным пользователем"""
        user_email = registered_user["email"]
        user_password = registered_user["password"]
        
        main_page = MainPage(driver)
        
        with allure.step("Авторизуемся в системе"):
            main_page.open()
            main_page.wait_for_page_load()
            login_page = LoginPage(driver)
            login_page.open()
            login_page.login(user_email, user_password)
            
            # Метод login() уже ждет изменения URL, поэтому просто открываем главную страницу
            main_page.open()
            main_page.wait_for_page_load()
            # Ждем авторизации через метод из Page Object
            main_page.wait_until_user_logged_in(timeout=Constants.TIMEOUT_MEDIUM)
        
        with allure.step("Переходим в конструктор"):
            main_page.click_constructor_button()
        
        with allure.step("Проверяем, что открылась страница конструктора и пользователь авторизован"):
            constructor_page = ConstructorPage(driver)
            assert constructor_page.is_constructor_visible(), \
                f"Заголовок '{Constants.CONSTRUCTOR_TITLE}' не найден на странице конструктора"
            assert main_page.is_user_logged_in(), \
                "Пользователь не авторизован. Кнопка 'Оформить заказ' не найдена."
        
        with allure.step("Добавляем ингредиент в конструктор"):
            initial_counter = main_page.get_ingredient_counter(main_page.locators.FIRST_BUN_INGREDIENT)
            main_page.drag_ingredient_to_constructor(main_page.locators.FIRST_BUN_INGREDIENT)
            main_page.wait_for_ingredient_counter_not_zero(timeout=Constants.TIMEOUT_MEDIUM)
        
        with allure.step("Проверяем, что счетчик ингредиента увеличился"):
            new_counter = main_page.get_ingredient_counter(main_page.locators.FIRST_BUN_INGREDIENT)
            assert new_counter > initial_counter, \
                f"Счетчик не изменился. Было: {initial_counter}, стало: {new_counter}"
        
        with allure.step("Оформляем заказ"):
            main_page.click_order_button()
            main_page.wait_for_order_number(timeout=Constants.TIMEOUT_MODAL_LOAD)
        
        with allure.step("Проверяем, что заказ оформлен успешно"):
            assert main_page.is_modal_visible(), "Модальное окно заказа не появилось"
            assert main_page.is_order_success_visible(), \
                "Идентификатор заказа не найден в модальном окне"
            order_number = main_page.get_order_number_from_modal(timeout=Constants.TIMEOUT_MODAL_LOAD)
            assert order_number and order_number.strip(), \
                f"Номер заказа не найден в модальном окне. Получено: {order_number}"
            assert main_page.is_order_cooking_text_visible(), \
                f"Текст '{Constants.ORDER_COOKING_TEXT}' не найден в модальном окне"
            assert main_page.is_order_wait_text_visible(), \
                f"Текст '{Constants.ORDER_WAIT_TEXT}' не найден в модальном окне"
