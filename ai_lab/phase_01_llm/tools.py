from api_framework.api_client import APIClient
from pages.SauceDemoPage import SauceDemoPage


def check_url_status(url: str) -> str:
    """
    Check whether a URL is reachable and return its HTTP status.
    """

    client = APIClient(timeout=10)

    response = client.get(url)

    return f"HTTP {response.status_code}"


def get_page_title(page) -> str:
    """
    Return the title of the Sauce Demo application page
    using the existing Playwright page.
    """

    page.goto(SauceDemoPage.BASE_URL)

    return page.title()