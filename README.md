# Avaliador

Avaliador is an agentic arXiv paper evaluator that takes an arXiv URL, runs a multi-step review pipeline, and generates an evaluation report in Markdown.

## Tech Stack

- LangGraph for workflow orchestration
- LangSmith for tracing and debugging
- OpenRouter as the LLM gateway
- Gemini AI as the evaluation model
- Streamlit for the frontend UI

## Installation

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Configuration

This project uses OpenRouter with Gemini AI. Environment variables are defined in [.env.example](/Users/senthilnathan/Downloads/avaliador/.env.example).

Create a `.env` file in the project root by copying `.env.example`, then fill in your keys:

```env
OPENROUTER_API_KEY=your-openrouter-api-key
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
GEMINI_MODEL=google/gemini-2.0-flash-001
LANGSMITH_API_KEY=your-langsmith-api-key
LANGSMITH_TRACING=true
LANGSMITH_PROJECT=your-project-name
```

## Run

Use the frontend UI:

```bash
streamlit run app.py
```

Then paste an arXiv URL into the app and run the evaluation.

Use the CLI:

```bash
python3 main.py https://arxiv.org/abs/2312.00752
```

## Output

After a successful run, the evaluation report is saved automatically as a Markdown file inside `outputs/`.

The generated report includes:

- Executive Summary with a pass/fail recommendation
- Consistency Score
- Grammar Rating
- Novelty Index
- Fact Check Log
- Accuracy/Fabrication Score
