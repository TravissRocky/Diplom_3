from __future__ import annotations

from locators.password_recovery_locators import PasswordRecoveryLocators, PasswordResetLocators
from pages.base_page import BasePage


class PasswordRecoveryPage(BasePage):
    def wait_until_loaded(self) -> None:
        self.wait_for_visible(PasswordRecoveryLocators.TITLE)
        self.wait_for_visible(PasswordRecoveryLocators.EMAIL_INPUT)
        self.wait_for_clickable(PasswordRecoveryLocators.RECOVER_BUTTON)

    def submit_email(self, email: str) -> None:
        self.fill(PasswordRecoveryLocators.EMAIL_INPUT, email)
        self.click(PasswordRecoveryLocators.RECOVER_BUTTON)


class PasswordResetPage(BasePage):
    def toggle_password_visibility(self) -> None:
        self.click(PasswordResetLocators.TOGGLE_BUTTON)

    def get_password_field_class(self) -> str:
        return self.get_attribute(PasswordResetLocators.PASSWORD_INPUT, "class")
