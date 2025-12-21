"""Unit tests for agent creation and configuration.

These tests verify that agents are created correctly with proper
configuration, system prompts, and tool bindings.
"""

import pytest
from unittest.mock import MagicMock, patch


class TestAgentCreation:
    """Test agent factory functions."""

    def test_create_analyst_subagent_with_defaults(self):
        """Test analyst agent creation with default parameters."""
        mock_deep_agent = MagicMock()
        mock_subagent = MagicMock()
        
        with patch(
            "deepscientist.agents.analyst.agent.create_deep_agent",
            return_value=mock_deep_agent,
        ), patch(
            "deepscientist.agents.analyst.agent.CompiledSubAgent",
            return_value=mock_subagent,
        ) as mock_compiled, patch(
            "deepscientist.agents.analyst.agent.init_chat_model",
            return_value=MagicMock(),
        ):
            from deepscientist.agents.analyst.agent import create_analyst_subagent
            agent = create_analyst_subagent()

        # Verify the subagent was created
        mock_compiled.assert_called_once()
        call_kwargs = mock_compiled.call_args[1]
        assert call_kwargs["name"] == "analyst-agent"
        # Description should mention analyses or computational work
        desc_lower = call_kwargs["description"].lower()
        assert "analys" in desc_lower or "computational" in desc_lower

    def test_create_analyst_subagent_with_custom_model(self):
        """Test analyst agent creation with custom model."""
        mock_deep_agent = MagicMock()
        mock_subagent = MagicMock()
        custom_model = MagicMock()
        
        with patch(
            "deepscientist.agents.analyst.agent.create_deep_agent",
            return_value=mock_deep_agent,
        ) as mock_create, patch(
            "deepscientist.agents.analyst.agent.CompiledSubAgent",
            return_value=mock_subagent,
        ):
            from deepscientist.agents.analyst.agent import create_analyst_subagent
            agent = create_analyst_subagent(model=custom_model)

        # Verify create_deep_agent was called with the custom model
        mock_create.assert_called_once()
        call_kwargs = mock_create.call_args[1]
        assert call_kwargs["model"] is custom_model

    def test_create_analyst_subagent_with_tools(self):
        """Test analyst agent creation with custom tools."""
        mock_deep_agent = MagicMock()
        mock_subagent = MagicMock()
        custom_model = MagicMock()
        mock_tool = MagicMock()
        
        with patch(
            "deepscientist.agents.analyst.agent.create_deep_agent",
            return_value=mock_deep_agent,
        ) as mock_create, patch(
            "deepscientist.agents.analyst.agent.CompiledSubAgent",
            return_value=mock_subagent,
        ):
            from deepscientist.agents.analyst.agent import create_analyst_subagent
            agent = create_analyst_subagent(model=custom_model, tools=[mock_tool])

        call_kwargs = mock_create.call_args[1]
        assert mock_tool in call_kwargs["tools"]

    def test_create_file_upload_subagent(self):
        """Test file upload agent creation."""
        mock_deep_agent = MagicMock()
        mock_subagent = MagicMock()
        
        with patch(
            "deepscientist.agents.file_upload.agent.create_deep_agent",
            return_value=mock_deep_agent,
        ), patch(
            "deepscientist.agents.file_upload.agent.CompiledSubAgent",
            return_value=mock_subagent,
        ) as mock_compiled, patch(
            "deepscientist.agents.file_upload.agent.init_chat_model",
            return_value=MagicMock(),
        ):
            from deepscientist.agents.file_upload.agent import create_file_upload_subagent
            agent = create_file_upload_subagent()

        mock_compiled.assert_called_once()
        call_kwargs = mock_compiled.call_args[1]
        assert call_kwargs["name"] == "file-upload-agent"

    def test_create_hypothesis_subagent(self):
        """Test hypothesis agent creation."""
        mock_deep_agent = MagicMock()
        mock_subagent = MagicMock()
        
        with patch(
            "deepscientist.agents.hypothesis.agent.create_deep_agent",
            return_value=mock_deep_agent,
        ), patch(
            "deepscientist.agents.hypothesis.agent.CompiledSubAgent",
            return_value=mock_subagent,
        ) as mock_compiled, patch(
            "deepscientist.agents.hypothesis.agent.init_chat_model",
            return_value=MagicMock(),
        ):
            from deepscientist.agents.hypothesis.agent import create_hypothesis_subagent
            agent = create_hypothesis_subagent()

        mock_compiled.assert_called_once()
        call_kwargs = mock_compiled.call_args[1]
        assert call_kwargs["name"] == "hypothesis-agent"

    def test_create_literature_subagent(self):
        """Test literature agent creation."""
        mock_deep_agent = MagicMock()
        mock_subagent = MagicMock()
        
        with patch(
            "deepscientist.agents.literature.agent.create_deep_agent",
            return_value=mock_deep_agent,
        ), patch(
            "deepscientist.agents.literature.agent.CompiledSubAgent",
            return_value=mock_subagent,
        ) as mock_compiled, patch(
            "deepscientist.agents.literature.agent.init_chat_model",
            return_value=MagicMock(),
        ):
            from deepscientist.agents.literature.agent import create_literature_subagent
            agent = create_literature_subagent()

        mock_compiled.assert_called_once()
        call_kwargs = mock_compiled.call_args[1]
        assert call_kwargs["name"] == "literature-agent"

    def test_create_planning_subagent(self):
        """Test planning agent creation."""
        mock_deep_agent = MagicMock()
        mock_subagent = MagicMock()
        
        with patch(
            "deepscientist.agents.planning.agent.create_deep_agent",
            return_value=mock_deep_agent,
        ), patch(
            "deepscientist.agents.planning.agent.CompiledSubAgent",
            return_value=mock_subagent,
        ) as mock_compiled, patch(
            "deepscientist.agents.planning.agent.init_chat_model",
            return_value=MagicMock(),
        ):
            from deepscientist.agents.planning.agent import create_planning_subagent
            agent = create_planning_subagent()

        mock_compiled.assert_called_once()
        call_kwargs = mock_compiled.call_args[1]
        assert call_kwargs["name"] == "planning-agent"

    def test_create_reflection_subagent(self):
        """Test reflection agent creation."""
        mock_deep_agent = MagicMock()
        mock_subagent = MagicMock()
        
        with patch(
            "deepscientist.agents.reflection.agent.create_deep_agent",
            return_value=mock_deep_agent,
        ), patch(
            "deepscientist.agents.reflection.agent.CompiledSubAgent",
            return_value=mock_subagent,
        ) as mock_compiled, patch(
            "deepscientist.agents.reflection.agent.init_chat_model",
            return_value=MagicMock(),
        ):
            from deepscientist.agents.reflection.agent import create_reflection_subagent
            agent = create_reflection_subagent()

        mock_compiled.assert_called_once()
        call_kwargs = mock_compiled.call_args[1]
        assert call_kwargs["name"] == "reflection-agent"

    def test_create_reply_subagent(self):
        """Test reply agent creation."""
        mock_deep_agent = MagicMock()
        mock_subagent = MagicMock()
        
        with patch(
            "deepscientist.agents.reply.agent.create_deep_agent",
            return_value=mock_deep_agent,
        ), patch(
            "deepscientist.agents.reply.agent.CompiledSubAgent",
            return_value=mock_subagent,
        ) as mock_compiled, patch(
            "deepscientist.agents.reply.agent.init_chat_model",
            return_value=MagicMock(),
        ):
            from deepscientist.agents.reply.agent import create_reply_subagent
            agent = create_reply_subagent()

        mock_compiled.assert_called_once()
        call_kwargs = mock_compiled.call_args[1]
        assert call_kwargs["name"] == "reply-agent"

    def test_create_subagent_custom_description(self):
        """Test that custom descriptions are passed through."""
        mock_deep_agent = MagicMock()
        mock_subagent = MagicMock()
        
        with patch(
            "deepscientist.agents.analyst.agent.create_deep_agent",
            return_value=mock_deep_agent,
        ), patch(
            "deepscientist.agents.analyst.agent.CompiledSubAgent",
            return_value=mock_subagent,
        ) as mock_compiled, patch(
            "deepscientist.agents.analyst.agent.init_chat_model",
            return_value=MagicMock(),
        ):
            from deepscientist.agents.analyst.agent import create_analyst_subagent
            custom_desc = "Custom analyst description for testing"
            agent = create_analyst_subagent(description=custom_desc)

        call_kwargs = mock_compiled.call_args[1]
        assert call_kwargs["description"] == custom_desc


class TestSystemPrompts:
    """Test that system prompts are properly formatted."""

    def test_analyst_system_prompt_is_non_empty(self):
        """Verify analyst system prompt exists and has content."""
        from deepscientist.agents.analyst.system_prompt import ANALYST_SYSTEM_PROMPT

        assert ANALYST_SYSTEM_PROMPT is not None
        assert len(ANALYST_SYSTEM_PROMPT) > 100
        assert isinstance(ANALYST_SYSTEM_PROMPT, str)

    def test_file_upload_system_prompt_is_non_empty(self):
        """Verify file upload system prompt exists and has content."""
        from deepscientist.agents.file_upload.system_prompt import FILE_UPLOAD_SYSTEM_PROMPT

        assert FILE_UPLOAD_SYSTEM_PROMPT is not None
        assert len(FILE_UPLOAD_SYSTEM_PROMPT) > 100

    def test_hypothesis_system_prompt_is_non_empty(self):
        """Verify hypothesis system prompt exists and has content."""
        from deepscientist.agents.hypothesis.system_prompt import HYPOTHESIS_SYSTEM_PROMPT

        assert HYPOTHESIS_SYSTEM_PROMPT is not None
        assert len(HYPOTHESIS_SYSTEM_PROMPT) > 100

    def test_literature_system_prompt_is_non_empty(self):
        """Verify literature system prompt exists and has content."""
        from deepscientist.agents.literature.system_prompt import LITERATURE_SYSTEM_PROMPT

        assert LITERATURE_SYSTEM_PROMPT is not None
        assert len(LITERATURE_SYSTEM_PROMPT) > 100

    def test_planning_system_prompt_is_non_empty(self):
        """Verify planning system prompt exists and has content."""
        from deepscientist.agents.planning.system_prompt import PLANNING_SYSTEM_PROMPT

        assert PLANNING_SYSTEM_PROMPT is not None
        assert len(PLANNING_SYSTEM_PROMPT) > 100

    def test_reflection_system_prompt_is_non_empty(self):
        """Verify reflection system prompt exists and has content."""
        from deepscientist.agents.reflection.system_prompt import REFLECTION_SYSTEM_PROMPT

        assert REFLECTION_SYSTEM_PROMPT is not None
        assert len(REFLECTION_SYSTEM_PROMPT) > 100

    def test_reply_system_prompt_is_non_empty(self):
        """Verify reply system prompt exists and has content."""
        from deepscientist.agents.reply.system_prompt import REPLY_SYSTEM_PROMPT

        assert REPLY_SYSTEM_PROMPT is not None
        assert len(REPLY_SYSTEM_PROMPT) > 100


class TestAgentImports:
    """Test that all agents can be imported from the main package."""

    def test_import_all_agent_factories(self):
        """Test importing all agent factory functions."""
        from deepscientist.agents import (
            create_analyst_subagent,
            create_file_upload_subagent,
            create_hypothesis_subagent,
            create_literature_subagent,
            create_planning_subagent,
            create_reflection_subagent,
            create_reply_subagent,
        )

        # All should be callable
        assert callable(create_analyst_subagent)
        assert callable(create_file_upload_subagent)
        assert callable(create_hypothesis_subagent)
        assert callable(create_literature_subagent)
        assert callable(create_planning_subagent)
        assert callable(create_reflection_subagent)
        assert callable(create_reply_subagent)
