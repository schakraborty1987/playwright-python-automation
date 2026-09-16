from api_framework.api_client import APIClient

def check_url_status(url: str) -> str:
    """
    Check whether a URL is reachable and return its HTTP status.
    """

    client = APIClient(timeout=10)

    response = client.get(url)

    return f"HTTP {response.status_code}"