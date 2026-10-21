---
title: "Rule-Based vs Deep Learning Inspection"
type: comparison
status: draft
tags:
  - task/anomaly-detection
  - task/classification
  - constraint/low-data
sources:
  - raw/web/pekat-deep-learning-vs-rule-based.md
  - raw/web/keyence-ai-in-machine-vision.md
  - raw/papers/bergmann-2019-mvtec-ad.md
  - raw/papers/martin-2021-surface-defect-detection-strategies.md
created: 2026-10-21
updated: 2026-10-21
---

# Rule-Based vs Deep Learning Inspection

검사 방식을 고를 때의 비교다. 두 벤더 출처 모두 한쪽이 다른 쪽을 대체하는
것이 아니라 함께 쓰는 것을 권한다.
^[raw/web/pekat-deep-learning-vs-rule-based.md]
^[raw/web/keyence-ai-in-machine-vision.md]

## 비교표

| 항목 | 룰 기반 | 딥러닝(지도학습) | 이상 탐지(정상만 학습) |
| --- | --- | --- | --- |
| 잘 맞는 일 | 치수 측정, 정렬, 바코드, 유무 확인 | 외관 변동이 큰 표면 결함, 유형 분류 | 드물거나 처음 보는 결함 |
| 전제 | 형상 일정, 기준이 명확 | 불량 샘플·라벨 확보 | 정상 샘플 다수 |
| 약점 | 제품·환경이 조금만 바뀌어도 수동 조정 | 데이터 불균형, 라벨 비용 | 정상 데이터만으로 임계값 정하기 어려움 |

근거:
- 룰 기반은 정밀하고 반복 가능한 규칙으로 정의되는 측정, 정렬, 바코드
  판독에서 더 빠르고 가볍고 설정이 쉽다.
  ^[raw/web/pekat-deep-learning-vs-rule-based.md]
- 공차가 명확하고 형상이 일정하면 결정적 측정 알고리즘이 속도, 단순성,
  신뢰성에서 딥러닝보다 낫다. ^[raw/web/pekat-deep-learning-vs-rule-based.md]
- 룰은 설정 당시의 형상, 조명, 부품 위치를 전제로 하며, 조명·소재·부품
  자세가 바뀌면 재조정이 필요하다. ^[raw/web/keyence-ai-in-machine-vision.md]
- 딥러닝은 제품에 자연적 변동이 있을 때 강하다.
  ^[raw/web/pekat-deep-learning-vs-rule-based.md]
- 이상 탐지는 결함이 드물거나, 처음 보거나, 정의하기 어려울 때 가치가 크다.
  ^[raw/web/pekat-deep-learning-vs-rule-based.md]
  제조 공정은 불량을 최소화하도록 최적화돼 있어 불량 이미지가 매우 적다.
  ^[raw/papers/bergmann-2019-mvtec-ad.md]
- 지도학습은 작은 결함, 드문 결함, 설명 가능성, 적은 데이터라는 요구사항을
  풀어야 한다. ^[raw/papers/martin-2021-surface-defect-detection-strategies.md]
- 정상 이미지만으로 좋은 임계값을 정하기 어렵다.
  ^[raw/papers/bergmann-2019-mvtec-ad.md]

## 혼합 구성

- 룰 기반으로 부품 위치를 정밀하게 잡고, 딥러닝으로 결함을 판정한다.
  ^[raw/web/pekat-deep-learning-vs-rule-based.md]
- 룰 기반은 정밀 측정, 정렬, 유무 확인을 맡고, AI는 변동이나 표면 복잡도
  때문에 고정 로직이 한계에 부딪히는 부분을 맡는다.
  ^[raw/web/keyence-ai-in-machine-vision.md]

## 사출·고무 부품에 대입 (제안)

출처 없는 시작 가설이며 샘플로 검증해야 한다.

- 쇼트샷, 치수, 인서트 유무 → 룰 기반 우선
- 싱크마크, 웰드라인, 표면 오염, 텍스처 면 결함 → 딥러닝 또는 이상 탐지
- 신규 금형 초기처럼 불량 샘플이 거의 없을 때 → 이상 탐지로 시작해 불량이
  쌓이면 지도학습 검토

## 관련 지식

- [[concepts/industrial-anomaly-detection|Industrial Anomaly Detection]]
- [[concepts/surface-defect-detection|Surface Defect Detection]]
- [[queries/vision-inspection-introduction-guide|비전검사 공정 도입 가이드]]

## TODO

- 두 웹 출처 모두 딥러닝 제품을 파는 벤더다. 중립 출처를 추가한다.
- Cognex 가이드는 접속 제한(HTTP 429)으로 미수집. 재시도한다.
