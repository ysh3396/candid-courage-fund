"""Copywriter Agent: Writes the Life Deck draft in Jamie's voice."""

import google.generativeai as genai
from .config import GEMINI_API_KEY, GEMINI_MODEL, DATA_DIR, OUTPUT_DIR, token_tracker

SYSTEM_PROMPT = """당신은 Jamie Yang(양승현)의 전담 카피라이터입니다.
Consultant가 구성한 전략적 프레이밍을 바탕으로, Jamie의 고유한 화법과 문체로 Life Deck을 작성합니다.

## Jamie의 화법 특징 (반드시 따를 것)

1. **"~인 것 같다" 톤**: 겸손하면서도 확신이 있는 특유의 어미. 단정적이지 않지만 진심이 느껴지는 톤.
   - 예: "세상을 바꾸는 것은 3가지로 결정되는 것 같다"
   - 예: "난 오히려 그런 집단에 속해 있을 때 행복함을 느끼는 것 같다"

2. **"뜬금없고 웃길 수 있겠지만" 패턴**: 큰 포부를 말할 때 선제적으로 방어한 후 진심을 드러내는 방식.
   - 예: "뜬금없고 웃길 수 있겠지만, 언젠가 세상을 바꾸고 싶다"

3. **숫자로 증명**: 주장만 하지 않고, 구체적 수치로 뒷받침.
   - 예: "Paying User 327% 성장", "배달 지연율 5% → 1%"

4. **짧은 문장 + 글머리 기호**: 핵심을 간결하게 전달. 긴 서술보다 구조화.

5. **3가지 구조화**: 주장을 3개 항목으로 정리하는 습관.
   - 예: "1) 좋은 제품으로 2) 많은 사람들에게 3) 긍정적인 영향력을 끼친다"

6. **주변 감사**: 글의 시작이나 끝에 동료/친구/가족에게 감사를 자연스럽게 표현.

7. **솔직한 실패 인정**: 실패를 숨기지 않고, 그로부터 배운 것을 강조.
   - 예: "내가 떠난 후 해지율 1% → 5% 상승. 나 없이도 돌아가는 시스템을 만드는 것이 PO의 역량"

8. **화학 비유**: 화학 전공 배경을 자연스럽게 녹이는 비유.
   - 예: "활성화 에너지", "화학적 반응"

9. **반복되는 핵심 메시지**: "세상을 바꾸고 싶다"를 여러 맥락에서 변주하며 반복.

10. **미래의 나에게**: "X년 뒤에 기다리고 있을 낯선 나를 아무 아쉬움 없이 맞이할 수 있기를"

## 출력 형식
Markdown으로 작성합니다. 각 섹션을 명확히 구분하세요.

```
# [CCF] Jamie Yang_Life Deck

## HERO
- name: (이름)
- tagline: (한 줄 태그라인)
- quote: (대표 인용구)

## 01. 나는 누구인가
(본문 작성)

## 02. 어떻게 살아왔는가
(본문 작성 - 타임라인 형식 + 내러티브 혼합)

## 03. 어떻게 살 것인가
(본문 작성)

## 04. 용기자금이 필요한 이유
(본문 작성)

## CLOSING
(마무리 문장)
```

## 작성 원칙
1. Jamie의 실제 글에서 사용한 표현과 문체를 최대한 살려라
2. 과도한 미사여구나 형용사 남발은 Jamie 스타일이 아니다 - 담백하게
3. CCF는 "사람"을 보므로, 실적 나열보다 인간적 이야기가 우선
4. 각 섹션의 분량은 자유이지만, 읽는 사람이 지루하지 않을 정도로
5. 추천사를 직접 인용할 때는 자연스럽게 녹여라 (인용구 형태)
6. 한국어로 작성하되, Jamie가 영어를 섞어 쓰는 습관도 반영
"""


class CopywriterAgent:
    """Writes the Life Deck draft in Jamie's authentic voice."""

    def __init__(self):
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel(
            model_name=GEMINI_MODEL,
            system_instruction=SYSTEM_PROMPT,
        )

    def run(self, consultant_framing: str) -> str:
        """Execute the copywriter agent."""
        print("\n[Copywriter] Jamie 화법으로 Life Deck 초안 작성 중...")

        writing_samples = (DATA_DIR / "writing_samples.md").read_text(encoding="utf-8")
        raw_input = (DATA_DIR / "raw_input.md").read_text(encoding="utf-8")

        prompt = f"""아래는 Consultant가 구성한 전략적 프레이밍, Jamie의 실제 글쓰기 샘플, 그리고 원본 데이터입니다.

## Consultant 전략 프레이밍
{consultant_framing}

## Jamie의 글쓰기 샘플 (화법 레퍼런스)
{writing_samples}

## Jamie 원본 데이터
{raw_input}

위 자료를 바탕으로, Jamie의 화법과 문체로 Candid Courage Fund Life Deck 초안을 작성하세요.

핵심 지침:
1. Jamie가 직접 쓴 것처럼 느껴져야 합니다 - 샘플의 톤과 문체를 철저히 모방하세요
2. Consultant의 전략적 프레이밍을 따르되, Jamie의 언어로 풀어내세요
3. 숫자와 구체적 사례를 적절히 배치하되, 나열식이 되지 않도록 하세요
4. 각 섹션은 독립적으로 읽혀도 좋지만, 전체가 하나의 이야기로 연결되어야 합니다
5. "활성화 에너지" 비유를 Q4에서 자연스럽고 강력하게 사용하세요
6. 과도한 포장 금지 - Jamie는 솔직하고 담백한 사람입니다

필수 반영 사항 (절대 빠뜨리지 마세요):
7. Q3에 관심 분야(건강/컨텐츠)를 반드시 포함하세요. 원본 데이터의 "인간의 시간이 효율적으로 쓰이는 방향으로 기술이 발달한다"는 명제와 건강(온디바이스 AI 건강수명 예측), 컨텐츠(Contents Acquisition Cost를 낮추는 AI 도구 = Claude Code for Creator) 관심 분야를 구체적으로 녹여내세요.
8. Q2에서 좌천 당시 "이대로 포기할까" 생각했지만 포기하지 않았다는 감정적 순간을 반드시 포함하세요.
9. Q4에서 자금 활용 계획을 구체적으로 포함하세요: 사무실/기기는 이미 보유, 자금 대부분은 AI API 비용(LLM, 클라우드 인프라)에 사용, 프로토타입 빠르게 만들고 검증하는 데 활용.
10. Q1에서 세상을 바꾸고 싶은 이유의 이상적/현실적 양면을 솔직하게 드러내세요.
"""

        response = self.model.generate_content(prompt)

        if response.usage_metadata:
            token_tracker.log(
                "Copywriter",
                response.usage_metadata.prompt_token_count or 0,
                response.usage_metadata.candidates_token_count or 0,
            )

        result = response.text
        output_path = OUTPUT_DIR / "life_deck_draft.md"
        output_path.write_text(result, encoding="utf-8")
        print(f"[Copywriter] 초안 작성 완료 -> {output_path}")
        return result
