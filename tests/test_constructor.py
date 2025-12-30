import allure
from pages.constructor_page import ConstructorPage
from pages.order_feed_page import OrderFeedPage
from config.constants import Constants


@allure.feature("Основной функционал")
@allure.story("Проверка основного функционала приложения")
class TestConstructor:
    
    @allure.title("Переход по клику на 'Конструктор'")
    def test_go_to_constructor(self, driver):
        """Проверяет переход по клику на 'Конструктор'"""
        from pages.main_page import MainPage
        from pages.constructor_page import ConstructorPage
        
        main_page = MainPage(driver)
        
        with allure.step("Убедиться, что страница загружена"):
            main_page.open()
            main_page.wait_for_page_load()
        
        with allure.step("Кликаем по кнопке 'Конструктор'"):
            main_page.click_constructor_button()
        
        with allure.step("Проверяем наличие заголовка 'Соберите бургер'"):
            constructor_page = ConstructorPage(driver)
            assert constructor_page.is_constructor_visible(), \
                f"Заголовок '{Constants.CONSTRUCTOR_TITLE}' не найден на странице конструктора"
    
    @allure.title("Переход по клику на 'Лента заказов'")
    def test_go_to_order_feed(self, driver):
        """Проверяет переход по клику на 'Лента заказов'"""
        from pages.main_page import MainPage
        from pages.order_feed_page import OrderFeedPage
        
        main_page = MainPage(driver)
        
        with allure.step("Проверяем, что страница загрузилась"):
            main_page.open()
            main_page.wait_for_page_load()
        
        with allure.step("Кликаем по кнопке 'Лента заказов'"):
            main_page.click_order_feed_button()
        
        with allure.step("Проверяем, что заголовок 'Лента заказов' отображается"):
            order_feed_page = OrderFeedPage(driver)
            assert order_feed_page.is_order_feed_title_visible(), \
                f"Заголовок '{Constants.ORDER_FEED_TITLE}' не найден на странице"
    
    @allure.title("Всплывающее окно с деталями ингредиента")
    def test_ingredient_modal(self, driver):
        """Проверяет открытие модального окна с деталями ингредиента"""
        from pages.main_page import MainPage
        from pages.constructor_page import ConstructorPage
        
        main_page = MainPage(driver)
        
        with allure.step("Проверяем загрузку сайта"):
            main_page.open()
            main_page.wait_for_page_load()
        
        with allure.step("Кликаем на конструктор и проверяем наличие заголовка 'Соберите бургер'"):
            main_page.click_constructor_button()
            constructor_page = ConstructorPage(driver)
            assert constructor_page.is_constructor_visible(), \
                "Заголовок 'Соберите бургер' не найден на странице конструктора"
        
        with allure.step("Кликаем на первый элемент в списке 'Булки' - 'Флюоресцентная булка R2-D3'"):
            main_page.click_first_bun_ingredient()
        
        with allure.step("Ждем открытия модального окна и проверяем, что окно открыто"):
            import time
            time.sleep(1)  # Даем время на открытие модального окна
            assert main_page.is_modal_visible(), "Модальное окно с деталями ингредиента не появилось"
        
        with allure.step("Проверяем наличие заголовка 'Детали ингредиента'"):
            modal_title = main_page.get_modal_title()
            assert modal_title and "Детали ингредиента" in modal_title, \
                f"Заголовок 'Детали ингредиента' не найден. Найден: {modal_title}"
        
        with allure.step("Проверяем название булки 'Флюоресцентная булка R2-D3'"):
            ingredient_name = main_page.get_modal_ingredient_name()
            assert ingredient_name and "Флюоресцентная булка R2-D3" in ingredient_name, \
                f"Название булки 'Флюоресцентная булка R2-D3' не найдено. Найдено: {ingredient_name}"
    
    @allure.title("Закрытие модального окна крестиком")
    def test_close_modal(self, driver):
        """Проверяет закрытие модального окна кликом по крестику"""
        from pages.main_page import MainPage
        from pages.constructor_page import ConstructorPage
        
        main_page = MainPage(driver)
        
        with allure.step("Проверяем загрузку сайта"):
            main_page.open()
            main_page.wait_for_page_load()
        
        with allure.step("Кликаем на конструктор и проверяем наличие заголовка 'Соберите бургер'"):
            main_page.click_constructor_button()
            constructor_page = ConstructorPage(driver)
            assert constructor_page.is_constructor_visible(), \
                f"Заголовок '{Constants.CONSTRUCTOR_TITLE}' не найден на странице конструктора"
        
        with allure.step(f"Кликаем на первый элемент в списке 'Булки' - '{Constants.FIRST_BUN_NAME}'"):
            main_page.click_first_bun_ingredient()
        
        with allure.step("Ждем открытия модального окна и проверяем, что окно открыто"):
            import time
            time.sleep(Constants.TIMEOUT)
            assert main_page.is_modal_visible(), "Модальное окно с деталями ингредиента не появилось"
        
        with allure.step(f"Проверяем наличие заголовка '{Constants.INGREDIENT_DETAILS_TITLE}'"):
            modal_title = main_page.get_modal_title()
            assert modal_title and Constants.INGREDIENT_DETAILS_TITLE in modal_title, \
                f"Заголовок '{Constants.INGREDIENT_DETAILS_TITLE}' не найден. Найден: {modal_title}"
        
        with allure.step(f"Проверяем название булки '{Constants.FIRST_BUN_NAME}'"):
            ingredient_name = main_page.get_modal_ingredient_name()
            assert ingredient_name and Constants.FIRST_BUN_NAME in ingredient_name, \
                f"Название булки '{Constants.FIRST_BUN_NAME}' не найдено. Найдено: {ingredient_name}"
        
        with allure.step("Кликаем на кнопку закрытия окна (крестик)"):
            main_page.close_modal()
        
        with allure.step(f"Проверяем, что заголовка '{Constants.INGREDIENT_DETAILS_TITLE}' нет"):
            main_page.wait_for_element_to_disappear(main_page.locators.MODAL)
            assert not main_page.is_modal_visible(), "Модальное окно не закрылось"
    
    @allure.title("Увеличение счетчика ингредиента при добавлении")
    def test_ingredient_counter_increase(self, driver):
        """Проверяет увеличение счетчика ингредиента при добавлении в заказ"""
        from pages.main_page import MainPage
        from pages.constructor_page import ConstructorPage
        
        main_page = MainPage(driver)
        
        with allure.step("Загружаем сайт и проверяем загрузку"):
            main_page.open()
            main_page.wait_for_page_load()
        
        with allure.step("Кликаем на Конструктор и проверяем, что страница конструктора загружена (проверяем заголовок 'Соберите бургер')"):
            main_page.click_constructor_button()
            constructor_page = ConstructorPage(driver)
            assert constructor_page.is_constructor_visible(), \
                "Заголовок 'Соберите бургер' не найден на странице конструктора"
        
        with allure.step("Находим первый элемент и проверяем, что счетчик равен нулю"):
            initial_counter = main_page.get_ingredient_counter(main_page.locators.FIRST_BUN_INGREDIENT)
            assert initial_counter == 0, \
                f"Начальный счетчик должен быть равен нулю, но равен {initial_counter}"
        
        with allure.step("Перетаскиваем элемент в область конструктора (зажать, перетащить, отпустить в области конструктора)"):
            main_page.drag_ingredient_to_constructor(main_page.locators.FIRST_BUN_INGREDIENT)
        
        with allure.step("Ожидаем появления счетчика"):
            # Ждем, пока счетчик появится и станет больше 0
            main_page.wait_for_ingredient_counter_not_zero(timeout=10)
        
        with allure.step("Проверяем, что значение в счетчике первого элемента (булки) строго больше нуля"):
            new_counter = main_page.get_ingredient_counter(main_page.locators.FIRST_BUN_INGREDIENT)
            assert new_counter > 0, \
                f"Счетчик должен быть больше нуля, но равен {new_counter}"
            assert new_counter == 2, \
                f"Счетчик должен быть равен 2 (булка добавляется дважды - верх и низ), но равен {new_counter}"
    
    @allure.title("Оформление заказа залогиненным пользователем")
    def test_create_order(self, driver, registered_user):
        """Проверяет оформление заказа залогиненным пользователем"""
        from pages.main_page import MainPage
        from pages.constructor_page import ConstructorPage
        from pages.login_page import LoginPage
        
        main_page = MainPage(driver)
        
        with allure.step("Загрузка сайта, проверка что сайт загружен"):
            main_page.open()
            main_page.wait_for_page_load()
        
        with allure.step("Авторизуемся (используем данные из фикстуры registered_user)"):
            # Проверяем, что пользователь зарегистрирован и данные получены
            assert registered_user.get("email"), "Email пользователя не получен из фикстуры registered_user"
            assert registered_user.get("password"), "Пароль пользователя не получен из фикстуры registered_user"
            assert registered_user.get("access_token"), "Access token не получен из фикстуры registered_user - пользователь не зарегистрирован через API"
            
            user_email = registered_user["email"]
            user_password = registered_user["password"]
            
            # Проверяем, что email и password не пустые и корректны
            assert user_email and "@" in user_email, f"Некорректный email: {user_email}"
            assert user_password and len(user_password) > 0, f"Пароль пустой или некорректный: {user_password}"
            
            # Выводим информацию для отладки (в Allure отчете)
            allure.attach(
                f"Данные пользователя из фикстуры:\nEmail: {user_email}\nPassword: {user_password[:3]}***\nAccess Token: {registered_user.get('access_token')[:20] if registered_user.get('access_token') else 'None'}...",
                name="User credentials",
                attachment_type=allure.attachment_type.TEXT
            )
            
            # Открываем главную страницу
            main_page.open()
            main_page.wait_for_page_load()
            
            # Кликаем на кнопку "Войти в аккаунт" на главной странице
            login_page = LoginPage(driver)
            # Открываем страницу логина напрямую для надежности
            login_page.open()
            
            # Проверяем, что мы на странице логина
            assert login_page.is_login_form_visible(), "Форма входа не найдена"
            
            # Выполняем авторизацию используя данные из фикстуры registered_user
            login_page.login(user_email, user_password)
            
            # Ждем перехода на главную страницу
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            from selenium.webdriver.common.by import By
            from config.urls import Urls
            wait = WebDriverWait(driver, 15)
            
            # Ждем перехода на главную страницу
            wait.until(lambda d: "/login" not in d.current_url)
            
            # Открываем главную страницу после логина
            main_page.open()
            main_page.wait_for_page_load()
            
            # Даем время на сохранение токена в cookies/localStorage и обновление UI
            import time
            time.sleep(Constants.TIMEOUT)
            
            # Проверяем авторизацию
            assert main_page.is_user_logged_in(), \
                f"Авторизация не прошла. Кнопка 'Оформить заказ' не найдена после логина. " \
                f"Использованы данные из фикстуры: email={user_email}, password={user_password[:3]}***"
        
        with allure.step(f"Переходим в конструктор, проверяем что находимся в конструкторе и мы авторизованы (находим заголовок '{Constants.CONSTRUCTOR_TITLE}' и в области конструктора есть кнопка 'Оформить заказ')"):
            main_page.click_constructor_button()
            constructor_page = ConstructorPage(driver)
            assert constructor_page.is_constructor_visible(), \
                f"Заголовок '{Constants.CONSTRUCTOR_TITLE}' не найден на странице конструктора"
            
            # Проверяем, что пользователь авторизован
            assert main_page.is_user_logged_in(), \
                "Пользователь не авторизован. Кнопка 'Оформить заказ' не найдена или кнопка 'Войти в аккаунт' все еще видна."
        
        with allure.step("Добавляем первый ингредиент из списка булки (перетаскиваем в область конструктора, проверяем что изменился счетчик)"):
            initial_counter = main_page.get_ingredient_counter(main_page.locators.FIRST_BUN_INGREDIENT)
            main_page.drag_ingredient_to_constructor(main_page.locators.FIRST_BUN_INGREDIENT)
            # Ждем обновления счетчика
            main_page.wait_for_ingredient_counter_not_zero(timeout=10)
            new_counter = main_page.get_ingredient_counter(main_page.locators.FIRST_BUN_INGREDIENT)
            assert new_counter > initial_counter, \
                f"Счетчик не изменился. Было: {initial_counter}, стало: {new_counter}"
        
        with allure.step("Кликаем на кнопку 'Оформить заказ'"):
            main_page.click_order_button()
        
        with allure.step(f"Получаем модальное окно с текстом 'идентификатор заказа', 'tick animation', '{Constants.ORDER_COOKING_TEXT}', '{Constants.ORDER_WAIT_TEXT}'"):
            # Ожидаем появления и загрузки модального окна с номером заказа
            main_page.wait_for_order_number(timeout=Constants.TIMEOUT_MODAL_LOAD)
            
            # Проверяем, что модальное окно открыто
            assert main_page.is_modal_visible(), "Модальное окно заказа не появилось"
            
            # Проверяем наличие идентификатора заказа
            assert main_page.is_order_success_visible(), \
                "Идентификатор заказа не найден в модальном окне"
            
            # Получаем номер заказа
            order_number = main_page.get_order_number_from_modal(timeout=Constants.TIMEOUT_MODAL_LOAD)
            assert order_number and order_number.strip(), \
                f"Номер заказа не найден в модальном окне. Получено: {order_number}"
            
            # Проверяем наличие текста "Ваш заказ начали готовить"
            assert main_page.is_order_cooking_text_visible(), \
                f"Текст '{Constants.ORDER_COOKING_TEXT}' не найден в модальном окне"
            
            # Проверяем наличие текста "Дождитесь готовности на орбитальной станции"
            assert main_page.is_order_wait_text_visible(), \
                f"Текст '{Constants.ORDER_WAIT_TEXT}' не найден в модальном окне"
            
            # Проверяем содержимое модального окна
            modal_text = main_page.get_order_modal_text()
            assert modal_text, "Не удалось получить текст модального окна"
            assert Constants.ORDER_COOKING_TEXT in modal_text, \
                f"Текст '{Constants.ORDER_COOKING_TEXT}' не найден в модальном окне. Текст: {modal_text[:200]}"
            assert Constants.ORDER_WAIT_TEXT in modal_text, \
                f"Текст '{Constants.ORDER_WAIT_TEXT}' не найден в модальном окне. Текст: {modal_text[:200]}"

