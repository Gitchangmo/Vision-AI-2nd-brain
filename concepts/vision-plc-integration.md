---
title: "Vision–PLC Integration"
type: concept
status: draft
tags:
  - deployment/plc
  - constraint/real-time
  - metric/false-positive-rate
sources:
  - raw/papers/maslanka-2025-vision-plc-integration.md
  - raw/web/roboflow-computer-vision-plc-integration.md
created: 2026-10-21
updated: 2026-10-21
---

# Vision–PLC Integration

비전 판정 결과를 PLC로 넘겨 배출·정지·알람 같은 실제 설비 동작으로 연결하는
부분이다. PoC에서 잘 되던 시스템이 라인에서 실패하는 흔한 지점이다.

## 역할 분담

- 비전은 "무엇이 보였는지"를 판단하고, PLC는 타이밍, 인터록, 실제 배출을
  책임진다. 이 분리가 양산 안전성을 만든다.
  ^[raw/web/roboflow-computer-vision-plc-integration.md]
- PLC는 라인 가동 여부, 배출 장치 준비 상태, 안전 인터록, 액추에이터 작동
  시점을 이미 알고 있다. ^[raw/web/roboflow-computer-vision-plc-integration.md]
- 사례 논문에서도 PLC가 촬영 트리거, 결과 버퍼링, 검증 로직을 맡았다.
  ^[raw/papers/maslanka-2025-vision-plc-integration.md]

## 통신 방식

| 방식 | 특징 |
| --- | --- |
| Digital I/O | 단순한 OK/NG 신호. 불량 유형, 신뢰도, 개수, 부품 ID는 못 보냄 ^[raw/web/roboflow-computer-vision-plc-integration.md] |
| Modbus TCP | 지원 범위가 넓어 구형 설비에서 가장 쉬운 선택인 경우가 많음 ^[raw/web/roboflow-computer-vision-plc-integration.md] |
| EtherNet/IP | PLC 태그 교환. 사례 논문은 implicit cyclic 모드로 결정적 통신 구성 ^[raw/papers/maslanka-2025-vision-plc-integration.md] |
| OPC UA | 지원 방식 중 하나. 방식 선택은 PLC 종류, 보낼 데이터 양, 기존 공장 네트워크로 정함 ^[raw/web/roboflow-computer-vision-plc-integration.md] |

PROFINET 등 다른 프로토콜은 아직 출처가 없다.

## 타이밍 예산

카메라 지나서 배출 장치까지 걸리는 시간 안에 다음이 모두 끝나야 한다:
노출, 이미지 전송, 추론, 후처리, PLC 통신, PLC 스캔 타임, 액추에이터 응답,
안전 여유. ^[raw/web/roboflow-computer-vision-plc-integration.md]

- 클라우드 전송은 지연과 변동을 키운다. 실시간 배출에는 엣지 처리가 유리하다.
  ^[raw/web/roboflow-computer-vision-plc-integration.md]
- 사례 논문의 측정 응답시간: 단순 검사 평균 54.7ms, 분류 검사 평균 58.9ms.
  ^[raw/papers/maslanka-2025-vision-plc-integration.md]

## 과검 줄이는 PLC 로직

- 연속 3회 검사 결과를 버퍼에 담고 PLC가 다수결과 조정 가능한 임계값으로
  최종 OK/NG를 정했다. ^[raw/papers/maslanka-2025-vision-plc-integration.md]
- 카메라 단독 대비 과검률이 7.5%에서 5.4%로 줄었다.
  ^[raw/papers/maslanka-2025-vision-plc-integration.md]
- 작업자가 HMI에서 공차와 품종을 바꿀 수 있게 했다.
  ^[raw/papers/maslanka-2025-vision-plc-integration.md]
- 주의: 같은 부품을 3번 찍으려면 촬영 시간이 늘어난다. 택트타임 안에
  들어오는지 확인해야 한다(제안).

## 배출 조건 (예시)

비전 NG 신호, 부품이 배출 위치에 도착, 배출 장치 준비 완료가 **모두 참일 때만**
솔레노이드를 작동한다. ^[raw/web/roboflow-computer-vision-plc-integration.md]

## 현장 강건성

- 주변광 ±20% 변화와 렌즈 커버 먼지 조건에서도 정확도 93% 이상을 유지했지만,
  조명이 흔들릴 때 과검이 2~3% 늘었다.
  ^[raw/papers/maslanka-2025-vision-plc-integration.md]
- 양산 적용에는 차광 케이스와 자동 게인 조정을 권고했다.
  ^[raw/papers/maslanka-2025-vision-plc-integration.md]

## 관련 지식

- [[queries/vision-inspection-introduction-guide|비전검사 공정 도입 가이드]]
- [[concepts/machine-vision-lighting|Machine Vision Lighting]]
- [[concepts/concept-drift|Concept Drift]]

## TODO

- 엔코더 기반 부품 추적(shift register/FIFO) 출처를 수집한다.
- PROFINET, 국내 PLC(LS, 미쓰비시) 연동 사례를 수집한다.
