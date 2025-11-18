import allure
import pytest
from selenium.webdriver.support.ui import WebDriverWait

from pages.login_page import LoginPage
from pages.main_page import MainPage
from pages.password_recovery_page import PasswordRecoveryPage, PasswordResetPage


@allure.feature('Восстановление пароля')
@pytest.mark.password_recovery
class TestPasswordRecovery:
    def test_open_recovery_page(self, driver, base_url):
        main_page = MainPage(driver)
        main_page.open(base_url)
        main_page.click_login_button()

        login_page = LoginPage(driver)
        login_page.wait_until_loaded()
        login_page.go_to_password_recovery()

        recovery_page = PasswordRecoveryPage(driver)
        recovery_page.wait_until_loaded()
        assert 'forgot-password' in driver.current_url

    def test_submit_recovery_email_redirects_to_reset(self, driver, base_url, test_user):
        main_page = MainPage(driver)
        main_page.open(base_url)
        main_page.click_login_button()

        login_page = LoginPage(driver)
        login_page.wait_until_loaded()
        login_page.go_to_password_recovery()

        recovery_page = PasswordRecoveryPage(driver)
        recovery_page.wait_until_loaded()
        recovery_page.submit_email(test_user['email'])

        WebDriverWait(driver, 10).until(lambda d: 'reset-password' in d.current_url)

    def test_password_field_highlighted_after_toggle(self, driver, base_url):
        main_page = MainPage(driver)
        main_page.open(base_url)
        main_page.click_login_button()

        login_page = LoginPage(driver)
        login_page.wait_until_loaded()
        login_page.toggle_password_visibility()

        field_class = login_page.get_password_field_class()
        assert 'input_status_active' in field_class
