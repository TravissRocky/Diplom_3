from selenium.webdriver.common.by import By


class LoginPageLocators:
    FORM_TITLE = (By.XPATH, "//h2[text()='Вход']")
    EMAIL_INPUT = (By.CSS_SELECTOR, "form fieldset:nth-of-type(1) input")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "form fieldset:nth-of-type(2) input")
    PASSWORD_INPUT_CONTAINER = (By.CSS_SELECTOR, "form fieldset:nth-of-type(2) .input")
    PASSWORD_TOGGLE = (By.CSS_SELECTOR, "form fieldset:nth-of-type(2) .input__icon-action")
    SUBMIT_BUTTON = (By.XPATH, "//form//button[text()='Войти']")
    FORGOT_PASSWORD_LINK = (By.LINK_TEXT, "Восстановить пароль")
    REGISTER_LINK = (By.LINK_TEXT, "Зарегистрироваться")
