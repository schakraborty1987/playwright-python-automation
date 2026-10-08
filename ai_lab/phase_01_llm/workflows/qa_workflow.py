from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from ai_lab.phase_01_llm.models.model_router import ModelRouter


class QAState(TypedDict):
    user_prompt: str
    decision: str
    final_response: str


model_router = ModelRouter("ollama")


def analyze_request(state: QAState) -> QAState:
    """
    Deterministically classify the request as GENERAL or TOOL.

    For now, use simple rules.
    Later, this will be replaced/enhanced with structured LLM output.
    """

    print("\n--- ENTERING analyze_request ---")
    print("State received:")
    print(state)

    user_prompt = state["user_prompt"].lower()

    # Deterministic rules for our current tools. This is a python list of keywords that we will use to classify the request as TOOL or GENERAL.
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

    if any(keyword in user_prompt for keyword in tool_keywords):
        decision = "TOOL"
    else:
        decision = "GENERAL"

    updated_state = {
        **state,
        "decision": decision,
    }

    print("State after analyze_request:")
    print(updated_state)

    return updated_state


def route_request(state: QAState) -> str:
    """
    Decide which graph branch should execute next.
    """

    print("\n--- ROUTING REQUEST ---")
    print(f"Decision: {state['decision']}")

    if state["decision"] == "TOOL":
        return "tool"

    return "general"


def handle_general_request(state: QAState) -> QAState:
    """
    Handle a general question without using a tool.
    """

    print("\n--- ENTERING handle_general_request ---")

    response = model_router.generate(state["user_prompt"])

    updated_state = {
        **state,
        "final_response": response,
    }

    print("State after handle_general_request:")
    print(updated_state)

    return updated_state


def handle_tool_request(state: QAState) -> QAState:
    """
    Placeholder for future tool execution.

    The actual Tool Registry will be connected later.
    """

    print("\n--- ENTERING handle_tool_request ---")

    response = "Tool execution branch selected."

    updated_state = {
        **state,
        "final_response": response,
    }

    print("State after handle_tool_request:")
    print(updated_state)

    return updated_state


def build_qa_workflow():
    """
    Build and compile the LangGraph QA workflow.
    """

    workflow = StateGraph(QAState)

    workflow.add_node("analyze_request", analyze_request)
    workflow.add_node("handle_general_request", handle_general_request)
    workflow.add_node("handle_tool_request", handle_tool_request)

    workflow.add_edge(START, "analyze_request")

    workflow.add_conditional_edges(
        "analyze_request",
        route_request,
        {
            "general": "handle_general_request",
            "tool": "handle_tool_request",
        },
    )

    workflow.add_edge("handle_general_request", END)
    workflow.add_edge("handle_tool_request", END)

    return workflow.compile()


qa_workflow = build_qa_workflow()