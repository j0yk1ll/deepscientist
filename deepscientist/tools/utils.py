from langchain.tools import ToolRuntime
from deepscientist.settings import Settings


def get_settings(runtime: ToolRuntime) -> Settings:
    """Retrieve injected Settings from runtime.context.

    Expected injection:
        agent.invoke(..., context={"settings": settings})
    """
    ctx = runtime.context
    if isinstance(ctx, dict):
        s = ctx.get("settings")
        if isinstance(s, Settings):
            return s
    raise RuntimeError(
        "Settings not found in runtime.context. "
        "Invoke the agent with context={'settings': Settings(...)}."
    )