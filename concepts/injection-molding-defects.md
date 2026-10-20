---
title: "Injection Molding Defects"
type: concept
status: draft
tags:
  - domain/injection-molding
sources:
  - raw/web/fictiv-injection-molding-defects.md
created: 2026-10-20
updated: 2026-10-20
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

## 비전검사 관점의 분류 (가설)

아래 분류는 출처가 아닌 추론이며, 실제 샘플로 검증해야 한다.

- **형상·치수형**: short shot, flash, warping → 백라이트·외곽 측정이나
  룰 기반 검사로 시작할 후보.
- **표면 요철형**: sink mark, weld line, flow line, jetting →
  저각 암시야나 방향성 조명으로 대비를 만들어야 할 후보.
- **색상형**: discoloration → 색/파장 선택이 중요한 후보.
- **내부형**: vacuum void → 표면 카메라로 안 보일 수 있음.

조명 기법은 [[concepts/machine-vision-lighting|Machine Vision Lighting]]을 참고한다.

## 관련 지식

- [[concepts/machine-vision-lighting|Machine Vision Lighting]]
- [[queries/vision-inspection-introduction-guide|비전검사 공정 도입 가이드]]
- [[concepts/surface-defect-detection|Surface Defect Detection]]

## TODO

- 고무 압착(compression molding) 불량 유형 출처를 수집해 별도 문서로 만든다.
- 출처가 제조 서비스 기업 블로그 1건뿐이다. 교재·학술 출처로 교차 확인한다.
