"""Central LLM factory so every agent uses the same provider and model configuration."""

import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

def get_llm(temperature: float = 0.2) -> ChatOpenAI:
    return ChatOpenAI(
        model=os.getenv("GEMINI_MODEL", "google/gemini-2.0-flash-exp:free"),
        temperature=temperature,
        openai_api_key=os.getenv("OPENROUTER_API_KEY"),
        openai_api_base=os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"),
        max_tokens=4096,
        default_headers={
            "HTTP-Referer": "https://arxiv-evaluator.local",
            "X-Title": "ArXiv Paper Evaluator",
        },
    )
