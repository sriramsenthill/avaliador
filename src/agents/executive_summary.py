from __future__ import annotations

import json
import re

from langchain_core.messages import HumanMessage

from src.llm import get_llm
from src.state import PaperState


def _fallback_summary(state: PaperState) -> dict:
    suspicious = sum(1 for item in state.get("fact_check_log", []) if item.get("status") == "suspicious")
    fabrication = state.get("accuracy_score", 50.0)
    consistency = state.get("consistency_score", 0)
    grammar = state.get("grammar_rating", "Medium")

    if consistency >= 75 and fabrication <= 25 and suspicious == 0 and grammar in {"High", "Medium"}:
        verdict = "PASS"
    elif consistency >= 55 and fabrication <= 55:
        verdict = "REVISE"
    else:
        verdict = "FAIL"

    summary = (
        f"The paper received a {verdict} verdict based on a consistency score of {consistency}/100, "
        f"a grammar rating of {grammar}, and a fabrication risk of {fabrication:.1f}%."
    )
    return {
        "overall_verdict": verdict,
        "reviewer_confidence": "Medium",
        "executive_summary": summary,
        "strengths": [
            "The paper was automatically decomposed and evaluated across multiple specialist reviewers.",
            "The final verdict is grounded in consistency, language, novelty, and fact-check signals.",
        ],
        "risks": [
            "Some analysis depends on extracted sections rather than the full paper body.",
            "The verdict should be treated as an audit aid, not a substitute for expert peer review.",
        ],
        "recommendations": [
            "Review the flagged risks and suspicious claims before publication.",
            "Use the detailed notes below to guide manual verification.",
        ],
    }


def executive_summary_node(state: PaperState) -> dict:
    llm = get_llm(temperature=0.2)

    related_titles = "\n".join(
        f"- {item.get('title', 'Unknown title')} ({item.get('published', 'n/a')})"
        for item in state.get("novelty_search_results", [])[:5]
    )
    fact_summary = "\n".join(
        f"- [{item.get('status', 'unknown').upper()}] {item.get('claim', '')}: {item.get('note', '')}"
        for item in state.get("fact_check_log", [])[:5]
    )

    prompt = f"""You are the lead reviewer synthesizing specialist agent outputs into a final editorial judgement.

Paper Title: {state['title']}

Consistency Score: {state.get('consistency_score')}/100
Consistency Notes: {state.get('consistency_notes')}

Grammar Rating: {state.get('grammar_rating')}
Grammar Notes: {state.get('grammar_notes')}

Novelty Index: {state.get('novelty_index')}
Novelty Notes: {state.get('novelty_notes')}

Related Literature:
{related_titles or '- No external literature results available'}

Fabrication Probability: {state.get('accuracy_score'):.1f}%
Fabrication Notes: {state.get('accuracy_notes')}

Fact Check Summary:
{fact_summary or '- No fact checks available'}

Return ONLY valid JSON with this schema:
{{
  "overall_verdict": "PASS" | "REVISE" | "FAIL",
  "reviewer_confidence": "High" | "Medium" | "Low",
  "executive_summary": "2-3 sentences",
  "strengths": ["bullet", "bullet", "bullet"],
  "risks": ["bullet", "bullet", "bullet"],
  "recommendations": ["bullet", "bullet", "bullet"]
}}"""

    response = llm.invoke([HumanMessage(content=prompt)])
    content = response.content.strip()
    content = re.sub(r"^```(?:json)?\n?", "", content)
    content = re.sub(r"\n?```$", "", content)

    try:
        payload = json.loads(content)
        return {
            "overall_verdict": payload.get("overall_verdict", "REVISE"),
            "reviewer_confidence": payload.get("reviewer_confidence", "Medium"),
            "executive_summary": payload.get("executive_summary", ""),
            "strengths": payload.get("strengths", []),
            "risks": payload.get("risks", []),
            "recommendations": payload.get("recommendations", []),
        }
    except Exception:
        return _fallback_summary(state)
