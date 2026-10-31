import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from pages.base_page import BasePage


class InventoryPage(BasePage):
    TITLE = (By.CSS_SELECTOR, "[data-test='title']")
    ITEM_CARDS = (By.CSS_SELECTOR, "[data-test='inventory-item']")
    ITEM_NAMES = (By.CSS_SELECTOR, "[data-test='inventory-item-name']")
    ITEM_PRICES = (By.CSS_SELECTOR, "[data-test='inventory-item-price']")
    SORT_DROPDOWN = (By.CSS_SELECTOR, "[data-test='product-sort-container']")
    CART_LINK = (By.CSS_SELECTOR, "[data-test='shopping-cart-link']")
    CART_BADGE = (By.CSS_SELECTOR, "[data-test='shopping-cart-badge']")
    BURGER_MENU = (By.ID, "react-burger-menu-btn")
    LOGOUT_LINK = (By.ID, "logout_sidebar_link")

    @staticmethod
    def _add_button(product_name: str) -> tuple:
        slug = product_name.lower().replace(" ", "-")
        return (By.ID, f"add-to-cart-{slug}")

    @staticmethod
    def _remove_button(product_name: str) -> tuple:
        slug = product_name.lower().replace(" ", "-")
        return (By.ID, f"remove-{slug}")

    # --- state ------------------------------------------------------------
    def is_loaded(self) -> bool:
        return self.is_visible(self.TITLE) and "inventory" in self.current_url

    def get_product_names(self) -> list[str]:
        return [el.text for el in self.find_all(self.ITEM_NAMES)]

    def get_product_prices(self) -> list[float]:
        return [float(el.text.replace("$", "")) for el in self.find_all(self.ITEM_PRICES)]

    def product_count(self) -> int:
        return len(self.find_all(self.ITEM_CARDS))

    def cart_count(self) -> int:
        """Number shown on the cart badge; 0 when the badge isn't displayed."""
        if self.is_visible(self.CART_BADGE):
            return int(self.get_text(self.CART_BADGE))
        return 0

    # --- actions ----------------------------------------------------------
    @allure.step("Add '{product_name}' to cart")
    def add_to_cart(self, product_name: str) -> None:
        self.click(self._add_button(product_name))

    @allure.step("Remove '{product_name}' from cart")
    def remove_from_cart(self, product_name: str) -> None:
        self.click(self._remove_button(product_name))

    @allure.step("Sort products by '{visible_text}'")
    def sort_by(self, visible_text: str) -> None:
        Select(self.find(self.SORT_DROPDOWN)).select_by_visible_text(visible_text)

    @allure.step("Open the cart")
    def open_cart(self) -> None:
        self.click(self.CART_LINK)

    @allure.step("Log out")
    def logout(self) -> None:
        self.click(self.BURGER_MENU)
        self.click(self.LOGOUT_LINK)
