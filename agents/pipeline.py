"""Pipeline orchestrator: runs 4 agents sequentially."""

import time
from .researcher import ResearcherAgent
from .consultant import ConsultantAgent
from .copywriter import CopywriterAgent
from .reviewer import ReviewerAgent
from .config import token_tracker, OUTPUT_DIR


class LifeDeckPipeline:
    """Orchestrates the 4-agent Life Deck generation pipeline."""

    def __init__(self):
        self.researcher = ResearcherAgent()
        self.consultant = ConsultantAgent()
        self.copywriter = CopywriterAgent()
        self.reviewer = ReviewerAgent()

    def run(self) -> dict[str, str]:
        """Run the full pipeline: Researcher -> Consultant -> Copywriter -> Reviewer."""
        start_time = time.time()

        print("=" * 60)
        print("  Candid Courage Fund - Life Deck Pipeline")
        print("  4-Agent System: Researcher -> Consultant -> Copywriter -> Reviewer")
        print("=" * 60)

        # Step 1: Researcher
        print(f"\n{'─' * 60}")
        print("  STEP 1/4: Researcher (인생 데이터 분석)")
        print(f"{'─' * 60}")
        research_analysis = self.researcher.run()

        # Step 2: Consultant
        print(f"\n{'─' * 60}")
        print("  STEP 2/4: Consultant (전략적 프레이밍)")
        print(f"{'─' * 60}")
        consultant_framing = self.consultant.run(research_analysis)

        # Step 3: Copywriter
        print(f"\n{'─' * 60}")
        print("  STEP 3/4: Copywriter (Jamie 화법으로 초안 작성)")
        print(f"{'─' * 60}")
        life_deck_draft = self.copywriter.run(consultant_framing)

        # Step 4: Reviewer
        print(f"\n{'─' * 60}")
        print("  STEP 4/4: Reviewer (리뷰 + 추가 질문)")
        print(f"{'─' * 60}")
        review_feedback = self.reviewer.run(life_deck_draft)

        elapsed = time.time() - start_time

        # Summary
        print(f"\n{'=' * 60}")
        print(f"  Pipeline 완료! ({elapsed:.1f}초)")
        print(f"{'=' * 60}")
        print(f"\n  출력 파일:")
        print(f"  1. {OUTPUT_DIR / 'research_analysis.md'}")
        print(f"  2. {OUTPUT_DIR / 'consultant_framing.md'}")
        print(f"  3. {OUTPUT_DIR / 'life_deck_draft.md'}  <-- Life Deck 초안")
        print(f"  4. {OUTPUT_DIR / 'review_feedback.md'}  <-- 리뷰 + 추가 질문")
        print(token_tracker.summary())

        return {
            "research": research_analysis,
            "framing": consultant_framing,
            "draft": life_deck_draft,
            "review": review_feedback,
        }

    def run_single(self, agent_name: str, **kwargs) -> str:
        """Run a single agent for testing or iteration."""
        agents = {
            "researcher": lambda: self.researcher.run(),
            "consultant": lambda: self.consultant.run(kwargs.get("research", "")),
            "copywriter": lambda: self.copywriter.run(kwargs.get("framing", "")),
            "reviewer": lambda: self.reviewer.run(kwargs.get("draft", "")),
        }
        if agent_name not in agents:
            raise ValueError(
                f"Unknown agent: {agent_name}. Choose from {list(agents.keys())}"
            )
        return agents[agent_name]()
