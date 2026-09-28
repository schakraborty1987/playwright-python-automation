import json

from ai_lab.phase_01_llm.local_ollama import generate_response_local
from ai_lab.phase_01_llm.tool_registry import TOOL_REGISTRY


SAUCE_DEMO_URL = "https://www.saucedemo.com/"


def run_agent(user_prompt: str, page=None) -> str:
    """
    Simple educational Python agent.

    The LLM decides:
    1. Which tool, if any, is required.
    2. What arguments should be passed to that tool.

    The selected tool is then looked up through the Tool Registry
    and executed dynamically.
    """

    available_tools = "\n".join(
        f"- {name}: {details['description']}\n"
        f"  Parameters: {details['parameters']}"
        for name, details in TOOL_REGISTRY.items()
    )

    decision_prompt = f"""
You are a routing agent.

Your job is to decide whether the user's question requires
one of the available tools.

Available tools:

{available_tools}

Known application context:

Sauce Demo URL:
{SAUCE_DEMO_URL}

Rules:

Return ONLY valid JSON.

If a tool is required, return:

{{
    "tool": "tool_name",
    "arguments": {{
        "argument_name": "argument_value"
    }}
}}

If no tool is required, return:

{{
    "tool": "ANSWER",
    "arguments": {{}}
}}

Available tool names:
{", ".join(TOOL_REGISTRY.keys())}

Examples:

User: Is Sauce Demo available?

Response:
{{
    "tool": "check_url_status",
    "arguments": {{
        "url": "{SAUCE_DEMO_URL}"
    }}
}}

User: What is the title of the Sauce Demo application?

Response:
{{
    "tool": "get_page_title",
    "arguments": {{}}
}}

User: What is Playwright?

Response:
{{
    "tool": "ANSWER",
    "arguments": {{}}
}}

Do not provide any explanation.
Do not provide markdown.
Do not wrap the JSON in ```.

User request:
{user_prompt}

Decision:
"""

    decision_response = generate_response_local(decision_prompt).strip()

    print("\nAgent Decision:")
    print(decision_response)

    try:
        decision = json.loads(decision_response)
    except json.JSONDecodeError:
        return "The agent returned an invalid tool decision."

    tool_name = decision.get("tool")
    arguments = decision.get("arguments", {})

    print("\nSelected Tool:")
    print(tool_name)

    print("\nTool Arguments:")
    print(arguments)

    if tool_name == "ANSWER":
        print("\nNo tool required.")

        final_response = generate_response_local(user_prompt)

        print("\nFinal Answer:")
        print(final_response)

        return final_response

    if tool_name not in TOOL_REGISTRY:
        return f"I could not execute the requested tool: {tool_name}"

    tool_definition = TOOL_REGISTRY[tool_name]
    tool_function = tool_definition["function"]

    print("\nExecuting Tool:")
    print(tool_name)

    if tool_definition["requires_page"]:
        if page is None:
            return "The Playwright page is required for this tool."

        tool_result = tool_function(page, **arguments)

    else:
        tool_result = tool_function(**arguments)

    print("\nTool Result:")
    print(tool_result)

    final_prompt = f"""
Answer the user's question using the tool result below.

User question:
{user_prompt}

Tool used:
{tool_name}

Tool arguments:
{arguments}

Tool result:
{tool_result}

Give a concise and accurate answer.
"""

    final_response = generate_response_local(final_prompt)

    print("\nFinal Answer:")
    print(final_response)

    return final_response