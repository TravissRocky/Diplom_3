from typing import Dict, List

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from data.urls import BASE_URL
from helpers.api_client import StellarApiClient
from helpers.user_factory import generate_user_credentials
from pages.login_page import LoginPage
from pages.main_page import MainPage
from locators.main_page_locators import MainPageLocators


SUPPORTED_BROWSERS = ["chrome", "firefox"]


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="all",
        choices=[*SUPPORTED_BROWSERS, "all"],
        help="Браузер для запуска UI-тестов",
    )


def pytest_generate_tests(metafunc):
    if "browser_name" in metafunc.fixturenames:
        option = metafunc.config.getoption("--browser")
        browsers = SUPPORTED_BROWSERS if option == "all" else [option]
        metafunc.parametrize("browser_name", browsers, scope="session")


@pytest.fixture(scope="session")
def api_client() -> StellarApiClient:
    return StellarApiClient()


@pytest.fixture(scope="session")
def ingredient_catalog(api_client: StellarApiClient) -> List[Dict]:
    return api_client.get_ingredients()


@pytest.fixture(scope="session")
def default_ingredient_set(ingredient_catalog: List[Dict]) -> Dict[str, Dict]:
    bun = next(item for item in ingredient_catalog if item["type"] == "bun")
    sauce = next(item for item in ingredient_catalog if item["type"] == "sauce")
    filling = next(item for item in ingredient_catalog if item["type"] == "main")
    return {"bun": bun, "sauce": sauce, "filling": filling}


@pytest.fixture(scope="function")
def api_user(api_client: StellarApiClient) -> Dict:
    creds = generate_user_credentials()
    api_client.create_user(**creds)
    tokens = api_client.login_user(creds["email"], creds["password"])
    creds.update(tokens)
    yield creds
    access_token = tokens.get("accessToken")
    if access_token:
        try:
            api_client.delete_user(access_token)
        except Exception:
            pass


@pytest.fixture
def driver(browser_name: str):
    if browser_name == "chrome":
        options = ChromeOptions()
        options.add_argument("--window-size=1440,900")
        driver = webdriver.Chrome(options=options)
    elif browser_name == "firefox":
        options = FirefoxOptions()
        options.add_argument("--width=1440")
        options.add_argument("--height=900")
        driver = webdriver.Firefox(options=options)
    else:
        raise pytest.UsageError(f"Неизвестный браузер: {browser_name}")
    driver.delete_all_cookies()
    yield driver
    driver.quit()


@pytest.fixture
def base_url() -> str:
    return BASE_URL


@pytest.fixture
def authorized_user(driver, base_url, api_user):
    main_page = MainPage(driver)
    main_page.open(base_url)
    main_page.click_login_button()
    login_page = LoginPage(driver)
    login_page.wait_until_loaded()
    login_page.login(api_user["email"], api_user["password"])
    main_page.wait_for_text(MainPageLocators.ORDER_BUTTON, "Оформить заказ")
    return api_user
