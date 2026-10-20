---
title: "MVTec AD — A Comprehensive Real-World Dataset for Unsupervised Anomaly Detection"
authors:
  - Paul Bergmann
  - Michael Fauser
  - David Sattlegger
  - Carsten Steger
year: 2019
venue: "Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)"
pages: "9592-9600"
source_url: "https://openaccess.thecvf.com/content_CVPR_2019/papers/Bergmann_MVTec_AD_--_A_Comprehensive_Real-World_Dataset_for_Unsupervised_Anomaly_CVPR_2019_paper.pdf"
captured: 2026-10-20
---

# Abstract

The detection of anomalous structures in natural image data is of utmost importance for numerous tasks in the field of computer vision. The development of methods for unsupervised anomaly detection requires data on which to train and evaluate new approaches and ideas. We introduce the MVTec Anomaly Detection (MVTec AD) dataset containing 5354 high-resolution color images of different object and texture categories. It contains normal, i.e., defect-free, images intended for training and images with anomalies intended for testing. The anomalies manifest themselves in the form of over 70 different types of defects such as scratches, dents, contaminations, and various structural changes. In addition, we provide pixel-precise ground truth regions for all anomalies. We also conduct a thorough evaluation of current state-of-the-art unsupervised anomaly detection methods based on deep architectures such as convolutional autoencoders, generative adversarial networks, and feature descriptors using pre-trained convolutional neural networks, as well as classical computer vision methods. This initial benchmark indicates that there is considerable room for improvement. To the best of our knowledge, this is the first comprehensive, multi-object, multi-defect dataset for anomaly detection that provides pixel-accurate ground truth regions and focuses on real-world applications.

# Provenance

- CVPR 2019 Open Access PDF (URL above).
- Text extracted locally with `pdftotext` from the downloaded PDF on 2026-10-20.

# Verified excerpts

- "Unsupervised methods play a significant role here since it is often unknown
  beforehand what types of defects might occur during manufacturing."
  (§1 Introduction)

- "In addition, industrial processes are optimized to produce a minimum amount
  of defective samples. Therefore, only a very limited amount of images with
  defects is available, in contrast to a vast amount of defectfree samples that
  can be used for training." (§1 Introduction)

- "The MVTec Anomaly Detection dataset comprises 15 categories with 3629 images
  for training and validation and 1725 images for testing. The training set
  contains only images without defects." (§3 Dataset Description)

- "Five categories cover different types of regular (carpet, grid) or random
  (leather, tile, wood) textures, while the remaining ten categories represent
  various types of objects." (§3 Dataset Description)

- "In total, 73 different defect types are present, on average five per
  category." (§3 Dataset Description)

- "All images were acquired using a 2048 × 2048 pixel high-resolution
  industrial RGB sensor in combination with two bilateral telecentric lenses
  [...] The images were acquired under highly controlled illumination
  conditions." (§3 Dataset Description)

- 고전적 기준선인 variation model은 객체 윤곽의 사전 정렬이 필요하며,
  픽셀별 평균·표준편차로 정상 밝기 통계를 모델링한다. 정렬이 거의
  픽셀 단위로 가능하지 않은 객체에는 적용 범위를 제한했다. (§4.1.5 Variation Model)

- 결함 영역 판정 임계값은 학습에서 제외한 정상 검증 이미지만으로 추정했다.
  카테고리별 최소 결함 면적을 정하고, 정상 검증셋에서 가장 큰 이상 영역이
  그 면적 바로 아래가 될 때까지 임계값을 올린다. (§4.3 Evaluation Metric)

- "None of the methods manages to consistently perform well across all object
  and texture classes." (§4.4 Results)

- "Table 3 shows that a high ROC AUC does not necessarily coincide with a high
  per-region overlap of the segmentation for the estimated threshold." /
  "This highlights the difficulty in trying to find a good threshold based
  solely on a set of anomaly-free images." (§4.4 Results)
