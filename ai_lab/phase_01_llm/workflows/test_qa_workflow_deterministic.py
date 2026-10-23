from langchain_core.messages import AIMessage
import pytest
from langchain_core.tools import tool

from ai_lab.phase_01_llm.tools import get_page_title
from ai_lab.phase_01_llm.workflows.qa_workflow import build_qa_workflow


@tool
def fake_status(url: str) -> str:
    """Return a mocked HTTP status for a URL."""
    return "HTTP 200"


class FakePage:
    def goto(self, url):
        self.url = url

    def title(self):
        return "Mock Sauce Demo"


class FakeRouter:
    def bind_tools(self, tools):
        class BoundModel:
            def invoke(self, messages):
                human = next(message for message in messages if message.type == "human")
                prompt = str(human.content).lower()
                tool_results = [message for message in messages if message.type == "tool"]
                if tool_results:
                    return AIMessage(content=f"Verified result: {tool_results[-1].content}")
                if "status" in prompt or "available" in prompt:
                    return AIMessage(content="", tool_calls=[{
                        "name": "fake_status",
                        "args": {"url": "https://example.test"},
                        "id": "call-status",
                        "type": "tool_call",
                    }])
                if "title" in prompt:
                    return AIMessage(content="", tool_calls=[{
                        "name": "get_page_title",
                        "args": {},
                        "id": "call-title",
                        "type": "tool_call",
                    }])
                return AIMessage(content="A deterministic general answer.")
        return BoundModel()


def _workflow():
    return build_qa_workflow(model_router=FakeRouter(), tools=[fake_status, get_page_title])


def test_general_request_uses_model_without_tools():
    result = _workflow().invoke({"user_prompt": "Explain a QA test plan."})
    assert result["decision"] == "GENERAL"
    assert result["final_response"] == "A deterministic general answer."
    assert result.get("tool_rounds", 0) == 0


def test_status_request_executes_mock_tool_and_returns_model_answer():
    result = _workflow().invoke({"user_prompt": "Is this service available?"})
    assert result["decision"] == "TOOL"
    assert result["tool_name"] == "fake_status"
    assert result["tool_result"] == "HTTP 200"
    assert result["final_response"] == "Verified result: HTTP 200"
    assert result["tool_rounds"] == 1


def test_page_tool_uses_passed_page_without_creating_browser():
    result = _workflow().invoke({"user_prompt": "What is the page title?", "page": FakePage()})
    assert result["tool_name"] == "get_page_title"
    assert result["tool_result"] == "Mock Sauce Demo"
    assert result["final_response"] == "Verified result: Mock Sauce Demo"



class LoopingRouter:
    def bind_tools(self, tools):
        class BoundModel:
            def invoke(self, messages):
                return AIMessage(content="", tool_calls=[{
                    "name": "fake_status",
                    "args": {"url": "https://example.test"},
                    "id": f"call-{sum(message.type == 'tool' for message in messages)}",
                    "type": "tool_call",
                }])
        return BoundModel()


def test_tool_round_limit_stops_repeated_tool_requests():
    workflow = build_qa_workflow(model_router=LoopingRouter(), tools=[fake_status])
    with pytest.raises(RuntimeError, match="Tool loop exceeded the limit of 5 rounds"):
        workflow.invoke({"user_prompt": "Keep checking status"})


def test_page_tool_requires_the_existing_playwright_page():
    with pytest.raises(ValueError, match="Pass the existing Playwright page"):
        _workflow().invoke({"user_prompt": "What is the page title?"})

