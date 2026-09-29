from ai_lab.phase_01_llm.models.model_router import ModelRouter


def test_ollama_model_router():
    router = ModelRouter("ollama")

    response = router.generate(
        "What is Playwright? Answer in one sentence."
    )

    assert response
    assert "Playwright" in response


def test_gemini_model_router():
    router = ModelRouter("gemini")

    response = router.generate(
        "What is Playwright? Answer in one sentence."
    )

    assert response
    assert "Playwright" in response