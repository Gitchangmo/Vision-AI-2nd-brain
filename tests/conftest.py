"""Shared fixtures: a small throwaway wiki and a test client bound to it."""

from __future__ import annotations

import importlib
from pathlib import Path

import pytest

SCHEMA = """\
# Test Schema

## Initial Tags

- `task/anomaly-detection`
- `hardware/lighting`
"""

INDEX = """\
# Wiki Index

> Total pages: 3

## Entities

## Concepts

- [[concepts/alpha|Alpha]] — first
- [[concepts/beta|Beta]] — second
- [[concepts/gamma|Gamma]] — third

## Comparisons

## Queries
"""

LOG = """\
# Wiki Log

## [2026-01-01] create | seed

- Created:
  - `concepts/alpha.md`
"""


def page(title: str, links: list[str], sources: list[str] = (), body: str = "") -> str:
    source_lines = "".join(f"\n  - {s}" for s in sources) if sources else " []"
    link_lines = "\n".join(f"- [[{link}]]" for link in links)
    return (
        "---\n"
        f'title: "{title}"\n'
        "type: concept\n"
        "status: draft\n"
        "tags:\n  - hardware/lighting\n"
        f"sources:{source_lines}\n"
        "created: 2026-01-01\n"
        "updated: 2026-01-01\n"
        "---\n\n"
        f"# {title}\n\n{body}\n\n## 관련 지식\n\n{link_lines}\n"
    )


RAW = """\
---
title: "A Paper"
source_url: "https://example.org/paper"
captured: 2026-01-01
---

# Abstract

Lighting matters.
"""


@pytest.fixture
def wiki_root(tmp_path: Path) -> Path:
    root = tmp_path / "wiki"
    for folder in ("entities", "concepts", "comparisons", "queries", "raw/papers", "raw/field-notes"):
        (root / folder).mkdir(parents=True)
    files = {
        "SCHEMA.md": SCHEMA,
        "index.md": INDEX,
        "log.md": LOG,
        "raw/papers/a-paper.md": RAW,
        "concepts/alpha.md": page(
            "Alpha", ["concepts/beta", "concepts/gamma|Gamma"], ["raw/papers/a-paper.md"],
            "Claim. ^[raw/papers/a-paper.md]",
        ),
        "concepts/beta.md": page("Beta", ["concepts/alpha", "concepts/gamma"]),
        "concepts/gamma.md": page("Gamma", ["concepts/alpha", "concepts/beta"]),
    }
    for name, text in files.items():
        (root / name).write_text(text, encoding="utf-8", newline="\n")
    return root


@pytest.fixture
def server(wiki_root: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """The app.server module, re-imported against the throwaway wiki."""
    monkeypatch.setenv("WIKI_ROOT", str(wiki_root))
    monkeypatch.setenv("WIKI_CHAT_DATA", str(tmp_path / "data"))
    monkeypatch.setenv("WIKI_CHAT_BACKEND", "cli")
    import app.server

    return importlib.reload(app.server)


@pytest.fixture
def client(server):
    from fastapi.testclient import TestClient

    return TestClient(server.app)
