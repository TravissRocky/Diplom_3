import allure
import pytest

from data.urls import BASE_URL
from locators.main_page_locators import MainPageLocators
from pages.main_page import MainPage


@allure.feature('Основной функционал')
@pytest.mark.main_functionality
class TestMainFunctionality:
    def test_navigate_constructor_from_feed(self, driver):
        driver.get(f"{BASE_URL}/feed")
        main_page = MainPage(driver)
        main_page.open_constructor()
        assert driver.current_url.rstrip('/') == BASE_URL.rstrip('/')

    def test_navigate_to_feed(self, driver):
        main_page = MainPage(driver)
        main_page.open(BASE_URL)
        main_page.open_feed()
        assert '/feed' in driver.current_url

    def test_ingredient_modal_open_and_close(self, driver):
        main_page = MainPage(driver)
        main_page.open(BASE_URL)
        main_page.open_first_ingredient_modal()
        assert main_page.is_visible(MainPageLocators.INGREDIENT_MODAL)
        main_page.close_ingredient_modal()
        main_page.wait_for_not_visible(MainPageLocators.INGREDIENT_MODAL)

    def test_counter_increases_after_adding_ingredient(self, driver, default_ingredient_set):
        sauce_name = default_ingredient_set['sauce']['name']
        main_page = MainPage(driver)
        main_page.open(BASE_URL)
        before = main_page.get_counter_by_name(sauce_name)
        main_page.add_ingredient_by_name(sauce_name)
        main_page.wait_for_counter_value(sauce_name, before + 1)

    def test_authenticated_user_can_place_order(self, driver, authorized_user, default_ingredient_set):
        main_page = MainPage(driver)
        main_page.open(BASE_URL)
        main_page.add_ingredient_by_name(default_ingredient_set['bun']['name'])
        main_page.add_ingredient_by_name(default_ingredient_set['sauce']['name'])
        main_page.add_ingredient_by_name(default_ingredient_set['filling']['name'])
        main_page.submit_order()
        order_number = main_page.wait_for_order_number()
        assert order_number.strip().isdigit()
        main_page.close_ingredient_modal()
