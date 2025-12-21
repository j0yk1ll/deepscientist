"""Unit tests for the orchestrator agent.

These tests verify orchestrator creation and configuration with mocked dependencies.
"""

import pytest
from unittest.mock import patch, MagicMock
import os


# Check if orchestrator can be imported
try:
    from deepscientist.orchestrator.agent import create_orchestrator_agent
    ORCHESTRATOR_AVAILABLE = True
except ImportError as e:
    ORCHESTRATOR_AVAILABLE = False
    ORCHESTRATOR_IMPORT_ERROR = str(e)


@pytest.mark.skipif(
    not ORCHESTRATOR_AVAILABLE,
    reason=f"Orchestrator import failed: {ORCHESTRATOR_IMPORT_ERROR if not ORCHESTRATOR_AVAILABLE else ''}"
)
class TestOrchestratorCreation:
    """Test orchestrator agent creation."""

    @pytest.fixture
    def mock_dependencies(self):
        """Mock all external dependencies for orchestrator creation."""
        with patch("deepscientist.orchestrator.agent.init_chat_model") as mock_init_model, \
             patch("deepscientist.orchestrator.agent.create_deep_agent") as mock_deep_agent, \
             patch("deepscientist.orchestrator.agent.InMemoryStore") as mock_store, \
             patch("deepscientist.orchestrator.agent.FilesystemBackend") as mock_fs_backend, \
             patch("deepscientist.orchestrator.agent.CompositeBackend") as mock_composite, \
             patch("deepscientist.orchestrator.agent.create_file_upload_subagent") as mock_file_upload, \
             patch("deepscientist.orchestrator.agent.create_planning_subagent") as mock_planning, \
             patch("deepscientist.orchestrator.agent.create_literature_subagent") as mock_literature, \
             patch("deepscientist.orchestrator.agent.create_hypothesis_subagent") as mock_hypothesis, \
             patch("deepscientist.orchestrator.agent.create_analyst_subagent") as mock_analyst, \
             patch("deepscientist.orchestrator.agent.create_reflection_subagent") as mock_reflection, \
             patch("deepscientist.orchestrator.agent.create_reply_subagent") as mock_reply:
            
            mock_model = MagicMock()
            mock_model.profile = None  # No profile to trigger token-based limits
            mock_init_model.return_value = mock_model
            
            mock_agent = MagicMock()
            mock_deep_agent.return_value = mock_agent
            
            yield {
                "init_model": mock_init_model,
                "deep_agent": mock_deep_agent,
                "store": mock_store,
                "fs_backend": mock_fs_backend,
                "composite": mock_composite,
                "file_upload": mock_file_upload,
                "planning": mock_planning,
                "literature": mock_literature,
                "hypothesis": mock_hypothesis,
                "analyst": mock_analyst,
                "reflection": mock_reflection,
                "reply": mock_reply,
                "model": mock_model,
            }

    def test_create_orchestrator_with_default_model(self, mock_dependencies, clean_env):
        """Should create orchestrator with default model when none provided."""
        from deepscientist.orchestrator.agent import create_orchestrator_agent
        
        agent = create_orchestrator_agent()

        # Should have called init_chat_model
        mock_dependencies["init_model"].assert_called_once()
        # Should have created the deep agent
        mock_dependencies["deep_agent"].assert_called_once()

    def test_create_orchestrator_with_custom_model(self, mock_dependencies):
        """Should use provided model without calling init_chat_model."""
        from deepscientist.orchestrator.agent import create_orchestrator_agent
        
        custom_model = MagicMock()
        custom_model.profile = None
        agent = create_orchestrator_agent(model=custom_model)

        # init_chat_model should not be called when model is provided
        mock_dependencies["init_model"].assert_not_called()
        
        # deep_agent should be created with the custom model
        call_kwargs = mock_dependencies["deep_agent"].call_args[1]
        assert call_kwargs["model"] is custom_model

    def test_create_orchestrator_creates_all_subagents(self, mock_dependencies, clean_env):
        """Should create all 7 subagents."""
        from deepscientist.orchestrator.agent import create_orchestrator_agent
        
        agent = create_orchestrator_agent()

        mock_dependencies["file_upload"].assert_called_once()
        mock_dependencies["planning"].assert_called_once()
        mock_dependencies["literature"].assert_called_once()
        mock_dependencies["hypothesis"].assert_called_once()
        mock_dependencies["analyst"].assert_called_once()
        mock_dependencies["reflection"].assert_called_once()
        mock_dependencies["reply"].assert_called_once()

    def test_create_orchestrator_literature_gets_tools(self, mock_dependencies, clean_env):
        """Literature subagent should receive search and KG tools."""
        from deepscientist.orchestrator.agent import create_orchestrator_agent
        
        agent = create_orchestrator_agent()

        # Check literature subagent was created with tools
        call_kwargs = mock_dependencies["literature"].call_args[1]
        tools = call_kwargs.get("tools", [])
        
        # Should have multiple tools (search + KG tools)
        assert len(tools) > 5

    def test_create_orchestrator_uses_env_vars(self, mock_dependencies, monkeypatch):
        """Should use environment variables for model configuration."""
        monkeypatch.setenv("LM_MODEL", "gpt-4-turbo")
        monkeypatch.setenv("LM_BASE_URL", "http://localhost:8080/v1")
        monkeypatch.setenv("LM_API_KEY", "test-key")
        monkeypatch.setenv("LM_TEMPERATURE", "0.5")
        
        from deepscientist.orchestrator.agent import create_orchestrator_agent
        
        agent = create_orchestrator_agent()

        call_kwargs = mock_dependencies["init_model"].call_args[1]
        assert call_kwargs["model"] == "gpt-4-turbo"
        assert call_kwargs["base_url"] == "http://localhost:8080/v1"
        assert call_kwargs["api_key"] == "test-key"
        assert call_kwargs["temperature"] == 0.5

    def test_create_orchestrator_uses_workspace_env(self, mock_dependencies, monkeypatch):
        """Should use WORKSPACE env var for root directory."""
        monkeypatch.setenv("WORKSPACE", "/custom/workspace")
        
        from deepscientist.orchestrator.agent import create_orchestrator_agent
        
        agent = create_orchestrator_agent()

        # Check FilesystemBackend was created with custom root
        call_kwargs = mock_dependencies["fs_backend"].call_args[1]
        assert call_kwargs["root_dir"] == "/custom/workspace"

    def test_create_orchestrator_with_model_profile(self, mock_dependencies, clean_env):
        """Should use fraction-based limits when model has profile."""
        # Set up model with profile
        mock_dependencies["model"].profile = {
            "max_input_tokens": 128000,
        }
        
        from deepscientist.orchestrator.agent import create_orchestrator_agent
        
        agent = create_orchestrator_agent()

        # The summarization middleware should use fraction-based limits
        # This is tested implicitly by not erroring

    def test_create_orchestrator_uses_token_limits_from_env(self, mock_dependencies, monkeypatch):
        """Should use LM_MAX_INPUT_TOKENS env var for trigger."""
        monkeypatch.setenv("LM_MAX_INPUT_TOKENS", "32000")
        
        from deepscientist.orchestrator.agent import create_orchestrator_agent
        
        agent = create_orchestrator_agent()
        # Should not error with custom token limit


class TestOrchestratorSystemPrompt:
    """Test orchestrator system prompt."""

    def test_system_prompt_exists(self):
        """Verify system prompt is defined."""
        try:
            from deepscientist.orchestrator.system_prompt import ORCHESTRATOR_SYSTEM_PROMPT
        except ImportError:
            pytest.skip("Cannot import orchestrator system prompt")

        assert ORCHESTRATOR_SYSTEM_PROMPT is not None
        assert len(ORCHESTRATOR_SYSTEM_PROMPT) > 100
        assert isinstance(ORCHESTRATOR_SYSTEM_PROMPT, str)

    def test_system_prompt_mentions_orchestration(self):
        """System prompt should describe orchestration role."""
        try:
            from deepscientist.orchestrator.system_prompt import ORCHESTRATOR_SYSTEM_PROMPT
        except ImportError:
            pytest.skip("Cannot import orchestrator system prompt")

        prompt_lower = ORCHESTRATOR_SYSTEM_PROMPT.lower()
        # Should mention its role as coordinator/orchestrator
        assert any(word in prompt_lower for word in ["orchestrat", "coordinat", "manag", "research"])


@pytest.mark.skipif(
    not ORCHESTRATOR_AVAILABLE,
    reason=f"Orchestrator import failed"
)
class TestOrchestratorImports:
    """Test that orchestrator components can be imported."""

    def test_import_create_orchestrator_agent(self):
        """Test importing the main factory function."""
        from deepscientist.orchestrator.agent import create_orchestrator_agent
        
        assert callable(create_orchestrator_agent)

    def test_import_from_package(self):
        """Test importing from the orchestrator package."""
        from deepscientist.orchestrator import create_orchestrator_agent
        
        assert callable(create_orchestrator_agent)
