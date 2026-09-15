from ai_lab.phase_01_llm.local_ollama import generate_response_local
from ai_lab.phase_01_llm.tools import get_sauce_demo_status


def test_generate_response_local():
    prompt = "What is Playwright? Explain it in three sentences."

    response = generate_response_local(prompt)

    assert response
    assert "Playwright" in response

    print("\nLLM Response:")
    print(response)

def test_sauce_demo_status_tool():
    result = get_sauce_demo_status()

    assert result == "Sauce Demo is available."

    print("\nTool Result:")
    print(result)