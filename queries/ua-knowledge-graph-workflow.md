---
title: UA 위키 지식그래프 전체 워크플로
created: 2026-07-21
updated: 2026-07-21
type: query
tags:
  - knowledge-base
  - knowledge-graph
  - research
  - workflow
sources:
  - "raw/notebooklm/understand-anything-github.md"
  - "raw/notebooklm/2026-07-16-all-notes.md"
confidence: medium
contested: false
contradictions: []
---

# UA 위키 지식그래프 전체 워크플로

## 질의

위키 문서가 이미 생성되었다고 가정할 때 Understand Anything의 스킬은 어떤 역할을 하며, 지식그래프 생성부터 분석·활용·갱신까지 어떤 순서로 실행해야 하는가?

## 핵심 결론

Karpathy 패턴의 [[llm-wiki]]가 이미 존재한다면 시작점은 일반 코드 분석용 `understand`가 아니라 위키 전용 `understand-knowledge`다.

이 스킬로 지식그래프를 생성한 뒤 대시보드, 그래프 질의, 도메인 분석을 수행한다. 발견한 공백과 오류를 위키에 반영한 다음 그래프를 다시 생성한다. ^[raw/notebooklm/understand-anything-github.md]

    LLM Wiki 문서·index.md·wikilink
      → understand-knowledge
      → .ua/knowledge-graph.json
      → dashboard·chat·domain 분석
      → 위키 보강
      → understand-knowledge 재실행

## 코드 그래프와 지식그래프

`understand`는 파일·함수·클래스·서비스의 구조와 호출·의존 관계를 중심으로 코드 아키텍처를 만든다. `understand-knowledge`는 문서 제목, frontmatter, 위키링크를 추출하고 암시적 관계, 엔티티와 핵심 주장을 보강한다.

- 코드 그래프의 질문: 무엇이 무엇을 호출하고 의존하는가?
- 지식그래프의 질문: 어떤 개념과 주장이 연결되고 어떤 주제 군집을 이루는가?

## 권장 실행 순서

1. 위키의 `index.md`, canonical 문서와 wikilink가 유효한지 lint한다.
2. `understand-knowledge`로 `.ua/knowledge-graph.json`과 메타데이터를 생성한다.
3. 노드·관계 수, 미해결 링크, 고립 문서, 과도한 허브와 출처 없는 주장을 점검한다.
4. `understand-dashboard`로 주제 군집, 브리지와 학습 순서를 탐색한다.
5. `understand-chat`으로 관계와 근거가 약한 부분을 질의한다.
6. `understand-domain`으로 도메인·흐름·단계를 별도 그래프로 파생한다.
7. 검증된 공백·중복·약한 연결만 위키에 반영한다.
8. 위키가 바뀌면 `understand-knowledge`를 다시 실행한다.

그래프에서 보이는 빈 공간은 곧바로 연구 공백을 뜻하지 않는다. 자료 누락, 링크 부족, 추출 실패 또는 엔티티 중복일 수 있으므로 원문과 대조한다. ^[raw/notebooklm/2026-07-16-all-notes.md]

## 역할 분담과 환류

NotebookLM은 선택한 원본을 집중적으로 종합하고, LLM Wiki는 검증된 내용을 영속적인 상호 연결 문서로 컴파일한다. Understand Anything은 그 문서를 질의하고 시각화할 수 있는 지식그래프로 변환한다. 이 분석에서 나온 후보를 원본으로 확인하고 [[research-feedback-loop]]를 따라 환류한다.

그래프 품질은 문서 품질을 대신하지 않는다. 전체 PKM 운영 원칙은 [[ai-personal-knowledge-management]], 단계별 품질 관문은 [[ai-knowledge-workflow]]를 참고한다.
