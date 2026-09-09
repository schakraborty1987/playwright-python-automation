# spec: specs/saucedemo-core-operations.plan.md

from pages.SauceDemoPage import SauceDemoPage

PRODUCTS = [
    "Sauce Labs Backpack",
    "Sauce Labs Bike Light",
    "Sauce Labs Bolt T-Shirt",
    "Sauce Labs Fleece Jacket",
    "Sauce Labs Onesie",
    "Test.allTheThings() T-Shirt (Red)",
]


def test_authenticate_and_browse_product_catalog(page):
    demo = SauceDemoPage(page)

    # 1. Starting from a fresh browser state, navigate to https://www.saucedemo.com/.
    demo.open()
    assert page.get_by_placeholder("Username").is_visible()
    assert page.get_by_placeholder("Password").is_visible()
    assert page.get_by_role("button", name="Login").is_visible()
    assert "standard_user" in page.locator(".login_credentials").inner_text()
    assert "secret_sauce" in page.locator(".login_password").inner_text()

    # 2. Enter standard_user in Username and secret_sauce in Password, then select Login.
    demo.login()
    assert page.url.endswith("/inventory.html")
    assert page.get_by_text("Products", exact=True).is_visible()
    assert page.locator('[data-test="product-sort-container"]').is_visible()

    # 3. Verify that the catalog shows the six expected products with names, descriptions, prices, and Add to cart controls.
    assert page.locator(".inventory_item").count() == 6
    for product_name in PRODUCTS:
        card = demo.product_card(product_name)
        assert card.is_visible()
        assert card.locator(".inventory_item_desc").is_visible()
        assert card.locator(".inventory_item_price").is_visible()
        assert card.get_by_role("button", name="Add to cart").is_visible()

    # 4. Open the Sauce Labs Backpack product link.
    demo.open_product("Sauce Labs Backpack")
    assert page.locator(".inventory_details_name").inner_text() == "Sauce Labs Backpack"
    assert page.locator(".inventory_details_desc").is_visible()
    assert page.locator(".inventory_details_price").inner_text() == "$29.99"
    assert page.get_by_role("button", name="Add to cart").is_visible()
    assert page.get_by_role("button", name="Back to products").is_visible()
    page.get_by_role("button", name="Back to products").click()

    # 5. Use the sort combobox to select Price (low to high), then select Name (Z to A).
    sort = page.locator('[data-test="product-sort-container"]')
    sort.select_option("lohi")
    assert page.locator(".inventory_item_name").first.inner_text() == "Sauce Labs Onesie"
    sort.select_option("za")
    assert page.locator(".inventory_item_name").first.inner_text() == "Test.allTheThings() T-Shirt (Red)"

    # 6. Log out through the Open Menu navigation.
    demo.logout()
    assert page.url == "https://www.saucedemo.com/"
    assert not page.get_by_text("Products", exact=True).is_visible()

    # 7. Negative check: from the fresh login page, submit Login with an empty Username and Password.
    page.get_by_role("button", name="Login").click()
    assert page.url == "https://www.saucedemo.com/"
    assert page.get_by_text("Username is required").is_visible()
