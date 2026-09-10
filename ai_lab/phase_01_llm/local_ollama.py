from api_framework.api_client import APIClient
from api_framework.config import OLLAMA_BASE_URL, API_TIMEOUT, OLLAMA_MODEL


def generate_response_local(prompt: str) -> str:
    """Send a prompt to the local Ollama model and return the response."""

    client = APIClient(
        base_url=OLLAMA_BASE_URL,
        timeout=API_TIMEOUT,
    )

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False, # This is set to False to get the complete response in one go. If set to True, the response would be streamed in chunks.
    }

    response = client.post(
        "/api/generate",
        json=payload,
    )

    response_data = response.json()

    return response_data["response"]