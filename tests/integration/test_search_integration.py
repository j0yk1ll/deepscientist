"""Integration tests for HTTP API clients.

These tests make real HTTP requests to external APIs.
Run with: pytest -m integration

Note: These tests require network access and may be rate-limited.
"""

import pytest


pytestmark = pytest.mark.integration


class TestSearchToolsIntegration:
    """Integration tests for search tool wrapper functions."""

    def test_search_web(self):
        """search_web should aggregate results."""
        from deepscientist.tools.search import search_web
        
        # Only test sources that don't require configuration
        results = search_web(
            "neural networks",
            max_results=3,
        )
        
        assert "results" in results
        assert len(results["results"]) > 0
