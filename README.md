# Research Crew Starter Kit

A complete starter kit for building a multi-agent Research & Report Crew using CrewAI. This kit provides a curated corpus of 15 foundational research papers on AI agents, a vector store for RAG retrieval, and evaluation tools.

## Overview

This starter kit enables you to build a multi-agent system that:
1. **Expands** research questions into comprehensive search strategies
2. **Hunts** for relevant passages in academic papers using RAG
3. **Synthesizes** findings across sources to identify themes and gaps
4. **Writes** well-structured literature reviews with proper citations

## Paper Corpus

The kit includes 15 foundational papers on agentic AI:

| Category | Papers |
|----------|--------|
| **Agent Theory** | Wooldridge 1995, Wang 2023 Survey, Xi 2023 Survey |
| **Reasoning** | ReAct, Chain-of-Thought, Tree of Thoughts, Reflexion |
| **Multi-Agent** | CAMEL, Generative Agents, AutoGen |
| **Tool Use & RAG** | Toolformer, RAG (2020), RAG Survey (2023) |
| **Planning & Safety** | Planning Abilities, Constitutional AI |

## Prerequisites

- Python 3.11+
- OpenAI API key OR Google API key (for embeddings)
- ~500MB disk space for PDFs and vector store

## Quick Start

### 1. Clone and Setup Environment

```bash
# Using Conda (recommended)
conda env create -f environment.yml
conda activate research-crew

# OR using pip
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure API Keys

```bash
cp .env.example .env
# Edit .env and add your API key(s)
```

Choose your embedding provider in `.env`:
```bash
# For OpenAI embeddings
EMBEDDING_PROVIDER=openai
OPENAI_API_KEY=sk-your-key-here

# OR for Gemini embeddings (free tier)
EMBEDDING_PROVIDER=gemini
GOOGLE_API_KEY=AIza-your-key-here
```

### 3. Build Vector Store

The 15 research papers are already included in `data/papers/`. Just build the index:

```bash
# Build the vector store
python scripts/setup_vectorstore.py

# Verify everything works
python scripts/verify_setup.py
```

> **Note:** If you need to re-download papers, run `python scripts/download_papers.py`

### 4. Run the Crew

```bash
# Interactive mode
python main.py -i

# With a specific question
python main.py "What are the main approaches to building AI agents?"

# With an example question
python main.py --example
```

## Project Structure

```
research_crew_starter/
├── config/                 # Configuration
│   ├── settings.py        # Environment settings
│   └── chunking.py        # Chunking parameters
├── data/
│   ├── papers/            # PDF files + paper_index.json
│   ├── processed/         # Extracted text cache
│   ├── vectorstore/       # ChromaDB (gitignored)
│   └── evals/             # Test queries
├── tools/                 # Core tools
│   ├── pdf_processor.py   # PDF text extraction
│   ├── chunker.py         # Document chunking
│   ├── embeddings.py      # OpenAI/Gemini embeddings
│   └── paper_rag_tool.py  # CrewAI search tool
├── scripts/               # Setup scripts
│   ├── download_papers.py
│   ├── setup_vectorstore.py
│   └── verify_setup.py
├── evals/                 # Evaluation suite
│   ├── retrieval_metrics.py
│   ├── run_evals.py
│   └── report_generator.py
├── agents/                # Agent definitions (customize these!)
│   ├── query_expander.py
│   ├── source_hunter.py
│   ├── synthesizer.py
│   └── report_writer.py
├── tasks/                 # Task definitions (customize these!)
│   └── task_definitions.py
├── outputs/               # Generated reports
├── crew.py               # Crew configuration
└── main.py               # Entry point
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `EMBEDDING_PROVIDER` | "openai" or "gemini" | openai |
| `OPENAI_API_KEY` | OpenAI API key | - |
| `GOOGLE_API_KEY` | Google API key | - |
| `CHUNK_SIZE` | Tokens per chunk | 800 |
| `CHUNK_OVERLAP` | Overlap between chunks | 200 |

### Chunking Configuration

Edit `config/chunking.py` to adjust:
- Chunk size and overlap
- Section header detection
- Text cleanup patterns

## Learning Goals

By completing this assignment, you will:

1. **Understand Multi-Agent Architectures**
   - Learn how to decompose complex tasks into specialized agent roles
   - Understand agent collaboration patterns (sequential, hierarchical)
   - Practice designing agent personas with clear roles, goals, and backstories

2. **Master CrewAI Framework**
   - Create and configure CrewAI Agents with appropriate attributes
   - Define Tasks with descriptions, expected outputs, and context passing
   - Wire agents and tasks together into a functional Crew

3. **Work with RAG Systems**
   - Use pre-built RAG tools to retrieve relevant information
   - Understand how vector search enhances LLM capabilities
   - Learn to format and pass context between agents

4. **Build Real-World AI Applications**
   - Create an end-to-end literature review system
   - Handle task dependencies and information flow
   - Produce structured, citable academic output

## Assignment: What to Implement

### Provided (Ready to Use)
- All tools (PDF processing, chunking, embeddings, RAG)
- All scripts (download, setup, verify)
- Evaluation suite
- Configuration system
- `main.py` entry point

### Your Task (Implement These)

1. **`agents/*.py`** - Implement all 4 agents:
   - `query_expander.py` - Breaks down research questions
   - `source_hunter.py` - Searches the paper corpus (uses `search_papers` tool)
   - `synthesizer.py` - Identifies themes and gaps
   - `report_writer.py` - Writes the literature review

2. **`tasks/task_definitions.py`** - Define all 4 tasks:
   - Query expansion task
   - Source hunting task
   - Synthesis task
   - Report writing task

3. **`crew.py`** - Wire it together:
   - Create the crew with your agents
   - Configure sequential process
   - Implement `run_research()` function

### Optional Enhancements
- Add custom tools (keyword extraction, citation formatting)
- Implement query expansion logic
- Create additional helper agents

### Grading Rubric

| Level | Points | Description |
|-------|--------|-------------|
| **Basic** | 60% | Runs without errors, produces output |
| **Proficient** | 75% | Customized agents, reasonable output quality |
| **Advanced** | 90% | Added custom tools, high-quality synthesis |
| **Complete** | 100% | Meets all rubric requirements with polished implementation |
| **Exceptional** | Bonus | Novel approaches, excellent reports (extra credit) |

#### Detailed Rubric

**Basic (60%)**
- [ ] All 4 agents are implemented and instantiated
- [ ] All 4 tasks are defined with descriptions and expected outputs
- [ ] Crew runs without errors using `python main.py --example`
- [ ] Produces some form of text output

**Proficient (75%)**
- [ ] Agents have meaningful, differentiated roles and backstories
- [ ] Tasks have clear, detailed descriptions guiding agent behavior
- [ ] Context is properly passed between tasks
- [ ] Output includes content from the paper corpus (uses RAG tool)
- [ ] Report has recognizable structure (intro, findings, conclusion)

**Advanced (90%)**
- [ ] Agent prompts are well-crafted for optimal LLM performance
- [ ] Tasks include specific formatting requirements in expected_output
- [ ] Report includes proper citations referencing source papers
- [ ] Themes are coherently identified and synthesized
- [ ] Output quality is suitable for academic use

**Complete (100%)**
- [ ] All above criteria met with polish
- [ ] Report follows the full structure (Executive Summary through References)
- [ ] Citations are accurate and properly formatted
- [ ] Synthesis shows critical analysis, not just summarization
- [ ] Code is clean, well-commented, and follows best practices

**Exceptional (Bonus)**
- [ ] Custom tools added (e.g., keyword extraction, citation formatter)
- [ ] Additional helper agents for specialized tasks
- [ ] Novel workflow improvements or agent interactions
- [ ] Outstanding report quality with insights beyond source material
- [ ] Creative enhancements that improve the research process

## Running Evaluations

```bash
# Run full evaluation suite
python -m evals.run_evals

# With verbose output
python -m evals.run_evals -v

# Adjust k parameter
python -m evals.run_evals -k 10
```

Evaluation metrics:
- **Recall@k**: Fraction of expected papers in top-k results
- **Precision@k**: Fraction of top-k results that are relevant
- **MRR**: Mean Reciprocal Rank (position of first relevant result)
- **Concept Coverage**: Fraction of expected concepts found

## Troubleshooting

### "Vector store not found"
Run `python scripts/setup_vectorstore.py`

### "API key not found"
Check your `.env` file has the correct key set

### "PDF download failed"
Some papers may require manual download. Check `data/papers/paper_index.json` for URLs.

### "ChromaDB collection not found"
Delete `data/vectorstore/` and re-run setup

### Import errors
Make sure you're in the `research_crew_starter/` directory

## Example Research Questions

Try these questions to test your implementation:

### Beginner Questions
```bash
python main.py "What is an AI agent?"
python main.py "How does chain-of-thought prompting work?"
```

### Intermediate Questions
```bash
python main.py "What are the main approaches to building AI agents that can reason and act?"
python main.py "How do multi-agent systems coordinate and communicate?"
python main.py "What role does memory play in AI agent architectures?"
```

### Advanced Questions
```bash
python main.py "How does retrieval-augmented generation improve language model outputs?"
python main.py "What are the key challenges in making AI agents safe and aligned?"
python main.py "Compare and contrast different reasoning frameworks for LLM agents."
```

## Expected Output

### During Execution
When you run the crew, you'll see each agent working in sequence:

```
============================================================
[Query Expander] Breaking down research question...
- Identifying sub-questions
- Extracting key concepts and keywords
- Formulating search strategy

[Source Hunter] Searching paper corpus...
- Executing RAG queries against vector store
- Retrieving relevant passages from papers
- Collecting citations and sources

[Synthesizer] Analyzing findings...
- Identifying common themes across papers
- Noting contradictions or debates
- Finding research gaps

[Report Writer] Generating literature review...
- Structuring findings into sections
- Writing narrative synthesis
- Formatting citations
============================================================
```

### Final Report Structure
Your implementation should produce a markdown report with these sections:

```markdown
# Literature Review: [Research Question]

## Executive Summary
Brief overview of key findings (2-3 paragraphs)

## Introduction
Context and scope of the review

## Methodology
How sources were identified and analyzed

## Findings
### Theme 1: [e.g., "Reasoning Approaches"]
Discussion of findings with citations (Author, Year)

### Theme 2: [e.g., "Memory Systems"]
...

## Discussion
Synthesis of themes, contradictions, and gaps

## Conclusion
Key takeaways and future directions

## References
- Paper 1 (Author, Year)
- Paper 2 (Author, Year)
...
```

### Sample Output Snippet
For the question "What are the main approaches to building AI agents?":

```markdown
## Findings

### Theme 1: Reasoning and Acting Frameworks
The ReAct framework (Yao et al., 2023) introduces a paradigm where
agents interleave reasoning traces with actions. This approach
addresses limitations of chain-of-thought prompting by grounding
reasoning in actionable steps...

### Theme 2: Multi-Agent Collaboration
CAMEL (Li et al., 2023) demonstrates that multiple agents can
engage in role-playing scenarios to solve complex tasks. Similarly,
Generative Agents (Park et al., 2023) shows how agents can simulate
human behavior through memory and reflection...
```

Reports are saved to `outputs/` with timestamps.

## Resources

- [CrewAI Documentation](https://docs.crewai.com/)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [OpenAI Embeddings](https://platform.openai.com/docs/guides/embeddings)
- [Course Materials](https://ucla-extension.edu)

## License

This starter kit is provided for educational purposes as part of UCLA Extension's Agentic AI course.

---

**Happy researching!** If you encounter issues, check the troubleshooting section or reach out to course staff.
