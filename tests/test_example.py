import time


def test_example(page):
    page.goto("https://playwright.dev/")
    time.sleep(5)
    assert "Playwright" in page.title()
