from copy import deepcopy
from typing import Callable

from src.graph import build_graph


INITIAL_STATE = {
    "arxiv_url": "",
    "raw_text": "",
    "title": "",
    "sections": {},
    "consistency_score": 0,
    "consistency_notes": "",
    "grammar_rating": "",
    "grammar_notes": "",
    "novelty_index": "",
    "novelty_notes": "",
    "novelty_search_results": [],
    "fact_check_log": [],
    "accuracy_score": 0.0,
    "accuracy_notes": "",
    "overall_verdict": "",
    "executive_summary": "",
    "reviewer_confidence": "",
    "strengths": [],
    "risks": [],
    "recommendations": [],
    "final_report": "",
    "error": None,
}

DISPLAY_ORDER = [
    "scraper",
    "decomposer",
    "consistency",
    "grammar",
    "novelty",
    "fact_checker",
    "accuracy",
    "executive_summary",
    "reporter",
]

NODE_LABELS = {
    "scraper": "Paper Ingestion",
    "decomposer": "Section Decomposition",
    "consistency": "Consistency Review",
    "grammar": "Language Review",
    "novelty": "Novelty Search",
    "fact_checker": "Fact Verification",
    "accuracy": "Authenticity Audit",
    "executive_summary": "Meta Reviewer",
    "reporter": "Report Composer",
}


def build_initial_state(arxiv_url: str) -> dict:
    state = deepcopy(INITIAL_STATE)
    state["arxiv_url"] = arxiv_url.strip()
    return state


def run_evaluation(
    arxiv_url: str,
    on_step: Callable[[str, dict, dict], None] | None = None,
) -> dict:
    app = build_graph()
    initial_state = build_initial_state(arxiv_url)
    final_state = deepcopy(initial_state)

    for step in app.stream(initial_state):
        node_name, node_data = next(iter(step.items()))
        final_state.update(node_data)
        if on_step:
            on_step(node_name, node_data, deepcopy(final_state))

    return final_state
