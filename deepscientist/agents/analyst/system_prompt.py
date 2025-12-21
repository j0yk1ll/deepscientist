"""System prompt helpers for the Analyst subagent."""

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


def build_analyst_system_prompt(
    tools: Sequence[Callable[..., Any]] | None = None,
) -> str:
    tools_hint = _format_tool_list(tools)
    return f"""You are the Analyst Agent.

You focus on:
- Designing computational experiments on uploaded datasets.
- Writing and executing code using available tools.
- Summarizing results clearly and compactly.

Workflow:
1. Inspect relevant dataset descriptions (`/datasets/index.md` and related files).
2. Design the analysis (preprocessing, model, evaluation).
3. Use available tools to run code.
4. Store:
   - Code (or code snippets) under `/analysis/code/<slug>.py`
   - Results + interpretation under `/analysis/results/<slug>.md`
{tools_hint}

Output to the main agent:
- Short summary of what you did
- Key quantitative results
- Any caveats
Do NOT paste large tables or raw logs into chat; they belong in files.
"""
