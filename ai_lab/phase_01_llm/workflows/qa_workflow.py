
from typing import Annotated, Any, TypedDict

from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
)
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

from ai_lab.phase_01_llm.models.gemini_model import GeminiModel
from ai_lab.phase_01_llm.tools import (
    QA_TOOLS,
    check_url_status,
    get_page_title,
)


class QAState(TypedDict, total=False):
    user_prompt: str
    decision: str
    final_response: str
    page: Any
    tool_name: str
    tool_result: str
    messages: Annotated[list[BaseMessage], add_messages]


SYSTEM_INSTRUCTIONS = """
You are a QA automation assistant.
Follow these tool-selection rules:
- For a request about a website's availability, reachability, or HTTP status,
  call check_url_status only.
- For a request asking for a page title, call get_page_title only.
- Never call multiple tools for one request.
- For general questions that do not require a tool, answer directly.
"""


gemini_model = GeminiModel()
model_with_tools = gemini_model.bind_tools(QA_TOOLS)

tool_node = ToolNode([check_url_status])


def call_model(state: QAState) -> dict:
    """Ask Gemini to answer or request a tool."""
    messages = state.get("messages", [])

    if not messages:
        messages = [HumanMessage(content=state["user_prompt"])]

    response = model_with_tools.invoke(
        [SystemMessage(content=SYSTEM_INSTRUCTIONS), *messages]
    )

    updates = {"messages": [response]}

    # Preserve the initial human message in graph state.
    if not state.get("messages"):
        updates["messages"] = [
            messages[0],
            response,
        ]

    if response.tool_calls:
        updates["decision"] = "TOOL"
        updates["tool_name"] = response.tool_calls[0]["name"]
    else:
        updates["decision"] = state.get("decision") or "GENERAL"
        updates["final_response"] = str(response.content)

    return updates


def route_tool_call(state: QAState) -> str:
    """Route browser tools separately from other tools."""
    messages = state.get("messages", [])

    if not messages or not isinstance(messages[-1], AIMessage):
        return "finish"

    tool_calls = messages[-1].tool_calls

    if not tool_calls:
        return "finish"

    # Do not allow the model to schedule browser operations
    # alongside other tool calls.
    if len(tool_calls) != 1:
        raise ValueError(
            f"Expected one tool call, received: "
            f"{[call['name'] for call in tool_calls]}"
        )

    tool_name = tool_calls[0]["name"]

    if tool_name == "get_page_title":
        return "playwright"

    if tool_name == "check_url_status":
        return "tools"

    raise ValueError(f"Unsupported tool call: {tool_name}")


def execute_playwright_tool(state: QAState) -> dict:
    """Run the synchronous Playwright operation on this graph node."""
    response = state["messages"][-1]
    tool_call = response.tool_calls[0]

    page = state.get("page")
    if page is None:
        raise ValueError(
            "Pass the existing Playwright page in workflow state."
        )

    # Call the underlying Python function directly.
    result = get_page_title.func(page=page)

    return {
        "messages": [
            ToolMessage(
                content=str(result),
                tool_call_id=tool_call["id"],
                name=tool_call["name"],
            )
        ],
        "tool_name": tool_call["name"],
        "tool_result": str(result),
    }


def capture_tool_result(state: QAState) -> dict:
    """Capture the latest browser-independent tool result."""
    for message in reversed(state.get("messages", [])):
        if isinstance(message, ToolMessage):
            return {
                "tool_name": message.name or "",
                "tool_result": str(message.content),
            }

    return {}


def build_qa_workflow():
    workflow = StateGraph(QAState)

    workflow.add_node("call_model", call_model)
    workflow.add_node("playwright_tool", execute_playwright_tool)
    workflow.add_node("tools", tool_node)
    workflow.add_node("capture_tool_result", capture_tool_result)

    workflow.add_edge(START, "call_model")

    workflow.add_conditional_edges(
        "call_model",
        route_tool_call,
        {
            "playwright": "playwright_tool",
            "tools": "tools",
            "finish": END,
        },
    )

    workflow.add_edge("playwright_tool", "call_model")
    workflow.add_edge("tools", "capture_tool_result")
    workflow.add_edge("capture_tool_result", "call_model")

    return workflow.compile()


qa_workflow = build_qa_workflow()
