"""Reviewer node that scores language quality from representative paper sections."""

from langchain_core.messages import HumanMessage
from src.state import PaperState
from src.llm import get_llm
import re


def grammar_node(state: PaperState) -> dict:
    """Evaluate professional tone, grammar, and language quality."""
    llm = get_llm()

    sample_text = (
        state["sections"].get("abstract", "") + "\n\n" +
        state["sections"].get("conclusion", "")
    )[:3000]

    prompt = f"""You are an academic language editor.
Evaluate the following paper excerpt for:
1. Grammar and spelling correctness
2. Academic/professional tone
3. Clarity and readability
4. Technical writing quality

Text:
{sample_text}

Respond in this exact format:
RATING: <High|Medium|Low>
NOTES: <2-3 sentences with specific observations>"""

    response = llm.invoke([HumanMessage(content=prompt)])
    content = response.content

    rating_match = re.search(r"RATING:\s*(High|Medium|Low)", content, re.IGNORECASE)
    notes_match = re.search(r"NOTES:\s*(.+)", content, re.DOTALL)

    rating = rating_match.group(1).capitalize() if rating_match else "Medium"
    notes = notes_match.group(1).strip() if notes_match else content

    return {"grammar_rating": rating, "grammar_notes": notes}
