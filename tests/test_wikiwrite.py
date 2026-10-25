from pathlib import Path

import pytest

from app.wikiwrite import WikiWriteError, write_field_note, write_query_page
from scripts.wikilint import lint_repo

QUERY = """\
---
title: "How to light"
type: query
status: draft
tags:
  - hardware/lighting
sources:
  - raw/papers/a-paper.md
created: 2026-02-01
updated: 2026-02-01
---

# How to light

Use low angle. ^[raw/papers/a-paper.md]

## 관련 지식

- [[concepts/alpha|Alpha]]
- [[concepts/beta|Beta]]
"""


def note(root: Path, **overrides) -> str:
    args = dict(title="사출 부품 PoC", process="injection-molding", status="poc",
                date="2026-02", body="## 상황\n\n- 내용", today="2026-02-03")
    args.update(overrides)
    return write_field_note(root, **args)


def test_field_note_is_written_numbered_and_logged(wiki_root: Path):
    assert note(wiki_root) == "raw/field-notes/2026-02-injection-molding-01.md"
    assert note(wiki_root) == "raw/field-notes/2026-02-injection-molding-02.md"
    text = (wiki_root / "raw/field-notes/2026-02-injection-molding-01.md").read_text(encoding="utf-8")
    assert "type: field-note\n" in text and "confidentiality: anonymized\n" in text
    assert "## [2026-02-03] ingest | 현장 메모: 사출 부품 PoC" in (wiki_root / "log.md").read_text(encoding="utf-8")
    assert [i for i in lint_repo(wiki_root) if i.level == "error"] == []


@pytest.mark.parametrize(
    "overrides",
    [{"date": "2026-13"}, {"process": "welding"}, {"status": "done"}, {"title": " "}, {"body": ""}],
)
def test_field_note_rejects_bad_fields(wiki_root: Path, overrides):
    with pytest.raises(WikiWriteError):
        note(wiki_root, **overrides)
    assert list((wiki_root / "raw/field-notes").iterdir()) == []


def test_query_page_updates_index_and_log(wiki_root: Path):
    write_query_page(wiki_root, path="queries/how-to-light.md", text=QUERY, summary="조명 선택", today="2026-02-01")
    index = (wiki_root / "index.md").read_text(encoding="utf-8")
    assert "Total pages: 4" in index
    assert "- [[queries/how-to-light|How to light]] — 조명 선택" in index
    assert "## [2026-02-01] query | How to light" in (wiki_root / "log.md").read_text(encoding="utf-8")
    assert [i for i in lint_repo(wiki_root) if i.level == "error"] == []


def test_query_pages_stay_sorted(wiki_root: Path):
    write_query_page(wiki_root, path="queries/zeta.md", text=QUERY, summary="z", today="2026-02-01")
    write_query_page(wiki_root, path="queries/alpha-q.md", text=QUERY, summary="a", today="2026-02-01")
    index = (wiki_root / "index.md").read_text(encoding="utf-8")
    assert index.index("queries/alpha-q") < index.index("queries/zeta")
    assert "Total pages: 5" in index


def test_query_page_rejections_leave_wiki_untouched(wiki_root: Path):
    before = {p: p.read_bytes() for p in wiki_root.rglob("*.md")}
    bad_marker = QUERY.replace("Use low angle.", "Use low angle. ^[raw/papers/none.md]")
    for path, text, summary in [
        ("queries/x.md", bad_marker, "s"),
        ("concepts/x.md", QUERY, "s"),
        ("queries/Bad.md", QUERY, "s"),
        ("queries/x.md", QUERY, " "),
    ]:
        with pytest.raises(WikiWriteError):
            write_query_page(wiki_root, path=path, text=text, summary=summary, today="2026-02-01")
    assert {p: p.read_bytes() for p in wiki_root.rglob("*.md")} == before


def test_existing_query_page_is_not_overwritten(wiki_root: Path):
    write_query_page(wiki_root, path="queries/how-to-light.md", text=QUERY, summary="s", today="2026-02-01")
    with pytest.raises(WikiWriteError, match="이미 있습니다"):
        write_query_page(wiki_root, path="queries/how-to-light.md", text=QUERY, summary="s", today="2026-02-01")
