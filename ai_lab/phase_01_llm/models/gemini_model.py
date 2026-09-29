from ai_lab.phase_01_llm.models.base_model import BaseModel
from ai_lab.phase_01_llm.cloud_api import generate_response_cloud


class GeminiModel(BaseModel):
    """
    Gemini implementation of the common model interface.
    """

    def generate(self, prompt: str) -> str:
        return generate_response_cloud(prompt)