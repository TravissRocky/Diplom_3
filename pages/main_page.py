from __future__ import annotations

from typing import Optional

import allure
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    TimeoutException,
    WebDriverException,
)
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput

from locators.main_page_locators import MainPageLocators
from pages.base_page import BasePage


class MainPage(BasePage):
    OVERLAY_LOCATOR = (By.CSS_SELECTOR, "div[class*='Modal_modal_overlay']")

    @allure.step('Открыть главную страницу')
    def open(self, base_url: str) -> None:  # type: ignore[override]
        super().open(base_url)
        self.wait_for_visible(MainPageLocators.CONSTRUCTOR_LINK)
        self.wait_overlay_gone()

    @allure.step('Нажать кнопку входа в аккаунт')
    def click_login_button(self) -> None:
        self._click_with_overlay_guard(MainPageLocators.LOGIN_ACCOUNT_BUTTON)

    @allure.step('Открыть личный кабинет')
    def open_personal_account(self) -> None:
        self._click_with_overlay_guard(MainPageLocators.PERSONAL_ACCOUNT_LINK)

    @allure.step('Открыть конструктор')
    def open_constructor(self) -> None:
        self._click_with_overlay_guard(MainPageLocators.CONSTRUCTOR_LINK)

    @allure.step('Открыть ленту заказов')
    def open_feed(self) -> None:
        self._click_with_overlay_guard(MainPageLocators.FEED_LINK)

    @allure.step('Открыть модальное окно первого ингредиента')
    def open_first_ingredient_modal(self) -> None:
        ingredient = self.driver.find_elements(*MainPageLocators.INGREDIENT_CARDS)[0]
        ingredient.click()
        self.wait_for_visible(MainPageLocators.INGREDIENT_MODAL)

    @allure.step('Открыть модальное окно ингредиента: {ingredient_name}')
    def open_ingredient_modal_by_name(self, ingredient_name: str) -> None:
        locator = (By.XPATH, f"//p[text()='{ingredient_name}']/ancestor::a")
        element = self.get_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        element.click()
        self.wait_for_visible(MainPageLocators.INGREDIENT_MODAL)

    @allure.step('Закрыть модальное окно ингредиента')
    def close_ingredient_modal(self) -> None:
        try:
            self.click(MainPageLocators.INGREDIENT_MODAL_CLOSE_BUTTON)
        except ElementClickInterceptedException:
            close_button = self.get_element(MainPageLocators.INGREDIENT_MODAL_CLOSE_BUTTON)
            self.driver.execute_script("arguments[0].click();", close_button)

    @allure.step('Добавить ингредиент в конструктор по индексу: {index}')
    def add_ingredient_to_constructor(self, index: int = 0) -> None:
        ingredient = self.driver.find_elements(*MainPageLocators.INGREDIENT_CARDS)[index]
        constructor = self.get_element(MainPageLocators.CONSTRUCTOR_DROP_AREA)
        self._drag_ingredient_to_constructor(ingredient, constructor)

    @allure.step('Добавить ингредиент в конструктор: {ingredient_name}')
    def add_ingredient_by_name(self, ingredient_name: str) -> None:
        import time
        locator = (By.XPATH, f"//p[text()='{ingredient_name}']/ancestor::a")
        ingredient = self.get_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", ingredient)
        time.sleep(0.3)  # Пауза после прокрутки для стабильности в Firefox
        constructor = self.get_element(MainPageLocators.CONSTRUCTOR_DROP_AREA)
        self._drag_ingredient_to_constructor(ingredient, constructor)
        time.sleep(0.5)  # Пауза после drag-and-drop для обновления счетчика

    @allure.step('Получить значение счетчика ингредиента по индексу: {index}')
    def get_ingredient_counter_value(self, index: int = 0) -> int:
        ingredient = self.driver.find_elements(*MainPageLocators.INGREDIENT_CARDS)[index]
        counters = ingredient.find_elements(By.CSS_SELECTOR, "p[class*='counter__num']")
        if not counters:
            return 0
        return int(counters[0].text)

    @allure.step('Получить значение счетчика ингредиента: {ingredient_name}')
    def get_counter_by_name(self, ingredient_name: str) -> int:
        locator = (By.XPATH, f"//p[text()='{ingredient_name}']/ancestor::a")
        ingredient = self.get_element(locator)
        counters = ingredient.find_elements(By.CSS_SELECTOR, "p[class*='counter__num']")
        if not counters:
            return 0
        return int(counters[0].text)

    @allure.step('Дождаться значения счетчика {expected_value} для ингредиента: {ingredient_name}')
    def wait_for_counter_value(self, ingredient_name: str, expected_value: int, timeout: int = 15) -> None:
        WebDriverWait(self.driver, timeout).until(
            lambda _: self.get_counter_by_name(ingredient_name) == expected_value
        )

    @allure.step('Оформить заказ')
    def submit_order(self) -> None:
        self._click_with_overlay_guard(MainPageLocators.ORDER_BUTTON)

    @allure.step('Дождаться номера заказа')
    def wait_for_order_number(self) -> str:
        WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located(MainPageLocators.ORDER_NUMBER_TITLE))
        return self.get_text(MainPageLocators.ORDER_NUMBER_TITLE)

    @allure.step('Дождаться исчезновения overlay')
    def wait_overlay_gone(self, timeout: int = 10) -> None:
        try:
            WebDriverWait(self.driver, timeout).until(EC.invisibility_of_element_located(self.OVERLAY_LOCATOR))
        except TimeoutException:
            overlays = self.driver.find_elements(*self.OVERLAY_LOCATOR)
            if overlays:
                self.driver.execute_script("arguments[0].style.display='none';", overlays[0])

    def _drag_ingredient_to_constructor(self, ingredient, constructor) -> None:
        # Для Firefox сразу используем JS, т.к. стандартный drag-and-drop работает нестабильно
        if 'firefox' in self.driver.capabilities.get('browserName', '').lower():
            self._drag_and_drop_via_js(ingredient, constructor)
            return

        actions = ActionChains(self.driver)
        try:
            actions.drag_and_drop(ingredient, constructor).perform()
            return
        except WebDriverException:
            try:
                actions.click_and_hold(ingredient).move_to_element(constructor).pause(0.5).release().perform()
                return
            except WebDriverException:
                try:
                    builder = ActionBuilder(self.driver)
                    pointer = builder.pointer_action
                    pointer.move_to(ingredient)
                    pointer.click_and_hold()
                    pointer.pause(0.2)
                    pointer.move_to(constructor)
                    pointer.pause(0.2)
                    pointer.release()
                    builder.perform()
                    return
                except WebDriverException:
                    try:
                        offset_x = constructor.rect["x"] - ingredient.rect["x"]
                        offset_y = constructor.rect["y"] - ingredient.rect["y"]
                        actions.reset_actions()
                        actions.click_and_hold(ingredient).move_by_offset(offset_x, offset_y).pause(0.2).release().perform()
                        return
                    except WebDriverException:
                        self._drag_and_drop_via_js(ingredient, constructor)
                return
            except WebDriverException:
                self._drag_and_drop_via_js(ingredient, constructor)

    def _drag_and_drop_via_js(self, source, target) -> None:
        self.driver.execute_script(
            """
const source = arguments[0];
const target = arguments[1];
const dataTransfer = new DataTransfer();
dataTransfer.dropEffect = 'move';
dataTransfer.effectAllowed = 'all';
dataTransfer.setData('text/plain', source.innerText);
dataTransfer.setData('application/json', JSON.stringify({name: source.innerText}));
const eventInit = {bubbles: true, cancelable: true, dataTransfer};
source.dispatchEvent(new DragEvent('dragstart', eventInit));
target.dispatchEvent(new DragEvent('dragenter', eventInit));
target.dispatchEvent(new DragEvent('dragover', eventInit));
target.dispatchEvent(new DragEvent('drop', eventInit));
source.dispatchEvent(new DragEvent('dragend', eventInit));
            """,
            source,
            target,
        )

    def _click_with_overlay_guard(self, locator) -> None:
        self.wait_overlay_gone()
        try:
            self.click(locator)
        except ElementClickInterceptedException:
            self.wait_overlay_gone(timeout=20)
            element = self.wait.until(EC.element_to_be_clickable(locator))
            self.driver.execute_script("arguments[0].click();", element)
