from ai_lab.phase_01_llm.cloud_api import generate_response_cloud


def test_generate_response_cloud():
    prompt = "What is Playwright? Explain it in three sentences."

    response = generate_response_cloud(prompt)

    assert response
    assert "Playwright" in response

    print("\nGemini Response:")
    print(response)