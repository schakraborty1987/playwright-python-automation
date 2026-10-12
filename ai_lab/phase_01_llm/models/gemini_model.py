from ai_lab.phase_01_llm.models.base_model import BaseModel
from ai_lab.phase_01_llm.cloud_api import (
    generate_response_cloud,
    select_cloud_tool,
)


class GeminiModel(BaseModel):
    """Gemini adapter supporting text generation and tool selection."""

    def generate(self, prompt: str) -> str:
        return generate_response_cloud(prompt)

    def select_tool(self, prompt: str, tools: list) -> dict:
        return select_cloud_tool(prompt, tools)