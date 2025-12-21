import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


def search_web(
	query: str, max_results: int = 10, include_raw_content: bool = False
) -> Dict[str, Any]:
	"""Run a web search using a configured SearXNG instance."""
	from .clients.searxng_client import SearxngClient

	client = SearxngClient()
	try:
		return client.search(
			query=query, max_results=max_results, include_raw_content=include_raw_content
		)
	finally:
		client.close()


__all__ = [
	"search_web",
]

