from ai_lab.phase_01_llm.local_ollama import generate_response_local
from ai_lab.phase_01_llm.tools import get_sauce_demo_status


def run_agent(user_prompt: str) -> str:
    """
    Simple educational python agent.

    The LLM decides whether the request requires
    the Sauce Demo status tool.
    """

    decision_prompt = f"""
You are a simple routing agent.

User request:
{user_prompt}

Decide what action is required.

If the user is asking about the availability or status
of Sauce Demo, respond with exactly:

USE_TOOL

Otherwise respond with exactly:

ANSWER
"""

    decision = generate_response_local(decision_prompt).strip()
    print("\nAgent Decision:")
    print(repr(decision))

    if decision == "USE_TOOL":
        tool_result = get_sauce_demo_status()

        final_prompt = f"""
Answer the user's question using the tool result below.

User question:
{user_prompt}

Tool result:
{tool_result}

Give a concise answer.
"""

        return generate_response_local(final_prompt)

    return generate_response_local(user_prompt)