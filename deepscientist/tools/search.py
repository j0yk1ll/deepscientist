from __future__ import annotations

import logging
from typing import Any, Dict

from langchain.tools import ToolRuntime
from langchain_core.tools import StructuredTool

logger = logging.getLogger(__name__)


_SEARCH_WEB_DESC = """Run a web search using a configured SearXNG instance.

Args:
- query: search query string
- max_results: maximum number of results to return (default: 10)
- include_raw_content: include raw page content if supported (default: false)

Returns:
- A dictionary containing search results as returned by the SearXNG client.
"""


def _search_web(runtime: ToolRuntime, query: str, max_results: int = 10, include_raw_content: bool = False) -> Dict[str, Any]:
    # Settings retrieved for consistency / future configurability; currently SearxngClient is self-configured.

    from .clients.searxng_client import SearxngClient

    client = SearxngClient()
    try:
        return client.search(query=query, max_results=max_results, include_raw_content=include_raw_content)
    finally:
        client.close()


search_web = StructuredTool.from_function(
    name="search_web",
    description=_SEARCH_WEB_DESC,
    func=_search_web,
)

__all__ = [
    "search_web",
]
