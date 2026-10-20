---
title: "Surface Defect Detection"
type: concept
status: draft
tags:
  - task/classification
  - task/segmentation
  - constraint/low-data
  - domain/rubber-molding
sources:
  - raw/papers/martin-2021-surface-defect-detection-strategies.md
created: 2026-10-20
updated: 2026-10-20
---

# Surface Defect Detection

결함 샘플을 수집·라벨링해 지도학습(분류·분할)으로 표면 결함을 찾는
접근이다. 정상 이미지만 쓰는
[[concepts/industrial-anomaly-detection|Industrial Anomaly Detection]]과 대비된다.

## 산업 적용의 네 가지 요구사항

Martin et al.(2021)은 문헌과 고무 성형품 제조 사례에서 다음 요구사항을
도출했다. ^[raw/papers/martin-2021-surface-defect-detection-strategies.md]

1. 매우 작은 결함을 찾아야 한다.
2. 드물게 발생하는 결함을 찾아야 한다 (데이터 불균형).
3. 판정을 설명할 수 있어야 한다 (검사자 신뢰).
4. 적은 학습 데이터로 학습해야 한다.

## 대응 전략

| 원칙 | 구체 방법 |
| --- | --- |
| 분할 촬영 | 부품을 여러 구간으로 나눠 촬영하고, 구간별 판정을 모아 부품 판정 |
| 데이터 균형 | 다수 클래스(정상) undersampling |
| 정보량 선택 | 용도에 맞게 이진 분류 / 다중 분류 / 분할 중 선택 |
| 지식 전이 | ImageNet 등 사전학습 가중치, 도메인 적응 |
| 정규화 | early stopping, dropout, 데이터 증강 |

^[raw/papers/martin-2021-surface-defect-detection-strategies.md]

## 고무 성형품 사례 수치

- 기존 방식: 확대경 100% 육안검사.
- 부품을 회전시키며 부품당 약 135장(약 25MP, 그레이스케일) 촬영.
- 원시 이미지 43,740장 중 결함 이미지 약 1.5% → undersampling 후 1,280장.
- 이진 분류 정확도: 무작위 초기화 0.664, ImageNet 사전학습 0.974,
  강판 결함 데이터 사전학습 0.977. 단, 사전학습 실험(0.974, 0.977)에는
  데이터 증강도 함께 적용돼 있어 차이 전부를 사전학습 효과로 볼 수는 없다.
- 분할 모델은 다중 분류보다 F1이 높았다 (0.930 vs 0.898).

^[raw/papers/martin-2021-surface-defect-detection-strategies.md]

**실무 시사점**: 범용 사전학습만으로도 큰 성능 향상이 있었다.
^[raw/papers/martin-2021-surface-defect-detection-strategies.md]
단, 단일 사례·통제된 R&D 환경 결과이며 양산 라인 성능은 아니다.

## 관련 지식

- [[concepts/industrial-anomaly-detection|Industrial Anomaly Detection]]
- [[concepts/machine-vision-lighting|Machine Vision Lighting]]
- [[queries/vision-inspection-introduction-guide|비전검사 공정 도입 가이드]]

## TODO

- 과검(overkill)/미검(underkill) 기준의 평가 사례를 수집한다.
- 라벨링 기준서 작성법과 라벨 품질 점검 방법 출처를 수집한다.
