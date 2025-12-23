from __future__ import annotations

from typing import Any, List, Optional

from langchain.tools import ToolRuntime
from langchain_core.tools import StructuredTool

from deepscientist.tools.utils import get_settings


# --------------------------------------------------------------------------------------
# Tool descriptions (fixed)
# --------------------------------------------------------------------------------------

_SEARCH_PAPERS_DESC = """Search for papers using the literature retrieval engine.

Usage:
- query: natural language query
- k: maximum number of papers to return (default: 10)
"""

_SEARCH_PAPER_BY_DOI_DESC = """Fetch a single paper by DOI.

Usage:
- doi: Digital Object Identifier (e.g., 10.1038/nature12345)
"""

_SEARCH_PAPER_BY_TITLE_DESC = """Fetch a single paper by exact or near-exact title."""

_GATHER_EVIDENCE_DESC = """Gather evidence snippets relevant to a query."""

_SEARCH_CITATIONS_DESC = """Retrieve citations for a paper identified by DOI."""

_CLEAR_CACHE_DESC = """Clear in-memory caches for papers and evidence."""


# --------------------------------------------------------------------------------------
# Tool implementations (SYNC ONLY, runtime-aware)
# --------------------------------------------------------------------------------------

def _search_papers(runtime: ToolRuntime, query: str, k: int = 10) -> List[Any]:
    _ = get_settings(runtime)  # ensures consistent injection; reserved for future config use
    from literature_retrieval_engine import search_papers as engine_search_papers

    return engine_search_papers(query, k=k)


def _search_paper_by_doi(runtime: ToolRuntime, doi: str) -> Optional[Any]:
    _ = get_settings(runtime)
    from literature_retrieval_engine import search_paper_by_doi as engine_search_paper_by_doi

    return engine_search_paper_by_doi(doi)


def _search_paper_by_title(runtime: ToolRuntime, title: str) -> Optional[Any]:
    _ = get_settings(runtime)
    from literature_retrieval_engine import search_paper_by_title as engine_search_paper_by_title

    return engine_search_paper_by_title(title)


def _gather_evidence(runtime: ToolRuntime, query: str) -> List[Any]:
    _ = get_settings(runtime)
    from literature_retrieval_engine import gather_evidence as engine_gather_evidence

    return engine_gather_evidence(query)


def _search_citations(runtime: ToolRuntime, doi: str) -> List[Any]:
    _ = get_settings(runtime)
    from literature_retrieval_engine import search_citations as engine_search_citations

    return engine_search_citations(doi)


def _clear_papers_and_evidence(runtime: ToolRuntime) -> None:
    _ = get_settings(runtime)
    from literature_retrieval_engine import clear_papers_and_evidence as engine_clear_papers_and_evidence

    engine_clear_papers_and_evidence()
    return None


# --------------------------------------------------------------------------------------
# Public tool objects (ONLY exports)
# --------------------------------------------------------------------------------------

search_papers = StructuredTool.from_function(
    name="search_papers",
    description=_SEARCH_PAPERS_DESC,
    func=_search_papers,
)

search_paper_by_doi = StructuredTool.from_function(
    name="search_paper_by_doi",
    description=_SEARCH_PAPER_BY_DOI_DESC,
    func=_search_paper_by_doi,
)

search_paper_by_title = StructuredTool.from_function(
    name="search_paper_by_title",
    description=_SEARCH_PAPER_BY_TITLE_DESC,
    func=_search_paper_by_title,
)

gather_evidence = StructuredTool.from_function(
    name="gather_evidence",
    description=_GATHER_EVIDENCE_DESC,
    func=_gather_evidence,
)

search_citations = StructuredTool.from_function(
    name="search_citations",
    description=_SEARCH_CITATIONS_DESC,
    func=_search_citations,
)

clear_papers_and_evidence = StructuredTool.from_function(
    name="clear_papers_and_evidence",
    description=_CLEAR_CACHE_DESC,
    func=_clear_papers_and_evidence,
)

__all__ = [
    "search_papers",
    "search_paper_by_doi",
    "search_paper_by_title",
    "gather_evidence",
    "search_citations",
    "clear_papers_and_evidence",
]
