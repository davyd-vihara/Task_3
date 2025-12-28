import allure
from pages.constructor_page import ConstructorPage
from pages.order_feed_page import OrderFeedPage


@allure.feature("Основной функционал")
@allure.story("Проверка основного функционала приложения")
class TestConstructor:
    
    @allure.title("Переход по клику на 'Конструктор'")
    def test_go_to_constructor(self, driver, logged_in_user):
        """Проверяет переход по клику на 'Конструктор'"""
        main_page = logged_in_user["main_page"]
        
        # Переходим на другую страницу, чтобы проверить переход обратно
        main_page.click_order_feed_button()
        
        with allure.step("Кликаем по кнопке 'Конструктор'"):
            main_page.click_constructor_button()
        
        constructor_page = ConstructorPage(driver)
        
        with allure.step("Проверяем, что открылась страница конструктора"):
            assert constructor_page.is_constructor_visible(), "Страница конструктора не открылась"
    
    @allure.title("Переход по клику на 'Лента заказов'")
    def test_go_to_order_feed(self, driver, logged_in_user):
        """Проверяет переход по клику на 'Лента заказов'"""
        main_page = logged_in_user["main_page"]
        
        with allure.step("Кликаем по кнопке 'Лента заказов'"):
            main_page.click_order_feed_button()
        
        order_feed_page = OrderFeedPage(driver)
        
        with allure.step("Проверяем, что открылась страница ленты заказов"):
            assert "feed" in order_feed_page.get_current_url(), "Страница ленты заказов не открылась"
    
    @allure.title("Всплывающее окно с деталями ингредиента")
    def test_ingredient_modal(self, driver, logged_in_user):
        """Проверяет открытие модального окна с деталями ингредиента"""
        main_page = logged_in_user["main_page"]
        
        with allure.step("Кликаем на ингредиент"):
            main_page.click_first_bun_ingredient()
        
        with allure.step("Проверяем, что появилось всплывающее окно"):
            assert main_page.is_modal_visible(), "Модальное окно с деталями ингредиента не появилось"
        
        with allure.step("Проверяем наличие заголовка в модальном окне"):
            modal_title = main_page.get_modal_title()
            assert modal_title, "Заголовок модального окна отсутствует"
    
    @allure.title("Закрытие модального окна крестиком")
    def test_close_modal(self, driver, logged_in_user):
        """Проверяет закрытие модального окна кликом по крестику"""
        main_page = logged_in_user["main_page"]
        
        # Открываем модальное окно
        main_page.click_first_bun_ingredient()
        assert main_page.is_modal_visible(), "Модальное окно не открылось"
        
        with allure.step("Кликаем по крестику для закрытия"):
            main_page.close_modal()
        
        with allure.step("Проверяем, что модальное окно закрылось"):
            # Ждем исчезновения модального окна
            main_page.wait_for_element_to_disappear(main_page.locators.MODAL)
            assert not main_page.is_modal_visible(), "Модальное окно не закрылось"
    
    @allure.title("Увеличение счетчика ингредиента при добавлении")
    def test_ingredient_counter_increase(self, driver, logged_in_user):
        """Проверяет увеличение счетчика ингредиента при добавлении в заказ"""
        main_page = logged_in_user["main_page"]
        
        # Получаем начальный счетчик
        initial_counter = main_page.get_ingredient_counter(main_page.locators.FIRST_BUN_INGREDIENT)
        
        with allure.step("Добавляем ингредиент в конструктор"):
            main_page.drag_ingredient_to_constructor(main_page.locators.FIRST_BUN_INGREDIENT)
        
        with allure.step("Проверяем увеличение счетчика"):
            # Ждем обновления счетчика
            import time
            time.sleep(1)
            new_counter = main_page.get_ingredient_counter(main_page.locators.FIRST_BUN_INGREDIENT)
            assert new_counter > initial_counter, f"Счетчик не увеличился. Было: {initial_counter}, стало: {new_counter}"
    
    @allure.title("Оформление заказа залогиненным пользователем")
    def test_create_order(self, driver, logged_in_user):
        """Проверяет оформление заказа залогиненным пользователем"""
        main_page = logged_in_user["main_page"]
        
        # Добавляем ингредиенты в конструктор
        with allure.step("Добавляем ингредиенты в конструктор"):
            main_page.drag_ingredient_to_constructor(main_page.locators.FIRST_BUN_INGREDIENT)
            import time
            time.sleep(1)
        
        with allure.step("Кликаем по кнопке 'Оформить заказ'"):
            main_page.click_order_button()
        
        with allure.step("Проверяем успешное оформление заказа"):
            # Ждем появления модального окна с номером заказа
            import time
            time.sleep(3)
            assert main_page.is_order_success_visible() or main_page.is_modal_visible(), \
                "Заказ не был оформлен или модальное окно не появилось"

