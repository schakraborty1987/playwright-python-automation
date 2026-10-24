# Agentic QA Framework — Architecture and Learning Roadmap

## 1. Project Objective

This project is an experimental learning environment for building an AI-powered QA automation system using Python, LLMs, LangGraph, and Playwright.

The objective is to progressively learn and implement Generative AI and Agentic AI concepts through a practical SauceDemo application, while maintaining a single, modular architecture.

The project prioritizes hands-on implementation, deterministic testing, reusable components, and incremental evolution rather than building multiple competing implementations.

## 2. Current Architecture

The current implementation uses one canonical design:

**ModelRouter → Model Provider → LangGraph QA Workflow → Shared Tools**

### 2.1 Model Abstraction

Location: `models/`

- `base_model.py` — Defines the shared model abstraction.
- `model_router.py` — Selects and exposes the configured model provider.
- `ollama_model.py` — Implements the local Ollama provider.
- `gemini_model.py` — Implements the Gemini provider.

The active provider and model settings are configured in `api_framework/config.py`.

Supported providers:
- Ollama — Local model execution.
- Gemini — Cloud-based model execution.

The active provider is selected through configuration. Cloud usage must respect applicable data-security and privacy requirements.

### 2.2 LangGraph Workflow

Location: `workflows/qa_workflow.py`

The current QA workflow supports:
- General questions answered by the configured LLM.
- URL availability and HTTP status checks.
- SauceDemo page-title inspection using Playwright.
- Conditional workflow routing.
- Conversation message history.
- Sequential tool execution and tool-result handling.
- Tool-round limits to prevent uncontrolled loops.

The Playwright tool uses the existing caller-provided page. The workflow does not create a separate browser for that tool.

### 2.3 Shared Tools

Location: `tools.py`

Current tools:
- `check_url_status` — Checks URL reachability and returns the HTTP status.
- `get_page_title` — Navigates the provided Playwright page to SauceDemo and returns its title.

The tools are exposed through LangChain's tool abstraction and integrated into the LangGraph workflow.

### 2.4 Testing Strategy

Current tests are organized into three areas:

- `workflows/test_qa_workflow.py` — Integration tests using the configured model and real tool integrations.
- `workflows/test_qa_workflow_deterministic.py` — Deterministic tests using fake models and mocked tools to verify workflow behavior.
- `models/test_model_router.py` — Tests for the Ollama and Gemini model-router implementations.

The shared API client also has tests under `api_framework/`.

Deterministic tests should be used to validate workflow logic without depending on live LLM decisions. Integration tests validate actual model and tool interactions.

## 3. Current Technology Stack

| Technology | Purpose |
|---|---|
| Python | Primary implementation language |
| Ollama | Local LLM execution |
| Gemini | Alternative cloud LLM provider |
| LangChain Core | Tool abstractions and model/tool integration |
| LangGraph | Workflow state, nodes, edges, and orchestration |
| Playwright Python | Browser automation |
| pytest | Unit, deterministic, and integration testing |
| Requests / shared API client | HTTP requests and URL-status checks |

Additional technologies will be introduced when they solve a specific learning or implementation need.

## 4. Architecture Principles

1. Maintain one canonical agentic framework design.
2. Use model abstraction instead of coupling the workflow to a particular provider.
3. Keep reusable tools separate from workflow orchestration.
4. Prefer deterministic workflow logic for predictable operations.
5. Use LLM reasoning where flexible interpretation or decision-making is beneficial.
6. Keep browser lifecycle and Playwright page ownership explicit.
7. Retain both deterministic and integration tests.
8. Introduce new components incrementally and remove obsolete implementations only after checking dependencies.
9. Distinguish implemented capabilities from planned capabilities.

## 5. Target Learning Architecture

The long-term learning project will explore five logical QA roles. These roles are a target design, not five currently implemented agents.

### 5.1 QA Supervisor

Coordinates the request, delegates tasks, manages workflow execution, and consolidates results.

Concepts:
- Supervisor orchestration
- Conditional routing
- Agent delegation and handoffs
- Shared state and subgraphs
- Checkpointing and recovery
- Human-in-the-loop controls

### 5.2 Requirements and Test Design

Interprets fictional requirements and prepares test scenarios, test cases, and structured test data.

Concepts:
- Structured model output
- Prompt design
- Embeddings and vector search
- Retrieval-Augmented Generation (RAG)
- Graph-based knowledge retrieval

### 5.3 Test Automation

Selects or generates tests and executes approved automation actions.

Concepts:
- Tool calling
- Tool registries
- MCP integrations
- Playwright automation
- Model/provider abstraction
- Controlled execution

### 5.4 Test Analysis and Repair

Analyzes failures, evaluates evidence, identifies likely root causes, and proposes or validates repairs.

Concepts:
- Reflection and bounded retry loops
- Failure classification
- Evaluation
- Guardrails
- Observability
- Controlled self-healing

### 5.5 QA Review and Reporting

Validates results and produces a consolidated report with relevant evidence.

Concepts:
- Independent result review
- Structured validation
- Reporting integrations
- Evaluation metrics
- Multi-agent coordination

These roles may initially be implemented as ordinary graph nodes or subgraphs. They should become independent agents only when separate reasoning, tool access, or delegation justifies the additional complexity.

## 6. Learning and Implementation Roadmap

### Phase 1 — Stabilize the Foundation

Status: Current foundation implemented.

- Model abstraction and provider routing.
- Shared tools.
- LangGraph workflow and state management.
- Playwright page integration.
- Deterministic workflow tests.
- Model-router and integration tests.
- Removal of superseded legacy model and agent implementations.

### Phase 2 — Strengthen Orchestration

- Clarify workflow responsibilities and routing boundaries.
- Introduce the supervisor role incrementally.
- Learn delegation, subgraphs, and handoffs.
- Add checkpointing, recovery, and human approval where appropriate.
- Preserve the existing working workflow while extending it.

### Phase 3 — Requirements and Test Knowledge

- Introduce structured test-case generation.
- Explore embeddings and vector databases.
- Implement RAG using suitable sample requirements and test artifacts.
- Evaluate retrieval quality and grounded responses.

### Phase 4 — Analysis, Repair, and Reporting

- Add failure analysis and evidence collection.
- Introduce bounded retries and repair proposals.
- Add independent result review and consolidated reporting.
- Evaluate outcomes with deterministic checks wherever possible.

### Phase 5 — Graphify and Knowledge Graphs

Graphify should first be used as a codebase-understanding and dependency-mapping aid when reviewing repository structure and dependencies.

Later, investigate relationships between requirements, test cases, application components, and defects. Explore graph-based retrieval or GraphRAG only when those relationships provide value beyond ordinary vector retrieval.

**Important distinction:** a codebase dependency graph produced by a tool such as Graphify is not automatically a domain knowledge graph or a GraphRAG implementation.

### Phase 6 — Advanced Integrations and Evaluation

- Explore MCP for standardized access to external tools.
- Learn agent-to-agent communication concepts when cross-agent communication is needed.
- Evaluate persistent state and suitable infrastructure such as Redis where justified.
- Add tracing, evaluation datasets, and regression checks.
- Compare local and cloud model behavior, including tool selection, reliability, latency, and cost.

## 7. Definition of Progress

A phase is complete when:
- The capability has a clear purpose and documented implementation.
- Relevant deterministic tests pass.
- Required integration tests pass or documented environment limitations are understood.
- Existing functionality remains intact.
- The learning outcome is understood well enough to explain and extend it.

## 8. Working Agreement

The project will evolve through small, purposeful increments.

Avoid duplicate implementations, unnecessary abstractions, and prolonged cleanup exercises. Prefer learning through working code, targeted tests, and measurable progress.

This document should be updated as the architecture evolves. Planned capabilities must not be described as implemented until they actually exist and have been validated.