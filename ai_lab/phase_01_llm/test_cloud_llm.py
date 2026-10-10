
import json

from ai_lab.phase_01_llm.cloud_api import (
    generate_response_cloud,
    generate_structured_cloud,
    select_cloud_tool,
)


def test_generate_response_cloud():
    prompt = "What is Playwright? Explain it in three sentences."

    response = generate_response_cloud(prompt)

    assert response
    assert "Playwright" in response

    print("\nGemini Response:")
    print(response)


def test_gemini_structured_output():
    schema = {
        "type": "object",
        "properties": {
            "decision": {
                "type": "string",
                "enum": ["GENERAL", "TOOL"],
            }
        },
        "required": ["decision"],
        "additionalProperties": False,
    }

    response = generate_structured_cloud(
        "Classify this request: 'What is the title of the Sauce Demo "
        "application?' Choose TOOL because answering requires inspecting "
        "the application. Return the result using the required JSON schema.",
        schema,
    )

    result = json.loads(response)

    assert result["decision"] == "TOOL"


def test_gemini_tool_selection():
    tools = [
        {
            "type": "function",
            "name": "get_page_title",
            "description": (
                "Get the title of the Sauce Demo application "
                "using its browser page."
            ),
            "parameters": {
                "type": "object",
                "properties": {},
            },
        }
    ]

    result = select_cloud_tool(
        "Use the available function to get the title of the Sauce Demo "
        "application.",
        tools,
    )

    assert result["name"] == "get_page_title"
    assert result["arguments"] == {}
    assert result["call_id"]
    assert result["interaction_id"]
