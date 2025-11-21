from __future__ import annotations

import allure
from locators.password_recovery_locators import PasswordRecoveryLocators, PasswordResetLocators
from pages.base_page import BasePage


class PasswordRecoveryPage(BasePage):
    @allure.step('Дождаться загрузки страницы восстановления пароля')
    def wait_until_loaded(self) -> None:
        self.wait_for_visible(PasswordRecoveryLocators.TITLE)
        self.wait_for_visible(PasswordRecoveryLocators.EMAIL_INPUT)
        self.wait_for_clickable(PasswordRecoveryLocators.RECOVER_BUTTON)

    @allure.step('Отправить email для восстановления: {email}')
    def submit_email(self, email: str) -> None:
        self.fill(PasswordRecoveryLocators.EMAIL_INPUT, email)
        self.click(PasswordRecoveryLocators.RECOVER_BUTTON)


class PasswordResetPage(BasePage):
    @allure.step('Переключить видимость пароля')
    def toggle_password_visibility(self) -> None:
        self.click(PasswordResetLocators.TOGGLE_BUTTON)

    @allure.step('Получить класс поля пароля')
    def get_password_field_class(self) -> str:
        return self.get_attribute(PasswordResetLocators.PASSWORD_INPUT, "class")
