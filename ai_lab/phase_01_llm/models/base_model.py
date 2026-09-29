from abc import ABC, abstractmethod


class BaseModel(ABC):
    """
    Common interface for all LLM implementations.
    """

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """
        Generate a response from the model.
        """
        pass