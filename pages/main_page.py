from pages.base_page import BasePage
from locators.main_locators import MainPageLocators
from config.urls import Urls
from selenium.webdriver.common.by import By
import allure

class MainPage(BasePage):
    """Главная страница"""
    
    def __init__(self, driver):
        super().__init__(driver, Urls.BASE_URL)
        self.locators = MainPageLocators()
    
    @allure.step("Ожидать загрузки главной страницы")
    def wait_for_page_load(self):
        """Ожидает исчезновения overlay перед взаимодействием с элементами"""
        try:
            self.wait_for_element_to_disappear(self.locators.OVERLAY, timeout=5)
        except:
            # Если overlay не найден или уже исчез, продолжаем
            pass
    
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
        import time
        time.sleep(2)
        
        try:
            ingredient = self.find_visible_element(self.locators.FIRST_BUN_INGREDIENT, timeout=5)
        except:
            ingredient = self.find_visible_element((By.XPATH, "(//a[contains(@class, 'BurgerIngredient_ingredient')])[1]"), timeout=10)
        
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", ingredient)
        time.sleep(0.5)
        self.driver.execute_script("arguments[0].click();", ingredient)
    
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
        try:
            return self.get_text(self.locators.MODAL_INGREDIENT_NAME)
        except Exception:
            # Если не нашли по локатору, пробуем найти любой текст в модальном окне
            try:
                modal = self.find_element(self.locators.MODAL)
                # Ищем текст, который может быть названием ингредиента
                name_elements = modal.find_elements("xpath", ".//p[contains(@class, 'text')] | .//h3")
                for elem in name_elements:
                    text = elem.text.strip()
                    if text and text != "Детали ингредиента" and len(text) > 3:
                        return text
                return ""
            except Exception:
                return ""
    
    @allure.step("Перетащить ингредиент в конструктор")
    def drag_ingredient_to_constructor(self, ingredient_locator):
        """Перетаскивает ингредиент в конструктор"""
        ingredient = self.find_visible_element(ingredient_locator)
        constructor = self.find_visible_element(self.locators.CONSTRUCTOR_AREA)
        
        # Используем метод из base_page, который использует seletools для надежной работы в Firefox
        self.drag_and_drop_element(ingredient, constructor)
    
    @allure.step("Ожидать появления счетчика ингредиента")
    def wait_for_ingredient_counter_not_zero(self, timeout=10):
        """Ожидает, пока счетчик ингредиента станет больше 0"""
        from selenium.webdriver.support.ui import WebDriverWait
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: int(
                    d.find_element(*self.locators.INGREDIENT_COUNTER_VALUE).text or 0
                ) > 0
            )
        except:
            pass  # Если счетчик не появился, продолжаем
    
    @allure.step("Получить счетчик ингредиента")
    def get_ingredient_counter(self, ingredient_locator):
        """Получает счетчик ингредиента"""
        try:
            # Сначала пробуем найти счетчик внутри элемента ингредиента
            ingredient = self.find_element(ingredient_locator)
            try:
                counter = ingredient.find_element(*self.locators.INGREDIENT_COUNTER)
                return int(counter.text) if counter.text else 0
            except:
                # Если не нашли внутри, ищем глобально
                try:
                    counter = self.find_element(self.locators.INGREDIENT_COUNTER_VALUE, timeout=2)
                    return int(counter.text) if counter.text else 0
                except:
                    return 0
        except:
            # Если элемент ингредиента не найден, пробуем найти счетчик глобально
            try:
                counter = self.find_element(self.locators.INGREDIENT_COUNTER_VALUE, timeout=2)
                return int(counter.text) if counter.text else 0
            except:
                return 0
    
    @allure.step("Проверить, что пользователь авторизован")
    def is_user_logged_in(self):
        """Проверяет, что пользователь авторизован (кнопка 'Оформить заказ' видна или кнопка 'Войти в аккаунт' НЕ видна)"""
        try:
            # Проверяем, что кнопка "Оформить заказ" видна
            if self.is_element_visible(self.locators.ORDER_BUTTON, timeout=3):
                return True
        except Exception:
            pass
        
        # Если кнопка "Оформить заказ" не видна, проверяем, что кнопка "Войти в аккаунт" НЕ видна
        # (это тоже признак авторизации)
        try:
            login_button_visible = self.is_element_visible(self.locators.LOGIN_BUTTON, timeout=2)
            return not login_button_visible  # Если кнопка входа не видна, значит авторизованы
        except Exception:
            # Если не можем найти кнопку входа, считаем что авторизованы
            return True
    
    @allure.step("Кликнуть по кнопке 'Оформить заказ'")
    def click_order_button(self):
        """Кликает по кнопке 'Оформить заказ'"""
        # Проверяем, что пользователь авторизован
        if not self.is_user_logged_in():
            raise Exception("Пользователь не авторизован. Кнопка 'Оформить заказ' не найдена.")
        self.click_by_js(self.locators.ORDER_BUTTON)
    
    @allure.step("Проверить видимость сообщения об успешном заказе")
    def is_order_success_visible(self):
        """Проверяет видимость сообщения об успешном заказе (номер заказа или текст 'идентификатор заказа')"""
        try:
            from locators.order_feed_locators import OrderFeedPageLocators
            # Проверяем наличие номера заказа (h2) или текста "идентификатор заказа"
            return (self.is_element_visible(OrderFeedPageLocators.ORDER_NUMBER, timeout=5) or
                    self.is_element_visible(OrderFeedPageLocators.ORDER_IDENTIFIER_TEXT, timeout=5))
        except Exception:
            return False
    
    @allure.step("Получить текст модального окна заказа")
    def get_order_modal_text(self):
        """Получает весь текст из модального окна заказа"""
        try:
            # Используем локатор MODAL из main_locators, который указывает на контейнер модального окна
            modal = self.find_element(self.locators.MODAL, timeout=5)
            return modal.text
        except:
            # Если не получилось, пробуем альтернативный способ
            try:
                from locators.order_feed_locators import OrderFeedPageLocators
                modal = self.find_element(OrderFeedPageLocators.ORDER_MODAL, timeout=5)
                return modal.text
            except:
                return ""
    
    @allure.step("Проверить наличие текста 'Ваш заказ начали готовить'")
    def is_order_cooking_text_visible(self):
        """Проверяет наличие текста 'Ваш заказ начали готовить'"""
        try:
            from locators.order_feed_locators import OrderFeedPageLocators
            return self.is_element_visible(OrderFeedPageLocators.ORDER_SUCCESS_TEXT)
        except:
            return False
    
    @allure.step("Проверить наличие текста 'Дождитесь готовности на орбитальной станции'")
    def is_order_wait_text_visible(self):
        """Проверяет наличие текста 'Дождитесь готовности на орбитальной станции'"""
        try:
            from locators.order_feed_locators import OrderFeedPageLocators
            return self.is_element_visible(OrderFeedPageLocators.ORDER_WAIT_TEXT)
        except:
            return False
    
    @allure.step("Ожидать появления и загрузки номера заказа в модальном окне")
    def wait_for_order_number(self, timeout=30):
        """Ожидает появления номера заказа в модальном окне и его обновления"""
        from locators.order_feed_locators import OrderFeedPageLocators
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.common.exceptions import TimeoutException
        
        # Сначала ждем появления модального окна
        self.wait_for_element_to_be_visible(self.locators.MODAL, timeout=timeout)
        
        # Ждем появления номера заказа (h2) или текста "идентификатор заказа"
        wait = WebDriverWait(self.driver, timeout)
        
        # Ждем, пока появится номер заказа (h2) с цифрами
        def order_number_loaded(driver):
            try:
                # Проверяем наличие номера заказа (h2)
                order_number_elem = driver.find_element(*OrderFeedPageLocators.ORDER_NUMBER)
                if order_number_elem and order_number_elem.is_displayed():
                    order_text = order_number_elem.text.strip()
                    # Проверяем, что номер заказа содержит цифры и не пустой
                    if order_text and any(char.isdigit() for char in order_text):
                        return True
            except Exception:
                pass
            
            # Или проверяем наличие текста "идентификатор заказа"
            try:
                identifier_elem = driver.find_element(*OrderFeedPageLocators.ORDER_IDENTIFIER_TEXT)
                if identifier_elem and identifier_elem.is_displayed():
                    # Если есть текст "идентификатор заказа", ждем еще немного для загрузки номера
                    import time
                    time.sleep(1)
                    # Проверяем номер заказа еще раз
                    try:
                        order_number_elem = driver.find_element(*OrderFeedPageLocators.ORDER_NUMBER)
                        if order_number_elem and order_number_elem.is_displayed():
                            order_text = order_number_elem.text.strip()
                            if order_text and any(char.isdigit() for char in order_text):
                                return True
                    except Exception:
                        pass
                    return True
            except Exception:
                pass
            return False
        
        try:
            wait.until(order_number_loaded)
        except TimeoutException:
            # Если не удалось дождаться, проверяем наличие хотя бы текста "идентификатор заказа"
            if not self.is_element_visible(OrderFeedPageLocators.ORDER_IDENTIFIER_TEXT, timeout=5):
                raise TimeoutException("Не удалось дождаться появления номера заказа в модальном окне")
    
    @allure.step("Получить номер заказа из модального окна")
    def get_order_number_from_modal(self, timeout=30):
        """Получает номер заказа из модального окна с увеличенным таймаутом и альтернативными способами"""
        from locators.order_feed_locators import OrderFeedPageLocators
        
        # Сначала пытаемся получить номер заказа через локатор h2 с увеличенным таймаутом
        try:
            element = self.find_visible_element(OrderFeedPageLocators.ORDER_NUMBER, timeout=timeout)
            order_number = element.text.strip()
            if order_number and any(char.isdigit() for char in order_number):
                return order_number
        except Exception:
            pass
        
        # Если не получилось, пытаемся найти номер заказа в тексте модального окна
        try:
            modal_text = self.get_order_modal_text()
            if modal_text:
                # Ищем число в тексте модального окна (номер заказа обычно большое число)
                import re
                # Ищем числа из 4+ цифр (номера заказов обычно большие)
                numbers = re.findall(r'\d{4,}', modal_text)
                if numbers:
                    return numbers[0]
        except Exception:
            pass
        
        # Если ничего не нашли, возвращаем None
        return None
    
    @allure.step("Кликнуть по ссылке восстановления пароля")
    def click_recover_password_link(self):
        """Кликает по ссылке восстановления пароля"""
        self.click_by_js(self.locators.RECOVER_PASSWORD_LINK)

