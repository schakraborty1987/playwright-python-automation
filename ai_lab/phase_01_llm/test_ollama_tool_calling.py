
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_ollama import ChatOllama

from ai_lab.phase_01_llm.tools import check_url_status


def test_ollama_executes_existing_tool():
    model = ChatOllama(
        model="llama3.2",
        temperature=0,
    )

    model_with_tools = model.bind_tools([check_url_status])

    messages = [
        HumanMessage(
            content=(
                "Check whether https://www.saucedemo.com/ is reachable. "
                "You must use the check_url_status tool."
            )
        )
    ]

    # 1. Ask Ollama to choose a tool.
    response = model_with_tools.invoke(messages)

    print("\nRequested tool calls:")
    print(response.tool_calls)

    assert response.tool_calls, "Ollama did not request a tool."

    # 2. Execute each requested tool locally.
    tool_messages = []

    for tool_call in response.tool_calls:
        assert tool_call["name"] == "check_url_status"

        result = check_url_status.invoke(tool_call.get("args", {}))

        print("\nActual tool result:")
        print(result)

        tool_messages.append(
            ToolMessage(
                content=str(result),
                tool_call_id=tool_call["id"],
            )
        )

    # 3. Send the actual tool result back to Ollama.
    final_response = model_with_tools.invoke(
        messages + [response] + tool_messages
    )

    print("\nFinal response:")
    print(final_response.content)

    assert final_response.content
    assert "HTTP" in str(final_response.content)
