from langchain_ollama import ChatOllama

from ai_lab.phase_01_llm.models.base_model import BaseModel
from api_framework.config import OLLAMA_BASE_URL, OLLAMA_MODEL

class OllamaModel(BaseModel):
    """Ollama adapter for text generation and native tool calling."""

    def __init__(self):
        self.model = ChatOllama(
            base_url=OLLAMA_BASE_URL,
            model=OLLAMA_MODEL,
            temperature=0,
        )

    def generate(self, prompt: str) -> str:
        """Generate a regular text response."""
        response = self.model.invoke(prompt)
        return str(response.content)

    def bind_tools(self, tools: list):
        """Bind LangChain tools to Ollama for native tool calling."""
        return self.model.bind_tools(tools)
