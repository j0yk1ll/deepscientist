# DeepScientist – AI Scientist built on LangChain DeepAgents

This package defines an "AI Scientist" called **DeepScientist**, built on top of
[LangChain DeepAgents](https://github.com/langchain-ai/deepagents).

DeepScientist includes an integrated **Scientific Knowledge Graph** powered by Neo4j
and SPECTER embeddings for semantic search over scientific literature.


## Features

- **Multi-agent architecture** with specialized subagents for different research tasks
- **Scientific knowledge graph** with Neo4j backend for storing and querying papers, concepts, and methods
- **Semantic search** using SPECTER embeddings and Chroma vector index
- **LLM-powered concept extraction** to automatically identify scientific concepts and methods from papers
- **Literature search** across arXiv, bioRxiv, medRxiv, and ChemRxiv


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


## Knowledge Graph

The integrated knowledge graph provides:

- **Paper storage** with metadata (title, abstract, authors, citations)
- **Concept extraction** using LLM-powered analysis
- **Method tracking** to identify research techniques used in papers
- **Relationship mapping** between concepts
- **Semantic search** using SPECTER embeddings

### Knowledge Graph Tools

Agents have access to the following knowledge graph tools:

```python
# Ingestion
ingest_url_to_kg(url, ...)                           # Fetch and ingest a paper from URL

# Querying
search_kg_semantic(query, top_k=10)                  # Semantic search over papers
search_kg_by_concept(concept_name, ...)              # Find papers discussing a concept
search_kg_by_method(method_name, ...)                # Find papers using a method
find_related_concepts(concept_name, ...)             # Find related concepts
get_paper_from_kg(paper_id)                          # Retrieve paper details
```

### Direct Knowledge Graph Usage

```python
from deepscientist.knowledge_graph import ScientificKnowledgeGraph, PaperSource

graph = ScientificKnowledgeGraph(
    neo4j_uri="bolt://localhost:7687",
    neo4j_user="neo4j",
    neo4j_password="password",
)

# Ingest directly from a URL (metadata is extracted automatically)
paper = graph.ingest_url("https://arxiv.org/abs/2401.00001")

# Semantic search for related papers
results = graph.find_similar_papers_semantic("CRISPR off-target effects")
```


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

Required environment variables:
- `LM_API_KEY` - API key for your LLM provider

Optional:
- `LM_MODEL` - Model to use (default: gpt-4.1-mini)
- `LM_BASE_URL` - Base URL for OpenAI-compatible endpoints
- `NEO4J_URI` - Neo4j connection URI (default: bolt://localhost:7687)
- `NEO4J_USER` / `NEO4J_PASSWORD` - Neo4j credentials
- `WORKSPACE` - Filesystem root for agent workspace


## Docker Services

A `docker-compose.yaml` is provided to run Neo4j locally:

```bash
docker compose up -d
```

This starts:
- Neo4j (Bolt on `7687`, browser on `7474`) with default credentials `neo4j/password`

Stop with:

```bash
docker compose down
```
