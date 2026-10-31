import pytest

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage

BACKPACK = "Sauce Labs Backpack"


def _go_to_checkout_form(driver, inventory_page) -> CheckoutPage:
    inventory_page.add_to_cart(BACKPACK)
    inventory_page.open_cart()
    CartPage(driver).checkout()
    return CheckoutPage(driver)


@pytest.mark.smoke
def test_complete_purchase_end_to_end(driver, inventory_page):
    checkout = _go_to_checkout_form(driver, inventory_page)
    checkout.fill_details("Adrian", "Tester", "700000")
    checkout.continue_to_overview()
    checkout.finish()
    assert "thank you" in checkout.get_confirmation().lower()


@pytest.mark.negative
@pytest.mark.parametrize(
    "first, last, postal, expected_error",
    [
        ("", "Tester", "700000", "First Name is required"),
        ("Adrian", "", "700000", "Last Name is required"),
        ("Adrian", "Tester", "", "Postal Code is required"),
    ],
    ids=["no-first-name", "no-last-name", "no-postal-code"],
)
def test_checkout_form_validation(driver, inventory_page, first, last, postal, expected_error):
    checkout = _go_to_checkout_form(driver, inventory_page)
    checkout.fill_details(first, last, postal)
    checkout.continue_to_overview()
    assert expected_error in checkout.get_error_message()
