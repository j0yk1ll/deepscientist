from typing import Optional, Sequence, Callable, Any

from deepagents import create_deep_agent, CompiledSubAgent
from langchain.chat_models import init_chat_model
from langchain.agents.middleware.types import AgentMiddleware

from .system_prompt import build_literature_system_prompt

def _build_literature_deep_agent(
    model: Optional[Any] = None,
    tools: Optional[Sequence[Callable[..., Any]]] = None,
    middleware: Optional[Sequence[AgentMiddleware]] = None,
):
    """Build a deep agent dedicated to the literature role."""
    if model is None:
        model = init_chat_model("openai:gpt-4.1-mini")

    return create_deep_agent(
        model=model,
        tools=tools,
        system_prompt=build_literature_system_prompt(tools),
        middleware=middleware,
    )

def create_literature_subagent(
    description: str | None = None,
    model: Optional[Any] = None,
    tools: Optional[Sequence[Callable[..., Any]]] = None,
    middleware: Optional[Sequence[AgentMiddleware]] = None,
) -> CompiledSubAgent:
    """Create a CompiledSubAgent that wraps a deep agent for the literature role."""
    deep_agent = _build_literature_deep_agent(model=model, tools=tools, middleware=middleware)

    return CompiledSubAgent(
        name="literature-agent",
        description=description or "Searches and synthesizes scientific literature with inline citations.",
        runnable=deep_agent,
    )
