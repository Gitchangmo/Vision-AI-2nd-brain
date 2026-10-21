---
title: "Integration of Machine Vision and PLC-Based Control for Scalable Quality Inspection in Industry 4.0"
authors:
  - Maksymilian Maślanka
  - Daniel Jancarczyk
  - Jacek Rysinski
year: 2025
venue: "Sensors (Basel), 25(20):6383"
doi: "10.3390/s25206383"
license: "CC BY 4.0"
source_url: "https://pmc.ncbi.nlm.nih.gov/articles/PMC12568163/"
captured: 2026-10-21
---

# Abstract

The integration of machine vision systems with programmable logic controllers (PLCs) is increasingly crucial for automated quality assurance in Industry 4.0 environments. This paper presents an applied case study of vision–PLC integration, focusing on real-time synchronization, deterministic communication, and practical industrial deployment. The proposed platform combines a Cognex In-Sight 2802C smart camera (Cognex Corporation, Natick, MA, USA) with an Allen-Bradley Compact GuardLogix PLC through Ethernet/IP implicit cyclic exchange. Three representative case studies were investigated: 3D-printed prototypes with controlled defects, automotive electrical connectors inspected using Cognex ViDi supervised learning tools, and fiber optic tubes evaluated via a custom fixture-based heuristic method. Across all scenarios, detection accuracy exceeded 95%, while PLC-level triple verification reduced false classifications by 28% compared to camera-only operation. The work highlights the benefits of PLC-driven inspection, including robustness, real-time performance, and dynamic tolerance adjustment via HMI interfaces. At the same time, several limitations were identified, including sensitivity to lighting variations, limited dataset size, and challenges in scaling to full production environments. These findings demonstrate a replicable integration framework that supports intelligent manufacturing. Future research will focus on hybrid AI–PLC architectures, extended validation on industrial production lines, and predictive maintenance enabled by edge computing.

# Provenance

- PubMed Central full text (open access, CC BY 4.0), downloaded with curl and
  converted to text on 2026-10-21.

# Verified excerpts

- "The PLC handled image acquisition triggers, buffered inspection results, and
  implemented verification logic." (§3 Materials and Methods)
- "The vision system functioned as an Ethernet/IP adapter, while the PLC acted
  as the master." (§3)
- "In order to enable triggering via the Ethernet/IP protocol, the variable
  In-Sight_Out.Control.TriggerEnable had to be manually set to a logical “1”."
  (§3)
- "In this approach, inspection results from three consecutive vision cycles
  are buffered and then re-evaluated by PLC logic. The algorithm determines the
  final classification (OK/NOK) based on majority voting and adjustable
  thresholds, reducing the occurrence of false positives." (§3)
- "Additionally, the operator can dynamically modify tolerance limits or switch
  product types via the HMI interface." (§3)
- 커넥터 사례(Case Study 2)는 short shot, pin 관련 결함 등으로 부품을 묶어
  지도학습했고, 카테고리당 약 40장으로 안정화된 뒤 카테고리당 100장(총 300장)
  추가 학습으로 정확도 95%에 도달했다. 과검은 주로 금속 표면의 조명 반사에서
  발생했다: "occasional false positives occurred, primarily due to lighting
  reflections on metallic surfaces." (§4)
- 광섬유 튜브 사례(Case Study 3): 600개 시료, 결함은 collar 누락, short shot,
  내부 기포, flash. "Overall accuracy was 95.2%" (§4)
- "Specifically, the baseline system yielded an average false-positive rate of
  7.5%, while the integrated PLC verification reduced it to 5.4%" (§5)
- "Latency measurements revealed a mean response time of 54.7 ms (σ = 6.3 ms)
  for simple inspections (3D-printed holders) and 58.9 ms (σ = 8.1 ms) for
  complex classification tasks (electrical connectors)." (§5)
- "The system maintained >93% accuracy under all conditions, though false
  positives increased marginally (by 2–3%) in cases of fluctuating lighting."
  (§5, ±20% 주변광 변화와 렌즈 커버 먼지 조건)
- "for deployment in full-scale production, enclosure-based shielding and
  automatic gain adjustment are recommended." (§5)
