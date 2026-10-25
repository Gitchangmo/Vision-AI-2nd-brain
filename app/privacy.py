"""Deterministic last check before anything is written into the public wiki.

The model anonymizes drafts first, but a model can miss things. This gate
blocks a save when the text still contains a term the user registered as
sensitive (company, customer, product names, part numbers) or a contact-like
pattern. It never rewrites text; the user fixes the draft and saves again.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

PATTERNS = {
    "이메일 주소": re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"),
    "전화번호": re.compile(r"(?<!\d)(?:0\d{1,2}[-. ]?\d{3,4}[-. ]?\d{4})(?!\d)"),
    "회사 표기(㈜, 주식회사, Co., Ltd. 등)": re.compile(
        r"㈜|\(주\)|주식회사|\b(?:Co\.,?\s*Ltd|Inc\.|Corp\.|GmbH)\b", re.I
    ),
}


@dataclass(frozen=True)
class Finding:
    kind: str
    match: str


class SensitiveTerms:
    """The user's own list of words that must never reach the wiki.

    Stored one term per line in a git-ignored file; lines starting with # are
    comments.
    """

    def __init__(self, path: Path) -> None:
        self.path = path

    def load(self) -> list[str]:
        if not self.path.exists():
            return []
        terms = []
        for line in self.path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                terms.append(line)
        return terms

    def save(self, terms: list[str]) -> list[str]:
        cleaned = sorted({t.strip() for t in terms if t.strip()}, key=str.lower)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text("\n".join(cleaned) + ("\n" if cleaned else ""), encoding="utf-8")
        return cleaned


def find_sensitive(text: str, terms: list[str]) -> list[Finding]:
    findings = []
    lowered = text.lower()
    for term in terms:
        if term.lower() in lowered:
            findings.append(Finding("등록한 민감어", term))
    for kind, pattern in PATTERNS.items():
        for match in sorted(set(pattern.findall(text))):
            findings.append(Finding(kind, match))
    return findings
