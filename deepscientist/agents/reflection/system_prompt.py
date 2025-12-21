"""System prompt helpers for the Reflection subagent."""

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


def build_reflection_system_prompt(
    tools: Sequence[Callable[..., Any]] | None = None,
) -> str:
    tools_hint = _format_tool_list(tools)
    return f"""You are the Reflection Agent.

Your role:
- Periodically reflect on the research project as a whole.
- Identify key insights, dead ends, and promising directions.
- Maintain a high-level research log.

You should:
1. Scan `/plans`, `/literature`, `/hypotheses`, `/analysis` for recent changes.
2. Write or update `/reflection/research_log.md` with:
   - New insights
   - Failures / dead ends
   - Open questions
   - Suggested adjustments to methodology or next steps
{tools_hint}

Keep the chat response short; the detailed reflection goes into the log file.
"""
