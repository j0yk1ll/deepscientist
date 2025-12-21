"""Shared tools for DeepScientist agents."""

from .search import search_web
from .literature import (
    clear_papers_and_evidence,
    gather_evidence,
    search_citations,
    search_paper_by_doi,
    search_paper_by_title,
    search_papers,
)

__all__ = [
    # Search tools
    "search_web",
    # Literature search tools
    "search_papers",
    "search_paper_by_doi",
    "search_paper_by_title",
    "gather_evidence",
    "search_citations",
    "clear_papers_and_evidence",
]
