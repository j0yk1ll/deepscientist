from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional
from uuid import uuid4

from deepscientist.settings import Settings

_SANDBOXES: Dict[str, "SandboxHandle"] = {}


@dataclass
class SandboxHandle:
    session: Any
    workspace_host: Path
    workspace_container: str


def _filter_kwargs(callable_obj: Any, kwargs: Dict[str, Any]) -> Dict[str, Any]:
    import inspect

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


def create_sandbox(
    lang: str = "python",
    backend: Optional[str] = None,
    image: Optional[str] = None,
    libraries: Optional[list[str]] = None,
) -> Dict[str, Any]:
    """Create a persistent llm-sandbox session and return its identifier."""
    from llm_sandbox import SandboxSession

    settings = Settings()
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


def delete_sandbox(sandbox_id: str) -> Dict[str, Any]:
    """Close a previously created llm-sandbox session."""
    handle = _SANDBOXES.pop(sandbox_id, None)
    if handle is None:
        return {"deleted": False, "error": f"No sandbox found for id {sandbox_id}"}
    handle.session.__exit__(None, None, None)
    return {"deleted": True, "sandbox_id": sandbox_id}


def execute_code(
    sandbox_id: str,
    code: str,
    libraries: Optional[list[str]] = None,
) -> Dict[str, Any]:
    """Execute code in a running sandbox and return stdout/stderr/exit_code."""
    handle = _SANDBOXES.get(sandbox_id)
    if handle is None:
        return {"error": f"No sandbox found for id {sandbox_id}"}

    run_kwargs: Dict[str, Any] = {"libraries": libraries} if libraries is not None else {}
    run_kwargs = _filter_kwargs(handle.session.run, run_kwargs)

    result = handle.session.run(code, **run_kwargs)
    response = {
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


def list_sandboxes() -> Dict[str, Any]:
    """List active sandboxes and their workspace mappings."""
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


__all__ = [
    "create_sandbox",
    "delete_sandbox",
    "execute_code",
    "list_sandboxes",
]
