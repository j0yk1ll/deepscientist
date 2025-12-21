# DeepScientist – AI Scientist built on LangChain DeepAgents

This package defines an "AI Scientist" called **DeepScientist**, built on top of
[LangChain DeepAgents](https://github.com/langchain-ai/deepagents).

## Subagents

### File Upload Agent - Handles file parsing, storage, and automatic description generation

- Supports PDF, Excel, CSV, MD, JSON, TXT files
- Generates AI-powered descriptions for each dataset
- Stores files with metadata

### Planning Agent - Creates research plans based on user questions

- Analyzes available datasets and research context
- Generates task sequences (LITERATURE or ANALYSIS)
- Updates current research objectives

### Literature Agent - Searches and synthesizes scientific literature

- General scientific literature search with citations via arxiv, medrxiv, chemrxiv and biorxiv
- Searches the knowledge graph with semantic search
- Ingests papers into the knowledge graph for future reference
- Returns synthesized findings with inline citations in format: (claim)[DOI or URL]

### Hypothesis Agent - Generates testable research hypotheses

- Synthesizes findings from literature
- Creates testable hypotheses with inline citations
- Considers current research context and objectives

### Analyst Agent - Performs data analysis on uploaded datasets

- Designs experimental protocols
- Writes and executes code
- Synthesizes results

### Reflection Agent - Reflects on research progress

- Extracts key insights and discoveries
- Updates research methodology
- Maintains conversation-level understanding

### Reply Agent - Generates user-facing responses

- Deep Research Mode: Includes current objective, next steps, and asks for feedback
- Chat Mode: Concise answers without next steps
- Preserves inline citations throughout

Each subagent is itself a deep agent.

## Installation

```bash
# Using uv
uv sync

# With visualization support
uv sync --extra viz

# With test dependencies
uv sync --group tests
```

## Usage

```python
from deepscientist.orchestrator import create_orchestrator_agent

agent = create_orchestrator_agent()

result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "How do Yamanaka factors compare to small-molecule reprogramming for hepatocyte conversion?",
            }
        ]
    }
)

print(result["messages"][-1].content)
```

## Configuration

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

## Docker Services

```bash
docker compose up -d
```

Stop with:

```bash
docker compose down
```
