"""Pytest configuration and shared fixtures for DeepScientist tests.

This module provides:
- Common test fixtures for mocking external dependencies
- Configuration for test markers (unit vs integration)
- Shared mock implementations for LLMs, databases, and HTTP clients
"""

import os
import pytest
from unittest.mock import MagicMock, patch
from typing import Any, Dict, List, Optional


# --------------------------------------------------------------------------
# Pytest configuration
# --------------------------------------------------------------------------

def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test (fast, mocked dependencies)"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test (requires real services)"
    )


def pytest_collection_modifyitems(config, items):
    """Auto-mark tests based on their location."""
    for item in items:
        # Auto-mark based on path
        if "unit" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        elif "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)


# --------------------------------------------------------------------------
# Environment fixtures
# --------------------------------------------------------------------------

@pytest.fixture
def clean_env(monkeypatch):
    """Provide a clean environment without external service configuration."""
    env_vars = [
        "NEO4J_URI", "NEO4J_USER", "NEO4J_PASSWORD", "NEO4J_DATABASE",
        "OPENAI_API_KEY", "LM_API_KEY", "LM_MODEL", "LM_BASE_URL",
        "SEARXNG_BASE_URL", "VECTOR_DIR", "VECTOR_COLLECTION",
    ]
    for var in env_vars:
        monkeypatch.delenv(var, raising=False)
    return monkeypatch


# --------------------------------------------------------------------------
# Mock LLM fixtures
# --------------------------------------------------------------------------

class MockLLM:
    """Mock LLM that returns configurable responses."""
    
    def __init__(self, responses: Optional[List[str]] = None):
        self.responses = responses or ["Mock LLM response"]
        self._call_index = 0
        self.model_name = "mock-model"
        self.calls: List[Any] = []
    
    def invoke(self, messages, **kwargs):
        """Simulate LLM invocation."""
        self.calls.append((messages, kwargs))
        response = MagicMock()
        if self._call_index < len(self.responses):
            response.content = self.responses[self._call_index]
            self._call_index += 1
        else:
            response.content = self.responses[-1]
        return response
    
    def bind_tools(self, tools, **kwargs):
        """Return self for tool binding (no-op for mock)."""
        return self


@pytest.fixture
def mock_llm():
    """Provide a mock LLM instance."""
    return MockLLM()


@pytest.fixture
def mock_init_chat_model(mock_llm):
    """Patch init_chat_model to return a mock LLM."""
    with patch("langchain.chat_models.init_chat_model") as mock_init:
        mock_init.return_value = mock_llm
        yield mock_init


# --------------------------------------------------------------------------
# Mock HTTP client fixtures
# --------------------------------------------------------------------------

class MockHttpResponse:
    """Mock HTTP response object."""
    
    def __init__(
        self,
        status_code: int = 200,
        text: str = "",
        json_data: Optional[Dict] = None,
    ):
        self.status_code = status_code
        self.text = text
        self._json_data = json_data or {}
    
    def raise_for_status(self):
        if self.status_code >= 400:
            raise Exception(f"HTTP {self.status_code}")
    
    def json(self):
        return self._json_data


class MockHttpClient:
    """Mock HTTP client for testing API clients."""
    
    def __init__(self, responses: Optional[List[MockHttpResponse]] = None):
        self.responses = responses or [MockHttpResponse()]
        self._call_index = 0
        self.calls: List[tuple] = []
    
    def get(self, url: str, params: Optional[Dict] = None, **kwargs):
        self.calls.append(("GET", url, params, kwargs))
        if self._call_index < len(self.responses):
            response = self.responses[self._call_index]
            self._call_index += 1
            return response
        return self.responses[-1]
    
    def post(self, url: str, **kwargs):
        self.calls.append(("POST", url, kwargs))
        if self._call_index < len(self.responses):
            response = self.responses[self._call_index]
            self._call_index += 1
            return response
        return self.responses[-1]
    
    def close(self):
        pass


@pytest.fixture
def mock_http_client():
    """Provide a mock HTTP client."""
    return MockHttpClient()


@pytest.fixture
def mock_make_http_client(mock_http_client):
    """Patch make_http_client to return a mock client."""
    with patch(
        "deepscientist.tools.clients.common_http.make_http_client"
    ) as mock_factory:
        mock_factory.return_value = mock_http_client
        yield mock_factory


@pytest.fixture
def sample_searxng_json():
    """Sample SearXNG API JSON response."""
    return {
        "results": [
            {
                "title": "Web Search Result",
                "url": "https://example.com/result",
                "content": "This is the snippet.",
                "engine": "google",
            },
        ],
        "number_of_results": 100,
    }
