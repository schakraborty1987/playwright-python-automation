from api_framework.api_client import APIClient
from api_framework.config import OLLAMA_BASE_URL, API_TIMEOUT


def generate_response(prompt: str) -> str:
    """Send a prompt to the local Ollama model and return the response."""

    client = APIClient(
        base_url=OLLAMA_BASE_URL,
        timeout=API_TIMEOUT,
    )

    payload = {
        "model": "llama3.2",
        "prompt": prompt,
        "stream": False,
    }

    response = client.post(
        "/api/generate",
        json=payload,
    )

    response_data = response.json()

    return response_data["response"]