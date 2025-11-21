from __future__ import annotations

import allure
from locators.login_page_locators import LoginPageLocators
from pages.base_page import BasePage


class LoginPage(BasePage):
    @allure.step('Дождаться загрузки страницы логина')
    def wait_until_loaded(self) -> None:
        self.wait_for_visible(LoginPageLocators.FORM_TITLE)

    @allure.step('Войти с email: {email}')
    def login(self, email: str, password: str) -> None:
        self.fill(LoginPageLocators.EMAIL_INPUT, email)
        self.fill(LoginPageLocators.PASSWORD_INPUT, password)
        self.click(LoginPageLocators.SUBMIT_BUTTON)

    @allure.step('Перейти к восстановлению пароля')
    def go_to_password_recovery(self) -> None:
        self.click(LoginPageLocators.FORGOT_PASSWORD_LINK)

    @allure.step('Переключить видимость пароля')
    def toggle_password_visibility(self) -> None:
        self.wait_for_clickable(LoginPageLocators.PASSWORD_TOGGLE)
        self.click(LoginPageLocators.PASSWORD_TOGGLE)

    @allure.step('Получить класс поля пароля')
    def get_password_field_class(self) -> str:
        return self.get_attribute(LoginPageLocators.PASSWORD_INPUT_CONTAINER, "class")
