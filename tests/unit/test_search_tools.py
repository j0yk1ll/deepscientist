"""Unit tests for search tool functions.

These tests verify the search tool wrappers work correctly with mocked clients.
"""

import pytest
from unittest.mock import patch, MagicMock
import importlib


# Need to import and reload the module to properly patch the lazy imports
@pytest.fixture(autouse=True)
def reload_search_module():
    """Ensure fresh import of search module for each test."""
    import deepscientist.tools.search as search_module
    yield search_module
    # Reload after test to reset any patches
    importlib.reload(search_module)


class TestSearchWeb:
    """Tests for search_web function."""

    def test_search_web_calls_client(self, reload_search_module):
        """Should create client and call search."""
        mock_client_instance = MagicMock()
        mock_client_instance.search.return_value = {"results": []}
        mock_client_class = MagicMock(return_value=mock_client_instance)

        with patch(
            "deepscientist.tools.clients.searxng_client.SearxngClient",
            mock_client_class,
        ):
            results = reload_search_module.search_web("python tutorial")

        mock_client_instance.search.assert_called_once_with(
            query="python tutorial", 
            max_results=10, 
            include_raw_content=False
        )

    def test_search_web_passes_include_raw_content(self, reload_search_module):
        """Should pass include_raw_content to client."""
        mock_client_instance = MagicMock()
        mock_client_instance.search.return_value = {"results": [], "raw": {}}
        mock_client_class = MagicMock(return_value=mock_client_instance)

        with patch(
            "deepscientist.tools.clients.searxng_client.SearxngClient",
            mock_client_class,
        ):
            reload_search_module.search_web("test", include_raw_content=True)

        mock_client_instance.search.assert_called_once_with(
            query="test",
            max_results=10,
            include_raw_content=True
        )