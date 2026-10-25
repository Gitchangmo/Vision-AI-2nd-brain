"""Local chat server that answers questions from the wiki.

Two backends answer the questions:
- "cli": runs the logged-in Claude Code CLI headless, so it uses the Claude
  subscription and needs no API key. Default when no API key is set.
- "api": calls the Claude API with ANTHROPIC_API_KEY (billed per token).

Besides chat, the server drafts and writes wiki content (field notes and filed
query pages); every write passes the privacy gate and scripts.wikilint first.

Run from the repository root:
    app/.venv/Scripts/python -m uvicorn app.server:app --reload
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import tempfile
import threading
from collections.abc import AsyncIterator, Iterator
from datetime import date
from pathlib import Path
from typing import Literal

import anthropic
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from app import llm, prompts
from app.conversations import ConversationStore
from app.privacy import SensitiveTerms, find_sensitive
from app.wiki import WikiContext
from app.wikiwrite import PROCESSES, WikiWriteError, check_query_page, write_field_note, write_query_page
from scripts.wikilint import load_state

APP_DIR = Path(__file__).resolve().parent
load_dotenv(APP_DIR / ".env")
# Overridable so tests can run against a throwaway copy of the wiki.
REPO_ROOT = Path(os.getenv("WIKI_ROOT") or APP_DIR.parent)
DATA_DIR = Path(os.getenv("WIKI_CHAT_DATA") or APP_DIR / "data")

BACKEND = os.getenv("WIKI_CHAT_BACKEND") or ("api" if os.getenv("ANTHROPIC_API_KEY") else "cli")
EFFORT = os.getenv("WIKI_CHAT_EFFORT", "medium")
API_MODEL = os.getenv("WIKI_CHAT_MODEL", "claude-opus-5-5")
# Empty means the CLI's own configured model.
CLI_MODEL = os.getenv("WIKI_CHAT_MODEL", "")
MAX_TOKENS = 64000

# Images arrive as base64 content blocks. They reach disk only inside saved
# conversations, which stay in the git-ignored app/data directory.
IMAGE_TYPES = {"image/jpeg", "image/png", "image/gif", "image/webp"}
MAX_IMAGE_BASE64_CHARS = 6_500_000  # about 5 MB decoded, the API's per-image limit
MAX_IMAGES_PER_MESSAGE = 5
REQUEST_ID = re.compile(r"^[0-9a-f]{32}$")

# The CLI runs in an empty work directory so it picks up no project files or
# CLAUDE.md; the wiki reaches it only through the system prompt file.
CLI_WORKDIR = Path(tempfile.gettempdir()) / "vision-wiki-chat"

client = anthropic.AsyncAnthropic()
wiki = WikiContext(REPO_ROOT)
conversations = ConversationStore(DATA_DIR / "conversations")
sensitive_terms = SensitiveTerms(DATA_DIR / "sensitive-terms.txt")
# Field notes and query pages both append to log.md; one writer at a time.
wiki_write_lock = threading.Lock()
# CLI processes of answers in progress, so the stop button can end them.
running: dict[str, subprocess.Popen] = {}
running_lock = threading.Lock()

app = FastAPI(title="Vision Wiki Chat")
app.mount("/static", StaticFiles(directory=APP_DIR / "static"), name="static")


class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    # User turns are text or a list of text/image blocks. Assistant turns carry
    # the content this server returned earlier, sent back unchanged.
    content: str | list[dict]


class ChatRequest(BaseModel):
    messages: list[ChatMessage] = Field(min_length=1)
    request_id: str | None = None


class SavedConversation(BaseModel):
    title: str = Field(max_length=200)
    messages: list[ChatMessage] = Field(min_length=1)
    # Display-only notes keyed by message index, such as model and token counts.
    meta: dict[str, str] = {}


class TermsBody(BaseModel):
    terms: list[str]


class FieldNoteDraftRequest(BaseModel):
    title: str = ""
    process: str
    status: str
    date: str
    sections: dict[str, str]


class FieldNoteSave(BaseModel):
    title: str
    process: str
    status: str
    date: str
    body: str


class WikiDraftRequest(BaseModel):
    messages: list[ChatMessage] = Field(min_length=2)


class WikiPage(BaseModel):
    path: str
    text: str
    summary: str


def sse(payload: dict) -> str:
    return f"data: {json.dumps(payload, ensure_ascii=False)}\n\n"


def today() -> str:
    return date.today().isoformat()


def check_user_content(messages: list[dict]) -> str | None:
    """Returns an error message when a user turn holds an unusable block."""
    for message in messages:
        if message["role"] != "user" or isinstance(message["content"], str):
            continue
        images = 0
        for block in message["content"]:
            kind = block.get("type")
            if kind == "text" and isinstance(block.get("text"), str):
                continue
            if kind != "image":
                return "지원하지 않는 첨부 형식입니다."
            source = block.get("source") or {}
            if source.get("type") != "base64" or source.get("media_type") not in IMAGE_TYPES:
                return "이미지는 JPEG, PNG, GIF, WebP만 첨부할 수 있습니다."
            if len(source.get("data", "")) > MAX_IMAGE_BASE64_CHARS:
                return "이미지 하나가 너무 큽니다 (최대 약 5MB)."
            images += 1
        if images > MAX_IMAGES_PER_MESSAGE:
            return f"한 번에 이미지는 {MAX_IMAGES_PER_MESSAGE}장까지 첨부할 수 있습니다."
    return None


def findings_json(text: str) -> list[dict]:
    return [{"kind": f.kind, "match": f.match} for f in find_sensitive(text, sensitive_terms.load())]


def generate(system: str, prompt: str, schema: dict) -> dict:
    try:
        return llm.complete_json(
            backend=BACKEND, system=system, prompt=prompt, schema=schema, workdir=CLI_WORKDIR,
            effort=EFFORT, api_model=API_MODEL, cli_model=CLI_MODEL,
        )
    except llm.GenerationError as e:
        raise HTTPException(502, str(e)) from e


# --- pages and wiki info ---------------------------------------------------------


@app.get("/")
async def index() -> FileResponse:
    return FileResponse(APP_DIR / "static" / "index.html")


@app.get("/api/wiki")
async def wiki_info() -> dict:
    model = API_MODEL if BACKEND == "api" else (CLI_MODEL or "Claude Code 기본 모델")
    return {**wiki.summary(), "backend": BACKEND, "model": model, "effort": EFFORT}


@app.get("/api/doc")
def get_doc(path: str) -> dict:
    # Only files the wiki loader knows (index, canonical pages, raw records)
    # can be read; any other path, including traversal attempts, is not found.
    text = wiki.document(path)
    if text is None:
        raise HTTPException(404, "위키 문서를 찾을 수 없습니다.")
    return {"path": path, "text": text}


# --- saved conversations ---------------------------------------------------------


@app.get("/api/conversations")
def list_conversations() -> list[dict]:
    return conversations.list()


@app.get("/api/conversations/{conversation_id}")
def get_conversation(conversation_id: str) -> dict:
    data = conversations.get(conversation_id)
    if data is None:
        raise HTTPException(404, "대화를 찾을 수 없습니다.")
    return data


@app.put("/api/conversations/{conversation_id}")
def save_conversation(conversation_id: str, body: SavedConversation) -> dict:
    messages = [m.model_dump() for m in body.messages]
    problem = check_user_content(messages)
    if problem:
        raise HTTPException(400, problem)
    saved = conversations.save(conversation_id, body.title, messages, body.meta)
    if saved is None:
        raise HTTPException(400, "잘못된 대화 ID입니다.")
    return saved


@app.delete("/api/conversations/{conversation_id}")
def delete_conversation(conversation_id: str) -> dict:
    if not conversations.delete(conversation_id):
        raise HTTPException(404, "대화를 찾을 수 없습니다.")
    return {"deleted": conversation_id}


# --- sensitive terms -------------------------------------------------------------


@app.get("/api/sensitive-terms")
def get_terms() -> dict:
    return {"terms": sensitive_terms.load()}


@app.put("/api/sensitive-terms")
def put_terms(body: TermsBody) -> dict:
    return {"terms": sensitive_terms.save(body.terms)}


# --- field notes -----------------------------------------------------------------


@app.post("/api/field-notes/draft")
def draft_field_note(body: FieldNoteDraftRequest) -> dict:
    if body.process not in PROCESSES:
        raise HTTPException(400, "공정 분류가 잘못됐습니다.")
    filled = {k: v.strip() for k, v in body.sections.items() if v.strip()}
    if not filled:
        raise HTTPException(400, "내용을 한 칸 이상 입력하세요.")
    prompt = prompts.field_note_prompt(body.title, PROCESSES[body.process], filled, sensitive_terms.load())
    draft = generate(prompts.FIELD_NOTE_SYSTEM, prompt, prompts.FIELD_NOTE_SCHEMA)
    draft["findings"] = findings_json(f"{draft['title']}\n{draft['body']}")
    return draft


@app.post("/api/field-notes")
def save_field_note(body: FieldNoteSave):
    findings = findings_json(f"{body.title}\n{body.body}")
    if findings:
        return JSONResponse({"detail": "민감 정보가 남아 있어 저장하지 않았습니다.", "findings": findings}, 422)
    try:
        with wiki_write_lock:
            path = write_field_note(
                REPO_ROOT, title=body.title, process=body.process, status=body.status,
                date=body.date, body=body.body, today=today(),
            )
    except WikiWriteError as e:
        return JSONResponse({"detail": "저장하지 않았습니다.", "issues": e.issues}, 422)
    return {"path": path}


# --- chat answer to wiki page ------------------------------------------------------


def page_report(page: WikiPage) -> dict:
    text = page.text if page.text.endswith("\n") else page.text + "\n"
    issues = check_query_page(REPO_ROOT, page.path, text)
    return {
        "issues": [{"level": i.level, "message": i.message} for i in issues],
        "findings": findings_json(f"{page.summary}\n{text}"),
    }


@app.post("/api/wiki-drafts")
def draft_wiki_page(body: WikiDraftRequest) -> dict:
    messages = [m.model_dump() for m in body.messages]
    if messages[-1]["role"] != "assistant":
        raise HTTPException(400, "답변까지 포함한 대화가 필요합니다.")
    state = load_state(REPO_ROOT)
    schema = prompts.wiki_draft_schema(sorted(state.tags), wiki.raw_paths())
    system = prompts.WIKI_DRAFT_INSTRUCTIONS + "\n" + wiki.wiki_text()
    draft = generate(system, prompts.wiki_draft_prompt(messages, sensitive_terms.load()), schema)
    page = WikiPage(
        path=f"queries/{draft['slug']}.md",
        text=prompts.query_page_text(draft, today()),
        summary=draft["summary"],
    )
    return {**page.model_dump(), "warnings": draft["warnings"], **page_report(page)}


@app.post("/api/wiki-drafts/check")
def check_wiki_page(page: WikiPage) -> dict:
    return page_report(page)


@app.post("/api/wiki-drafts/save")
def save_wiki_page(page: WikiPage):
    findings = findings_json(f"{page.summary}\n{page.text}")
    if findings:
        return JSONResponse({"detail": "민감 정보가 남아 있어 저장하지 않았습니다.", "findings": findings}, 422)
    try:
        with wiki_write_lock:
            path = write_query_page(REPO_ROOT, path=page.path, text=page.text, summary=page.summary, today=today())
    except WikiWriteError as e:
        return JSONResponse({"detail": "위키 검사를 통과하지 못했습니다.", "issues": e.issues}, 422)
    return {"path": path}


# --- chat ------------------------------------------------------------------------


@app.post("/api/chat")
async def chat(request: ChatRequest) -> StreamingResponse:
    messages = [m.model_dump() for m in request.messages]
    problem = check_user_content(messages)
    if messages[-1]["role"] != "user":
        problem = "마지막 메시지는 질문이어야 합니다."
    if request.request_id is not None and not REQUEST_ID.fullmatch(request.request_id):
        problem = "잘못된 요청 ID입니다."
    if problem:
        stream = iter([sse({"type": "error", "message": problem})])
    elif BACKEND == "api":
        stream = stream_api(messages)
    else:
        stream = stream_cli(messages, request.request_id)
    return StreamingResponse(stream, media_type="text/event-stream")


@app.post("/api/chat/{request_id}/cancel")
def cancel_chat(request_id: str) -> dict:
    # The API backend stops when the browser drops the connection; only CLI
    # runs need an explicit kill.
    with running_lock:
        process = running.pop(request_id, None)
    if process is not None and process.poll() is None:
        process.kill()
    return {"cancelled": process is not None}


# --- API backend -----------------------------------------------------------


async def stream_api(messages: list[dict]) -> AsyncIterator[str]:
    try:
        async with client.beta.messages.stream(
            model=API_MODEL,
            max_tokens=MAX_TOKENS,
            betas=["server-side-fallback-2026-07-01"],
            fallbacks="default",
            output_config={"effort": EFFORT},
            cache_control={"type": "ephemeral"},
            system=wiki.system_blocks(),
            messages=messages,
        ) as stream:
            async for text in stream.text_stream:
                yield sse({"type": "text", "text": text})
            final = await stream.get_final_message()
    except anthropic.AuthenticationError:
        yield sse({"type": "error", "message": "API 키가 잘못됐습니다. app/.env를 확인하세요."})
        return
    except TypeError as e:
        # The SDK raises TypeError, not an API error, when no credential is configured.
        if "authentication method" not in str(e):
            raise
        yield sse({"type": "error", "message": "API 키가 설정되지 않았습니다. app/.env에 ANTHROPIC_API_KEY를 넣으세요."})
        return
    except anthropic.RateLimitError:
        yield sse({"type": "error", "message": "요청 한도에 걸렸습니다. 잠시 후 다시 시도하세요."})
        return
    except anthropic.BadRequestError as e:
        yield sse({"type": "error", "message": f"잘못된 요청: {e.message}"})
        return
    except anthropic.APIStatusError as e:
        yield sse({"type": "error", "message": f"API 오류 ({e.status_code}): {e.message}"})
        return
    except anthropic.APIConnectionError:
        yield sse({"type": "error", "message": "API 서버에 연결하지 못했습니다. 네트워크를 확인하세요."})
        return

    if final.stop_reason == "refusal":
        yield sse({"type": "notice", "message": "이 질문은 안전 정책으로 답변이 거절됐습니다."})
    elif final.stop_reason == "max_tokens":
        yield sse({"type": "notice", "message": "답변이 길이 제한에 걸려 잘렸습니다."})

    usage = final.usage
    yield sse(
        {
            "type": "done",
            "content": final.to_dict()["content"],
            "model": final.model,
            "usage": {
                "input": usage.input_tokens,
                "cache_read": usage.cache_read_input_tokens or 0,
                "cache_write": usage.cache_creation_input_tokens or 0,
                "output": usage.output_tokens,
            },
        }
    )


# --- CLI backend -----------------------------------------------------------


def stream_cli(messages: list[dict], request_id: str | None) -> Iterator[str]:
    # A sync generator: StreamingResponse runs it in a worker thread, which
    # avoids asyncio subprocess limits on Windows event loops.
    executable = shutil.which("claude")
    if executable is None:
        yield sse({"type": "error", "message": "claude CLI를 찾지 못했습니다. Claude Code가 설치돼 있는지 확인하세요."})
        return

    command = [
        executable, "-p",
        "--input-format", "stream-json",
        "--output-format", "stream-json", "--verbose", "--include-partial-messages",
        "--tools", "",
        "--system-prompt-file", str(wiki.system_prompt_file(CLI_WORKDIR)),
        "--no-session-persistence",
        "--effort", EFFORT,
    ]
    if CLI_MODEL:
        command += ["--model", CLI_MODEL]

    # stderr goes to a file so a chatty CLI can never fill the pipe and stall.
    errors = tempfile.TemporaryFile()
    process = subprocess.Popen(
        command,
        cwd=CLI_WORKDIR,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=errors,
    )
    if request_id:
        with running_lock:
            running[request_id] = process

    # Images can make the input several MB, so feed stdin from a thread while
    # this thread reads stdout.
    payload = (json.dumps(prompts.cli_user_message(messages), ensure_ascii=False) + "\n").encode("utf-8")

    def feed_stdin() -> None:
        try:
            process.stdin.write(payload)
        except OSError:
            pass  # the CLI exited early; its error is reported from stderr
        finally:
            process.stdin.close()

    threading.Thread(target=feed_stdin, daemon=True).start()
    text = ""
    result: dict | None = None
    try:
        for line in process.stdout:
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            if event.get("type") == "stream_event":
                inner = event["event"]
                delta = inner.get("delta", {})
                if inner.get("type") == "content_block_delta" and delta.get("type") == "text_delta":
                    text += delta["text"]
                    yield sse({"type": "text", "text": delta["text"]})
            elif event.get("type") == "result":
                result = event
        process.wait()
    finally:
        if process.poll() is None:
            process.kill()
        if request_id:
            with running_lock:
                running.pop(request_id, None)

    errors.seek(0)
    stderr_text = errors.read().decode("utf-8", "replace").strip()
    errors.close()
    if result is None or result.get("is_error"):
        detail = (result or {}).get("result") or stderr_text
        yield sse({"type": "error", "message": f"Claude CLI 오류: {detail or '응답이 없습니다.'}"})
        return

    usage = result.get("usage", {})
    # The CLI may call a small helper model too; the answer comes from the one
    # with the most output.
    model_usage = result.get("modelUsage", {})
    model = max(model_usage, key=lambda m: model_usage[m].get("outputTokens", 0), default="claude-cli")
    yield sse(
        {
            "type": "done",
            "content": text or result.get("result", ""),
            "model": model,
            "usage": {
                "input": usage.get("input_tokens", 0),
                "cache_read": usage.get("cache_read_input_tokens", 0),
                "cache_write": usage.get("cache_creation_input_tokens", 0),
                "output": usage.get("output_tokens", 0),
            },
        }
    )
