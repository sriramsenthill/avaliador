from pathlib import Path
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parent / ".env", override=True)

import streamlit as st
from src.graph import build_graph

st.set_page_config(
    page_title="ArXiv Paper Evaluator",
    page_icon="🔬",
    layout="wide",
)

st.title("🔬 Agentic ArXiv Research Paper Evaluator")
st.caption("Powered by LangGraph + Gemini via OpenRouter")

arxiv_url = st.text_input(
    "Enter arXiv Paper URL",
    placeholder="https://arxiv.org/abs/2312.00752",
)

if st.button("🚀 Evaluate Paper", type="primary") and arxiv_url:
    initial_state = {
        "arxiv_url": arxiv_url,
        "raw_text": "", "title": "", "sections": {},
        "consistency_score": 0, "consistency_notes": "",
        "grammar_rating": "", "grammar_notes": "",
        "novelty_index": "", "novelty_notes": "",
        "fact_check_log": [], "accuracy_score": 0.0,
        "accuracy_notes": "", "final_report": "", "error": None,
    }

    app = build_graph()
    
    NODES = ["scraper", "decomposer", "consistency",
             "grammar", "novelty", "fact_checker", "accuracy", "reporter"]
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    final_state = initial_state.copy()

    # ✅ Stream ONCE — collect state as each node completes
    for step in app.stream(initial_state):
        node_name = list(step.keys())[0]
        node_data = step[node_name]
        final_state.update(node_data)

        idx = NODES.index(node_name) + 1 if node_name in NODES else len(NODES)
        progress_bar.progress(int(idx / len(NODES) * 100))
        status_text.text(f"✅ Completed: {node_name}  ({idx}/{len(NODES)})")

    progress_bar.progress(100)
    status_text.text("🎉 Done!")

    if final_state.get("error"):
        st.error(f"❌ Error: {final_state['error']}")
    else:
        st.success(f"✅ **{final_state.get('title', 'Paper')}** evaluated successfully!")

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Consistency", f"{final_state.get('consistency_score', 0)}/100")
        col2.metric("Grammar", final_state.get('grammar_rating', 'N/A'))
        col3.metric("Novelty", final_state.get('novelty_index', 'N/A'))
        col4.metric("Fabrication Risk", f"{final_state.get('accuracy_score', 0):.1f}%")

        st.divider()

        if final_state.get("fact_check_log"):
            st.subheader("🔍 Fact Check Log")
            for item in final_state["fact_check_log"]:
                icon = {"verified": "✅", "plausible": "🟡",
                        "unverified": "❓", "suspicious": "🚨"}.get(
                    item.get("status", ""), "❓")
                st.markdown(f"{icon} **{item.get('claim', '')}** — {item.get('note', '')}")

        st.divider()
        st.subheader("📄 Judgement Report")

        report = final_state.get("final_report", "")
        if report:
            st.markdown(report)
            st.download_button(
                label="⬇️ Download Report as Markdown",
                data=report,
                file_name="judgement_report.md",
                mime="text/markdown",
            )
        else:
            st.warning("Reporter returned empty output. Check your API rate limits.")