# spec: specs/saucedemo-core-operations.plan.md

from pages.SauceDemoPage import SauceDemoPage

BACKPACK = "Sauce Labs Backpack"
BIKE_LIGHT = "Sauce Labs Bike Light"


def test_manage_shopping_cart(page):
    demo = SauceDemoPage(page)

    # 1. Starting from a fresh browser state, navigate to https://www.saucedemo.com/, sign in, and remain on the product catalog.
    demo.open()
    demo.login()
    assert page.url.endswith("/inventory.html")
    assert not page.locator('[data-test="shopping-cart-badge"]').is_visible()

    # 2. Select Add to cart for Sauce Labs Backpack from the catalog.
    demo.add_product(BACKPACK)
    assert demo.product_card(BACKPACK).get_by_role("button", name="Remove").is_visible()
    assert demo.cart_count() == "1"

    # 3. Open the shopping cart.
    demo.open_cart()
    assert page.get_by_text("Your Cart", exact=True).is_visible()
    backpack = demo.cart_item(BACKPACK)
    assert backpack.is_visible()
    assert backpack.locator(".cart_quantity").inner_text() == "1"
    assert backpack.locator(".inventory_item_price").inner_text() == "$29.99"
    assert page.get_by_role("button", name="Continue Shopping").is_visible()
    assert page.get_by_role("button", name="Checkout").is_visible()

    # 4. Select Continue Shopping, add Sauce Labs Bike Light, and reopen the cart.
    demo.continue_shopping()
    demo.add_product(BIKE_LIGHT)
    demo.open_cart()
    assert demo.cart_count() == "2"
    assert demo.cart_item(BACKPACK).is_visible()
    assert demo.cart_item(BIKE_LIGHT).is_visible()
    assert demo.cart_item(BACKPACK).locator(".cart_quantity").inner_text() == "1"
    assert demo.cart_item(BIKE_LIGHT).locator(".cart_quantity").inner_text() == "1"

    # 5. Remove the Backpack from the cart.
    demo.cart_item(BACKPACK).get_by_role("button", name="Remove").click()
    assert not demo.cart_item(BACKPACK).is_visible()
    assert demo.cart_count() == "1"
    assert demo.cart_item(BIKE_LIGHT).is_visible()

    # 6. Select Continue Shopping and verify that the removed Backpack can be added again.
    demo.continue_shopping()
    assert demo.product_card(BACKPACK).get_by_role("button", name="Add to cart").is_visible()
    demo.add_product(BACKPACK)
    assert demo.cart_count() == "2"
    demo.open_cart()
    assert demo.cart_item(BACKPACK).is_visible()

    # 7. Negative/boundary check: open the cart after removing every item.
    demo.cart_item(BACKPACK).get_by_role("button", name="Remove").click()
    demo.cart_item(BIKE_LIGHT).get_by_role("button", name="Remove").click()
    assert page.locator(".cart_item").count() == 0
    assert not page.locator('[data-test="shopping-cart-badge"]').is_visible()
    assert page.get_by_role("button", name="Continue Shopping").is_visible()
