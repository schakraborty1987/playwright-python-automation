from ai_lab.phase_01_llm.agent import run_agent


def test_agent_uses_sauce_demo_tool():
    response = run_agent(
        "Is the Sauce Demo application available?"
    )

    assert response

    print("\nAgent Response:")
    print(response)