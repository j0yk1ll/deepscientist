"""Unit tests for HTTP client implementations.

These tests verify the client classes work correctly with mocked HTTP responses.
"""

import pytest
from unittest.mock import patch, MagicMock


class MockHttpResponse:
    """Mock HTTP response for tests."""
    
    def __init__(self, status_code=200, text="", json_data=None):
        self.status_code = status_code
        self.text = text
        self._json = json_data or {}
    
    def raise_for_status(self):
        if self.status_code >= 400:
            raise Exception(f"HTTP {self.status_code}")
    
    def json(self):
        return self._json


class MockHttpClient:
    """Mock httpx client."""
    
    def __init__(self, responses=None):
        self.responses = responses or [MockHttpResponse()]
        self._idx = 0
        self.calls = []
    
    def get(self, url, params=None, **kwargs):
        self.calls.append(("GET", url, params))
        if self._idx < len(self.responses):
            resp = self.responses[self._idx]
            self._idx += 1
            return resp
        return self.responses[-1]
    
    def close(self):
        pass


class TestSearxngClient:
    """Tests for SearxngClient."""

    def test_init_requires_base_url(self, clean_env):
        """Should raise if no base URL configured."""
        from deepscientist.tools.clients.searxng_client import SearxngClient
        
        with pytest.raises(RuntimeError) as exc_info:
            SearxngClient()
        
        assert "SEARXNG_BASE_URL" in str(exc_info.value)

    def test_init_with_explicit_base_url(self):
        """Should work with explicit base URL."""
        from deepscientist.tools.clients.searxng_client import SearxngClient
        
        client = SearxngClient(base_url="http://localhost:8080")
        assert client.base_url == "http://localhost:8080"
        client.close()

    def test_search_returns_empty_for_empty_query(self):
        """Empty query should return empty results."""
        from deepscientist.tools.clients.searxng_client import SearxngClient
        
        client = SearxngClient(base_url="http://localhost:8080")
        results = client.search("")
        client.close()

        assert results == {"query": "", "results": []}

    def test_search_parses_response(self, sample_searxng_json):
        """Test correct parsing of SearXNG response."""
        from deepscientist.tools.clients.searxng_client import SearxngClient
        
        mock_http = MockHttpClient([MockHttpResponse(json_data=sample_searxng_json)])
        
        client = SearxngClient(base_url="http://localhost:8080")
        client.client = mock_http
        result = client.search("test")

        assert result["query"] == "test"
        assert len(result["results"]) == 1
        assert result["results"][0]["title"] == "Web Search Result"
        assert result["number_of_results"] == 100

    def test_search_respects_max_results(self):
        """Should trim results to max_results."""
        from deepscientist.tools.clients.searxng_client import SearxngClient
        
        many_results = {"results": [{"title": f"Result {i}"} for i in range(20)]}
        mock_http = MockHttpClient([MockHttpResponse(json_data=many_results)])
        
        client = SearxngClient(base_url="http://localhost:8080")
        client.client = mock_http
        result = client.search("test", max_results=5)

        assert len(result["results"]) == 5

    def test_search_includes_raw_content_when_requested(self, sample_searxng_json):
        """Raw content should be included when flag is True."""
        from deepscientist.tools.clients.searxng_client import SearxngClient
        
        mock_http = MockHttpClient([MockHttpResponse(json_data=sample_searxng_json)])
        
        client = SearxngClient(base_url="http://localhost:8080")
        client.client = mock_http
        result = client.search("test", include_raw_content=True)

        assert "raw" in result
        assert result["raw"] == sample_searxng_json


class TestCommonHttp:
    """Tests for common HTTP utilities."""

    def test_parse_year_from_iso_full_timestamp(self):
        """Parse year from full ISO timestamp."""
        from deepscientist.tools.clients.utils import parse_year_from_iso
        
        assert parse_year_from_iso("2024-01-15T12:30:00Z") == 2024
        assert parse_year_from_iso("2023-12-31T23:59:59+00:00") == 2023

    def test_parse_year_from_iso_date_only(self):
        """Parse year from date-only string."""
        from deepscientist.tools.clients.utils import parse_year_from_iso
        
        assert parse_year_from_iso("2024-01-15") == 2024
        assert parse_year_from_iso("2022-06-30") == 2022

    def test_parse_year_from_iso_year_only(self):
        """Parse year from year-only string."""
        from deepscientist.tools.clients.utils import parse_year_from_iso
        
        assert parse_year_from_iso("2024") == 2024

    def test_parse_year_from_iso_returns_none_for_invalid(self):
        """Invalid strings should return None."""
        from deepscientist.tools.clients.utils import parse_year_from_iso
        
        assert parse_year_from_iso(None) is None
        assert parse_year_from_iso("") is None
        assert parse_year_from_iso("invalid") is None

    def test_make_http_client_returns_client(self):
        """Should return an httpx.Client instance."""
        from deepscientist.tools.clients.utils import make_http_client
        import httpx
        
        client = make_http_client()
        try:
            assert isinstance(client, httpx.Client)
        finally:
            client.close()
