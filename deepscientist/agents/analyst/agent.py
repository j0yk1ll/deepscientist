from typing import Optional, Sequence, Callable, Any

from deepagents import create_deep_agent, CompiledSubAgent
from langchain.chat_models import init_chat_model

from .system_prompt import ANALYST_SYSTEM_PROMPT

def _build_analyst_deep_agent(
    model: Optional[Any] = None,
    tools: Optional[Sequence[Callable[..., Any]]] = None,
):
    """Build a deep agent dedicated to the analyst role."""
    if model is None:
        model = init_chat_model("openai:gpt-4.1-mini")

    return create_deep_agent(
        model=model,
        tools=tools,
        system_prompt=ANALYST_SYSTEM_PROMPT,
    )

def create_analyst_subagent(
    description: str | None = None,
    model: Optional[Any] = None,
    tools: Optional[Sequence[Callable[..., Any]]] = None,
) -> CompiledSubAgent:
    """Create a CompiledSubAgent that wraps a deep agent for the analyst role."""
    deep_agent = _build_analyst_deep_agent(model=model, tools=tools)

    return CompiledSubAgent(
        name="analyst-agent",
        description=description or "Designs and executes computational analyses on uploaded datasets and summarizes results.",
        runnable=deep_agent,
    )
