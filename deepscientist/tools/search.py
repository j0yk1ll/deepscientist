from typing import List, Dict, Any

def search_arxiv(
    query: str,
    max_results: int = 25,
) -> List[Dict[str, object]]:
    """Search across arxiv preprint server.

    This is a placeholder that you should implement with real API.

    Expected return items:
    {
        "title": str,
        "abstract": str,
        "doi_or_url": str,
        "source": str,
        "year": int | None,
    }
    """
    raise NotImplementedError(
        "search_arxiv is a stub. Implement it with your preferred literature search stack."
    )

def search_medrxiv(
    query: str,
    max_results: int = 25,
) -> List[Dict[str, object]]:
    """Search across medrxiv preprint server.

    This is a placeholder that you should implement with real API.

    Expected return items:
    {
        "title": str,
        "abstract": str,
        "doi_or_url": str,
        "source": str,
        "year": int | None,
    }
    """
    raise NotImplementedError(
        "search_medrxiv is a stub. Implement it with your preferred literature search stack."
    )

def search_biorxiv(
    query: str,
    max_results: int = 25,
) -> List[Dict[str, object]]:
    """Search across biorxiv preprint server.

    This is a placeholder that you should implement with real API.

    Expected return items:
    {
        "title": str,
        "abstract": str,
        "doi_or_url": str,
        "source": str,
        "year": int | None,
    }
    """
    raise NotImplementedError(
        "search_biorxiv is a stub. Implement it with your preferred literature search stack."
    )

def search_chemrxiv(
    query: str,
    max_results: int = 25,
) -> List[Dict[str, object]]:
    """Search across chemrxiv preprint server.

    This is a placeholder that you should implement with real API.

    Expected return items:
    {
        "title": str,
        "abstract": str,
        "doi_or_url": str,
        "source": str,
        "year": int | None,
    }
    """
    raise NotImplementedError(
        "search_chemrxiv is a stub. Implement it with your preferred literature search stack."
    )

def search_kb(
    query: str,
    top_k: int = 10,
    namespace: str = "scientist-kb",
) -> List[Dict[str, object]]:
    """Semantic search over your custom knowledge base.

    Implement this using your vector DB of choice (Chroma, PgVector, Weaviate, etc.)
    plus an optional reranker.

    Expected return items:
    {
        "text": str,
        "score": float,
        "source": str,   # e.g. file path or doc ID
        "metadata": dict
    }
    """
    raise NotImplementedError(
        "search_kb is a stub. Implement it with your vector database + reranker."
    )

def search_web(
    query: str,
    max_results: int = 10,
    include_raw_content: bool = False,
) -> Dict[str, Any]:
    """Run a web search using SearXNG.

    This is a thin wrapper so deepagents can treat it as a tool.
    """
    raise NotImplementedError(
        "internet_search is a stub. Implement it with your preferred web search stack."
    )
