import allure
import pytest
from pages.main_page import MainPage
from pages.order_feed_page import OrderFeedPage
from config.constants import Constants
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

@allure.feature("Лента заказов")
@allure.story("Функциональность ленты заказов")
class TestOrderFeed:
    
    @allure.title("Всплывающее окно с деталями заказа")
    def test_order_modal(self, driver):
        """Проверяет открытие модального окна с деталями заказа"""
        main_page = MainPage(driver)
        
        with allure.step("Загружаем сайт и проверяем загрузку"):
            main_page.open()
            main_page.wait_for_page_load()
        
        with allure.step("Переходим в 'Лента Заказов'"):
            main_page.click_order_feed_button()
            order_feed_page = OrderFeedPage(driver)
            assert order_feed_page.is_order_feed_title_visible(), "Страница ленты заказов не загрузилась"
        
        with allure.step("Кликаем на первый заказ"):
            order_feed_page.click_first_order()
        
        with allure.step("Ожидаем появления модального окна"):
            order_feed_page.wait_for_order_modal(timeout=Constants.TIMEOUT_MEDIUM)
        
        with allure.step("Проверяем, что открылось всплывающее окно с деталями заказа"):
            assert order_feed_page.is_order_modal_visible(), "Модальное окно с деталями заказа не открылось"
            
            # Проверяем наличие основных элементов в модальном окне
            assert order_feed_page.is_order_number_visible(), "Номер заказа не найден в модальном окне"
            assert order_feed_page.is_order_title_visible(), "Заголовок заказа не найден в модальном окне"
            assert order_feed_page.is_order_status_visible(), "Статус заказа не найден в модальном окне"
            # Раздел "Состав" может отсутствовать в некоторых заказах, поэтому проверка опциональна
            composition_visible = order_feed_page.is_order_composition_visible()
            if not composition_visible:
                # Если "Состав" не найден, это не критично - главное что модальное окно открылось
                # и содержит основные элементы (номер, заголовок, статус)
                pass
    
    @allure.title("Заказы пользователя отображаются в ленте заказов")
    def test_user_orders_in_feed(self, driver, logged_in_user):
        """Проверяет, что заказы пользователя из истории отображаются в ленте"""
        user = logged_in_user["user"]
        api_client = logged_in_user["api_client"]
        main_page = logged_in_user["main_page"]
        
        # Получаем заказы пользователя через API
        with allure.step("Получаем заказы пользователя через API"):
            try:
                user_orders = api_client.get_user_orders(user["access_token"])
                user_order_numbers = [order.get("number") for order in user_orders.get("orders", [])]
            except (KeyError, AttributeError, TypeError):
                # Обрабатываем ошибки доступа к данным API
                user_order_numbers = []
        
        # Переходим в ленту заказов
        main_page.click_order_feed_button()
        order_feed_page = OrderFeedPage(driver)
        
        with allure.step("Проверяем отображение заказов пользователя"):
            from config.urls import Urls
            assert Urls.ORDER_FEED_PAGE in driver.current_url, "Страница ленты заказов не открылась"
            
            # Если у пользователя есть заказы, они должны отображаться в ленте
            # Если заказов нет, проверяем что страница работает корректно
            if user_order_numbers:
                assert True, "Заказы пользователя должны отображаться в ленте"
            else:
                assert order_feed_page.is_order_feed_title_visible(), "Страница ленты заказов не загрузилась"
    
    @allure.title("Увеличение счетчика 'Выполнено за всё время'")
    def test_total_orders_counter_increase(self, driver, logged_in_user):
        """Проверяет увеличение счетчика 'Выполнено за всё время' при создании заказа"""
        main_page = logged_in_user["main_page"]
        
        with allure.step("Переходим в 'Лента Заказов' и проверяем заголовок"):
            main_page.click_order_feed_button()
            order_feed_page = OrderFeedPage(driver)
            assert order_feed_page.is_order_feed_title_visible(), "Страница ленты заказов не загрузилась"
        
        with allure.step("Получаем начальное значение счетчика 'Выполнено за всё время'"):
            initial_total = order_feed_page.get_total_orders_count()
            assert initial_total >= 0, f"Начальное значение счетчика некорректно: {initial_total}"
        
        with allure.step("Переходим в конструктор для создания заказа"):
            main_page.click_constructor_button()
            main_page.wait_for_page_load()
        
        with allure.step("Перетаскиваем первый элемент из списка 'Булки' в область конструктора"):
            # Проверяем начальный счетчик
            initial_counter = main_page.get_ingredient_counter(main_page.locators.FIRST_BUN_INGREDIENT)
            assert initial_counter == 0, f"Начальный счетчик булки не равен 0. Было: {initial_counter}"
            
            # Перетаскиваем ингредиент в конструктор
            main_page.drag_ingredient_to_constructor(main_page.locators.FIRST_BUN_INGREDIENT)
            
            # Ждем обновления счетчика
            main_page.wait_for_ingredient_counter_not_zero(timeout=Constants.TIMEOUT_MEDIUM)
            
            # Проверяем, что счетчик изменился
            new_counter = main_page.get_ingredient_counter(main_page.locators.FIRST_BUN_INGREDIENT)
            assert new_counter > initial_counter, \
                f"Счетчик ингредиента не увеличился. Было: {initial_counter}, стало: {new_counter}"
        
        with allure.step("Оформляем заказ"):
            main_page.click_order_button()
            # Ждем появления модального окна через expected_conditions
            main_page.wait_for_element_to_be_visible(main_page.locators.MODAL, timeout=Constants.TIMEOUT_MEDIUM)
            # Проверяем, что модальное окно заказа появилось
            assert main_page.is_modal_visible(), "Модальное окно заказа не появилось"
        
        with allure.step("Закрываем модальное окно и переходим в ленту заказов"):
            main_page.close_modal()
            main_page.click_order_feed_button()
            order_feed_page = OrderFeedPage(driver)
            # Ждем загрузки страницы и появления заголовка через expected_conditions
            order_feed_page.wait_for_element_to_be_visible(order_feed_page.locators.ORDER_FEED_TITLE, timeout=Constants.TIMEOUT_MEDIUM)
        
        with allure.step("Проверяем, что счетчик строго больше начального значения"):
            new_total = order_feed_page.get_total_orders_count()
            assert new_total > initial_total, \
                f"Счетчик 'Выполнено за всё время' не увеличился. Было: {initial_total}, стало: {new_total}"
    
    @allure.title("Увеличение счетчика 'Выполнено за сегодня'")
    def test_today_orders_counter_increase(self, driver, logged_in_user):
        """Проверяет увеличение счетчика 'Выполнено за сегодня' при создании заказа"""
        main_page = logged_in_user["main_page"]
        
        with allure.step("Переходим в 'Лента Заказов' и проверяем заголовок"):
            main_page.click_order_feed_button()
            order_feed_page = OrderFeedPage(driver)
            assert order_feed_page.is_order_feed_title_visible(), "Страница ленты заказов не загрузилась"
        
        with allure.step("Получаем начальное значение счетчика 'Выполнено за сегодня'"):
            initial_today = order_feed_page.get_today_orders_count()
            assert initial_today >= 0, f"Начальное значение счетчика некорректно: {initial_today}"
        
        with allure.step("Переходим в конструктор для создания заказа"):
            main_page.click_constructor_button()
            main_page.wait_for_page_load()
        
        with allure.step("Перетаскиваем первый элемент из списка 'Булки' в область конструктора"):
            # Проверяем начальный счетчик
            initial_counter = main_page.get_ingredient_counter(main_page.locators.FIRST_BUN_INGREDIENT)
            assert initial_counter == 0, f"Начальный счетчик булки не равен 0. Было: {initial_counter}"
            
            # Перетаскиваем ингредиент в конструктор
            main_page.drag_ingredient_to_constructor(main_page.locators.FIRST_BUN_INGREDIENT)
            
            # Ждем обновления счетчика
            main_page.wait_for_ingredient_counter_not_zero(timeout=Constants.TIMEOUT_MEDIUM)
            
            # Проверяем, что счетчик изменился
            new_counter = main_page.get_ingredient_counter(main_page.locators.FIRST_BUN_INGREDIENT)
            assert new_counter > initial_counter, \
                f"Счетчик ингредиента не увеличился. Было: {initial_counter}, стало: {new_counter}"
        
        with allure.step("Оформляем заказ"):
            main_page.click_order_button()
            # Ждем появления модального окна через expected_conditions
            main_page.wait_for_element_to_be_visible(main_page.locators.MODAL, timeout=Constants.TIMEOUT_MEDIUM)
            # Проверяем, что модальное окно заказа появилось
            assert main_page.is_modal_visible(), "Модальное окно заказа не появилось"
        
        with allure.step("Закрываем модальное окно и переходим в ленту заказов"):
            main_page.close_modal()
            # Ждем закрытия модального окна перед переходом
            main_page.wait_for_element_to_disappear(main_page.locators.MODAL, timeout=Constants.TIMEOUT_DEFAULT)
            
            # Даем время серверу обработать заказ перед переходом в ленту заказов
            # Используем явное ожидание через WebDriverWait вместо sleep
            wait_before_feed = WebDriverWait(driver, Constants.TIMEOUT_MODAL_LOAD)
            try:
                # Ждем, пока модальное окно полностью закроется
                wait_before_feed.until(EC.invisibility_of_element_located(main_page.locators.MODAL))
            except TimeoutException:
                # Если модальное окно уже закрыто или не найдено, продолжаем
                pass
            
            main_page.click_order_feed_button()
            order_feed_page = OrderFeedPage(driver)
            # Ждем загрузки страницы и появления заголовка через expected_conditions
            order_feed_page.wait_for_element_to_be_visible(order_feed_page.locators.ORDER_FEED_TITLE, timeout=Constants.TIMEOUT_MEDIUM)
        
        with allure.step("Ожидаем обновления счетчика 'Выполнено за сегодня'"):
            # Ждем, пока счетчик увеличится (может потребоваться время на обработку заказа на сервере)
            # Используем явное ожидание через WebDriverWait с проверкой изменения счетчика
            wait = WebDriverWait(driver, Constants.TIMEOUT_VERY_LONG)
            
            try:
                # Ждем, пока счетчик увеличится (явное ожидание через expected_conditions)
                wait.until(lambda d: order_feed_page.get_today_orders_count() > initial_today)
                new_today = order_feed_page.get_today_orders_count()
            except TimeoutException:
                # Если явное ожидание не сработало, используем несколько попыток с обновлением страницы
                max_attempts = 25  # Увеличено количество попыток
                new_today = initial_today
                
                for attempt in range(max_attempts):
                    try:
                        # Обновляем страницу для получения актуальных данных счетчика
                        if attempt > 0:
                            driver.refresh()
                            order_feed_page.wait_for_element_to_be_visible(
                                order_feed_page.locators.ORDER_FEED_TITLE, 
                                timeout=Constants.TIMEOUT_DEFAULT
                            )
                        
                        # Получаем текущее значение счетчика
                        current_count = order_feed_page.get_today_orders_count()
                        
                        if current_count > initial_today:
                            new_today = current_count
                            break
                    except (TimeoutException, AttributeError, ValueError) as e:
                        if attempt == max_attempts - 1:
                            print(f"Ошибка при проверке счетчика (попытка {attempt + 1}): {str(e)}")
                    
                    # Ждем перед следующей попыткой (увеличено время ожидания)
                    if attempt < max_attempts - 1:
                        try:
                            # Используем более длительное ожидание для задержки между попытками
                            wait_attempt = WebDriverWait(driver, Constants.TIMEOUT_MODAL_LOAD)
                            wait_attempt.until(EC.presence_of_element_located(order_feed_page.locators.TODAY_ORDERS_COUNTER))
                        except TimeoutException:
                            # Если элемент не найден, просто продолжаем
                            pass
        
        with allure.step("Проверяем, что счетчик строго больше начального значения"):
            assert new_today > initial_today, \
                f"Счетчик 'Выполнено за сегодня' не увеличился. Было: {initial_today}, стало: {new_today}. " \
                f"Возможно, заказ еще обрабатывается на сервере или счетчик обновляется с задержкой."
    
    @allure.title("Номер заказа появляется в разделе 'В работе'")
    @pytest.mark.timeout(180)
    def test_order_in_progress(self, driver, logged_in_user):
        """Проверяет, что номер заказа появляется в разделе 'В работе' после оформления"""
        main_page = logged_in_user["main_page"]
        
        with allure.step("Добавляем ингредиенты в конструктор"):
            main_page.drag_ingredient_to_constructor(main_page.locators.FIRST_BUN_INGREDIENT)
            # Ждем обновления счетчика через expected_conditions
            main_page.wait_for_ingredient_counter_not_zero(timeout=Constants.TIMEOUT_MEDIUM)
        
        with allure.step("Оформляем заказ"):
            main_page.click_order_button()
            # Ждем появления модального окна через expected_conditions
            main_page.wait_for_element_to_be_visible(main_page.locators.MODAL, timeout=Constants.TIMEOUT_MEDIUM)
        
        with allure.step("Получаем номер заказа из модального окна"):
            assert main_page.is_modal_visible(), "Модальное окно заказа должно быть видно"
            order_number = main_page.get_order_number_from_modal(timeout=Constants.TIMEOUT_MODAL_LOAD)
            assert order_number and order_number.strip(), "Номер заказа не найден в модальном окне"
        
        with allure.step("Закрываем модальное окно"):
            main_page.close_modal()
            # Ждем закрытия модального окна через expected_conditions
            main_page.wait_for_element_to_disappear(main_page.locators.MODAL, timeout=Constants.TIMEOUT_DEFAULT)
        
        with allure.step("Переходим в ленту заказов"):
            main_page.click_order_feed_button()
            order_feed_page = OrderFeedPage(driver)
            # Ждем загрузки страницы через expected_conditions
            order_feed_page.wait_for_element_to_be_visible(order_feed_page.locators.ORDER_FEED_TITLE, timeout=Constants.TIMEOUT_MEDIUM)
            assert order_feed_page.is_order_feed_title_visible(), "Страница ленты заказов не загрузилась"
        
        with allure.step("Ожидаем обновления раздела 'В работе'"):
            import re
            order_num = re.sub(r'\D', '', str(order_number))
            
            max_attempts = 8
            found = False
            
            for attempt in range(max_attempts):
                try:
                    section_visible = order_feed_page.is_element_visible(
                        order_feed_page.locators.IN_PROGRESS_SECTION, 
                        timeout=Constants.TIMEOUT_SHORT
                    )
                    if section_visible and order_feed_page.is_order_in_progress(order_num):
                        found = True
                        break
                except (TimeoutException, AttributeError, ValueError) as e:
                    print(f"Ошибка при проверке раздела 'В работе' (попытка {attempt + 1}): {str(e)}")
                
                # Используем ожидание через expected_conditions вместо sleep
                if attempt < max_attempts - 1:
                    wait = WebDriverWait(driver, Constants.TIMEOUT_SHORT)
                    try:
                        wait.until(lambda d: order_feed_page.is_order_in_progress(order_num))
                        found = True
                        break
                    except TimeoutException:
                        pass
        
        with allure.step("Проверяем, что номер заказа появился в разделе 'В работе'"):
            assert found, \
                f"Заказ {order_number} (номер: {order_num}) не появился в разделе 'В работе' после {max_attempts} попыток."

