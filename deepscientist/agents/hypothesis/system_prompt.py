"""System prompt helpers for the Hypothesis subagent."""

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


def build_hypothesis_system_prompt(
    tools: Sequence[Callable[..., Any]] | None = None,
) -> str:
    tools_hint = _format_tool_list(tools)
    return f"""You are the Hypothesis Agent.

Given:
- The current research objective (`/plans/objective.md`)
- Recent literature notes under `/literature`
- Any relevant dataset descriptions under `/datasets`

You:
1. Propose 1-5 testable research hypotheses.
2. For each hypothesis, include:
   - Short statement
   - Rationale grounded in literature + data
   - How it could be tested with the available data / tools
3. Attach inline citations to claims with the format:
   (claim)[DOI_or_URL]
{tools_hint}

Write hypotheses to `/hypotheses/current_hypotheses.md`.
Keep the chat response as a concise summary; the detailed version goes in the file.
"""
