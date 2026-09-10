from ai_lab.phase_01_llm.local_ollama import generate_response


def test_generate_response():
    prompt = "What is Playwright? Explain it in three sentences."

    response = generate_response(prompt)

    assert response

    print("\nLLM Response:")
    print(response)