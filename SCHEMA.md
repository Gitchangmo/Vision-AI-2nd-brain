# Industrial Vision AI Wiki Schema

## Purpose

이 저장소는 산업용 컴퓨터비전 AI의 연구와 현장 적용을 지원하는
개인 지식베이스다.

다루는 핵심 주제:
- 이상 탐지, 객체 탐지, 분할
- 데이터셋, 라벨링, 평가 지표
- 모델 최적화와 엣지 추론
- 카메라, 조명, 현장 배포
- 실험 결과, 실패 원인, 설계 결정

## Repository Structure

- `inbox/`: 아직 분류하지 않은 메모·링크·아이디어
- `raw/`: 논문, 공식 문서, 실험 로그 등 원본 자료
- `entities/`: 사람, 조직, 도구, 데이터셋, 모델 같은 개체
- `concepts/`: 기술 개념과 방법론
- `comparisons/`: 모델·도구·방법 비교
- `queries/`: 여러 출처를 종합한 질문과 답변
- `docs/`: 이 위키의 운영 문서
- `index.md`: 현재 정식 지식 목록
- `log.md`: 중요한 변경 기록

## Core Rules

1. 원본 자료는 `raw/`에 보관하고, 본문을 수정하지 않는다.
2. 정식 지식은 `entities/`, `concepts/`, `comparisons/`, `queries/`에 둔다.
3. 정식 지식에는 가능한 한 `sources`에 실제 `raw/` 파일 경로를 기록한다.
4. 원문 근거가 부족한 내용은 `status: draft` 또는 `TODO`로 표시한다.
5. 관련 문서는 `[[wikilink]]`로 연결한다.
6. 기존 문서가 있으면 중복 생성보다 기존 문서를 보강한다.
7. LLM은 `raw/` 원문을 수정하지 않고, canonical 문서 변경은 제안 또는 초안으로 만든다.
8. 중요한 정식 지식 생성·수정 후 `index.md`와 `log.md`를 갱신한다.

## Canonical Frontmatter

모든 정식 문서는 다음 형식을 권장한다.

---
title: "<문서 제목>"
type: concept | entity | comparison | query
status: draft | verified | disputed
tags: []
sources: []
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

## Initial Tags

처음에는 아래 태그만 사용한다.

- `task/anomaly-detection`
- `task/object-detection`
- `task/segmentation`
- `constraint/low-data`
- `constraint/real-time`
- `constraint/edge-device`
- `constraint/lighting-variation`
- `metric/auroc`
- `metric/f1-score`
- `metric/false-positive-rate`
- `deployment/onnx`
- `deployment/tensorrt`
- `deployment/gstreamer`

새 태그가 필요하면 임의로 만들지 말고,
SCHEMA.md의 이 목록에 먼저 추가한다.