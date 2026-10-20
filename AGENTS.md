# PROJECT KNOWLEDGE BASE

**Updated:** 2026-10-20
**Branch:** main

## OVERVIEW

- Markdown/Obsidian second brain for industrial computer-vision inspection,
  built on an evidence-first LLM wiki model.
- Scope: vision inspection in general (anomaly detection, detection, segmentation,
  lighting, cameras, evaluation, deployment) plus practical guides for introducing
  vision inspection into new processes (injection molding, rubber molding, etc.).
- The repository root is the wiki root; no database, service, or build system exists.
- `SCHEMA.md` is the operational contract. `README.md` covers optional tool setup
  but describes a generic PARA layout that is not the current repository structure.
- Current curated state: 9 raw Markdown records and 10 canonical pages.

## START HERE

1. Read `SCHEMA.md` completely.
2. Read `index.md` to find existing canonical subjects and avoid duplicates.
3. Read the newest entries in append-only `log.md` before changing the wiki.
4. Resolve every path relative to this repository root.

## STRUCTURE

```text
./
├── inbox/                 # Temporary intake; neither evidence nor canonical
├── raw/
│   ├── papers/            # Paper records (metadata, abstract, located excerpts)
│   ├── articles/          # Captured article Markdown
│   ├── web/               # Captured web pages and vendor/tool documentation
│   ├── notebooklm/        # NotebookLM-imported source records
│   ├── transcripts/       # Captured transcript Markdown
│   ├── youtube/           # Video transcript captures
│   └── assets/            # Local assets referenced by raw records
├── entities/              # Canonical type: entity (tools, datasets, orgs, models)
├── concepts/              # Canonical type: concept
├── comparisons/           # Canonical type: comparison
├── queries/               # Canonical type: query (multi-source answers, guides)
├── docs/                  # Architecture and diagram deliverables; not evidence
├── SCHEMA.md              # Authoritative content contract and tag list
├── index.md               # Complete active canonical catalog
└── log.md                 # Append-only wiki operation history
```

`.obsidian/` is shared editor configuration; ignored `.ua/` is derived
knowledge-graph state, never canonical evidence.

## WHERE TO LOOK

| Task | Location | Notes |
| --- | --- | --- |
| Learn the rules | `SCHEMA.md` | Wins over README examples |
| Install optional tools | `README.md` | Obsidian, Zotero, MCP, CLI, and agent skills |
| Find existing knowledge | `index.md` | Count must equal active canonical files |
| Understand recent work | `log.md` | Read the tail; never rewrite history |
| Stage unclassified input | `inbox/` | Capture properly before canonical use |
| Preserve source evidence | `raw/` | Do not edit captured bodies |
| Curate reusable knowledge | `entities/`, `concepts/`, `comparisons/`, `queries/` | Folder and frontmatter `type` must agree |
| Process introduction guide | `queries/vision-inspection-introduction-guide.md` | Hub page for deployment work |

## CONTENT CONTRACT

- Canonical filenames are lowercase kebab-case and end in `.md`.
- Canonical frontmatter starts at byte zero and contains `title`, `type`,
  `status`, `tags`, `sources`, `created`, and `updated` (see `SCHEMA.md`).
- `type`: `concept | entity | comparison | query`, matching the folder.
- `status`: `draft | verified | disputed`. LLM-written or LLM-edited pages stay
  `draft` until the user verifies them.
- Preserve `created`; bump `updated` whenever content or metadata changes.
- Use only tags listed in `SCHEMA.md`; add a tag there before first use.
- Create a page only for a source's central subject or a subject repeated across
  at least two sources. Update an existing subject instead of creating a synonym.
- Link related pages with path-based `[[folder/slug|Title]]` wikilinks; each page
  should link to at least two other active canonical pages.
- Mark statements without source support as proposals, hypotheses, or `TODO`.
- Split pages near 200 lines while preserving provenance and useful links.

## RAW RECORDS AND PROVENANCE

- Treat captured raw bodies as immutable; put corrections and interpretation in
  canonical pages.
- Raw frontmatter records at least `title`, `source_url`, and `captured`; papers
  also record authors, year, and venue.
- Excerpts carry a location (section, table, or page heading). Web captures made
  by automated extraction say so in a capture note.
- Canonical `sources` entries must be exact, existing repository-relative raw
  Markdown paths. Assets do not qualify as sources.
- A claim-level `^[raw/...md]` marker must resolve and already appear in that
  page's `sources` list.
- Do not invent provenance, quotes, or numbers. Record fetch failures in the log.

## TRANSACTIONAL WIKI UPDATES

For every canonical create, update, filed query, archive, or delete:

1. Keep `index.md` alphabetic, type-correct, unique, and count-accurate.
2. Append one `log.md` entry using an allowed action and list every affected path.
3. Archive only fully superseded pages; repair active links and remove them from
   the index.

Log headings use `## [YYYY-MM-DD] <action> | <subject>`; actions are `ingest`,
`create`, `update`, `query`, `lint`, `archive`, `delete`, `map`, and `repair`.
Never rewrite earlier log entries; correct them with a new `repair` entry.

## VALIDATION

No build, test, lint, or CI is configured. Validate the contract directly:

- UTF-8, LF, no BOM, final newline, and leading frontmatter.
- Required fields, allowed `type`/`status` values, registered tags, type-directory fit.
- Existing source paths and valid claim-level provenance markers.
- No broken canonical wikilinks.
- Filesystem canonical count equals `index.md`; each active page appears once.

## ANTI-PATTERNS

- Do not use README's PARA tree or free-form tags for canonical work.
- Do not edit raw bodies, invent provenance paths, or treat attachments or
  `docs/` as evidence.
- Do not create passing-mention, isolated, or duplicate canonical pages.
- Do not rewrite prior `log.md` entries or skip index/log synchronization.
- Do not commit credentials, personal or confidential company data, Obsidian
  workspace state, `.ua/`, `output/`, or QA artifacts.
