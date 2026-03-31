from langchain_core.messages import HumanMessage
from src.state import PaperState
from src.llm import get_llm
from datetime import datetime


def reporter_node(state: PaperState) -> dict:
    """Compile all agent outputs into a final Judgement Report."""
    llm = get_llm(temperature=0.3)

    fact_log_str = "\n".join(
        f"  - [{f.get('status', '?').upper()}] {f.get('claim', '')} — {f.get('note', '')}"
        for f in state.get("fact_check_log", [])
    )

    fabrication = state.get("accuracy_score", 50.0)
    pass_fail = "✅ PASS" if (
        state.get("consistency_score", 0) >= 60
        and state.get("grammar_rating", "Low") in ["High", "Medium"]
        and fabrication <= 40
    ) else "❌ FAIL"

    prompt = f"""Generate a formal Peer Review Judgement Report in Markdown for the following paper evaluation data.

Paper Title: {state['title']}
Evaluated On: {datetime.now().strftime('%Y-%m-%d %H:%M')}
Overall Verdict: {pass_fail}

## Scores
- Consistency Score: {state.get('consistency_score')}/100
  Notes: {state.get('consistency_notes')}

- Grammar Rating: {state.get('grammar_rating')}
  Notes: {state.get('grammar_notes')}

- Novelty Index: {state.get('novelty_index')}
  Notes: {state.get('novelty_notes')}

- Fabrication Probability: {fabrication:.1f}%
  Notes: {state.get('accuracy_notes')}

## Fact Check Log
{fact_log_str}

Write a clean, professional Markdown report with:
1. Executive Summary (verdict + 2-3 sentence summary)
2. Detailed Scores section
3. Fact Check Log table (Claim | Status | Note)
4. Risk Assessment
5. Recommendations for authors

Use proper Markdown headers, tables, and bold text."""

    response = llm.invoke([HumanMessage(content=prompt)])
    return {"final_report": response.content}