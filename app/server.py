"""Local chat server that answers questions from the wiki.

Two backends answer the questions:
- "cli": runs the logged-in Claude Code CLI headless, so it uses the Claude
  subscription and needs no API key. Default when no API key is set.
- "api": calls the Claude API with ANTHROPIC_API_KEY (billed per token).

Run from the repository root:
    app/.venv/Scripts/python -m uvicorn app.server:app --reload
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
import threading
from collections.abc import AsyncIterator, Iterator
from pathlib import Path
from typing import Literal

import anthropic
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from app.conversations import ConversationStore
from app.wiki import WikiContext

APP_DIR = Path(__file__).resolve().parent
REPO_ROOT = APP_DIR.parent
load_dotenv(APP_DIR / ".env")

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

# The CLI runs in an empty work directory so it picks up no project files or
# CLAUDE.md; the wiki reaches it only through the system prompt file.
CLI_WORKDIR = Path(tempfile.gettempdir()) / "vision-wiki-chat"

client = anthropic.AsyncAnthropic()
wiki = WikiContext(REPO_ROOT)
conversations = ConversationStore(APP_DIR / "data" / "conversations")
app = FastAPI(title="Vision Wiki Chat")
app.mount("/static", StaticFiles(directory=APP_DIR / "static"), name="static")


class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    # User turns are text or a list of text/image blocks. Assistant turns carry
    # the content this server returned earlier, sent back unchanged.
    content: str | list[dict]


class ChatRequest(BaseModel):
    messages: list[ChatMessage] = Field(min_length=1)


class SavedConversation(BaseModel):
    title: str = Field(max_length=200)
    messages: list[ChatMessage] = Field(min_length=1)
    # Display-only notes keyed by message index, such as model and token counts.
    meta: dict[str, str] = {}


def sse(payload: dict) -> str:
    return f"data: {json.dumps(payload, ensure_ascii=False)}\n\n"


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


@app.get("/")
async def index() -> FileResponse:
    return FileResponse(APP_DIR / "static" / "index.html")


@app.get("/api/wiki")
async def wiki_info() -> dict:
    model = API_MODEL if BACKEND == "api" else (CLI_MODEL or "Claude Code 기본 모델")
    return {**wiki.summary(), "backend": BACKEND, "model": model, "effort": EFFORT}


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


@app.post("/api/chat")
async def chat(request: ChatRequest) -> StreamingResponse:
    messages = [m.model_dump() for m in request.messages]
    problem = check_user_content(messages)
    if messages[-1]["role"] != "user":
        problem = "마지막 메시지는 질문이어야 합니다."
    if problem:
        stream = iter([sse({"type": "error", "message": problem})])
    elif BACKEND == "api":
        stream = stream_api(messages)
    else:
        stream = stream_cli(messages)
    return StreamingResponse(stream, media_type="text/event-stream")


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


def as_text(content: str | list[dict]) -> str:
    if isinstance(content, str):
        return content
    return "".join(b.get("text", "") for b in content if b.get("type") == "text")


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


def stream_cli(messages: list[dict]) -> Iterator[str]:
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
    # Images can make the input several MB, so feed stdin from a thread while
    # this thread reads stdout.
    payload = (json.dumps(cli_user_message(messages), ensure_ascii=False) + "\n").encode("utf-8")

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
