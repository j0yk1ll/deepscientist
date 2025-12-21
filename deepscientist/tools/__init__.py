"""Shared tools for DeepScientist agents."""

from .search import (
    search_arxiv,
    search_biorxiv,
    search_medrxiv,
    search_chemrxiv,
    search_web,
)
from .knowledge_graph import (
    ingest_url_to_kg,
    search_kg_semantic,
    search_kg_by_concept,
    search_kg_by_method,
    find_related_concepts,
    get_paper_from_kg,
)

# search_kb is now an alias for search_kg_semantic for backwards compatibility
search_kb = search_kg_semantic

__all__ = [
    # Search tools
    "search_web",
    "search_arxiv",
    "search_medrxiv",
    "search_biorxiv",
    "search_chemrxiv",
    # Knowledge graph tools - ingestion
    "ingest_url_to_kg",
    # Knowledge graph tools - querying
    "search_kb",
    "search_kg_semantic",
    "search_kg_by_concept",
    "search_kg_by_method",
    "find_related_concepts",
    "get_paper_from_kg",
]
