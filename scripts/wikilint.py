"""Checks the wiki against the SCHEMA.md contract.

Usage from the repository root:
    python -m scripts.wikilint

Exits with status 1 when any error is found. Warnings are printed but do not
fail the run. The chat app imports check_page() to validate a page before it
writes it.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path

TYPE_DIRS = {"concept": "concepts", "entity": "entities", "comparison": "comparisons", "query": "queries"}
CANONICAL_DIRS = tuple(TYPE_DIRS.values())
STATUSES = {"draft", "verified", "disputed"}
REQUIRED_FIELDS = ("title", "type", "status", "tags", "sources", "created", "updated")
LOG_ACTIONS = {"ingest", "create", "update", "query", "lint", "archive", "delete", "map", "repair"}
MAX_LINES = 200

FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.S)
KEBAB_FILENAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*\.md$")
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
WIKILINK = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]")
MARKER = re.compile(r"\^\[(raw/[^\]]+)\]")
LOG_HEADING = re.compile(r"^## \[(\d{4}-\d{2}-\d{2})\] (\w+) \| .+$")


@dataclass(frozen=True)
class Issue:
    path: str
    message: str
    level: str = "error"  # "error" or "warning"

    def __str__(self) -> str:
        return f"[{self.level}] {self.path}: {self.message}"


@dataclass
class WikiState:
    root: Path
    tags: set[str]
    canonical: set[str]  # page paths without ".md", e.g. "concepts/patchcore"
    raw: set[str]  # repository-relative raw record paths


def load_state(root: Path) -> WikiState:
    schema = (root / "SCHEMA.md").read_text(encoding="utf-8")
    tag_section = re.search(r"^## Initial Tags\n(.*?)(?=^## |\Z)", schema, re.M | re.S)
    tags = set(re.findall(r"^- `([^`]+)`", tag_section.group(1), re.M)) if tag_section else set()
    canonical = {
        p.relative_to(root).with_suffix("").as_posix()
        for d in CANONICAL_DIRS
        for p in (root / d).glob("*.md")
    }
    raw = {p.relative_to(root).as_posix() for p in (root / "raw").rglob("*.md")}
    return WikiState(root, tags, canonical, raw)


def parse_frontmatter(text: str) -> dict[str, str | list[str]] | None:
    """Parses the small YAML subset the wiki uses: scalars and string lists."""
    match = FRONTMATTER.match(text)
    if not match:
        return None
    fields: dict[str, str | list[str]] = {}
    key = None
    for line in match.group(1).split("\n"):
        item = re.match(r"^  - (.+)$", line)
        if item and key is not None:
            value = fields.setdefault(key, [])
            if isinstance(value, list):
                value.append(item.group(1).strip().strip('"'))
            continue
        pair = re.match(r"^([A-Za-z_]+):\s*(.*)$", line)
        if pair:
            key, value = pair.group(1), pair.group(2).strip()
            fields[key] = [] if value in ("", "[]") else value.strip('"')
    return fields


def check_text_format(path: str, data: bytes) -> list[Issue]:
    issues = []
    if data.startswith(b"\xef\xbb\xbf"):
        issues.append(Issue(path, "UTF-8 BOM이 있습니다"))
    if b"\r\n" in data:
        issues.append(Issue(path, "줄바꿈이 CRLF입니다 (LF 필요)"))
    if data and not data.endswith(b"\n"):
        issues.append(Issue(path, "마지막 줄바꿈이 없습니다"))
    try:
        data.decode("utf-8")
    except UnicodeDecodeError:
        issues.append(Issue(path, "UTF-8이 아닙니다"))
    return issues


def check_page(path: str, text: str, state: WikiState) -> list[Issue]:
    """Checks one canonical page. `path` is repository-relative, e.g. "queries/x.md"."""
    issues = check_text_format(path, text.encode("utf-8"))
    folder, _, filename = path.partition("/")
    if folder not in CANONICAL_DIRS or "/" in filename:
        return issues + [Issue(path, "정식 문서 폴더(entities/concepts/comparisons/queries) 바로 아래가 아닙니다")]
    if not KEBAB_FILENAME.match(filename):
        issues.append(Issue(path, "파일명은 소문자 kebab-case .md여야 합니다"))

    fields = parse_frontmatter(text)
    if fields is None:
        return issues + [Issue(path, "파일 맨 앞에 frontmatter가 없습니다")]
    for name in REQUIRED_FIELDS:
        if name not in fields:
            issues.append(Issue(path, f"frontmatter에 {name}가 없습니다"))

    page_type = fields.get("type")
    if page_type not in TYPE_DIRS:
        issues.append(Issue(path, f"type이 잘못됐습니다: {page_type}"))
    elif TYPE_DIRS[page_type] != folder:
        issues.append(Issue(path, f"type {page_type}은 {TYPE_DIRS[page_type]}/에 있어야 합니다"))
    if fields.get("status") not in STATUSES:
        issues.append(Issue(path, f"status가 잘못됐습니다: {fields.get('status')}"))
    for name in ("created", "updated"):
        value = fields.get(name)
        if isinstance(value, str) and not DATE.match(value):
            issues.append(Issue(path, f"{name} 날짜 형식은 YYYY-MM-DD입니다"))

    tags = fields.get("tags", [])
    for tag in tags if isinstance(tags, list) else []:
        if tag not in state.tags:
            issues.append(Issue(path, f"SCHEMA.md에 등록되지 않은 태그: {tag}"))

    sources = fields.get("sources", [])
    sources = sources if isinstance(sources, list) else []
    for source in sources:
        if not source.startswith("raw/") or not source.endswith(".md"):
            issues.append(Issue(path, f"sources는 raw/ 아래 .md 경로여야 합니다: {source}"))
        elif source not in state.raw:
            issues.append(Issue(path, f"존재하지 않는 출처: {source}"))
    for marker in MARKER.findall(text):
        if marker not in sources:
            issues.append(Issue(path, f"출처 표시가 sources 목록에 없습니다: {marker}"))

    self_slug = path.removesuffix(".md")
    links = {link.strip() for link in WIKILINK.findall(text)}
    for link in sorted(links):
        if link not in state.canonical and link != self_slug:
            issues.append(Issue(path, f"깨진 위키링크: [[{link}]]"))
    if len(links - {self_slug}) < 2:
        issues.append(Issue(path, "다른 정식 문서로 가는 위키링크가 2개 이상 필요합니다"))

    lines = text.count("\n")
    if lines > MAX_LINES:
        issues.append(Issue(path, f"{lines}줄입니다. {MAX_LINES}줄 근처에서 분할을 검토하세요", "warning"))
    return issues


def check_index(root: Path, state: WikiState) -> list[Issue]:
    path = "index.md"
    text = (root / path).read_text(encoding="utf-8")
    issues = []
    count = re.search(r"Total pages: (\d+)", text)
    if not count or int(count.group(1)) != len(state.canonical):
        issues.append(Issue(path, f"Total pages가 실제 문서 수({len(state.canonical)})와 다릅니다"))

    sections = {"Entities": "entities", "Concepts": "concepts", "Comparisons": "comparisons", "Queries": "queries"}
    seen: list[str] = []
    for heading, body in re.findall(r"^## (\w+)\n(.*?)(?=^## |\Z)", text, re.M | re.S):
        entries = re.findall(r"^- \[\[([^|\]]+)", body, re.M)
        folder = sections.get(heading)
        for entry in entries:
            if folder and not entry.startswith(folder + "/"):
                issues.append(Issue(path, f"{entry}가 {heading} 섹션에 잘못 들어 있습니다"))
        if entries != sorted(entries, key=str.lower):
            issues.append(Issue(path, f"{heading} 섹션이 알파벳순이 아닙니다"))
        seen += entries
    for entry in {e for e in seen if seen.count(e) > 1}:
        issues.append(Issue(path, f"중복 항목: {entry}"))
    for missing in sorted(state.canonical - set(seen)):
        issues.append(Issue(path, f"index에 없는 문서: {missing}"))
    for extra in sorted(set(seen) - state.canonical):
        issues.append(Issue(path, f"존재하지 않는 문서가 index에 있습니다: {extra}"))
    return issues


def check_raw(root: Path, path: str) -> list[Issue]:
    return check_raw_text(path, (root / path).read_bytes())


def check_raw_text(path: str, data: bytes) -> list[Issue]:
    issues = check_text_format(path, data)
    fields = parse_frontmatter(data.decode("utf-8", "replace"))
    if fields is None:
        return issues + [Issue(path, "파일 맨 앞에 frontmatter가 없습니다")]
    if "title" not in fields:
        issues.append(Issue(path, "frontmatter에 title이 없습니다"))
    if fields.get("type") == "field-note":
        for name in ("date", "process", "confidentiality"):
            if name not in fields:
                issues.append(Issue(path, f"현장 메모 frontmatter에 {name}가 없습니다"))
    elif "source_url" not in fields or "captured" not in fields:
        issues.append(Issue(path, "frontmatter에 source_url과 captured가 필요합니다"))
    return issues


def check_log(root: Path) -> list[Issue]:
    issues = []
    for line in (root / "log.md").read_text(encoding="utf-8").split("\n"):
        if not line.startswith("## "):
            continue
        match = LOG_HEADING.match(line)
        if not match or match.group(2) not in LOG_ACTIONS:
            # The log is append-only, so a malformed past heading cannot be fixed.
            issues.append(Issue("log.md", f"형식에 맞지 않는 기록 제목: {line}", "warning"))
    return issues


def lint_repo(root: Path) -> list[Issue]:
    state = load_state(root)
    issues: list[Issue] = []
    for slug in sorted(state.canonical):
        path = f"{slug}.md"
        issues += check_page(path, (root / path).read_bytes().decode("utf-8", "replace"), state)
    for path in sorted(state.raw):
        issues += check_raw(root, path)
    issues += check_index(root, state)
    issues += check_log(root)
    for name in ("index.md", "log.md", "SCHEMA.md"):
        issues += check_text_format(name, (root / name).read_bytes())
    return issues


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    issues = lint_repo(root)
    for issue in issues:
        print(issue)
    errors = sum(issue.level == "error" for issue in issues)
    warnings = len(issues) - errors
    state = load_state(root)
    print(f"\n정식 문서 {len(state.canonical)}개, raw {len(state.raw)}개 검사: 오류 {errors}, 경고 {warnings}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
