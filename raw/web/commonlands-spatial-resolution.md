---
title: "Spatial Resolution in Machine Vision | mm per Pixel"
publisher: "Commonlands Optics"
published: 2026-05-20
source_url: "https://commonlands.com/blogs/technical/spatial-resolution-machine-vision"
captured: 2026-10-21
capture_method: "curl download, HTML converted to text, quotes copied from the text"
---

# Capture note

렌즈 제조사의 기술 블로그다. 인용은 내려받은 원문 텍스트에서 그대로 복사했다.

# Excerpts

- "Spatial resolution is the real-world size one pixel samples at the working
  distance: the sampling interval, not the smallest feature the system can
  resolve."
- "The sampling needed for detection or measurement depends on feature
  contrast, blur, noise, sampling phase, and the algorithm. Establish it with
  representative targets and an acceptance test."
- "Pixel math sets the ceiling, not the result."
- "Minimum detectable size is the smallest feature a system reliably
  identifies. Multiply spatial resolution by the pixel coverage the task needs:
  minimum size = (FOV ÷ pixel count) × required pixels."
- "Production inspection typically needs 3 to 5 pixels across a defect, and
  measurement 10 or more. Both are starting heuristics moved by contrast, SNR,
  and algorithm."
- "Because real-world contrast, noise, and blur are worse than on the bench,
  many teams carry a 2× to 3× design margin over the theoretical minimum pixel
  count."
- "Coverage is the second requirement: the lens image circle must be at least
  the sensor diagonal, or the corners vignette."
