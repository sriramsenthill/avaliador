"""Reviewer node that extracts structured claim-level checks from the paper body."""

from langchain_core.messages import HumanMessage
from src.state import PaperState
from src.llm import get_llm
import json, re


def fact_check_node(state: PaperState) -> dict:
    """Extract and verify factual claims, constants, and citations."""
    llm = get_llm()

    text = (
        state["sections"].get("methodology", "") + "\n" +
        state["sections"].get("results", "")
    )[:4000]

    prompt = f"""You are a scientific fact-checker.

From the following paper text, identify up to 8 key factual claims, constants, formulas, or cited statistics.
For each, assess whether it appears verifiable, plausible, or suspicious based on your knowledge.

Text:
{text}

Return a JSON array of objects with keys:
- "claim": the factual statement (short)
- "status": "verified" | "plausible" | "unverified" | "suspicious"
- "note": brief explanation

Return ONLY a valid JSON array. No markdown, no explanation."""

    response = llm.invoke([HumanMessage(content=prompt)])
    content = response.content.strip()

    content = re.sub(r"^```(?:json)?\n?", "", content)
    content = re.sub(r"\n?```$", "", content)

    try:
        fact_log = json.loads(content)
        if not isinstance(fact_log, list):
            raise ValueError("Not a list")
    except Exception:
        fact_log = [{"claim": "Unable to parse claims", "status": "unverified", "note": content[:200]}]

    return {"fact_check_log": fact_log}
