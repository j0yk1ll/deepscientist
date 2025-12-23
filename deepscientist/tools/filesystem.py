from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Literal

from langchain.tools import ToolRuntime
from langchain_core.messages import ToolMessage
from langchain_core.tools import StructuredTool
from langgraph.types import Command

from deepscientist.settings import Settings
from deepagents.backends.filesystem import FilesystemBackend
from deepagents.backends.protocol import EditResult, WriteResult
from deepagents.backends.utils import format_grep_matches, truncate_if_too_long

from deepscientist.tools.utils import get_settings

DEFAULT_READ_OFFSET = 0
DEFAULT_READ_LIMIT = 500


# --------------------------------------------------------------------------------------
# Path validation / normalization
# --------------------------------------------------------------------------------------


def _validate_path(path: str) -> str:
    """Validate and normalize a virtual filesystem path."""
    if ".." in path or path.startswith("~"):
        raise ValueError(f"Path traversal not allowed: {path}")

    if re.match(r"^[a-zA-Z]:", path):
        raise ValueError(
            "Windows absolute paths are not supported: "
            f"{path}. Use virtual paths starting with /"
        )

    normalized = os.path.normpath(path).replace("\\", "/")
    if not normalized.startswith("/"):
        normalized = f"/{normalized}"
    return normalized


def _backend(settings: Settings) -> FilesystemBackend:
    """Instantiate a FilesystemBackend rooted at settings.workspace_root."""
    root_dir = Path(settings.workspace_root).expanduser().resolve()
    root_dir.mkdir(parents=True, exist_ok=True)
    # Preserve your prior behavior (virtual paths). If your FilesystemBackend
    # defaults differ, keep virtual_mode=True as you did in orchestrator.
    return FilesystemBackend(root_dir=str(root_dir), virtual_mode=True)


# --------------------------------------------------------------------------------------
# Tool descriptions (fixed)
# --------------------------------------------------------------------------------------

_LS_DESC = """Lists all files in the filesystem.

Usage:
- path must be an absolute virtual path (starting with /)
- Use this to explore the workspace before reading or editing files.
"""

_READ_DESC = """Reads a file from the filesystem.

Usage:
- file_path must be an absolute virtual path (starting with /)
- Use offset and limit to page through large files
- Defaults to reading the first 500 lines
"""

_WRITE_DESC = """Writes content to a file in the filesystem.

Usage:
- file_path must be an absolute virtual path (starting with /)
- content must be a string
- Creates or overwrites the file
"""

_EDIT_DESC = """Performs exact string replacements in a file.

Usage:
- file_path must be an absolute virtual path
- old_string must match exactly
- Set replace_all=True to replace multiple occurrences
"""

_GLOB_DESC = """Find files matching a glob pattern.

Usage:
- Supports *, **, ?
- pattern may be absolute or relative
- path optionally scopes the search
"""

_GREP_DESC = """Search for a literal string in files.

Usage:
- pattern is a literal string (not regex)
- path optionally scopes the search
- glob filters which files to search
- output_mode: files_with_matches | content | count
"""


# --------------------------------------------------------------------------------------
# Tool implementations (SYNC ONLY)
# --------------------------------------------------------------------------------------


def _ls(runtime: ToolRuntime, path: str) -> str:
    settings = get_settings(runtime)
    backend = _backend(settings)
    validated = _validate_path(path)
    infos = backend.ls_info(validated)
    paths = [fi.get("path", "") for fi in infos]
    return str(truncate_if_too_long(paths))


def _read_file(
    runtime: ToolRuntime,
    file_path: str,
    offset: int = DEFAULT_READ_OFFSET,
    limit: int = DEFAULT_READ_LIMIT,
) -> str:
    settings = _get_settings(runtime)
    backend = _backend(settings)
    validated = _validate_path(file_path)
    return backend.read(validated, offset=offset, limit=limit)


def _write_file(
    runtime: ToolRuntime,
    file_path: str,
    content: str,
) -> Command | str:
    settings = _get_settings(runtime)
    backend = _backend(settings)
    validated = _validate_path(file_path)
    res: WriteResult = backend.write(validated, content)

    if res.error:
        return res.error

    if res.files_update is not None:
        return Command(
            update={
                "files": res.files_update,
                "messages": [
                    ToolMessage(
                        content=f"Updated file {res.path}",
                        tool_call_id=runtime.tool_call_id,
                    )
                ],
            }
        )

    return f"Updated file {res.path}"


def _edit_file(
    runtime: ToolRuntime,
    file_path: str,
    old_string: str,
    new_string: str,
    *,
    replace_all: bool = False,
) -> Command | str:
    settings = _get_settings(runtime)
    backend = _backend(settings)
    validated = _validate_path(file_path)
    res: EditResult = backend.edit(validated, old_string, new_string, replace_all=replace_all)

    if res.error:
        return res.error

    if res.files_update is not None:
        return Command(
            update={
                "files": res.files_update,
                "messages": [
                    ToolMessage(
                        content=f"Successfully replaced {res.occurrences} instance(s) in '{res.path}'",
                        tool_call_id=runtime.tool_call_id,
                    )
                ],
            }
        )

    return f"Successfully replaced {res.occurrences} instance(s) in '{res.path}'"


def _glob(runtime: ToolRuntime, pattern: str, path: str = "/") -> str:
    settings = _get_settings(runtime)
    backend = _backend(settings)
    infos = backend.glob_info(pattern, path=path)
    paths = [fi.get("path", "") for fi in infos]
    return str(truncate_if_too_long(paths))


def _grep(
    runtime: ToolRuntime,
    pattern: str,
    path: str | None = None,
    glob: str | None = None,
    output_mode: Literal["files_with_matches", "content", "count"] = "files_with_matches",
) -> str:
    settings = _get_settings(runtime)
    backend = _backend(settings)
    raw = backend.grep_raw(pattern, path=path, glob=glob)
    if isinstance(raw, str):
        return raw
    formatted = format_grep_matches(raw, output_mode)
    return truncate_if_too_long(formatted)  # type: ignore[arg-type]


# --------------------------------------------------------------------------------------
# Public tool objects (ONLY exports)
# --------------------------------------------------------------------------------------

ls = StructuredTool.from_function(
    name="ls",
    description=_LS_DESC,
    func=_ls,
)

read_file = StructuredTool.from_function(
    name="read_file",
    description=_READ_DESC,
    func=_read_file,
)

write_file = StructuredTool.from_function(
    name="write_file",
    description=_WRITE_DESC,
    func=_write_file,
)

edit_file = StructuredTool.from_function(
    name="edit_file",
    description=_EDIT_DESC,
    func=_edit_file,
)

glob = StructuredTool.from_function(
    name="glob",
    description=_GLOB_DESC,
    func=_glob,
)

grep = StructuredTool.from_function(
    name="grep",
    description=_GREP_DESC,
    func=_grep,
)

__all__ = [
    "ls",
    "read_file",
    "write_file",
    "edit_file",
    "glob",
    "grep",
]
