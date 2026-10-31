import os
from datetime import datetime

import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

import config as cfg
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome",
                     choices=["chrome", "firefox"], help="Browser to run tests in")
    parser.addoption("--headed", action="store_true", default=False,
                     help="Show the browser window (default is headless)")


def pytest_report_header(config):
    return f"environment: {cfg.ENV_NAME} (UI: {cfg.BASE_URL}, API: {cfg.API_BASE_URL})"


def pytest_sessionfinish(session):
    """Show environment details on the Allure report's Overview page."""
    alluredir = session.config.getoption("allure_report_dir", default=None)
    if alluredir:
        os.makedirs(alluredir, exist_ok=True)
        with open(os.path.join(alluredir, "environment.properties"), "w") as f:
            f.write(f"Environment={cfg.ENV_NAME}\n"
                    f"Browser={session.config.getoption('--browser')}\n"
                    f"UI_URL={cfg.BASE_URL}\n"
                    f"API_URL={cfg.API_BASE_URL}\n")


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
        # SauceDemo's password is in public breach lists, so Chrome pops up a
        # "change your password" bubble that swallows clicks. Turn it off.
        options.add_argument("--disable-features=PasswordLeakDetection")
        options.add_experimental_option("prefs", {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.password_manager_leak_detection": False,
        })
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
    login_page.login(cfg.VALID_USER, cfg.PASSWORD)
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
            allure.attach(drv.get_screenshot_as_png(), name="screenshot",
                          attachment_type=allure.attachment_type.PNG)
            allure.attach(drv.current_url, name="url",
                          attachment_type=allure.attachment_type.TEXT)
