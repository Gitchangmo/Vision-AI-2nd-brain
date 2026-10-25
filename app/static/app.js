// Chat client: streams answers over SSE, previews images, saves conversations,
// opens wiki documents, files answers into the wiki, and takes field notes.

const $ = (id) => document.getElementById(id);
const messagesEl = $("messages");
const emptyEl = $("empty");
const form = $("composer");
const input = $("input");
const sendBtn = $("send");
const attachmentsEl = $("attachments");
const listEl = $("conversation-list");

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
let controller = null;
let requestId = null;

const newId = () => crypto.randomUUID().replaceAll("-", "");

function escapeHtml(text) {
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}

async function postJson(url, body, method = "POST") {
  const res = await fetch(url, {
    method,
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  let data = {};
  try {
    data = await res.json();
  } catch {
    // keep the empty object; the status code still tells what happened
  }
  return { ok: res.ok, status: res.status, data };
}

// --- markdown with links into the wiki ------------------------------------------

function docLink(className, path, label) {
  const p = escapeHtml(path).replaceAll('"', "&quot;");
  return `<a href="#" class="${className}" data-doc="${p}" title="${p}">${escapeHtml(label)}</a>`;
}

// Wiki links, claim markers and bare raw paths become clickable. They are
// swapped for placeholders first so Markdown parsing cannot mangle them.
function renderMarkdown(text) {
  const links = [];
  const keep = (html) => `@@LINK${links.push(html) - 1}@@`;
  const source = text
    .replace(/\^\[(raw\/[^\]\s]+\.md)\]/g, (_, path) => keep(docLink("rawlink", path, "출처")))
    .replace(/\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|([^\]]+))?\]\]/g, (_, path, label) =>
      keep(docLink("wikilink", `${path.trim()}.md`, label || path.trim())),
    )
    .replace(/(?<![\w/])raw\/[\w.\/-]+\.md/g, (path) => keep(docLink("rawlink", path, path)));
  const html =
    window.marked && window.DOMPurify ? marked.parse(source) : escapeHtml(source).replace(/\n/g, "<br>");
  const linked = html.replace(/@@LINK(\d+)@@/g, (_, i) => links[Number(i)]);
  return window.DOMPurify ? DOMPurify.sanitize(linked) : linked;
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

function report(el, { issues = [], findings = [] } = {}, okText = "") {
  el.replaceChildren();
  const errors = issues.filter((i) => (i.level || "error") === "error");
  const warnings = issues.filter((i) => i.level === "warning");
  const box = (cls, title, items) => {
    const div = document.createElement("div");
    div.className = `box ${cls}`;
    div.innerHTML = `<strong>${escapeHtml(title)}</strong>`;
    if (items.length) {
      const ul = document.createElement("ul");
      for (const item of items) {
        const li = document.createElement("li");
        li.textContent = item;
        ul.appendChild(li);
      }
      div.appendChild(ul);
    }
    el.appendChild(div);
  };
  if (findings.length) box("bad", "민감 정보가 남아 있어요 (저장 불가)", findings.map((f) => `${f.kind}: ${f.match}`));
  if (errors.length) box("bad", "위키 검사 오류 (저장 불가)", errors.map((i) => i.message || i));
  if (warnings.length) box("warn", "경고", warnings.map((i) => i.message));
  if (!findings.length && !errors.length && okText) box("good", okText, []);
}

// --- lightbox ----------------------------------------------------------------

const lightbox = $("lightbox");
let lightboxUrls = [];
let lightboxIndex = 0;

function showLightboxImage() {
  $("lightbox-image").src = lightboxUrls[lightboxIndex];
  const many = lightboxUrls.length > 1;
  $("lightbox-prev").hidden = !many;
  $("lightbox-next").hidden = !many;
  $("lightbox-counter").textContent = many ? `${lightboxIndex + 1} / ${lightboxUrls.length}` : "";
}

function openLightbox(urls, index) {
  lightboxUrls = urls;
  lightboxIndex = index;
  showLightboxImage();
  lightbox.hidden = false;
}

function closeLightbox() {
  lightbox.hidden = true;
  $("lightbox-image").removeAttribute("src");
}

function stepLightbox(delta) {
  lightboxIndex = (lightboxIndex + delta + lightboxUrls.length) % lightboxUrls.length;
  showLightboxImage();
}

lightbox.addEventListener("click", (e) => {
  if (e.target === lightbox) closeLightbox();
});
$("lightbox-close").addEventListener("click", closeLightbox);
$("lightbox-prev").addEventListener("click", () => stepLightbox(-1));
$("lightbox-next").addEventListener("click", () => stepLightbox(1));

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

function addNotice(message, html = false) {
  emptyEl.hidden = true;
  const p = document.createElement("p");
  p.className = "notice";
  if (html) p.innerHTML = message;
  else p.textContent = message;
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
  body.className = "markdown";
  box.appendChild(body);
  messagesEl.appendChild(box);
  box.scrollIntoView({ block: "end" });
  return { box, body };
}

// Actions under a finished answer; `index` is the answer's position in history.
function addActions(box, index) {
  const actions = document.createElement("div");
  actions.className = "actions";
  const draft = document.createElement("button");
  draft.type = "button";
  draft.textContent = "📄 위키 초안으로";
  draft.title = "이 답변까지의 대화를 익명화된 위키 문서 초안으로 만들어요";
  draft.addEventListener("click", () => openDraft(index));
  actions.appendChild(draft);
  box.appendChild(actions);
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
      addActions(box, i);
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
  let items = null;
  try {
    items = await (await fetch("/api/conversations")).json();
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
  if (!conversationId) conversationId = newId();
  const { ok, data } = await postJson(
    `/api/conversations/${conversationId}`,
    { title: titleOf(history), messages: history, meta },
    "PUT",
  ).catch((err) => ({ ok: false, data: { detail: err.message } }));
  if (!ok) addNotice(`대화를 저장하지 못했어요: ${data.detail || "알 수 없는 오류"}`);
  refreshList();
}

async function openConversation(id) {
  if (busy) return;
  closeSidebar();
  switchView("chat");
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

function setBusy(value) {
  busy = value;
  sendBtn.textContent = value ? "■ 중지" : "전송";
  sendBtn.title = value ? "답변 생성을 멈춰요" : "";
}

function stopAnswer() {
  controller?.abort();
  if (requestId) fetch(`/api/chat/${requestId}/cancel`, { method: "POST" }).catch(() => {});
}

async function ask(question, images = []) {
  setBusy(true);
  controller = new AbortController();
  requestId = newId();
  history.push({ role: "user", content: userContent(question, images) });
  renderUser(question, images);

  const { box, body } = renderAssistant();
  body.classList.add("pending");

  let text = "";
  let finished = false;
  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ messages: history, request_id: requestId }),
      signal: controller.signal,
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
          addActions(box, history.length - 1);
        }
      }
    }
  } catch (err) {
    if (err.name === "AbortError") addLine(box, "notice", "중지했어요. 이 답변은 대화 기록에 남지 않아요.");
    else addLine(box, "error", err.message);
  } finally {
    body.classList.remove("pending");
    if (!finished) history.pop(); // drop the unanswered question so the next request stays valid
    controller = null;
    requestId = null;
    setBusy(false);
    input.focus();
  }
  if (finished) saveConversation();
}

// --- document drawer -----------------------------------------------------------

const drawer = $("doc-drawer");
let docStack = [];

async function openDoc(path, push = true) {
  const res = await fetch(`/api/doc?path=${encodeURIComponent(path)}`);
  const docBody = $("doc-body");
  drawer.hidden = false;
  $("doc-path").textContent = path;
  if (!res.ok) {
    docBody.innerHTML = `<p class="error">문서를 찾을 수 없어요: ${escapeHtml(path)}</p>`;
  } else {
    const { text } = await res.json();
    const match = text.match(/^---\n([\s\S]*?)\n---\n/);
    const front = match ? `<pre class="frontmatter">${escapeHtml(match[1])}</pre>` : "";
    docBody.innerHTML = front + renderMarkdown(match ? text.slice(match[0].length) : text);
    docBody.scrollTop = 0;
  }
  if (push) docStack.push(path);
  $("doc-back").disabled = docStack.length < 2;
}

function closeDoc() {
  drawer.hidden = true;
  docStack = [];
}

$("doc-close").addEventListener("click", closeDoc);
$("doc-back").addEventListener("click", () => {
  if (docStack.length < 2) return;
  docStack.pop();
  openDoc(docStack[docStack.length - 1], false);
});

document.addEventListener("click", (e) => {
  const link = e.target.closest("[data-doc]");
  if (!link) return;
  e.preventDefault();
  openDoc(link.dataset.doc);
});

// --- wiki draft from an answer -------------------------------------------------

const draftModal = $("draft-modal");
let draftBusy = false;

function draftPage() {
  return { path: $("draft-path").value.trim(), text: $("draft-text").value, summary: $("draft-summary").value.trim() };
}

async function openDraft(index) {
  if (draftBusy) return;
  draftBusy = true;
  draftModal.hidden = false;
  $("draft-form").hidden = true;
  $("draft-status").textContent = "초안을 만드는 중이에요. 위키 전체를 참고해서 30초~1분 정도 걸려요…";
  const { ok, data } = await postJson("/api/wiki-drafts", { messages: history.slice(0, index + 1) }).catch((err) => ({
    ok: false,
    data: { detail: err.message },
  }));
  draftBusy = false;
  if (!ok) {
    $("draft-status").textContent = `초안을 만들지 못했어요: ${data.detail || "알 수 없는 오류"}`;
    return;
  }
  $("draft-status").textContent = "익명화된 초안이에요. 내용을 확인하고 필요하면 고친 뒤 저장하세요.";
  $("draft-path").value = data.path;
  $("draft-summary").value = data.summary;
  $("draft-text").value = data.text;
  const warnings = $("draft-warnings");
  warnings.replaceChildren();
  if (data.warnings.length) report(warnings, { issues: data.warnings.map((w) => ({ level: "warning", message: w })) });
  report($("draft-issues"), data, "위키 검사와 민감어 검사를 통과했어요.");
  $("draft-form").hidden = false;
}

$("draft-check").addEventListener("click", async () => {
  const { data } = await postJson("/api/wiki-drafts/check", draftPage());
  report($("draft-issues"), data, "위키 검사와 민감어 검사를 통과했어요.");
});

$("draft-save").addEventListener("click", async () => {
  const page = draftPage();
  const { ok, data } = await postJson("/api/wiki-drafts/save", page);
  if (!ok) {
    report($("draft-issues"), {
      issues: (data.issues || []).map((m) => ({ level: "error", message: m })),
      findings: data.findings || [],
    });
    return;
  }
  draftModal.hidden = true;
  addNotice(`위키에 저장했어요: ${docLink("wikilink", data.path, data.path)} (index.md, log.md 갱신)`, true);
  loadWikiInfo();
});

$("draft-close").addEventListener("click", () => {
  draftModal.hidden = true;
});

// --- field notes ---------------------------------------------------------------

const noteForm = $("note-form");
let noteBusy = false;

function thisMonth() {
  const d = new Date();
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}`;
}

async function loadTerms() {
  const { terms } = await (await fetch("/api/sensitive-terms")).json();
  $("terms").value = terms.join("\n");
  $("terms-count").textContent = `(${terms.length}개)`;
}

$("save-terms").addEventListener("click", async () => {
  const terms = $("terms").value.split("\n");
  const { ok, data } = await postJson("/api/sensitive-terms", { terms }, "PUT");
  $("terms-status").textContent = ok ? `저장했어요 (${data.terms.length}개)` : "저장하지 못했어요";
  if (ok) {
    $("terms").value = data.terms.join("\n");
    $("terms-count").textContent = `(${data.terms.length}개)`;
  }
});

function noteMeta() {
  return {
    process: $("note-process").value,
    status: $("note-status").value,
    date: $("note-date").value,
  };
}

noteForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  if (noteBusy) return;
  const sections = {};
  noteForm.querySelectorAll("textarea[data-section]").forEach((t) => {
    sections[t.dataset.section] = t.value;
  });
  if (!Object.values(sections).some((v) => v.trim())) {
    $("note-status-line").textContent = "내용을 한 칸 이상 적어 주세요.";
    return;
  }
  noteBusy = true;
  $("note-draft").disabled = true;
  $("note-status-line").textContent = "익명화 초안을 만드는 중이에요 (30초 정도)…";
  const { ok, data } = await postJson("/api/field-notes/draft", {
    title: $("note-title").value,
    sections,
    ...noteMeta(),
  }).catch((err) => ({ ok: false, data: { detail: err.message } }));
  noteBusy = false;
  $("note-draft").disabled = false;
  if (!ok) {
    $("note-status-line").textContent = `초안을 만들지 못했어요: ${data.detail || "알 수 없는 오류"}`;
    return;
  }
  $("note-status-line").textContent = "";
  $("review-title").value = data.title;
  $("review-body").value = data.body;
  const rows = $("note-replacements").querySelector("tbody");
  rows.replaceChildren();
  for (const r of data.replacements) {
    const tr = document.createElement("tr");
    for (const value of [r.category, r.before, r.after]) {
      const td = document.createElement("td");
      td.textContent = value;
      tr.appendChild(td);
    }
    rows.appendChild(tr);
  }
  $("note-replacements").hidden = data.replacements.length === 0;
  report($("note-warnings"), { issues: data.warnings.map((w) => ({ level: "warning", message: w })) });
  report($("note-findings"), data, "민감어 검사를 통과했어요. 내용을 확인하고 저장하세요.");
  $("note-review").hidden = false;
  $("note-review").scrollIntoView({ block: "start", behavior: "smooth" });
});

$("note-save").addEventListener("click", async () => {
  const { ok, data } = await postJson("/api/field-notes", {
    title: $("review-title").value,
    body: $("review-body").value,
    ...noteMeta(),
  });
  if (!ok) {
    report($("note-findings"), {
      issues: (data.issues || []).map((m) => ({ level: "error", message: m })),
      findings: data.findings || [],
    });
    return;
  }
  $("note-review").hidden = true;
  noteForm.reset();
  $("note-date").value = thisMonth();
  $("note-status-line").innerHTML = `저장했어요: ${docLink("rawlink", data.path, data.path)} — 이제 채팅 답변의 근거로 쓰여요.`;
  loadWikiInfo();
});

$("note-discard").addEventListener("click", () => {
  $("note-review").hidden = true;
});

// --- views, sidebar, input events -----------------------------------------------

function switchView(view) {
  const chat = view === "chat";
  messagesEl.hidden = !chat;
  form.hidden = !chat;
  $("note-view").hidden = chat;
  document.querySelectorAll(".tab").forEach((tab) => tab.classList.toggle("active", tab.dataset.view === view));
  if (!chat) loadTerms();
}

document.querySelectorAll(".tab").forEach((tab) => tab.addEventListener("click", () => switchView(tab.dataset.view)));

form.addEventListener("submit", (e) => {
  e.preventDefault();
  if (busy) {
    stopAnswer();
    return;
  }
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
    if (!busy) form.requestSubmit();
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

$("attach").addEventListener("click", () => $("file").click());
$("file").addEventListener("change", () => {
  addFiles($("file").files);
  $("file").value = "";
});

let dragDepth = 0;
const dropOverlay = $("drop-overlay");
window.addEventListener("dragenter", (e) => {
  if (form.hidden || ![...e.dataTransfer.types].includes("Files")) return;
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
  if (!form.hidden) addFiles(e.dataTransfer.files);
});

document.addEventListener("keydown", (e) => {
  if (e.key !== "Escape" && !lightbox.hidden) {
    if (e.key === "ArrowLeft") stepLightbox(-1);
    else if (e.key === "ArrowRight") stepLightbox(1);
    return;
  }
  if (e.key !== "Escape") return;
  if (!lightbox.hidden) closeLightbox();
  else if (!draftModal.hidden) draftModal.hidden = true;
  else if (!drawer.hidden) closeDoc();
});

document.querySelectorAll(".example").forEach((btn) =>
  btn.addEventListener("click", () => {
    if (!busy) ask(btn.textContent);
  }),
);

$("new-chat").addEventListener("click", () => {
  if (busy) return;
  closeSidebar();
  switchView("chat");
  startNewConversation();
});

const backdrop = $("sidebar-backdrop");
function closeSidebar() {
  document.body.classList.remove("sidebar-open");
  backdrop.hidden = true;
}
$("toggle-sidebar").addEventListener("click", () => {
  document.body.classList.add("sidebar-open");
  backdrop.hidden = false;
});
backdrop.addEventListener("click", closeSidebar);

function loadWikiInfo() {
  fetch("/api/wiki")
    .then((r) => r.json())
    .then((w) => {
      $("wiki-info").textContent =
        `정식 문서 ${w.canonical_pages}개 · 원본 ${w.raw_records}개 · ${w.backend === "cli" ? "Claude Code 구독" : "API"} · ${w.model} (effort ${w.effort})`;
    })
    .catch(() => {
      $("wiki-info").textContent = "위키 정보를 불러오지 못했습니다.";
    });
}

$("note-date").value = thisMonth();
loadWikiInfo();
refreshList();
