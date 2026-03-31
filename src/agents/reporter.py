from src.state import PaperState
from datetime import datetime


def _markdown_list(items: list[str]) -> str:
    if not items:
        return "- None provided"
    return "\n".join(f"- {item}" for item in items)


def _escape_pipes(text: str) -> str:
    return str(text).replace("|", "\\|").replace("\n", " ")


def _fact_check_table(fact_log: list[dict]) -> str:
    if not fact_log:
        return "| Claim | Status | Note |\n|---|---|---|\n| No claims extracted | N/A | The fact checker did not return structured claims. |"

    rows = [
        f"| {_escape_pipes(item.get('claim', ''))} | {_escape_pipes(item.get('status', '')).upper()} | {_escape_pipes(item.get('note', ''))} |"
        for item in fact_log
    ]
    return "\n".join(["| Claim | Status | Note |", "|---|---|---|", *rows])


def _related_work_table(results: list[dict]) -> str:
    if not results:
        return "| Related Paper | Published | Why It Matters |\n|---|---|---|\n| No related work retrieved | N/A | Novelty assessment fell back to the paper abstract only. |"

    rows = [
        f"| [{_escape_pipes(item.get('title', 'Untitled'))}]({_escape_pipes(item.get('url', ''))}) | "
        f"{_escape_pipes(item.get('published', 'n/a'))} | {_escape_pipes(item.get('summary', ''))} |"
        for item in results
    ]
    return "\n".join(["| Related Paper | Published | Why It Matters |", "|---|---|---|", *rows])


def reporter_node(state: PaperState) -> dict:
    """Compile all agent outputs into a deterministic Markdown report."""
    evaluated_on = datetime.now().strftime("%Y-%m-%d %H:%M")
    verdict = state.get("overall_verdict", "REVISE").upper()
    verdict_badge = {
        "PASS": "✅ PASS",
        "REVISE": "🟡 REVISE",
        "FAIL": "❌ FAIL",
    }.get(verdict, verdict)

    report = f"""# Peer Review Judgement Report

## Executive Snapshot

**Paper Title:** {state['title']}
**Evaluated On:** {evaluated_on}
**Overall Verdict:** {verdict_badge}
**Reviewer Confidence:** {state.get('reviewer_confidence', 'Medium')}

{state.get('executive_summary', 'No executive summary was generated.')}

## Scorecard

| Category | Result | Analyst Notes |
|---|---|---|
| Consistency | {state.get('consistency_score', 0)}/100 | {_escape_pipes(state.get('consistency_notes', ''))} |
| Grammar & Language | {state.get('grammar_rating', 'N/A')} | {_escape_pipes(state.get('grammar_notes', ''))} |
| Novelty | {state.get('novelty_index', 'N/A')} | {_escape_pipes(state.get('novelty_notes', ''))} |
| Fabrication Probability | {state.get('accuracy_score', 0.0):.1f}% | {_escape_pipes(state.get('accuracy_notes', ''))} |

## Specialist Strengths

{_markdown_list(state.get('strengths', []))}

## Risk Assessment

{_markdown_list(state.get('risks', []))}

## Related Work Grounding

{_related_work_table(state.get('novelty_search_results', []))}

## Fact Check Log

{_fact_check_table(state.get('fact_check_log', []))}

## Recommendations For Authors

{_markdown_list(state.get('recommendations', []))}
"""

    return {"final_report": report}
