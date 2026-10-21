// Chat client: keeps the conversation in memory and streams answers over SSE.

const messagesEl = document.getElementById("messages");
const emptyEl = document.getElementById("empty");
const form = document.getElementById("composer");
const input = document.getElementById("input");
const sendBtn = document.getElementById("send");

// Anthropic message params. Assistant turns keep the exact content blocks the
// server returned so they can be sent back unchanged.
let history = [];
let busy = false;

function renderMarkdown(text) {
  const withLinks = text.replace(
    /\[\[([^\]|]+)(?:\|([^\]]+))?\]\]/g,
    (_, path, label) => `<span class="wikilink" title="${path}">${label || path}</span>`,
  );
  if (window.marked && window.DOMPurify) {
    return DOMPurify.sanitize(marked.parse(withLinks));
  }
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML.replace(/\n/g, "<br>");
}

function addMessage(role, text = "") {
  emptyEl.hidden = true;
  const el = document.createElement("div");
  el.className = `msg ${role}`;
  if (role === "user") el.textContent = text;
  messagesEl.appendChild(el);
  el.scrollIntoView({ block: "end" });
  return el;
}

function addLine(parent, className, text) {
  const p = document.createElement("p");
  p.className = className;
  p.textContent = text;
  parent.appendChild(p);
}

async function ask(question) {
  busy = true;
  sendBtn.disabled = true;
  history.push({ role: "user", content: question });
  addMessage("user", question);

  const box = addMessage("assistant");
  const body = document.createElement("div");
  body.className = "pending";
  box.appendChild(body);

  let text = "";
  let finished = false;
  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ messages: history }),
    });
    if (!res.ok) throw new Error(`서버 오류 (${res.status})`);

    const reader = res.body.getReader();
    const decoder = new TextDecoder();
    let buffer = "";
    while (true) {
      const { value, done } = await reader.read();
      if (done) break;
      buffer += decoder.decode(value, { stream: true });
      const events = buffer.split("\n\n");
      buffer = events.pop();
      for (const raw of events) {
        if (!raw.startsWith("data: ")) continue;
        const event = JSON.parse(raw.slice(6));
        if (event.type === "text") {
          text += event.text;
          body.innerHTML = renderMarkdown(text);
          box.scrollIntoView({ block: "end" });
        } else if (event.type === "notice") {
          addLine(box, "notice", event.message);
        } else if (event.type === "error") {
          addLine(box, "error", event.message);
        } else if (event.type === "done") {
          finished = true;
          history.push({ role: "assistant", content: event.content });
          const u = event.usage;
          addLine(box, "meta", `${event.model} · 입력 ${u.input + u.cache_read + u.cache_write} (캐시 ${u.cache_read}) · 출력 ${u.output} 토큰`);
        }
      }
    }
  } catch (err) {
    addLine(box, "error", err.message);
  } finally {
    body.classList.remove("pending");
    if (!finished) history.pop(); // drop the unanswered question so the next request stays valid
    busy = false;
    sendBtn.disabled = false;
    input.focus();
  }
}

form.addEventListener("submit", (e) => {
  e.preventDefault();
  const question = input.value.trim();
  if (!question || busy) return;
  input.value = "";
  input.style.height = "auto";
  ask(question);
});

input.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey && !e.isComposing) {
    e.preventDefault();
    form.requestSubmit();
  }
});

input.addEventListener("input", () => {
  input.style.height = "auto";
  input.style.height = `${input.scrollHeight}px`;
});

document.querySelectorAll(".example").forEach((btn) =>
  btn.addEventListener("click", () => {
    if (!busy) ask(btn.textContent);
  }),
);

document.getElementById("new-chat").addEventListener("click", () => {
  if (busy) return;
  history = [];
  messagesEl.querySelectorAll(".msg").forEach((el) => el.remove());
  emptyEl.hidden = false;
  input.focus();
});

fetch("/api/wiki")
  .then((r) => r.json())
  .then((w) => {
    document.getElementById("wiki-info").textContent =
      `정식 문서 ${w.canonical_pages}개 · 원본 ${w.raw_records}개 · ${w.backend === "cli" ? "Claude Code 구독" : "API"} · ${w.model} (effort ${w.effort})`;
  })
  .catch(() => {
    document.getElementById("wiki-info").textContent = "위키 정보를 불러오지 못했습니다.";
  });
