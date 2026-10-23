import re
from typing import Annotated, Any, Sequence, TypedDict

from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
)
from langchain_core.tools import BaseTool
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

from api_framework.config import MODEL_PROVIDER
from ai_lab.phase_01_llm.models.model_router import ModelRouter
from ai_lab.phase_01_llm.tools import QA_TOOLS, get_page_title


MAX_TOOL_ROUNDS = 5

SYSTEM_INSTRUCTIONS = """
You are a QA automation assistant.

Rules:
- Use check_url_status for website availability, reachability, or HTTP status.
- Use get_page_title to inspect the Sauce Demo page title when requested.
- For general questions, answer directly without a tool.
- Request tools only when needed.
- You may request tools sequentially, using earlier results to guide later calls.
- Never claim a tool was executed unless its result is available.
"""


class QAState(TypedDict, total=False):
    user_prompt: str
    intent: str
    decision: str
    final_response: str
    page: Any
    tool_name: str
    tool_result: str
    tool_rounds: int
    messages: Annotated[list[BaseMessage], add_messages]


def classify_request(state: QAState) -> dict[str, str]:
    """Classify supported request types before invoking a tool-enabled model."""
    prompt = state["user_prompt"].lower()
    words = set(re.findall(r"\b[a-z]+\b", prompt))

    status_phrases = (
        "http status",
        "check url",
        "check the url",
        "url status",
        "website status",
        "website availability",
        "is the website up",
        "is the site up",
        "is the service up",
        "is the service available",
        "is this service available",
        "is sauce demo available",
        "is the website available",
        "is the site available",
        "can you reach",
        "check reachability",
    )

    title_phrases = (
        "page title",
        "website title",
        "application title",
        "title of the page",
        "title of this page",
        "title of the website",
        "title of the application",
        "title of sauce demo",
        "title of the sauce demo application",
    )

    if any(phrase in prompt for phrase in status_phrases) or (
        words.intersection({"status", "reachable", "reachability"})
    ):
        return {"intent": "status"}

    if any(phrase in prompt for phrase in title_phrases) or (
        "title" in words
        and words.intersection({"page", "website", "application", "sauce"})
    ):
        return {"intent": "page_title"}

    return {"intent": "general"}


def _single_tool_call(state: QAState) -> dict[str, Any]:
    """Validate the latest model response before routing."""
    messages = state.get("messages", [])

    if not messages or not isinstance(messages[-1], AIMessage):
        return {"route": "finish"}

    calls = messages[-1].tool_calls

    if len(calls) > 1:
        raise ValueError("Only one tool call per model response is supported.")

    if not calls:
        return {"route": "finish"}

    return {"route": calls[0]["name"]}


def _capture_tool_result(state: QAState) -> dict[str, str]:
    """Capture the latest tool output for callers and diagnostics."""
    for message in reversed(state.get("messages", [])):
        if isinstance(message, ToolMessage):
            return {
                "tool_name": message.name or "",
                "tool_result": str(message.content),
            }

    return {}


def _increment_tool_round(state: QAState) -> dict[str, int]:
    """Count tool rounds and stop excessive tool loops."""
    rounds = state.get("tool_rounds", 0) + 1

    if rounds > MAX_TOOL_ROUNDS:
        raise RuntimeError(
            f"Tool loop exceeded the limit of {MAX_TOOL_ROUNDS} rounds."
        )

    return {"tool_rounds": rounds}


def _execute_playwright_tool(state: QAState) -> dict[str, Any]:
    """Execute the title tool using the caller-owned Playwright page."""
    messages = state.get("messages", [])

    if not messages or not isinstance(messages[-1], AIMessage):
        raise ValueError("No model tool call is available.")

    calls = messages[-1].tool_calls

    if len(calls) != 1 or calls[0]["name"] != "get_page_title":
        raise ValueError("Expected exactly one get_page_title tool call.")

    call = calls[0]
    page = state.get("page")

    if page is None:
        raise ValueError(
            "Pass the existing Playwright page in workflow state."
        )

    result = get_page_title.func(page=page)

    return {
        "messages": [
            ToolMessage(
                content=str(result),
                tool_call_id=call["id"],
                name=call["name"],
            )
        ],
        "tool_name": call["name"],
        "tool_result": str(result),
    }


def build_qa_workflow(
    model_router: ModelRouter | None = None,
    tools: Sequence[BaseTool] = QA_TOOLS,
):
    """Build the workflow with injectable model and tools for testing."""
    router = model_router or ModelRouter(MODEL_PROVIDER)
    tool_list = list(tools)

    # Keep separate model bindings for general questions and tool requests.
    model_without_tools = router.bind_tools([])
    model_with_tools = router.bind_tools(tool_list)

    browser_tool_names = {"get_page_title"}
    general_tools = [
        tool for tool in tool_list if tool.name not in browser_tool_names
    ]
    tool_node = ToolNode(general_tools)

    def request_model(state: QAState) -> dict[str, Any]:
        """Invoke the appropriate model binding while preserving history."""
        is_initial_turn = not state.get("messages")

        if is_initial_turn:
            human_message = HumanMessage(content=state["user_prompt"])
            existing_messages = [human_message]
        else:
            existing_messages = state["messages"]

        messages = [
            SystemMessage(content=SYSTEM_INSTRUCTIONS),
            *existing_messages,
        ]

        if state.get("intent", "general") == "general":
            response = model_without_tools.invoke(messages)
        else:
            response = model_with_tools.invoke(messages)

        messages_update = (
            [human_message, response]
            if is_initial_turn
            else [response]
        )

        updates: dict[str, Any] = {"messages": messages_update}

        if response.tool_calls:
            if len(response.tool_calls) != 1:
                raise ValueError(
                    "Only one tool call per model response is supported."
                )

            updates["decision"] = "TOOL"
            updates["tool_name"] = response.tool_calls[0]["name"]
        else:
            updates["decision"] = (
                "TOOL" if state.get("tool_name") else "GENERAL"
            )
            updates["final_response"] = str(response.content)

        return updates

    def route_tool(state: QAState) -> str:
        route = _single_tool_call(state).get("route", "finish")

        if route == "get_page_title":
            return "playwright"

        if route in {tool.name for tool in general_tools}:
            return "tools"

        if route == "finish":
            return "finish"

        raise ValueError(f"Unsupported tool call: {route}")

    workflow = StateGraph(QAState)

    workflow.add_node("classify_request", classify_request)
    workflow.add_node("request_model", request_model)
    workflow.add_node("increment_tool_round", _increment_tool_round)
    workflow.add_node("playwright_tool", _execute_playwright_tool)
    workflow.add_node("tools", tool_node)
    workflow.add_node("capture_tool_result", _capture_tool_result)

    workflow.add_edge(START, "classify_request")
    workflow.add_edge("classify_request", "request_model")

    workflow.add_conditional_edges(
        "request_model",
        route_tool,
        {
            "playwright": "increment_tool_round",
            "tools": "increment_tool_round",
            "finish": END,
        },
    )

    workflow.add_conditional_edges(
        "increment_tool_round",
        route_tool,
        {
            "playwright": "playwright_tool",
            "tools": "tools",
            "finish": END,
        },
    )

    workflow.add_edge("playwright_tool", "request_model")
    workflow.add_edge("tools", "capture_tool_result")
    workflow.add_edge("capture_tool_result", "request_model")

    return workflow.compile()


qa_workflow = build_qa_workflow()
