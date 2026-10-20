---
title: "Industrial Anomaly Detection"
type: concept
status: draft
tags:
  - task/anomaly-detection
  - constraint/low-data
sources:
  - raw/papers/bergmann-2019-mvtec-ad.md
created: 2026-08-20
updated: 2026-10-20
---

# Industrial Anomaly Detection

산업 현장에서 정상 상태와 다른 결함, 이상, 비정상 패턴을 탐지하는
컴퓨터비전 문제다. 보통 정상 이미지만으로 학습한다.

## 왜 정상 데이터만으로 학습하나

- 제조 중 어떤 불량이 생길지 미리 모르는 경우가 많다.
  ^[raw/papers/bergmann-2019-mvtec-ad.md]
- 공정은 불량을 최소화하도록 최적화돼 있어 불량 이미지는 매우 적고,
  정상 이미지는 많다. ^[raw/papers/bergmann-2019-mvtec-ad.md]

## 실무 주의점

- 정상 이미지만으로 좋은 판정 임계값을 정하기 어렵다.
  ^[raw/papers/bergmann-2019-mvtec-ad.md]
- 불량 샘플을 모을 수 있고 유형 구분이 필요하면
  [[concepts/surface-defect-detection|Surface Defect Detection]]
  (지도학습)도 함께 검토한다.

## 관련 지식

- [[concepts/patchcore|PatchCore]]
- [[concepts/mvtec-ad|MVTec AD]]
- [[concepts/memory-bank|Memory Bank]]
- [[concepts/surface-defect-detection|Surface Defect Detection]]
- [[entities/anomalib|Anomalib]]

## TODO

- 이상 탐지, 객체 탐지, 분할 기반 검사 방식의 적용 조건을 비교한다.
