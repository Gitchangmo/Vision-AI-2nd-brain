# Wiki Log

> Chronological record of wiki actions. This file is append-only: add entries at
> the end and never rewrite or remove an earlier entry.
>
> Entry heading format: `## [YYYY-MM-DD] <action> | <subject>`
>
> Allowed actions: `ingest`, `create`, `update`, `query`, `lint`, `archive`,
> `delete`, `map`, and `repair`.
>
> Each entry lists every affected repository-relative path. After 500 entries,
> rotate the completed file to `log-YYYY.md` and begin a new `log.md`; preserve the
> completed file unchanged.

## [2026-07-21] ingest | 2nd-Brain 개인지식 관리 원본 배치

- Selection: `understand-chat` identified the 2nd-Brain PKM core subgraph and its one-hop canonical neighbors; their leading frontmatter referenced 13 unique raw sources.
- Created:
  - `raw/notebooklm/2026-07-16-all-notes.md`
  - `raw/notebooklm/codegraph-github.md`
  - `raw/notebooklm/graphify-github.md`
  - `raw/notebooklm/llm-wiki-skill-github.md`
  - `raw/notebooklm/llm-wiki-zotero-notebooklm-youtube.md`
  - `raw/notebooklm/notebooklm-py-github.md`
  - `raw/notebooklm/understand-anything-github.md`
  - `raw/notebooklm/zotero-mcp-github.md`
  - `raw/web/NomaDamasslides-grab Best harness + editor + linter for generating slides in Claude Code  Codex - Claude Design Open Source Alternative.md`
  - `raw/web/stablyaiorca Orca is the ADE for working with a fleet of parallel agents. Run any coding agent with your own subscription. Available on desktop and mobile..md`
  - `raw/youtube/📺 How To Build LLM Wiki In Obsidian 🧠 A Memory Layer For Any Agentic AI.md`
  - `raw/youtube/📺 LLM Wiki를 업그레이드하는 외부 지식 시스템! 연구자를 위한 최강의 조합 Zotero × Notebook × Obsidian x Claude Code.md`
  - `raw/youtube/📺 Orca Is the Free Cursor Killer Nobody's Talking About!.md`
- Updated: `SCHEMA.md`, `AGENTS.md` to register importer-preserved raw directories and legacy hash-coverage handling.
- Integrity: all 13 target files are byte-identical to the source vault; all 8 recorded post-frontmatter body hashes match; 5 legacy web/video captures have no recorded `sha256` and retain their original missing final LF as explicit coverage and format gaps.
- Canonical state: unchanged at 0 pages; `index.md` was not modified.

## [2026-07-21] lint | 0 issues found

- Raw files in the imported source set: 13.
- Source/target byte-identical files: 13.
- Recorded post-frontmatter body hashes checked and matched: 8.
- Documented legacy hash-coverage and final-LF format gaps: 5.
- Invalid UTF-8, BOM, CRLF, body-hash drift, missing ingest-log paths, and unregistered importer directories: 0.
- Canonical pages and index entries: 0; no canonical navigation update was required.

## [2026-07-21] create | 2nd-Brain canonical 지식 코어

- Evidence: the existing 13-file raw source set was mapped to eight central, reusable PKM subjects; no raw record was duplicated or mutated.
- Created:
  - `concepts/ai-knowledge-workflow.md`
  - `concepts/ai-personal-knowledge-management.md`
  - `concepts/llm-wiki.md`
  - `concepts/research-feedback-loop.md`
  - `concepts/second-brain-research-workflow.md`
  - `comparisons/knowledge-tool-roles.md`
  - `queries/notebooklm-query-compounding.md`
  - `queries/ua-knowledge-graph-workflow.md`
- Updated:
  - `SCHEMA.md`
  - `index.md`
  - `log.md`
- Navigation: the eight-page graph uses only resolvable canonical wikilinks, with at least two distinct non-self links per page.
- Provenance: every source and claim marker resolves to an existing repository-relative raw Markdown path.

## [2026-07-21] lint | 0 issues found

- Canonical pages: 8 total (5 concepts, 1 comparison, and 2 queries); all required frontmatter fields, types, dates, confidence values, contestation fields, and contradiction lists are valid.
- Taxonomy and navigation: 9 registered tags, 8 exact alphabetical index entries, 33 canonical links, minimum 3 outbound links per page, and minimum 2 inbound links per page.
- Provenance: 27 source references and 17 claim-level markers resolve to existing raw Markdown records; no marker is absent from its page source list.
- Raw integrity: 13 Markdown records checked, 8 recorded body hashes matched, and 5 importer-preserved legacy hash/final-LF coverage gaps remain documented.
- Formatting, duplicate slugs, broken links, self-links, orphan pages, source drift, and lint warnings: 0.

## [2026-07-21] repair | lint source-reference count correction

- Correction: the immediately preceding lint entry reports 27 source references, but the measured canonical frontmatter total is 30.
- Unchanged measurements: 17 claim-level markers, 33 canonical links, 8 canonical pages, and 0 lint errors or warnings.
- Updated: `log.md` only; no raw or canonical page was changed.

## [2026-07-29] delete | canonical wiki 및 지식그래프 초기화

- Preserved: `raw/` 아래 원본 Markdown 13개는 변경하지 않음.
- Deleted canonical pages:
  - `concepts/ai-knowledge-workflow.md`
  - `concepts/ai-personal-knowledge-management.md`
  - `concepts/llm-wiki.md`
  - `concepts/research-feedback-loop.md`
  - `concepts/second-brain-research-workflow.md`
  - `comparisons/knowledge-tool-roles.md`
  - `queries/notebooklm-query-compounding.md`
  - `queries/ua-knowledge-graph-workflow.md`
- Deleted derived graph state:
  - `.ua/knowledge-graph.json`
  - `.ua/meta.json`
- Updated:
  - `index.md`
  - `log.md`
- Canonical state: 0 pages; 새 canonical 문서 생성과 이후 지식그래프 재생성을 위한 초기 상태.

## [2026-07-29] delete | raw 원본 자료 초기화

- Deleted raw source records:
  - `raw/notebooklm/2026-07-16-all-notes.md`
  - `raw/notebooklm/codegraph-github.md`
  - `raw/notebooklm/graphify-github.md`
  - `raw/notebooklm/llm-wiki-skill-github.md`
  - `raw/notebooklm/llm-wiki-zotero-notebooklm-youtube.md`
  - `raw/notebooklm/notebooklm-py-github.md`
  - `raw/notebooklm/understand-anything-github.md`
  - `raw/notebooklm/zotero-mcp-github.md`
  - `raw/web/NomaDamasslides-grab Best harness + editor + linter for generating slides in Claude Code  Codex - Claude Design Open Source Alternative.md`
  - `raw/web/stablyaiorca Orca is the ADE for working with a fleet of parallel agents. Run any coding agent with your own subscription. Available on desktop and mobile..md`
  - `raw/youtube/📺 How To Build LLM Wiki In Obsidian 🧠 A Memory Layer For Any Agentic AI.md`
  - `raw/youtube/📺 LLM Wiki를 업그레이드하는 외부 지식 시스템! 연구자를 위한 최강의 조합 Zotero × Notebook × Obsidian x Claude Code.md`
  - `raw/youtube/📺 Orca Is the Free Cursor Killer Nobody's Talking About!.md`
- Created empty directory placeholders:
  - `raw/notebooklm/.gitkeep`
  - `raw/web/.gitkeep`
  - `raw/youtube/.gitkeep`
- Updated:
  - `log.md`
- Result: raw source records 0, canonical pages 0, derived knowledge-graph state 0.

## 2026-08-20

- Replaced the initial schema with a simplified Industrial Vision AI wiki schema.
- Added `raw/papers/patchcore-paper.md` as an initial source record.
- Created draft canonical pages for Industrial Anomaly Detection, Memory Bank, MVTec AD, and PatchCore.
- Added path-based wikilinks between the initial concept pages.
- Updated `index.md` with the initial concept pages.

## [2026-10-20] repair | wiki 정합성 정리

- Issues found:
  - `index.md`의 `Total pages: 0`이 실제 등재 4건과 불일치.
  - `concepts/edge-inference.md`가 0바이트 빈 파일이며 index에 없음.
  - 직전 2026-08-20 기록이 언급한 `raw/papers/patchcore-paper.md`는 존재하지 않으며,
    실제 경로는 `raw/papers/roth-2022-patchcore.md`. 해당 기록은 헤딩 형식도
    `## [YYYY-MM-DD] <action> | <subject>`를 따르지 않음. append-only 원칙에 따라
    기존 기록은 수정하지 않고 이 항목으로 정정함.
  - `AGENTS.md`가 현재 `SCHEMA.md`(단순화된 Industrial Vision AI 스키마)와 다른
    이전 스키마를 설명함.
  - `SCHEMA.md`, `concepts/memory-bank.md`, `concepts/patchcore.md`에 최종 줄바꿈이
    없음. 내용 변경 없이 최종 LF만 추가함.
- Deleted:
  - `concepts/edge-inference.md`
- Updated:
  - `SCHEMA.md`
  - `concepts/memory-bank.md`
  - `concepts/patchcore.md`
  - `index.md`
  - `AGENTS.md`
  - `log.md`

## [2026-10-20] ingest | 비전검사 도입 공개 자료 1차 수집

- Created:
  - `raw/papers/bergmann-2019-mvtec-ad.md`
  - `raw/papers/martin-2021-surface-defect-detection-strategies.md`
  - `raw/web/advanced-illumination-practical-guide-machine-vision-lighting.md`
  - `raw/web/anomalib-documentation.md`
  - `raw/web/fictiv-injection-molding-defects.md`
  - `raw/web/keyence-machine-vision-lighting-selection.md`
  - `raw/web/minitab-attribute-agreement-analysis-overview.md`
  - `raw/web/mvtec-ad-dataset-page.md`
- Notes: 논문 2건은 PDF에서 `pdftotext`로 추출해 확인. 웹 6건은 자동 추출 결과이며
  각 파일의 capture note에 재확인 필요를 표시함. Cognex 자료는 HTTP 429로 미수집.
- Updated:
  - `log.md`

## [2026-10-20] create | 비전검사 공정 도입 가이드와 기반 개념

- Created:
  - `concepts/attribute-agreement-analysis.md`
  - `concepts/injection-molding-defects.md`
  - `concepts/machine-vision-lighting.md`
  - `concepts/surface-defect-detection.md`
  - `entities/anomalib.md`
  - `queries/vision-inspection-introduction-guide.md`
- Updated:
  - `concepts/industrial-anomaly-detection.md` (sources 추가, 내용 보강)
  - `concepts/mvtec-ad.md` (sources 추가, 구성·라이선스·평가 내용 보강)
  - `SCHEMA.md` (태그 8개 등록: `task/classification`, `deployment/openvino`,
    `hardware/lighting`, `hardware/camera`, `domain/injection-molding`,
    `domain/rubber-molding`, `process/introduction`, `quality/msa`)
  - `index.md`
  - `log.md`
- Canonical state: 10 pages, 모두 `status: draft`.

## [2026-10-20] lint | 출처·인용 검증

- Method: 웹 원문 6건을 직접 내려받아 raw 인용 64개를 글자 단위로 대조. 논문 2건의
  인용 22개는 `pdftotext` 추출 원문과 대조. 정식 문서의 `^[...]` 표시가 출처 범위를
  넘는지 수동 점검.
- Fixed capture errors (raw 본문을 원문에 맞게 정정):
  - `raw/web/anomalib-documentation.md`: 인용문의 빠진 쉼표 복원, 출처에 없는
    publisher 설명 삭제.
  - `raw/web/advanced-illumination-practical-guide-machine-vision-lighting.md`: 저자
    표기를 웹 메타데이터(Luke Weaver)와 PDF판(Daryl Martin, 2013-02)으로 구분.
  - `raw/papers/martin-2021-surface-defect-detection-strategies.md`: Trelleborg는
    공저자 소속이며 사례 회사는 논문에 명시되지 않음을 명확화. E2/E3의 데이터 증강
    적용 인용 추가.
  - 웹 raw 6건의 capture note를 대조 완료 상태로 갱신.
- Fixed over-claims in canonical pages:
  - `concepts/machine-vision-lighting.md`: 백라이트 용도를 출처 범위로 축소.
  - `concepts/injection-molding-defects.md`: 출처에 없는 별칭 삭제.
  - `concepts/surface-defect-detection.md`: 사전학습 수치에 데이터 증강 병행 명시.
  - `queries/vision-inspection-introduction-guide.md`: 불량별 조명 매칭을 출처 근거와
    가설로 분리, 룰 기반 근거를 variation model 범위로 한정, 사전학습 수치 정정.
- Result: 인용 86개 원문 일치, frontmatter·태그·출처 경로·표시·링크·index 검사 통과.
- Updated:
  - `log.md`

## [2026-10-21] ingest | 도입 가이드 약점 보강 자료 2차 수집

- Created:
  - `raw/papers/hinder-2023-concept-drift-survey.md`
  - `raw/papers/maslanka-2025-vision-plc-integration.md`
  - `raw/papers/yang-2020-diagnosing-concept-drift.md`
  - `raw/web/commonlands-field-of-view.md`
  - `raw/web/commonlands-spatial-resolution.md`
  - `raw/web/imaging-source-lens-selection.md`
  - `raw/web/keyence-2d-measurement-pixel-resolution.md`
  - `raw/web/keyence-ai-in-machine-vision.md`
  - `raw/web/keyence-selecting-machine-vision-camera.md`
  - `raw/web/overview-ai-injection-molding-inspection.md`
  - `raw/web/pekat-deep-learning-vs-rule-based.md`
  - `raw/web/roboflow-computer-vision-plc-integration.md`
- Method: 모든 원문을 curl로 내려받아 텍스트 변환 후 직접 인용. 인용 95개를 원문과
  기계 대조해 전부 일치 확인. 논문 섹션 번호도 원문 헤딩과 대조.
- Notes:
  - 검색 요약에 나온 Yang 2020의 메인보드 높이 변화 사례는 원문에 없어 제외.
  - Cognex 가이드는 다시 HTTP 429로 미수집.
  - Overview.ai는 싱크마크 조명을 페이지마다 다르게 제시(저각 vs 돔). 불일치로 기록.
- Updated:
  - `log.md`

## [2026-10-21] create | 카메라·렌즈, PLC 연동, 드리프트, 검사 방식 비교

- Created:
  - `comparisons/rule-based-vs-deep-learning-inspection.md`
  - `concepts/camera-and-lens-selection.md`
  - `concepts/concept-drift.md`
  - `concepts/vision-plc-integration.md`
- Updated:
  - `concepts/injection-molding-defects.md` (불량별 검출 방법, 출처 내 불일치 추가)
  - `queries/vision-inspection-introduction-guide.md` (세부 내용을 개념 문서로 넘기고
    해상도·방식 선택·PLC·드리프트 단계 보강, 200줄 이내 유지)
  - `SCHEMA.md` (태그 등록: `deployment/plc`, `operation/drift-monitoring`)
  - `AGENTS.md` (raw·canonical 개수)
  - `index.md`
  - `log.md`
- Canonical state: 14 pages, 모두 `status: draft`.
