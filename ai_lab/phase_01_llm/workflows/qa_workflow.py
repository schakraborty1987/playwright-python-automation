from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from ai_lab.phase_01_llm.models.model_router import ModelRouter
from pprint import pprint

class QAState(TypedDict):
    user_prompt: str
    decision: str
    final_response: str

model_router = ModelRouter("ollama")

def analyze_request(state: QAState) -> QAState:
    """
    Analyze the user's request and store the LLM decision in state.
    """

    print("\n--- ENTERING analyze_request ---")
    print("State received:")
    pprint(state)

    prompt = f"""
You are a QA assistant.

Analyze the following user request and decide what should happen.

User request:
{state["user_prompt"]}

Return a short description of the action required.
"""

    decision = model_router.generate(prompt)

    updated_state = {
        **state,
        "decision": decision,
    }

    print("State after analyze_request:")
    pprint(updated_state)

    return updated_state

def generate_response(state: QAState) -> QAState:
    """
    Generate the final response using the information stored in state.
    """

    print("\n--- ENTERING generate_response ---")
    print("State received:")
    pprint(state)

    prompt = f"""
You are a QA assistant.

User request:
{state["user_prompt"]}

Analysis:
{state["decision"]}

Provide a concise and useful response.
"""

    response = model_router.generate(prompt)

    updated_state = {
        **state,
        "final_response": response,
    }

    print("State after generate_response:")
    pprint(updated_state)

    return updated_state

def build_qa_workflow():
    """
    Build and compile the LangGraph QA workflow.
    """

    workflow = StateGraph(QAState)

    workflow.add_node("analyze_request", analyze_request)
    workflow.add_node("generate_response", generate_response)

    workflow.add_edge(START, "analyze_request")
    workflow.add_edge("analyze_request", "generate_response")
    workflow.add_edge("generate_response", END)

    return workflow.compile()

qa_workflow = build_qa_workflow()