from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional
from uuid import uuid4

from langchain.tools import ToolRuntime
from langchain_core.tools import StructuredTool

from deepscientist.tools.utils import get_settings
import inspect

from llm_sandbox import SandboxSession

_SANDBOXES: Dict[str, "SandboxHandle"] = {}


@dataclass
class SandboxHandle:
    session: Any
    workspace_host: Path
    workspace_container: str


def _filter_kwargs(callable_obj: Any, kwargs: Dict[str, Any]) -> Dict[str, Any]:
    try:
        signature = inspect.signature(callable_obj)
    except (TypeError, ValueError):
        return kwargs
    return {key: value for key, value in kwargs.items() if key in signature.parameters}


def _mount_kwargs(workspace_host: Path, workspace_container: str) -> Dict[str, Any]:
    volumes = {
        str(workspace_host): {
            "bind": workspace_container,
            "mode": "rw",
        }
    }
    mounts = [
        {
            "source": str(workspace_host),
            "target": workspace_container,
            "type": "bind",
            "read_only": False,
        }
    ]
    return {
        "volumes": volumes,
        "mounts": mounts,
        "binds": {str(workspace_host): workspace_container},
        "workspace_dir": str(workspace_host),
        "workspace": str(workspace_host),
        "workdir": workspace_container,
    }


# --------------------------------------------------------------------------------------
# Tool descriptions (fixed)
# --------------------------------------------------------------------------------------

_CREATE_SANDBOX_DESC = """Create a persistent llm-sandbox session and return its identifier.

Args:
- lang: language runtime (default: python)
- backend: optional sandbox backend identifier
- image: optional container image identifier
- libraries: optional list of libraries to preinstall or enable

Returns:
- sandbox_id
- workspace_host
- workspace_container
"""

_DELETE_SANDBOX_DESC = """Close a previously created llm-sandbox session.

Args:
- sandbox_id: identifier returned by create_sandbox

Returns:
- deleted: bool
- sandbox_id (if deleted)
- error (if not deleted)
"""

_EXECUTE_CODE_DESC = """Execute code in a running sandbox.

Args:
- sandbox_id: identifier returned by create_sandbox
- code: code string to execute
- libraries: optional list of libraries for this run

Returns:
- stdout, stderr, exit_code, workspace_container
- plots (if provided)
- artifacts (if provided)
"""

_LIST_SANDBOXES_DESC = """List active sandboxes and their workspace mappings.

Returns:
- sandboxes: list of {sandbox_id, workspace_host, workspace_container}
"""


# --------------------------------------------------------------------------------------
# Tool implementations (SYNC ONLY, runtime-aware)
# --------------------------------------------------------------------------------------

def _create_sandbox(
    runtime: ToolRuntime,
    lang: str = "python",
    backend: Optional[str] = None,
    image: Optional[str] = None,
    libraries: Optional[list[str]] = None,
) -> Dict[str, Any]:
    """Create a persistent llm-sandbox session and return its identifier."""
    settings = get_settings(runtime)

    workspace_host = Path(settings.workspace_root).expanduser().resolve()
    workspace_host.mkdir(parents=True, exist_ok=True)
    workspace_container = "/workspace"

    session_kwargs: Dict[str, Any] = {
        "lang": lang,
        "backend": backend,
        "image": image,
        "libraries": libraries,
    }
    session_kwargs = {key: value for key, value in session_kwargs.items() if value is not None}

    mount_kwargs = _mount_kwargs(workspace_host, workspace_container)
    session_kwargs.update(_filter_kwargs(SandboxSession, mount_kwargs))
    session_kwargs = _filter_kwargs(SandboxSession, session_kwargs)

    session = SandboxSession(**session_kwargs)
    session.__enter__()

    sandbox_id = uuid4().hex
    _SANDBOXES[sandbox_id] = SandboxHandle(
        session=session,
        workspace_host=workspace_host,
        workspace_container=workspace_container,
    )

    return {
        "sandbox_id": sandbox_id,
        "workspace_host": str(workspace_host),
        "workspace_container": workspace_container,
    }


def _delete_sandbox(runtime: ToolRuntime, sandbox_id: str) -> Dict[str, Any]:
    """Close a previously created llm-sandbox session."""
    _ = get_settings(runtime)

    handle = _SANDBOXES.pop(sandbox_id, None)
    if handle is None:
        return {"deleted": False, "error": f"No sandbox found for id {sandbox_id}"}

    handle.session.__exit__(None, None, None)
    return {"deleted": True, "sandbox_id": sandbox_id}


def _execute_code(
    runtime: ToolRuntime,
    sandbox_id: str,
    code: str,
    libraries: Optional[list[str]] = None,
) -> Dict[str, Any]:
    """Execute code in a running sandbox and return stdout/stderr/exit_code."""
    _ = get_settings(runtime)

    handle = _SANDBOXES.get(sandbox_id)
    if handle is None:
        return {"error": f"No sandbox found for id {sandbox_id}"}

    run_kwargs: Dict[str, Any] = {"libraries": libraries} if libraries is not None else {}
    run_kwargs = _filter_kwargs(handle.session.run, run_kwargs)

    result = handle.session.run(code, **run_kwargs)

    response: Dict[str, Any] = {
        "stdout": getattr(result, "stdout", None),
        "stderr": getattr(result, "stderr", None),
        "exit_code": getattr(result, "exit_code", None),
        "workspace_container": handle.workspace_container,
    }
    if hasattr(result, "plots"):
        response["plots"] = getattr(result, "plots")
    if hasattr(result, "artifacts"):
        response["artifacts"] = getattr(result, "artifacts")
    return response


def _list_sandboxes(runtime: ToolRuntime) -> Dict[str, Any]:
    """List active sandboxes and their workspace mappings."""
    _ = get_settings(runtime)

    return {
        "sandboxes": [
            {
                "sandbox_id": sandbox_id,
                "workspace_host": str(handle.workspace_host),
                "workspace_container": handle.workspace_container,
            }
            for sandbox_id, handle in _SANDBOXES.items()
        ]
    }


# --------------------------------------------------------------------------------------
# Public tool objects (ONLY exports)
# --------------------------------------------------------------------------------------

create_sandbox = StructuredTool.from_function(
    name="create_sandbox",
    description=_CREATE_SANDBOX_DESC,
    func=_create_sandbox,
)

delete_sandbox = StructuredTool.from_function(
    name="delete_sandbox",
    description=_DELETE_SANDBOX_DESC,
    func=_delete_sandbox,
)

execute_code = StructuredTool.from_function(
    name="execute_code",
    description=_EXECUTE_CODE_DESC,
    func=_execute_code,
)

list_sandboxes = StructuredTool.from_function(
    name="list_sandboxes",
    description=_LIST_SANDBOXES_DESC,
    func=_list_sandboxes,
)

__all__ = [
    "create_sandbox",
    "delete_sandbox",
    "execute_code",
    "list_sandboxes",
]
