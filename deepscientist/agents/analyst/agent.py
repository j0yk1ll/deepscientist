from typing import Optional, Sequence, Callable, Any

from deepagents import create_deep_agent, CompiledSubAgent
from langchain.chat_models import init_chat_model
from langchain.agents.middleware.types import AgentMiddleware

from .system_prompt import build_analyst_system_prompt

def _build_analyst_deep_agent(
    model: Optional[Any] = None,
    tools: Optional[Sequence[Callable[..., Any]]] = None,
    middleware: Optional[Sequence[AgentMiddleware]] = None,
):
    """Build a deep agent dedicated to the analyst role."""
    if model is None:
        model = init_chat_model("openai:gpt-4.1-mini")

    return create_deep_agent(
        model=model,
        tools=tools,
        system_prompt=build_analyst_system_prompt(tools),
        middleware=middleware,
    )

def create_analyst_subagent(
    description: str | None = None,
    model: Optional[Any] = None,
    tools: Optional[Sequence[Callable[..., Any]]] = None,
    middleware: Optional[Sequence[AgentMiddleware]] = None,
) -> CompiledSubAgent:
    """Create a CompiledSubAgent that wraps a deep agent for the analyst role."""
    deep_agent = _build_analyst_deep_agent(model=model, tools=tools, middleware=middleware)

    return CompiledSubAgent(
        name="analyst-agent",
        description=description or "Designs and executes computational analyses on uploaded datasets and summarizes results.",
        runnable=deep_agent,
    )
