from __future__ import annotations

import allure
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from locators.account_page_locators import AccountPageLocators
from pages.base_page import BasePage


class AccountPage(BasePage):
    @allure.step('Открыть историю заказов')
    def open_order_history(self) -> None:
        self.click(AccountPageLocators.ORDER_HISTORY_LINK)

    @allure.step('Выйти из аккаунта')
    def logout(self) -> None:
        self.click(AccountPageLocators.LOGOUT_BUTTON)
        WebDriverWait(self.driver, 15).until(EC.url_contains("/login"))

    @allure.step('Получить номер первого заказа')
    def get_first_order_number(self) -> str:
        self.wait_for_visible(AccountPageLocators.ORDER_HISTORY_LIST)
        order_numbers = self.driver.find_elements(*AccountPageLocators.ORDER_CARD_NUMBER)
        if not order_numbers:
            raise AssertionError('Order history is empty')
        return order_numbers[0].text

    @allure.step('Дождаться появления заказа {order_number} в истории')
    def wait_for_order_in_history(self, order_number: str, timeout: int = 20) -> None:
        WebDriverWait(self.driver, timeout).until(
            lambda d: any(order_number in el.text for el in d.find_elements(*AccountPageLocators.ORDER_CARD_NUMBER))
        )
