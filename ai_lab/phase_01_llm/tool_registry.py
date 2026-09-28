from ai_lab.phase_01_llm.tools import check_url_status, get_page_title


TOOL_REGISTRY = {
    "check_url_status": {
        "function": check_url_status,
        "description": "Check whether a URL is reachable and return its HTTP status.",
        "requires_page": False,
        "parameters": {
            "url": {
                "type": "string",
                "description": "The URL to check.",
            }
        },
    },
    "get_page_title": {
        "function": get_page_title,
        "description": "Open Sauce Demo using the existing Playwright page and return its page title.",
        "requires_page": True,
        "parameters": {},
    },
}