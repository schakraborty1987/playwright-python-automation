from ai_lab.phase_01_llm.local_ollama import generate_response_local
from ai_lab.phase_01_llm.models.base_model import BaseModel


class OllamaModel(BaseModel):
    """
    Ollama implementation of the common model interface.
    """

    def generate(self, prompt: str) -> str:
        return generate_response_local(prompt)