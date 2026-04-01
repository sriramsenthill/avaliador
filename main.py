"""CLI entrypoint that runs the same pipeline as the Streamlit UI."""

from pathlib import Path
from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parent / ".env", override=True)

import sys
from src.service import run_evaluation, save_evaluation_report

def run_cli(arxiv_url: str):
    print(f"\n🔬 Starting evaluation for: {arxiv_url}\n")
    print("⏳ Running pipeline... (this takes 30-60 seconds)\n")

    def on_step(node_name: str, _node_data: dict, _state: dict) -> None:
        print(f"  ✅ Completed: {node_name}")

    final_state = run_evaluation(arxiv_url, on_step=on_step)

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
        report_path = save_evaluation_report(final_state)
        print(f"\n✅ Report saved to {report_path}")
    else:
        print("⚠️  Reporter returned empty. Raw state dump:")
        for k, v in final_state.items():
            if k not in ("raw_text",):
                print(f"  {k}: {str(v)[:200]}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <arxiv_url>")
        sys.exit(1)
    run_cli(sys.argv[1])
