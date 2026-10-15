
from typing import Annotated, Any

from langchain_core.tools import tool
from langgraph.prebuilt import InjectedState #This is a custom state injection for LangGraph workflows. Meaning that the state of the workflow can be injected into the tool function as a parameter.

from api_framework.api_client import APIClient
from pages.SauceDemoPage import SauceDemoPage


@tool
def check_url_status(url: str) -> str:
    """Check whether a URL is reachable and return its HTTP status."""
    client = APIClient(timeout=10)
    response = client.get(url)
    return f"HTTP {response.status_code}"


@tool
def get_page_title(
    page: Annotated[Any, InjectedState("page")],
) -> str:
    """Get the title of the Sauce Demo application using the existing browser page."""
    if page is None:
        raise ValueError(
            "A Playwright page must be provided in the workflow state."
        )

    page.goto(SauceDemoPage.BASE_URL)
    return page.title()


QA_TOOLS = [
    check_url_status,
    get_page_title,
]
