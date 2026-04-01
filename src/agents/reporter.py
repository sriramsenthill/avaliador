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
    pass_fail_recommendation = "PASS" if verdict == "PASS" else "FAIL"
    verdict_badge = {
        "PASS": "✅ PASS",
        "REVISE": "🟡 REVISE",
        "FAIL": "❌ FAIL",
    }.get(verdict, verdict)

    report = f"""# Evaluation Report

## Executive Summary

**Paper Title:** {state['title']}
**Evaluated On:** {evaluated_on}
**Pass/Fail Recommendation:** {pass_fail_recommendation}
**Overall Verdict:** {verdict_badge}
**Reviewer Confidence:** {state.get('reviewer_confidence', 'Medium')}

{state.get('executive_summary', 'No executive summary was generated.')}

## Detailed Scores

### Consistency Score

**Score:** {state.get('consistency_score', 0)}/100

{state.get('consistency_notes', 'No consistency notes were generated.')}

### Grammar Rating

**Rating:** {state.get('grammar_rating', 'N/A')}

{state.get('grammar_notes', 'No grammar notes were generated.')}

### Novelty Index

**Assessment:** {state.get('novelty_index', 'N/A')}

{state.get('novelty_notes', 'No novelty notes were generated.')}

### Fact Check Log

{_fact_check_table(state.get('fact_check_log', []))}

### Accuracy/Fabrication Score

**Risk Assessment:** {state.get('accuracy_score', 0.0):.1f}%

{state.get('accuracy_notes', 'No fabrication-risk notes were generated.')}

## Specialist Strengths

{_markdown_list(state.get('strengths', []))}

## Risk Assessment

{_markdown_list(state.get('risks', []))}

## Related Work Grounding

{_related_work_table(state.get('novelty_search_results', []))}

## Recommendations For Authors

{_markdown_list(state.get('recommendations', []))}
"""

    return {"final_report": report}
