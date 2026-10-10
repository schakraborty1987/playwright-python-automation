
from google import genai
from api_framework.config import GEMINI_MODEL


def _get_client():
    """Create a Gemini API client using the configured API key."""
    return genai.Client()


def generate_response_cloud(prompt: str) -> str:
    """
    Send a prompt to the Gemini cloud model
    and return the generated response.
    """
    client = _get_client()

    interaction = client.interactions.create(
        model=GEMINI_MODEL,
        input=prompt,
    )

    return interaction.output_text


def generate_structured_cloud(prompt: str, schema: dict) -> str:
    """
    Ask Gemini to return a response matching the supplied JSON schema.
    Returns the generated JSON as a string.
    """
    client = _get_client()

    interaction = client.interactions.create(
        model=GEMINI_MODEL,
        input=prompt,
        response_format={
            "type": "text",
            "mime_type": "application/json",
            "schema": schema,
        },
    )

    return interaction.output_text


def select_cloud_tool(prompt: str, tools: list) -> dict:
    """
    Ask Gemini to select a function from the supplied tool definitions.

    Returns the selected function name, arguments, call ID, and
    interaction ID. This function selects a tool; it does not execute it.
    """
    client = _get_client()

    interaction = client.interactions.create(
        model=GEMINI_MODEL,
        input=prompt,
        tools=tools,
    )

    for step in interaction.steps:
        if step.type == "function_call":
            return {
                "name": step.name,
                "arguments": step.arguments,
                "call_id": step.id,
                "interaction_id": interaction.id,
            }

    return {
        "name": None,
        "arguments": {},
        "call_id": None,
        "interaction_id": interaction.id,
    }
