from ai_lab.phase_01_llm.local_ollama import generate_response, generate_response_local


def test_generate_response():
    prompt = "What is Playwright? Explain it in three sentences."

    response = generate_response_local(prompt)

    assert response
    assert "Playwright" in response

    print("\nLLM Response:")
    print(response)