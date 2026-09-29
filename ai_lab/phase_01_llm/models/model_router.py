from ai_lab.phase_01_llm.models.base_model import BaseModel
from ai_lab.phase_01_llm.models.ollama_model import OllamaModel
from ai_lab.phase_01_llm.models.gemini_model import GeminiModel


class ModelRouter:
    """
    Provides a common entry point for selecting the LLM.
    """

    def __init__(self, provider: str = "ollama"):
        self.provider = provider.lower()

        if self.provider == "ollama":
            self.model: BaseModel = OllamaModel()

        elif self.provider == "gemini":
            self.model: BaseModel = GeminiModel()

        else:
            raise ValueError(f"Unsupported model provider: {provider}")

    def generate(self, prompt: str) -> str:
        return self.model.generate(prompt)