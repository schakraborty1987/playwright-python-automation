from api_framework.api_client import APIClient
from api_framework.config import OLLAMA_BASE_URL, API_TIMEOUT, OLLAMA_MODEL

def test_get_ollama_models():
    client = APIClient(
        base_url=OLLAMA_BASE_URL,
        timeout=API_TIMEOUT,
    )

    response = client.get("/api/tags") #This is the endpoint to get the list of available models from the local Ollama server

    assert response.status_code == 200

    data = response.json()

    assert "models" in data
    assert any(model["name"] == OLLAMA_MODEL for model in data["models"]) # This checks if the model "llama3.2:latest" is present in the list of available models