from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CheckoutPage(BasePage):
    FIRST_NAME = (By.ID, "first-name")
    LAST_NAME = (By.ID, "last-name")
    POSTAL_CODE = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    FINISH_BUTTON = (By.ID, "finish")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")
    COMPLETE_HEADER = (By.CSS_SELECTOR, "[data-test='complete-header']")

    def fill_details(self, first: str, last: str, postal: str) -> None:
        self.type_text(self.FIRST_NAME, first)
        self.type_text(self.LAST_NAME, last)
        self.type_text(self.POSTAL_CODE, postal)

    def continue_to_overview(self) -> None:
        self.click(self.CONTINUE_BUTTON)

    def finish(self) -> None:
        self.click(self.FINISH_BUTTON)

    def get_error_message(self) -> str:
        return self.get_text(self.ERROR_MESSAGE)

    def get_confirmation(self) -> str:
        return self.get_text(self.COMPLETE_HEADER)
