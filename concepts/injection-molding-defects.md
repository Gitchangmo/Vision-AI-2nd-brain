---
title: "Injection Molding Defects"
type: concept
status: draft
tags:
  - domain/injection-molding
sources:
  - raw/web/fictiv-injection-molding-defects.md
  - raw/web/overview-ai-injection-molding-inspection.md
created: 2026-10-20
updated: 2026-10-21
---

# Injection Molding Defects

사출 성형품에서 자주 나오는 외관 불량 유형이다. 비전검사 도입 시
불량 정의서와 조명·알고리즘 선택의 출발점으로 쓴다.

## 불량 유형 (출처 기준 10종)

| 불량 | 외관 | 주요 원인 |
| --- | --- | --- |
| Flow lines | 표면의 줄무늬·물결 | 금형 부위별 두께 차이 |
| Sink marks | 움푹 들어간 자국 | 두꺼운 부위의 느린 냉각 |
| Surface delamination | 표면이 얇은 층으로 벗겨짐 | 이형제 등 오염물 |
| Weld lines | 두 흐름이 만난 선 자국 | 두 흐름 선단의 온도 차 |
| Short shots | 캐비티 미충전 | 금형 내 흐름 제한 |
| Warping | 휨·뒤틀림 | 부위별 냉각 속도 차이 |
| Jetting | 가늘고 구불구불한 선 | 수지가 너무 빨리 들어가 먼저 굳음 |
| Vacuum voids | 내부·표면 근처 기포 | 표면과 내부의 불균일 고화 |
| Discoloration | 갈색·검은 자국 | 설비·금형 문제 |
| Flash | 파팅라인 등의 넘침 | 파팅라인 불일치, 벤팅 불량, 낮은 형체력 |

^[raw/web/fictiv-injection-molding-defects.md]

## 비전검사 관점의 검출 방법

아래 매칭은 AI 비전 장비 벤더 1곳의 자료이며, 실제 샘플로 검증해야 한다.

| 불량 | 벤더가 제시한 방법 |
| --- | --- |
| Sink marks | 저각(grazing-angle) 구조광 ^[raw/web/overview-ai-injection-molding-inspection.md] |
| 반짝이는 표면 | 확산 돔 조명 ^[raw/web/overview-ai-injection-molding-inspection.md] |
| 투명·반투명 부품의 기포·이물 | 백라이트 ^[raw/web/overview-ai-injection-molding-inspection.md] |
| Short shots | 양품 기준 이미지와 실루엣 비교 ^[raw/web/overview-ai-injection-molding-inspection.md] |
| Weld lines | 표면 텍스처 분류 + 위치별 임계값(안 보이는 부위는 허용) ^[raw/web/overview-ai-injection-molding-inspection.md] |

- **출처 내 불일치**: 같은 벤더의 다른 페이지는 싱크마크 조명 예로 돔 조명을
  든다. 저각과 돔 중 무엇이 맞는지는 샘플 테스트로 정한다.
  ^[raw/web/overview-ai-injection-molding-inspection.md]
- **한계**: 표면에 흔적이 없는 내부 기포는 카메라로 볼 수 없다.
  ^[raw/web/overview-ai-injection-molding-inspection.md]
- **광택·텍스처 면**: 광택 면은 반사광이 결함처럼 보이거나 결함을 가리고,
  텍스처 면은 고정 임계값이 무늬를 노이즈로 읽는다.
  ^[raw/web/overview-ai-injection-molding-inspection.md]

조명 기법은 [[concepts/machine-vision-lighting|Machine Vision Lighting]]을,
방식 선택은
[[comparisons/rule-based-vs-deep-learning-inspection|Rule-Based vs Deep Learning Inspection]]을 참고한다.

## 관련 지식

- [[concepts/machine-vision-lighting|Machine Vision Lighting]]
- [[queries/vision-inspection-introduction-guide|비전검사 공정 도입 가이드]]
- [[concepts/surface-defect-detection|Surface Defect Detection]]

## TODO

- 고무 압착(compression molding) 불량 유형 출처를 수집해 별도 문서로 만든다.
- 출처 2건 모두 기업 블로그다. 교재·학술 출처로 교차 확인한다.
