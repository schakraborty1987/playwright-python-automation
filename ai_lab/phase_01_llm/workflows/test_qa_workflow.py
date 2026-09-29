from ai_lab.phase_01_llm.workflows.qa_workflow import qa_workflow


def test_qa_workflow():
    initial_state = {
        "user_prompt": "What is Playwright?",
        "decision": "",
        "final_response": "",
    }

    result = qa_workflow.invoke(initial_state)

    print("\nFinal Workflow State:")
    print(result)

    assert result["decision"]
    assert result["final_response"]
    assert "Playwright" in result["final_response"]