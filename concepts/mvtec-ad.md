---
title: "MVTec AD"
type: concept
status: draft
tags:
  - task/anomaly-detection
  - metric/auroc
sources:
  - raw/papers/bergmann-2019-mvtec-ad.md
  - raw/web/mvtec-ad-dataset-page.md
created: 2026-08-20
updated: 2026-10-20
---

# MVTec AD

MVTec AD는 산업용 이상 탐지 모델을 평가할 때 자주 활용되는 이미지 데이터셋이다.

## 구성

- 15개 카테고리: 텍스처 5종(carpet, grid, leather, tile, wood)과 객체 10종.
  ^[raw/papers/bergmann-2019-mvtec-ad.md]
- 학습·검증 3,629장(정상만), 평가 1,725장(정상 + 결함), 총 5,354장.
  ^[raw/papers/bergmann-2019-mvtec-ad.md]
- 결함 유형 73종, 카테고리당 평균 5종. 모든 결함에 픽셀 단위 정답 영역 제공.
  ^[raw/papers/bergmann-2019-mvtec-ad.md]
- 2048×2048 산업용 RGB 센서와 텔레센트릭 렌즈로, 엄격히 통제된 조명에서
  촬영했다. ^[raw/papers/bergmann-2019-mvtec-ad.md]

## 라이선스 주의

CC BY-NC-SA 4.0이며 상업적 목적으로 사용할 수 없다.
^[raw/web/mvtec-ad-dataset-page.md]

## 평가에서 배울 점

- 원 논문 벤치마크에서 어떤 방법도 모든 카테고리에서 고르게 잘하지 못했다.
  ^[raw/papers/bergmann-2019-mvtec-ad.md]
- ROC AUC가 높아도, 정상 이미지만으로 추정한 임계값에서는 분할이 실패할 수
  있다. ^[raw/papers/bergmann-2019-mvtec-ad.md]
- 통제된 조명에서 찍은 데이터라, 이 벤치마크 점수가 현장 라인 성능을
  보장하지 않는다는 점을 감안한다.

## 관련 지식

- [[concepts/patchcore|PatchCore]]
- [[concepts/industrial-anomaly-detection|Industrial Anomaly Detection]]
- [[queries/vision-inspection-introduction-guide|비전검사 공정 도입 가이드]]

## TODO

- 확장판(IJCV)과 후속 평가 지표(PRO 등)를 원본 출처로 보강한다.
