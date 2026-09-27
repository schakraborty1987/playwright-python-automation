from ai_lab.phase_01_llm.local_ollama import generate_response_local
from ai_lab.phase_01_llm.tools import check_url_status


# Tool Registry
#
# The agent knows about available tools through this registry.
# The key is the tool name that the LLM can select.
# The value is the actual Python function that will be executed.
TOOL_REGISTRY = {
    "check_url_status": check_url_status,
}


SAUCE_DEMO_URL = "https://www.saucedemo.com/"


def run_agent(user_prompt: str) -> str:
    """
    Simple educational Python agent.

    The LLM decides whether a tool is required.
    The Tool Registry maps the selected tool name
    to the corresponding Python function.
    """

    decision_prompt = f"""
You are a routing agent.

Your job is to decide whether the user's question
requires one of the available tools.

Available tool:

1. check_url_status
   - Checks whether a URL is reachable.
   - Returns the HTTP status code.

RULES:

If the user asks about the availability, status,
or whether Sauce Demo is up, respond with exactly:

check_url_status

For every other question, respond with exactly:

ANSWER

Examples:

User: Is Sauce Demo available?
Response: check_url_status

User: Is Sauce Demo up?
Response: check_url_status

User: What is the status of Sauce Demo?
Response: check_url_status

User: What is Playwright?
Response: ANSWER

User: Explain Python.
Response: ANSWER

Do not provide any explanation.
Do not provide any other text.

User request:
{user_prompt}

Decision:
"""

    decision = generate_response_local(decision_prompt).strip()

    print("\nAgent Decision:")
    print(repr(decision))

    # ---------------------------------------------------------
    # Tool execution through the Tool Registry
    # ---------------------------------------------------------

    if decision in TOOL_REGISTRY:

        print("\nSelected Tool:")
        print(decision)

        tool = TOOL_REGISTRY[decision]

        print("\nExecuting Tool:")
        print(decision)

        tool_result = tool(SAUCE_DEMO_URL)

        print("\nTool Result:")
        print(tool_result)

        final_prompt = f"""
Answer the user's question using the tool result below.

User question:
{user_prompt}

Tool used:
{decision}

Tool result:
{tool_result}

Give a concise and accurate answer.
"""

        final_response = generate_response_local(final_prompt)

        print("\nFinal Answer:")
        print(final_response)

        return final_response

    # ---------------------------------------------------------
    # No tool required
    # ---------------------------------------------------------

    print("\nNo tool required.")

    final_response = generate_response_local(user_prompt)

    print("\nFinal Answer:")
    print(final_response)

    return final_response