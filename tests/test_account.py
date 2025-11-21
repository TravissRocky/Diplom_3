import allure
import pytest

from pages.account_page import AccountPage
from pages.main_page import MainPage


@allure.feature('Личный кабинет')
@pytest.mark.personal_account
class TestPersonalAccount:
    def test_open_personal_account(self, driver, authorized_user):
        main_page = MainPage(driver)
        main_page.open_personal_account()
        assert main_page.url_contains('/account')

    def test_open_order_history(self, driver, authorized_user):
        main_page = MainPage(driver)
        main_page.open_personal_account()

        account_page = AccountPage(driver)
        account_page.open_order_history()
        assert account_page.url_contains('order-history')

    def test_logout_from_account(self, driver, authorized_user):
        main_page = MainPage(driver)
        main_page.open_personal_account()

        account_page = AccountPage(driver)
        account_page.logout()
        assert account_page.url_contains('/login')
