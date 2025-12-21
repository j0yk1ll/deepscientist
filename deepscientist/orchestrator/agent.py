from __future__ import annotations

import os
from typing import Any

from dotenv import load_dotenv

from langchain.chat_models import init_chat_model
from langchain.agents.middleware.summarization import SummarizationMiddleware

from langgraph.store.memory import InMemoryStore

from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend, CompositeBackend
from deepagents.middleware import (
    FilesystemMiddleware,
    SubAgentMiddleware,
    PatchToolCallsMiddleware,
)

from deepscientist.tools import (
    clear_papers_and_evidence,
    gather_evidence,
    search_citations,
    search_paper_by_doi,
    search_paper_by_title,
    search_papers,
    search_web,
)

from deepscientist.agents import (
    create_file_upload_subagent,
    create_planning_subagent,
    create_literature_subagent,
    create_hypothesis_subagent,
    create_analyst_subagent,
    create_reflection_subagent,
    create_reply_subagent,
)

from .system_prompt import ORCHESTRATOR_SYSTEM_PROMPT


def create_orchestrator_agent(
    model: Any | None = None
):
    """Create the top-level Orchestrator.

    Parameters
    ----------
    model:
        Optional LangChain chat model instance. If omitted, a default OpenAI
        model is initialized via `init_chat_model("openai:gpt-4.1")`.
    """
    if model is None:
        # Load environment variables from a .env file if present.
        # This uses python-dotenv so the project dependency was added.
        load_dotenv()
        # Initialize a provider-backed chat model using `init_chat_model`.
        # Environment vars supported (see `.env.example`):
        # - LM_MODEL (model identifier, default: "gpt-5-nano")
        # - LM_BASE_URL (optional OpenAI-compatible base URL)
        # - LM_API_KEY (optional API key)
        # - LM_TEMPERATURE (optional float)
        model_name = os.environ.get("LM_MODEL", "gpt-5-nano")
        base_url = os.environ.get("LM_BASE_URL") or None
        api_key = os.environ.get("LM_API_KEY") or None
        temp = os.environ.get("LM_TEMPERATURE")
        temperature = float(temp) if temp not in (None, "") else None

        # Use 'openai' as the model provider by default. This works for
        # OpenAI as well as OpenAI-compatible endpoints (LM Studio, OpenRouter, etc.).
        model = init_chat_model(
            model=model_name,
            model_provider="openai",
            api_key=api_key,
            base_url=base_url,
            temperature=temperature,
        )
        
    # Determine trigger/keep strategy based on whether the model exposes a
    # `profile` with `max_input_tokens`. If present, use fractional limits
    # (they rely on the model profile). Otherwise fall back to token/message
    # based limits that do not require the profile.
    if (
        getattr(model, "profile", None) is not None
        and isinstance(model.profile, dict)
        and "max_input_tokens" in model.profile
        and isinstance(model.profile["max_input_tokens"], int)
    ):
        trigger = ("fraction", 0.85)
        keep = ("fraction", 0.10)
    else:
        tokens = os.environ.get("LM_MAX_INPUT_TOKENS")
        trigger = ("tokens", int(tokens) if tokens is not None else 64000)
        keep = ("messages", 6)
        
    root_dir = os.environ.get("WORKSPACE", "./workspace")
    
    default_tools = []

    orchestrator_tools = []
    
    file_upload_tools = []
    
    planning_tools = []
    
    literature_tools = [
        search_web,
        search_papers,
        search_paper_by_doi,
        search_paper_by_title,
        gather_evidence,
        search_citations,
        clear_papers_and_evidence,
    ]
    
    hypothesis_tools = []
    
    analyst_tools = []
    
    reflection_tools = []
    
    reply_tools = []

    subagents = [
        create_file_upload_subagent(model=model, tools=file_upload_tools),
        create_planning_subagent(model=model, tools=planning_tools),
        create_literature_subagent(model=model, tools=literature_tools),
        create_hypothesis_subagent(model=model, tools=hypothesis_tools),
        create_analyst_subagent(model=model, tools=analyst_tools),
        create_reflection_subagent(model=model, tools=reflection_tools),
        create_reply_subagent(model=model, tools=reply_tools),
    ]
    
    composite_backend = CompositeBackend(
        default=FilesystemBackend(root_dir=root_dir, virtual_mode=True),
        routes={
            "/memories/": FilesystemBackend(root_dir=root_dir, virtual_mode=True),
            "/scratchpad/": FilesystemBackend(root_dir=root_dir, virtual_mode=True),
        }
    )
    
    interrupt_on = {}
    
    middleware = [
        FilesystemMiddleware(backend=composite_backend),
        SubAgentMiddleware(
            default_model=model,
            default_tools=default_tools,
            subagents=subagents if subagents is not None else [],
            default_middleware=[
                FilesystemMiddleware(backend=composite_backend),
                SummarizationMiddleware(
                    model=model,
                    trigger=trigger,
                    keep=keep,
                    trim_tokens_to_summarize=None,
                ),
                PatchToolCallsMiddleware(),
            ],
            default_interrupt_on=interrupt_on,
            general_purpose_agent=True,
        ),
        SummarizationMiddleware(
            model=model,
            trigger=trigger,
            keep=keep,
            trim_tokens_to_summarize=None,
        ),
        PatchToolCallsMiddleware(),
    ]

    agent = create_deep_agent(
        model=model,
        tools=orchestrator_tools,
        middleware=middleware,
        system_prompt=ORCHESTRATOR_SYSTEM_PROMPT,
        subagents=subagents,
        backend=composite_backend,
        store=InMemoryStore()
    )
    return agent
