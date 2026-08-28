---
title: "PatchCore"
type: concept
status: draft
tags:
  - task/anomaly-detection
  - constraint/low-data
sources:
  - raw/papers/roth-2022-patchcore.md
created: 2026-08-20
updated: 2026-08-20
---

# PatchCore

## 핵심 요약

PatchCore는 정상 이미지에서 얻은 locally aware,
mid-level patch feature를 대표성이 높은 memory bank에 저장한다.
추론 시 입력 patch feature와 memory bank의 최근접 이웃 간 거리를
사용해 이상 점수를 계산한다. ^[raw/papers/roth-2022-patchcore.md]

논문은 MVTec AD에서 PatchCore-25% memory bank 설정으로
image-level AUROC 99.1%를 보고했으며, 더 큰 backbone·고해상도·앙상블을
사용한 설정에서는 최대 99.6%를 보고했다.
^[raw/papers/roth-2022-patchcore.md]

## 적용 조건

- 정상 이미지 데이터는 있지만 결함 라벨이 부족한 경우
- 이미지 기반 품질 검사 또는 표면 결함 검사
- false positive와 추론 지연시간을 함께 검증해야 하는 환경

## 관련 지식

- [[concepts/industrial-anomaly-detection|Industrial Anomaly Detection]]
- [[concepts/memory-bank|Memory Bank]]
- [[concepts/mvtec-ad|MVTec AD]]

## 확인할 점

- 실제 원본 논문에서 사용한 feature extractor와 memory bank 구성
- 사내 데이터에서 false positive가 발생하는 원인
- 엣지 GPU에서의 memory bank 크기와 추론 지연시간