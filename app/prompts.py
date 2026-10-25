"""Prompts, output schemas, and message shaping for the model calls."""

from __future__ import annotations

ANONYMIZATION_RULES = """\
Anonymization rules (the wiki is a public repository):
- Remove or generalize: company, customer, supplier and own-company names; \
product names, model and part numbers, drawing and mold numbers; people's \
names, employee ids, contact details; plant locations and line names.
- Business figures (yield, defect rate, production volume, unit price, \
investment) become ranges or relative statements, e.g. "과검이 절반 정도 줄었다".
- Keep the technical knowledge: generalized part category (e.g. 자동차 내장 \
사출 부품), material and color, defect types, lighting, camera, lens, \
algorithm and settings, trial and error, lessons.
- When unsure whether something identifies the company, generalize it and \
mention it in warnings."""

# --- field notes ---------------------------------------------------------------

SECTION_LABELS = {
    "situation": "상황",
    "tried": "시도한 것",
    "result": "결과",
    "problems": "실패·문제",
    "lessons": "교훈",
}

FIELD_NOTE_SYSTEM = f"""\
You turn a practitioner's raw notes about an industrial vision inspection \
project into an anonymized field note for their public knowledge wiki.

{ANONYMIZATION_RULES}

Output:
- title: a generalized Korean title such as "자동차 내장 사출 부품 싱크마크 검사 PoC".
- body: Korean Markdown with exactly these sections in order, each a \
"## " heading: 상황, 시도한 것, 결과, 실패·문제, 교훈. Keep the author's facts \
and wording where they are not sensitive; do not invent results. If a section \
had no input, write "- (기록 없음)". Use a table when several setups were compared.
- replacements: every change you made for anonymization, with the category, \
the original text, and what replaced it.
- warnings: anything you could not anonymize confidently or that the author \
should double-check.
"""

FIELD_NOTE_SCHEMA = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "body": {"type": "string"},
        "replacements": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "category": {"type": "string"},
                    "before": {"type": "string"},
                    "after": {"type": "string"},
                },
                "required": ["category", "before", "after"],
                "additionalProperties": False,
            },
        },
        "warnings": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["title", "body", "replacements", "warnings"],
    "additionalProperties": False,
}


def field_note_prompt(title: str, process_label: str, sections: dict[str, str], terms: list[str]) -> str:
    parts = [f"공정 분류: {process_label}"]
    if title.strip():
        parts.append(f"작성자가 붙인 제목: {title.strip()}")
    for key, label in SECTION_LABELS.items():
        if key in sections:
            parts.append(f"<{label}>\n{sections[key]}\n</{label}>")
    if terms:
        parts.append("반드시 제거할 등록 민감어: " + ", ".join(terms))
    return "\n\n".join(parts)


# --- chat answer to wiki page ------------------------------------------------------

WIKI_DRAFT_INSTRUCTIONS = f"""\
You file a useful chat exchange as a query page for an industrial vision \
inspection wiki. The wiki follows the content contract below; the full wiki \
is provided after these instructions.

Write the page so it stands on its own for a future reader:
- Frame the question generically, without the asker's specifics that could \
identify a company or product.
- Answer in Korean from the wiki. Put a claim-level marker such as \
^[raw/papers/bergmann-2019-mvtec-ad.md] after each sourced statement; every \
marker must also be listed in sources. Label unsourced reasoning as 제안 or \
가설. Never invent sources.
- If the conversation included images, describe only the generalized \
observation that matters for the answer.
- body starts with "# <title>", then a "> **질문**: ..." line, then "## 답변", \
and ends with "## 관련 지식" listing at least two existing canonical pages as \
path wikilinks like [[concepts/machine-vision-lighting|Machine Vision Lighting]]. \
Add "## TODO" for gaps worth filling.
- slug: lowercase kebab-case English, a few words, unique among existing pages.
- summary: one Korean line for index.md.
- tags: only from the allowed list; sources: only raw paths you cite.

{ANONYMIZATION_RULES}

Put anything that still needs the author's judgment in warnings.
"""


def wiki_draft_schema(tags: list[str], raw_paths: list[str]) -> dict:
    return {
        "type": "object",
        "properties": {
            "slug": {"type": "string"},
            "title": {"type": "string"},
            "summary": {"type": "string"},
            "tags": {"type": "array", "items": {"type": "string", "enum": tags}},
            "sources": {"type": "array", "items": {"type": "string", "enum": raw_paths}},
            "body": {"type": "string"},
            "warnings": {"type": "array", "items": {"type": "string"}},
        },
        "required": ["slug", "title", "summary", "tags", "sources", "body", "warnings"],
        "additionalProperties": False,
    }


def wiki_draft_prompt(messages: list[dict], terms: list[str]) -> str:
    turns = []
    for m in messages:
        text = as_text(m["content"])
        if m["role"] == "user" and image_count(m["content"]):
            text = f"[이미지 {image_count(m['content'])}장 첨부]\n{text}"
        turns.append(f'<turn role="{m["role"]}">\n{text}\n</turn>')
    prompt = "다음 대화를 위키 query 문서 초안으로 만들어줘.\n\n<conversation>\n" + "\n".join(turns) + "\n</conversation>"
    if terms:
        prompt += "\n\n반드시 제거할 등록 민감어: " + ", ".join(terms)
    return prompt


def _yaml_list(values: list[str]) -> str:
    return "".join(f"\n  - {v}" for v in values) if values else " []"


def query_page_text(draft: dict, today: str) -> str:
    title = draft["title"].replace('"', "'")
    return (
        "---\n"
        f'title: "{title}"\n'
        "type: query\n"
        "status: draft\n"
        f"tags:{_yaml_list(draft['tags'])}\n"
        f"sources:{_yaml_list(draft['sources'])}\n"
        f"created: {today}\n"
        f"updated: {today}\n"
        "---\n\n"
        f"{draft['body'].strip()}\n"
    )


# --- chat messages ---------------------------------------------------------------


def as_text(content: str | list[dict]) -> str:
    if isinstance(content, str):
        return content
    return "".join(b.get("text", "") for b in content if b.get("type") == "text")


def image_count(content: str | list[dict]) -> int:
    return 0 if isinstance(content, str) else sum(b.get("type") == "image" for b in content)


def cli_user_message(messages: list[dict]) -> dict:
    """Flattens the conversation into one user message; each CLI run is stateless.

    Images from earlier user turns stay in place so follow-up questions can
    refer back to them.
    """
    blocks: list[dict] = []

    def add_text(text: str) -> None:
        if blocks and blocks[-1]["type"] == "text":
            blocks[-1]["text"] += text
        else:
            blocks.append({"type": "text", "text": text})

    def add_user_content(content: str | list[dict]) -> None:
        if isinstance(content, str):
            add_text(content)
            return
        for block in content:
            if block["type"] == "image":
                blocks.append(block)
            else:
                add_text(block["text"])

    *earlier, last = messages
    if earlier:
        add_text("<conversation_so_far>\n")
        for m in earlier:
            add_text(f'<turn role="{m["role"]}">\n')
            if m["role"] == "user":
                add_user_content(m["content"])
            else:
                add_text(as_text(m["content"]))
            add_text("\n</turn>\n")
        add_text("</conversation_so_far>\n\n")
    add_text("<question>\n")
    add_user_content(last["content"])
    add_text("\n</question>")
    return {"type": "user", "message": {"role": "user", "content": blocks}}
