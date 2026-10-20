---
title: "비전검사 공정 도입 가이드"
type: query
status: draft
tags:
  - process/introduction
  - hardware/lighting
  - constraint/low-data
  - metric/false-positive-rate
sources:
  - raw/papers/bergmann-2019-mvtec-ad.md
  - raw/papers/martin-2021-surface-defect-detection-strategies.md
  - raw/web/advanced-illumination-practical-guide-machine-vision-lighting.md
  - raw/web/keyence-machine-vision-lighting-selection.md
  - raw/web/minitab-attribute-agreement-analysis-overview.md
  - raw/web/fictiv-injection-molding-defects.md
  - raw/web/anomalib-documentation.md
  - raw/web/mvtec-ad-dataset-page.md
created: 2026-10-20
updated: 2026-10-20
---

# 비전검사 공정 도입 가이드

> **질문**: 새 공정(사출, 고무 압착 등)에 비전검사를 도입할 때
> 무엇을, 어떤 순서로 검토해야 하나?

제품을 가리지 않는 일반 절차다. 각 단계는 **목적 → 할 일 → 통과 기준**
순서로 정리했다. 출처 표시(^[...])가 없는 문장은 정리자의 제안이며
현장 경험으로 검증·수정해야 한다.

## 전체 흐름

```text
1 요구사항 정의 → 2 현행 검사 기준선 → 3 광학 타당성 검토
→ 4 방식 선택 → 5 데이터·라벨링 → 6 PoC 평가 → 7 라인 파일럿 → 8 양산 이관·운영
```

## 1단계. 요구사항 정의

**목적**: "무엇을 불량으로 볼지"를 문서로 고정한다.

- 불량 정의서: 불량 유형, 위치, 최소 크기, 한도 견본(OK/NG 경계 샘플).
  사출이면 [[concepts/injection-molding-defects|Injection Molding Defects]]의
  10종을 출발 목록으로 쓴다. ^[raw/web/fictiv-injection-molding-defects.md]
- 생산 조건: 택트타임, 부품 공급 방식(컨베이어, 로봇, 회전), 검사면 수.
- 판정 정책: 미검(불량 유출)과 과검(양품 폐기) 중 무엇을 더 줄여야 하는지,
  목표 수치는 얼마인지.
- 연동: NG 배출 방식, PLC/MES 신호, 결과 이미지 보관 기간.

**통과 기준**: 불량 정의서와 목표 미검률·과검률에 품질·생산 부서가 서명.

## 2단계. 현행 검사 기준선 측정

**목적**: 비교 기준이 없으면 도입 효과를 증명할 수 없다.

- 현행 육안검사자를 대상으로
  [[concepts/attribute-agreement-analysis|Attribute Agreement Analysis]]를
  수행한다. 검사자 자신, 검사자 간, 기준 대비 일치성을 본다.
  ^[raw/web/minitab-attribute-agreement-analysis-overview.md]
- 사람끼리 판정이 갈리는 불량 유형을 따로 표시한다. 이 유형은 정의서를
  다시 다듬거나 AI 라벨링에서 특별 관리한다.
- 같은 표본 세트를 보관해 두고 6단계에서 비전 시스템 평가에 재사용한다.

**통과 기준**: 기준선 수치 확보, 판정 불일치 유형 목록 작성.

## 3단계. 광학 타당성 검토 (가장 먼저, 가장 중요)

**목적**: 불량이 **이미지에서 보이는지** 확인한다. 안 보이면 어떤
알고리즘도 못 찾는다.

- 조명은 역사적으로 가장 나중에 정해지던 요소였다. 체계적 조명 분석을
  먼저 한다. ^[raw/web/advanced-illumination-practical-guide-machine-vision-lighting.md]
- 불량 유형별로 조명을 바꿔가며 실제 샘플을 촬영한다.
  [[concepts/machine-vision-lighting|Machine Vision Lighting]] 참고.
  출처가 직접 말하는 근거:
  - 저각 조명은 스크래치·질감 변화를 어두운 배경 위에 드러낸다.
    ^[raw/web/keyence-machine-vision-lighting-selection.md]
  - 돔 조명은 여러 방향에서 빛을 비춘다.
    ^[raw/web/advanced-illumination-practical-guide-machine-vision-lighting.md]
  - 백라이트는 밝은 배경에 어두운 실루엣을 만든다.
    ^[raw/web/advanced-illumination-practical-guide-machine-vision-lighting.md]
  - 물체 색의 보색 조명을 쓰면 물체가 거의 검게 보여 대비가 커진다.
    ^[raw/web/keyence-machine-vision-lighting-selection.md]

  사출 불량에 대입한 시작 가설(출처 없음, 샘플로 검증 필요):
  싱크마크·웰드라인 → 저각 조명, 쇼트샷·플래시 → 백라이트 외곽 검사,
  반짝이는 곡면 → 돔 조명, 변색 → 보색 조명 또는 컬러 카메라.
- 해상도: 최소 불량 크기가 이미지에서 몇 픽셀인지 계산한다.
  불량이 부품보다 매우 작으면 부품을 구간으로 나눠 촬영한다.
  고무 성형품 사례는 부품을 회전시키며 부품당 약 135장을 찍었다.
  ^[raw/papers/martin-2021-surface-defect-detection-strategies.md]
- 외란광(천장 조명, 햇빛)을 차광·필터로 막는다.
  ^[raw/web/advanced-illumination-practical-guide-machine-vision-lighting.md]
- 공간 제약(설치 거리, 간섭)을 현장에서 확인한다.
  ^[raw/web/advanced-illumination-practical-guide-machine-vision-lighting.md]

**통과 기준**: 모든 필수 불량 유형이 사람 눈으로 이미지에서 구분됨.
안 보이는 유형은 범위에서 빼거나 다른 센서(3D, 투과 등)를 검토.

## 4단계. 검사 방식 선택

| 상황 | 우선 후보 | 근거 |
| --- | --- | --- |
| 치수·위치·유무, 형상이 일정 | 룰 기반(측정, 패턴 매칭) | 제안(출처 미수집). 참고로 픽셀 비교형 고전 방법인 variation model은 사전 정렬이 필요했다 ^[raw/papers/bergmann-2019-mvtec-ad.md] |
| 불량 샘플이 거의 없음, 불량 종류를 미리 모름 | 이상 탐지(정상만 학습) | ^[raw/papers/bergmann-2019-mvtec-ad.md] |
| 불량 샘플 수집 가능, 유형별 구분 필요 | 지도학습 분류·분할 | ^[raw/papers/martin-2021-surface-defect-detection-strategies.md] |

- 이상 탐지는 제조 공정에서 어떤 불량이 생길지 미리 모르는 경우가 많고,
  불량 이미지가 매우 적기 때문에 유용하다.
  ^[raw/papers/bergmann-2019-mvtec-ad.md]
  대표 방법은 [[concepts/patchcore|PatchCore]],
  개념은 [[concepts/industrial-anomaly-detection|Industrial Anomaly Detection]].
- 지도학습은 [[concepts/surface-defect-detection|Surface Defect Detection]] 참고.
  출력 형태(이진·다중·분할)는 현장이 필요로 하는 정보에 맞춰 고른다.
  ^[raw/papers/martin-2021-surface-defect-detection-strategies.md]
- 실무에서는 섞어 쓰는 경우가 많다. 예: 룰 기반으로 위치를 잡고,
  AI로 표면을 판정.

## 5단계. 데이터 수집·라벨링

- 촬영 조건(조명, 거리, 노출)을 3단계에서 확정한 값으로 고정한 뒤 수집한다.
- 정상 데이터: 로트·금형 캐비티·소재 변동을 포함한다.
- 불량 데이터: 매우 불균형하다. 고무 사례는 결함 이미지가 약 1.5%였고
  undersampling으로 균형을 맞췄다.
  ^[raw/papers/martin-2021-surface-defect-detection-strategies.md]
- 데이터가 적으면 사전학습 가중치를 쓴다. 고무 사례에서 ImageNet
  사전학습과 데이터 증강을 함께 적용하자 정확도가 0.664에서 0.974로 올랐다.
  ^[raw/papers/martin-2021-surface-defect-detection-strategies.md]
- 라벨링 기준서를 만들고, 2단계에서 판정이 갈린 유형은 여러 명이
  교차 검토한다.

## 6단계. PoC 평가

- 학습/검증/평가 데이터를 섞지 않는다. 평가셋에 한도 견본을 포함한다.
- 지표는 정확도만 보지 말고 미검률·과검률(혼동행렬)로 본다.
  불균형 데이터에서는 F1도 함께 본다.
  ^[raw/papers/martin-2021-surface-defect-detection-strategies.md]
- **AUROC가 높아도 실제 임계값 판정은 실패할 수 있다.** 정상 이미지만으로
  좋은 임계값을 정하기는 어렵다.
  ^[raw/papers/bergmann-2019-mvtec-ad.md]
  → 임계값은 별도 검증셋으로 정하고, 최소 결함 면적 같은 현장 기준을 같이 쓴다.
  ^[raw/papers/bergmann-2019-mvtec-ad.md]
- 어떤 방법도 모든 대상에서 고르게 잘하지 않았다. 여러 모델을 비교한다.
  ^[raw/papers/bergmann-2019-mvtec-ad.md]
  이상 탐지 모델 비교에는 [[entities/anomalib|Anomalib]]을 쓸 수 있다.
  ^[raw/web/anomalib-documentation.md]
- 공개 데이터셋 [[concepts/mvtec-ad|MVTec AD]]는 비상업 라이선스다.
  사내 제품 모델 학습에 쓰기 전 확인한다. ^[raw/web/mvtec-ad-dataset-page.md]
- 2단계의 육안 기준선과 같은 표본으로 비교한다.

**통과 기준**: 목표 미검률·과검률 달성, 택트타임 내 추론.

## 7단계. 라인 파일럿

- 실제 라인에서 기존 검사와 병행 운영(shadow mode)한다.
- 검사자가 결과를 신뢰할 수 있게 판정 근거(히트맵, 결함 위치)를 보여준다.
  고무 사례의 검사자들도 판정 근거 추적 가능성을 중요하게 봤다.
  ^[raw/papers/martin-2021-surface-defect-detection-strategies.md]
- 연구실 결과와 라인 결과는 다르다. 진동, 오염, 외란광, 부품 자세 변동을
  기록한다.
- 과검 이미지를 모아 재학습·임계값 조정에 쓴다.

**통과 기준**: 정해진 기간 동안 목표 성능 유지, 생산 부서 승인.

## 8단계. 양산 이관·운영

- 기준 이미지·한도 견본·조명 세팅값을 문서로 남긴다.
- 금형 수정, 소재 변경, 신규 캐비티 투입 시 재검증 절차를 정한다.
- 정기 점검: 조명 밝기 저하, 렌즈 오염, 카메라 위치 틀어짐.
- 과검·미검 사례를 계속 쌓아 모델을 개선한다.

## 단계별 체크리스트

- [ ] 불량 정의서·한도 견본 확정
- [ ] 목표 미검률·과검률·택트타임 합의
- [ ] 현행 육안검사 일치성 기준선 측정
- [ ] 불량 유형별 조명·해상도 테스트 완료
- [ ] 검사 방식(룰/이상 탐지/지도학습) 결정과 근거 기록
- [ ] 촬영 조건 고정 후 데이터 수집, 라벨 기준서 작성
- [ ] PoC: 혼동행렬, 임계값 결정 근거, 추론 시간
- [ ] 라인 병행 운영 결과와 과검 원인 분석
- [ ] 운영·재검증 절차 문서화

## 관련 지식

- [[concepts/machine-vision-lighting|Machine Vision Lighting]]
- [[concepts/injection-molding-defects|Injection Molding Defects]]
- [[concepts/attribute-agreement-analysis|Attribute Agreement Analysis]]
- [[concepts/surface-defect-detection|Surface Defect Detection]]
- [[concepts/industrial-anomaly-detection|Industrial Anomaly Detection]]

## 보강할 자료 (TODO)

- 고무 압착 성형 불량 유형 출처
- 룰 기반 vs 딥러닝 선택 기준 (벤더·중립 출처)
- 카메라·렌즈 선정 (해상도, 시야, 작동 거리 계산)
- 엣지 추론과 PLC 연동 사례
- 양산 후 데이터 드리프트·재학습 운영 사례
- 본인 현장 경험 메모 (`raw/` 기록으로 남기면 이 가이드의 근거가 됨)
