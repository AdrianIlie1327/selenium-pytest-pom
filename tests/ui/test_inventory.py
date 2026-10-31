import pytest


@pytest.mark.smoke
def test_inventory_shows_six_products(inventory_page):
    assert inventory_page.product_count() == 6


@pytest.mark.regression
def test_sort_by_price_low_to_high(inventory_page):
    inventory_page.sort_by("Price (low to high)")
    prices = inventory_page.get_product_prices()
    assert prices == sorted(prices)


@pytest.mark.regression
def test_sort_by_name_z_to_a(inventory_page):
    inventory_page.sort_by("Name (Z to A)")
    names = inventory_page.get_product_names()
    assert names == sorted(names, reverse=True)
