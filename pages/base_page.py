"""BasePage: thin wrapper around Selenium that every page object inherits.

Why it exists: waits, clicks and typing live in ONE place, so page objects
stay short and tests never touch raw Selenium calls.
"""
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import config


class BasePage:
    def __init__(self, driver: WebDriver, timeout: int = config.DEFAULT_TIMEOUT):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    # --- navigation -------------------------------------------------------
    def open_url(self, path: str = "") -> None:
        self.driver.get(f"{config.BASE_URL}{path}")

    @property
    def current_url(self) -> str:
        return self.driver.current_url

    # --- finding elements (explicit waits) --------------------------------
    def find(self, locator: tuple) -> WebElement:
        return self.wait.until(EC.visibility_of_element_located(locator))

    def find_all(self, locator: tuple) -> list[WebElement]:
        self.wait.until(EC.presence_of_element_located(locator))
        return self.driver.find_elements(*locator)

    def is_visible(self, locator: tuple) -> bool:
        try:
            self.find(locator)
            return True
        except Exception:
            return False

    # --- actions ----------------------------------------------------------
    def click(self, locator: tuple) -> None:
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def type_text(self, locator: tuple, text: str) -> None:
        element = self.find(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator: tuple) -> str:
        return self.find(locator).text
