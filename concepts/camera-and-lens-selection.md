---
title: "Camera and Lens Selection"
type: concept
status: draft
tags:
  - hardware/camera
  - constraint/real-time
sources:
  - raw/web/keyence-2d-measurement-pixel-resolution.md
  - raw/web/keyence-selecting-machine-vision-camera.md
  - raw/web/commonlands-spatial-resolution.md
  - raw/web/commonlands-field-of-view.md
  - raw/web/imaging-source-lens-selection.md
created: 2026-10-21
updated: 2026-10-21
---

# Camera and Lens Selection

최소 불량 크기에서 출발해 필요한 해상도, 시야(FOV), 초점거리를 계산하는 절차다.
계산은 출발점일 뿐이며 실제 샘플 촬영으로 확인해야 한다.

## 1. 픽셀 분해능 (mm/pixel)

**픽셀 분해능 = 시야(mm) ÷ 그 방향 센서 픽셀 수**
^[raw/web/keyence-2d-measurement-pixel-resolution.md]

예: 시야 100mm, 세로 1200픽셀(2MP) → 0.083 mm/pixel.
^[raw/web/keyence-2d-measurement-pixel-resolution.md]

픽셀 분해능은 "샘플링 간격"이지 시스템이 구분할 수 있는 최소 크기가 아니다.
^[raw/web/commonlands-spatial-resolution.md]

## 2. 불량이 몇 픽셀이어야 하나

| 용도 | 기준 | 출처 |
| --- | --- | --- |
| 외관 결함 검출 | 4픽셀 면적 | ^[raw/web/keyence-selecting-machine-vision-camera.md] |
| 생산 검사 결함 | 결함을 가로질러 3~5픽셀 | ^[raw/web/commonlands-spatial-resolution.md] |
| 치수 측정 공차 | ±5픽셀 (반복성 0.5픽셀 × 10) | ^[raw/web/keyence-2d-measurement-pixel-resolution.md] |
| 측정 일반 | 10픽셀 이상 | ^[raw/web/commonlands-spatial-resolution.md] |

두 출처의 결함 기준은 단위가 다르다(면적 vs 가로지르는 폭). 둘 다 경험칙이며
대비, 노이즈, 알고리즘에 따라 달라진다. 현장 조건이 실험대보다 나쁘기 때문에
이론 최소 픽셀 수에 2~3배 여유를 두는 팀이 많다.
^[raw/web/commonlands-spatial-resolution.md]

**계산 예**: 시야 30mm에서 0.1mm 이물을 찾으려면 2MP 이상이 필요하다.
^[raw/web/keyence-selecting-machine-vision-camera.md]

## 3. 카메라 종류

- 에어리어 스캔: 한 번에 전체 이미지. 라인 스캔: 움직이는 대상을 한 줄씩
  쌓아 연속 소재·고속 부품에 적합. ^[raw/web/keyence-selecting-machine-vision-camera.md]
- 빠른 라인은 짧은 노출이 필요하고, 노출이 짧으면 빛이 부족해 조명 설계가
  함께 바뀐다. ^[raw/web/keyence-selecting-machine-vision-camera.md]
- 색상(hue) 차이로 구분해야 하면 컬러 카메라가 유리할 수 있다.
  ^[raw/web/keyence-selecting-machine-vision-camera.md]
- 자동 설정(특히 화이트밸런스)은 색상 검사를 불안정하게 만든다.
  ^[raw/web/keyence-selecting-machine-vision-camera.md]

## 4. 렌즈 초점거리

**초점거리 = 센서 크기 × 작동거리 ÷ 시야**
^[raw/web/imaging-source-lens-selection.md]

- 가로·세로 둘 다 계산하고 더 짧은 초점거리를 고른다.
  ^[raw/web/imaging-source-lens-selection.md]
- 계산값을 표준 초점거리(6, 8, 12, 16, 25, 35, 50, 75mm)로 맞추고 시야를
  다시 확인한다. ^[raw/web/imaging-source-lens-selection.md]
- 센서 크기는 공칭 규격이 아니라 데이터시트의 유효 크기를 쓴다.
  1/2인치 센서의 유효 폭은 약 6.4mm다. ^[raw/web/commonlands-field-of-view.md]
- 이 공식은 작동거리가 초점거리보다 충분히 길 때의 근사다.
  ^[raw/web/commonlands-field-of-view.md]

## 5. 렌즈 품질과 조리개

- 고해상도 카메라도 렌즈가 분해하지 못하는 디테일은 복원하지 못한다.
  ^[raw/web/keyence-selecting-machine-vision-camera.md]
- 렌즈 이미지 서클이 센서 대각선보다 작으면 모서리가 어두워진다.
  ^[raw/web/commonlands-spatial-resolution.md]
- 치수 측정에는 왜곡이 낮은 렌즈가 중요하다.
  ^[raw/web/imaging-source-lens-selection.md]
- 조리개를 조이면(f값↑) 피사계 심도는 깊어지지만 빛이 줄어든다. 그래서
  조리개와 조명은 함께 정한다. ^[raw/web/imaging-source-lens-selection.md]

## 흔한 실수

해상도만 올리고 조명·광학을 소홀히 하는 것. 픽셀 수로 나쁜 조명을 메울 수 없다.
^[raw/web/keyence-selecting-machine-vision-camera.md]

## 관련 지식

- [[concepts/machine-vision-lighting|Machine Vision Lighting]]
- [[queries/vision-inspection-introduction-guide|비전검사 공정 도입 가이드]]
- [[concepts/surface-defect-detection|Surface Defect Detection]]

## TODO

- 출처 5건이 모두 벤더 문서다. 광학 교재로 교차 확인한다.
- 텔레센트릭 렌즈, 3D 센서 선정 기준을 보강한다.
