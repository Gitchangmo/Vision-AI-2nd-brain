"""Writes field notes and filed query pages into the wiki, keeping index.md and
log.md in step as SCHEMA.md requires.

Every write is validated with scripts.wikilint first; nothing is written when
a check fails.
"""

from __future__ import annotations

import re
from pathlib import Path

from scripts.wikilint import Issue, check_page, check_raw_text, load_state, parse_frontmatter

PROCESSES = {
    "injection-molding": "사출",
    "rubber-molding": "고무 성형",
    "extrusion": "압출",
    "press": "프레스",
    "assembly": "조립",
    "other": "기타",
}
NOTE_STATUSES = {"poc", "pilot", "production", "abandoned"}
YEAR_MONTH = re.compile(r"^\d{4}-(0[1-9]|1[0-2])$")
QUERY_PATH = re.compile(r"^queries/[a-z0-9]+(?:-[a-z0-9]+)*\.md$")


class WikiWriteError(Exception):
    def __init__(self, issues: list[str]) -> None:
        super().__init__("; ".join(issues))
        self.issues = issues


def _quote(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def append_log(root: Path, date: str, action: str, subject: str, body_lines: list[str]) -> None:
    log = root / "log.md"
    text = log.read_text(encoding="utf-8")
    separator = "" if text.endswith("\n\n") else ("\n" if text.endswith("\n") else "\n\n")
    entry = f"## [{date}] {action} | {subject}\n\n" + "\n".join(body_lines) + "\n"
    log.write_text(text + separator + entry, encoding="utf-8", newline="\n")


# --- field notes ---------------------------------------------------------------


def field_note_text(title: str, process: str, status: str, date: str, captured: str, body: str) -> str:
    return (
        "---\n"
        f"title: {_quote(title)}\n"
        "type: field-note\n"
        f"date: {date}\n"
        f"process: {process}\n"
        f"status: {status}\n"
        "confidentiality: anonymized\n"
        f"captured: {captured}\n"
        "---\n\n"
        f"{body.strip()}\n"
    )


def next_field_note_path(root: Path, date: str, process: str) -> str:
    folder = root / "raw" / "field-notes"
    number = 1
    while (folder / f"{date}-{process}-{number:02d}.md").exists():
        number += 1
    return f"raw/field-notes/{date}-{process}-{number:02d}.md"


def write_field_note(
    root: Path, *, title: str, process: str, status: str, date: str, body: str, today: str
) -> str:
    problems = []
    if not title.strip():
        problems.append("제목이 비어 있습니다.")
    if process not in PROCESSES:
        problems.append(f"공정 분류가 잘못됐습니다: {process}")
    if status not in NOTE_STATUSES:
        problems.append(f"진행 단계가 잘못됐습니다: {status}")
    if not YEAR_MONTH.match(date):
        problems.append("날짜는 YYYY-MM 형식이어야 합니다.")
    if not body.strip():
        problems.append("본문이 비어 있습니다.")
    if problems:
        raise WikiWriteError(problems)

    path = next_field_note_path(root, date, process)
    text = field_note_text(title.strip(), process, status, date, today, body)
    issues = [i for i in check_raw_text(path, text.encode("utf-8")) if i.level == "error"]
    if issues:
        raise WikiWriteError([i.message for i in issues])

    target = root / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8", newline="\n")
    append_log(
        root,
        today,
        "ingest",
        f"현장 메모: {title.strip()}",
        [
            "- Created:",
            f"  - `{path}`",
            "- Method: 채팅 앱 현장 메모 입력 (AI 익명화 초안 → 사용자 검토 → 민감어 검사 통과).",
            "- Updated:",
            "  - `log.md`",
        ],
    )
    return path


# --- filed query pages -----------------------------------------------------------


def add_index_entry(root: Path, slug: str, title: str, summary: str) -> None:
    """Adds a page to the Queries section, keeping it sorted, and bumps the count."""
    index = root / "index.md"
    text = index.read_text(encoding="utf-8")
    match = re.search(r"(^## Queries\n)(.*?)(?=^## |\Z)", text, re.M | re.S)
    if match is None:
        raise WikiWriteError(["index.md에 Queries 섹션이 없습니다."])
    entries = re.findall(r"^- \[\[.+$", match.group(2), re.M)
    entries.append(f"- [[{slug}|{title}]] — {summary}")
    entries.sort(key=lambda line: line[4:].split("|")[0].lower())
    section = match.group(1) + "\n" + "\n".join(entries) + "\n"
    if text[match.end():]:
        section += "\n"
    text = text[: match.start()] + section + text[match.end():]

    total = len(re.findall(r"^- \[\[", text, re.M))
    text = re.sub(r"Total pages: \d+", f"Total pages: {total}", text)
    index.write_text(text, encoding="utf-8", newline="\n")


def check_query_page(root: Path, path: str, text: str) -> list[Issue]:
    issues = []
    if not QUERY_PATH.match(path):
        issues.append(Issue(path, "경로는 queries/<소문자-kebab-case>.md 형식이어야 합니다"))
    elif (root / path).exists():
        issues.append(Issue(path, "같은 이름의 문서가 이미 있습니다"))
    issues += check_page(path, text, load_state(root))
    fields = parse_frontmatter(text) or {}
    if fields.get("type") != "query":
        issues.append(Issue(path, "type은 query여야 합니다"))
    return issues


def write_query_page(root: Path, *, path: str, text: str, summary: str, today: str) -> str:
    if not text.endswith("\n"):
        text += "\n"
    errors = [i.message for i in check_query_page(root, path, text) if i.level == "error"]
    if not summary.strip():
        errors.append("index에 넣을 한 줄 요약이 비어 있습니다.")
    if errors:
        raise WikiWriteError(errors)

    fields = parse_frontmatter(text) or {}
    title = str(fields.get("title", path))
    (root / path).write_text(text, encoding="utf-8", newline="\n")
    add_index_entry(root, path.removesuffix(".md"), title, summary.strip())
    append_log(
        root,
        today,
        "query",
        title,
        [
            "- Created:",
            f"  - `{path}`",
            "- Method: 채팅 앱 답변에서 초안 생성 → 사용자 검토 → 위키 검사·민감어 검사 통과.",
            "- Updated:",
            "  - `index.md`",
            "  - `log.md`",
        ],
    )
    return path
