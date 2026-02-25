"""Reviewer Agent: Checks completeness and generates follow-up questions."""

import google.generativeai as genai
from .config import GEMINI_API_KEY, GEMINI_MODEL, DATA_DIR, OUTPUT_DIR, token_tracker

SYSTEM_PROMPT = """당신은 Candid Courage Fund 지원서 리뷰어입니다.
Copywriter가 작성한 Life Deck 초안을 CCF 가이드라인 기준으로 검토하고,
부족한 부분을 식별하여 지원자에게 추가 질문을 제시합니다.

## 역할
1. CCF의 4개 질문 기준으로 초안의 완성도를 평가
2. 제공된 정보로 커버되지 않는 영역을 식별
3. 지원자에게 직접 물어볼 추가 질문을 생성
4. 초안의 개선 방향을 제시

## 평가 기준
각 질문(Q1-Q4)에 대해 아래를 평가:
- 진정성: 솔직하고 진심이 느껴지는가?
- 구체성: 추상적이지 않고 구체적인 사례가 있는가?
- 설득력: 읽는 사람이 공감하고 이 사람에게 투자하고 싶어지는가?
- 차별화: 다른 지원자와 구별되는 고유한 이야기가 있는가?
- 일관성: 4개 섹션이 하나의 이야기로 연결되는가?

## 출력 형식
Markdown으로 작성합니다.

### 완성도 평가
- 전체 점수: X/100
- Q1 점수: X/100 (한 줄 평가)
- Q2 점수: X/100 (한 줄 평가)
- Q3 점수: X/100 (한 줄 평가)
- Q4 점수: X/100 (한 줄 평가)

### 잘 된 부분
- 구체적으로 어떤 부분이 잘 되었는지

### 부족한 부분
- 구체적으로 어떤 정보가 부족한지
- 왜 그 정보가 필요한지

### 지원자에게 할 추가 질문
우선순위별로 정리합니다:

#### 필수 질문 (이 정보 없이는 완성도가 크게 떨어짐)
각 질문에 대해:
- **질문**: (구체적인 질문)
- **맥락**: (왜 이 질문이 필요한지)
- **활용 섹션**: (Q1/Q2/Q3/Q4 중 어디에 활용될지)

#### 권장 질문 (있으면 훨씬 좋아지는 정보)
(동일 형식)

#### 선택 질문 (있으면 플러스알파)
(동일 형식)

### 개선 방향 제안
- 전체적인 톤/구조 관련 개선 방향
- 특정 섹션의 구체적 개선 포인트

## 리뷰 원칙
1. CCF의 핵심 가치인 "사람을 본다"에 맞게 평가하라
2. 추가 질문은 지원자가 쉽게 답할 수 있는 구체적인 형태로 작성하라
3. "더 좋은 글"이 아니라 "더 진정성 있는 글"을 위한 피드백을 주라
4. 지원자의 화법과 스타일을 존중하면서 개선점을 제시하라
"""


class ReviewerAgent:
    """Reviews the Life Deck draft and generates follow-up questions."""

    def __init__(self):
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel(
            model_name=GEMINI_MODEL,
            system_instruction=SYSTEM_PROMPT,
        )

    def run(self, life_deck_draft: str) -> str:
        """Execute the reviewer agent."""
        print("\n[Reviewer] Life Deck 초안 리뷰 중...")

        ccf_guide = (DATA_DIR / "ccf_guidelines.md").read_text(encoding="utf-8")
        raw_input = (DATA_DIR / "raw_input.md").read_text(encoding="utf-8")

        prompt = f"""아래는 Copywriter가 작성한 Life Deck 초안, CCF 가이드라인, 그리고 원본 입력 데이터입니다.

## Life Deck 초안
{life_deck_draft}

## CCF 가이드라인
{ccf_guide}

## 원본 입력 데이터
{raw_input}

위 초안을 CCF 가이드라인 기준으로 검토하세요.

핵심 체크포인트:
1. 원본 데이터에 있는 중요한 내용이 초안에서 빠지지 않았는가?
2. CCF의 4개 질문에 충분히 답하고 있는가?
3. 지원자(Jamie)가 제공한 정보만으로 커버되지 않는 영역은 무엇인가?
4. 특히 개인적/감정적 깊이가 필요한 부분에서 추가 정보가 필요하지 않은가?
5. "왜 창업인가", "왜 지금인가", "자금 구체적 활용 계획" 등이 충분한가?

추가 질문은 지원자가 쉽게 답할 수 있는 구체적이고 친절한 형태로 작성하세요.
"""

        response = self.model.generate_content(prompt)

        if response.usage_metadata:
            token_tracker.log(
                "Reviewer",
                response.usage_metadata.prompt_token_count or 0,
                response.usage_metadata.candidates_token_count or 0,
            )

        result = response.text
        output_path = OUTPUT_DIR / "review_feedback.md"
        output_path.write_text(result, encoding="utf-8")
        print(f"[Reviewer] 리뷰 완료 -> {output_path}")
        return result
