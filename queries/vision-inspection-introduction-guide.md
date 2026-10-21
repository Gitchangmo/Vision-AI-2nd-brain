---
title: "비전검사 공정 도입 가이드"
type: query
status: draft
tags:
  - process/introduction
  - hardware/lighting
  - hardware/camera
  - deployment/plc
  - operation/drift-monitoring
  - metric/false-positive-rate
sources:
  - raw/papers/bergmann-2019-mvtec-ad.md
  - raw/papers/martin-2021-surface-defect-detection-strategies.md
  - raw/papers/maslanka-2025-vision-plc-integration.md
  - raw/papers/hinder-2023-concept-drift-survey.md
  - raw/web/advanced-illumination-practical-guide-machine-vision-lighting.md
  - raw/web/keyence-selecting-machine-vision-camera.md
  - raw/web/commonlands-spatial-resolution.md
  - raw/web/minitab-attribute-agreement-analysis-overview.md
  - raw/web/fictiv-injection-molding-defects.md
  - raw/web/overview-ai-injection-molding-inspection.md
  - raw/web/pekat-deep-learning-vs-rule-based.md
  - raw/web/roboflow-computer-vision-plc-integration.md
  - raw/web/anomalib-documentation.md
  - raw/web/mvtec-ad-dataset-page.md
created: 2026-10-20
updated: 2026-10-21
---

# 비전검사 공정 도입 가이드

> **질문**: 새 공정(사출, 고무 압착 등)에 비전검사를 도입할 때
> 무엇을, 어떤 순서로 검토해야 하나?

제품을 가리지 않는 일반 절차다. 세부 내용은 각 단계의 링크 문서에 있다.
출처 표시(^[...])가 없는 문장은 정리자의 제안이며 현장 경험으로 검증해야 한다.

```text
1 요구사항 → 2 현행 기준선 → 3 광학 타당성 → 4 방식 선택
→ 5 데이터·라벨링 → 6 PoC → 7 라인 파일럿(PLC 연동) → 8 양산·운영(드리프트)
```

## 1단계. 요구사항 정의

**목적**: "무엇을 불량으로 볼지"를 문서로 고정한다.

- 불량 정의서: 유형, 위치, 최소 크기, 한도 견본(OK/NG 경계 샘플).
  사출이면 [[concepts/injection-molding-defects|Injection Molding Defects]]의
  10종을 출발 목록으로 쓴다. ^[raw/web/fictiv-injection-molding-defects.md]
- 생산 조건: 택트타임, 부품 공급 방식, 검사면 수.
- 판정 정책: 미검(유출)과 과검(양품 폐기) 중 무엇을 더 줄일지, 목표 수치.
- 연동: NG 배출 방식, PLC/MES 신호, 결과 이미지 보관 기간.

**통과 기준**: 불량 정의서와 목표 미검률·과검률에 품질·생산 부서 합의.

## 2단계. 현행 검사 기준선

- 육안검사자 대상
  [[concepts/attribute-agreement-analysis|Attribute Agreement Analysis]]로
  검사자 자신, 검사자 간, 기준 대비 일치성을 잰다.
  ^[raw/web/minitab-attribute-agreement-analysis-overview.md]
- 사람끼리 판정이 갈리는 불량은 정의서를 다듬고 라벨링에서 특별 관리한다.
- 같은 표본 세트를 6단계 평가에 재사용한다.

**통과 기준**: 기준선 수치, 판정 불일치 유형 목록.

## 3단계. 광학 타당성 검토 (가장 중요)

**목적**: 불량이 **이미지에서 보이는지** 확인한다. 안 보이면 어떤 알고리즘도 못 찾는다.

**조명** → [[concepts/machine-vision-lighting|Machine Vision Lighting]]
- 조명은 역사적으로 가장 나중에 정해지던 요소였다. 먼저 분석한다.
  ^[raw/web/advanced-illumination-practical-guide-machine-vision-lighting.md]
- 사출 불량 대부분의 검사 실패는 알고리즘이 아니라 조명 실패라는 벤더 의견이 있다.
  ^[raw/web/overview-ai-injection-molding-inspection.md]
- 불량별 조명 후보(싱크마크 → 저각 또는 돔, 투명 부품 → 백라이트 등)는
  사출 불량 문서에 정리했다. 출처 간에도 갈리므로 샘플로 정한다.
- 외란광(천장 조명, 햇빛)을 차광·필터로 막는다.
  ^[raw/web/advanced-illumination-practical-guide-machine-vision-lighting.md]

**해상도·렌즈** → [[concepts/camera-and-lens-selection|Camera and Lens Selection]]
- 픽셀 분해능 = 시야 ÷ 픽셀 수. 생산 검사는 결함을 가로질러 3~5픽셀을
  출발점으로 삼고, 현장 조건 때문에 2~3배 여유를 둔다.
  ^[raw/web/commonlands-spatial-resolution.md]
- 해상도로 나쁜 조명을 메울 수 없다.
  ^[raw/web/keyence-selecting-machine-vision-camera.md]
- 불량이 부품보다 매우 작으면 구간을 나눠 찍는다. 고무 성형품 사례는 부품을
  회전시키며 부품당 약 135장을 찍었다.
  ^[raw/papers/martin-2021-surface-defect-detection-strategies.md]
- 표면에 흔적이 없는 내부 결함은 카메라로 볼 수 없다.
  ^[raw/web/overview-ai-injection-molding-inspection.md]

**통과 기준**: 필수 불량 유형이 이미지에서 눈으로 구분됨. 안 보이는 유형은
범위에서 빼거나 다른 센서(3D, 투과 등)를 검토.

## 4단계. 검사 방식 선택

→ [[comparisons/rule-based-vs-deep-learning-inspection|Rule-Based vs Deep Learning Inspection]]

| 상황 | 우선 후보 |
| --- | --- |
| 치수·정렬·유무, 형상 일정, 기준 명확 | 룰 기반 ^[raw/web/pekat-deep-learning-vs-rule-based.md] |
| 불량이 드물거나 처음 보거나 정의하기 어려움 | 이상 탐지 ^[raw/web/pekat-deep-learning-vs-rule-based.md] |
| 불량 샘플 수집 가능, 유형 구분 필요 | 지도학습 분류·분할 ^[raw/papers/martin-2021-surface-defect-detection-strategies.md] |

- 실무에서는 섞어 쓴다. 예: 룰 기반으로 위치를 잡고 딥러닝으로 결함 판정.
  ^[raw/web/pekat-deep-learning-vs-rule-based.md]
- 이상 탐지 방법은 [[concepts/patchcore|PatchCore]],
  지도학습은 [[concepts/surface-defect-detection|Surface Defect Detection]] 참고.

## 5단계. 데이터 수집·라벨링

- 3단계에서 확정한 촬영 조건을 고정한 뒤 수집한다.
- 정상 데이터에는 로트·금형 캐비티·소재 변동을 포함한다.
- 불량은 매우 불균형하다. 고무 사례는 결함 이미지가 약 1.5%였다.
  ^[raw/papers/martin-2021-surface-defect-detection-strategies.md]
- 데이터가 적으면 사전학습 가중치와 데이터 증강을 쓴다.
  ^[raw/papers/martin-2021-surface-defect-detection-strategies.md]
- 라벨링 기준서를 만들고, 2단계에서 갈린 유형은 교차 검토한다.

## 6단계. PoC 평가

- 지표는 미검률·과검률(혼동행렬)로 보고, 불균형 데이터는 F1도 본다.
  ^[raw/papers/martin-2021-surface-defect-detection-strategies.md]
- **AUROC가 높아도 임계값 판정은 실패할 수 있다.** 임계값은 별도 검증셋과
  최소 결함 면적 같은 현장 기준으로 정한다.
  ^[raw/papers/bergmann-2019-mvtec-ad.md]
- 여러 모델을 비교한다([[entities/anomalib|Anomalib]] 활용 가능).
  ^[raw/web/anomalib-documentation.md]
- [[concepts/mvtec-ad|MVTec AD]]는 비상업 라이선스다.
  ^[raw/web/mvtec-ad-dataset-page.md]
- 2단계 육안 기준선과 같은 표본으로 비교한다.

**통과 기준**: 목표 미검률·과검률 달성, 택트타임 내 처리.

## 7단계. 라인 파일럿과 PLC 연동

→ [[concepts/vision-plc-integration|Vision–PLC Integration]]

- 비전은 판정, PLC는 타이밍·인터록·배출을 맡는다.
  ^[raw/web/roboflow-computer-vision-plc-integration.md]
- 타이밍 예산: 노출, 전송, 추론, PLC 통신·스캔, 액추에이터 응답, 안전 여유가
  카메라~배출기 이동 시간 안에 끝나야 한다.
  ^[raw/web/roboflow-computer-vision-plc-integration.md]
- PLC에서 연속 3회 결과를 다수결로 판정해 과검률을 7.5%에서 5.4%로 줄인
  사례가 있다. ^[raw/papers/maslanka-2025-vision-plc-integration.md]
- 기존 검사와 병행 운영하고, 판정 근거(히트맵, 결함 위치)를 검사자에게 보여준다.
  ^[raw/papers/martin-2021-surface-defect-detection-strategies.md]
- 주변광 변화에 과검이 늘 수 있어 차광 케이스와 자동 게인 조정이 권고됐다.
  ^[raw/papers/maslanka-2025-vision-plc-integration.md]

**통과 기준**: 정해진 기간 목표 성능 유지, 생산 부서 승인.

## 8단계. 양산 이관·운영

→ [[concepts/concept-drift|Concept Drift]]

- 드리프트는 공정, 환경, 센서 변화로 생긴다. 공정 변화는 불량 신호일 수 있고,
  센서·환경 변화는 장비 교체나 재조정이 필요하다.
  ^[raw/papers/hinder-2023-concept-drift-survey.md]
- 정상 판정 이미지의 밝기·이상 점수 분포를 주기적으로 기록한다(라벨 불필요).
- 금형 수정, 소재 변경, 조명 교체 때 기준 이미지로 재검증한다.
- 재학습 기준을 이관 전에 정하고, 기준 이미지·한도 견본·세팅값을 문서화한다.

## 체크리스트

- [ ] 불량 정의서·한도 견본, 목표 미검률·과검률·택트타임 합의
- [ ] 현행 육안검사 일치성 기준선 측정
- [ ] 불량별 조명 테스트, 해상도·렌즈 계산과 실촬영 확인
- [ ] 검사 방식 결정과 근거 기록
- [ ] 촬영 조건 고정 후 수집, 라벨 기준서
- [ ] PoC: 혼동행렬, 임계값 근거, 처리 시간
- [ ] PLC 신호·타이밍 예산·배출 조건 설계, 병행 운영
- [ ] 드리프트 감시 지표와 재검증·재학습 절차

## 남은 보강 과제

- 고무 압착 성형 불량 유형 출처
- 엔코더 기반 부품 추적, PROFINET·국내 PLC 연동 사례
- 비전검사 양산 드리프트 실측 사례
- 본인 현장 경험 메모 (`raw/` 기록으로 남기면 이 가이드의 근거가 됨)
