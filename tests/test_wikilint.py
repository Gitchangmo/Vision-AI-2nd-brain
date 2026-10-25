from pathlib import Path

from scripts.wikilint import check_page, lint_repo, load_state

from conftest import page


def errors(issues):
    return [i.message for i in issues if i.level == "error"]


def test_valid_wiki_has_no_errors(wiki_root: Path):
    assert errors(lint_repo(wiki_root)) == []


def test_tags_come_only_from_the_tag_section(wiki_root: Path):
    schema = wiki_root / "SCHEMA.md"
    schema.write_text("# S\n\n- `not/a-tag` mentioned in prose\n\n" + schema.read_text(encoding="utf-8"), encoding="utf-8", newline="\n")
    assert load_state(wiki_root).tags == {"task/anomaly-detection", "hardware/lighting"}


def test_page_problems_are_reported(wiki_root: Path):
    state = load_state(wiki_root)
    text = page("Bad", ["concepts/alpha", "concepts/missing"], ["raw/papers/none.md"], "x ^[raw/papers/a-paper.md]")
    text = text.replace("hardware/lighting", "free/tag")
    found = errors(check_page("concepts/bad.md", text, state))
    assert "SCHEMA.md에 등록되지 않은 태그: free/tag" in found
    assert "존재하지 않는 출처: raw/papers/none.md" in found
    assert "출처 표시가 sources 목록에 없습니다: raw/papers/a-paper.md" in found
    assert "깨진 위키링크: [[concepts/missing]]" in found


def test_page_needs_two_distinct_links(wiki_root: Path):
    text = page("Lonely", ["concepts/alpha", "concepts/alpha|Alpha again"])
    assert "다른 정식 문서로 가는 위키링크가 2개 이상 필요합니다" in errors(
        check_page("concepts/lonely.md", text, load_state(wiki_root))
    )


def test_type_must_match_folder_and_name_is_kebab_case(wiki_root: Path):
    text = page("Q", ["concepts/alpha", "concepts/beta"])
    found = errors(check_page("queries/Bad_Name.md", text, load_state(wiki_root)))
    assert "type concept은 concepts/에 있어야 합니다" in found
    assert "파일명은 소문자 kebab-case .md여야 합니다" in found


def test_crlf_and_index_count_are_caught(wiki_root: Path):
    (wiki_root / "concepts/beta.md").write_bytes((wiki_root / "concepts/beta.md").read_bytes().replace(b"\n", b"\r\n"))
    index = wiki_root / "index.md"
    index.write_text(index.read_text(encoding="utf-8").replace("Total pages: 3", "Total pages: 9"), encoding="utf-8", newline="\n")
    found = errors(lint_repo(wiki_root))
    assert "줄바꿈이 CRLF입니다 (LF 필요)" in found
    assert "Total pages가 실제 문서 수(3)와 다릅니다" in found


def test_page_missing_from_index_is_reported(wiki_root: Path):
    (wiki_root / "concepts/delta.md").write_text(page("Delta", ["concepts/alpha", "concepts/beta"]), encoding="utf-8", newline="\n")
    assert "index에 없는 문서: concepts/delta" in errors(lint_repo(wiki_root))


def test_malformed_log_heading_is_only_a_warning(wiki_root: Path):
    log = wiki_root / "log.md"
    log.write_text(log.read_text(encoding="utf-8") + "\n## 2026-02-02\n\n- note\n", encoding="utf-8", newline="\n")
    issues = lint_repo(wiki_root)
    assert errors(issues) == []
    assert any(i.level == "warning" and i.path == "log.md" for i in issues)
