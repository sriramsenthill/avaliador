from langchain_core.messages import HumanMessage
from src.state import PaperState
from src.llm import get_llm
import re


def accuracy_node(state: PaperState) -> dict:
    """Calculate fabrication probability based on anomalies and logical leaps."""
    llm = get_llm()

    # Summarize previous findings for context
    fact_summary = "\n".join(
        f"- [{f['status'].upper()}] {f['claim']}: {f['note']}"
        for f in state.get("fact_check_log", [])[:6]
    )

    prompt = f"""You are an academic integrity auditor calculating a "Fabrication Probability Score".

Paper Title: {state['title']}

Consistency Score: {state.get('consistency_score', 'N/A')}/100
Grammar Rating: {state.get('grammar_rating', 'N/A')}
Novelty Index: {state.get('novelty_index', 'N/A')}

Fact Check Summary:
{fact_summary or 'No fact data available'}

Abstract:
{state['sections'].get('abstract', '')[:1500]}

Based on all signals above, calculate a Fabrication Probability (0 = certainly authentic, 100 = likely fabricated).
Consider: statistical anomalies, overclaimed results, missing methodology details, implausible benchmarks.

Respond in this exact format:
FABRICATION_SCORE: <float 0.0-100.0>
NOTES: <3-4 sentences explaining key risk factors or confidence signals>"""

    response = llm.invoke([HumanMessage(content=prompt)])
    content = response.content

    score_match = re.search(r"FABRICATION_SCORE:\s*([\d.]+)", content)
    notes_match = re.search(r"NOTES:\s*(.+)", content, re.DOTALL)

    score = float(score_match.group(1)) if score_match else 50.0
    score = max(0.0, min(100.0, score))
    notes = notes_match.group(1).strip() if notes_match else content

    return {"accuracy_score": score, "accuracy_notes": notes}