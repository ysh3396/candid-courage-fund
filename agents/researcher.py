"""Researcher Agent: Analyzes life data and structures it for the pipeline."""

import google.generativeai as genai
from .config import GEMINI_API_KEY, GEMINI_MODEL, DATA_DIR, OUTPUT_DIR, token_tracker

SYSTEM_PROMPT = """당신은 인생 분석 리서처입니다. 지원자의 인생 데이터를 깊이 분석하여 구조화된 인사이트를 도출합니다.

## 역할
- 지원자의 인생 이야기, 이력서, 포트폴리오를 종합 분석
- 반복되는 패턴, 가치관, 성장 궤적을 식별
- 실패와 회복의 사이클을 깊이 있게 분석
- Candid Courage Fund의 4개 질문에 매핑 가능한 소재를 태깅

## 출력 형식
아래 구조로 한국어로 분석 결과를 작성하세요. Markdown 형식으로 작성합니다.

### 1. 정체성 키워드 (Identity Keywords)
이 사람을 정의하는 5-7개 핵심 키워드와 각각에 대한 근거

### 2. 인생 테마 (Life Themes)
반복적으로 나타나는 3-5개 패턴/테마. 각 테마에 대해:
- 테마 이름
- 발현된 구체적 사례들
- 이 테마가 의미하는 것

### 3. 타임라인 (Timeline)
시간순으로 정리한 핵심 사건들. 각 사건에 대해:
- 시기
- 사건
- 의미/중요성
- 카테고리 (실패/회복/성장/전환점)

### 4. 가치관 (Values)
핵심 가치관 목록과 이를 뒷받침하는 행동/발언 근거

### 5. 강점 분석 (Strengths)
데이터로 증명된 강점들 (수치 포함)

### 6. 실패-회복 사이클 (Failure-Recovery Cycles)
가장 인상적인 실패와 회복 사례 3-5개. 각각에 대해:
- 실패 상황
- 핵심 원인
- 회복 과정
- 배운 교훈
- 이후 변화

### 7. CCF 질문 매핑 (CCF Question Mapping)
Candid Courage Fund의 4개 질문 각각에 활용할 수 있는 소재 태깅:
- Q1 (나는 누구인가): 활용 가능한 소재들
- Q2 (어떻게 살아왔는가): 활용 가능한 소재들
- Q3 (어떻게 살 것인가): 활용 가능한 소재들
- Q4 (용기자금이 필요한 이유): 활용 가능한 소재들

## 분석 원칙
1. 표면적 사실이 아닌, 그 뒤에 숨겨진 동기와 패턴을 파악하라
2. 숫자로 증명된 성과는 반드시 포함하라
3. 실패를 숨기지 말고, 실패에서 배운 것을 강조하라
4. 추천사에서 나오는 타인의 시선도 분석에 포함하라
5. 화학 전공 → IT 창업이라는 전환의 의미를 깊이 분석하라
"""


class ResearcherAgent:
    """Analyzes life data and produces structured insights."""

    def __init__(self):
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel(
            model_name=GEMINI_MODEL,
            system_instruction=SYSTEM_PROMPT,
        )

    def _load_data(self) -> str:
        """Load all input data files."""
        raw_input = (DATA_DIR / "raw_input.md").read_text(encoding="utf-8")
        portfolio = (DATA_DIR / "portfolio_summary.md").read_text(encoding="utf-8")
        ccf_guide = (DATA_DIR / "ccf_guidelines.md").read_text(encoding="utf-8")
        return f"""## 원본 입력 데이터
{raw_input}

## 포트폴리오 요약
{portfolio}

## CCF 가이드라인
{ccf_guide}
"""

    def run(self) -> str:
        """Execute the researcher agent and return analysis."""
        print("\n[Researcher] 인생 데이터 분석 중...")
        data = self._load_data()

        prompt = f"""아래 데이터를 분석하여 구조화된 인생 분석 리포트를 작성해주세요.

{data}

위 데이터를 기반으로 시스템 프롬프트에 명시된 형식대로 깊이 있는 분석을 수행하세요.
특히 이 사람의 '왜'에 집중하세요 - 왜 이런 선택을 했는지, 왜 이런 패턴이 반복되는지.
"""

        response = self.model.generate_content(prompt)

        # Track tokens
        if response.usage_metadata:
            token_tracker.log(
                "Researcher",
                response.usage_metadata.prompt_token_count or 0,
                response.usage_metadata.candidates_token_count or 0,
            )

        result = response.text
        # Save output
        output_path = OUTPUT_DIR / "research_analysis.md"
        output_path.write_text(result, encoding="utf-8")
        print(f"[Researcher] 분석 완료 -> {output_path}")
        return result
