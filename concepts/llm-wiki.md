---
title: LLM Wiki
created: 2026-07-21
updated: 2026-07-21
type: concept
tags:
  - knowledge-base
  - pkm
  - provenance
  - workflow
sources:
  - "raw/youtube/📺 How To Build LLM Wiki In Obsidian 🧠 A Memory Layer For Any Agentic AI.md"
  - "raw/youtube/📺 LLM Wiki를 업그레이드하는 외부 지식 시스템! 연구자를 위한 최강의 조합 Zotero × Notebook × Obsidian x Claude Code.md"
  - "raw/notebooklm/llm-wiki-skill-github.md"
  - "raw/notebooklm/2026-07-16-all-notes.md"
confidence: high
contested: false
contradictions: []
---

# LLM Wiki

LLM Wiki는 원본 자료를 한 번 구조화해 사람과 여러 AI 에이전트가 반복해서 사용할 수 있게 만드는 지속형 Markdown 지식베이스다. 질문할 때마다 원본을 처음부터 검색하는 방식과 달리, 개념·비교·질의와 그 출처 연결을 누적한다. ^[raw/notebooklm/llm-wiki-skill-github.md]

## 세 계층

1. **Raw:** 변경하지 않는 원본 자료와 출처 메타데이터.
2. **Wiki:** 원본을 요약·비교·연결한 canonical 문서.
3. **Schema:** 파일명, frontmatter, 태그, 링크, 갱신과 검증 규칙.

이 분리는 원본과 해석을 섞지 않으면서도 하나의 탐색 가능한 공간처럼 사용할 수 있게 한다. [[ai-personal-knowledge-management]]은 이 구조를 전체 PKM 관점에서 설명하고, [[ai-knowledge-workflow]]는 수집부터 산출까지의 위치를 설명한다.

## RAG와의 차이

RAG는 질의 시점에 관련 조각을 검색해 답변 문맥을 구성한다. LLM Wiki는 자주 재사용할 지식을 미리 컴파일하고, 모순과 관계를 문서에 남긴다.

둘은 배타적이지 않다. RAG는 대규모 원본 검색에, 위키는 검토된 장기 지식과 연결 구조에 적합하다. ^[raw/youtube/📺 How To Build LLM Wiki In Obsidian 🧠 A Memory Layer For Any Agentic AI.md]

## 운영 원칙

- 원본을 `raw/`에 보존하고 canonical 페이지에서 정확한 경로로 인용한다.
- 특정 소스 묶음의 탐색은 NotebookLM 같은 도구로 보조한다.
- NotebookLM 결과는 [[notebooklm-query-compounding]]의 가치 판정과 출처 검증을 거쳐 편입한다.
- 새 자료를 기존 페이지에 연결하고 중복 페이지를 피한다.
- 생성 결과는 링크·태그·출처·모순 검사를 거친다.
- 지식그래프 분석은 [[ua-knowledge-graph-workflow]]에 따라 고립 문서와 약한 연결을 찾는 보조 수단으로 사용한다.

유지보수의 순환 구조는 [[research-feedback-loop]], 도구별 책임 경계는 [[knowledge-tool-roles]]에 정리한다.

## 열린 질문

- 위키가 커질 때 자동 생성과 사람의 검토 비율을 어떻게 조정할 것인가?
- 빠르게 변하는 제품 정보의 신선도를 어떤 주기로 확인할 것인가?
- 개인 메모와 외부 지식의 경계를 얼마나 엄격하게 유지할 것인가?
