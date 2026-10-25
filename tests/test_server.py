import json

from app import prompts


def events(response):
    return [json.loads(chunk[6:]) for chunk in response.text.split("\n\n") if chunk.startswith("data: ")]


IMAGE = {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": "iVBORw0KGgo="}}
CONVERSATION = {"title": "t", "messages": [{"role": "user", "content": "q"}, {"role": "assistant", "content": "a"}]}


# --- chat validation (no model call is made for invalid requests) ----------------


def test_chat_rejects_bad_image_type(client):
    bad = {"type": "image", "source": {"type": "base64", "media_type": "image/bmp", "data": "x"}}
    body = {"messages": [{"role": "user", "content": [bad, {"type": "text", "text": "q"}]}]}
    assert events(client.post("/api/chat", json=body))[0]["type"] == "error"


def test_chat_rejects_too_many_images(client):
    body = {"messages": [{"role": "user", "content": [IMAGE] * 6 + [{"type": "text", "text": "q"}]}]}
    assert "5장" in events(client.post("/api/chat", json=body))[0]["message"]


def test_chat_rejects_bad_request_id(client):
    body = {"messages": [{"role": "user", "content": "q"}], "request_id": "../x"}
    assert events(client.post("/api/chat", json=body))[0]["type"] == "error"


def test_cancel_unknown_request_is_harmless(client):
    assert client.post(f"/api/chat/{'a' * 32}/cancel").json() == {"cancelled": False}


def test_cli_message_keeps_images_and_history():
    message = prompts.cli_user_message([
        {"role": "user", "content": [IMAGE, {"type": "text", "text": "첫 질문"}]},
        {"role": "assistant", "content": [{"type": "thinking", "thinking": ""}, {"type": "text", "text": "답"}]},
        {"role": "user", "content": "이어지는 질문"},
    ])
    blocks = message["message"]["content"]
    assert [b["type"] for b in blocks] == ["text", "image", "text"]
    assert "답" in blocks[2]["text"] and "<question>\n이어지는 질문" in blocks[2]["text"]


# --- conversations --------------------------------------------------------------


def test_conversation_round_trip(client):
    cid = "a" * 32
    assert client.put(f"/api/conversations/{cid}", json=CONVERSATION).status_code == 200
    assert [c["id"] for c in client.get("/api/conversations").json()] == [cid]
    assert client.get(f"/api/conversations/{cid}").json()["messages"][1]["content"] == "a"
    assert client.delete(f"/api/conversations/{cid}").status_code == 200
    assert client.get(f"/api/conversations/{cid}").status_code == 404


def test_conversation_id_must_be_hex(client):
    assert client.put("/api/conversations/not-an-id", json=CONVERSATION).status_code == 400
    assert client.get("/api/conversations/..%2Fx").status_code == 404


# --- documents ---------------------------------------------------------------------


def test_doc_serves_wiki_files_only(client):
    assert client.get("/api/doc", params={"path": "concepts/alpha.md"}).status_code == 200
    assert client.get("/api/doc", params={"path": "raw/papers/a-paper.md"}).status_code == 200
    for path in ["SCHEMA.md", "../SCHEMA.md", "concepts/../SCHEMA.md", "app/.env", "C:/Windows/win.ini"]:
        assert client.get("/api/doc", params={"path": path}).status_code == 404


# --- field notes ---------------------------------------------------------------------


def test_field_note_save_is_blocked_by_registered_term(client, wiki_root):
    client.put("/api/sensitive-terms", json={"terms": ["ACME"]})
    note = {"title": "PoC", "process": "injection-molding", "status": "poc", "date": "2026-02", "body": "acme 부품"}
    response = client.post("/api/field-notes", json=note)
    assert response.status_code == 422
    assert response.json()["findings"] == [{"kind": "등록한 민감어", "match": "ACME"}]
    assert list((wiki_root / "raw/field-notes").iterdir()) == []

    note["body"] = "## 상황\n\n- 일반화한 부품"
    assert client.post("/api/field-notes", json=note).json()["path"].startswith("raw/field-notes/2026-02-")


def test_field_note_draft_reports_leftover_terms(client, server, monkeypatch):
    client.put("/api/sensitive-terms", json={"terms": ["ACME"]})
    seen = {}

    def fake(**kwargs):
        seen.update(kwargs)
        return {"title": "PoC", "body": "ACME 남음", "replacements": [], "warnings": []}

    monkeypatch.setattr(server.llm, "complete_json", fake)
    draft = client.post("/api/field-notes/draft", json={
        "process": "rubber-molding", "status": "poc", "date": "2026-02", "sections": {"situation": "ACME 개스킷"},
    }).json()
    assert draft["findings"] == [{"kind": "등록한 민감어", "match": "ACME"}]
    assert "ACME" in seen["prompt"] and "고무 성형" in seen["prompt"]


# --- chat answer to wiki page ------------------------------------------------------


def fake_page_draft(**kwargs):
    return {
        "slug": "how-to-light",
        "title": "How to light",
        "summary": "조명 선택",
        "tags": ["hardware/lighting"],
        "sources": ["raw/papers/a-paper.md"],
        "body": "# How to light\n\nLow angle. ^[raw/papers/a-paper.md]\n\n## 관련 지식\n\n"
                "- [[concepts/alpha|Alpha]]\n- [[concepts/beta|Beta]]",
        "warnings": ["check it"],
    }


def test_wiki_draft_then_save(client, server, wiki_root, monkeypatch):
    monkeypatch.setattr(server.llm, "complete_json", fake_page_draft)
    draft = client.post("/api/wiki-drafts", json={"messages": CONVERSATION["messages"]}).json()
    assert draft["path"] == "queries/how-to-light.md"
    assert draft["issues"] == [] and draft["findings"] == []
    page = {k: draft[k] for k in ("path", "text", "summary")}
    assert client.post("/api/wiki-drafts/save", json=page).json() == {"path": "queries/how-to-light.md"}
    assert (wiki_root / "queries/how-to-light.md").exists()
    assert "Total pages: 4" in (wiki_root / "index.md").read_text(encoding="utf-8")


def test_wiki_draft_schema_limits_tags_and_sources(client, server, monkeypatch):
    seen = {}

    def capture(**kwargs):
        seen.update(kwargs)
        return fake_page_draft()

    monkeypatch.setattr(server.llm, "complete_json", capture)
    client.post("/api/wiki-drafts", json={"messages": CONVERSATION["messages"]})
    properties = seen["schema"]["properties"]
    assert properties["tags"]["items"]["enum"] == ["hardware/lighting", "task/anomaly-detection"]
    assert properties["sources"]["items"]["enum"] == ["raw/papers/a-paper.md"]


def test_wiki_draft_needs_an_answer(client):
    assert client.post("/api/wiki-drafts", json={"messages": [
        {"role": "assistant", "content": "a"}, {"role": "user", "content": "q"},
    ]}).status_code == 400


def test_wiki_page_save_blocked_by_term_and_lint(client):
    client.put("/api/sensitive-terms", json={"terms": ["ACME"]})
    page = {"path": "queries/x.md", "text": "---\ntitle: x\n---\n", "summary": "ACME"}
    assert client.post("/api/wiki-drafts/save", json=page).json()["findings"][0]["match"] == "ACME"
    page["summary"] = "ok"
    assert client.post("/api/wiki-drafts/save", json=page).status_code == 422
