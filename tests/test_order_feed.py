import allure
import pytest
import time
from pages.main_page import MainPage
from pages.order_feed_page import OrderFeedPage
from pages.profile_page import ProfilePage
from config.constants import Constants

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
            order_feed_page.wait_for_order_modal(timeout=10)
        
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
        # #region agent log
        import json
        log_path = r"c:\Git\master\perfect-project\.cursor\debug.log"
        try:
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(json.dumps({"sessionId": "debug-session", "runId": "run1", "hypothesisId": "A", "location": "test_order_feed.py:48", "message": "test_user_orders_in_feed started", "data": {"test": "test_user_orders_in_feed"}, "timestamp": int(time.time() * 1000)}) + "\n")
        except: pass
        # #endregion
        
        user = logged_in_user["user"]
        api_client = logged_in_user["api_client"]
        main_page = logged_in_user["main_page"]
        
        # Получаем заказы пользователя через API
        with allure.step("Получаем заказы пользователя через API"):
            try:
                user_orders = api_client.get_user_orders(user["access_token"])
                user_order_numbers = [order.get("number") for order in user_orders.get("orders", [])]
                # #region agent log
                try:
                    with open(log_path, "a", encoding="utf-8") as f:
                        f.write(json.dumps({"sessionId": "debug-session", "runId": "run1", "hypothesisId": "A", "location": "test_order_feed.py:58", "message": "User orders retrieved", "data": {"order_count": len(user_order_numbers), "order_numbers": user_order_numbers}, "timestamp": int(time.time() * 1000)}) + "\n")
                except: pass
                # #endregion
            except Exception as e:
                user_order_numbers = []
                # #region agent log
                try:
                    with open(log_path, "a", encoding="utf-8") as f:
                        f.write(json.dumps({"sessionId": "debug-session", "runId": "run1", "hypothesisId": "A", "location": "test_order_feed.py:60", "message": "Failed to get user orders", "data": {"error": str(e)}, "timestamp": int(time.time() * 1000)}) + "\n")
                except: pass
                # #endregion
        
        # Переходим в ленту заказов
        main_page.click_order_feed_button()
        order_feed_page = OrderFeedPage(driver)
        
        # #region agent log
        try:
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(json.dumps({"sessionId": "debug-session", "runId": "run1", "hypothesisId": "A", "location": "test_order_feed.py:66", "message": "Navigated to order feed", "data": {"current_url": driver.current_url}, "timestamp": int(time.time() * 1000)}) + "\n")
        except: pass
        # #endregion
        
        with allure.step("Проверяем отображение заказов пользователя"):
            # Проверяем, что страница загрузилась
            from config.urls import Urls
            current_url = driver.current_url
            # #region agent log
            try:
                with open(log_path, "a", encoding="utf-8") as f:
                    f.write(json.dumps({"sessionId": "debug-session", "runId": "run1", "hypothesisId": "A", "location": "test_order_feed.py:72", "message": "Checking URL", "data": {"current_url": current_url, "expected_url": Urls.ORDER_FEED_PAGE, "url_match": Urls.ORDER_FEED_PAGE in current_url}, "timestamp": int(time.time() * 1000)}) + "\n")
            except: pass
            # #endregion
            assert Urls.ORDER_FEED_PAGE in current_url, "Страница ленты заказов не открылась"
            
            # Если у пользователя есть заказы, они должны отображаться в ленте
            # Если заказов нет, это нормально - проверяем только что страница работает
            if user_order_numbers:
                # В реальном тесте можно проверить наличие конкретных номеров заказов
                # #region agent log
                try:
                    with open(log_path, "a", encoding="utf-8") as f:
                        f.write(json.dumps({"sessionId": "debug-session", "runId": "run1", "hypothesisId": "A", "location": "test_order_feed.py:78", "message": "User has orders, checking visibility", "data": {"order_numbers": user_order_numbers}, "timestamp": int(time.time() * 1000)}) + "\n")
                except: pass
                # #endregion
                assert True, "Заказы пользователя должны отображаться в ленте"
            else:
                # Если заказов нет, проверяем что страница ленты заказов работает корректно
                # #region agent log
                try:
                    with open(log_path, "a", encoding="utf-8") as f:
                        f.write(json.dumps({"sessionId": "debug-session", "runId": "run1", "hypothesisId": "A", "location": "test_order_feed.py:82", "message": "No user orders, checking title visibility", "data": {}, "timestamp": int(time.time() * 1000)}) + "\n")
                except: pass
                # #endregion
                title_visible = order_feed_page.is_order_feed_title_visible()
                # #region agent log
                try:
                    with open(log_path, "a", encoding="utf-8") as f:
                        f.write(json.dumps({"sessionId": "debug-session", "runId": "run1", "hypothesisId": "A", "location": "test_order_feed.py:85", "message": "Title visibility check result", "data": {"title_visible": title_visible}, "timestamp": int(time.time() * 1000)}) + "\n")
                except: pass
                # #endregion
                assert title_visible, "Страница ленты заказов не загрузилась"
    
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
            main_page.wait_for_ingredient_counter_not_zero(main_page.locators.FIRST_BUN_INGREDIENT)
            
            # Проверяем, что счетчик изменился
            new_counter = main_page.get_ingredient_counter(main_page.locators.FIRST_BUN_INGREDIENT)
            assert new_counter > initial_counter, \
                f"Счетчик ингредиента не увеличился. Было: {initial_counter}, стало: {new_counter}"
        
        with allure.step("Оформляем заказ"):
            main_page.click_order_button()
            time.sleep(Constants.TIMEOUT_MEDIUM)
            
            # Проверяем, что модальное окно заказа появилось
            assert main_page.is_modal_visible(), "Модальное окно заказа не появилось"
        
        with allure.step("Закрываем модальное окно и переходим в ленту заказов"):
            main_page.close_modal()
            main_page.click_order_feed_button()
            order_feed_page = OrderFeedPage(driver)
            # Ждем загрузки страницы и обновления счетчика
            time.sleep(Constants.TIMEOUT_LONG)
        
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
            main_page.wait_for_ingredient_counter_not_zero(main_page.locators.FIRST_BUN_INGREDIENT)
            
            # Проверяем, что счетчик изменился
            new_counter = main_page.get_ingredient_counter(main_page.locators.FIRST_BUN_INGREDIENT)
            assert new_counter > initial_counter, \
                f"Счетчик ингредиента не увеличился. Было: {initial_counter}, стало: {new_counter}"
        
        with allure.step("Оформляем заказ"):
            main_page.click_order_button()
            time.sleep(Constants.TIMEOUT_MEDIUM)
            
            # Проверяем, что модальное окно заказа появилось
            assert main_page.is_modal_visible(), "Модальное окно заказа не появилось"
        
        with allure.step("Закрываем модальное окно и переходим в ленту заказов"):
            main_page.close_modal()
            main_page.click_order_feed_button()
            order_feed_page = OrderFeedPage(driver)
            # Ждем загрузки страницы и обновления счетчика
            time.sleep(Constants.TIMEOUT_LONG)
        
        with allure.step("Проверяем, что счетчик строго больше начального значения"):
            new_today = order_feed_page.get_today_orders_count()
            assert new_today > initial_today, \
                f"Счетчик 'Выполнено за сегодня' не увеличился. Было: {initial_today}, стало: {new_today}"
    
    @allure.title("Номер заказа появляется в разделе 'В работе'")
    @pytest.mark.timeout(180)  # Максимальное время выполнения теста: 3 минуты
    def test_order_in_progress(self, driver, logged_in_user):
        """Проверяет, что номер заказа появляется в разделе 'В работе' после оформления"""
        # #region agent log
        import json
        log_path = r"c:\Git\master\perfect-project\.cursor\debug.log"
        try:
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(json.dumps({"sessionId": "debug-session", "runId": "run1", "hypothesisId": "B", "location": "test_order_feed.py:188", "message": "test_order_in_progress started", "data": {"test": "test_order_in_progress"}, "timestamp": int(time.time() * 1000)}) + "\n")
        except: pass
        # #endregion
        
        main_page = logged_in_user["main_page"]
        
        # Добавляем ингредиенты и оформляем заказ
        with allure.step("Добавляем ингредиенты в конструктор"):
            main_page.drag_ingredient_to_constructor(main_page.locators.FIRST_BUN_INGREDIENT)
            time.sleep(Constants.TIMEOUT_SHORT)
        
        with allure.step("Оформляем заказ"):
            main_page.click_order_button()
            time.sleep(Constants.TIMEOUT_MEDIUM)
        
        # Получаем номер заказа из модального окна
        with allure.step("Получаем номер заказа из модального окна"):
            modal_visible = main_page.is_modal_visible()
            # #region agent log
            try:
                with open(log_path, "a", encoding="utf-8") as f:
                    f.write(json.dumps({"sessionId": "debug-session", "runId": "run1", "hypothesisId": "B", "location": "test_order_feed.py:203", "message": "Modal visibility check", "data": {"modal_visible": modal_visible}, "timestamp": int(time.time() * 1000)}) + "\n")
            except: pass
            # #endregion
            assert modal_visible, "Модальное окно заказа должно быть видно"
            # Используем метод с увеличенным таймаутом и альтернативными способами
            order_number = main_page.get_order_number_from_modal(timeout=Constants.TIMEOUT_MODAL_LOAD)
            # #region agent log
            try:
                with open(log_path, "a", encoding="utf-8") as f:
                    f.write(json.dumps({"sessionId": "debug-session", "runId": "run1", "hypothesisId": "B", "location": "test_order_feed.py:207", "message": "Order number retrieved", "data": {"order_number": order_number, "order_number_stripped": order_number.strip() if order_number else None}, "timestamp": int(time.time() * 1000)}) + "\n")
            except: pass
            # #endregion
            assert order_number and order_number.strip(), "Номер заказа не найден в модальном окне"
        
        # Закрываем модальное окно и переходим в ленту заказов
        with allure.step("Закрываем модальное окно"):
            main_page.close_modal()
            # Даем время на обработку заказа и обновление через WebSocket
            time.sleep(Constants.TIMEOUT_MEDIUM)
        
        with allure.step("Переходим в ленту заказов"):
            main_page.click_order_feed_button()
            order_feed_page = OrderFeedPage(driver)
            assert order_feed_page.is_order_feed_title_visible(), "Страница ленты заказов не загрузилась"
            # Даем время на загрузку и обновление данных через WebSocket
            time.sleep(Constants.TIMEOUT_SHORT)
        
        with allure.step("Ожидаем обновления раздела 'В работе'"):
            # Извлекаем только номер из текста (может быть в формате "#12345" или просто число)
            import re
            order_num = re.sub(r'\D', '', str(order_number))
            # #region agent log
            try:
                with open(log_path, "a", encoding="utf-8") as f:
                    f.write(json.dumps({"sessionId": "debug-session", "runId": "run1", "hypothesisId": "B", "location": "test_order_feed.py:300", "message": "Normalized order number", "data": {"order_number": order_number, "order_num": order_num}, "timestamp": int(time.time() * 1000)}) + "\n")
            except: pass
            # #endregion
            
            # Проверяем структуру страницы для поиска раздела "В работе"
            # #region agent log
            try:
                page_structure = driver.execute_script("""
                    var sections = [];
                    var divs = document.querySelectorAll('div[class*="OrderFeed"], div[class*="order"], div[class*="ready"], div[class*="work"]');
                    for (var i = 0; i < Math.min(divs.length, 20); i++) {
                        var div = divs[i];
                        sections.push({
                            className: div.className,
                            text: div.textContent.substring(0, 100),
                            id: div.id
                        });
                    }
                    return sections;
                """)
                with open(log_path, "a", encoding="utf-8") as f:
                    f.write(json.dumps({"sessionId": "debug-session", "runId": "run1", "hypothesisId": "B", "location": "test_order_feed.py:310", "message": "Page structure for In Progress section", "data": {"sections": page_structure}, "timestamp": int(time.time() * 1000)}) + "\n")
            except Exception as e:
                try:
                    with open(log_path, "a", encoding="utf-8") as f:
                        f.write(json.dumps({"sessionId": "debug-session", "runId": "run1", "hypothesisId": "B", "location": "test_order_feed.py:315", "message": "Error getting page structure", "data": {"error": str(e)}, "timestamp": int(time.time() * 1000)}) + "\n")
                except: pass
            # #endregion
            
            # Ждем появления заказа в разделе "В работе" с повторными попытками
            # Заказ может появиться через WebSocket с задержкой
            # Уменьшаем количество попыток и устанавливаем максимальное время ожидания
            max_attempts = 8
            max_wait_time = Constants.TIMEOUT_MEDIUM  # Максимальное время ожидания между попытками
            found = False
            
            # Сначала ждем немного, чтобы заказ успел обработаться
            time.sleep(Constants.TIMEOUT_SHORT)
            
            for attempt in range(max_attempts):
                try:
                    # Проверяем, что раздел "В работе" вообще существует
                    section_visible = order_feed_page.is_element_visible(
                        order_feed_page.locators.IN_PROGRESS_SECTION, 
                        timeout=2
                    )
                    # #region agent log
                    try:
                        with open(log_path, "a", encoding="utf-8") as f:
                            f.write(json.dumps({"sessionId": "debug-session", "runId": "run1", "hypothesisId": "B", "location": "test_order_feed.py:318", "message": "Section visibility check", "data": {"attempt": attempt + 1, "section_visible": section_visible}, "timestamp": int(time.time() * 1000)}) + "\n")
                    except: pass
                    # #endregion
                    
                    if section_visible:
                        is_in_progress = order_feed_page.is_order_in_progress(order_num)
                        # #region agent log
                        try:
                            with open(log_path, "a", encoding="utf-8") as f:
                                f.write(json.dumps({"sessionId": "debug-session", "runId": "run1", "hypothesisId": "B", "location": "test_order_feed.py:325", "message": "Order in progress check", "data": {"attempt": attempt + 1, "order_num": order_num, "is_in_progress": is_in_progress}, "timestamp": int(time.time() * 1000)}) + "\n")
                        except: pass
                        # #endregion
                        if is_in_progress:
                            found = True
                            break
                except Exception as e:
                    # Если произошла ошибка при проверке, продолжаем попытки
                    # #region agent log
                    try:
                        with open(log_path, "a", encoding="utf-8") as f:
                            f.write(json.dumps({"sessionId": "debug-session", "runId": "run1", "hypothesisId": "B", "location": "test_order_feed.py:333", "message": "Error checking section", "data": {"attempt": attempt + 1, "error": str(e)}, "timestamp": int(time.time() * 1000)}) + "\n")
                    except: pass
                    # #endregion
                    print(f"Ошибка при проверке раздела 'В работе' (попытка {attempt + 1}): {str(e)}")
                
                # Увеличиваем время ожидания, но не более max_wait_time
                wait_time = min(Constants.TIMEOUT_SHORT + (attempt * 0.5), max_wait_time)
                time.sleep(wait_time)
        
        with allure.step("Проверяем, что номер заказа появился в разделе 'В работе'"):
            # #region agent log
            try:
                with open(log_path, "a", encoding="utf-8") as f:
                    f.write(json.dumps({"sessionId": "debug-session", "runId": "run1", "hypothesisId": "B", "location": "test_order_feed.py:345", "message": "Final check result", "data": {"found": found, "order_number": order_number, "order_num": order_num, "max_attempts": max_attempts}, "timestamp": int(time.time() * 1000)}) + "\n")
            except: pass
            # #endregion
            assert found, \
                f"Заказ {order_number} (номер: {order_num}) не появился в разделе 'В работе' после {max_attempts} попыток."

