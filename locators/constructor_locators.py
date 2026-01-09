from selenium.webdriver.common.by import By

class ConstructorPageLocators:
    """Локаторы для страницы конструктора"""
    CONSTRUCTOR_TITLE = (By.XPATH, "//h1[contains(text(), 'Соберите бургер')]")
    INGREDIENT_LIST = (By.CLASS_NAME, "BurgerIngredients_ingredients__")






