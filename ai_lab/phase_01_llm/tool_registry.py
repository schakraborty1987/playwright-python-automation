
from ai_lab.phase_01_llm.tools import check_url_status, get_page_title


TOOL_REGISTRY = {
    "check_url_status": {
        "function": check_url_status,
        "description": "Check whether a URL is reachable and return its HTTP status.",
        "requires_page": False,
        "parameters": {
            "url": {
                "type": "string",
                "description": "The URL to check.",
            }
        },
    },
    "get_page_title": {
        "function": get_page_title,
        "description": (
            "Open Sauce Demo using the existing Playwright page "
            "and return its page title."
        ),
        "requires_page": True,
        "parameters": {},
    },
}


def get_gemini_tool_declarations() -> list:
    """Generate Gemini function declarations from the tool registry."""
    declarations = []

    for name, tool in TOOL_REGISTRY.items():
        properties = {
            parameter_name: {
                "type": parameter["type"],
                "description": parameter["description"],
            }
            for parameter_name, parameter in tool["parameters"].items()
        }

        parameters_schema = {
            "type": "object",
            "properties": properties,
        }

        if properties:
            parameters_schema["required"] = list(properties.keys())

        declarations.append(
            {
                "type": "function",
                "name": name,
                "description": tool["description"],
                "parameters": parameters_schema,
            }
        )

    return declarations
