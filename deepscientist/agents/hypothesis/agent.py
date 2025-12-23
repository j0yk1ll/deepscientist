from typing import Optional, Sequence, Callable, Any

from deepagents import create_deep_agent, CompiledSubAgent
from langchain.chat_models import init_chat_model
from langchain.agents.middleware.types import AgentMiddleware

from .system_prompt import build_hypothesis_system_prompt

def _build_hypothesis_deep_agent(
    model: Optional[Any] = None,
    tools: Optional[Sequence[Callable[..., Any]]] = None,
    middleware: Optional[Sequence[AgentMiddleware]] = None,
):
    """Build a deep agent dedicated to the hypothesis role."""
    if model is None:
        model = init_chat_model("openai:gpt-4.1-mini")

    return create_deep_agent(
        model=model,
        tools=tools,
        system_prompt=build_hypothesis_system_prompt(tools),
        middleware=middleware,
    )

def create_hypothesis_subagent(
    description: str | None = None,
    model: Optional[Any] = None,
    tools: Optional[Sequence[Callable[..., Any]]] = None,
    middleware: Optional[Sequence[AgentMiddleware]] = None,
) -> CompiledSubAgent:
    """Create a CompiledSubAgent that wraps a deep agent for the hypothesis role."""
    deep_agent = _build_hypothesis_deep_agent(model=model, tools=tools, middleware=middleware)

    return CompiledSubAgent(
        name="hypothesis-agent",
        description=description or "Generates testable research hypotheses grounded in literature and data.",
        runnable=deep_agent,
    )
