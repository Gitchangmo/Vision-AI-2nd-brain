// Chat client: streams answers over SSE, previews images, and saves each
// conversation to the local server after every answer.

const messagesEl = document.getElementById("messages");
const emptyEl = document.getElementById("empty");
const form = document.getElementById("composer");
const input = document.getElementById("input");
const sendBtn = document.getElementById("send");
const attachBtn = document.getElementById("attach");
const fileInput = document.getElementById("file");
const attachmentsEl = document.getElementById("attachments");
const dropOverlay = document.getElementById("drop-overlay");
const listEl = document.getElementById("conversation-list");
const backdrop = document.getElementById("sidebar-backdrop");
const lightbox = document.getElementById("lightbox");
const lightboxImage = document.getElementById("lightbox-image");
const lightboxCounter = document.getElementById("lightbox-counter");
const lightboxPrev = document.getElementById("lightbox-prev");
const lightboxNext = document.getElementById("lightbox-next");

const MAX_IMAGES = 5;
// Claude does not use detail beyond about 1568 px on the long edge, so larger
// images are scaled down before upload.
const MAX_EDGE = 1568;
const IMAGE_TYPES = ["image/jpeg", "image/png", "image/gif", "image/webp"];
const IMAGE_ONLY_QUESTION = "첨부한 이미지를 위키 관점에서 분석해줘.";

// Anthropic message params. Assistant turns keep the exact content the server
// returned so they can be sent back unchanged.
let history = [];
// Display-only notes (model, tokens) keyed by message index; saved alongside.
let meta = {};
let conversationId = null;
// Images waiting to be sent: {mediaType, data (base64), url (for preview)}.
let pending = [];
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

function textOf(content) {
  if (typeof content === "string") return content;
  return content.filter((b) => b.type === "text").map((b) => b.text).join("");
}

function imagesOf(content) {
  if (typeof content === "string") return [];
  return content
    .filter((b) => b.type === "image")
    .map((b) => ({ url: `data:${b.source.media_type};base64,${b.source.data}` }));
}

// --- lightbox ----------------------------------------------------------------

let lightboxUrls = [];
let lightboxIndex = 0;

function showLightboxImage() {
  lightboxImage.src = lightboxUrls[lightboxIndex];
  const many = lightboxUrls.length > 1;
  lightboxPrev.hidden = !many;
  lightboxNext.hidden = !many;
  lightboxCounter.textContent = many ? `${lightboxIndex + 1} / ${lightboxUrls.length}` : "";
}

function openLightbox(urls, index) {
  lightboxUrls = urls;
  lightboxIndex = index;
  showLightboxImage();
  lightbox.hidden = false;
}

function closeLightbox() {
  lightbox.hidden = true;
  lightboxImage.removeAttribute("src");
}

function stepLightbox(delta) {
  lightboxIndex = (lightboxIndex + delta + lightboxUrls.length) % lightboxUrls.length;
  showLightboxImage();
}

lightbox.addEventListener("click", (e) => {
  if (e.target === lightbox) closeLightbox();
});
document.getElementById("lightbox-close").addEventListener("click", closeLightbox);
lightboxPrev.addEventListener("click", () => stepLightbox(-1));
lightboxNext.addEventListener("click", () => stepLightbox(1));
document.addEventListener("keydown", (e) => {
  if (lightbox.hidden) return;
  if (e.key === "Escape") closeLightbox();
  else if (e.key === "ArrowLeft") stepLightbox(-1);
  else if (e.key === "ArrowRight") stepLightbox(1);
});

function thumbnail(urls, index, alt) {
  const img = document.createElement("img");
  img.src = urls[index];
  img.alt = alt;
  img.addEventListener("click", () => openLightbox(urls, index));
  return img;
}

// --- attachments -------------------------------------------------------------

function loadImage(file) {
  return new Promise((resolve, reject) => {
    const url = URL.createObjectURL(file);
    const img = new Image();
    img.onload = () => resolve({ img, url });
    img.onerror = () => {
      URL.revokeObjectURL(url);
      reject(new Error(`${file.name || "이미지"}를 읽지 못했습니다.`));
    };
    img.src = url;
  });
}

function blobToBase64(blob) {
  return new Promise((resolve) => {
    const reader = new FileReader();
    reader.onload = () => resolve(reader.result.split(",")[1]);
    reader.readAsDataURL(blob);
  });
}

// Small images in a supported format go as-is; anything larger is redrawn at
// MAX_EDGE and sent as JPEG.
async function prepareImage(file) {
  const { img, url } = await loadImage(file);
  const scale = Math.min(1, MAX_EDGE / Math.max(img.naturalWidth, img.naturalHeight));
  if (scale === 1 && IMAGE_TYPES.includes(file.type) && file.size <= 3_500_000) {
    return { mediaType: file.type, data: await blobToBase64(file), url };
  }
  const canvas = document.createElement("canvas");
  canvas.width = Math.round(img.naturalWidth * scale);
  canvas.height = Math.round(img.naturalHeight * scale);
  const ctx = canvas.getContext("2d");
  ctx.fillStyle = "#fff"; // transparent PNG areas would turn black in JPEG
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
  const blob = await new Promise((resolve) => canvas.toBlob(resolve, "image/jpeg", 0.92));
  URL.revokeObjectURL(url);
  return { mediaType: "image/jpeg", data: await blobToBase64(blob), url: URL.createObjectURL(blob) };
}

async function addFiles(files) {
  const images = [...files].filter((f) => f.type.startsWith("image/"));
  for (const file of images) {
    if (pending.length >= MAX_IMAGES) {
      addNotice(`이미지는 한 번에 ${MAX_IMAGES}장까지 첨부할 수 있어요.`);
      break;
    }
    try {
      pending.push(await prepareImage(file));
    } catch (err) {
      addNotice(err.message);
    }
  }
  renderAttachments();
}

function renderAttachments() {
  attachmentsEl.replaceChildren();
  attachmentsEl.hidden = pending.length === 0;
  const urls = pending.map((item) => item.url);
  pending.forEach((item, i) => {
    const wrap = document.createElement("div");
    wrap.className = "thumb";
    const remove = document.createElement("button");
    remove.type = "button";
    remove.textContent = "✕";
    remove.setAttribute("aria-label", "첨부 삭제");
    remove.addEventListener("click", () => {
      URL.revokeObjectURL(item.url);
      pending.splice(i, 1);
      renderAttachments();
    });
    wrap.append(thumbnail(urls, i, `첨부 이미지 ${i + 1}`), remove);
    attachmentsEl.appendChild(wrap);
  });
}

// --- message rendering -------------------------------------------------------

function addNotice(message) {
  emptyEl.hidden = true;
  const p = document.createElement("p");
  p.className = "notice";
  p.textContent = message;
  messagesEl.appendChild(p);
  p.scrollIntoView({ block: "end" });
}

function addLine(parent, className, text) {
  const p = document.createElement("p");
  p.className = className;
  p.textContent = text;
  parent.appendChild(p);
}

function renderUser(text, images) {
  emptyEl.hidden = true;
  const el = document.createElement("div");
  el.className = "msg user";
  if (images.length) {
    const strip = document.createElement("div");
    strip.className = "images";
    const urls = images.map((item) => item.url);
    urls.forEach((_, i) => strip.appendChild(thumbnail(urls, i, `첨부 이미지 ${i + 1}`)));
    el.appendChild(strip);
  }
  el.appendChild(document.createTextNode(text));
  messagesEl.appendChild(el);
  el.scrollIntoView({ block: "end" });
}

function renderAssistant() {
  const box = document.createElement("div");
  box.className = "msg assistant";
  const body = document.createElement("div");
  box.appendChild(body);
  messagesEl.appendChild(box);
  box.scrollIntoView({ block: "end" });
  return { box, body };
}

function clearMessages() {
  messagesEl.querySelectorAll(".msg, .notice").forEach((el) => el.remove());
}

function renderHistory() {
  clearMessages();
  emptyEl.hidden = history.length > 0;
  history.forEach((message, i) => {
    if (message.role === "user") {
      renderUser(textOf(message.content), imagesOf(message.content));
    } else {
      const { box, body } = renderAssistant();
      body.innerHTML = renderMarkdown(textOf(message.content));
      if (meta[i]) addLine(box, "meta", meta[i]);
    }
  });
}

// --- saved conversations -----------------------------------------------------

function titleOf(messages) {
  const first = messages.find((m) => m.role === "user");
  const text = first ? textOf(first.content).trim() : "";
  if (!text || text === IMAGE_ONLY_QUESTION) return "이미지 질문";
  return text.length > 40 ? `${text.slice(0, 40)}…` : text;
}

function formatDate(iso) {
  const d = new Date(iso);
  return Number.isNaN(d.getTime())
    ? ""
    : d.toLocaleString("ko-KR", { month: "numeric", day: "numeric", hour: "2-digit", minute: "2-digit" });
}

async function refreshList() {
  let items = [];
  try {
    const res = await fetch("/api/conversations");
    items = await res.json();
  } catch {
    items = null;
  }
  listEl.replaceChildren();
  if (!items || !items.length) {
    const li = document.createElement("li");
    li.className = "none";
    li.textContent = items ? "저장된 대화가 없어요." : "목록을 불러오지 못했어요.";
    listEl.appendChild(li);
    return;
  }
  for (const item of items) {
    const li = document.createElement("li");
    if (item.id === conversationId) li.classList.add("active");

    const open = document.createElement("button");
    open.type = "button";
    open.className = "open";
    const title = document.createElement("span");
    title.className = "title";
    title.textContent = item.title || "제목 없음";
    const date = document.createElement("span");
    date.className = "date";
    date.textContent = formatDate(item.updated_at);
    open.append(title, date);
    open.addEventListener("click", () => openConversation(item.id));

    const del = document.createElement("button");
    del.type = "button";
    del.className = "delete";
    del.textContent = "✕";
    del.setAttribute("aria-label", `"${item.title}" 삭제`);
    del.addEventListener("click", () => deleteConversation(item.id, item.title));

    li.append(open, del);
    listEl.appendChild(li);
  }
}

async function saveConversation() {
  if (!conversationId) conversationId = crypto.randomUUID().replaceAll("-", "");
  try {
    const res = await fetch(`/api/conversations/${conversationId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title: titleOf(history), messages: history, meta }),
    });
    if (!res.ok) throw new Error((await res.json()).detail || res.status);
  } catch (err) {
    addNotice(`대화를 저장하지 못했어요: ${err.message}`);
  }
  refreshList();
}

async function openConversation(id) {
  if (busy) return;
  closeSidebar();
  const res = await fetch(`/api/conversations/${id}`);
  if (!res.ok) {
    addNotice("대화를 불러오지 못했어요.");
    refreshList();
    return;
  }
  const data = await res.json();
  conversationId = id;
  history = data.messages;
  meta = data.meta || {};
  renderHistory();
  refreshList();
}

async function deleteConversation(id, title) {
  if (busy) return;
  if (!confirm(`"${title}" 대화를 삭제할까요? 되돌릴 수 없어요.`)) return;
  await fetch(`/api/conversations/${id}`, { method: "DELETE" });
  if (id === conversationId) startNewConversation();
  refreshList();
}

function startNewConversation() {
  history = [];
  meta = {};
  conversationId = null;
  clearMessages();
  emptyEl.hidden = false;
  refreshList();
  input.focus();
}

// --- asking ------------------------------------------------------------------

function userContent(question, images) {
  if (!images.length) return question;
  return [
    ...images.map((item) => ({
      type: "image",
      source: { type: "base64", media_type: item.mediaType, data: item.data },
    })),
    { type: "text", text: question },
  ];
}

async function ask(question, images = []) {
  busy = true;
  sendBtn.disabled = true;
  history.push({ role: "user", content: userContent(question, images) });
  renderUser(question, images);

  const { box, body } = renderAssistant();
  body.className = "pending";

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
          const note = `${event.model} · 입력 ${u.input + u.cache_read + u.cache_write} (캐시 ${u.cache_read}) · 출력 ${u.output} 토큰`;
          meta[history.length - 1] = note;
          addLine(box, "meta", note);
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
  if (finished) saveConversation();
}

// --- events ------------------------------------------------------------------

form.addEventListener("submit", (e) => {
  e.preventDefault();
  if (busy) return;
  const images = pending;
  const question = input.value.trim() || (images.length ? IMAGE_ONLY_QUESTION : "");
  if (!question) return;
  pending = [];
  renderAttachments();
  input.value = "";
  input.style.height = "auto";
  ask(question, images);
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

input.addEventListener("paste", (e) => {
  const files = [...e.clipboardData.files];
  if (files.some((f) => f.type.startsWith("image/"))) {
    e.preventDefault();
    addFiles(files);
  }
});

attachBtn.addEventListener("click", () => fileInput.click());
fileInput.addEventListener("change", () => {
  addFiles(fileInput.files);
  fileInput.value = "";
});

let dragDepth = 0;
window.addEventListener("dragenter", (e) => {
  if (![...e.dataTransfer.types].includes("Files")) return;
  dragDepth += 1;
  dropOverlay.hidden = false;
});
window.addEventListener("dragleave", () => {
  dragDepth = Math.max(0, dragDepth - 1);
  if (dragDepth === 0) dropOverlay.hidden = true;
});
window.addEventListener("dragover", (e) => e.preventDefault());
window.addEventListener("drop", (e) => {
  e.preventDefault();
  dragDepth = 0;
  dropOverlay.hidden = true;
  addFiles(e.dataTransfer.files);
});

document.querySelectorAll(".example").forEach((btn) =>
  btn.addEventListener("click", () => {
    if (!busy) ask(btn.textContent);
  }),
);

document.getElementById("new-chat").addEventListener("click", () => {
  if (busy) return;
  closeSidebar();
  startNewConversation();
});

function closeSidebar() {
  document.body.classList.remove("sidebar-open");
  backdrop.hidden = true;
}
document.getElementById("toggle-sidebar").addEventListener("click", () => {
  document.body.classList.add("sidebar-open");
  backdrop.hidden = false;
});
backdrop.addEventListener("click", closeSidebar);

fetch("/api/wiki")
  .then((r) => r.json())
  .then((w) => {
    document.getElementById("wiki-info").textContent =
      `정식 문서 ${w.canonical_pages}개 · 원본 ${w.raw_records}개 · ${w.backend === "cli" ? "Claude Code 구독" : "API"} · ${w.model} (effort ${w.effort})`;
  })
  .catch(() => {
    document.getElementById("wiki-info").textContent = "위키 정보를 불러오지 못했습니다.";
  });

refreshList();
