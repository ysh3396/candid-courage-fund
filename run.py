#!/usr/bin/env python3
"""CLI entry point for the Life Deck 4-Agent Pipeline."""

import argparse
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from agents.pipeline import LifeDeckPipeline
from agents.config import GEMINI_API_KEY, OUTPUT_DIR


def main():
    parser = argparse.ArgumentParser(
        description="Candid Courage Fund - Life Deck 4-Agent Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run.py                    # Run full pipeline
  python run.py --agent researcher # Run only researcher agent
  python run.py --agent reviewer   # Re-run reviewer on existing draft
        """,
    )
    parser.add_argument(
        "--agent",
        choices=["researcher", "consultant", "copywriter", "reviewer"],
        help="Run a specific agent instead of the full pipeline",
    )
    args = parser.parse_args()

    # Check API key
    if not GEMINI_API_KEY:
        print("ERROR: GEMINI_API_KEY not found.")
        print("Set it in .env file or as environment variable.")
        sys.exit(1)

    pipeline = LifeDeckPipeline()

    if args.agent:
        # Run single agent
        print(f"\nRunning single agent: {args.agent}")
        kwargs = {}

        # Load previous outputs if needed
        if args.agent == "consultant":
            research_path = OUTPUT_DIR / "research_analysis.md"
            if research_path.exists():
                kwargs["research"] = research_path.read_text(encoding="utf-8")
            else:
                print("ERROR: research_analysis.md not found. Run researcher first.")
                sys.exit(1)

        elif args.agent == "copywriter":
            framing_path = OUTPUT_DIR / "consultant_framing.md"
            if framing_path.exists():
                kwargs["framing"] = framing_path.read_text(encoding="utf-8")
            else:
                print("ERROR: consultant_framing.md not found. Run consultant first.")
                sys.exit(1)

        elif args.agent == "reviewer":
            draft_path = OUTPUT_DIR / "life_deck_draft.md"
            if draft_path.exists():
                kwargs["draft"] = draft_path.read_text(encoding="utf-8")
            else:
                print("ERROR: life_deck_draft.md not found. Run copywriter first.")
                sys.exit(1)

        pipeline.run_single(args.agent, **kwargs)
    else:
        # Run full pipeline
        pipeline.run()


if __name__ == "__main__":
    main()
