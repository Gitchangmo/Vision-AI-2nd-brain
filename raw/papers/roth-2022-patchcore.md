---
title: "Towards Total Recall in Industrial Anomaly Detection"
authors:
  - Karsten Roth
  - Latha Pemula
  - Joaquin Zepeda
  - Bernhard Schölkopf
  - Thomas Brox
  - Peter Gehler
year: 2022
venue: "Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)"
pages: "14318-14328"
source_url: "https://openaccess.thecvf.com/content/CVPR2022/papers/Roth_Towards_Total_Recall_in_Industrial_Anomaly_Detection_CVPR_2022_paper.pdf"
arxiv: "2106.08265"
code_url: "https://github.com/amazon-science/patchcore-inspection"
captured: 2026-08-25
---

# Abstract

Being able to spot defective parts is a critical component in large-scale industrial manufacturing. A particular challenge that we address in this work is the cold-start problem: fit a model using nominal (non-defective) example images only. While handcrafted solutions per class are possible, the goal is to build systems that work well simultaneously on many different tasks automatically. The best performing approaches combine embeddings from ImageNet models with an outlier detection model. In this paper, we extend on this line of work and propose PatchCore, which uses a maximally representative memory bank of nominal patch-features. PatchCore offers competitive inference times while achieving state-of-the-art performance for both detection and localization. On the challenging, widely used MVTec AD benchmark PatchCore achieves an image-level anomaly detection AUROC score of up to 99.6%, more than halving the error compared to the next best competitor. We further report competitive results on two additional datasets and also find competitive results in the few samples regime. Code: github.com/amazon-research/patchcore-inspection.

# Provenance

- CVPR Open Access: https://openaccess.thecvf.com/content/CVPR2022/html/Roth_Towards_Total_Recall_in_Industrial_Anomaly_Detection_CVPR_2022_paper.html
- arXiv: https://arxiv.org/abs/2106.08265
- Captured from the official CVPR Open Access record and arXiv metadata on 2026-08-25.

# Verified excerpts

- PatchCore는 정상 이미지의 locally aggregated, mid-level patch feature를
  memory bank에 저장해 정상 패턴의 정보를 최대한 유지하려고 한다.
  (Paper §1, p. 14319)

- memory bank가 커지면 저장 공간과 추론 시간이 증가하므로,
  greedy coreset subsampling으로 중복을 줄이고 feature-space coverage를
  보존한다. (Paper §3.2, p. 14321)

- 테스트 시 PatchCore는 입력 이미지의 patch feature와 memory bank의
  최근접 이웃 간 거리를 사용해 anomaly score를 계산한다.
  이미지 점수는 가장 이상적인 patch의 거리와 이웃 기반 재가중치를
  사용한다. (Paper §3.3, p. 14321)

- MVTec AD는 15개 하위 데이터셋, 총 5,354개 이미지를 포함하며,
  각 하위 데이터셋은 정상 전용 학습 데이터와 정상·이상 샘플이 섞인
  테스트 데이터로 구성된다. (Paper §4.1, p. 14322)

- 논문 표 1에서 PatchCore-25%는 MVTec AD image-level AUROC 99.1%,
  PatchCore-10%와 PatchCore-1%는 각각 99.0%를 보고했다.
  (Paper Table 1, p. 14323)

- 논문은 PatchCore의 한계로, ImageNet 사전학습 feature의 전이 가능성에
  적용 성능이 제한된다고 명시한다. (Paper §5 Limitations, p. 14325)
