from selenium.webdriver.common.by import By


class MainPageLocators:
    LOGIN_ACCOUNT_BUTTON = (By.XPATH, "//button[text()='Войти в аккаунт']")
    PERSONAL_ACCOUNT_LINK = (By.XPATH, "//p[text()='Личный Кабинет']/..")
    CONSTRUCTOR_LINK = (By.XPATH, "//p[text()='Конструктор']/..")
    FEED_LINK = (By.XPATH, "//a[@href='/feed']")
    INGREDIENT_CARDS = (By.CSS_SELECTOR, "a[class*='BurgerIngredient_ingredient']")
    INGREDIENT_COUNTER = (By.CSS_SELECTOR, "div[class*='counter__num']")
    INGREDIENT_MODAL = (By.CSS_SELECTOR, "div[class*='Modal_modal__contentBox']")
    INGREDIENT_MODAL_CLOSE_BUTTON = (By.CSS_SELECTOR, "button[class*='modal__close']")
    CONSTRUCTOR_DROP_AREA = (By.CSS_SELECTOR, "section[class*='BurgerConstructor_basket']")
    ORDER_BUTTON = (By.XPATH, "//button[.='Оформить заказ' or .='Войти в аккаунт']")
    ORDER_NUMBER_TITLE = (By.CSS_SELECTOR, "h2[class*='text_type_digits-large']")
