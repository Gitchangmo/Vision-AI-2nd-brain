---
title: "Attribute Agreement Analysis"
type: concept
status: draft
tags:
  - quality/msa
  - metric/false-positive-rate
sources:
  - raw/web/minitab-attribute-agreement-analysis-overview.md
created: 2026-10-20
updated: 2026-10-20
---

# Attribute Agreement Analysis

합격/불합격처럼 측정값이 아닌 판정(계수형 데이터)을 내리는 검사자가
얼마나 일관되고 정확한지 평가하는 측정시스템분석(MSA) 방법이다.

## 핵심

- 계수형 데이터는 직접적인 물리 측정이 아니라 평가자의 주관적 판정이다.
  ^[raw/web/minitab-attribute-agreement-analysis-overview.md]
- 판정 유형은 이진(pass/fail), 순서형(1~10 척도), 명목형(색상 범주)이 있다.
  ^[raw/web/minitab-attribute-agreement-analysis-overview.md]
- 세 가지 일치성을 본다: 평가자 자신과의 일치(반복성), 평가자 간 일치,
  알려진 기준(표준)과의 일치.
  ^[raw/web/minitab-attribute-agreement-analysis-overview.md]

## 비전검사 도입에서 쓰는 이유 (적용 제안)

아래는 출처의 정의를 비전검사에 적용한 제안이다.

- 도입 전 현행 육안검사의 기준선(baseline)을 숫자로 남긴다.
  사람끼리도 판정이 갈리는 불량은 AI 학습 라벨도 흔들린다.
- 비전 시스템을 하나의 "평가자"로 보고 같은 표본 세트로 사람과 비교한다.
- 한도 견본(경계 샘플)을 표본 세트에 꼭 포함한다.

## 관련 지식

- [[queries/vision-inspection-introduction-guide|비전검사 공정 도입 가이드]]
- [[concepts/surface-defect-detection|Surface Defect Detection]]

## TODO

- 표본 수, 반복 횟수, Kappa 판정 기준 등 실무 기준을 AIAG MSA 등 출처로 보강한다.
