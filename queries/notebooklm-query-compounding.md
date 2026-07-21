---
title: NotebookLM 질의 지식 증분 워크플로
created: 2026-07-21
updated: 2026-07-21
type: query
tags:
  - automation
  - knowledge-base
  - notebooklm
  - provenance
  - workflow
sources:
  - "raw/notebooklm/notebooklm-py-github.md"
  - "raw/notebooklm/llm-wiki-skill-github.md"
  - "raw/notebooklm/2026-07-16-all-notes.md"
confidence: medium
contested: false
contradictions: []
---

# NotebookLM 질의 지식 증분 워크플로

## 질의

NotebookLM 질의응답에서 원본 대화 전문을 별도로 저장하지 않으면서, 재사용 가능한 지식만 `queries/`에 편입해 개인 지식베이스를 증분시키려면 어떻게 운영해야 하는가?

## 핵심 결론

NotebookLM 답변은 일시적인 합성 결과이고 `queries/` 문서는 검토를 통과한 장기 지식이다. 두 계층을 구분하되 원본 Q&A 파일은 만들지 않는다.

답변의 가치와 근거를 평가한 뒤 하나의 canonical query 문서만 생성하거나 갱신하고, 실제 raw source와 NotebookLM 대화 식별자를 기록한다. ^[raw/notebooklm/notebooklm-py-github.md]

    NotebookLM 질의
      → JSON 답변과 source ID 확보
      → 저장 가치 판정
      → 기존 위키 문서 검색
      → 근거·사실 교차검증
      → canonical query 생성 또는 갱신
      → index·log·역링크 갱신
      → lint

## 저장 대상 판정

다시 도출하기 어렵고 반복 활용할 수 있는 다음 결과만 저장한다.

- 여러 source를 결합한 비교와 종합
- 반복 가능한 연구·개발 워크플로
- 장기적으로 적용할 의사결정 기준
- 연구 가설, 지식 공백과 검증 계획
- 기존 문서 여러 개를 새롭게 연결하는 분석
- 오류와 제약까지 검토된 심층 설명

단순 명령어, 상태 조회, 기존 페이지와 중복되는 설명, 근거가 불명확한 답변은 저장하지 않는다. 답변 길이가 아니라 가치·검증 가능성·재사용성이 기준이다.

## 출처 매핑

NotebookLM 응답의 source ID는 로컬 `raw/**/*.md`의 `notebooklm_source_id`와 연결한다. UUID가 일치하는 파일만 query의 `sources:`에 기록한다.

인용 번호나 제목이 비슷하다는 이유로 경로를 추정하지 않는다. 과거 대화를 재질의한 결과는 기존 인용 복구가 아니라 새로운 검증 turn으로 기록한다. ^[raw/notebooklm/llm-wiki-skill-github.md]

## 편입 체크리스트

1. 같은 장기 질문을 다루는 query가 이미 있는지 검색한다.
2. 실제 source 경로와 주요 주장을 교차검증한다.
3. 불확실하거나 버전 의존적인 내용을 표시한다.
4. 질문, 결론, 근거, 적용 절차와 한계를 작성한다.
5. 최소 두 개의 유효한 위키링크와 역링크를 확보한다.
6. `index.md`, `log.md`, 갱신일과 lint 결과를 동기화한다.

이 과정은 [[research-feedback-loop]]의 집중 합성 결과를 [[llm-wiki]]의 검증된 장기 지식으로 승격시키는 관문이다. 전체 수집·검증 맥락은 [[ai-knowledge-workflow]]를 참고한다.

## 제한

- NotebookLM 답변 전문을 저장하지 않으므로 서버 대화가 삭제되면 원문을 복원할 수 없다.
- 대신 질문, 검증된 최종 지식, 실제 source 경로와 대화 식별자를 보존한다.
- source ID가 로컬 원본에 매핑되지 않으면 신뢰도를 낮추거나 편입을 보류한다.
- 빠르게 변하는 기능은 편입 시점의 공식 문서와 설치된 CLI 도움말을 다시 확인한다.
