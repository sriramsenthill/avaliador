from pathlib import Path
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parent / ".env", override=True)

import sys
from src.graph import build_graph

def run_evaluation(arxiv_url: str):
    print(f"\n🔬 Starting evaluation for: {arxiv_url}\n")
    app = build_graph()

    initial_state = {
        "arxiv_url": arxiv_url,
        "raw_text": "", "title": "", "sections": {},
        "consistency_score": 0, "consistency_notes": "",
        "grammar_rating": "", "grammar_notes": "",
        "novelty_index": "", "novelty_notes": "",
        "fact_check_log": [], "accuracy_score": 0.0,
        "accuracy_notes": "", "final_report": "", "error": None,
    }

    print("⏳ Running pipeline... (this takes 30-60 seconds)\n")

    # Stream with live node progress
    final_state = initial_state.copy()
    for step in app.stream(initial_state):
        node_name = list(step.keys())[0]
        node_data = step[node_name]
        final_state.update(node_data)
        print(f"  ✅ Completed: {node_name}")

    print("\n" + "=" * 60)

    if final_state.get("error"):
        print(f"❌ Error: {final_state['error']}")
        sys.exit(1)

    print(f"📄 Paper: {final_state.get('title', 'Unknown')}")
    print(f"📊 Consistency: {final_state.get('consistency_score')}/100")
    print(f"📝 Grammar: {final_state.get('grammar_rating')}")
    print(f"💡 Novelty: {final_state.get('novelty_index')}")
    print(f"🔍 Fabrication Risk: {final_state.get('accuracy_score'):.1f}%")
    print("=" * 60 + "\n")

    report = final_state.get("final_report", "")
    if report:
        print(report)
        with open("judgement_report.md", "w") as f:
            f.write(report)
        print(f"\n✅ Report saved to judgement_report.md")
    else:
        print("⚠️  Reporter returned empty. Raw state dump:")
        for k, v in final_state.items():
            if k not in ("raw_text",):
                print(f"  {k}: {str(v)[:200]}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <arxiv_url>")
        sys.exit(1)
    run_evaluation(sys.argv[1])