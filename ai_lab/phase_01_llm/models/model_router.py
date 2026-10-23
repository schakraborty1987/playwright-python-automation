from ai_lab.phase_01_llm.models.base_model import BaseModel
from ai_lab.phase_01_llm.models.ollama_model import OllamaModel
from ai_lab.phase_01_llm.models.gemini_model import GeminiModel
from api_framework.config import MODEL_PROVIDER


class ModelRouter:
    """Provider selection and common LLM entry point."""

    def __init__(self, provider: str | None = None):
        self.provider = (provider or MODEL_PROVIDER).strip().lower()
        providers: dict[str, type[BaseModel]] = {
            "ollama": OllamaModel,
            "gemini": GeminiModel,
        }
        try:
            self.model = providers[self.provider]()
        except KeyError as exc:
            raise ValueError(f"Unsupported model provider: {self.provider}") from exc

    def generate(self, prompt: str) -> str:
        """Generate a plain-text response through the selected adapter."""
        return self.model.generate(prompt)

    def bind_tools(self, tools):
        """Bind tools through the provider-neutral adapter contract."""
        return self.model.bind_tools(tools)
