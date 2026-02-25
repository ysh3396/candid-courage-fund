"""Configuration for the Life Deck agent pipeline."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from project root, fallback to shorts-generator .env
PROJECT_ROOT = Path(__file__).parent.parent
SHORTS_GEN_ENV = (
    PROJECT_ROOT.parent / "shorts-generator" / "gukppong-shorts-maker" / ".env"
)

# Try project .env first, then shorts-generator .env
if (PROJECT_ROOT / ".env").exists():
    load_dotenv(PROJECT_ROOT / ".env")
elif SHORTS_GEN_ENV.exists():
    load_dotenv(SHORTS_GEN_ENV)

# Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = "gemini-2.5-pro"

# Paths
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "output"

# Ensure output directory exists
OUTPUT_DIR.mkdir(exist_ok=True)


# Token tracking
class TokenTracker:
    """Tracks API usage across all agents."""

    def __init__(self):
        self.calls = []

    def log(self, agent_name: str, input_tokens: int, output_tokens: int):
        self.calls.append(
            {
                "agent": agent_name,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
            }
        )

    def summary(self) -> str:
        total_input = sum(c["input_tokens"] for c in self.calls)
        total_output = sum(c["output_tokens"] for c in self.calls)
        lines = [
            f"\n{'=' * 50}",
            f"  API Usage Summary",
            f"{'=' * 50}",
        ]
        for call in self.calls:
            lines.append(
                f"  {call['agent']:20s} | in: {call['input_tokens']:>8,} | out: {call['output_tokens']:>8,}"
            )
        lines.append(f"{'─' * 50}")
        lines.append(
            f"  {'TOTAL':20s} | in: {total_input:>8,} | out: {total_output:>8,}"
        )
        lines.append(f"{'=' * 50}")
        return "\n".join(lines)


# Global tracker
token_tracker = TokenTracker()
