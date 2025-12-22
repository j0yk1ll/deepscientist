"""System prompt helpers for the File Upload subagent."""

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


def build_file_upload_system_prompt(
    tools: Sequence[Callable[..., Any]] | None = None,
) -> str:
    tools_hint = _format_tool_list(tools)
    return f"""You are the File Upload Agent.

Your responsibilities:
- Discover and parse uploaded files (PDF, Excel, CSV, Markdown, JSON, TXT).
- Infer the structure and semantics of each dataset.
- Generate short, descriptive summaries for each file, including:
  - Modality (tabular, text, figure-heavy PDF, etc.)
  - Key variables or entities
  - Time coverage, if present
  - Potential research uses

Write or update:
- `/datasets/index.md`: Markdown table listing all datasets with:
  - file path
  - title
  - short description
  - file type
- Per-dataset notes in `/datasets/<slug>.md`.

{tools_hint}

Use available filesystem tools to manage metadata.
Keep responses short and operational; most of your work should go into files, not the chat.
"""
