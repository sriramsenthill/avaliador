from langchain_core.messages import HumanMessage
from src.state import PaperState
from src.llm import get_llm
import re


def novelty_node(state: PaperState) -> dict:
    """Assess the uniqueness and novelty of the paper's contribution."""
    llm = get_llm()

    abstract = state["sections"].get("abstract", state["raw_text"][:1500])

    prompt = f"""You are a research novelty assessor with broad knowledge of academic literature.

Paper Title: {state['title']}

Abstract:
{abstract[:2000]}

Based on your knowledge of existing literature, evaluate:
1. Is this topic well-explored or a fresh area?
2. Does the paper propose a new method, dataset, or perspective?
3. How does it compare to known prior work?

Respond in this exact format:
NOVELTY_INDEX: <Highly Novel | Moderately Novel | Incremental | Derivative>
NOTES: <2-3 sentences citing comparable known works or gaps filled>"""

    response = llm.invoke([HumanMessage(content=prompt)])
    content = response.content

    index_match = re.search(
        r"NOVELTY_INDEX:\s*(Highly Novel|Moderately Novel|Incremental|Derivative)",
        content, re.IGNORECASE
    )
    notes_match = re.search(r"NOTES:\s*(.+)", content, re.DOTALL)

    index = index_match.group(1) if index_match else "Moderately Novel"
    notes = notes_match.group(1).strip() if notes_match else content

    return {"novelty_index": index, "novelty_notes": notes}