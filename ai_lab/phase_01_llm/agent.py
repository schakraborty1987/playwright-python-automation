from ai_lab.phase_01_llm.local_ollama import generate_response_local
from ai_lab.phase_01_llm.tools import check_url_status


def run_agent(user_prompt: str) -> str:
    """
    Simple educational Python agent.

    The LLM decides whether the request requires
    the Sauce Demo URL status tool.
    """

    decision_prompt = f"""
You are a routing agent.

Your job is to decide whether the user's question
requires calling the Sauce Demo URL status tool.

The available tool is:

check_url_status

- Accepts a URL as input.
- Checks whether the URL is reachable.
- Returns the HTTP status of the URL.

RULES:

1. If the user asks about Sauce Demo availability, status,
   whether Sauce Demo is available, or whether Sauce Demo is up,
   respond with exactly:

USE_TOOL

2. For every other question, respond with exactly:

ANSWER

Examples:

User: Is Sauce Demo available?
Response: USE_TOOL

User: Is Sauce Demo up?
Response: USE_TOOL

User: What is the status of Sauce Demo?
Response: USE_TOOL

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

    if decision == "USE_TOOL":
        sauce_demo_url = "https://www.saucedemo.com/"

        print("\nExecuting Tool:")
        print("check_url_status")

        tool_result = check_url_status(sauce_demo_url)

        print("\nTool Result:")
        print(tool_result)

        final_prompt = f"""
Answer the user's question using the tool result below.

User question:
{user_prompt}

Tool result:
{tool_result}

Give a concise answer.
"""

        final_response = generate_response_local(final_prompt)

        print("\nFinal Answer:")
        print(final_response)

        return final_response

    print("\nNo tool required.")

    final_response = generate_response_local(user_prompt)

    print("\nFinal Answer:")
    print(final_response)

    return final_response