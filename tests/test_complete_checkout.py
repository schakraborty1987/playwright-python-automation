# spec: specs/saucedemo-core-operations.plan.md

from pages.SauceDemoPage import SauceDemoPage

BACKPACK = "Sauce Labs Backpack"


def test_complete_checkout_and_place_order(page):
    demo = SauceDemoPage(page)

    # 1. Starting from a fresh browser state, sign in, add Sauce Labs Backpack, open the cart, and select Checkout.
    demo.open()
    demo.login()
    demo.add_product(BACKPACK)
    demo.open_cart()
    demo.checkout()
    assert page.url.endswith("/checkout-step-one.html")
    assert page.get_by_placeholder("First Name").is_visible()
    assert page.get_by_placeholder("Last Name").is_visible()
    assert page.get_by_placeholder("Zip/Postal Code").is_visible()
    assert page.get_by_role("button", name="Cancel").is_visible()
    assert page.get_by_role("button", name="Continue").is_visible()

    # 2. Select Continue without entering any checkout information.
    demo.continue_checkout()
    assert page.url.endswith("/checkout-step-one.html")
    assert page.get_by_text("First Name is required").is_visible()

    # 3. Enter first name Ada, last name Lovelace, and postal code 12345, then select Continue.
    demo.fill_checkout_information("Ada", "Lovelace", "12345")
    demo.continue_checkout()
    assert page.url.endswith("/checkout-step-two.html")
    assert page.get_by_text("Checkout: Overview", exact=True).is_visible()
    assert page.get_by_text(BACKPACK, exact=True).is_visible()
    assert page.get_by_text("Payment Information:", exact=True).is_visible()
    assert page.get_by_text("Shipping Information:", exact=True).is_visible()

    # 4. Verify the displayed totals for the Backpack.
    assert page.locator(".summary_subtotal_label").inner_text() == "Item total: $29.99"
    assert page.locator(".summary_tax_label").inner_text() == "Tax: $2.40"
    assert page.locator(".summary_total_label").inner_text() == "Total: $32.39"

    # 5. Select Finish.
    page.get_by_role("button", name="Finish").click()
    assert page.url.endswith("/checkout-complete.html")
    assert page.get_by_text("Thank you for your order!", exact=True).is_visible()
    assert page.get_by_text("Your order has been dispatched", exact=False).is_visible()
    assert page.get_by_role("button", name="Back Home").is_visible()
    assert page.get_by_role("button", name="Generate PDF order").is_visible()

    # 6. Select Back Home.
    page.get_by_role("button", name="Back Home").click()
    assert page.url.endswith("/inventory.html")
    assert page.get_by_text("Products", exact=True).is_visible()
    assert not page.locator('[data-test="shopping-cart-badge"]').is_visible()

    # 7. Negative check: begin a second checkout attempt with a cart item and leave one required field blank.
    demo.add_product(BACKPACK)
    demo.open_cart()
    demo.checkout()
    page.get_by_placeholder("First Name").fill("Ada")
    page.get_by_placeholder("Zip/Postal Code").fill("12345")
    demo.continue_checkout()
    assert page.url.endswith("/checkout-step-one.html")
    assert page.get_by_text("Last Name is required").is_visible()
    assert not page.get_by_text("Checkout: Overview", exact=True).is_visible()
