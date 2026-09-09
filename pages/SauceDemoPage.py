from playwright.sync_api import Page

# Reusable page object for the SauceDemo storefront.
class SauceDemoPage:
    """Reusable page object for the SauceDemo storefront."""

    BASE_URL = "https://www.saucedemo.com/"

    def __init__(self, page: Page):
        self.page = page

    def open(self):
        self.page.goto(self.BASE_URL)

    def login(self, username="standard_user", password="secret_sauce"):
        self.page.get_by_placeholder("Username").fill(username)
        self.page.get_by_placeholder("Password").fill(password)
        self.page.get_by_role("button", name="Login").click()

    def logout(self):
        self.page.get_by_role("button", name="Open Menu").click()
        self.page.locator('[data-test="logout-sidebar-link"]').click()

    def product_card(self, product_name):
        return self.page.locator(".inventory_item").filter(has_text=product_name)

    def add_product(self, product_name):
        self.product_card(product_name).get_by_role("button", name="Add to cart").click()

    def open_product(self, product_name):
        self.product_card(product_name).locator('[data-test$="-title-link"]').click()

    def open_cart(self):
        self.page.locator('[data-test="shopping-cart-link"]').click()

    def cart_item(self, product_name):
        return self.page.locator(".cart_item").filter(has_text=product_name)

    def cart_count(self):
        return self.page.locator('[data-test="shopping-cart-badge"]').inner_text()

    def continue_shopping(self):
        self.page.get_by_role("button", name="Continue Shopping").click()

    def checkout(self):
        self.page.get_by_role("button", name="Checkout").click()

    def fill_checkout_information(self, first_name, last_name, postal_code):
        self.page.get_by_placeholder("First Name").fill(first_name)
        self.page.get_by_placeholder("Last Name").fill(last_name)
        self.page.get_by_placeholder("Zip/Postal Code").fill(postal_code)

    def continue_checkout(self):
        self.page.get_by_role("button", name="Continue").click()
