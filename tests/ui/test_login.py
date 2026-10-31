import pytest

import config
from pages.inventory_page import InventoryPage


@pytest.mark.smoke
def test_valid_login_lands_on_inventory(driver, login_page):
    login_page.login(config.VALID_USER, config.PASSWORD)
    assert InventoryPage(driver).is_loaded()


@pytest.mark.negative
def test_locked_out_user_sees_error(login_page):
    login_page.login(config.LOCKED_USER, config.PASSWORD)
    assert "locked out" in login_page.get_error_message().lower()


# Parametrization: one test body, many data rows. Great for negative cases.
@pytest.mark.negative
@pytest.mark.parametrize(
    "username, password, expected_error",
    [
        ("", "", "Username is required"),
        (config.VALID_USER, "", "Password is required"),
        ("", config.PASSWORD, "Username is required"),
        (config.VALID_USER, "wrong_password", "do not match"),
        ("no_such_user", config.PASSWORD, "do not match"),
    ],
    ids=["empty-both", "empty-password", "empty-username", "bad-password", "unknown-user"],
)
def test_invalid_login_shows_error(login_page, username, password, expected_error):
    login_page.login(username, password)
    assert expected_error in login_page.get_error_message()


@pytest.mark.regression
def test_logout_returns_to_login(driver, inventory_page):
    inventory_page.logout()
    assert driver.current_url.rstrip("/") == config.BASE_URL
