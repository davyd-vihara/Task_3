import allure
import pytest
import re
from pages.main_page import MainPage
from pages.order_feed_page import OrderFeedPage
from config.constants import Constants
from config.urls import Urls

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
        
        with allure.step("Кликаем на первый заказ"):
            order_feed_page.click_first_order()
            order_feed_page.wait_for_order_modal(timeout=Constants.TIMEOUT_MEDIUM)
        
        with allure.step("Проверяем, что модальное окно открылось"):
            assert order_feed_page.is_order_modal_visible(), "Модальное окно с деталями заказа не открылось"
    
    @allure.title("Заказы пользователя отображаются в ленте заказов")
    def test_user_orders_in_feed(self, driver, logged_in_user):
        """Проверяет, что заказы пользователя из истории отображаются в ленте"""
        user = logged_in_user["user"]
        api_client = logged_in_user["api_client"]
        main_page = logged_in_user["main_page"]
        
        with allure.step("Переходим в ленту заказов"):
            main_page.click_order_feed_button()
        
        with allure.step("Проверяем, что открылась страница ленты заказов"):
            order_feed_page = OrderFeedPage(driver)
            assert Urls.ORDER_FEED_PAGE in order_feed_page.get_current_url(), "Страница ленты заказов не открылась"
    
    @allure.title("Увеличение счетчика 'Выполнено за всё время'")
    def test_total_orders_counter_increase(self, driver, logged_in_user):
        """Проверяет увеличение счетчика 'Выполнено за всё время' при создании заказа"""
        main_page = logged_in_user["main_page"]
        
        with allure.step("Переходим в 'Лента Заказов' и получаем начальное значение счетчика"):
            main_page.click_order_feed_button()
            order_feed_page = OrderFeedPage(driver)
            initial_total = order_feed_page.get_total_orders_count()
        
        with allure.step("Переходим в конструктор, добавляем ингредиент и оформляем заказ"):
            main_page.click_constructor_button()
            main_page.wait_for_page_load()
            main_page.drag_ingredient_to_constructor(main_page.locators.FIRST_BUN_INGREDIENT)
            main_page.wait_for_ingredient_counter_not_zero(timeout=Constants.TIMEOUT_MEDIUM)
            main_page.click_order_button()
            main_page.wait_for_element_to_be_visible(main_page.locators.MODAL, timeout=Constants.TIMEOUT_MEDIUM)
        
        with allure.step("Закрываем модальное окно и переходим в ленту заказов"):
            main_page.close_modal()
            main_page.wait_for_element_to_disappear(main_page.locators.MODAL, timeout=Constants.TIMEOUT_MODAL_LOAD)
            
            main_page.click_order_feed_button()
            order_feed_page = OrderFeedPage(driver)
            order_feed_page.wait_for_element_to_be_visible(order_feed_page.locators.ORDER_FEED_TITLE, timeout=Constants.TIMEOUT_MEDIUM)
        
        with allure.step("Ожидаем обновления счетчика 'Выполнено за всё время'"):
            order_feed_page.wait_for_total_orders_increase(initial_total, timeout=Constants.TIMEOUT_VERY_LONG)
            new_total = order_feed_page.get_total_orders_count()
        
        with allure.step("Проверяем, что счетчик 'Выполнено за всё время' увеличился"):
            assert new_total > initial_total, \
                f"Счетчик 'Выполнено за всё время' не увеличился. Было: {initial_total}, стало: {new_total}."
    
    @allure.title("Увеличение счетчика 'Выполнено за сегодня'")
    def test_today_orders_counter_increase(self, driver, logged_in_user):
        """Проверяет увеличение счетчика 'Выполнено за сегодня' при создании заказа"""
        main_page = logged_in_user["main_page"]
        
        with allure.step("Переходим в 'Лента Заказов' и получаем начальное значение счетчика"):
            main_page.click_order_feed_button()
            order_feed_page = OrderFeedPage(driver)
            initial_today = order_feed_page.get_today_orders_count()
        
        with allure.step("Переходим в конструктор, добавляем ингредиент и оформляем заказ"):
            main_page.click_constructor_button()
            main_page.wait_for_page_load()
            main_page.drag_ingredient_to_constructor(main_page.locators.FIRST_BUN_INGREDIENT)
            main_page.wait_for_ingredient_counter_not_zero(timeout=Constants.TIMEOUT_MEDIUM)
            main_page.click_order_button()
            main_page.wait_for_element_to_be_visible(main_page.locators.MODAL, timeout=Constants.TIMEOUT_MEDIUM)
        
        with allure.step("Закрываем модальное окно и переходим в ленту заказов"):
            main_page.close_modal()
            main_page.wait_for_element_to_disappear(main_page.locators.MODAL, timeout=Constants.TIMEOUT_MODAL_LOAD)
            
            main_page.click_order_feed_button()
            order_feed_page = OrderFeedPage(driver)
            order_feed_page.wait_for_element_to_be_visible(order_feed_page.locators.ORDER_FEED_TITLE, timeout=Constants.TIMEOUT_MEDIUM)
        
        with allure.step("Ожидаем обновления счетчика 'Выполнено за сегодня'"):
            order_feed_page.wait_for_today_orders_increase(initial_today, timeout=Constants.TIMEOUT_VERY_LONG)
            new_today = order_feed_page.get_today_orders_count()
        
        with allure.step("Проверяем, что счетчик 'Выполнено за сегодня' увеличился"):
            assert new_today > initial_today, \
                f"Счетчик 'Выполнено за сегодня' не увеличился. Было: {initial_today}, стало: {new_today}."
    
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
        
        with allure.step("Получаем номер заказа, закрываем модальное окно и переходим в ленту заказов"):
            order_number = main_page.get_order_number_from_modal(timeout=Constants.TIMEOUT_MODAL_LOAD)
            main_page.close_modal()
            main_page.wait_for_element_to_disappear(main_page.locators.MODAL, timeout=Constants.TIMEOUT_DEFAULT)
            main_page.click_order_feed_button()
            order_feed_page = OrderFeedPage(driver)
            order_feed_page.wait_for_element_to_be_visible(order_feed_page.locators.ORDER_FEED_TITLE, timeout=Constants.TIMEOUT_MEDIUM)
        
        with allure.step("Ожидаем обновления раздела 'В работе'"):
            order_num = re.sub(r'\D', '', str(order_number))
            order_feed_page.wait_for_order_in_progress(order_num, timeout=Constants.TIMEOUT_VERY_LONG)
        
        with allure.step("Проверяем, что заказ появился в разделе 'В работе'"):
            assert order_feed_page.is_order_in_progress(order_num), \
                f"Заказ {order_number} (номер: {order_num}) не появился в разделе 'В работе'."

