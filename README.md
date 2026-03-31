# Avaliador: Agentic ArXiv Research Paper Evaluator

An agentic audit platform for research papers built with **LangGraph**, **Streamlit**, and **Gemini via OpenRouter**.

`Avaliador` means `evaluator` in Portuguese.

Instead of summarizing a paper once, the system:

- scrapes an arXiv paper
- decomposes it into reviewer-friendly sections
- fans out specialist reviewer agents in parallel
- grounds novelty with real external arXiv literature search
- synthesizes a board-level verdict
- renders a deterministic judgement report in Markdown

## What Makes This Version Stronger

- Real agent orchestration with LangGraph fan-out and fan-in, not just a linear chain
- Grounded novelty search using retrieved related work from the arXiv API
- Explicit meta-reviewer node for executive summary, verdict, risks, and recommendations
- Deterministic final report formatting, so the deliverable looks polished and consistent
- Upgraded Streamlit UI with reviewer board, progress timeline, evidence views, and downloads
- LangSmith tracing support for inspecting agent runs and debugging LLM behavior

## Architecture

Workflow:

1. `scraper`
2. `decomposer`
3. Parallel specialists:
   - `consistency`
   - `grammar`
   - `novelty`
   - `fact_checker`
4. `accuracy`
5. `executive_summary`
6. `reporter`

The shared state is carried through LangGraph and enriched at every step.

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```env
OPENROUTER_API_KEY=your_key_here
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
GEMINI_MODEL=google/gemini-2.0-flash-exp:free
LANGSMITH_API_KEY=your_langsmith_key_here
LANGSMITH_TRACING=true
LANGSMITH_PROJECT=avaliador
```

If LangSmith is configured, the application will trace LLM activity under the `avaliador` project so you can inspect agent execution and debugging logs.

## Run

### Recommended: Streamlit App

```bash
streamlit run app.py
```

Then paste an arXiv URL into the UI and run the full evaluation from the frontend.

### Optional: CLI

```bash
python3 main.py https://arxiv.org/abs/2312.00752
```

## Output

The system generates a structured judgement packet with:

- Executive summary and editorial verdict
- Consistency score
- Grammar rating
- Novelty index grounded by retrieved related papers
- Fact-check log
- Fabrication probability
- Recommendations for authors

The Streamlit app also exposes:

- extracted section previews
- related literature evidence
- specialist reviewer notes
- downloadable Markdown report
- downloadable raw evaluation JSON

## Notes

- The evaluator accepts arXiv `abs` and `pdf` URLs, then fetches the abstract page and HTML body when available.
- To stay within assignment constraints, prompts are aggressively size-limited before each LLM call.
- Novelty search is now grounded against external arXiv results, but this is still a lightweight literature scan rather than a full bibliographic review.
