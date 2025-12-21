from typing import Optional, Sequence, Callable, Any

from deepagents import create_deep_agent, CompiledSubAgent
from langchain.chat_models import init_chat_model

from .system_prompt import build_reply_system_prompt

def _build_reply_deep_agent(
    model: Optional[Any] = None,
    tools: Optional[Sequence[Callable[..., Any]]] = None,
):
    """Build a deep agent dedicated to the reply role."""
    if model is None:
        model = init_chat_model("openai:gpt-4.1-mini")

    return create_deep_agent(
        model=model,
        tools=tools,
        system_prompt=build_reply_system_prompt(tools),
    )

def create_reply_subagent(
    description: str | None = None,
    model: Optional[Any] = None,
    tools: Optional[Sequence[Callable[..., Any]]] = None,
) -> CompiledSubAgent:
    """Create a CompiledSubAgent that wraps a deep agent for the reply role."""
    deep_agent = _build_reply_deep_agent(model=model, tools=tools)

    return CompiledSubAgent(
        name="reply-agent",
        description=description or "Produces final user-facing responses in chat or deep research mode, preserving citations.",
        runnable=deep_agent,
    )
