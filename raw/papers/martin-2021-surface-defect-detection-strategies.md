---
title: "Deep Learning Strategies for Industrial Surface Defect Detection Systems"
authors:
  - Dominik Martin
  - Simon Heinzel
  - Johannes Kunze von Bischhoffshausen
  - Niklas Kühl
year: 2021
venue: "55th Hawaii International Conference on System Sciences (HICSS-55)"
arxiv: "2109.11304"
source_url: "https://arxiv.org/abs/2109.11304"
captured: 2026-10-20
---

# Abstract

Deep learning methods have proven to outperform traditional computer vision methods in various areas of image processing. However, the application of deep learning in industrial surface defect detection systems is challenging due to the insufficient amount of training data, the expensive data generation process, the small size, and the rare occurrence of surface defects. From literature and a polymer products manufacturing use case, we identify design requirements which reflect the aforementioned challenges. Addressing these, we conceptualize design principles and features informed by deep learning research. Finally, we instantiate and evaluate the gained design knowledge in the form of actionable guidelines and strategies based on an industrial surface defect detection use case. This article, therefore, contributes to academia as well as practice by (1) systematically identifying challenges for the industrial application of deep learning-based surface defect detection, (2) strategies to overcome these, and (3) an experimental case study assessing the strategies' applicability and usefulness.

# Provenance

- arXiv abstract page and PDF (arXiv:2109.11304v1, 2021-09-23).
- Text extracted locally with `pdftotext` from the downloaded PDF on 2026-10-20.
- Author affiliation: Johannes Kunze von Bischhoffshausen is listed with Trelleborg Sealing Solutions Germany GmbH.
  The paper does not name the case company.

# Verified excerpts

- 설계 요구사항(§3.2):
  - "DR1: Industrial surface defect detection systems should be able to detect very small defects."
  - "DR2: Industrial surface defect detection systems should be able to detect rarely occurring defects."
  - "DR3: The decisions of industrial surface defect detection systems should be explainable."
  - "DR4: Industrial surface defect detection systems should be able to learn from small amounts of training data."

- 설계 원칙(§4):
  - "DP1: Provide the system with segment-wise examination capabilities."
  - "DP2: Provide the system with data balancing functions."
  - "DP3: Provide the system with mechanisms to address the appropriate information needs of the users based on the objectives and priorities of the specific use case."
  - "DP4: Provide the system with knowledge transfer functions to utilize shared features from other models."
  - "DP5: Provide the system with regularization mechanisms to to prevent the model from overfitting."

- "Datasets from manufacturing processes are often highly imbalanced due to the
  deliberately low probability of defect occurrences." (§3.2)

- "The quality inspectors in our use case also emphasize the importance of
  trusting deep learning methods because their model decisions as such are
  untraceable" (§3.2)

- 사례 대상은 engineered molded parts(고무 성형품)이며, 기존에는 작업자가
  확대경으로 100% 수작업 검사했다. 일반 O-ring보다 지름이 훨씬 커서
  형상이 고정되지 않아 자동화가 어렵다. (§6.1)

- 모터로 부품을 회전시키며 부품당 약 135장의 약간 겹치는 그레이스케일
  이미지(약 25MP)를 촬영했다. 결함 부품 324개, 결함 유형 5종, 원시
  이미지 43,740장 중 결함 포함 이미지는 약 1.5%였고, undersampling 후
  최종 데이터셋은 1,280장이었다. (§6.1)

- 이진 분류 실험에서 무작위 초기화(E1) 정확도 0.664, ImageNet 사전학습(E2)
  0.974, 강판 결함 Kaggle 데이터 사전학습(E3) 0.977을 보고했다.
  E2와 E3에는 데이터 증강(flip, zoom, shift)도 적용했다:
  "In experiments E2 and E3, we apply data augmentation by randomly flipping,
  zooming, and shifting the images (DF12)." (§6.2)
  (§6.3 Evaluation, Table 2)

- "For practitioners, the key finding is that already a generic knowledge
  transfer leads to significant performance improvements." (§7 Discussion)

- 분할 모델(E8)은 다중 분류 모델(E6)과 정확도는 같았지만 precision,
  recall, F1은 더 높았으며, 저자들은 픽셀 단위 라벨이 더 많은 학습 신호를
  제공했을 가능성을 제시했다. (§7 Discussion)

- 한계: 단일 사례에서만 평가했고, 실험 수가 제한적이며, 체계적
  하이퍼파라미터 최적화를 수행하지 않았다. (§8 Conclusion)
