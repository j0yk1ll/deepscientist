"""Integration tests for agents with real LLM.

These tests require:
- An OpenAI-compatible API key and endpoint

Set environment variables:
- LM_API_KEY or OPENAI_API_KEY
- LM_BASE_URL (optional, for OpenAI-compatible endpoints)
- LM_MODEL (optional, defaults to gpt-4.1-mini)

Run with: pytest -m integration
"""

import os
import pytest


pytestmark = pytest.mark.integration


def llm_available():
    """Check if LLM API is configured."""
    return bool(os.getenv("LM_API_KEY") or os.getenv("OPENAI_API_KEY"))


@pytest.mark.skipif(
    not llm_available(),
    reason="LLM API not configured (set LM_API_KEY or OPENAI_API_KEY)"
)
class TestAgentIntegration:
    """Integration tests for agents with real LLM."""

    @pytest.fixture
    def model(self):
        """Create a real LLM instance."""
        from langchain.chat_models import init_chat_model
        
        model_name = os.getenv("LM_MODEL", "gpt-4.1-mini")
        api_key = os.getenv("LM_API_KEY") or os.getenv("OPENAI_API_KEY")
        base_url = os.getenv("LM_BASE_URL")
        
        return init_chat_model(
            model=model_name,
            model_provider="openai",
            api_key=api_key,
            base_url=base_url,
            temperature=0,
        )

    def test_create_analyst_agent(self, model):
        """Should create analyst agent with real model."""
        from deepscientist.agents import create_analyst_subagent
        
        agent = create_analyst_subagent(model=model)
        
        assert agent is not None
        assert agent.name == "analyst-agent"

    def test_create_literature_agent(self, model):
        """Should create literature agent with real model."""
        from deepscientist.agents import create_literature_subagent
        
        agent = create_literature_subagent(model=model)
        
        assert agent is not None
        assert agent.name == "literature-agent"

    def test_create_all_agents(self, model):
        """Should create all 7 agent types."""
        from deepscientist.agents import (
            create_analyst_subagent,
            create_file_upload_subagent,
            create_hypothesis_subagent,
            create_literature_subagent,
            create_planning_subagent,
            create_reflection_subagent,
            create_reply_subagent,
        )
        
        agents = [
            create_analyst_subagent(model=model),
            create_file_upload_subagent(model=model),
            create_hypothesis_subagent(model=model),
            create_literature_subagent(model=model),
            create_planning_subagent(model=model),
            create_reflection_subagent(model=model),
            create_reply_subagent(model=model),
        ]
        
        assert len(agents) == 7
        assert all(a is not None for a in agents)


@pytest.mark.skipif(
    not llm_available(),
    reason="LLM API not configured"
)
class TestConceptExtractionIntegration:
    """Integration tests for LLM-based concept extraction."""

    def test_extract_concepts_from_paper(self):
        """Should extract concepts using real LLM."""
        from deepscientist.knowledge_graph.agents.concept_extraction import (
            LangChainConceptExtractor,
        )
        from deepscientist.knowledge_graph.models import Paper, PaperSource
        
        paper = Paper(
            primary_identifier="concept-test-001",
            source=PaperSource.ARXIV,
            title="Deep Learning for Protein Structure Prediction",
            abstract=(
                "We present a novel deep learning approach for predicting "
                "protein tertiary structure from amino acid sequences. "
                "Our method uses transformer architectures combined with "
                "evolutionary information from multiple sequence alignments. "
                "We achieve state-of-the-art results on CASP14 targets."
            ),
        )
        
        extractor = LangChainConceptExtractor()
        result = extractor.extract(paper)

        assert result.paper_id == paper.primary_identifier
        assert len(result.concepts) > 0
        
        # Should extract relevant concepts
        concept_names = [c.name.lower() for c in result.concepts]
        assert any("protein" in name or "deep learning" in name for name in concept_names)

    def test_extract_concepts_with_methods(self):
        """Should extract both concepts and methods."""
        from deepscientist.knowledge_graph.agents.concept_extraction import (
            LangChainConceptExtractor,
        )
        from deepscientist.knowledge_graph.models import Paper, PaperSource
        
        paper = Paper(
            primary_identifier="method-test-001",
            source=PaperSource.ARXIV,
            title="CRISPR-Cas9 Gene Editing in Human Cells",
            abstract=(
                "We demonstrate efficient gene editing using CRISPR-Cas9 "
                "in human embryonic stem cells. Using guide RNAs targeting "
                "specific genomic loci, we achieved 90% editing efficiency. "
                "Single-cell RNA sequencing revealed minimal off-target effects."
            ),
        )
        
        extractor = LangChainConceptExtractor()
        result = extractor.extract(paper)

        # Should extract methods
        assert len(result.methods) > 0
        method_names = [m.name.lower() for m in result.methods]
        assert any(
            "crispr" in name or "rna sequencing" in name or "gene editing" in name
            for name in method_names
        )


@pytest.mark.skipif(
    not llm_available(),
    reason="LLM API not configured"
)
class TestOrchestratorIntegration:
    """Integration tests for the full orchestrator."""

    def test_create_orchestrator(self):
        """Should create orchestrator with real LLM."""
        from deepscientist.orchestrator import create_orchestrator_agent
        
        agent = create_orchestrator_agent()
        
        assert agent is not None

    @pytest.mark.slow
    def test_orchestrator_simple_query(self):
        """Should handle a simple research query.
        
        Note: This test makes real LLM calls and may be slow/expensive.
        Mark with @pytest.mark.slow to skip in quick test runs.
        """
        from deepscientist.orchestrator import create_orchestrator_agent
        
        agent = create_orchestrator_agent()
        
        # Use a simple query that doesn't require much computation
        result = agent.invoke({
            "messages": [
                {"role": "user", "content": "What is machine learning?"}
            ]
        })
        
        assert result is not None
        # Should have generated some response
        assert len(result.get("messages", [])) > 0
