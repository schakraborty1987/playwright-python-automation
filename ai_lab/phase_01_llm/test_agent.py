from ai_lab.phase_01_llm.agent import run_agent


def test_agent_uses_sauce_demo_status_tool():
    user_prompt = "Is Sauce Demo available?"

    response = run_agent(user_prompt)

    assert response
    assert "Sauce Demo" in response


def test_agent_uses_sauce_demo_title_tool(page):
    user_prompt = "What is the title of the Sauce Demo application?"

    response = run_agent(user_prompt, page)

    assert response
    assert "Swag Labs" in response


def test_agent_answers_without_tool():
    user_prompt = "What is Playwright?"

    response = run_agent(user_prompt)

    assert response
    assert "Playwright" in response