---
title: "Anomalib"
type: entity
status: draft
tags:
  - task/anomaly-detection
  - deployment/openvino
sources:
  - raw/web/anomalib-documentation.md
created: 2026-10-20
updated: 2026-10-20
---

# Anomalib

시각 이상 탐지 알고리즘을 모아 둔 오픈소스 딥러닝 라이브러리다.
PoC 단계에서 여러 이상 탐지 모델을 빠르게 비교할 때 후보가 된다.

## 핵심

- 최신 이상 탐지 알고리즘을 공개·사설 데이터셋에서 벤치마크할 수 있도록
  모은 라이브러리이며, 이미지·영상의 이상을 탐지 또는 위치 추정하는
  시각 이상 탐지에 초점을 둔다. ^[raw/web/anomalib-documentation.md]
- 학습·추론·벤치마크용 API와 CLI를 제공한다.
  ^[raw/web/anomalib-documentation.md]
- 대부분의 모델을 OpenVINO IR로 내보내 Intel 하드웨어에서 가속 추론할 수
  있다. ^[raw/web/anomalib-documentation.md]

## 관련 지식

- [[concepts/patchcore|PatchCore]]
- [[concepts/industrial-anomaly-detection|Industrial Anomaly Detection]]
- [[queries/vision-inspection-introduction-guide|비전검사 공정 도입 가이드]]

## TODO

- 지원 모델 목록, 라이선스, ONNX 내보내기 지원 여부를 공식 저장소에서 확인한다.
