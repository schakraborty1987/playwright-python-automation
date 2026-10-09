from ai_lab.phase_01_llm.workflows.qa_workflow import qa_workflow


def create_initial_state(user_prompt, page=None):
    return {
        "user_prompt": user_prompt,
        "decision": "",
        "final_response": "",
        "page": page,
        "tool_name": "",
        "tool_result": "",
    }


def test_qa_workflow_general_question():
    result = qa_workflow.invoke(
        create_initial_state("What is Playwright?")
    )

    assert result["decision"] == "GENERAL"
    assert result["final_response"]
    assert "Playwright" in result["final_response"]


def test_qa_workflow_executes_page_title_tool(page):
    result = qa_workflow.invoke(
        create_initial_state(
            "What is the title of the Sauce Demo application?",
            page=page,
        )
    )

    assert result["decision"] == "TOOL"
    assert result["tool_name"] == "get_page_title"
    assert result["tool_result"] == "Swag Labs"
    assert "Swag Labs" in result["final_response"]


def test_qa_workflow_executes_url_status_tool():
    result = qa_workflow.invoke(
        create_initial_state("Is Sauce Demo available?")
    )

    assert result["decision"] == "TOOL"
    assert result["tool_name"] == "check_url_status"
    assert result["tool_result"].startswith("HTTP ")
    assert result["final_response"]