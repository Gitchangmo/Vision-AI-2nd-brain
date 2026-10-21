---
title: "Concept Drift"
type: concept
status: draft
tags:
  - operation/drift-monitoring
  - task/anomaly-detection
sources:
  - raw/papers/hinder-2023-concept-drift-survey.md
  - raw/papers/yang-2020-diagnosing-concept-drift.md
created: 2026-10-21
updated: 2026-10-21
---

# Concept Drift

시간이 지나며 데이터 분포가 바뀌어, 과거 데이터로 만든 모델이 부정확해지는
현상이다. ^[raw/papers/yang-2020-diagnosing-concept-drift.md]
비전검사를 양산에 이관한 뒤 성능이 서서히 떨어지는 주요 원인이다.

## 원인은 세 곳

드리프트는 관측 대상 공정, 환경, 데이터를 얻는 센서의 변화로 생긴다.
^[raw/papers/hinder-2023-concept-drift-survey.md]

- **공정 변화**: 불량 증가 같은 생산 이상 신호일 수 있다.
- **센서·환경 변화**: 센서 교체나 시스템 재조정이 필요할 수 있다.

^[raw/papers/hinder-2023-concept-drift-survey.md]

비전검사에 대입한 예(제안, 출처 없음): 공정 쪽은 금형 마모·소재 로트 변경,
환경 쪽은 조명 노화·외광, 센서 쪽은 렌즈 오염·카메라 위치 틀어짐.

## 탐지 방식 두 가지

| 방식 | 원리 | 한계 |
| --- | --- | --- |
| 오류율 기반 | 정답 라벨로 모델 오류율을 감시 | 양산 데이터의 정답 라벨 확보가 어려움 |
| 분포 기반 | 입력 데이터 분포 변화를 감시 | 정답 라벨이 필요 없음 |

^[raw/papers/yang-2020-diagnosing-concept-drift.md]

## 언제와 어디

- 탐지(when): 변화 시점과 속도를 찾는다.
- 위치 추정(where): 데이터 중 어느 부분이 변했는지 찾는다.

^[raw/papers/hinder-2023-concept-drift-survey.md]

품질검사에서는 이미 알려진 불량을 걸러내는 알고리즘이 있어도, 새로운 유형의
이상이 나타나면 해당 품목을 찾아내 조치가 필요한지 분석해야 한다.
^[raw/papers/hinder-2023-concept-drift-survey.md]

## 비전검사 운영 적용 (제안)

출처의 개념을 운영에 적용한 제안이며 현장 검증이 필요하다.

- 정상 판정 이미지의 밝기·이상 점수 분포를 일·주 단위로 기록한다
  (라벨 없이 가능한 분포 기반 감시).
- 과검·미검 재판정 결과를 주기적으로 모아 오류율도 함께 본다.
- 조명 교체, 금형 수리, 소재 변경 때마다 기준 이미지를 다시 찍어 비교한다.
- 모델 업데이트 기준(어떤 지표가 얼마나 변하면 재학습할지)을 양산 이관 전에
  정한다. 배포 후 성능을 감시하고 업데이트 시점을 정하는 것은 연구에 참여한
  실무자들이 공통으로 겪은 핵심 문제였다.
  ^[raw/papers/yang-2020-diagnosing-concept-drift.md]

## 관련 지식

- [[concepts/industrial-anomaly-detection|Industrial Anomaly Detection]]
- [[concepts/vision-plc-integration|Vision–PLC Integration]]
- [[queries/vision-inspection-introduction-guide|비전검사 공정 도입 가이드]]

## TODO

- 비전검사 양산 운영에서 드리프트를 실제 측정한 사례를 수집한다.
- 재학습 주기와 재검증 절차 사례를 수집한다.
