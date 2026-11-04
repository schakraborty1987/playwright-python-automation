
from typing import Any, TypedDict

from langgraph.graph import END, START, StateGraph

from ai_lab.phase_01_llm.workflows.qa_workflow import qa_workflow


class SupervisorState(TypedDict, total=False):
    user_prompt: str
    page: Any
    selected_workflow: str
    final_response: str


def delegate_to_qa_workflow(state: SupervisorState) -> dict[str, str]:
    """Delegate the request to the existing QA workflow."""

    result = qa_workflow.invoke(
        {
            "user_prompt": state["user_prompt"],
            "page": state.get("page"),
        }
    )

    return {
        "selected_workflow": "qa_workflow",
        "final_response": result.get(
            "final_response",
            "No response was generated.",
        ),
    }


def build_supervisor_workflow():
    """Build and compile the Supervisor workflow."""

    workflow = StateGraph(SupervisorState)

    workflow.add_node("delegate_to_qa", delegate_to_qa_workflow)

    workflow.add_edge(START, "delegate_to_qa")
    workflow.add_edge("delegate_to_qa", END)

    return workflow.compile()


supervisor_workflow = build_supervisor_workflow()
