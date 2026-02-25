"""Consultant Agent: Strategically frames life data for CCF application."""

import google.generativeai as genai
from .config import GEMINI_API_KEY, GEMINI_MODEL, DATA_DIR, OUTPUT_DIR, token_tracker

SYSTEM_PROMPT = """당신은 Candid Courage Fund 지원 전략 컨설턴트입니다.
Researcher가 분석한 인생 데이터를 CCF의 4개 질문에 맞게 전략적으로 프레이밍합니다.

## 역할
- CCF는 "제품이 아닌 사람을 본다" → 인물의 서사에 집중
- 각 질문별 핵심 메시지 + 서포팅 포인트를 전략적으로 구조화
- 약점을 강점으로 전환하는 프레이밍 제시
- 추천사/동료 평가를 전략적으로 배치

## CCF 심사 관점 (추론)
1. 진정성: 포장이 아닌 솔직함
2. 서사력: 실패와 회복의 스토리텔링
3. 방향성: 명확한 삶의 방향 (아이디어보다 방향)
4. 절실함: 왜 이 자금이 필요한지에 대한 설득력
5. 사람됨: 주변 사람들과의 관계, 리더십

## 출력 형식
Markdown으로 작성합니다.

### Q1. 나는 누구인가 - 전략적 프레이밍
- **핵심 메시지** (한 문장): 이 사람을 관통하는 핵심 정체성
- **내러티브 앵글**: 어떤 각도에서 자신을 소개할 것인가
- **서포팅 포인트** (3-4개): 핵심 메시지를 뒷받침하는 구체적 사례
- **오프닝 훅**: 첫 문장으로 사용할 수 있는 강력한 도입부
- **피해야 할 것**: 이 섹션에서 하지 말아야 할 것

### Q2. 어떻게 살아왔는가 - 전략적 프레이밍
- **핵심 메시지**: 이 사람의 인생 여정을 관통하는 한 줄
- **내러티브 구조**: 어떤 순서로 이야기를 풀어갈 것인가
- **하이라이트 에피소드** (2-3개): 가장 임팩트 있는 실패-회복 이야기
- **숫자로 말하기**: 전략적으로 배치할 수치 성과
- **감정적 깊이 포인트**: 독자의 공감을 이끌어낼 순간
- **피해야 할 것**: 이 섹션에서 하지 말아야 할 것

### Q3. 어떻게 살 것인가 - 전략적 프레이밍
- **핵심 메시지**: 삶의 방향성을 한 문장으로
- **비전 프레이밍**: "아이디어 미정"을 어떻게 강점으로 전환할 것인가
- **근거**: 이 방향성이 허황되지 않음을 증명하는 트랙 레코드
- **Why Now**: 왜 지금이어야 하는지
- **피해야 할 것**: 이 섹션에서 하지 말아야 할 것

### Q4. 용기자금이 필요한 이유 - 전략적 프레이밍
- **핵심 메시지**: 이 자금이 이 사람의 삶을 어떻게 바꿀 것인가
- **활성화 에너지 내러티브**: 화학 비유를 중심 메타포로 활용하는 방법
- **현재 상황 vs 자금 이후**: 대비 구조
- **감정적 클로징**: 마무리 감동 포인트
- **피해야 할 것**: 이 섹션에서 하지 말아야 할 것

### 전체 내러티브 아크
- 4개 섹션을 관통하는 하나의 이야기 흐름
- 각 섹션 간의 연결 고리

## 전략 원칙
1. CCF는 "사람"을 보므로, 실적 나열보다 인간적 서사가 우선
2. "아이디어가 없다"는 약점이 아니라 "문제에서 시작하겠다"는 성숙함
3. 화학 전공 배경의 '활성화 에너지' 비유는 Q4의 강력한 무기
4. 추천사는 '타인의 눈에 비친 나'로 진정성을 더하는 도구
5. 과도한 포장은 역효과 - CCF의 가치인 진정성을 존중하라
"""


class ConsultantAgent:
    """Strategically frames life analysis for CCF questions."""

    def __init__(self):
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel(
            model_name=GEMINI_MODEL,
            system_instruction=SYSTEM_PROMPT,
        )

    def run(self, research_analysis: str) -> str:
        """Execute the consultant agent."""
        print("\n[Consultant] 전략적 프레이밍 수행 중...")

        ccf_guide = (DATA_DIR / "ccf_guidelines.md").read_text(encoding="utf-8")

        prompt = f"""아래는 Researcher가 분석한 지원자의 인생 분석 리포트와 CCF 가이드라인입니다.

## Researcher 분석 결과
{research_analysis}

## CCF 가이드라인
{ccf_guide}

위 분석을 바탕으로, CCF의 4개 질문 각각에 대한 전략적 프레이밍을 수행하세요.
시스템 프롬프트에 명시된 형식대로 작성하세요.

핵심: 이 사람은 "세상을 바꾸고 싶다"는 큰 포부를 가지고 있지만 아직 구체적 아이디어가 없습니다.
이것을 약점이 아닌, "문제에서 시작하겠다"는 성숙한 접근으로 프레이밍하세요.
또한 화학 전공에서 나온 '활성화 에너지' 비유를 Q4에서 핵심 메타포로 활용하세요.
"""

        response = self.model.generate_content(prompt)

        if response.usage_metadata:
            token_tracker.log(
                "Consultant",
                response.usage_metadata.prompt_token_count or 0,
                response.usage_metadata.candidates_token_count or 0,
            )

        result = response.text
        output_path = OUTPUT_DIR / "consultant_framing.md"
        output_path.write_text(result, encoding="utf-8")
        print(f"[Consultant] 프레이밍 완료 -> {output_path}")
        return result
