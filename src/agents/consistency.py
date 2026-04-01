"""Reviewer node that compares methods and results for internal scientific consistency."""

from langchain_core.messages import HumanMessage
from src.state import PaperState
from src.llm import get_llm
import re


def consistency_node(state: PaperState) -> dict:
    """Check if methodology logically supports the claimed results."""
    llm = get_llm()
    sections = state["sections"]

    prompt = f"""You are a scientific peer reviewer evaluating internal consistency.

Methodology Section:
{sections.get('methodology', 'Not found')[:3000]}

Results Section:
{sections.get('results', 'Not found')[:3000]}

Evaluate:
1. Does the methodology adequately support the results claimed?
2. Are there logical gaps or unsupported leaps?
3. Are the experimental design and conclusions aligned?

Respond in this exact format:
SCORE: <integer 0-100>
NOTES: <2-3 sentence explanation>"""

    response = llm.invoke([HumanMessage(content=prompt)])
    content = response.content

    score_match = re.search(r"SCORE:\s*(\d+)", content)
    notes_match = re.search(r"NOTES:\s*(.+)", content, re.DOTALL)

    score = int(score_match.group(1)) if score_match else 50
    notes = notes_match.group(1).strip() if notes_match else content

    return {"consistency_score": score, "consistency_notes": notes}
