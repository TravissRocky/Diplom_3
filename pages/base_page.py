from __future__ import annotations

from typing import Tuple

import allure
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class BasePage:
    def __init__(self, driver: WebDriver, timeout: int = 15):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    @allure.step('Открыть URL: {url}')
    def open(self, url: str) -> None:
        self.driver.get(url)

    @allure.step('Кликнуть на элемент')
    def click(self, locator: Tuple[str, str]) -> None:
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()

    @allure.step('Заполнить поле значением: {value}')
    def fill(self, locator: Tuple[str, str], value: str, clear: bool = True) -> None:
        element = self.wait.until(EC.visibility_of_element_located(locator))
        if clear:
            element.clear()
        element.send_keys(value)

    def get_text(self, locator: Tuple[str, str]) -> str:
        element = self.wait.until(EC.visibility_of_element_located(locator))
        return element.text

    def wait_for_visible(self, locator: Tuple[str, str]) -> None:
        self.wait.until(EC.visibility_of_element_located(locator))

    def wait_for_clickable(self, locator: Tuple[str, str]) -> None:
        self.wait.until(EC.element_to_be_clickable(locator))

    def wait_for_not_visible(self, locator: Tuple[str, str]) -> None:
        self.wait.until(EC.invisibility_of_element_located(locator))

    def is_visible(self, locator: Tuple[str, str]) -> bool:
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def get_attribute(self, locator: Tuple[str, str], attribute: str) -> str:
        element = self.wait.until(EC.presence_of_element_located(locator))
        return element.get_attribute(attribute)

    def wait_for_text(self, locator: Tuple[str, str], text: str) -> None:
        self.wait.until(EC.text_to_be_present_in_element(locator, text))

    def get_element(self, locator: Tuple[str, str]):
        return self.wait.until(EC.presence_of_element_located(locator))

    def get_current_url(self) -> str:
        return self.driver.current_url

    def url_contains(self, text: str) -> bool:
        return text in self.driver.current_url

    def wait_for_url_contains(self, text: str, timeout: int = 10) -> None:
        WebDriverWait(self.driver, timeout).until(EC.url_contains(text))

    def refresh_page(self) -> None:
        self.driver.refresh()

    def go_back(self) -> None:
        self.driver.back()
