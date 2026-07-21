---
title: AI 개인 지식관리
created: 2026-07-21
updated: 2026-07-21
type: concept
tags:
  - knowledge-base
  - knowledge-graph
  - pkm
  - provenance
  - workflow
sources:
  - "raw/youtube/📺 How To Build LLM Wiki In Obsidian 🧠 A Memory Layer For Any Agentic AI.md"
  - "raw/youtube/📺 LLM Wiki를 업그레이드하는 외부 지식 시스템! 연구자를 위한 최강의 조합 Zotero × Notebook × Obsidian x Claude Code.md"
  - "raw/notebooklm/2026-07-16-all-notes.md"
  - "raw/notebooklm/understand-anything-github.md"
confidence: medium
contested: false
contradictions: []
---

# AI 개인 지식관리

AI 개인 지식관리는 자료를 많이 저장하는 일이 아니라, 원본과 해석의 경계를 보존하면서 검증된 지식을 반복해서 재사용할 수 있게 만드는 운영 체계다.

핵심 단위는 특정 앱이 아니라 추적 가능한 원본, 상호 연결된 Markdown, 명시적인 품질 규칙이다. ^[raw/youtube/📺 How To Build LLM Wiki In Obsidian 🧠 A Memory Layer For Any Agentic AI.md]

## 지식의 세 층

| 층 | 목적 | 보존 원칙 |
| --- | --- | --- |
| 원본 | 논문·웹·영상과 메타데이터 보존 | 수정하지 않고 출처와 수집 시점을 남긴다. |
| 컴파일된 지식 | 개념·비교·질의를 재사용 가능하게 정리 | 출처, 링크, 갱신일과 신뢰도를 유지한다. |
| 집중 탐색 | 제한된 소스 묶음에 질문하고 가설 생성 | 생성 답변을 확정 지식과 구분한다. |

원본 도서관, 컴파일된 위키, 소스 기반 질의 공간을 분리하면 대용량 원본을 Markdown 저장소에 모두 복제하지 않으면서도 근거로 돌아갈 수 있다.

한 도구의 대화 기록이나 독점 형식이 사라져도 핵심 지식과 출처 관계가 남는다는 점도 중요하다. ^[raw/youtube/📺 LLM Wiki를 업그레이드하는 외부 지식 시스템! 연구자를 위한 최강의 조합 Zotero × Notebook × Obsidian x Claude Code.md]

## 운영 순환

1. 원본과 메타데이터를 먼저 보존한다.
2. 반복해서 쓸 가치가 있는 내용만 개념·비교·질의 문서로 컴파일한다.
3. 새 문서를 기존 지식과 연결하고 중복·모순·출처 누락을 검사한다.
4. 지식그래프로 군집, 브리지, 고립 문서와 약한 연결을 탐색한다.
5. 그래프가 제안한 관계를 원본 또는 제한된 소스 묶음으로 검증한다.
6. 검증된 결과만 위키에 환류한다.

이 순환은 [[ai-knowledge-workflow]]의 단계적 흐름과 [[research-feedback-loop]]의 반복 구조를 결합한다. 지식그래프는 문서 관계를 탐색하는 관측 도구이며, 그래프에 나타난 연결 자체가 사실의 증거는 아니다. ^[raw/notebooklm/understand-anything-github.md]

## 편입 기준

- 같은 질문에서 다시 사용할 가능성이 높은가?
- 원본 위치와 근거 문장을 다시 찾을 수 있는가?
- 기존 문서의 갱신으로 충분한가, 새 문서가 필요한가?
- AI 요약, 외부 주장의 사실, 개인 판단을 구분했는가?
- 빠르게 변하는 정보에 날짜와 적절한 신뢰도를 표시했는가?

이 기준을 통과하지 못한 탐색 결과는 임시 메모로 남기고 canonical 위키에는 편입하지 않는다. 구체적인 도구 경계는 [[knowledge-tool-roles]], 연구 중심 구현은 [[second-brain-research-workflow]]에 정리한다.

## 열린 질문

- 어떤 재사용 빈도와 검증 비용을 새 페이지 생성 임계값으로 삼을 것인가?
- 자동화된 그래프 분석과 사람의 의미 검토 사이에 어떤 승인 관문을 둘 것인가?
- 개인 경험에서 나온 지식과 외부 출처 기반 지식을 어떤 구조로 연결할 것인가?
