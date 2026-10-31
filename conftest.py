import os
from datetime import datetime

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

import config
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome",
                     choices=["chrome", "firefox"], help="Browser to run tests in")
    parser.addoption("--headed", action="store_true", default=False,
                     help="Show the browser window (default is headless)")


@pytest.fixture
def driver(request):
    """Create a fresh browser per test and always quit it afterwards."""
    browser = request.config.getoption("--browser")
    headed = request.config.getoption("--headed")

    if browser == "firefox":
        options = FirefoxOptions()
        if not headed:
            options.add_argument("-headless")
        drv = webdriver.Firefox(options=options)
    else:
        options = ChromeOptions()
        if not headed:
            options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        # Selenium Manager (built into Selenium 4) downloads the right driver.
        drv = webdriver.Chrome(options=options)

    drv.implicitly_wait(0)  # we use explicit waits only (see pages/base_page.py)
    yield drv
    drv.quit()


@pytest.fixture
def login_page(driver):
    page = LoginPage(driver)
    page.open()
    return page


@pytest.fixture
def inventory_page(driver, login_page):
    """A logged-in user sitting on the inventory page."""
    login_page.login(config.VALID_USER, config.PASSWORD)
    page = InventoryPage(driver)
    assert page.is_loaded(), "Login did not land on the inventory page"
    return page


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Save a screenshot whenever a test fails."""
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        drv = item.funcargs.get("driver")
        if drv:
            os.makedirs("screenshots", exist_ok=True)
            stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            path = f"screenshots/{item.name}-{stamp}.png"
            drv.save_screenshot(path)
