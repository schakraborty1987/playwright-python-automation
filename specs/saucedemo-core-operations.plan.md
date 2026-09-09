# SauceDemo Core User Operations Test Plan

## Application Overview

SauceDemo (Swag Labs) is an e-commerce demo storefront. Users authenticate with a supplied demo account, browse and sort a six-product catalog, open product details, add or remove products from a cart, enter checkout information, review calculated totals, place an order, and return home or log out. The plan covers three independent end-user operations using the observed UI and assumes a fresh browser state at the beginning of every test.

## Test Scenarios

### 1. Core end-user operations

**Seed:** `seed.spec.ts`

#### 1.1. Authenticate and browse the product catalog

**File:** `specs/core/authenticate-and-browse.spec.ts`

**Steps:**
  1. Starting from a fresh browser state, navigate to https://www.saucedemo.com/.
    - expect: The Swag Labs login page is displayed with Username, Password, and Login controls.
    - expect: The page provides the accepted demo usernames and the shared password.
  2. Enter `standard_user` in Username and `secret_sauce` in Password, then select Login.
    - expect: The user is authenticated and navigated to `/inventory.html`.
    - expect: The Products heading, sorting control, product cards, and navigation controls are displayed.
  3. Verify that the catalog shows the six expected products, including Sauce Labs Backpack, Sauce Labs Bike Light, Sauce Labs Bolt T-Shirt, Sauce Labs Fleece Jacket, Sauce Labs Onesie, and Test.allTheThings() T-Shirt (Red), with names, descriptions, prices, and Add to cart controls.
    - expect: Each product has a visible name, description, price, and actionable Add to cart control.
  4. Open the Sauce Labs Backpack product link.
    - expect: The product detail page shows the product image, name, description, price, Add to cart control, and Back to products control.
  5. Use the sort combobox to select Price (low to high), then select Name (Z to A).
    - expect: The product order changes after each selection according to the selected sorting rule.
  6. Log out through the Open Menu navigation.
    - expect: The session ends and the login page is displayed.
    - expect: Authenticated catalog content is no longer visible.
  7. Negative check: from the fresh login page, submit Login with an empty Username and Password.
    - expect: Login is rejected.
    - expect: A required-field validation message is displayed and the user remains on the login page.

#### 1.2. Manage the shopping cart

**File:** `specs/core/manage-cart.spec.ts`

**Steps:**
  1. Starting from a fresh browser state, navigate to https://www.saucedemo.com/, sign in as `standard_user` with password `secret_sauce`, and remain on the product catalog.
    - expect: The inventory page is displayed with an initially empty cart indicator.
  2. Select Add to cart for Sauce Labs Backpack from the catalog.
    - expect: The Backpack control changes to Remove.
    - expect: The cart indicator shows 1 item.
  3. Open the shopping cart.
    - expect: The cart page displays Your Cart, one Backpack line item, quantity 1, its description, and price $29.99.
    - expect: Continue Shopping and Checkout controls are available.
  4. Select Continue Shopping, add Sauce Labs Bike Light, and reopen the cart.
    - expect: The cart indicator shows 2 items.
    - expect: The cart contains both the Backpack and Bike Light as separate line items with quantity 1 each.
  5. Remove the Backpack from the cart.
    - expect: The Backpack line item is removed.
    - expect: The cart indicator decreases to 1 and the Bike Light remains.
  6. Select Continue Shopping and verify that the removed Backpack can be added again.
    - expect: The catalog is displayed and the Backpack has an Add to cart control.
    - expect: Adding it restores the cart indicator and cart line item.
  7. Negative/boundary check: open the cart after removing every item.
    - expect: The cart contains no product line items and no stale item count is shown.
    - expect: Continue Shopping remains available and Checkout does not proceed to a purchasable order without items.

#### 1.3. Complete checkout and place an order

**File:** `specs/core/complete-checkout.spec.ts`

**Steps:**
  1. Starting from a fresh browser state, sign in as `standard_user` with password `secret_sauce`, add Sauce Labs Backpack, open the cart, and select Checkout.
    - expect: The Checkout: Your Information page is displayed.
    - expect: First Name, Last Name, Zip/Postal Code, Cancel, and Continue controls are visible.
  2. Select Continue without entering any checkout information.
    - expect: The user remains on the information page.
    - expect: A required-field error is displayed and checkout does not advance.
  3. Enter first name `Ada`, last name `Lovelace`, and postal code `12345`, then select Continue.
    - expect: The Checkout: Overview page is displayed.
    - expect: The Backpack is listed with quantity 1 and price $29.99.
    - expect: Payment information, shipping information, item total, tax, total, Cancel, and Finish are displayed.
  4. Verify the displayed totals for the Backpack.
    - expect: Item total is $29.99, tax is $2.40, and total is $32.39.
  5. Select Finish.
    - expect: The Checkout: Complete! page is displayed.
    - expect: A Thank you for your order! confirmation and dispatch message are shown.
    - expect: Back Home and Generate PDF order controls are available.
  6. Select Back Home.
    - expect: The user returns to the product catalog.
    - expect: The completed order does not leave the previous cart item as an active checkout.
  7. Negative check: begin a second checkout attempt with a cart item and leave one or more required information fields blank before selecting Continue.
    - expect: The corresponding required-field validation error identifies the missing field.
    - expect: The user cannot reach Checkout: Overview until all required fields are provided.
