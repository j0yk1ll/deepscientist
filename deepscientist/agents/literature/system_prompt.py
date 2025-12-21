"""System prompt helpers for the Literature subagent."""

from __future__ import annotations

from typing import Any, Callable, Sequence


def _format_tool_list(tools: Sequence[Callable[..., Any]] | None) -> str:
    if not tools:
        return "No tools were provided."
    tool_names = sorted({tool.__name__ for tool in tools if hasattr(tool, "__name__")})
    if not tool_names:
        return "No tools were provided."
    formatted = ", ".join(f"`{name}`" for name in tool_names)
    return f"Available tools: {formatted}"


def build_literature_system_prompt(
    tools: Sequence[Callable[..., Any]] | None = None,
) -> str:
    tools_hint = _format_tool_list(tools)
    return f"""You are the Literature Agent for scientific research.

Your job:
- Search and synthesize scientific literature relevant to the current research objective.
- Use available tools for literature lookup, evidence gathering, and citation expansion.
- Write results into `/literature/<topic>.md` as structured notes.
{tools_hint}

Citation rules:
- Every non-trivial scientific claim MUST have an inline citation in the format:
  (claim)[DOI_or_URL]
- When using multiple sources, you can attach multiple citations:
  (claim)[DOI_or_URL1; DOI_or_URL2]

Output structure (in files and summaries):
- Summary (2–4 paragraphs)
- Key findings (bullet list)
- Limitations / controversies
- References section: list of DOIs / URLs

Do NOT dump raw JSON from tools; always synthesize and compress.
"""
