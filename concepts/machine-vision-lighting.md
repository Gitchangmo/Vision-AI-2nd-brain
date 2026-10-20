---
title: "Machine Vision Lighting"
type: concept
status: draft
tags:
  - hardware/lighting
  - constraint/lighting-variation
sources:
  - raw/web/advanced-illumination-practical-guide-machine-vision-lighting.md
  - raw/web/keyence-machine-vision-lighting-selection.md
created: 2026-10-20
updated: 2026-10-20
---

# Machine Vision Lighting

비전검사에서 조명은 결함과 배경 사이의 대비를 만드는 단계다.
알고리즘보다 먼저, 실제 부품 샘플로 검증해야 한다.

## 왜 먼저 해야 하나

- 조명은 역사적으로 가장 나중에 사양이 정해지거나 예산이 배정되던
  요소였고, 체계적인 조명 분석이 일관되고 견고한 해법의 틀이 된다.
  ^[raw/web/advanced-illumination-practical-guide-machine-vision-lighting.md]
- 검사 위치의 물리적 공간 제약을 먼저 파악해야 한다.
  ^[raw/web/advanced-illumination-practical-guide-machine-vision-lighting.md]

## 대비를 만드는 네 가지 축

Advanced Illumination 가이드는 이미지 대비의 네 축을 다음과 같이 둔다:
① 광원 기하(geometry), ② 패턴/구조(structure), ③ 색/파장, ④ 필터.
경면(반짝이는) 표면에서는 기하와 구조가 특히 중요하고,
한 애플리케이션에 여러 기법을 함께 쓰는 경우도 흔하다.
^[raw/web/advanced-illumination-practical-guide-machine-vision-lighting.md]

## 기법별 용도

| 기법 | 원리 | 대표 용도 |
| --- | --- | --- |
| 명시야(bright field) | 정반사광이 렌즈로 들어옴 | 마킹 판독, 유무 확인 ^[raw/web/keyence-machine-vision-lighting-selection.md] |
| 부분 명시야(방향성) | 방향성 있는 조사 | 대비 생성, 표면 요철 강조 ^[raw/web/advanced-illumination-practical-guide-machine-vision-lighting.md] |
| 암시야(dark field, 저각) | 저각 조사광이 결함에서 산란 | 스크래치, 엠보싱, 질감 변화 ^[raw/web/keyence-machine-vision-lighting-selection.md] |
| 돔(확산) | 여러 방향에서 균일 조사 | 경면·곡면 부품의 반사 억제 ^[raw/web/advanced-illumination-practical-guide-machine-vision-lighting.md] |
| 동축(on-axis) | 광축과 같은 방향 조사 | 평평한 물체에서 돔과 유사한 효과 ^[raw/web/advanced-illumination-practical-guide-machine-vision-lighting.md] |
| 백라이트(투과) | 물체 뒤에서 조사, 밝은 배경에 어두운 실루엣 ^[raw/web/advanced-illumination-practical-guide-machine-vision-lighting.md] | 부직포 같은 투과성 소재의 이물 ^[raw/web/keyence-machine-vision-lighting-selection.md] |

## 색과 파장

- 컬러 카메라에는 보통 백색광을 쓴다.
  ^[raw/web/keyence-machine-vision-lighting-selection.md]
- 물체 색의 보색 조명을 비추면 그 물체는 거의 검게 보여 대비가 커진다.
  ^[raw/web/keyence-machine-vision-lighting-selection.md]
- 카메라 센서의 최대 분광 감도와 광원의 피크 파장을 맞춘다.
  ^[raw/web/advanced-illumination-practical-guide-machine-vision-lighting.md]

## 외란광

공장 천장 조명과 햇빛이 가장 흔한 외란광이며, 필터와 차광으로 대응한다.
^[raw/web/advanced-illumination-practical-guide-machine-vision-lighting.md]

## 관련 지식

- [[queries/vision-inspection-introduction-guide|비전검사 공정 도입 가이드]]
- [[concepts/injection-molding-defects|Injection Molding Defects]]
- [[concepts/surface-defect-detection|Surface Defect Detection]]

## TODO

- 두 출처 모두 벤더 문서다. 중립 출처(교재, 표준)로 교차 확인한다.
- 편광·스트로브·라인 조명 내용을 원문 후반부(미수집 구간)에서 보강한다.
- 검정 고무처럼 반사가 낮은 소재에 대한 조명 사례를 수집한다.
