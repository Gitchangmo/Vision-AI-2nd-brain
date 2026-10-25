"""One-shot structured (JSON) generation through either backend.

Used for drafting: anonymizing field notes and turning a chat answer into a
wiki page. Chat answers stream through server.py instead.
"""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
from pathlib import Path

import anthropic


class GenerationError(Exception):
    """A user-facing message explaining why a draft could not be generated."""


def complete_json(
    *,
    backend: str,
    system: str,
    prompt: str,
    schema: dict,
    workdir: Path,
    effort: str,
    api_model: str,
    cli_model: str,
) -> dict:
    if backend == "api":
        return _complete_api(system, prompt, schema, effort, api_model)
    return _complete_cli(system, prompt, schema, workdir, effort, cli_model)


def _complete_api(system: str, prompt: str, schema: dict, effort: str, model: str) -> dict:
    client = anthropic.Anthropic()
    try:
        response = client.beta.messages.create(
            model=model,
            max_tokens=16000,
            betas=["server-side-fallback-2026-07-01"],
            fallbacks="default",
            output_config={"effort": effort, "format": {"type": "json_schema", "schema": schema}},
            system=[{"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}],
            messages=[{"role": "user", "content": prompt}],
        )
    except TypeError as e:
        if "authentication method" not in str(e):
            raise
        raise GenerationError("API 키가 설정되지 않았습니다.") from e
    except anthropic.APIStatusError as e:
        raise GenerationError(f"API 오류 ({e.status_code}): {e.message}") from e
    except anthropic.APIConnectionError as e:
        raise GenerationError("API 서버에 연결하지 못했습니다.") from e
    if response.stop_reason == "refusal":
        raise GenerationError("안전 정책으로 초안 생성이 거절됐습니다.")
    if response.stop_reason == "max_tokens":
        raise GenerationError("초안이 길이 제한에 걸려 잘렸습니다.")
    text = next(b.text for b in response.content if b.type == "text")
    return json.loads(text)


def _complete_cli(system: str, prompt: str, schema: dict, workdir: Path, effort: str, model: str) -> dict:
    executable = shutil.which("claude")
    if executable is None:
        raise GenerationError("claude CLI를 찾지 못했습니다.")
    workdir.mkdir(parents=True, exist_ok=True)
    # One file per distinct system prompt, so concurrent drafts never clash.
    digest = hashlib.sha256(system.encode("utf-8")).hexdigest()[:16]
    system_file = workdir / f"system-{digest}.md"
    if not system_file.exists():
        system_file.write_text(system, encoding="utf-8")

    command = [
        executable, "-p",
        "--output-format", "json",
        "--json-schema", json.dumps(schema, ensure_ascii=False),
        "--tools", "",
        "--system-prompt-file", str(system_file),
        "--no-session-persistence",
        "--effort", effort,
    ]
    if model:
        command += ["--model", model]
    try:
        completed = subprocess.run(
            command, cwd=workdir, input=prompt.encode("utf-8"), capture_output=True, timeout=600
        )
    except subprocess.TimeoutExpired as e:
        raise GenerationError("초안 생성이 10분 안에 끝나지 않았습니다.") from e
    try:
        result = json.loads(completed.stdout)
    except json.JSONDecodeError as e:
        detail = completed.stderr.decode("utf-8", "replace").strip()
        raise GenerationError(f"Claude CLI 오류: {detail or '응답을 해석하지 못했습니다.'}") from e
    if result.get("is_error") or not isinstance(result.get("structured_output"), dict):
        raise GenerationError(f"Claude CLI 오류: {result.get('result') or '구조화된 결과가 없습니다.'}")
    return result["structured_output"]
