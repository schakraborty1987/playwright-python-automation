import requests
from typing import Any, Optional


class APIClient:
    """
    Generic HTTP API client built on top of the requests library.

    Provides reusable wrappers for common HTTP methods:
    GET, POST, PUT, PATCH and DELETE.
    """

    def __init__(
        self,
        base_url: str = "",
        headers: Optional[dict[str, str]] = None,
        timeout: int = 30,
    ):
        self.base_url = base_url.rstrip("/")
        self.headers = headers or {}
        self.timeout = timeout
        self.session = requests.Session()

        if self.headers:
            self.session.headers.update(self.headers)

    def _build_url(self, endpoint: str) -> str:
        """Build the complete URL from base URL and endpoint."""
        if endpoint.startswith("http://") or endpoint.startswith("https://"):
            return endpoint

        return f"{self.base_url}/{endpoint.lstrip('/')}"

    def _request(
        self,
        method: str,
        endpoint: str,
        **kwargs: Any,
    ) -> requests.Response:
        """
        Execute an HTTP request and return the raw response.
        """
        url = self._build_url(endpoint)

        response = self.session.request(
            method=method,
            url=url,
            timeout=self.timeout,
            **kwargs,
        )

        response.raise_for_status()

        return response

    def get(
        self,
        endpoint: str,
        params: Optional[dict[str, Any]] = None,
        **kwargs: Any,
    ) -> requests.Response:
        """Send a GET request."""
        return self._request(
            "GET",
            endpoint,
            params=params,
            **kwargs,
        )

    def post(
        self,
        endpoint: str,
        json: Optional[dict[str, Any]] = None,
        **kwargs: Any,
    ) -> requests.Response:
        """Send a POST request."""
        return self._request(
            "POST",
            endpoint,
            json=json,
            **kwargs,
        )

    def put(
        self,
        endpoint: str,
        json: Optional[dict[str, Any]] = None,
        **kwargs: Any,
    ) -> requests.Response:
        """Send a PUT request."""
        return self._request(
            "PUT",
            endpoint,
            json=json,
            **kwargs,
        )

    def patch(
        self,
        endpoint: str,
        json: Optional[dict[str, Any]] = None,
        **kwargs: Any,
    ) -> requests.Response:
        """Send a PATCH request."""
        return self._request(
            "PATCH",
            endpoint,
            json=json,
            **kwargs,
        )

    def delete(
        self,
        endpoint: str,
        **kwargs: Any,
    ) -> requests.Response:
        """Send a DELETE request."""
        return self._request(
            "DELETE",
            endpoint,
            **kwargs,
        )