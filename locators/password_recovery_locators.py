from selenium.webdriver.common.by import By


class PasswordRecoveryLocators:
    TITLE = (By.XPATH, "//h2[contains(text(),'Восстановление пароля')]")
    EMAIL_INPUT = (By.CSS_SELECTOR, "form fieldset:nth-of-type(1) input")
    RECOVER_BUTTON = (By.XPATH, "//button[text()='Восстановить']")


class PasswordResetLocators:
    PASSWORD_INPUT = (By.CSS_SELECTOR, "form fieldset:nth-of-type(1) input")
    TOGGLE_BUTTON = (By.CSS_SELECTOR, "form fieldset:nth-of-type(1) button")
    CODE_INPUT = (By.CSS_SELECTOR, "form fieldset:nth-of-type(2) input")
    SAVE_BUTTON = (By.XPATH, "//button[text()='Сохранить']")
