from langgraph.graph import StateGraph, END
from src.state import PaperState
from src.scraper import scrape_arxiv_paper
from src.agents.decomposer import decomposer_node
from src.agents.consistency import consistency_node
from src.agents.grammar import grammar_node
from src.agents.novelty import novelty_node
from src.agents.fact_checker import fact_check_node
from src.agents.accuracy import accuracy_node
from src.agents.executive_summary import executive_summary_node
from src.agents.reporter import reporter_node


def scraper_node(state: PaperState) -> dict:
    """Node 1: Scrape arXiv paper."""
    try:
        result = scrape_arxiv_paper(state["arxiv_url"])
        return {
            "raw_text": result["raw_text"],
            "title": result["title"],
        }
    except Exception as e:
        return {"error": str(e), "raw_text": "", "title": "Unknown"}


def should_stop(state: PaperState) -> str:
    """Stop early if scraping failed."""
    if state.get("error"):
        return "end"
    return "continue"


def build_graph() -> StateGraph:
    graph = StateGraph(PaperState)

    # Register nodes
    graph.add_node("scraper", scraper_node)
    graph.add_node("decomposer", decomposer_node)
    graph.add_node("consistency", consistency_node)
    graph.add_node("grammar", grammar_node)
    graph.add_node("novelty", novelty_node)
    graph.add_node("fact_checker", fact_check_node)
    graph.add_node("accuracy", accuracy_node)
    graph.add_node("executive_summary", executive_summary_node)
    graph.add_node("reporter", reporter_node)

    # Entry point
    graph.set_entry_point("scraper")

    # Conditional: stop on scrape error
    graph.add_conditional_edges(
        "scraper",
        should_stop,
        {"continue": "decomposer", "end": END},
    )

    # Specialist fan-out / fan-in pipeline
    graph.add_edge("decomposer", "consistency")
    graph.add_edge("decomposer", "grammar")
    graph.add_edge("decomposer", "novelty")
    graph.add_edge("decomposer", "fact_checker")

    graph.add_edge("consistency", "accuracy")
    graph.add_edge("grammar", "accuracy")
    graph.add_edge("novelty", "accuracy")
    graph.add_edge("fact_checker", "accuracy")

    graph.add_edge("accuracy", "executive_summary")
    graph.add_edge("executive_summary", "reporter")
    graph.add_edge("reporter", END)

    return graph.compile()
