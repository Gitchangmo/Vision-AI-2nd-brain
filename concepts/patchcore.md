---
title: "PatchCore"
type: concept
status: draft
tags:
  - task/anomaly-detection
  - constraint/low-data
sources:
  - raw/papers/patchcore-paper.md
created: 2026-08-20
updated: 2026-08-20
---

# PatchCore

## 핵심 요약

PatchCore는 정상 이미지에서 추출한 특징을 memory bank에 저장하고,
새 입력 이미지의 특징이 정상 특징 분포와 얼마나 다른지 측정해
이상 여부를 판단하는 산업용 이상 탐지 방법이다.

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