from selenium.webdriver.common.by import By


class AccountPageLocators:
    PROFILE_LINK = (By.XPATH, "//a[contains(@href,'/account/profile')]")
    ORDER_HISTORY_LINK = (By.XPATH, "//a[contains(@href,'/account/order-history')]")
    LOGOUT_BUTTON = (By.XPATH, "//button[text()='Выход']")
    ORDER_HISTORY_LIST = (By.CSS_SELECTOR, "ul[class*='OrderHistory_list']")
    ORDER_CARD_NUMBER = (By.CSS_SELECTOR, "li[class*='OrderHistory_listItem'] p.text_type_digits-default")
