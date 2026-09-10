from api_framework.api_client import APIClient
from api_framework.config import OLLAMA_BASE_URL, API_TIMEOUT


def test_get_ollama_models():
    client = APIClient(
        base_url=OLLAMA_BASE_URL,
        timeout=API_TIMEOUT,
    )

    response = client.get("/api/tags")

    assert response.status_code == 200

    data = response.json()

    assert "models" in data
    assert any(model["name"] == "llama3.2:latest" for model in data["models"])