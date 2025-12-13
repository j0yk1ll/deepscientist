from typing import Optional, Sequence, Callable, Any

from deepagents import create_deep_agent, CompiledSubAgent
from langchain.chat_models import init_chat_model

from .system_prompt import FILE_UPLOAD_SYSTEM_PROMPT

def _build_file_upload_deep_agent(
    model: Optional[Any] = None,
    tools: Optional[Sequence[Callable[..., Any]]] = None,
):
    """Build a deep agent dedicated to the file upload role."""
    if model is None:
        model = init_chat_model("openai:gpt-4.1-mini")

    return create_deep_agent(
        model=model,
        tools=tools,
        system_prompt=FILE_UPLOAD_SYSTEM_PROMPT,
    )

def create_file_upload_subagent(
    description: str | None = None,
    model: Optional[Any] = None,
    tools: Optional[Sequence[Callable[..., Any]]] = None,
) -> CompiledSubAgent:
    """Create a CompiledSubAgent that wraps a deep agent for the file upload role."""
    deep_agent = _build_file_upload_deep_agent(model=model, tools=tools)

    return CompiledSubAgent(
        name="file-upload-agent",
        description=description or "Parses uploaded files, infers structure, and writes dataset descriptions + metadata.",
        runnable=deep_agent,
    )
