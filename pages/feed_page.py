from __future__ import annotations

from typing import Optional

import allure
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException

from locators.feed_page_locators import FeedPageLocators
from pages.base_page import BasePage


class FeedPage(BasePage):
    @allure.step('Открыть страницу ленты заказов')
    def open(self, base_url: str) -> None:  # type: ignore[override]
        super().open(f"{base_url}/feed")
        self.wait_until_loaded()

    @allure.step('Дождаться загрузки страницы ленты заказов')
    def wait_until_loaded(self) -> None:
        self.wait_for_visible(FeedPageLocators.PAGE_TITLE)
        self.wait_for_orders()

    @allure.step('Открыть модальное окно первого заказа')
    def open_first_order_modal(self) -> bool:
        orders = self.driver.find_elements(*FeedPageLocators.ORDER_CARDS)
        if not orders:
            self.wait_for_orders()
            orders = self.driver.find_elements(*FeedPageLocators.ORDER_CARDS)
        order = orders[0]
        try:
            order.click()
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].click();", order)
        try:
            self.wait_for_visible(FeedPageLocators.MODAL)
            return True
        except TimeoutException:
            return False

    @allure.step('Закрыть модальное окно')
    def close_modal(self) -> None:
        self.click(FeedPageLocators.MODAL_CLOSE)

    @allure.step('Получить общее количество заказов')
    def get_total_count(self) -> int:
        text = self.get_text(FeedPageLocators.TOTAL_COUNT)
        return int(text.replace(' ', ''))

    @allure.step('Получить количество заказов за сегодня')
    def get_today_count(self) -> int:
        text = self.get_text(FeedPageLocators.TODAY_COUNT)
        return int(text.replace(' ', ''))

    @allure.step('Проверить наличие заказа {number}')
    def is_order_present(self, number: str) -> bool:
        numbers = self.driver.find_elements(*FeedPageLocators.ORDER_NUMBERS)
        return any(number in element.text for element in numbers)

    @allure.step('Дождаться появления заказа {number}')
    def wait_for_order(self, number: str, timeout: int = 15) -> None:
        for _ in range(timeout):
            if self.is_order_present(number):
                return
            self.refresh_page()
            self.wait_until_loaded()
        raise AssertionError(f'Order {number} not found in feed')

    @allure.step('Проверить, находится ли заказ {number} в работе')
    def is_order_in_progress(self, number: str) -> bool:
        in_progress = self.get_element(FeedPageLocators.IN_PROGRESS_LIST)
        return number in in_progress.text

    @allure.step('Дождаться появления заказов в ленте')
    def wait_for_orders(self) -> None:
        self.wait.until(lambda d: len(d.find_elements(*FeedPageLocators.ORDER_CARDS)) > 0)
