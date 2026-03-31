# 🔬 Agentic ArXiv Research Paper Evaluator

Multi-agent research paper auditor built with **LangGraph** + **Gemini via OpenRouter**.

## Setup

```bash
# 1. Clone and enter directory
git clone https://github.com/yourname/arxiv-evaluator
cd arxiv-evaluator

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env and add your OPENROUTER_API_KEY
```

## Get Your OpenRouter API Key
1. Go to https://openrouter.ai and sign up (free)
2. Navigate to **Keys** → **Create Key**
3. Paste it in `.env` as `OPENROUTER_API_KEY`

## Run

### CLI
```bash
python main.py https://arxiv.org/abs/2312.00752
```

### Streamlit UI
```bash
streamlit run app.py
```