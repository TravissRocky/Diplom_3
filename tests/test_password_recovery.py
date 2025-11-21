import allure
import pytest

from data.urls import BASE_URL
from pages.login_page import LoginPage
from pages.main_page import MainPage
from pages.password_recovery_page import PasswordRecoveryPage, PasswordResetPage


@allure.feature('Восстановление пароля')
@pytest.mark.password_recovery
class TestPasswordRecovery:
    def test_open_recovery_page(self, driver):
        main_page = MainPage(driver)
        main_page.open(BASE_URL)
        main_page.click_login_button()

        login_page = LoginPage(driver)
        login_page.wait_until_loaded()
        login_page.go_to_password_recovery()

        recovery_page = PasswordRecoveryPage(driver)
        recovery_page.wait_until_loaded()
        assert recovery_page.url_contains('forgot-password')

    def test_submit_recovery_email_redirects_to_reset(self, driver, api_user):
        main_page = MainPage(driver)
        main_page.open(BASE_URL)
        main_page.click_login_button()

        login_page = LoginPage(driver)
        login_page.wait_until_loaded()
        login_page.go_to_password_recovery()

        recovery_page = PasswordRecoveryPage(driver)
        recovery_page.wait_until_loaded()
        recovery_page.submit_email(api_user['email'])
        recovery_page.wait_for_url_contains('reset-password')

    def test_password_field_highlighted_after_toggle(self, driver):
        main_page = MainPage(driver)
        main_page.open(BASE_URL)
        main_page.click_login_button()

        login_page = LoginPage(driver)
        login_page.wait_until_loaded()
        login_page.toggle_password_visibility()

        field_class = login_page.get_password_field_class()
        assert 'input_status_active' in field_class
