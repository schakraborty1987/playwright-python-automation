from google import genai
from api_framework.config import GEMINI_MODEL


def generate_response_cloud(prompt: str) -> str:
    """
    Send a prompt to the Gemini cloud model
    and return the generated response.
    """

    client = genai.Client()

    interaction = client.interactions.create(
        model=GEMINI_MODEL,
        input=prompt,
    )

    return interaction.output_text