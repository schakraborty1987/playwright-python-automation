from ai_lab.phase_01_llm.workflows.qa_workflow import qa_workflow


def test_qa_workflow():
    initial_state = {
        "user_prompt": "What is Playwright?",
        "decision": "",
        "final_response": "",
    }

    result = qa_workflow.invoke(initial_state) #This 'invoke' method is used to start the workflow with the initial state. It will process the state through the defined steps of the workflow, which includes analyzing the request and generating a response based on the user's prompt.

    print("\nFinal Workflow State:")
    print(result)

    assert result["decision"]
    assert result["final_response"]
    assert "Playwright" in result["final_response"]