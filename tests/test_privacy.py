from pathlib import Path

from app.privacy import SensitiveTerms, find_sensitive


def kinds(findings):
    return {(f.kind, f.match) for f in findings}


def test_registered_terms_match_case_insensitively():
    found = kinds(find_sensitive("Acme 납품 부품 ab-12", ["ACME", "AB-12", "없는말"]))
    assert ("등록한 민감어", "ACME") in found
    assert ("등록한 민감어", "AB-12") in found
    assert len(found) == 2


def test_contact_and_company_patterns():
    found = kinds(find_sensitive("문의 kim@corp.co.kr, 010-1234-5678, ㈜대한, Foo Co., Ltd", []))
    assert ("이메일 주소", "kim@corp.co.kr") in found
    assert ("전화번호", "010-1234-5678") in found
    assert any(kind.startswith("회사 표기") for kind, _ in found)


def test_technical_text_is_not_flagged():
    text = "2026-10-25 측정, 5MP 16mm 렌즈, 0.083 mm/pixel, 시야 100mm, 15도 저각 조명, 택트 40초대"
    assert find_sensitive(text, []) == []


def test_terms_file_round_trip(tmp_path: Path):
    store = SensitiveTerms(tmp_path / "data" / "terms.txt")
    assert store.load() == []
    assert store.save(["  B사 ", "a사", "", "B사"]) == ["a사", "B사"]
    (tmp_path / "data" / "terms.txt").write_text("# comment\nX\n", encoding="utf-8")
    assert store.load() == ["X"]
