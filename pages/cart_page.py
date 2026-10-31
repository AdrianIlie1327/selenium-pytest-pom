from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CartPage(BasePage):
    ITEM_NAMES = (By.CSS_SELECTOR, "[data-test='inventory-item-name']")
    CHECKOUT_BUTTON = (By.ID, "checkout")
    CONTINUE_SHOPPING = (By.ID, "continue-shopping")

    def get_item_names(self) -> list[str]:
        if not self.is_visible(self.CHECKOUT_BUTTON):
            return []
        return [el.text for el in self.driver.find_elements(*self.ITEM_NAMES)]

    def checkout(self) -> None:
        self.click(self.CHECKOUT_BUTTON)

    def continue_shopping(self) -> None:
        self.click(self.CONTINUE_SHOPPING)
