
from langchain_core.messages import HumanMessage, ToolMessage

from ai_lab.phase_01_llm.models.gemini_model import GeminiModel
from ai_lab.phase_01_llm.tools import QA_TOOLS


SAUCE_DEMO_URL = "https://www.saucedemo.com/"

gemini_model = GeminiModel()
model_with_tools = gemini_model.bind_tools(QA_TOOLS)


def _content_to_text(content) -> str:
    """Convert Gemini/LangChain message content to readable text."""
    if isinstance(content, str):
        return content

    if isinstance(content, list):
        parts = [
            item["text"]
            for item in content
            if isinstance(item, dict)
            and item.get("type") == "text"
            and isinstance(item.get("text"), str)
        ]
        if parts:
            return "\n".join(parts)

    return str(content)


def _is_availability_request(user_prompt: str) -> bool:
    """Identify requests that should use the URL-status tool."""
    prompt = user_prompt.lower()
    keywords = (
        "available",
        "availability",
        "reachable",
        "reachability",
        "http status",
        "website status",
        "site status",
        "is the website up",
        "is the site up",
    )
    return any(keyword in prompt for keyword in keywords)


def _find_tool(tool_name: str):
    """Find a LangChain tool by name."""
    return next(
        (tool for tool in QA_TOOLS if tool.name == tool_name),
        None,
    )


def run_agent(user_prompt: str, page=None) -> str:
    """
    Use Gemini native tool calling to answer QA requests.

    Availability requests use the URL-status tool directly.
    Browser tools reuse the Playwright page supplied by the caller.
    """
    print("\nUser Request:")
    print(user_prompt)

    # Deterministic routing prevents an availability request from
    # incorrectly selecting a browser tool that requires a page fixture.
    if _is_availability_request(user_prompt):
        status_tool = _find_tool("check_url_status")

        if status_tool is None:
            return "The check_url_status tool is not configured."

        try:
            tool_result = status_tool.invoke({"url": SAUCE_DEMO_URL})
        except Exception as exc:
            return f"Could not check Sauce Demo availability: {exc}"

        print("\nSelected Tool:")
        print("check_url_status")
        print("\nTool Result:")
        print(tool_result)

        if str(tool_result).startswith("HTTP 2"):
            answer = f"Sauce Demo is available. {tool_result}"
        else:
            answer = f"Sauce Demo returned the following status: {tool_result}"

        print("\nFinal Answer:")
        print(answer)
        return answer

    human_message = HumanMessage(content=user_prompt)

    try:
        response = model_with_tools.invoke([human_message])

        # Gemini can answer without requesting any tool.
        if not response.tool_calls:
            answer = _content_to_text(response.content)
            print("\nFinal Answer:")
            print(answer)
            return answer

        tool_messages = []

        # Execute every tool requested in this response.
        for tool_call in response.tool_calls:
            tool_name = tool_call["name"]
            arguments = tool_call.get("args", {})

            print("\nSelected Tool:")
            print(tool_name)
            print("\nTool Arguments:")
            print(arguments)

            selected_tool = _find_tool(tool_name)

            if selected_tool is None:
                return f"Unsupported tool requested: {tool_name}"

            if tool_name == "get_page_title":
                if page is None:
                    return (
                        "The Playwright page is required for "
                        "the get_page_title tool."
                    )

                # Reuse the existing Playwright page; do not create a browser.
                tool_result = selected_tool.func(page=page)
            else:
                tool_result = selected_tool.invoke(arguments)

            print("\nTool Result:")
            print(tool_result)

            tool_messages.append(
                ToolMessage(
                    content=str(tool_result),
                    tool_call_id=tool_call["id"],
                )
            )

        # Give Gemini the tool results so it can formulate the final answer.
        final_response = model_with_tools.invoke(
            [
                human_message,
                response,
                *tool_messages,
            ]
        )

        answer = _content_to_text(final_response.content)

        print("\nFinal Answer:")
        print(answer)
        return answer

    except Exception as exc:
        print(f"\nAgent execution failed: {exc}")
        return f"Agent execution failed: {exc}"
