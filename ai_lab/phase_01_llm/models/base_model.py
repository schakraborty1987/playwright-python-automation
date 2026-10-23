from abc import ABC, abstractmethod
from typing import Sequence

from langchain_core.runnables import Runnable
from langchain_core.tools import BaseTool


class BaseModel(ABC):
    """Provider-neutral contract for chat generation and tool binding."""

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """Generate a plain-text response."""
        raise NotImplementedError

    @abstractmethod
    def bind_tools(self, tools: Sequence[BaseTool]) -> Runnable:
        """Return a runnable model configured with the supplied tools."""
        raise NotImplementedError
