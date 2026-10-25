"""Browser check of the chat app against a throwaway copy of the wiki.

Requires Playwright and a local Chrome (`pip install playwright`; no browser
download is needed). Run from the repository root:

    app/.venv/Scripts/python tests/e2e/ui_check.py          # UI only, no model calls
    app/.venv/Scripts/python tests/e2e/ui_check.py --llm    # also asks, drafts, and stops answers

The --llm run uses the configured backend (Claude subscription or API key) and
takes a few minutes.
"""

from __future__ import annotations

import json
import os
import shutil
import socket
import subprocess
import sys
import tempfile
import time
import urllib.request
from pathlib import Path

from playwright.sync_api import Page, sync_playwright

REPO = Path(__file__).resolve().parents[2]
WIKI_PARTS = ["SCHEMA.md", "index.md", "log.md", "entities", "concepts", "comparisons", "queries", "raw"]
PNG = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="

results: list[tuple[str, bool]] = []


def check(name: str, ok: bool) -> None:
    results.append((name, ok))
    print(f"{'PASS' if ok else 'FAIL'}  {name}")


def free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def put(base: str, path: str, body: dict) -> None:
    request = urllib.request.Request(
        base + path, method="PUT", data=json.dumps(body).encode(), headers={"Content-Type": "application/json"}
    )
    urllib.request.urlopen(request).close()


def ui_only(page: Page, base: str) -> None:
    # A saved conversation with an image and an answer that links into the wiki.
    answer = "조명 선택은 [[concepts/machine-vision-lighting|Machine Vision Lighting]] 참고. ^[raw/web/keyence-machine-vision-lighting-selection.md]"
    put(base, f"/api/conversations/{'e' * 32}", {
        "title": "seed",
        "messages": [
            {"role": "user", "content": [
                {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": PNG}},
                {"type": "text", "text": "질문"},
            ]},
            {"role": "assistant", "content": answer},
        ],
        "meta": {"1": "seed · 0 토큰"},
    })
    page.goto(base)
    page.click("#conversation-list li .open")
    page.wait_for_selector(".msg.assistant a.wikilink")
    check("saved conversation reopens", page.locator(".msg").count() == 2)

    page.click(".msg.user .images img")
    check("image opens in lightbox", page.is_visible("#lightbox"))
    page.keyboard.press("Escape")
    check("Esc closes lightbox", page.is_hidden("#lightbox"))

    page.click(".msg.assistant a.wikilink")
    page.wait_for_selector("#doc-drawer:not([hidden])")
    check("wiki link opens drawer", page.inner_text("#doc-path") == "concepts/machine-vision-lighting.md")
    page.locator("#doc-body a.wikilink").first.click()
    page.wait_for_function("document.getElementById('doc-path').textContent !== 'concepts/machine-vision-lighting.md'")
    check("drawer follows links", page.is_enabled("#doc-back"))
    page.click("#doc-back")
    page.wait_for_function("document.getElementById('doc-path').textContent === 'concepts/machine-vision-lighting.md'")
    check("drawer back button", True)
    page.keyboard.press("Escape")
    page.click(".msg.assistant a.rawlink")
    page.wait_for_selector("#doc-drawer:not([hidden])")
    check("claim marker opens raw record", page.inner_text("#doc-path").startswith("raw/web/"))
    page.click("#doc-close")

    page.click(".tab[data-view=note]")
    check("note tab shows form", page.is_visible("#note-form") and page.is_hidden("#composer"))
    page.click("#terms-box summary")
    page.fill("#terms", "테스트사\nAB-12")
    page.click("#save-terms")
    page.wait_for_function("document.getElementById('terms-count').textContent === '(2개)'")
    check("sensitive terms save", True)
    page.click(".tab[data-view=chat]")

    page.set_viewport_size({"width": 420, "height": 800})
    page.wait_for_timeout(400)
    hidden = page.evaluate("document.getElementById('sidebar').getBoundingClientRect().right <= 0")
    page.click("#toggle-sidebar")
    page.wait_for_timeout(400)
    shown = page.evaluate("document.getElementById('sidebar').getBoundingClientRect().left >= 0")
    check("narrow screen sidebar toggle", hidden and shown)
    page.set_viewport_size({"width": 1280, "height": 900})


def with_llm(page: Page, base: str) -> None:
    page.goto(base)
    page.fill("#input", "검정 사출 부품 싱크마크 조명? 2줄로.")
    page.click("#send")
    page.wait_for_selector(".msg.assistant .actions button", timeout=300_000)
    check("answer streams and finishes", page.locator(".msg.assistant .meta").count() == 1)

    page.click(".msg.assistant .actions button")
    page.wait_for_selector("#draft-form:not([hidden])", timeout=300_000)
    page.click("#draft-save")
    page.wait_for_selector("#draft-modal[hidden]", state="attached", timeout=30_000)
    check("answer filed as wiki page", "위키에 저장했어요" in page.locator(".notice").last.inner_text())

    page.fill("#input", "위키의 모든 개념 문서를 각각 아주 길게 요약해줘.")
    page.click("#send")
    page.wait_for_timeout(5000)
    page.click("#send")
    page.wait_for_function("document.getElementById('send').textContent === '전송'", timeout=30_000)
    check("stop button ends the answer", "중지했어요" in page.locator(".msg.assistant .notice").last.inner_text())


def main() -> int:
    use_llm = "--llm" in sys.argv
    work = Path(tempfile.mkdtemp(prefix="wiki-ui-"))
    (work / "wiki").mkdir()
    for part in WIKI_PARTS:
        source = REPO / part
        (shutil.copytree if source.is_dir() else shutil.copy2)(source, work / "wiki" / part)
    port = free_port()
    env = {**os.environ, "WIKI_ROOT": str(work / "wiki"), "WIKI_CHAT_DATA": str(work / "data")}
    server = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.server:app", "--port", str(port)],
        cwd=REPO, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    base = f"http://127.0.0.1:{port}"
    try:
        for _ in range(60):
            try:
                urllib.request.urlopen(base + "/api/wiki").close()
                break
            except OSError:
                time.sleep(0.5)
        errors: list[str] = []
        with sync_playwright() as p:
            browser = p.chromium.launch(channel="chrome")
            page = browser.new_page(viewport={"width": 1280, "height": 900})
            page.on("pageerror", lambda e: errors.append(str(e)))
            page.on("dialog", lambda d: d.accept())
            ui_only(page, base)
            if use_llm:
                with_llm(page, base)
            browser.close()
        check("no JavaScript errors", not errors)
    finally:
        server.kill()
        shutil.rmtree(work, ignore_errors=True)
    failed = [name for name, ok in results if not ok]
    print(f"\n{len(results) - len(failed)}/{len(results)} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
