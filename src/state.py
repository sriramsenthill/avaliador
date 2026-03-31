from typing import TypedDict, Optional


class PaperState(TypedDict):
    arxiv_url: str
    raw_text: str
    title: str
    sections: dict           # {"abstract": ..., "methodology": ..., "results": ..., "conclusion": ...}
    consistency_score: int
    consistency_notes: str
    grammar_rating: str      # High / Medium / Low
    grammar_notes: str
    novelty_index: str
    novelty_notes: str
    novelty_search_results: list
    fact_check_log: list     # [{"claim": ..., "status": "verified"/"unverified", "note": ...}]
    accuracy_score: float    # fabrication probability 0-100
    accuracy_notes: str
    overall_verdict: str
    executive_summary: str
    reviewer_confidence: str
    strengths: list
    risks: list
    recommendations: list
    final_report: str
    error: Optional[str]
