"""Section extractor that turns the scraped paper text into reviewer-friendly slices."""

from langchain_core.messages import HumanMessage
from src.state import PaperState
from src.llm import get_llm
import json, re


def decomposer_node(state: PaperState) -> dict:
    """Break paper text into logical sections."""
    llm = get_llm()

    text_snippet = state["raw_text"][:10000]

    prompt = f"""You are a research paper parser.
Given the following paper text, extract and return a JSON object with these keys:
"abstract", "methodology", "results", "conclusion"

Each value should contain the relevant section text (or empty string if not found).
Keep each section under 1500 words.

Paper Title: {state['title']}

Paper Text:
{text_snippet}

Return ONLY valid JSON. No markdown fences, no explanation."""

    response = llm.invoke([HumanMessage(content=prompt)])
    content = response.content.strip()

    content = re.sub(r"^```(?:json)?\n?", "", content)
    content = re.sub(r"\n?```$", "", content)

    try:
        sections = json.loads(content)
    except json.JSONDecodeError:
        # Keep the pipeline moving even when the model returns malformed JSON.
        sections = {
            "abstract": state["raw_text"][:1000],
            "methodology": "",
            "results": "",
            "conclusion": "",
        }

    return {"sections": sections}
