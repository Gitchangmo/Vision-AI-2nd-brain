---
title: "Computer Vision PLC Integration: Camera to Machine Action"
publisher: "Roboflow"
author: "Timothy M"
published: 2026-08-03
updated: 2026-10-10
source_url: "https://blog.roboflow.com/computer-vision-plc-integration/"
captured: 2026-10-21
capture_method: "curl download, HTML converted to text, quotes copied from the text"
---

# Capture note

컴퓨터비전 플랫폼 기업의 블로그이며 자사 제품 사용 예시를 포함한다.
인용은 내려받은 원문 텍스트에서 그대로 복사했다.

# Excerpts

- "The vision system decides what happened; the PLC keeps ownership of timing,
  interlocks, and the physical reject, which is what makes the integration
  production-safe."
- "It already knows whether the line is running, whether the reject station is
  available, whether safety interlocks are satisfied, and when an actuator
  should fire."
- "The total system timing also includes camera exposure, image transfer,
  inference, Workflow processing, communication with the PLC, PLC scan time,
  actuator response time, and a safety margin."
- "Sending every frame to a remote cloud server introduces network latency and
  additional variability."
- "A vision system can send inspection results to a PLC using OPC UA, Modbus
  TCP, EtherNet/IP, or digital I/O . The right option depends mainly on the
  PLC, the amount of data being sent, and the existing factory network."
- "Modbus is very widely supported, which often makes it the easiest option on
  older equipment."
- Digital I/O: "This is simple, but it cannot carry richer information such as
  defect class, confidence, counts, or part identifiers."
- 예시 PLC 로직(Structured Text): 비전 reject 신호, 부품이 reject 위치에 도착,
  reject 장치 준비 완료가 모두 참일 때만 솔레노이드를 작동한다.
