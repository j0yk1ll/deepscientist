from __future__ import annotations

from typing import Any, List, Optional


def search_papers(query: str, k: int = 10) -> List[Any]:
    """Search for papers using the literature-retrieval-engine."""
    from literature_retrieval_engine import search_papers as engine_search_papers

    return engine_search_papers(query, k=k)


def search_paper_by_doi(doi: str) -> Optional[Any]:
    """Fetch a single paper by DOI."""
    from literature_retrieval_engine import search_paper_by_doi as engine_search_paper_by_doi

    return engine_search_paper_by_doi(doi)


def search_paper_by_title(title: str) -> Optional[Any]:
    """Fetch a single paper by title."""
    from literature_retrieval_engine import (
        search_paper_by_title as engine_search_paper_by_title,
    )

    return engine_search_paper_by_title(title)


def gather_evidence(query: str) -> List[Any]:
    """Gather evidence snippets for a query."""
    from literature_retrieval_engine import gather_evidence as engine_gather_evidence

    return engine_gather_evidence(query)


def search_citations(doi: str) -> List[Any]:
    """Search citations for a DOI."""
    from literature_retrieval_engine import search_citations as engine_search_citations

    return engine_search_citations(doi)


def clear_papers_and_evidence() -> None:
    """Clear in-memory caches for papers and evidence."""
    from literature_retrieval_engine import (
        clear_papers_and_evidence as engine_clear_papers_and_evidence,
    )

    engine_clear_papers_and_evidence()


__all__ = [
    "search_papers",
    "search_paper_by_doi",
    "search_paper_by_title",
    "gather_evidence",
    "search_citations",
    "clear_papers_and_evidence",
]
