
from langchain_google_genai import ChatGoogleGenerativeAI

from ai_lab.phase_01_llm.models.base_model import BaseModel
from api_framework.config import GEMINI_MODEL


class GeminiModel(BaseModel):
    """Gemini adapter for text generation and native tool calling."""

    def __init__(self):
        self.model = ChatGoogleGenerativeAI(
            model=GEMINI_MODEL,
            temperature=0,
        )

    def generate(self, prompt: str) -> str:
        """Generate a regular text response."""
        response = self.model.invoke(prompt)
        return str(response.content)

    def bind_tools(self, tools: list):
        """Bind LangChain tools to Gemini for native tool calling."""
        return self.model.bind_tools(tools)
