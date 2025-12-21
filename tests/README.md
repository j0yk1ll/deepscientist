# DeepScientist Test Suite

This directory contains the test suite for DeepScientist, organized into unit tests and integration tests.

## Structure

```
tests/
├── conftest.py              # Shared pytest fixtures and configuration
├── unit/                    # Unit tests (mocked dependencies)
│   ├── test_agents.py       # Tests for agent creation and configuration
│   ├── test_clients.py      # Tests for HTTP API clients
│   ├── test_orchestrator.py # Tests for orchestrator creation
│   ├── test_search_tools.py # Tests for search tool wrappers
└── integration/             # Integration tests (real services)
    ├── test_agents_integration.py       # Tests with real LLM
    └── test_search_integration.py       # Tests with real APIs
```

## Running Tests

### Unit Tests Only (default)

Unit tests mock all external dependencies and run quickly:

```bash
# Run all unit tests
uv run pytest

# Run with verbose output
uv run pytest -v

# Run with coverage
uv run pytest --cov=deepscientist --cov-report=term-missing

# Run specific test file
uv run pytest tests/unit/test_agents.py

# Run specific test class or function
uv run pytest tests/unit/test_agents.py::TestAgentCreation
uv run pytest tests/unit/test_agents.py::TestAgentCreation::test_create_analyst_subagent_with_defaults
```

### Integration Tests

Integration tests require real services and may be slow:

```bash
# Run integration tests only
uv run pytest -m integration

# Run all tests including integration
uv run pytest -m ""
```

### Required Environment Variables for Integration Tests

#### For LLM tests:
- `LM_API_KEY` or `OPENAI_API_KEY`: API key for OpenAI-compatible endpoint
- `LM_BASE_URL` (optional): Base URL for OpenAI-compatible endpoint
- `LM_MODEL` (optional): Model name (default: gpt-4.1-mini)

#### For Web Search tests:
- `SEARXNG_BASE_URL`: URL of SearXNG instance (required for web search)

## Test Markers

- `@pytest.mark.unit` - Unit tests with mocked dependencies (fast)
- `@pytest.mark.integration` - Integration tests requiring real services (slow)
- `@pytest.mark.slow` - Particularly slow tests (e.g., LLM inference)

## Writing Tests

### Unit Tests

Unit tests should:
1. Mock all external dependencies (LLMs, databases, HTTP clients)
2. Use fixtures from `conftest.py` for common mocks
3. Test one specific behavior per test function
4. Run quickly (< 1 second per test)

Example:
```python
def test_search_returns_results(self):
    from deepscientist.tools.clients.searxng_client import SearxngClient
    
    # Create mock HTTP client
    mock_http = MockHttpClient([MockHttpResponse(text=sample_xml)])
    
    client = SearxngClient()
    client.client = mock_http  # Replace real client with mock
    results = client.search("test")

    assert len(results) > 0
```

### Integration Tests

Integration tests should:
1. Check for service availability with `pytest.mark.skipif`
2. Clean up any created resources
3. Use isolation (unique test data identifiers)

Example:
```python
@pytest.mark.skipif(not searxng_available(), reason="SearxNG not available")
def test_search_returns_results(self, query):
    result = client.search(query)
    assert result is not None
```

## Coverage

To generate a coverage report:

```bash
# Terminal report
uv run pytest --cov=deepscientist --cov-report=term-missing

# HTML report
uv run pytest --cov=deepscientist --cov-report=html
# Then open htmlcov/index.html in browser
```
