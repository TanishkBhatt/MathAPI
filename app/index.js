(() => {
  "use strict";

  const API_BASE = "https://mathapi.vercel.app";
  const KEYS = Object.freeze({ api: "mathlabs.apiKey", state: "mathlabs.state", legacy: "mathlabs.session" });
  const TTL = Object.freeze({ topics: 600000, explanation: 1800000, content: 1800000, daily: 3600000 });
  const BRANCHES = Object.freeze(["Number Theory", "Algebra", "Geometry", "Coordinate Geometry", "Trigonometry", "Applied Mathematics"]);
  const LEVELS = Object.freeze(["Beginner", "Intermediate", "Advanced"]);
  const TYPES = Object.freeze(["Conceptual", "Numerical", "To Prove", "Word Problem", "Case Based", "Higher Order Thinking Skills"]);
  const TABS = Object.freeze(["explanation", "examples", "questions", "formulae", "sources"]);
  const ROUTES = Object.freeze({
    dashboard: ["Workspace", "Dashboard"], topics: ["Library", "Explore Topics"], topic: ["Topic studio", "Topic"],
    practice: ["Workspace", "Practice Arena"], daily: ["Discover", "Daily Challenge"], random: ["Discover", "Random Question"],
    formulas: ["Library", "Formula Vault"], saved: ["Your data", "Saved & Progress"], settings: ["Your data", "Settings"]
  });
  const SVG = Object.freeze({
    dashboard: '<rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/>',
    book: '<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2Z"/>',
    target: '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.5"/>',
    calendar: '<rect x="3" y="4" width="18" height="17" rx="2"/><path d="M8 2v4M16 2v4M3 9h18"/>',
    shuffle: '<path d="M16 3h5v5"/><path d="M4 20 21 3"/><path d="M21 16v5h-5"/><path d="m15 15 6 6"/><path d="m4 4 5 5"/>',
    formula: '<path d="M18 4H7l6 8-6 8h11"/><path d="M4 4h14"/>',
    bookmark: '<path d="M6 3h12a1 1 0 0 1 1 1v17l-7-4-7 4V4a1 1 0 0 1 1-1Z"/>',
    settings: '<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.7 1.7 0 0 0 .34 1.87l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06A1.7 1.7 0 0 0 15 19.4a1.7 1.7 0 0 0-1 1.55V21a2 2 0 1 1-4 0v-.09A1.7 1.7 0 0 0 9 19.4a1.7 1.7 0 0 0-1.87.34l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06A1.7 1.7 0 0 0 4.6 15a1.7 1.7 0 0 0-1.55-1H3a2 2 0 1 1 0-4h.09A1.7 1.7 0 0 0 4.6 9a1.7 1.7 0 0 0-.34-1.87l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06A1.7 1.7 0 0 0 9 4.6a1.7 1.7 0 0 0 1-1.55V3a2 2 0 1 1 4 0v.09A1.7 1.7 0 0 0 15 4.6a1.7 1.7 0 0 0 1.87-.34l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06A1.7 1.7 0 0 0 19.4 9c.2.63.78 1.06 1.44 1.06H21a2 2 0 1 1 0 4h-.09A1.7 1.7 0 0 0 19.4 15Z"/>',
    refresh: '<path d="M20 11a8 8 0 1 0-2.34 5.66"/><path d="M20 4v7h-7"/>',
    database: '<ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v6c0 1.66 3.58 3 8 3s8-1.34 8-3V5"/><path d="M4 11v6c0 1.66 3.58 3 8 3s8-1.34 8-3v-6"/>',
    menu: '<path d="M4 7h16M4 12h16M4 17h16"/>',
    search: '<circle cx="11" cy="11" r="7"/><path d="m20 20-4-4"/>',
    "chevron-right": '<path d="m9 18 6-6-6-6"/>',
    "arrow-right": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "arrow-left": '<path d="M19 12H5M11 18l-6-6 6-6"/>',
    sparkles: '<path d="m12 3 1.6 4.4L18 9l-4.4 1.6L12 15l-1.6-4.4L6 9l4.4-1.6L12 3Z"/><path d="m5 16 .8 2.2L8 19l-2.2.8L5 22l-.8-2.2L2 19l2.2-.8L5 16Z"/><path d="m19 14 .7 1.8 1.8.7-1.8.7L19 19l-.7-1.8-1.8-.7 1.8-.7L19 14Z"/>',
    layers: '<path d="m12 3 9 5-9 5-9-5 9-5Z"/><path d="m3 12 9 5 9-5"/><path d="m3 16 9 5 9-5"/>',
    "file-text": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8Z"/><path d="M14 2v6h6M8 13h8M8 17h6"/>',
    link: '<path d="M10 13a5 5 0 0 0 7.5.5l2-2a5 5 0 0 0-7-7l-1.2 1.2"/><path d="M14 11a5 5 0 0 0-7.5-.5l-2 2a5 5 0 0 0 7 7l1.2-1.2"/>',
    external: '<path d="M15 3h6v6"/><path d="M10 14 21 3"/><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>',
    check: '<path d="m20 6-11 11-5-5"/>',
    x: '<path d="M18 6 6 18M6 6l12 12"/>',
    alert: '<path d="M10.3 3.9 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0Z"/><path d="M12 9v4M12 17h.01"/>',
    clock: '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    lightbulb: '<path d="M9 18h6M10 22h4"/><path d="M8.5 14.5A6 6 0 1 1 15.5 14.5c-.9.7-1.5 1.5-1.5 2.5h-4c0-1-.6-1.8-1.5-2.5Z"/>',
    copy: '<rect x="9" y="9" width="12" height="12" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>',
    play: '<path d="m7 4 13 8-13 8V4Z"/>',
    rotate: '<path d="M3 12a9 9 0 1 0 3-6.7L3 8"/><path d="M3 3v5h5"/>',
    trash: '<path d="M3 6h18M8 6V4h8v2M19 6l-1 15H6L5 6M10 10v7M14 10v7"/>',
    wifi: '<path d="M5 12.5a10 10 0 0 1 14 0"/><path d="M8.5 16a5 5 0 0 1 7 0"/><path d="M12 20h.01"/>',
    server: '<rect x="3" y="4" width="18" height="6" rx="2"/><rect x="3" y="14" width="18" height="6" rx="2"/><path d="M7 7h.01M7 17h.01"/>',
    lock: '<rect x="4" y="10" width="16" height="11" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/>',
    plus: '<path d="M12 5v14M5 12h14"/>',
    "check-circle": '<circle cx="12" cy="12" r="9"/><path d="m8 12 2.5 2.5L16 9"/>',
    "book-open": '<path d="M2 4h6a4 4 0 0 1 4 4v13a3 3 0 0 0-3-3H2V4Z"/><path d="M22 4h-6a4 4 0 0 0-4 4v13a3 3 0 0 1 3-3h7V4Z"/>'
  });

  const $ = (selector, root = document) => root.querySelector(selector);
  const $$ = (selector, root = document) => [...root.querySelectorAll(selector)];
  const esc = (value) => String(value ?? "").replace(/[&<>"']/g, (character) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[character]);
  const icon = (name, className = "icon") => `<svg class="${className}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${SVG[name] || SVG.sparkles}</svg>`;
  const paint = (root = document) => $$("[data-icon]", root).forEach((node) => { node.innerHTML = icon(node.dataset.icon); });
  const prose = (value) => String(value ?? "").trim().split(/\n{2,}/).filter(Boolean).map((block) => `<p>${esc(block).replace(/\n/g, "<br>")}</p>`).join("");
  const safeUrl = (value) => {
    try { const url = new URL(String(value ?? ""), window.location.href); return ["http:", "https:"].includes(url.protocol) ? esc(url.href) : ""; }
    catch (error) { return ""; }
  };
  const external = (url, label, className = "") => {
    const href = safeUrl(url);
    return href ? `<a class="${esc(className)}" href="${href}" target="_blank" rel="noopener noreferrer">${esc(label)}${icon("external")}</a>` : `<span class="${esc(className)}">${esc(label)}</span>`;
  };
  const safeTab = (value) => TABS.includes(value) ? value : "explanation";
  const diffChip = (value) => `<span class="chip difficulty difficulty-${esc(String(value || "unrated").toLowerCase())}">${esc(value || "Unrated")}</span>`;
  const chips = (values, className = "chip") => (Array.isArray(values) ? values : values ? [values] : []).map((value) => `<span class="${className}">${esc(value)}</span>`).join("");
  const formatDate = (value, options) => {
    if (!value) return "—";
    const date = value instanceof Date ? value : new Date(value);
    return Number.isNaN(date.getTime()) ? String(value) : new Intl.DateTimeFormat(undefined, options || { month: "short", day: "numeric", year: "numeric" }).format(date);
  };
  const formatDateTime = (value) => {
    if (!value) return "—";
    const date = value instanceof Date ? value : new Date(value);
    return Number.isNaN(date.getTime()) ? String(value) : new Intl.DateTimeFormat(undefined, { month: "short", day: "numeric", year: "numeric", hour: "numeric", minute: "2-digit" }).format(date);
  };
  const ago = (value) => {
    if (!value) return "Not started";
    const time = new Date(value).getTime();
    if (!Number.isFinite(time)) return "Not started";
    const seconds = Math.max(0, Math.round((Date.now() - time) / 1000));
    if (seconds < 60) return "Just now";
    const minutes = Math.round(seconds / 60), hours = Math.round(minutes / 60), days = Math.round(hours / 24);
    if (minutes < 60) return `${minutes}m ago`;
    if (hours < 24) return `${hours}h ago`;
    return days < 7 ? `${days}d ago` : formatDate(time);
  };
  const expiry = (apiKey) => {
    const match = /_exp=(\d+)/.exec(String(apiKey || "")), time = match ? Number(match[1]) * 1000 : 0;
    return Number.isFinite(time) ? time : 0;
  };
  const expired = (connection) => Boolean(expiry(connection?.apiKey) && expiry(connection.apiKey) <= Date.now());
  const mask = (value) => !value ? "Not available" : value.length < 28 ? "••••••••" : `${value.slice(0, 14)}…${value.slice(-10)}`;
  const normalizeLatex = (value) => {
    let latex = String(value ?? "").trim();
    for (const [left, right] of [["$$", "$$"], ["$", "$"], ["\\[", "\\]"], ["\\(", "\\)"]]) {
      if (latex.startsWith(left) && latex.endsWith(right) && latex.length >= left.length + right.length) { latex = latex.slice(left.length, -right.length); break; }
    }
    return latex.trim();
  };
  const math = (value) => {
    const latex = normalizeLatex(value);
    if (!latex) return "";
    if (!window.katex) return `<code class="formula-raw">${esc(value)}</code>`;
    try { return window.katex.renderToString(latex, { displayMode: true, throwOnError: false, strict: "ignore", trust: false }); }
    catch (error) { return `<code class="formula-raw">${esc(value)}</code>`; }
  };
  const typeset = (root = document) => {
    if (!window.renderMathInElement || !root) return;
    try {
      window.renderMathInElement(root, {
        delimiters: [{ left: "$$", right: "$$", display: true }, { left: "\\[", right: "\\]", display: true }, { left: "\\(", right: "\\)", display: false }, { left: "$", right: "$", display: false }],
        ignoredTags: ["script", "noscript", "style", "textarea", "pre", "code", "option"], throwOnError: false, strict: "ignore", trust: false
      });
    } catch (error) { return; }
  };
  const topicTotal = (topic) => ["formulae_available", "examples_available", "questions_available", "sources_available"].reduce((sum, key) => sum + (Number(topic[key]) || 0), 0);
  const selected = (value, current) => value === current ? " selected" : "";
  const blankState = () => ({ bookmarks: [], progress: Object.create(null), history: [], lastTopic: null });

  function normalizeProgress(value) {
    if (!value || typeof value !== "object" || Array.isArray(value)) return {};
    const result = Object.create(null);
    Object.entries(value).forEach(([key, entry]) => {
      if (!entry || typeof entry !== "object") return;
      result[String(key)] = { attempted: Math.max(0, Number(entry.attempted) || 0), correct: Math.max(0, Number(entry.correct) || 0), lastAttempt: typeof entry.lastAttempt === "string" ? entry.lastAttempt : null };
    });
    return result;
  }

  function loadState() {
    const fallback = blankState();
    try {
      const raw = sessionStorage.getItem(KEYS.state);
      if (!raw) return fallback;
      const data = JSON.parse(raw);
      return {
        bookmarks: Array.isArray(data.bookmarks) ? [...new Set(data.bookmarks.filter((item) => typeof item === "string"))] : [],
        progress: normalizeProgress(data.progress),
        history: Array.isArray(data.history) ? data.history.filter((item) => item && typeof item === "object").slice(0, 40) : [],
        lastTopic: data.lastTopic && typeof data.lastTopic.id === "string" ? data.lastTopic : null
      };
    } catch (error) { return fallback; }
  }

  function saveState() {
    try { sessionStorage.setItem(KEYS.state, JSON.stringify(state)); }
    catch (error) { toast("Session progress could not be saved.", "error"); }
  }

  function isBookmarked(topicId) { return state.bookmarks.includes(topicId); }

  function toggleBookmark(topicId) {
    if (!topicId) return false;
    const saved = isBookmarked(topicId);
    state.bookmarks = saved ? state.bookmarks.filter((item) => item !== topicId) : [topicId, ...state.bookmarks];
    saveState();
    return !saved;
  }

  function recordAnswer(topicId, correct) {
    const key = topicId || "unknown", entry = state.progress[key] || { attempted: 0, correct: 0, lastAttempt: null };
    entry.attempted += 1;
    if (correct) entry.correct += 1;
    entry.lastAttempt = new Date().toISOString();
    state.progress[key] = entry;
    saveState();
  }

  function recordQuiz(session) {
    if (!session || session.historyRecorded) return;
    session.historyRecorded = true;
    state.history = [{ label: session.config.modeLabel || "Practice", topicId: session.config.topicId || "", topicName: session.config.topicName || "", attempted: session.attempted, correct: session.score, total: session.questions.length, completedAt: new Date().toISOString() }, ...state.history].slice(0, 40);
    saveState();
  }

  function resetProgress() { state.progress = Object.create(null); state.history = []; saveState(); }
  function resetLearning() { state = blankState(); saveState(); }

  function clearLegacy() {
    try {
      sessionStorage.removeItem(KEYS.legacy);
      localStorage.removeItem(KEYS.legacy);
      localStorage.removeItem(KEYS.api);
    } catch (error) { return; }
  }

  function loadConnection() {
    try {
      const raw = sessionStorage.getItem(KEYS.api);
      if (!raw) return null;
      const data = JSON.parse(raw);
      if (!data || typeof data.apiKey !== "string" || !data.apiKey.trim()) return null;
      const connection = { apiKey: data.apiKey.trim(), savedAt: typeof data.savedAt === "string" ? data.savedAt : new Date().toISOString() };
      if (!expired(connection)) return connection;
      clearConnection();
      return null;
    } catch (error) { return null; }
  }

  function saveConnection(connection) {
    try { sessionStorage.setItem(KEYS.api, JSON.stringify(connection)); return true; }
    catch (error) { return false; }
  }

  function clearConnection() {
    try { sessionStorage.removeItem(KEYS.api); }
    catch (error) { return; }
  }

  const app = { connection: null, health: null, healthAt: 0, cache: new Map(), inflight: new Map(), topics: [], online: false };
  const ui = { search: "", branch: "", difficulty: "", sort: "name", practice: { topicId: "", difficulty: "", type: "", limit: "10", stage: "idle" }, formulaTopicId: "" };
  let state = loadState(), currentRoute = null, renderSequence = 0, quizSession = null, modalResolve = null, toastSequence = 0, randomRequest = 0;

  class ApiError extends Error {
    constructor(message, options = {}) {
      super(message);
      this.name = "ApiError";
      this.status = Number(options.status) || 0;
      this.detail = options.detail || message;
      this.data = options.data || null;
    }
  }

  function apiStatus(kind, text) {
    const pill = $("#api-status");
    const label = $("#api-status-text");
    const gateStatus = $("#auth-status");
    if (kind === "online") app.online = true;
    if (kind === "offline") app.online = false;
    [gateStatus, pill].forEach((node) => {
      if (!node) return;
      node.classList.remove("is-online", "is-offline", "is-checking");
      if (kind) node.classList.add(`is-${kind}`);
    });
    if (gateStatus) gateStatus.textContent = text;
    if (label) label.textContent = text;
    if (pill) pill.title = text;
  }

  function loadingDone() {
    $("#loading-screen")?.classList.add("is-hidden");
  }

  function sessionUI() {
    const connection = app.connection;
    const card = $(".session-card");
    const status = $("#session-state");
    const expiryNode = $("#session-expiry");
    const keyNode = $("#session-key");
    if (status) status.textContent = connection ? "MathAPI connected" : "Not connected";
    if (card) card.classList.toggle("is-connected", Boolean(connection));
    if (expiryNode) {
      if (!connection) expiryNode.textContent = "API key required";
      else if (expired(connection)) expiryNode.textContent = "Key expired";
      else expiryNode.textContent = expiry(connection.apiKey) ? `Expires ${formatDate(expiry(connection.apiKey))}` : "Session only";
    }
    if (keyNode) keyNode.textContent = connection ? mask(connection.apiKey) : "Not connected";
  }

  function apiError(data, status) {
    const detail = data?.detail;
    if (Array.isArray(detail)) return detail.map((item) => item?.msg || String(item)).join("; ");
    if (typeof detail === "string" && detail.trim()) return detail;
    if (typeof data?.message === "string" && data.message.trim()) return data.message;
    if (status === 401) return "Your API key was rejected or has expired.";
    if (status === 404) return "The requested item was not found.";
    if (status === 429) return "The hourly MathAPI rate limit was reached.";
    if (status === 503) return "MathAPI could not reach its database.";
    return status ? `MathAPI returned an error (${status}).` : `MathAPI is not reachable at ${API_BASE}.`;
  }

  async function request(path, options = {}) {
    const { method = "GET", body, auth = true, apiKey, timeout = 25000, handleAuth = true } = options;
    const controller = new AbortController(), timer = window.setTimeout(() => controller.abort(), timeout), headers = { Accept: "application/json" };
    if (body !== undefined) headers["Content-Type"] = "application/json";
    const key = apiKey || (auth ? app.connection?.apiKey : "");
    if (key) headers["X-API-Key"] = key;
    let response;
    try {
      response = await fetch(`${API_BASE}${path}`, { method, headers, body: body === undefined ? undefined : JSON.stringify(body), signal: controller.signal });
    } catch (error) {
      if (error?.name === "AbortError") { apiStatus("offline", "API timed out"); throw new ApiError("MathAPI did not respond in time.", { status: 0 }); }
      apiStatus("offline", "API offline");
      throw new ApiError(`MathAPI is not reachable at ${API_BASE}.`, { status: 0 });
    } finally { window.clearTimeout(timer); }
    const raw = await response.text();
    let data = null;
    if (raw) {
      try { data = JSON.parse(raw); }
      catch (error) { if (response.ok) throw new ApiError("MathAPI returned an unreadable response.", { status: response.status }); }
    }
    if (!response.ok) {
      const detail = apiError(data, response.status);
      if (response.status === 401 && auth) {
        if (handleAuth) handleAuthFailure(detail);
        throw new ApiError(detail, { status: 401, detail, data });
      }
      if (response.status === 429) apiStatus("checking", "Rate limited");
      else if (response.status === 503) apiStatus("offline", "Database offline");
      else if (response.status >= 500) apiStatus("offline", "API unavailable");
      throw new ApiError(detail, { status: response.status, detail, data });
    }
    apiStatus("online", "API online");
    return data;
  }

  async function health() {
    const controller = new AbortController(), timer = window.setTimeout(() => controller.abort(), 6000);
    apiStatus("checking", "Checking API");
    try {
      const response = await fetch(`${API_BASE}/`, { headers: { Accept: "application/json" }, signal: controller.signal });
      if (!response.ok) throw new ApiError(`Health check failed (${response.status}).`, { status: response.status });
      app.health = await response.json();
      app.healthAt = Date.now();
      apiStatus("online", "API online");
      return app.health;
    } catch (error) {
      app.health = null;
      app.healthAt = Date.now();
      apiStatus("offline", "API offline");
      if (error instanceof ApiError) throw error;
      throw new ApiError(`MathAPI is not reachable at ${API_BASE}.`, { status: 0 });
    } finally { window.clearTimeout(timer); }
  }

  function setApp(visible) {
    const shell = $("#app-shell");
    if (!shell) return;
    shell.hidden = !visible;
    shell.inert = !visible;
  }

  function gateSync() {
    const status = $("#auth-status");
    if (!status) return;
    const kind = !app.healthAt ? "checking" : app.online ? "online" : "offline";
    status.textContent = !app.healthAt ? "Checking API…" : app.online ? "API online" : "API offline";
    status.classList.remove("is-online", "is-offline", "is-checking");
    status.classList.add(`is-${kind}`);
  }

  function gateError(message) {
    const error = $("#auth-error");
    if (!error) return;
    error.textContent = message || "";
    error.hidden = !message;
  }

  function gateBusy(busy) {
    const form = $("#api-key-form"), input = $("#api-key-input"), submit = $("#auth-submit"), toggle = $('[data-action="toggle-key-visibility"]'), cancel = $("#auth-cancel");
    if (form) form.setAttribute("aria-busy", String(busy));
    if (input) input.disabled = busy;
    if (submit) { submit.disabled = busy; submit.textContent = busy ? (app.connection ? "Updating key…" : "Connecting…") : (app.connection ? "Update API key" : "Connect to MathAPI"); }
    if (toggle) toggle.disabled = busy;
    if (cancel) cancel.disabled = busy;
  }

  function showGate(message = "") {
    const gate = $("#auth-gate");
    if (!gate) return;
    const replacing = Boolean(app.connection), input = $("#api-key-input"), toggle = $('[data-action="toggle-key-visibility"]'), title = $("#auth-title"), copy = $("#auth-copy-text"), cancel = $("#auth-cancel");
    closeSidebar();
    gate.hidden = false;
    document.body.classList.add("is-gated");
    setApp(replacing);
    const shell = $("#app-shell");
    if (shell) shell.inert = true;
    if (title) title.textContent = replacing ? "Replace your MathAPI key." : "Bring your own MathAPI key.";
    if (copy) copy.textContent = replacing ? "Paste a new key to replace this tab's connection. The new key is checked before the old one is replaced." : "Paste your key to load topics, examples, formulae, and quizzes. It stays in this tab only.";
    if (cancel) cancel.hidden = !replacing;
    if (input) { input.value = ""; input.type = "password"; input.disabled = false; }
    if (toggle) { toggle.textContent = "Show"; toggle.setAttribute("aria-pressed", "false"); toggle.setAttribute("aria-label", "Show API key"); toggle.disabled = false; }
    gateError(message);
    gateBusy(false);
    gateSync();
    if (!replacing) document.title = "Connect API key · MathLabs";
    window.setTimeout(() => { if (!gate.hidden) input?.focus(); }, 30);
  }

  function hideGate() {
    const gate = $("#auth-gate");
    if (!gate) return;
    gate.hidden = true;
    document.body.classList.remove("is-gated");
    const input = $("#api-key-input");
    if (input) { input.value = ""; input.type = "password"; }
    gateError("");
    gateBusy(false);
    setApp(Boolean(app.connection));
  }

  function toggleKeyVisibility() {
    const input = $("#api-key-input"), toggle = $('[data-action="toggle-key-visibility"]');
    if (!input || !toggle) return;
    const reveal = input.type === "password";
    input.type = reveal ? "text" : "password";
    toggle.textContent = reveal ? "Hide" : "Show";
    toggle.setAttribute("aria-pressed", String(reveal));
    toggle.setAttribute("aria-label", reveal ? "Hide API key" : "Show API key");
    input.focus();
  }

  function validationMessage(error) {
    if (error instanceof ApiError) {
      if (error.status === 401) return /expired/i.test(error.detail || "") ? "That API key has expired. Create a new key, then paste it here." : "That API key was rejected. Check the key and try again.";
      if (error.status === 429) return "MathAPI's hourly rate limit is currently active. Wait for it to reset, then try again.";
      if (error.status === 503) return "MathAPI could not reach its database. Try again shortly.";
      if (error.status === 0) return error.message;
    }
    return error?.message || "That API key could not be verified.";
  }

  async function validateKey(apiKey) {
    const data = await request("/api/v1/topics", { auth: false, apiKey, handleAuth: false, timeout: 15000 });
    return { ...(data && typeof data === "object" ? data : {}), topics: Array.isArray(data?.topics) ? data.topics : [] };
  }

  function clearApi() {
    renderSequence += 1;
    app.topics = [];
    app.cache.clear();
    app.inflight.clear();
    quizSession = null;
    const view = $("#view");
    if (view) view.innerHTML = "";
  }

  function handleAuthFailure(message) {
    if (modalResolve) closeModal(false);
    const isExpired = /expired/i.test(message || "");
    app.connection = null;
    clearConnection();
    clearApi();
    sessionUI();
    setApp(false);
    showGate(isExpired ? "Your API key has expired. Create a new key, then paste it here." : "Your API key was rejected. Check the key and try again.");
  }

  async function connectWithKey(event) {
    if (event) event.preventDefault();
    const input = $("#api-key-input"), apiKey = input?.value.trim() || "";
    if (!apiKey) { gateError("Paste your MathAPI key to continue."); input?.focus(); return; }
    const replacing = Boolean(app.connection);
    gateBusy(true);
    gateError("");
    try {
      const data = await validateKey(apiKey), connection = { apiKey, savedAt: new Date().toISOString() }, stored = saveConnection(connection);
      app.connection = connection;
      app.cache.clear();
      app.inflight.clear();
      app.topics = data.topics;
      app.cache.set("/api/v1/topics", { value: data, expires: Date.now() + TTL.topics });
      sessionUI();
      hideGate();
      setApp(true);
      toast(replacing ? "API key updated." : "Connected to MathAPI.", "success");
      if (!stored) toast("This browser blocked sessionStorage. The key will be lost when this page reloads.", "error");
      await renderRoute();
    } catch (error) {
      gateBusy(false);
      gateError(validationMessage(error));
      input?.focus();
    }
  }

  async function disconnect() {
    const confirmed = await openModal({ title: "Disconnect MathAPI?", message: "This removes the API key from this tab and clears cached API data. Bookmarks and learning progress stay intact.", confirmLabel: "Disconnect", danger: true });
    if (!confirmed) return;
    app.connection = null;
    clearConnection();
    clearApi();
    sessionUI();
    setApp(false);
    toast("API key disconnected.", "success");
    showGate();
  }

  async function testGate(element) {
    if (element) element.disabled = true;
    try { await health(); gateError(""); toast("MathAPI is reachable.", "success"); }
    catch (error) { gateError(error.message || "MathAPI is not reachable."); }
    finally { if (element) element.disabled = false; }
  }

  async function fetchData(path, params = {}, cacheType = null) {
    const query = new URLSearchParams();
    Object.entries(params).forEach(([key, value]) => { if (value !== undefined && value !== null && value !== "") query.set(key, String(value)); });
    const suffix = query.toString() ? `?${query.toString()}` : "", key = `${path}${suffix}`, ttl = cacheType ? TTL[cacheType] || 0 : 0;
    if (ttl) { const cached = app.cache.get(key); if (cached && cached.expires > Date.now()) return cached.value; }
    if (app.inflight.has(key)) return app.inflight.get(key);
    const promise = request(key).then((data) => { if (ttl) app.cache.set(key, { value: data, expires: Date.now() + ttl }); return data; }).finally(() => app.inflight.delete(key));
    app.inflight.set(key, promise);
    return promise;
  }

  async function getTopics() {
    const data = await fetchData("/api/v1/topics", {}, "topics");
    app.topics = Array.isArray(data?.topics) ? data.topics : [];
    return { ...(data && typeof data === "object" ? data : {}), topics: app.topics };
  }

  function topicName(topicId) { return app.topics.find((topic) => topic.topic_id === topicId)?.topic_name || topicId || "Mathematics"; }

  const notFound = (error) => error instanceof ApiError && error.status === 404;
  const clearCache = () => app.cache.clear();

  function toast(message, type = "info") {
    const stack = $("#toast-stack");
    if (!stack) return;
    const iconName = type === "success" ? "check-circle" : type === "error" ? "alert" : "sparkles", element = document.createElement("div");
    element.className = `toast${type === "success" ? " is-success" : type === "error" ? " is-error" : ""}`;
    element.id = `toast-${++toastSequence}`;
    element.innerHTML = `${icon(iconName)}<span>${esc(message)}</span>`;
    element.addEventListener("click", () => element.remove());
    stack.appendChild(element);
    while (stack.children.length > 4) stack.firstElementChild.remove();
    window.setTimeout(() => element.remove(), type === "error" ? 6500 : 4200);
  }

  function openModal(options = {}) {
    const root = $("#modal-root");
    if (!root) return Promise.resolve(false);
    if (modalResolve) { const previous = modalResolve; modalResolve = null; previous(false); }
    root.innerHTML = `<div class="modal" role="dialog" aria-modal="true" aria-labelledby="modal-title" aria-describedby="modal-copy"><h3 id="modal-title">${esc(options.title || "Are you sure?")}</h3><p id="modal-copy">${esc(options.message || "")}</p><div class="modal-actions"><button class="btn btn-ghost" type="button" data-modal-cancel>${esc(options.cancelLabel || "Cancel")}</button><button class="btn ${options.danger ? "btn-danger" : "btn-primary"}" type="button" data-modal-confirm>${esc(options.confirmLabel || "Confirm")}</button></div></div>`;
    root.classList.add("is-open");
    document.body.style.overflow = "hidden";
    $("[data-modal-cancel]", root)?.focus();
    return new Promise((resolve) => { modalResolve = resolve; });
  }

  function closeModal(value) {
    const root = $("#modal-root");
    if (!root) return;
    root.classList.remove("is-open");
    root.innerHTML = "";
    document.body.style.overflow = $("#sidebar")?.classList.contains("is-open") ? "hidden" : "";
    const resolve = modalResolve;
    modalResolve = null;
    if (resolve) resolve(Boolean(value));
  }

  function setSidebar(open) {
    const sidebar = $("#sidebar"), button = $("#menu-toggle");
    sidebar?.classList.toggle("is-open", open);
    button?.setAttribute("aria-expanded", String(open));
    document.body.style.overflow = open || modalResolve ? "hidden" : "";
  }

  const closeSidebar = () => setSidebar(false);
  const onResize = () => { if (window.innerWidth > 980 && $("#sidebar")?.classList.contains("is-open")) closeSidebar(); };

  function chrome(route, override = {}) {
    const [eyebrow, title] = ROUTES[route.name] || ROUTES.dashboard, heading = override.title || title, kicker = override.eyebrow || eyebrow;
    if ($("#page-title")) $("#page-title").textContent = heading;
    if ($("#page-eyebrow")) $("#page-eyebrow").textContent = kicker;
    document.title = `${heading} · MathLabs`;
    const active = route.name === "topic" ? "topics" : route.name;
    $$(".nav-link[data-route]").forEach((link) => {
      const match = link.dataset.route === active;
      link.classList.toggle("is-active", match);
      if (match) link.setAttribute("aria-current", "page");
      else link.removeAttribute("aria-current");
    });
  }

  function head(options = {}) {
    return `<section class="page-head"><div class="page-head-copy"><span class="eyebrow">${esc(options.eyebrow || "MathLabs")}</span><h2>${esc(options.title || "")}</h2>${options.text ? `<p class="lede">${esc(options.text)}</p>` : ""}</div>${options.actions ? `<div class="page-actions">${options.actions}</div>` : ""}</section>`;
  }

  const skeleton = () => `<div class="page-loading"><div class="skeleton skeleton-line skeleton-short"></div><div class="skeleton skeleton-title"></div><div class="skeleton skeleton-line"></div><div class="skeleton-grid"><div class="skeleton-card"><div class="skeleton skeleton-title"></div><div class="skeleton skeleton-line"></div></div><div class="skeleton-card"><div class="skeleton skeleton-title"></div><div class="skeleton skeleton-line"></div></div><div class="skeleton-card"><div class="skeleton skeleton-title"></div><div class="skeleton skeleton-line"></div></div></div></div>`;

  function emptyState(options = {}) {
    return `<div class="empty-state"><span class="empty-icon">${icon(options.iconName || "sparkles")}</span><h3>${esc(options.title || "Nothing here yet")}</h3><p>${esc(options.text || "")}</p>${options.action || ""}</div>`;
  }

  function errorState(error, action = "retry-route", label = "Try again") {
    const status = error instanceof ApiError ? error.status : 0, message = error instanceof Error ? error.message : String(error || "Something went wrong."), extra = status === 0 ? `Check that MathAPI is reachable at ${API_BASE}, then try again.` : status === 429 ? "MathAPI allows 100 authenticated requests per hour and 300 per IP. Try again later." : "";
    return `<div class="error-state"><span class="error-icon">${icon("alert")}</span><h3>This section could not load</h3><p>${esc(message)}</p>${extra ? `<p class="muted">${esc(extra)}</p>` : ""}${status ? `<code class="error-code">MathAPI status ${status}</code>` : ""}<button class="btn btn-primary" type="button" data-action="${esc(action)}">${esc(label)}</button></div>`;
  }

  function bookmarkButton(topicId) {
    const saved = isBookmarked(topicId);
    return `<button class="bookmark-btn${saved ? " is-saved" : ""}" type="button" data-action="toggle-bookmark" data-topic-id="${esc(topicId)}" aria-label="${saved ? "Remove bookmark" : "Save topic"}" aria-pressed="${saved}">${icon("bookmark")}</button>`;
  }

  function syncBookmarks(topicId) {
    const saved = isBookmarked(topicId);
    $$('[data-action="toggle-bookmark"]').forEach((button) => {
      if (button.dataset.topicId !== topicId) return;
      button.classList.toggle("is-saved", saved);
      button.setAttribute("aria-pressed", String(saved));
      button.setAttribute("aria-label", saved ? "Remove bookmark" : "Save topic");
    });
  }

  function resourceRow(topic) {
    return `<div class="resource-row"><span class="resource">${icon("file-text")}${Number(topic.examples_available) || 0}</span><span class="resource">${icon("target")}${Number(topic.questions_available) || 0}</span><span class="resource">${icon("formula")}${Number(topic.formulae_available) || 0}</span><span class="resource">${icon("link")}${Number(topic.sources_available) || 0}</span></div>`;
  }

  function topicCard(topic) {
    const subtopics = Array.isArray(topic.sub_topics) ? topic.sub_topics.slice(0, 3) : [], href = `#/topic/${encodeURIComponent(topic.topic_id)}/explanation`;
    const summary = subtopics.length ? subtopics.join(" · ") : (topic.prerequisites || []).length ? `Prerequisites: ${topic.prerequisites.join(", ")}` : "A focused topic in the MathAPI catalog.";
    return `<article class="topic-card" data-topic-id="${esc(topic.topic_id)}"><div class="topic-card-top"><h3 class="topic-title"><a href="${href}">${esc(topic.topic_name)}</a></h3>${bookmarkButton(topic.topic_id)}</div><p class="topic-id">${esc(topic.topic_id)}</p><p>${esc(summary)}</p><div class="chip-row">${chips(topic.branch)}${diffChip(topic.difficulty)}</div><div class="topic-card-footer">${resourceRow(topic)}<a class="btn btn-soft btn-sm" href="${href}">Open ${icon("arrow-right")}</a></div></article>`;
  }

  function formulaCard(formula) {
    const raw = normalizeLatex(formula?.code);
    return `<article class="formula-card"><div class="formula-card-head"><h4>${esc(formula?.title || "Formula")}</h4><button class="btn btn-ghost btn-sm" type="button" data-action="copy-formula">${icon("copy")} Copy</button></div><div class="formula">${math(formula?.code)}</div><span data-latex hidden>${esc(raw)}</span></article>`;
  }

  function sourceCard(source) {
    return `<article class="source-card"><span class="chip chip-orange">${esc(source?.type || "Resource")}</span><h4>${esc(source?.title || "Learning source")}</h4><p>${esc(source?.link || "")}</p>${external(source?.link, "Open source", "source-link")}</article>`;
  }

  const detail = (title, body) => `<section class="detail-section"><h3>${esc(title)}</h3>${body}</section>`;
  const statCard = (iconName, value, label) => `<article class="stat-card"><span class="stat-icon">${icon(iconName)}</span><div><span class="stat-value">${esc(value)}</span><span class="stat-label">${esc(label)}</span></div></article>`;

  function filteredTopics() {
    const query = ui.search.trim().toLowerCase(), order = { Beginner: 0, Intermediate: 1, Advanced: 2 };
    return app.topics.filter((topic) => {
      if (ui.branch && !(topic.branch || []).includes(ui.branch)) return false;
      if (ui.difficulty && topic.difficulty !== ui.difficulty) return false;
      if (!query) return true;
      return [topic.topic_id, topic.topic_name, topic.difficulty, ...(topic.branch || []), ...(topic.sub_topics || []), ...(topic.prerequisites || [])].join(" ").toLowerCase().includes(query);
    }).sort((left, right) => ui.sort === "resources" ? topicTotal(right) - topicTotal(left) : ui.sort === "difficulty" ? (order[left.difficulty] ?? 9) - (order[right.difficulty] ?? 9) : left.topic_name.localeCompare(right.topic_name));
  }

  function topicResults() {
    const topics = filteredTopics();
    return topics.length ? `<div class="topic-grid">${topics.map(topicCard).join("")}</div>` : emptyState({ title: "No topics match those filters", text: "Try a broader search or clear the branch and difficulty filters.", iconName: "search", action: '<button class="btn btn-secondary" type="button" data-action="clear-topic-filters">Clear filters</button>' });
  }

  function refreshTopics() {
    const results = $("#topic-results"), count = $("#topic-result-count");
    if (!results) return;
    const topics = filteredTopics();
    results.innerHTML = topicResults();
    if (count) count.textContent = `${topics.length} of ${app.topics.length} topics`;
    paint(results);
    typeset(results);
  }

  async function viewDashboard(route, sequence) {
    const data = await getTopics();
    if (sequence !== renderSequence) return null;
    const topics = data.topics || [];
    if (!topics.length) return { html: head({ eyebrow: "Workspace", title: "Your mathematics workspace", text: "No topics were returned by MathAPI." }) + emptyState({ title: "The catalog is empty", text: "Add topic data to the MathAPI database, then refresh.", iconName: "book-open" }), title: "Dashboard", eyebrow: "Workspace" };
    const branchCounts = new Map(BRANCHES.map((branch) => [branch, 0]));
    topics.forEach((topic) => (topic.branch || []).forEach((branch) => branchCounts.set(branch, (branchCounts.get(branch) || 0) + 1)));
    const resources = topics.reduce((sum, topic) => sum + topicTotal(topic), 0), questions = topics.reduce((sum, topic) => sum + (Number(topic.questions_available) || 0), 0);
    const last = state.lastTopic && topics.find((topic) => topic.topic_id === state.lastTopic.id), saved = state.bookmarks.map((id) => topics.find((topic) => topic.topic_id === id)).filter(Boolean).slice(0, 3);
    const continueMarkup = last ? `<div class="continue-card"><div><span class="eyebrow">Last opened</span><h3>${esc(last.topic_name)}</h3><p>${esc(last.difficulty)} · ${esc((last.branch || [])[0] || "Mathematics")} · ${topicTotal(last)} learning assets</p></div><a class="btn btn-primary btn-sm" href="#/topic/${encodeURIComponent(last.topic_id)}/${safeTab(state.lastTopic.tab)}">Continue ${icon("arrow-right")}</a></div>` : `<div class="continue-card"><div><span class="eyebrow">First step</span><h3>Pick a topic to begin</h3><p>Browse the catalog, then follow explanations, examples, and practice questions.</p></div><a class="btn btn-primary btn-sm" href="#/topics">Explore topics ${icon("arrow-right")}</a></div>`;
    const savedMarkup = saved.length ? `<div class="topic-progress-list">${saved.map((topic) => `<div class="progress-row"><div><strong>${esc(topic.topic_name)}</strong><br><span>${esc((topic.branch || []).join(", ") || "Mathematics")}</span></div><a class="btn btn-ghost btn-sm" href="#/topic/${encodeURIComponent(topic.topic_id)}/explanation">Open</a></div>`).join("")}</div>` : '<p class="muted">Save topics with the bookmark button to keep a shortlist here.</p>';
    return {
      html: `${head({ eyebrow: "Workspace", title: "Your mathematics workspace", text: "Explore the MathAPI catalog, work through examples, and check your understanding with guided practice.", actions: `<a class="btn btn-primary" href="#/topics">${icon("book-open")} Explore topics</a><a class="btn btn-secondary" href="#/practice">${icon("target")} Practice</a>` })}<div class="stats-grid">${statCard("book", topics.length, "Topics")}${statCard("layers", [...branchCounts.values()].filter(Boolean).length, "Branches")}${statCard("target", questions, "Questions")}${statCard("file-text", resources, "Learning assets")}</div><section class="section"><div class="dashboard-grid"><article class="panel daily-card"><span class="daily-date">${icon("calendar")} Daily challenge</span><h3>Three problems. One shared challenge.</h3><p>Beginner, intermediate, and advanced questions selected for today. Compare your reasoning with the solution sources when you are ready.</p><a class="btn btn-primary" href="#/daily">${icon("sparkles")} Open daily challenge</a></article><article class="panel"><div class="panel-head"><div><h3 class="panel-title">Continue learning</h3><p class="panel-caption">Your session picks up where you left it.</p></div></div>${continueMarkup}</article></div></section><section class="section"><div class="section-head"><div><h3 class="section-title">Explore by branch</h3><p class="section-subtitle">Move from foundations to specialist territory.</p></div><a class="section-link" href="#/topics">All topics ${icon("arrow-right")}</a></div><div class="branch-grid">${BRANCHES.map((branch) => `<a class="branch-card" href="#/topics?branch=${encodeURIComponent(branch)}"><strong>${esc(branch)}</strong><span>${branchCounts.get(branch) || 0} topics</span></a>`).join("")}</div></section><section class="section"><div class="section-head"><div><h3 class="section-title">Your bookmarks</h3><p class="section-subtitle">A short list of topics worth returning to.</p></div><a class="section-link" href="#/saved">Saved &amp; progress ${icon("arrow-right")}</a></div>${savedMarkup}</section>`,
      title: "Dashboard",
      eyebrow: "Workspace"
    };
  }

  async function viewTopics(route, sequence) {
    const data = await getTopics();
    if (sequence !== renderSequence) return null;
    const branch = route.query.get("branch");
    ui.branch = branch && BRANCHES.includes(branch) ? branch : "";
    return {
      html: `
        ${head({ eyebrow: "Library", title: "The whole map, minus the noise.", text: "Search by topic, branch, or prerequisite. Open a topic studio to read, work through examples, and practice.", actions: `<a class="btn btn-secondary" href="#/practice">${icon("target")} Practice Arena</a>` })}
        <div class="filter-bar">
          <label class="field field-grow"><span class="field-label">Search topics</span><span class="search-field"><span class="search-icon">${icon("search")}</span><input class="input" id="topic-search" type="search" value="${esc(ui.search)}" placeholder="Try algebra, proof, circle…" autocomplete="off"></span></label>
          <label class="field"><span class="field-label">Branch</span><select class="select" id="topic-branch"><option value="">All branches</option>${BRANCHES.map((item) => `<option value="${esc(item)}"${selected(item, ui.branch)}>${esc(item)}</option>`).join("")}</select></label>
          <label class="field"><span class="field-label">Difficulty</span><select class="select" id="topic-difficulty"><option value="">All levels</option>${LEVELS.map((item) => `<option value="${esc(item)}"${selected(item, ui.difficulty)}>${esc(item)}</option>`).join("")}</select></label>
          <label class="field"><span class="field-label">Sort</span><select class="select" id="topic-sort"><option value="name"${selected("name", ui.sort)}>Name A–Z</option><option value="resources"${selected("resources", ui.sort)}>Most resources</option><option value="difficulty"${selected("difficulty", ui.sort)}>Easiest first</option></select></label>
          <button class="btn btn-ghost" type="button" data-action="clear-topic-filters">${icon("x")} Clear</button>
        </div>
        <div class="section-head"><p class="result-count" id="topic-result-count">${filteredTopics().length} of ${data.topics.length} topics</p></div>
        <div id="topic-results">${topicResults()}</div>`,
      title: "Explore Topics",
      eyebrow: "Library"
    };
  }

  async function viewTopic(route, sequence) {
    const data = await getTopics();
    if (sequence !== renderSequence) return null;
    const topic = data.topics.find((item) => item.topic_id === route.id);
    if (!topic) throw new ApiError("That topic is not available in the MathAPI catalog.", { status: 404 });
    const tab = safeTab(route.tab);
    state.lastTopic = { id: topic.topic_id, name: topic.topic_name, tab };
    saveState();
    const href = (nextTab) => `#/topic/${encodeURIComponent(topic.topic_id)}/${nextTab}`;
    return {
      html: `<section class="topic-hero"><nav class="breadcrumbs" aria-label="Breadcrumb"><a href="#/topics">Topics</a>${icon("chevron-right")}<span>${esc(topic.topic_name)}</span></nav><div class="topic-hero-main"><div><span class="eyebrow">${esc((topic.branch || [])[0] || "Mathematics")}</span><h2>${esc(topic.topic_name)}</h2><div class="topic-meta">${diffChip(topic.difficulty)}${chips(topic.branch)}</div></div>${bookmarkButton(topic.topic_id)}</div><div class="topic-stats"><div class="topic-stat"><strong>${Number(topic.examples_available) || 0}</strong><span>Worked examples</span></div><div class="topic-stat"><strong>${Number(topic.questions_available) || 0}</strong><span>Practice questions</span></div><div class="topic-stat"><strong>${Number(topic.formulae_available) || 0}</strong><span>Formulae</span></div><div class="topic-stat"><strong>${Number(topic.sources_available) || 0}</strong><span>Learning sources</span></div></div><div class="topic-hero-actions"><a class="btn btn-primary" href="${href("questions")}">${icon("target")} Practice questions</a><a class="btn btn-secondary" href="${href("formulae")}">${icon("formula")} Formula sheet</a><a class="btn btn-ghost" href="${href("sources")}">${icon("link")} Sources</a></div></section><nav class="tabs" aria-label="Topic sections">${TABS.map((item) => `<a class="tab${item === tab ? " is-active" : ""}" href="${href(item)}"${item === tab ? ' aria-current="page"' : ""}>${esc(item[0].toUpperCase() + item.slice(1))}</a>`).join("")}</nav><div id="topic-tab-content">${skeleton()}</div>`,
      title: topic.topic_name,
      eyebrow: (topic.branch || [])[0] || "Topic studio",
      after: () => loadTab(topic, tab, sequence)
    };
  }

  function topicRef(value) {
    const topic = app.topics.find((item) => item.topic_id === value || item.topic_name === value);
    return topic ? `<a class="chip chip-orange" href="#/topic/${encodeURIComponent(topic.topic_id)}/explanation">${esc(value)}</a>` : `<span class="chip">${esc(value)}</span>`;
  }

  function explanationMarkup(explanation, topic) {
    const sections = Array.isArray(explanation.explanation) ? explanation.explanation : [], applications = Array.isArray(explanation.applications) ? explanation.applications : [], prerequisites = Array.isArray(topic.prerequisites) ? topic.prerequisites : [], related = Array.isArray(topic.related_topics) ? topic.related_topics : [];
    return `${detail("Definition", `<div class="prose">${prose(explanation.definition) || '<p class="muted">No definition supplied.</p>'}</div>`)}${explanation.origin ? detail("Origin", `<div class="prose">${prose(explanation.origin)}</div>`) : ""}${applications.length ? detail("Real-world applications", `<ul class="application-list">${applications.map((item) => `<li>${esc(item)}</li>`).join("")}</ul>`) : ""}${sections.length ? detail("How it works", `<div class="explanation-list">${sections.map((section) => `<article class="explanation-block"><h4>${esc(section.title)}</h4><div class="prose">${prose(section.content)}</div></article>`).join("")}</div>`) : ""}${prerequisites.length || related.length ? `<div class="settings-grid">${prerequisites.length ? `<div class="info-card"><h3>Prerequisites</h3><p>Ideas worth knowing before this topic.</p><div class="chip-row">${prerequisites.map(topicRef).join("")}</div></div>` : ""}${related.length ? `<div class="info-card"><h3>Related topics</h3><p>Continue the thread into nearby ideas.</p><div class="chip-row">${related.map(topicRef).join("")}</div></div>` : ""}</div>` : ""}`;
  }

  function examplesMarkup(data) {
    const examples = Array.isArray(data?.examples) ? data.examples : [];
    return examples.length ? examples.map((example, index) => `<article class="example-card"><div class="example-top"><span class="example-index">Example ${index + 1}</span>${diffChip(example.difficulty)}</div><div class="example-question">${prose(example.question)}</div>${example.key_observation ? `<div class="observation"><strong>Key observation</strong>${esc(example.key_observation).replace(/\n/g, "<br>")}</div>` : ""}${(example.concept_used || []).length ? `<div class="chip-row">${chips(example.concept_used)}${chips(example.question_type)}</div>` : ""}${(example.formulae_used || []).length ? `<div class="formula-stack">${example.formulae_used.map(formulaCard).join("")}</div>` : ""}${(example.steps || []).length ? `<ol class="step-list">${example.steps.map((step) => `<li>${esc(step).replace(/\n/g, "<br>")}</li>`).join("")}</ol>` : ""}<div class="answer-box"><strong>Final answer</strong><div class="prose">${prose(example.answer)}</div>${example.interpretation ? `<div class="prose">${prose(example.interpretation)}</div>` : ""}</div></article>`).join("") : emptyState({ title: "No worked examples yet", text: "MathAPI has no examples for this topic right now.", iconName: "file-text" });
  }

  function formulaeMarkup(data) {
    const formulae = Array.isArray(data?.formulae) ? data.formulae : [];
    return formulae.length ? `<div class="formula-grid">${formulae.map(formulaCard).join("")}</div>` : emptyState({ title: "No formulae for this topic", text: "The formula sheet for this topic is still empty.", iconName: "formula" });
  }

  function sourcesMarkup(data) {
    const sources = Array.isArray(data?.sources) ? data.sources : [];
    return sources.length ? `<div class="source-grid">${sources.map(sourceCard).join("")}</div>` : emptyState({ title: "No learning sources yet", text: "MathAPI has no source links for this topic right now.", iconName: "link" });
  }

  async function loadTab(topic, tab, sequence) {
    const mount = $("#topic-tab-content");
    if (!mount) return;
    try {
      if (tab === "questions") {
        const data = await fetchData("/api/v1/questions", { topic_id: topic.topic_id, limit: 10 }, "content");
        if (sequence !== renderSequence) return;
        const questions = Array.isArray(data?.questions) ? data.questions : [];
        if (!questions.length) { mount.innerHTML = emptyState({ title: "No questions for this topic", text: "Try the Practice Arena with a different topic or difficulty.", iconName: "target", action: '<a class="btn btn-primary" href="#/practice">Open Practice Arena</a>' }); paint(mount); return; }
        mountQuiz(mount, newQuiz(questions, { mode: "topic", modeLabel: "Topic practice", kicker: `${topic.topic_name} · Practice`, topicId: topic.topic_id, topicName: topic.topic_name, returnTab: "questions" }));
        return;
      }
      const params = { topic_id: topic.topic_id };
      if (tab === "examples") params.limit = 12;
      const data = await fetchData(`/api/v1/${tab}`, params, tab === "explanation" ? "explanation" : "content");
      if (sequence !== renderSequence) return;
      mount.innerHTML = tab === "explanation" ? explanationMarkup(data?.explanation || {}, topic) : tab === "examples" ? examplesMarkup(data) : tab === "formulae" ? formulaeMarkup(data) : sourcesMarkup(data);
      paint(mount);
      typeset(mount);
    } catch (error) {
      if (sequence !== renderSequence) return;
      mount.innerHTML = notFound(error) ? emptyState({ title: "Nothing has been added here yet", text: "Try another tab or explore a different topic.", iconName: "layers" }) : errorState(error);
      paint(mount);
    }
  }

  function newQuiz(questions, config = {}) {
    const list = Array.isArray(questions) ? questions.filter((question) => question && typeof question.question === "string") : [];
    return { questions: list, index: 0, selected: null, revealed: false, showHint: false, score: 0, attempted: 0, completed: false, historyRecorded: false, config: { mode: "practice", kicker: "Practice", modeLabel: "Practice", topicId: "", topicName: "", ...config } };
  }

  function quizResultActions(session) {
    if (session.config.mode === "practice") return `<button class="btn btn-primary" type="button" data-action="practice-restart">${icon("rotate")} New practice set</button><a class="btn btn-secondary" href="#/topics">Explore topics</a>`;
    if (session.config.mode === "random") return `<button class="btn btn-primary" type="button" data-action="random-new">${icon("shuffle")} Another question</button><a class="btn btn-secondary" href="#/practice">Practice Arena</a>`;
    if (session.config.mode === "daily") return `<a class="btn btn-primary" href="#/random">${icon("shuffle")} Try a random question</a><button class="btn btn-secondary" type="button" data-action="retry-route">${icon("refresh")} Refresh challenge</button>`;
    const topicLink = session.config.topicId ? `#/topic/${encodeURIComponent(session.config.topicId)}/${safeTab(session.config.returnTab)}` : "#/practice";
    return `<a class="btn btn-primary" href="#/practice">${icon("target")} Practice Arena</a><a class="btn btn-secondary" href="${topicLink}">${icon("arrow-left")} Back to topic</a>`;
  }

  function quizResult(session) {
    const percent = session.attempted ? Math.round((session.score / session.attempted) * 100) : 0, heading = percent === 100 ? "Flawless work." : percent >= 80 ? "Strong finish." : percent >= 60 ? "Good progress." : "Keep building.";
    return `<div class="quiz-result"><div class="score-ring">${percent}%<span>accuracy</span></div><h3>${heading}</h3><p>You answered ${session.score} of ${session.attempted} attempted questions correctly.</p><div class="quiz-actions">${quizResultActions(session)}</div></div>`;
  }

  function quizQuestion(session) {
    const question = session.questions[session.index], options = question.options && typeof question.options === "object" ? Object.keys(question.options).sort() : [], types = Array.isArray(question.question_type) ? question.question_type : [], selectedKey = session.selected, sources = Array.isArray(question.solution_sources) ? question.solution_sources : [], percent = Math.round(((session.index + 1) / session.questions.length) * 100);
    const optionMarkup = options.map((key) => {
      const className = `option-btn${session.revealed ? (key === question.answer ? " is-correct" : key === selectedKey ? " is-wrong" : "") : key === selectedKey ? " is-selected" : ""}`;
      return `<button class="${className}" type="button" data-action="quiz-option" data-option="${esc(key)}" ${session.revealed ? "disabled" : ""} aria-pressed="${key === selectedKey}"><span class="option-letter">${esc(key)}</span><span class="option-text">${esc(question.options[key]).replace(/\n/g, "<br>")}</span></button>`;
    }).join("");
    const correctOption = question.options?.[question.answer], feedback = session.revealed ? `<div class="quiz-feedback ${selectedKey === question.answer ? "is-success" : "is-error"}"><strong>${selectedKey === question.answer ? "Correct." : "Not quite."}</strong><span>${selectedKey === question.answer ? "The selected option is correct." : `The correct answer is ${esc(question.answer)}${correctOption ? ` — ${esc(correctOption)}` : ""}.`}</span>${sources.length ? `<ul class="source-list">${sources.map((source) => `<li>${external(source.link, source.source || source.type || "Solution source")}</li>`).join("")}</ul>` : ""}</div>` : "";
    return `<div class="quiz-top"><span class="quiz-kicker">${esc(session.config.kicker)}</span><span class="quiz-counter">Question ${session.index + 1} of ${session.questions.length}</span></div><div class="progress-bar"><div class="progress-fill" style="width: ${percent}%"></div></div><div class="quiz-meta"><span class="chip chip-orange">${esc(topicName(question.topic_id || session.config.topicId))}</span>${diffChip(question.difficulty)}${chips(types)}${question.expected_time_limit ? `<span class="chip">${icon("clock")} ${esc(question.expected_time_limit)}</span>` : ""}</div><h3 class="quiz-question">${esc(question.question).replace(/\n/g, "<br>")}</h3><div class="options-grid">${optionMarkup}</div>${question.hint && !session.showHint ? `<div class="quiz-actions"><button class="btn btn-ghost btn-sm" type="button" data-action="quiz-hint">${icon("lightbulb")} Show hint</button></div>` : ""}${question.hint && session.showHint ? `<div class="observation"><strong>Hint</strong>${esc(question.hint).replace(/\n/g, "<br>")}</div>` : ""}${feedback}<div class="quiz-actions">${session.revealed ? `<button class="btn btn-primary" type="button" data-action="quiz-next">${session.index + 1 >= session.questions.length ? "See results" : "Next question"} ${icon("arrow-right")}</button>` : `<button class="btn btn-primary" type="button" data-action="quiz-check" ${session.selected ? "" : "disabled"}>Check answer ${icon("check")}</button>`}</div>`;
  }

  function quizInner(session) { return !session || !session.questions.length ? emptyState({ title: "No questions available", text: "This selection does not have any questions yet.", iconName: "target" }) : session.completed ? quizResult(session) : quizQuestion(session); }

  const quizShell = (session) => `<div class="quiz-shell" id="quiz-container">${quizInner(session)}</div>`;

  function mountQuiz(container, session) {
    if (!container) return;
    quizSession = session;
    container.innerHTML = quizShell(session);
    paint(container);
    typeset(container);
  }

  function updateQuiz(session) {
    const container = $("#quiz-container");
    if (!container || !session) return;
    container.innerHTML = quizInner(session);
    paint(container);
    typeset(container);
  }

  function finishQuiz(session) {
    recordQuiz(session);
    if (session.config.topicId && session.config.topicName) { state.lastTopic = { id: session.config.topicId, name: session.config.topicName, tab: safeTab(session.config.returnTab) }; saveState(); }
  }

  function quizAction(action, element) {
    if (!quizSession) return;
    const session = quizSession;
    if (action === "quiz-option" && !session.revealed && !session.completed) { session.selected = element.dataset.option || null; updateQuiz(session); return; }
    if (action === "quiz-hint" && !session.completed) { session.showHint = true; updateQuiz(session); return; }
    if (action === "quiz-check" && !session.revealed && !session.completed) {
      const question = session.questions[session.index];
      if (!question || !session.selected) return;
      session.revealed = true;
      session.attempted += 1;
      if (session.selected === question.answer) session.score += 1;
      recordAnswer(question.topic_id || session.config.topicId, session.selected === question.answer);
      updateQuiz(session);
      return;
    }
    if (action === "quiz-next" && session.revealed && !session.completed) {
      if (session.index + 1 >= session.questions.length) { session.completed = true; finishQuiz(session); }
      else { session.index += 1; session.selected = null; session.revealed = false; session.showHint = false; }
      updateQuiz(session);
    }
  }

  function practiceOptions(selectedId) {
    return app.topics.map((topic) => `<option value="${esc(topic.topic_id)}"${selected(topic.topic_id, selectedId)}>${esc(topic.topic_name)} · ${Number(topic.questions_available) || 0} questions</option>`).join("");
  }

  const practiceIntro = () => `<div class="panel"><div class="panel-head"><div><h3 class="panel-title">Build a practice set</h3><p class="panel-caption">Choose a topic and narrow the question pool before you begin.</p></div><span class="chip chip-orange">${icon("target")} Quiz mode</span></div><div class="info-list"><div class="info-row"><span class="info-label">Hints</span><span class="info-value plain">Available before checking an answer</span></div><div class="info-row"><span class="info-label">Difficulty</span><span class="info-value plain">Beginner, Intermediate, or Advanced</span></div><div class="info-row"><span class="info-label">Question types</span><span class="info-value plain">Conceptual, numerical, proof, word, case, HOTS</span></div></div></div>`;

  function readPractice() {
    const topic = $("#practice-topic"), difficulty = $("#practice-difficulty"), type = $("#practice-type"), limit = $("#practice-limit");
    ui.practice.topicId = topic?.value || ui.practice.topicId;
    ui.practice.difficulty = difficulty?.value || "";
    ui.practice.type = type?.value || "";
    ui.practice.limit = limit?.value || "10";
    return { ...ui.practice };
  }

  async function startPractice(button) {
    const filters = readPractice(), mount = $("#practice-stage");
    if (!mount || !filters.topicId) { toast("Choose a topic before starting practice.", "error"); return; }
    const sequence = renderSequence;
    if (button) button.disabled = true;
    ui.practice.stage = "loading";
    mount.innerHTML = `<div class="quiz-shell">${skeleton()}</div>`;
    try {
      const data = await fetchData("/api/v1/questions", { topic_id: filters.topicId, limit: filters.limit, difficulty: filters.difficulty, question_type: filters.type }, "content");
      if (sequence !== renderSequence || currentRoute?.name !== "practice") return;
      const topic = app.topics.find((item) => item.topic_id === filters.topicId), questions = Array.isArray(data?.questions) ? data.questions : [];
      if (!questions.length) { ui.practice.stage = "idle"; mount.innerHTML = emptyState({ title: "No questions match this set", text: "Try another topic, difficulty, or question type.", iconName: "search" }); paint(mount); typeset(mount); return; }
      const quiz = newQuiz(questions, { mode: "practice", modeLabel: "Practice Arena", kicker: `${topic?.topic_name || "Practice"} · Practice`, topicId: filters.topicId, topicName: topic?.topic_name || "", returnTab: "questions" });
      if (topic) { state.lastTopic = { id: topic.topic_id, name: topic.topic_name, tab: "questions" }; saveState(); }
      ui.practice.stage = "quiz";
      mountQuiz(mount, quiz);
      if (typeof mount.scrollIntoView === "function") mount.scrollIntoView({ behavior: "smooth", block: "start" });
    } catch (error) {
      if (sequence !== renderSequence || currentRoute?.name !== "practice") return;
      ui.practice.stage = "idle";
      mount.innerHTML = notFound(error) ? emptyState({ title: "No questions found", text: "MathAPI returned no questions for this combination.", iconName: "target" }) : errorState(error, "practice-start", "Try this set again");
      paint(mount);
      typeset(mount);
    } finally {
      if (button) button.disabled = false;
    }
  }

  async function viewPractice(route, sequence) {
    const data = await getTopics();
    if (sequence !== renderSequence) return null;
    if (!data.topics.length) return { html: head({ eyebrow: "Workspace", title: "Practice Arena", text: "Build custom practice sets from the topic catalog." }) + emptyState({ title: "No topics available", text: "The practice arena needs topics and questions in MathAPI.", iconName: "target" }), title: "Practice Arena", eyebrow: "Workspace" };
    const requested = route.query.get("topic");
    if (requested && data.topics.some((topic) => topic.topic_id === requested)) ui.practice.topicId = requested;
    if (!data.topics.some((topic) => topic.topic_id === ui.practice.topicId)) ui.practice.topicId = state.lastTopic?.id && data.topics.some((topic) => topic.topic_id === state.lastTopic.id) ? state.lastTopic.id : data.topics[0].topic_id;
    ui.practice.stage = "idle";
    return {
      html: `${head({ eyebrow: "Workspace", title: "Practice Arena", text: "Choose the topic, difficulty, and question style. Every attempt updates your session accuracy.", actions: '<a class="btn btn-secondary" href="#/daily">Daily Challenge</a>' })}<div class="filter-bar"><label class="field field-grow"><span class="field-label">Topic</span><select class="select" id="practice-topic">${practiceOptions(ui.practice.topicId)}</select></label><label class="field"><span class="field-label">Difficulty</span><select class="select" id="practice-difficulty"><option value="">Any level</option>${LEVELS.map((item) => `<option value="${esc(item)}"${selected(item, ui.practice.difficulty)}>${esc(item)}</option>`).join("")}</select></label><label class="field"><span class="field-label">Question type</span><select class="select" id="practice-type"><option value="">Any type</option>${TYPES.map((item) => `<option value="${esc(item)}"${selected(item, ui.practice.type)}>${esc(item)}</option>`).join("")}</select></label><label class="field"><span class="field-label">Questions</span><select class="select" id="practice-limit">${[5, 10, 15, 20].map((count) => `<option value="${count}"${selected(String(count), ui.practice.limit)}>${count}</option>`).join("")}</select></label><button class="btn btn-primary" type="button" data-action="practice-start">${icon("play")} Start practice</button></div><div id="practice-stage">${practiceIntro()}</div>`,
      title: "Practice Arena",
      eyebrow: "Workspace"
    };
  }

  function challengeDate(value) {
    const match = /^(\d{4})-(\d{2})-(\d{2})/.exec(String(value || ""));
    return match ? formatDate(new Date(Number(match[1]), Number(match[2]) - 1, Number(match[3]))) : formatDate(value);
  }

  async function viewDaily(route, sequence) {
    await getTopics().catch(() => null);
    if (!app.connection) return null;
    const data = await fetchData("/api/v1/daily-challenge", {}, "daily");
    if (sequence !== renderSequence) return null;
    const questions = Array.isArray(data?.questions) ? data.questions : [];
    if (!questions.length) return { html: head({ eyebrow: "Discover", title: "Daily Challenge", text: "Three questions selected for everyone using this API today." }) + emptyState({ title: "No challenge today", text: "MathAPI did not return a daily challenge.", iconName: "calendar" }), title: "Daily Challenge", eyebrow: "Discover" };
    const quiz = newQuiz(questions, { mode: "daily", modeLabel: "Daily Challenge", kicker: "Daily challenge · Shared set" });
    return { html: `${head({ eyebrow: "Discover", title: "Three problems for today.", text: `One beginner, one intermediate, and one advanced problem · ${challengeDate(data?.challenge_date)}`, actions: '<a class="btn btn-secondary" href="#/practice">Practice Arena</a>' })}<div id="daily-stage">${quizShell(quiz)}</div>`, title: "Daily Challenge", eyebrow: "Discover", quiz };
  }

  async function loadRandom(sequence) {
    const mount = $("#random-stage");
    if (!mount) return;
    const token = ++randomRequest;
    mount.innerHTML = `<div class="quiz-shell">${skeleton()}</div>`;
    try {
      if (!app.topics.length) await getTopics().catch(() => null);
      if (!app.connection) return;
      const data = await fetchData("/api/v1/random-question", {}, null);
      if (token !== randomRequest || sequence !== renderSequence || currentRoute?.name !== "random") return;
      if (!data?.question) { mount.innerHTML = emptyState({ title: "No question available", text: "MathAPI returned no random question.", iconName: "shuffle" }); paint(mount); return; }
      mountQuiz(mount, newQuiz([data.question], { mode: "random", modeLabel: "Random question", kicker: "Random question · Any topic" }));
    } catch (error) {
      if (token !== randomRequest || sequence !== renderSequence || currentRoute?.name !== "random") return;
      mount.innerHTML = errorState(error, "random-new", "Try another question");
      paint(mount);
    }
  }

  async function viewRandom(route, sequence) {
    if (!app.topics.length) await getTopics().catch(() => null);
    if (!app.connection) return null;
    const data = await fetchData("/api/v1/random-question", {}, null);
    if (sequence !== renderSequence) return null;
    const question = data?.question;
    if (!question) return { html: head({ eyebrow: "Discover", title: "Random Question", text: "Pull one question from anywhere in the catalog." }) + emptyState({ title: "No question available", text: "MathAPI returned no random question.", iconName: "shuffle" }), title: "Random Question", eyebrow: "Discover" };
    const quiz = newQuiz([question], { mode: "random", modeLabel: "Random question", kicker: "Random question · Any topic" });
    return { html: `${head({ eyebrow: "Discover", title: "A question from anywhere.", text: "A fresh random prompt from any topic, difficulty, or question type.", actions: `<button class="btn btn-primary" type="button" data-action="random-new">${icon("shuffle")} Shuffle again</button>` })}<div id="random-stage">${quizShell(quiz)}</div>`, title: "Random Question", eyebrow: "Discover", quiz };
  }

  async function loadFormulaSheet(topic, sequence) {
    const mount = $("#formula-stage");
    if (!mount) return;
    try {
      const data = await fetchData("/api/v1/formulae", { topic_id: topic.topic_id }, "content");
      if (sequence !== renderSequence) return;
      const formulae = Array.isArray(data?.formulae) ? data.formulae : [];
      mount.innerHTML = formulae.length ? `<div class="section-head"><div><h3 class="section-title">${esc(topic.topic_name)}</h3><p class="section-subtitle">${Number(data?.total_formulae) || formulae.length} formulae · rendered with KaTeX</p></div><a class="section-link" href="#/topic/${encodeURIComponent(topic.topic_id)}/formulae">Open topic studio ${icon("arrow-right")}</a></div><div class="formula-grid">${formulae.map(formulaCard).join("")}</div>` : emptyState({ title: "No formulae for this topic", text: "Pick another topic from the selector above.", iconName: "formula" });
      paint(mount);
      typeset(mount);
    } catch (error) {
      if (sequence !== renderSequence) return;
      mount.innerHTML = notFound(error) ? emptyState({ title: "No formulae for this topic", text: "Choose a different topic or try again later.", iconName: "formula" }) : errorState(error);
      paint(mount);
    }
  }

  async function viewFormulas(route, sequence) {
    const data = await getTopics();
    if (sequence !== renderSequence) return null;
    if (!data.topics.length) return { html: head({ eyebrow: "Library", title: "Formula Vault", text: "Concise, LaTeX-rendered formula sheets from the catalog." }) + emptyState({ title: "No topics available", text: "The formula vault needs topics in MathAPI.", iconName: "formula" }), title: "Formula Vault", eyebrow: "Library" };
    const requested = route.query.get("topic");
    if (requested && data.topics.some((topic) => topic.topic_id === requested)) ui.formulaTopicId = requested;
    if (!data.topics.some((topic) => topic.topic_id === ui.formulaTopicId)) ui.formulaTopicId = state.lastTopic?.id && data.topics.some((topic) => topic.topic_id === state.lastTopic.id) ? state.lastTopic.id : (data.topics.find((topic) => Number(topic.formulae_available) > 0) || data.topics[0]).topic_id;
    const topic = data.topics.find((item) => item.topic_id === ui.formulaTopicId) || data.topics[0];
    return {
      html: `${head({ eyebrow: "Library", title: "Formula Vault", text: "Scan a single well-curated sheet, copy the LaTeX, and get back to the reasoning.", actions: `<a class="btn btn-secondary" href="#/topic/${encodeURIComponent(topic.topic_id)}/formulae">${icon("book-open")} Topic studio</a>` })}<div class="filter-bar"><label class="field field-grow"><span class="field-label">Formula sheet</span><select class="select" id="formula-topic">${data.topics.map((item) => `<option value="${esc(item.topic_id)}"${selected(item.topic_id, topic.topic_id)}>${esc(item.topic_name)} · ${Number(item.formulae_available) || 0} formulae</option>`).join("")}</select></label><span class="result-count">${Number(topic.formulae_available) || 0} formulae available</span></div><div id="formula-stage">${skeleton()}</div>`,
      title: "Formula Vault",
      eyebrow: "Library",
      after: () => loadFormulaSheet(topic, sequence)
    };
  }

  async function viewSaved(route, sequence) {
    const data = await getTopics();
    if (sequence !== renderSequence) return null;
    const savedTopics = state.bookmarks.map((id) => data.topics.find((topic) => topic.topic_id === id)).filter(Boolean), progress = Object.entries(state.progress).filter(([, entry]) => entry && entry.attempted > 0).sort((left, right) => new Date(right[1].lastAttempt || 0) - new Date(left[1].lastAttempt || 0)), attempted = progress.reduce((sum, [, entry]) => sum + entry.attempted, 0), correct = progress.reduce((sum, [, entry]) => sum + entry.correct, 0), accuracy = attempted ? Math.round((correct / attempted) * 100) : 0;
    const actions = `${progress.length ? `<button class="btn btn-ghost" type="button" data-action="reset-progress">${icon("rotate")} Reset progress</button>` : ""}${savedTopics.length ? `<button class="btn btn-ghost" type="button" data-action="clear-bookmarks">${icon("trash")} Clear bookmarks</button>` : ""}`;
    const savedMarkup = savedTopics.length ? `<div class="topic-grid">${savedTopics.map(topicCard).join("")}</div>` : emptyState({ title: "No saved topics", text: "Tap the bookmark icon on any topic to keep it here for this browser session.", iconName: "bookmark", action: '<a class="btn btn-primary" href="#/topics">Browse topics</a>' });
    const progressMarkup = progress.length ? `<div class="topic-progress-list">${progress.map(([topicId, entry]) => {
      const topicAccuracy = entry.attempted ? Math.round((entry.correct / entry.attempted) * 100) : 0;
      return `<div class="progress-row"><div><strong>${esc(topicName(topicId))}</strong><br><span>${entry.attempted} attempted · ${topicAccuracy}% accuracy · ${esc(ago(entry.lastAttempt))}</span></div><div class="progress-bar" aria-label="${topicAccuracy}% accuracy"><div class="progress-fill" style="width: ${topicAccuracy}%"></div></div><a class="btn btn-ghost btn-sm" href="#/topic/${encodeURIComponent(topicId)}/questions">Practice</a></div>`;
    }).join("")}</div>` : emptyState({ title: "No attempts yet", text: "Answer a practice question and your session accuracy will appear here.", iconName: "target", action: '<a class="btn btn-primary" href="#/practice">Start practicing</a>' });
    const historyMarkup = state.history.length ? `<div class="topic-progress-list">${state.history.slice(0, 6).map((entry) => `<div class="progress-row"><div><strong>${esc(entry.label || "Practice session")}</strong><br><span>${esc(entry.topicName || topicName(entry.topicId))} · ${esc(ago(entry.completedAt))}</span></div><span>${Number(entry.correct) || 0} / ${Number(entry.attempted) || 0}</span></div>`).join("")}</div>` : "";
    return {
      html: `${head({ eyebrow: "Your data", title: "Saved work, session by session.", text: "Bookmarks and accuracy are stored in this tab's sessionStorage. Closing the tab clears the learning record.", actions })}<div class="progress-grid">${statCard("bookmark", savedTopics.length, "Saved topics")}${statCard("target", attempted, "Questions attempted")}${statCard("check-circle", `${accuracy}%`, "Overall accuracy")}${statCard("layers", progress.length, "Topics touched")}</div><section class="section"><div class="section-head"><div><h3 class="section-title">Saved topics</h3><p class="section-subtitle">Your current shortlist.</p></div><a class="section-link" href="#/topics">Add topics ${icon("plus")}</a></div>${savedMarkup}</section><section class="section"><div class="section-head"><div><h3 class="section-title">Topic progress</h3><p class="section-subtitle">Accuracy from answered quiz questions.</p></div></div>${progressMarkup}</section>${historyMarkup ? `<section class="section"><div class="section-head"><div><h3 class="section-title">Recent sessions</h3><p class="section-subtitle">The latest completed quiz sets in this tab.</p></div></div>${historyMarkup}</section>` : ""}`,
      title: "Saved & Progress",
      eyebrow: "Your data"
    };
  }

  const settingsRow = (label, value, plain = false) => `<div class="info-row"><span class="info-label">${esc(label)}</span><span class="info-value${plain ? " plain" : ""}">${esc(value)}</span></div>`;

  function viewSettings() {
    const connection = app.connection, keyExpiry = expiry(connection?.apiKey), online = Boolean(app.online), attempted = Object.values(state.progress).reduce((sum, entry) => sum + (entry.attempted || 0), 0);
    const healthMessage = online ? (app.health?.message || "The API responded successfully.") : `MathAPI is not reachable at ${API_BASE}. Check the connection and try again.`;
    return {
      html: `${head({ eyebrow: "Your data", title: "Settings & connection.", text: "Manage the MathAPI key for this tab. Keys are session-only and are sent only to MathAPI.", actions: `<button class="btn btn-secondary" type="button" data-action="test-connection">${icon("wifi")} Test connection</button>` })}<div class="settings-grid"><article class="info-card"><h3>API connection</h3><p>Your key is stored in sessionStorage and cleared when this tab closes.</p><div class="info-list">${settingsRow("Status", connection ? "Connected" : "Not connected", true)}${settingsRow("API key", connection ? mask(connection.apiKey) : "Not connected")}${settingsRow("Expires", keyExpiry ? formatDateTime(keyExpiry) : connection ? "Unknown" : "—", true)}${settingsRow("Storage", "This tab only", true)}</div><div class="actions-row"><button class="btn btn-primary btn-sm" type="button" data-action="change-api-key">${icon("lock")} Change API key</button><button class="btn btn-ghost btn-sm" type="button" data-action="clear-cache">${icon("database")} Clear cache</button><button class="btn btn-danger btn-sm" type="button" data-action="disconnect-api-key" ${connection ? "" : "disabled"}>${icon("x")} Disconnect</button></div></article><article class="info-card"><h3>MathAPI</h3><p>All requests go to the live MathAPI endpoint.</p><div class="health-card ${online ? "is-online" : "is-offline"}"><span class="health-icon">${icon(online ? "wifi" : "server")}</span><div><strong>${online ? "API reachable" : "API offline"}</strong><p>${esc(healthMessage)}</p></div></div><div class="info-list">${settingsRow("Endpoint", API_BASE)}${settingsRow("API key header", "X-API-Key")}${settingsRow("Rate limit", "100/hour per key · 300/hour per IP", true)}${settingsRow("Docs", `${API_BASE}/docs`)}</div><div class="actions-row">${external(`${API_BASE}/docs`, "Open API docs", "btn btn-secondary btn-sm")}</div></article><article class="info-card span-2"><h3>Session data</h3><p>Bookmarks, quiz progress, and cached responses stay in this tab. The interface is always light and follows your system text preferences.</p><div class="info-list">${settingsRow("Bookmarked topics", String(state.bookmarks.length), true)}${settingsRow("Questions attempted", String(attempted), true)}${settingsRow("Cached API responses", String(app.cache.size), true)}${settingsRow("Last topic", state.lastTopic?.name || "None", true)}</div><div class="actions-row"><button class="btn btn-danger btn-sm" type="button" data-action="reset-learning-data">${icon("trash")} Reset learning data</button></div></article></div>`,
      title: "Settings",
      eyebrow: "Your data"
    };
  }

  function safeDecode(value) {
    try {
      return decodeURIComponent(value || "");
    } catch (error) {
      return value || "";
    }
  }

  function parseHash() {
    const raw = window.location.hash.replace(/^#/, "") || "/dashboard";
    const split = raw.indexOf("?");
    const path = split >= 0 ? raw.slice(0, split) : raw;
    const query = new URLSearchParams(split >= 0 ? raw.slice(split + 1) : "");
    const segments = path.split("/").filter(Boolean).map(safeDecode);
    const name = Object.prototype.hasOwnProperty.call(ROUTES, segments[0]) ? segments[0] : "dashboard";
    return {
      name,
      id: name === "topic" ? segments[1] || "" : "",
      tab: name === "topic" ? segments[2] || "explanation" : "",
      query
    };
  }

  async function renderRoute() {
    if (!app.connection) {
      showGate();
      return;
    }
    const sequence = ++renderSequence;
    const route = parseHash();
    currentRoute = route;
    closeSidebar();
    quizSession = null;
    chrome(route);
    const view = $("#view");
    if (!view) return;
    view.innerHTML = skeleton();
    try { window.scrollTo({ top: 0, left: 0, behavior: "auto" }); } catch (error) { window.scrollTo?.(0, 0); }
    try {
      const views = { dashboard: viewDashboard, topics: viewTopics, topic: viewTopic, practice: viewPractice, daily: viewDaily, random: viewRandom, formulas: viewFormulas, saved: viewSaved, settings: viewSettings };
      const result = await (views[route.name] || viewDashboard)(route, sequence);
      if (!result || sequence !== renderSequence) return;
      chrome(route, { title: result.title, eyebrow: result.eyebrow });
      if (result.quiz) quizSession = result.quiz;
      view.dataset.route = route.name;
      view.innerHTML = result.html;
      paint(view);
      typeset(view);
      if (typeof result.after === "function") {
        try {
          await result.after();
        } catch (error) {
          if (sequence !== renderSequence) return;
          if (error instanceof ApiError && error.status === 401 && !app.connection) return;
          toast(error.message || "This section could not load.", "error");
        }
      }
    } catch (error) {
      if (sequence !== renderSequence) return;
      if (error instanceof ApiError && error.status === 401 && !app.connection) return;
      view.innerHTML = errorState(error);
      paint(view);
    }
  }

  async function copyText(value) {
    if (navigator.clipboard?.writeText && window.isSecureContext) {
      await navigator.clipboard.writeText(value);
      return;
    }
    const area = document.createElement("textarea");
    area.value = value;
    area.setAttribute("readonly", "");
    area.style.position = "fixed";
    area.style.left = "-9999px";
    document.body.appendChild(area);
    area.select();
    const copied = document.execCommand("copy");
    area.remove();
    if (!copied) throw new Error("Copy is not available in this browser.");
  }

  async function handleAction(action, element) {
    try {
      if (action === "change-api-key") return showGate();
      if (action === "cancel-key-gate") { if (app.connection) hideGate(); return; }
      if (action === "toggle-key-visibility") return toggleKeyVisibility();
      if (action === "copy-auth-curl") {
        const curl = $("#auth-curl")?.textContent?.trim();
        if (!curl) return toast("The request example is unavailable.", "error");
        await copyText(curl);
        return toast("Request example copied.", "success");
      }
      if (action === "auth-test-connection") { await testGate(element); return; }
      if (action === "disconnect-api-key") { await disconnect(); return; }
      if (action === "clear-cache") { clearCache(); toast("Cached MathAPI responses cleared.", "success"); if (currentRoute?.name === "settings") await renderRoute(); return; }
      if (action === "toggle-bookmark") {
        const topicId = element?.dataset.topicId;
        if (!topicId) return;
        const saved = toggleBookmark(topicId);
        toast(saved ? "Topic saved for this session." : "Bookmark removed.", "success");
        syncBookmarks(topicId);
        if (currentRoute?.name === "saved") await renderRoute();
        return;
      }
      if (action === "copy-formula") {
        const latex = element?.closest(".formula-card")?.querySelector("[data-latex]")?.textContent?.trim();
        if (!latex) return toast("There is no LaTeX code to copy.", "error");
        await copyText(latex);
        return toast("LaTeX copied to the clipboard.", "success");
      }
      if (action.startsWith("quiz-")) { quizAction(action, element); return; }
      if (action === "retry-route") { await renderRoute(); return; }
      if (action === "clear-topic-filters") {
        ui.search = ""; ui.branch = ""; ui.difficulty = ""; ui.sort = "name";
        if (window.location.hash.includes("?")) history.replaceState(null, "", "#/topics");
        await renderRoute();
        return;
      }
      if (action === "practice-start" || action === "practice-restart") { await startPractice(element); return; }
      if (action === "practice-reset") { await renderRoute(); return; }
      if (action === "random-new") { await loadRandom(renderSequence); return; }
      if (action === "test-connection") {
        if (element) element.disabled = true;
        try { await health(); toast("MathAPI is reachable.", "success"); if (currentRoute?.name === "settings") await renderRoute(); }
        catch (error) { toast(error.message || "MathAPI is not reachable.", "error"); if (currentRoute?.name === "settings") await renderRoute(); }
        finally { if (element) element.disabled = false; }
        return;
      }
      if (action === "reset-progress") {
        const confirmed = await openModal({ title: "Reset quiz progress?", message: "This clears session accuracy and recent quiz history. Your bookmarks stay intact.", confirmLabel: "Reset progress", danger: true });
        if (!confirmed) return;
        resetProgress(); toast("Quiz progress reset.", "success"); await renderRoute(); return;
      }
      if (action === "clear-bookmarks") {
        const confirmed = await openModal({ title: "Clear saved topics?", message: "This removes every bookmark from this browser session.", confirmLabel: "Clear bookmarks", danger: true });
        if (!confirmed) return;
        state.bookmarks = []; saveState(); toast("Saved topics cleared.", "success"); await renderRoute(); return;
      }
      if (action === "reset-learning-data") {
        const confirmed = await openModal({ title: "Reset all learning data?", message: "Bookmarks, progress, recent sessions, and the last-opened topic will be cleared from sessionStorage.", confirmLabel: "Reset everything", danger: true });
        if (!confirmed) return;
        resetLearning(); toast("Session learning data reset.", "success"); await renderRoute();
      }
    } catch (error) {
      if (error instanceof ApiError && error.status === 401 && !app.connection) return;
      toast(error.message || "That action could not be completed.", "error");
    }
  }

  async function onDocumentClick(event) {
    if (event.target.closest("[data-modal-confirm]")) { event.preventDefault(); closeModal(true); return; }
    if (event.target.closest("[data-modal-cancel]")) { event.preventDefault(); closeModal(false); return; }
    if (event.target.id === "modal-root") { closeModal(false); return; }
    if (event.target.closest("#menu-toggle")) { event.preventDefault(); setSidebar(!$("#sidebar")?.classList.contains("is-open")); return; }
    if (event.target.closest("#sidebar-backdrop")) { closeSidebar(); return; }
    if (event.target.closest("[data-skip-link]")) {
      event.preventDefault();
      const gate = $("#auth-gate");
      if (gate && !gate.hidden) { $("#api-key-input")?.focus(); return; }
      const view = $("#view");
      if (view) { view.focus(); if (typeof view.scrollIntoView === "function") view.scrollIntoView({ block: "start" }); }
      return;
    }
    if (event.target.closest('a[href^="#/"]')) closeSidebar();
    const actionElement = event.target.closest("[data-action]");
    if (actionElement) { event.preventDefault(); await handleAction(actionElement.dataset.action || "", actionElement); }
  }

  function onDocumentInput(event) {
    if (event.target.id !== "topic-search") return;
    ui.search = event.target.value;
    refreshTopics();
  }

  function onDocumentChange(event) {
    const id = event.target.id, value = event.target.value;
    if (id === "formula-topic") { if (value) window.location.hash = `#/formulas?topic=${encodeURIComponent(value)}`; return; }
    const filters = { "topic-branch": "branch", "topic-difficulty": "difficulty", "topic-sort": "sort" };
    if (filters[id]) { ui[filters[id]] = value; refreshTopics(); return; }
    const practice = { "practice-topic": "topicId", "practice-difficulty": "difficulty", "practice-type": "type", "practice-limit": "limit" };
    if (practice[id]) ui.practice[practice[id]] = value;
  }

  function onDocumentSubmit(event) {
    if (event.target.id !== "api-key-form") return;
    connectWithKey(event);
  }

  function onDocumentKeydown(event) {
    if (event.key !== "Escape") return;
    if (modalResolve) { closeModal(false); return; }
    const gate = $("#auth-gate");
    if (gate && !gate.hidden) { const cancel = $("#auth-cancel"); if (cancel && !cancel.hidden) hideGate(); return; }
    if ($("#sidebar")?.classList.contains("is-open")) closeSidebar();
  }

  function bindEvents() {
    document.addEventListener("click", onDocumentClick);
    document.addEventListener("input", onDocumentInput);
    document.addEventListener("change", onDocumentChange);
    document.addEventListener("submit", onDocumentSubmit);
    document.addEventListener("keydown", onDocumentKeydown);
    window.addEventListener("hashchange", renderRoute);
    window.addEventListener("resize", onResize);
  }

  async function boot() {
    paint();
    bindEvents();
    clearLegacy();
    app.connection = loadConnection();
    sessionUI();
    apiStatus("checking", "Checking API");
    if (!window.location.hash || window.location.hash === "#/") {
      try { history.replaceState(null, "", "#/dashboard"); } catch (error) { window.location.hash = "#/dashboard"; }
    }
    const healthPromise = health().catch(() => null);
    if (app.connection) { setApp(true); loadingDone(); await renderRoute(); }
    else { loadingDone(); showGate(); }
    healthPromise.then(() => { if (app.connection && currentRoute?.name === "settings") renderRoute(); });
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot, { once: true });
  else boot();
})();
