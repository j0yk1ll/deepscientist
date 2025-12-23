from __future__ import annotations

import dotenv
import httpx
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional
from langfuse import get_client
from langfuse.langchain import CallbackHandler


@dataclass(slots=True)
class Settings:
    """Configuration for HTTP clients, LLM runtime, and external integrations."""

    timeout: float = 10.0
    user_agent: str = "Kosmos-Preprint-Client/1.0"
    unpaywall_email: Optional[str] = None
    grobid_base_url: Optional[str] = None
    lm_model: str = "gpt-4.1-mini"
    lm_base_url: Optional[str] = None
    lm_api_key: Optional[str] = None
    lm_temperature: Optional[float] = 0.0
    lm_max_input_tokens: int = 32768
    workspace_root: str = "./workspace"
    langfuse_public_key: Optional[str] = None
    langfuse_secret_key: Optional[str] = None
    langfuse_base_url: Optional[str] = None
    client: Optional[httpx.Client] = field(default=None, repr=False)
    langfuse_client: Optional[Any] = field(default=None, repr=False)
    langfuse_handler: Optional[Any] = field(default=None, repr=False)

    def __post_init__(self) -> None:
        self._try_load_dotenv_from_project_root()
        self._apply_env_overrides()
        self._initialize_langfuse()

    def _apply_env_overrides(self) -> None:
        env_timeout = self._get_env_value("RETRIEVAL_REQUEST_TIMEOUT_S")
        if env_timeout and self.timeout == 10.0:
            self.timeout = float(env_timeout)

        env_unpaywall_email = self._get_env_value("RETRIEVAL_UNPAYWALL_EMAIL")
        if env_unpaywall_email and self.unpaywall_email is None:
            self.unpaywall_email = env_unpaywall_email

        env_grobid_url = self._get_env_value("RETRIEVAL_GROBID_URL")
        if env_grobid_url and self.grobid_base_url is None:
            self.grobid_base_url = env_grobid_url

        env_lm_model = self._get_env_value("LM_MODEL")
        if env_lm_model and self.lm_model == "gpt-4.1-mini":
            self.lm_model = env_lm_model

        env_lm_base_url = self._get_env_value("LM_BASE_URL")
        if env_lm_base_url and self.lm_base_url is None:
            self.lm_base_url = env_lm_base_url

        env_lm_api_key = self._get_env_value("LM_API_KEY")
        if env_lm_api_key and self.lm_api_key is None:
            self.lm_api_key = env_lm_api_key

        env_lm_temperature = self._get_env_value("LM_TEMPERATURE")
        if env_lm_temperature and self.lm_temperature == 0.0:
            self.lm_temperature = float(env_lm_temperature)

        env_lm_max_tokens = self._get_env_value("LM_MAX_INPUT_TOKENS")
        if env_lm_max_tokens and self.lm_max_input_tokens == 32768:
            self.lm_max_input_tokens = int(env_lm_max_tokens)

        env_workspace = self._get_env_value("WORKSPACE")
        if env_workspace and self.workspace_root == "./workspace":
            self.workspace_root = env_workspace

        env_langfuse_public_key = self._get_env_value("LANGFUSE_PUBLIC_KEY")
        if env_langfuse_public_key and self.langfuse_public_key is None:
            self.langfuse_public_key = env_langfuse_public_key

        env_langfuse_secret_key = self._get_env_value("LANGFUSE_SECRET_KEY")
        if env_langfuse_secret_key and self.langfuse_secret_key is None:
            self.langfuse_secret_key = env_langfuse_secret_key

        env_langfuse_base_url = self._get_env_value("LANGFUSE_BASE_URL")
        if env_langfuse_base_url and self.langfuse_base_url is None:
            self.langfuse_base_url = env_langfuse_base_url

        env_langfuse_host = self._get_env_value("LANGFUSE_HOST")
        if env_langfuse_host and self.langfuse_base_url is None:
            self.langfuse_base_url = env_langfuse_host

    def build_client(self) -> httpx.Client:
        """Return a configured :class:`httpx.Client` using the settings."""

        if self.client is not None:
            client = self.client
        else:
            client = httpx.Client(
                timeout=httpx.Timeout(self.timeout, connect=min(self.timeout, 10.0)),
                follow_redirects=True,
            )

        if self.user_agent:
            client.headers.setdefault("User-Agent", self.user_agent)
        return client

    def _initialize_langfuse(self) -> None:
        if self.langfuse_client is not None or self.langfuse_handler is not None:
            return
        if not self.langfuse_public_key or not self.langfuse_secret_key:
            return

        os.environ.setdefault("LANGFUSE_PUBLIC_KEY", self.langfuse_public_key)
        os.environ.setdefault("LANGFUSE_SECRET_KEY", self.langfuse_secret_key)
        if self.langfuse_base_url:
            os.environ.setdefault("LANGFUSE_HOST", self.langfuse_base_url)

        langfuse_client = get_client()
        if not langfuse_client.auth_check():
            print(
                "Langfuse authentication failed. Please check "
                "LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY, and LANGFUSE_HOST."
            )
            return

        self.langfuse_client = langfuse_client
        self.langfuse_handler = CallbackHandler()


    def _get_env_value(self, name: str) -> Optional[str]:
        value = os.environ.get(name)
        if value is None:
            return None
        value = value.strip()
        return value or None

    def _try_load_dotenv_from_project_root(self) -> None:
        """
        Best-effort dotenv loading.
        - If python-dotenv is not installed: do nothing.
        - If .env is missing: do nothing.
        - Does NOT override already-set environment variables.
        """
        # The package layout is <repo>/deepscientist/deepscientist/settings.py,
        # so the repository root is one level up from the first parent.
        project_root = Path(__file__).resolve().parents[1]

        env_path = project_root / ".env"

        if not env_path.exists():
            raise RuntimeError(f"Failed to find .env file at {env_path}")

        try:
            dotenv.load_dotenv(dotenv_path=str(env_path), override=False)
        except Exception:
            raise RuntimeError(f"Failed to load .env file at {env_path}")
