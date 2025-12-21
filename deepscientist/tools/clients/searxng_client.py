import logging
import os
from typing import Dict, Any, List, Optional

from .common_http import make_http_client

logger = logging.getLogger(__name__)

SEARXNG_BASE_URL = os.environ.get("SEARXNG_BASE_URL", "").rstrip("/")


class SearxngClient:
    """Thin wrapper for a SearXNG instance."""

    def __init__(self, base_url: Optional[str] = None) -> None:
        base = (base_url or SEARXNG_BASE_URL or "").rstrip("/")
        if not base:
            raise RuntimeError(
                "SEARXNG_BASE_URL is not configured. "
                "Set SEARXNG_BASE_URL env var or pass base_url explicitly."
            )
        self.base_url = base
        self.client = make_http_client()

    def close(self) -> None:
        self.client.close()

    def search(
        self,
        query: str,
        max_results: int = 10,
        include_raw_content: bool = False,
    ) -> Dict[str, Any]:
        if not query:
            return {"query": query, "results": []}

        params = {
            "q": query,
            "format": "json",
            "pageno": 1,
        }

        url = f"{self.base_url}/search"
        try:
            resp = self.client.get(url, params=params)
            resp.raise_for_status()
        except Exception as e:
            logger.error("SearXNG request failed: %s", e)
            return {"query": query, "results": [], "error": str(e)}

        try:
            data = resp.json()
        except ValueError as e:
            logger.error("SearXNG JSON parsing error: %s", e)
            return {"query": query, "results": [], "error": str(e)}

        raw_results = data.get("results", []) or []
        trimmed = raw_results[:max_results]

        results: List[Dict[str, Any]] = [
            {
                "title": r.get("title"),
                "url": r.get("url"),
                "snippet": r.get("content"),
                "engine": r.get("engine"),
                "score": None,  # SearXNG doesn't expose a numeric score
            }
            for r in trimmed
        ]

        out: Dict[str, Any] = {
            "query": query,
            "results": results,
            "number_of_results": data.get("number_of_results"),
        }
        if include_raw_content:
            out["raw"] = data

        return out

