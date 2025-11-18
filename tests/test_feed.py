import time

import allure
import pytest
from selenium.webdriver.support.ui import WebDriverWait

from helpers.api_client import StellarApiClient
from locators.account_page_locators import AccountPageLocators
from pages.account_page import AccountPage
from pages.feed_page import FeedPage
from pages.main_page import MainPage


def _create_order(api_client: StellarApiClient, ingredient_set, access_token: str) -> str:
    ingredient_ids = [
        ingredient_set['bun']['_id'],
        ingredient_set['filling']['_id'],
        ingredient_set['sauce']['_id'],
    ]
    response = api_client.create_order(ingredient_ids, access_token)
    return str(response['order']['number'])


@allure.feature('Лента заказов')
@pytest.mark.feed
class TestFeed:
    def test_order_card_has_details_modal(self, driver, base_url):
        main_page = MainPage(driver)
        main_page.open(base_url)
        main_page.open_feed()
        feed_page = FeedPage(driver)
        feed_page.wait_until_loaded()
        if feed_page.open_first_order_modal():
            feed_page.close_modal()
        else:
            assert "/feed/" in driver.current_url
            driver.back()

    def test_user_history_order_visible_in_feed(
        self,
        driver,
        base_url,
        authorized_user,
        api_client,
        default_ingredient_set,
    ):
        order_number = _create_order(api_client, default_ingredient_set, authorized_user['accessToken'])

        main_page = MainPage(driver)
        main_page.open_personal_account()
        account_page = AccountPage(driver)
        account_page.open_order_history()

        WebDriverWait(driver, 20).until(
            lambda d: any(order_number in el.text for el in d.find_elements(*AccountPageLocators.ORDER_CARD_NUMBER))
        )

        main_page.open_feed()
        feed_page = FeedPage(driver)
        feed_page.wait_until_loaded()
        feed_page.wait_for_order(order_number)

    def test_total_counters_increase_after_new_order(
        self,
        driver,
        base_url,
        api_client,
        test_user,
        default_ingredient_set,
    ):
        driver.get(f"{base_url}/feed")
        feed_page = FeedPage(driver)
        feed_page.wait_until_loaded()
        total_before = feed_page.get_total_count()
        today_before = feed_page.get_today_count()

        order_number = _create_order(api_client, default_ingredient_set, test_user['accessToken'])

        for _ in range(30):
            driver.refresh()
            feed_page.wait_until_loaded()
            total_after = feed_page.get_total_count()
            today_after = feed_page.get_today_count()
            if total_after > total_before and today_after > today_before:
                break
            time.sleep(1)
        else:
            raise AssertionError('Счетчики не обновились после нового заказа')

        assert feed_page.is_order_present(order_number)

    def test_new_order_appears_in_progress_list(
        self,
        driver,
        base_url,
        api_client,
        test_user,
        default_ingredient_set,
    ):
        driver.get(f"{base_url}/feed")
        feed_page = FeedPage(driver)
        feed_page.wait_until_loaded()
        order_number = _create_order(api_client, default_ingredient_set, test_user['accessToken'])
        for _ in range(30):
            driver.refresh()
            feed_page.wait_until_loaded()
            if feed_page.is_order_in_progress(order_number):
                return
            time.sleep(1)
        raise AssertionError('Номер заказа не появился в блоке "В работе"')
