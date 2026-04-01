"""Streamlit entrypoint for running the evaluation pipeline from the browser."""

from pathlib import Path
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parent / ".env", override=True)

import streamlit as st
from src.service import DISPLAY_ORDER, NODE_LABELS, run_evaluation, save_evaluation_report

st.set_page_config(
    page_title="Avaliador",
    page_icon="🔬",
    layout="wide",
)

st.markdown(
    """
    <link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=DM+Mono:wght@300;400;500&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;1,9..40,300&display=swap" rel="stylesheet">

    <style>
    /* ── Root tokens ───────────────────────────────────────────── */
    :root {
        --bg:          #0e0f11;
        --bg-2:        #161719;
        --bg-3:        #1f2023;
        --bg-4:        #27292d;
        --border:      #2e3035;
        --border-2:    #3a3d44;
        --text:        #e8e6e1;
        --text-2:      #a8a49d;
        --text-3:      #55524d;
        --accent:      #e05c3a;
        --pass:        #4ade80;
        --pass-bg:     rgba(74,222,128,0.1);
        --pass-text:   #86efac;
        --revise:      #fbbf24;
        --revise-bg:   rgba(251,191,36,0.1);
        --revise-text: #fde68a;
        --fail:        #f87171;
        --fail-bg:     rgba(248,113,113,0.1);
        --fail-text:   #fca5a5;
        --serif:       'Instrument Serif', Georgia, serif;
        --mono:        'DM Mono', 'Courier New', monospace;
        --sans:        'DM Sans', system-ui, sans-serif;
        --r:           5px;
    }

    /* ── App shell ─────────────────────────────────────────────── */
    html, body,
    .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stAppViewBlockContainer"],
    .main {
        background-color: var(--bg) !important;
        color: var(--text) !important;
        font-family: var(--sans) !important;
    }
    .stApp > header { display: none !important; }
    .block-container {
        padding: 2.5rem 2.5rem 4rem !important;
        max-width: 1200px !important;
        background: transparent !important;
    }

    /* ── Sidebar ───────────────────────────────────────────────── */
    [data-testid="stSidebar"],
    [data-testid="stSidebar"] > div,
    [data-testid="stSidebarContent"],
    section[data-testid="stSidebar"] {
        background-color: var(--bg-2) !important;
        border-right: 1px solid var(--border) !important;
    }
    [data-testid="stSidebar"] * {
        font-family: var(--sans) !important;
        color: var(--text-2) !important;
    }
    [data-testid="stSidebar"] strong {
        color: var(--text) !important;
    }
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h1 * {
        font-family: var(--serif) !important;
        color: var(--text) !important;
        font-size: 1.25rem !important;
        font-weight: 400 !important;
        border-bottom: 1px solid var(--border) !important;
        padding-bottom: 0.75rem !important;
        margin-bottom: 1rem !important;
    }
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] p,
    [data-testid="stSidebar"] .stCaption p {
        color: var(--text-3) !important;
        font-size: 0.77rem !important;
        line-height: 1.6 !important;
    }

    /* ── Masthead ──────────────────────────────────────────────── */
    .masthead {
        display: flex;
        align-items: flex-start;
        justify-content: space-between;
        border-top: 2px solid var(--text);
        border-bottom: 1px solid var(--border);
        padding: 1.4rem 0 1.3rem;
        margin-bottom: 2rem;
        gap: 2rem;
    }
    .masthead-kicker {
        font-family: var(--mono);
        font-size: 0.68rem;
        letter-spacing: 0.16em;
        text-transform: uppercase;
        color: var(--accent);
        margin-bottom: 0.45rem;
    }
    .masthead-title {
        font-family: var(--serif);
        font-size: 2.5rem;
        line-height: 1.06;
        color: var(--text);
        margin: 0 0 0.65rem;
        font-weight: 400;
    }
    .masthead-title em { font-style: italic; color: var(--accent); }
    .masthead-desc {
        font-size: 0.88rem;
        color: var(--text-2);
        line-height: 1.7;
        max-width: 54ch;
        font-weight: 300;
    }
    .masthead-badge {
        font-family: var(--mono);
        font-size: 0.66rem;
        letter-spacing: 0.08em;
        color: var(--text-3);
        text-align: right;
        white-space: nowrap;
        padding-top: 0.3rem;
    }
    .masthead-badge span {
        display: block;
        font-family: var(--serif);
        font-size: 2rem;
        color: var(--text);
        letter-spacing: 0;
        line-height: 1.1;
    }

    /* ── Buttons ───────────────────────────────────────────────── */
    .stButton > button {
        font-family: var(--mono) !important;
        font-size: 0.77rem !important;
        letter-spacing: 0.05em !important;
        background: var(--bg-3) !important;
        color: var(--text-2) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--r) !important;
        transition: all 0.15s ease !important;
        box-shadow: none !important;
    }
    .stButton > button:hover {
        background: var(--bg-4) !important;
        color: var(--text) !important;
        border-color: var(--border-2) !important;
    }
    [data-testid="stFormSubmitButton"] > button {
        background: var(--text) !important;
        color: var(--bg) !important;
        border: none !important;
        font-family: var(--sans) !important;
        font-size: 0.88rem !important;
        font-weight: 500 !important;
        letter-spacing: 0.02em !important;
        border-radius: var(--r) !important;
        transition: background 0.15s !important;
    }
    [data-testid="stFormSubmitButton"] > button:hover {
        background: var(--accent) !important;
        color: #fff !important;
    }

    /* ── Text input ────────────────────────────────────────────── */
    .stTextInput > div > div > input {
        font-family: var(--mono) !important;
        font-size: 0.85rem !important;
        background: var(--bg-3) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--r) !important;
        color: var(--text) !important;
        padding: 0.6rem 0.9rem !important;
        caret-color: var(--accent) !important;
    }
    .stTextInput > div > div > input::placeholder {
        color: var(--text-3) !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: var(--border-2) !important;
        box-shadow: 0 0 0 2px rgba(255,255,255,0.04) !important;
        outline: none !important;
    }
    .stTextInput label p,
    .stTextInput label {
        font-family: var(--mono) !important;
        font-size: 0.7rem !important;
        letter-spacing: 0.12em !important;
        text-transform: uppercase !important;
        color: var(--text-3) !important;
    }

    /* ── Tabs ──────────────────────────────────────────────────── */
    .stTabs [data-baseweb="tab-list"] {
        background: transparent !important;
        border-bottom: 1px solid var(--border) !important;
        gap: 0 !important;
    }
    .stTabs [data-baseweb="tab"] {
        font-family: var(--sans) !important;
        font-size: 0.83rem !important;
        font-weight: 400 !important;
        color: var(--text-3) !important;
        padding: 0.65rem 1.1rem !important;
        border-bottom: 2px solid transparent !important;
        background: transparent !important;
        letter-spacing: 0.01em !important;
    }
    .stTabs [aria-selected="true"] {
        color: var(--text) !important;
        font-weight: 500 !important;
        border-bottom-color: var(--accent) !important;
    }
    .stTabs [data-baseweb="tab-highlight"],
    .stTabs [data-baseweb="tab-border"] { display: none !important; }
    .stTabs [data-baseweb="tab-panel"] {
        background: transparent !important;
        padding-top: 1.2rem !important;
    }

    /* ── Metrics ───────────────────────────────────────────────── */
    [data-testid="stMetric"] {
        background: var(--bg-2) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--r) !important;
        padding: 1rem 1.15rem !important;
    }
    [data-testid="stMetricLabel"] p {
        font-family: var(--mono) !important;
        font-size: 0.66rem !important;
        letter-spacing: 0.12em !important;
        text-transform: uppercase !important;
        color: var(--text-3) !important;
    }
    [data-testid="stMetricValue"],
    [data-testid="stMetricValue"] div {
        font-family: var(--serif) !important;
        font-size: 1.9rem !important;
        color: var(--text) !important;
    }

    /* ── Progress ──────────────────────────────────────────────── */
    [data-testid="stProgressBar"] > div {
        background: var(--bg-3) !important;
        border-radius: 2px !important;
        height: 2px !important;
    }
    [data-testid="stProgressBar"] > div > div {
        background: var(--accent) !important;
        border-radius: 2px !important;
    }

    /* ── Expanders ─────────────────────────────────────────────── */
    [data-testid="stExpander"] {
        background: var(--bg-2) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--r) !important;
    }
    [data-testid="stExpander"] summary {
        font-family: var(--sans) !important;
        font-size: 0.87rem !important;
        font-weight: 500 !important;
        color: var(--text) !important;
        background: transparent !important;
        padding: 0.8rem 1rem !important;
    }
    [data-testid="stExpander"] > div > div {
        background: transparent !important;
        padding: 0 1rem 0.9rem !important;
    }
    [data-testid="stExpander"] p {
        color: var(--text-2) !important;
        font-size: 0.86rem !important;
        line-height: 1.75 !important;
    }

    /* ── Alerts ────────────────────────────────────────────────── */
    .stAlert {
        background: var(--bg-2) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--r) !important;
        font-family: var(--sans) !important;
        font-size: 0.86rem !important;
    }
    .stAlert p { color: var(--text-2) !important; }

    /* ── Download buttons ──────────────────────────────────────── */
    [data-testid="stDownloadButton"] > button {
        font-family: var(--mono) !important;
        font-size: 0.78rem !important;
        letter-spacing: 0.05em !important;
        background: var(--bg-3) !important;
        color: var(--text-2) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--r) !important;
        transition: all 0.15s !important;
    }
    [data-testid="stDownloadButton"] > button:hover {
        background: var(--text) !important;
        color: var(--bg) !important;
        border-color: var(--text) !important;
    }

    /* ── General markdown / text overrides ────────────────────── */
    .stMarkdown p, .stMarkdown li {
        color: var(--text-2) !important;
        font-family: var(--sans) !important;
        font-size: 0.88rem !important;
        line-height: 1.7 !important;
    }
    .stMarkdown h3, h3 {
        font-family: var(--serif) !important;
        font-size: 1.15rem !important;
        font-weight: 400 !important;
        color: var(--text) !important;
    }
    .stCaption p {
        color: var(--text-3) !important;
        font-size: 0.77rem !important;
    }
    /* Make sure generic <p> inside stMarkdown in main area is readable */
    .main .stMarkdown p { color: var(--text-2) !important; }

    /* ── Custom components ─────────────────────────────────────── */
    .section-label {
        font-family: var(--mono);
        font-size: 0.66rem;
        letter-spacing: 0.16em;
        text-transform: uppercase;
        color: var(--text-3);
        border-top: 1px solid var(--border);
        padding-top: 1.1rem;
        margin: 1.5rem 0 0.8rem;
    }

    .verdict-card {
        background: var(--bg-2);
        border: 1px solid var(--border);
        border-left: 3px solid var(--border-2);
        border-radius: var(--r);
        padding: 1.4rem 1.6rem;
        margin-bottom: 1.5rem;
    }
    .verdict-card.pass   { border-left-color: var(--pass); }
    .verdict-card.revise { border-left-color: var(--revise); }
    .verdict-card.fail   { border-left-color: var(--fail); }
    .verdict-row {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        margin-bottom: 0.85rem;
        flex-wrap: wrap;
    }
    .verdict-label {
        font-family: var(--mono);
        font-size: 0.68rem;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        padding: 0.25rem 0.65rem;
        border-radius: 3px;
        font-weight: 500;
    }
    .verdict-label.pass   { background: var(--pass-bg);   color: var(--pass-text); }
    .verdict-label.revise { background: var(--revise-bg); color: var(--revise-text); }
    .verdict-label.fail   { background: var(--fail-bg);   color: var(--fail-text); }
    .verdict-chip {
        font-family: var(--mono);
        font-size: 0.68rem;
        letter-spacing: 0.06em;
        color: var(--text-3);
        padding: 0.25rem 0.65rem;
        border: 1px solid var(--border);
        border-radius: 3px;
    }
    .verdict-title {
        font-family: var(--serif);
        font-size: 1.1rem;
        font-style: italic;
        color: var(--text);
        margin-bottom: 0.5rem;
    }
    .verdict-summary {
        font-size: 0.88rem;
        color: var(--text-2);
        line-height: 1.7;
        font-weight: 300;
    }

    .analyst-card {
        background: var(--bg-2);
        border: 1px solid var(--border);
        border-radius: var(--r);
        padding: 1.2rem 1.3rem;
        margin-bottom: 0.9rem;
    }
    .analyst-title {
        font-family: var(--mono);
        font-size: 0.65rem;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        color: var(--text-3);
        margin-bottom: 0.5rem;
    }
    .analyst-result {
        font-family: var(--serif);
        font-size: 1.8rem;
        color: var(--text);
        margin-bottom: 0.5rem;
        line-height: 1;
    }
    .analyst-divider { height: 1px; background: var(--border); margin: 0.65rem 0; }
    .analyst-notes {
        font-size: 0.84rem;
        color: var(--text-2);
        line-height: 1.65;
        font-weight: 300;
    }

    .finding-item {
        font-size: 0.87rem;
        color: var(--text-2);
        line-height: 1.65;
        margin: 0 0 0.4rem;
        padding-left: 0.9rem;
        border-left: 2px solid var(--border-2);
    }

    .fact-row {
        display: flex;
        gap: 0.75rem;
        align-items: flex-start;
        padding: 0.7rem 0;
        border-bottom: 1px solid var(--border);
    }
    .fact-icon {
        font-family: var(--mono);
        font-size: 0.8rem;
        color: var(--text-3);
        flex-shrink: 0;
        padding-top: 0.1rem;
        min-width: 1rem;
    }
    .fact-claim { font-size: 0.87rem; font-weight: 500; color: var(--text); margin-bottom: 0.2rem; }
    .fact-note  { font-size: 0.82rem; color: var(--text-3); font-weight: 300; }

    .timeline-wrap { padding: 0.2rem 0; }
    .timeline-item {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        padding: 0.3rem 0;
        font-family: var(--sans);
        font-size: 0.81rem;
        color: var(--text-3);
    }
    .timeline-item.done { color: var(--text-2); }
    .timeline-dot {
        width: 6px; height: 6px;
        border-radius: 50%;
        background: var(--bg-4);
        border: 1px solid var(--border-2);
        flex-shrink: 0;
    }
    .timeline-item.done .timeline-dot { background: var(--pass); border-color: var(--pass); }

    /* ── Hide Streamlit chrome ─────────────────────────────────── */
    #MainMenu, footer, .stDeployButton,
    [data-testid="stToolbar"] { display: none !important; }
    </style>

    <div class="masthead">
        <div class="masthead-left">
            <div class="masthead-kicker">LangGraph · Agentic Pipeline · v2</div>
            <h1 class="masthead-title">Avaliador</h1>
            <p class="masthead-desc">
                An agentic arXiv paper evaluator. Papers are scraped, decomposed,
                evaluated by specialist agents, grounded against related literature,
                and synthesised into a board-level judgement report.
            </p>
        </div>
        <div class="masthead-badge">
            REVIEW STAGES<br>
            <span>07</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.sidebar.title("Review Board")
for node in DISPLAY_ORDER:
    st.sidebar.markdown(f"**{NODE_LABELS[node]}**")
st.sidebar.caption(
    "The graph fans out specialist reviewers after decomposition, "
    "then a meta-reviewer and deterministic reporter assemble the final judgement packet."
)

example_papers = {
    "Mamba":                     "https://arxiv.org/abs/2312.00752",
    "Attention Is All You Need": "https://arxiv.org/abs/1706.03762",
    "LLaMA":                     "https://arxiv.org/abs/2302.13971",
}

if "example_url" not in st.session_state:
    st.session_state.example_url = ""

st.markdown('<div class="section-label">Quick load</div>', unsafe_allow_html=True)
sample_cols = st.columns(len(example_papers))
for col, (label, url) in zip(sample_cols, example_papers.items()):
    if col.button(label, use_container_width=True):
        st.session_state.example_url = url

with st.form("evaluation_form"):
    arxiv_url = st.text_input(
        "arXiv paper URL",
        value=st.session_state.example_url,
        placeholder="https://arxiv.org/abs/2312.00752",
        help="Paste an arXiv abs or pdf URL.",
    )
    submitted = st.form_submit_button(
        "Run Full Evaluation →",
        type="primary",
        use_container_width=True,
    )


def render_timeline_html(completed_nodes: list[str]) -> str:
    rows = []
    for node in DISPLAY_ORDER:
        done  = node in completed_nodes
        cls   = "timeline-item done" if done else "timeline-item"
        label = NODE_LABELS[node]
        rows.append(f'<div class="{cls}"><div class="timeline-dot"></div>{label}</div>')
    return f'<div class="timeline-wrap">{"".join(rows)}</div>'


def render_findings(items: list[str]) -> str:
    if not items:
        return '<p style="color:var(--text-3);font-size:0.84rem;">No items returned.</p>'
    return "".join(f'<p class="finding-item">{item}</p>' for item in items)


def render_related_work(results: list[dict]) -> None:
    if not results:
        st.info("No related-work results retrieved during novelty search.")
        return
    for item in results:
        title   = item.get("title", "Untitled paper")
        url     = item.get("url", "")
        summary = item.get("summary", "")
        meta    = " · ".join(v for v in [item.get("published", ""), item.get("authors", "")] if v)
        with st.expander(title, expanded=False):
            if url:
                st.markdown(f"[Open paper ↗]({url})")
            if meta:
                st.caption(meta)
            st.write(summary or "No summary available.")


if submitted and arxiv_url:
    progress_bar = st.progress(0)
    status_col, timeline_col = st.columns([2, 1])
    status_text  = status_col.empty()
    timeline_box = timeline_col.empty()
    completed_nodes: list[str] = []

    def on_step(node_name: str, _node_data: dict, _state: dict) -> None:
        if node_name not in completed_nodes:
            completed_nodes.append(node_name)
        pct = int(len(completed_nodes) / len(DISPLAY_ORDER) * 100)
        progress_bar.progress(pct)
        status_text.markdown(
            f'<p style="font-family:var(--mono);font-size:0.7rem;letter-spacing:0.12em;'
            f'text-transform:uppercase;color:var(--text-3);margin:0;">'
            f'Stage {len(completed_nodes)} / {len(DISPLAY_ORDER)}</p>'
            f'<p style="font-family:var(--serif);font-size:1.15rem;color:var(--text);margin:0.2rem 0 0;">'
            f'{NODE_LABELS.get(node_name, node_name)}</p>',
            unsafe_allow_html=True,
        )
        timeline_box.markdown(render_timeline_html(completed_nodes), unsafe_allow_html=True)

    final_state = run_evaluation(arxiv_url, on_step=on_step)
    progress_bar.progress(100)

    if final_state.get("error"):
        st.error(f"Evaluation failed: {final_state['error']}")
    else:
        saved_report_path = None
        save_error = None
        try:
            saved_report_path = save_evaluation_report(final_state)
        except Exception as exc:
            save_error = str(exc)

        verdict     = final_state.get("overall_verdict", "REVISE")
        verdict_cls = verdict.lower()
        verdict_labels = {"PASS": "✓ PASS", "REVISE": "◑ REVISE", "FAIL": "✕ FAIL"}

        if saved_report_path:
            st.success(f"Report saved locally: `{saved_report_path}`")
        elif save_error:
            st.warning(f"Evaluation completed, but local save failed: {save_error}")

        st.markdown(
            f"""
            <div class="verdict-card {verdict_cls}">
                <div class="verdict-row">
                    <span class="verdict-label {verdict_cls}">{verdict_labels.get(verdict, verdict)}</span>
                    <span class="verdict-chip">Confidence: {final_state.get("reviewer_confidence", "Medium")}</span>
                </div>
                <div class="verdict-title">{final_state.get("title", "Unknown Paper")}</div>
                <div class="verdict-summary">{final_state.get("executive_summary", "")}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Consistency",     f"{final_state.get('consistency_score', 0)}/100")
        m2.metric("Grammar",          final_state.get("grammar_rating", "N/A"))
        m3.metric("Novelty",          final_state.get("novelty_index", "N/A"))
        m4.metric("Fabrication Risk", f"{final_state.get('accuracy_score', 0.0):.1f}%")

        overview_tab, analysts_tab, evidence_tab, report_tab = st.tabs(
            ["Overview", "Analyst Board", "Evidence", "Report"]
        )

        with overview_tab:
            s_col, r_col = st.columns(2)
            with s_col:
                st.markdown('<div class="section-label">Strengths</div>', unsafe_allow_html=True)
                st.markdown(render_findings(final_state.get("strengths", [])), unsafe_allow_html=True)
            with r_col:
                st.markdown('<div class="section-label">Risks</div>', unsafe_allow_html=True)
                st.markdown(render_findings(final_state.get("risks", [])), unsafe_allow_html=True)
            st.markdown('<div class="section-label">Recommendations</div>', unsafe_allow_html=True)
            st.markdown(render_findings(final_state.get("recommendations", [])), unsafe_allow_html=True)

        with analysts_tab:
            analyst_specs = [
                ("Consistency Review",  f"{final_state.get('consistency_score', 0)}/100",  final_state.get("consistency_notes", "")),
                ("Language Review",      final_state.get("grammar_rating", "N/A"),           final_state.get("grammar_notes", "")),
                ("Novelty Review",       final_state.get("novelty_index", "N/A"),             final_state.get("novelty_notes", "")),
                ("Authenticity Audit",  f"{final_state.get('accuracy_score', 0.0):.1f}%",   final_state.get("accuracy_notes", "")),
            ]
            a1, a2 = st.columns(2)
            col_cycle = [a1, a2, a1, a2]
            for col, (title, result, notes) in zip(col_cycle, analyst_specs):
                with col:
                    st.markdown(
                        f"""
                        <div class="analyst-card">
                            <div class="analyst-title">{title}</div>
                            <div class="analyst-result">{result}</div>
                            <div class="analyst-divider"></div>
                            <div class="analyst-notes">{notes}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

            st.markdown('<div class="section-label">Fact Check Log</div>', unsafe_allow_html=True)
            fact_items = final_state.get("fact_check_log", [])
            if fact_items:
                icons = {"verified": "✓", "plausible": "◑", "unverified": "?", "suspicious": "!"}
                for item in fact_items:
                    icon = icons.get(item.get("status", ""), "?")
                    st.markdown(
                        f"""
                        <div class="fact-row">
                            <div class="fact-icon">{icon}</div>
                            <div>
                                <div class="fact-claim">{item.get("claim", "")}</div>
                                <div class="fact-note">{item.get("note", "")}</div>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
            else:
                st.info("No fact checks returned.")

        with evidence_tab:
            st.markdown('<div class="section-label">Extracted Sections</div>', unsafe_allow_html=True)
            for key in ["abstract", "methodology", "results", "conclusion"]:
                with st.expander(key.capitalize(), expanded=(key == "abstract")):
                    st.write(final_state.get("sections", {}).get(key, "No content extracted."))

            st.markdown('<div class="section-label">Related Literature</div>', unsafe_allow_html=True)
            render_related_work(final_state.get("novelty_search_results", []))

        with report_tab:
            report = final_state.get("final_report", "")
            if report:
                st.markdown(report)
                st.download_button(
                    label="↓ Markdown Report",
                    data=report,
                    file_name="judgement_report.md",
                    mime="text/markdown",
                    use_container_width=True,
                )
            else:
                st.warning("The reporter did not return a final report.")
