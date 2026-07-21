---
title: 세컨드 브레인 연구 워크플로
created: 2026-07-21
updated: 2026-07-21
type: concept
tags:
  - knowledge-base
  - pkm
  - research
  - workflow
sources:
  - "raw/notebooklm/2026-07-16-all-notes.md"
  - "raw/notebooklm/llm-wiki-zotero-notebooklm-youtube.md"
  - "raw/youtube/📺 LLM Wiki를 업그레이드하는 외부 지식 시스템! 연구자를 위한 최강의 조합 Zotero × Notebook × Obsidian x Claude Code.md"
confidence: medium
contested: false
contradictions: []
---

# 세컨드 브레인 연구 워크플로

세컨드 브레인 연구 워크플로는 원본 보존, AI 합성, 개인 해석을 분리하면서 하나의 반복 가능한 연구 환경으로 연결하는 방식이다. 이는 [[ai-personal-knowledge-management]]의 계층 원칙을 연구 자료 수집과 검증에 적용한 구현이다.

## 역할 분담

| 단계 | 역할 | 대표 도구 |
| --- | --- | --- |
| 수집 | 논문·웹 자료와 서지정보 보존 | Zotero, 브라우저 클리퍼 |
| 컴파일 | 재사용할 개념·비교·질의 생성 | LLM Wiki |
| 집중 탐색 | 제한된 소스 묶음 질의 | NotebookLM |
| 구조 분석 | 관계, 군집, 고립 문서 후보 탐색 | Understand Anything |
| 장기 편집 | Markdown과 개인 메모 관리 | Obsidian |

역할을 분리하면 각 도구의 생성 결과가 곧바로 확정 지식이 되는 것을 막고, 원문으로 돌아가는 경로를 유지할 수 있다. ^[raw/notebooklm/llm-wiki-zotero-notebooklm-youtube.md]

## 개인 지식과 외부 지식

외부 원본의 요약과 사용자의 경험·판단을 같은 층에서 섞으면 출처와 의견의 경계가 흐려진다. 원본과 컴파일된 지식은 출처를 유지하고, 개인 메모는 별도 섹션이나 문서로 기록하는 편이 안전하다.

## 성공 조건

- 원문으로 돌아갈 수 있다.
- AI가 만든 주장과 개인 판단을 구분할 수 있다.
- 도구가 바뀌어도 Markdown과 메타데이터가 남는다.
- 새 자료가 기존 지식과 연결되거나 모순으로 표시된다.
- 편입 전후에 스키마와 링크를 자동 검증한다.

전체 운영 절차는 [[ai-knowledge-workflow]], 반복적 개선은 [[research-feedback-loop]], 도구 선택 기준은 [[knowledge-tool-roles]]에 정리한다. ^[raw/notebooklm/2026-07-16-all-notes.md]
