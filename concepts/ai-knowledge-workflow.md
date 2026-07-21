---
title: AI 지식 워크플로
created: 2026-07-21
updated: 2026-07-21
type: concept
tags:
  - automation
  - provenance
  - research
  - workflow
sources:
  - "raw/youtube/📺 How To Build LLM Wiki In Obsidian 🧠 A Memory Layer For Any Agentic AI.md"
  - "raw/youtube/📺 LLM Wiki를 업그레이드하는 외부 지식 시스템! 연구자를 위한 최강의 조합 Zotero × Notebook × Obsidian x Claude Code.md"
  - "raw/notebooklm/2026-07-16-all-notes.md"
  - "raw/notebooklm/llm-wiki-zotero-notebooklm-youtube.md"
confidence: medium
contested: false
contradictions: []
---

# AI 지식 워크플로

AI 지식 워크플로는 원본 수집부터 검토된 지식과 산출물 생성까지를 역할별 계층으로 나누는 운영 방식이다. 개인 지식관리 체계 전체에서 이 흐름이 갖는 의미는 [[ai-personal-knowledge-management]]에 정리한다.

## 기본 흐름

    수집 → 원본 보존 → 탐색·질의 → 위키 컴파일 → 검증 → 산출

- Zotero와 브라우저 클리퍼는 원본과 서지정보를 수집한다.
- NotebookLM은 선택한 소스 묶음을 탐색하고 질문한다.
- LLM Wiki와 Obsidian은 장기 지식과 관계를 Markdown으로 유지한다.
- Understand Anything은 지식 연결과 공백 후보를 그래프로 탐색한다.
- 검토된 지식은 글, 보고서, 프레젠테이션 같은 산출물로 변환한다.

한 도구가 모든 책임을 갖지 않도록 원본 보존, 지식 합성, 구조 분석, 결과 표현을 분리하면 도구를 교체해도 축적된 Markdown과 출처 관계를 유지할 수 있다. ^[raw/youtube/📺 LLM Wiki를 업그레이드하는 외부 지식 시스템! 연구자를 위한 최강의 조합 Zotero × Notebook × Obsidian x Claude Code.md]

## 검증 관문

1. 원본과 요약이 분리되어 있는가?
2. 모든 핵심 주장에 추적 가능한 출처가 있는가?
3. 기존 문서와 중복되거나 충돌하지 않는가?
4. 내부 링크가 실제 문서를 가리키는가?
5. 산출물이 목적에 맞는 형식으로 직접 열리고 사용되는가?

## 위험과 제어

- 여러 에이전트가 같은 문서를 서로 다르게 해석할 수 있다.
- 프로젝트 README나 소개 영상의 홍보성 주장이 검증 없이 굳어질 수 있다.
- 자동화가 늘수록 잘못된 메타데이터가 빠르게 전파될 수 있다.

따라서 생성 속도는 출처, 링크, 스키마와 일관성 검사를 자동화할 때 비로소 장기 지식 품질로 이어진다.

구체적인 단계 배치는 [[knowledge-tool-roles]], 반복 운영 모델은 [[research-feedback-loop]], 연구 환경 구현은 [[second-brain-research-workflow]]를 참고한다. ^[raw/notebooklm/2026-07-16-all-notes.md]
