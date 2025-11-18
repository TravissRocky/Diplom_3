from selenium.webdriver.common.by import By


class FeedPageLocators:
    PAGE_TITLE = (By.XPATH, "//h1[contains(text(),'Лента заказов')]")
    ORDER_CARDS = (By.CSS_SELECTOR, "li[class*='OrderHistory_listItem']")
    ORDER_NUMBERS = (By.CSS_SELECTOR, "li[class*='OrderHistory_listItem'] p.text_type_digits-default")
    MODAL = (By.CSS_SELECTOR, "div[class*='Modal_modal__contentBox']")
    MODAL_CLOSE = (By.CSS_SELECTOR, "button[class*='modal__close']")
    TOTAL_COUNT = (By.XPATH, "//p[text()='Выполнено за все время:']/following-sibling::p")
    TODAY_COUNT = (By.XPATH, "//p[text()='Выполнено за сегодня:']/following-sibling::p")
    IN_PROGRESS_LIST = (By.XPATH, "//p[text()='В работе:']/following-sibling::ul")
