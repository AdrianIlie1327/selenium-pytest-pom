import pytest

from pages.cart_page import CartPage

BACKPACK = "Sauce Labs Backpack"
BIKE_LIGHT = "Sauce Labs Bike Light"


@pytest.mark.smoke
def test_add_item_updates_cart_badge(inventory_page):
    inventory_page.add_to_cart(BACKPACK)
    assert inventory_page.cart_count() == 1


@pytest.mark.regression
def test_added_items_appear_in_cart(driver, inventory_page):
    inventory_page.add_to_cart(BACKPACK)
    inventory_page.add_to_cart(BIKE_LIGHT)
    inventory_page.open_cart()
    assert sorted(CartPage(driver).get_item_names()) == sorted([BACKPACK, BIKE_LIGHT])


@pytest.mark.regression
def test_remove_item_clears_badge(inventory_page):
    inventory_page.add_to_cart(BACKPACK)
    inventory_page.remove_from_cart(BACKPACK)
    assert inventory_page.cart_count() == 0
