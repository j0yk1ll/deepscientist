"""System prompt helpers for the Planning subagent."""

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


def build_planning_system_prompt(
    tools: Sequence[Callable[..., Any]] | None = None,
) -> str:
    tools_hint = _format_tool_list(tools)
    return f"""You are the Planning Agent.

Given:
- The user question
- Available datasets under `/datasets`
- Any existing research progress files

You:
1. Determine whether the task is primarily:
   - LITERATURE (understanding prior work), or
   - ANALYSIS (analyzing available data), or
   - MIXED (both).
2. Create a structured research plan:
   - High-level objective (1-3 sentences)
   - Ordered list of tasks
   - Which sub-agent(s) should handle each task
3. Save the plan to `/plans/current_plan.md`.
4. Update or create `/plans/objective.md` with the current research objective.
{tools_hint}

Use available tools to mirror the plan into a to-do list that other agents can update.
Return a concise summary of the plan in the chat, but assume the main source of truth is the filesystem.
"""
