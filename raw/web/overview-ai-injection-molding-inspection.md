---
title: "Plastic Injection Molding AI Defect Inspection: A Practical Guide"
publisher: "Overview.ai"
published: 2026-04-30
source_url: "https://www.overview.ai/blog/plastic-injection-molding-ai-defect-inspection/"
related_url: "https://www.overview.ai/applications/molded-part-integrity/"
captured: 2026-10-21
capture_method: "curl download, HTML converted to text, quotes copied from the text"
---

# Capture note

AI 비전 장비를 판매하는 기업의 블로그와 애플리케이션 페이지다. 마케팅 성격이
강하므로 수치 주장은 근거로 쓰지 않는다. 인용은 내려받은 원문 텍스트에서
그대로 복사했다.

# Excerpts — blog (2026-04-30)

- "Most injection molding inspection failures are lighting failures, not
  algorithm failures. Black plastic, glossy surfaces, and complex geometries
  require careful lighting design."
- "Diffuse dome lighting for highly reflective or glossy surfaces."
- "Grazing-angle structured lighting for sink marks, dents, and surface defects."
- "Backlighting for transparent or translucent parts to detect voids and
  inclusions."
- "Coaxial lighting for highly specular surfaces where reflections need to be
  controlled."
- Short shots: "Easy to detect by silhouette comparison against a known-good
  baseline."
- Weld lines: "Detection approach: surface texture classifier with
  location-aware thresholding (some weld lines are acceptable in non-visible
  regions)."

# Excerpts — application page (molded-part-integrity)

- Sink Marks: "Using specific lighting (like a dome light), cameras can
  highlight these subtle topographical changes that are difficult to see with
  the naked eye."
  (블로그는 싱크마크에 grazing-angle 조명을, 이 페이지는 돔 조명을 예로 든다.)
- "Internal voids with no surface consequence are the honest exception, since
  a camera sees the surface."
- "A glossy surface reflects its surroundings, so a highlight can look like a
  mark and a real defect can vanish into one. Texture adds its own busy pattern
  that a fixed threshold reads as noise. Controlled lighting deals with the
  gloss, usually diffuse or at an angle chosen so the specular return misses
  the lens."
