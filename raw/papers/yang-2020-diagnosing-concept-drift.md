---
title: "Diagnosing Concept Drift with Visual Analytics"
authors:
  - Weikai Yang
  - Zhen Li
  - Mengchen Liu
  - Yafeng Lu
  - Kelei Cao
  - Ross Maciejewski
  - Shixia Liu
year: 2020
venue: "arXiv preprint (v3)"
arxiv: "2007.14372"
source_url: "https://arxiv.org/abs/2007.14372"
captured: 2026-10-21
---

# Provenance

- arXiv:2007.14372v3 (2020-09-15) PDF, text extracted locally with `pdftotext`.
- 검색 요약에 나온 메인보드 높이 변화 사례는 원문 텍스트에서 확인되지 않아
  기록하지 않았다.

# Verified excerpts

- "Concept drift is a phenomenon in which the distribution of a data stream
  changes over time in unforeseen ways, causing prediction models built on
  historical data to become inaccurate." (Abstract)
- "Error-rate-based methods and data-distributionbased methods are the most
  popular drift detection methods." (§2 Related Work)
- "These methods are less efficient in practice as it is often challenging to
  acquire high-quality data labels for calculating the error rate of streaming
  data." (§2, error-rate-based methods에 대해)
- "In our system, we utilize a distribution-based concept drift detection
  method, as these methods do not need ground-truth labels." (§2)
- "E2 focuses on predicting whether a computer motherboard meets the quality
  standards for a computer manufacturing company, Inventec." (§3)
- "A central problem each of these experts faces after deploying a machine
  learning model is how to monitor the model performance over time and decide
  when the model needs to be updated if an unsatisfactory performance is
  identified." (§3)
