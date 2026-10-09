from typing import Any, TypedDict

from langgraph.graph import StateGraph, START, END

from ai_lab.phase_01_llm.models.model_router import ModelRouter
from ai_lab.phase_01_llm.tool_registry import TOOL_REGISTRY
from pages.SauceDemoPage import SauceDemoPage


class QAState(TypedDict):
    user_prompt: str
    decision: str
    final_response: str
    page: Any
    tool_name: str
    tool_result: str


model_router = ModelRouter("ollama")
  

def analyze_request(state: QAState) -> QAState:
    """Deterministically classify the request."""

    print("\n--- ENTERING analyze_request ---")
    print("State received:")
    print(state)

    user_prompt = state["user_prompt"].lower()

    tool_keywords = [
        "page title",
        "title of",
        "is sauce demo available",
        "is sauce demo reachable",
        "http status",
        "status of",
        "check url",
        "check website",
    ]

    decision = (
        "TOOL"
        if any(keyword in user_prompt for keyword in tool_keywords)
        else "GENERAL"
    )

    updated_state = {
        **state,
        "decision": decision,
    }

    print("State after analyze_request:")
    print(updated_state)

    return updated_state


def route_request(state: QAState) -> str:
    """Select the appropriate workflow branch."""

    print("\n--- ROUTING REQUEST ---")
    print(f"Decision: {state['decision']}")

    return "tool" if state["decision"] == "TOOL" else "general"


def select_tool(state: QAState) -> QAState:
    """Select a registered tool using deterministic rules."""

    print("\n--- ENTERING select_tool ---")

    user_prompt = state["user_prompt"].lower()

    if "title" in user_prompt:
        tool_name = "get_page_title"
    elif any(
        keyword in user_prompt
        for keyword in [
            "available",
            "reachable",
            "http status",
            "status of",
            "check url",
            "check website",
        ]
    ):
        tool_name = "check_url_status"
    else:
        raise ValueError(
            f"No registered tool matches this request: "
            f"{state['user_prompt']}"
        )

    if tool_name not in TOOL_REGISTRY:
        raise ValueError(f"Tool is not registered: {tool_name}")

    updated_state = {
        **state,
        "tool_name": tool_name,
    }

    print(f"Selected tool: {tool_name}")

    return updated_state


def execute_tool(state: QAState) -> QAState:
    """Execute the selected function from TOOL_REGISTRY."""

    print("\n--- ENTERING execute_tool ---")

    tool_name = state["tool_name"]
    tool_definition = TOOL_REGISTRY[tool_name]
    tool_function = tool_definition["function"]

    if tool_definition["requires_page"]:
        page = state.get("page")

        if page is None:
            raise ValueError(
                f"Tool '{tool_name}' requires a Playwright page. "
                "Pass the existing page fixture to the workflow."
            )

        result = tool_function(page)

    else:
        # Sauce Demo availability requests use the existing application URL.
        url = SauceDemoPage.BASE_URL
        result = tool_function(url=url)

    updated_state = {
        **state,
        "tool_result": str(result),
        "final_response": (
            f"Tool executed: {tool_name}\n"
            f"Result: {result}"
        ),
    }

    print("State after execute_tool:")
    print(updated_state)

    return updated_state


def handle_general_request(state: QAState) -> QAState:
    """Answer a general question without executing a tool."""

    print("\n--- ENTERING handle_general_request ---")

    response = model_router.generate(state["user_prompt"])

    updated_state = {
        **state,
        "final_response": response,
    }

    print("State after handle_general_request:")
    print(updated_state)

    return updated_state


def build_qa_workflow():
    """Build and compile the LangGraph workflow."""

    workflow = StateGraph(QAState)

    workflow.add_node("analyze_request", analyze_request)
    workflow.add_node("select_tool", select_tool)
    workflow.add_node("execute_tool", execute_tool)
    workflow.add_node("handle_general_request", handle_general_request)

    workflow.add_edge(START, "analyze_request")

    workflow.add_conditional_edges(
        "analyze_request",
        route_request,
        {
            "general": "handle_general_request",
            "tool": "select_tool",
        },
    )

    workflow.add_edge("select_tool", "execute_tool")
    workflow.add_edge("execute_tool", END)
    workflow.add_edge("handle_general_request", END)

    return workflow.compile()


qa_workflow = build_qa_workflow()