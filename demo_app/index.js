(() => {
  "use strict";

  const API_BASE = "https://mathapi.vercel.app";
  const DEMO_IDENTITY = Object.freeze({
    username: "demo_app",
    email: "demo_app@example.com"
  });
  const STORAGE_KEYS = Object.freeze({
    session: "mathlabs.session",
    state: "mathlabs.state",
    theme: "mathlabs.theme"
  });
  const CACHE_TTL = Object.freeze({
    topics: 10 * 60 * 1000,
    explanation: 30 * 60 * 1000,
    content: 30 * 60 * 1000,
    daily: 60 * 60 * 1000
  });
  const BRANCHES = Object.freeze([
    "Number Theory",
    "Algebra",
    "Geometry",
    "Coordinate Geometry",
    "Trigonometry",
    "Combinatorics",
    "Applied Mathematics"
  ]);
  const DIFFICULTIES = Object.freeze(["Beginner", "Intermediate", "Advanced"]);
  const QUESTION_TYPES = Object.freeze([
    "Conceptual",
    "Numerical",
    "To Prove",
    "Word Problem",
    "Case Based",
    "Higher Order Thinking Skills"
  ]);
  const TOPIC_TABS = Object.freeze(["explanation", "examples", "questions", "formulae", "sources"]);
  const ROUTES = Object.freeze({
    dashboard: { eyebrow: "Workspace", title: "Dashboard" },
    topics: { eyebrow: "Library", title: "Explore Topics" },
    topic: { eyebrow: "Topic studio", title: "Topic" },
    practice: { eyebrow: "Workspace", title: "Practice Arena" },
    daily: { eyebrow: "Discover", title: "Daily Challenge" },
    random: { eyebrow: "Discover", title: "Random Question" },
    formulas: { eyebrow: "Library", title: "Formula Vault" },
    saved: { eyebrow: "Account", title: "Saved & Progress" },
    settings: { eyebrow: "Account", title: "Settings" }
  });

  const ICON_PATHS = Object.freeze({
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
    sun: '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.42 1.42M17.66 17.66l1.41 1.41M2 12h2M20 12h2M4.93 19.07l1.42-1.42M17.66 6.34l1.41-1.41"/>',
    moon: '<path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79Z"/>',
    search: '<circle cx="11" cy="11" r="7"/><path d="m20 20-4-4"/>',
    "chevron-right": '<path d="m9 18 6-6-6-6"/>',
    "arrow-right": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "arrow-left": '<path d="M19 12H5M11 18l-6-6 6-6"/>',
    sparkles: '<path d="m12 3 1.6 4.4L18 9l-4.4 1.6L12 15l-1.6-4.4L6 9l4.4-1.6L12 3Z"/><path d="m5 16 .8 2.2L8 19l-2.2.8L5 22l-.8-2.2L2 19l2.2-.8L5 16Z"/><path d="m19 14 .7 1.8 1.8.7-1.8.7L19 19l-.7-1.8-1.8-.7 1.8-.7L19 14Z"/>',
    layers: '<path d="m12 3 9 5-9 5-9-5 9-5Z"/><path d="m3 12 9 5 9-5"/><path d="m3 16 9 5 9-5"/>',
    "file-text": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8Z"/><path d="M14 2v6h6M8 13h8M8 17h6"/>',
    help: '<circle cx="12" cy="12" r="9"/><path d="M9.5 9a2.7 2.7 0 0 1 5.2.9c0 1.8-2.7 2.1-2.7 4.1"/><path d="M12 18h.01"/>',
    "book-open": '<path d="M2 4h6a4 4 0 0 1 4 4v13a3 3 0 0 0-3-3H2V4Z"/><path d="M22 4h-6a4 4 0 0 0-4 4v13a3 3 0 0 1 3-3h7V4Z"/>',
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
    home: '<path d="m3 10 9-7 9 7v10a1 1 0 0 1-1 1h-5v-7H9v7H4a1 1 0 0 1-1-1V10Z"/>',
    trash: '<path d="M3 6h18M8 6V4h8v2M19 6l-1 15H6L5 6M10 10v7M14 10v7"/>',
    wifi: '<path d="M5 12.5a10 10 0 0 1 14 0"/><path d="M8.5 16a5 5 0 0 1 7 0"/><path d="M12 20h.01"/>',
    server: '<rect x="3" y="4" width="18" height="6" rx="2"/><rect x="3" y="14" width="18" height="6" rx="2"/><path d="M7 7h.01M7 17h.01"/>',
    lock: '<rect x="4" y="10" width="16" height="11" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/>',
    mail: '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
    shield: '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10Z"/><path d="m9 12 2 2 4-4"/>',
    hash: '<path d="M4 9h16M4 15h16M10 3 8 21M16 3l-2 18"/>',
    plus: '<path d="M12 5v14M5 12h14"/>',
    filter: '<path d="M3 5h18l-7 8v6l-4 2v-8L3 5Z"/>',
    "check-circle": '<circle cx="12" cy="12" r="9"/><path d="m8 12 2.5 2.5L16 9"/>',
    award: '<circle cx="12" cy="8" r="5"/><path d="m8.5 12-1.5 9 5-3 5 3-1.5-9"/>',
    terminal: '<path d="m4 17 6-6-6-6"/><path d="M12 19h8"/>'
  });

  const app = {
    session: null,
    health: null,
    healthAt: 0,
    cache: new Map(),
    inflight: new Map(),
    topics: [],
    authenticated: false,
    online: false
  };
  const ui = {
    topicSearch: "",
    topicBranch: "",
    topicDifficulty: "",
    topicSort: "name",
    practice: {
      topicId: "",
      difficulty: "",
      questionType: "",
      limit: "10",
      stage: "idle",
      error: null
    },
    formulaTopicId: ""
  };
  let state = loadState();
  let currentRoute = null;
  let renderSequence = 0;
  let quizSession = null;
  let modalResolve = null;
  let toastSequence = 0;
  let randomRequest = 0;

  function icon(name, className = "icon") {
    const paths = ICON_PATHS[name] || ICON_PATHS.sparkles;
    return `<svg class="${className}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${paths}</svg>`;
  }

  function hydrateIcons(root = document) {
    root.querySelectorAll("[data-icon]").forEach((node) => {
      const name = node.getAttribute("data-icon");
      if (name) node.innerHTML = icon(name);
    });
  }

  function escapeHtml(value) {
    return String(value ?? "").replace(/[&<>"']/g, (character) => ({
      "&": "&amp;",
      "<": "&lt;",
      ">": "&gt;",
      '"': "&quot;",
      "'": "&#39;"
    })[character]);
  }

  function prose(value) {
    const text = String(value ?? "").trim();
    if (!text) return "";
    return text.split(/\n{2,}/).map((block) => (
      `<p>${escapeHtml(block).replace(/\n/g, "<br>")}</p>`
    )).join("");
  }

  function safeUrl(value) {
    try {
      const url = new URL(String(value ?? ""), window.location.href);
      if (url.protocol !== "http:" && url.protocol !== "https:") return "";
      return escapeHtml(url.href);
    } catch (error) {
      return "";
    }
  }

  function externalLink(url, label, className = "") {
    const href = safeUrl(url);
    if (!href) return `<span class="${escapeHtml(className)}">${escapeHtml(label)}</span>`;
    return `<a class="${escapeHtml(className)}" href="${href}" target="_blank" rel="noopener noreferrer">${escapeHtml(label)}${icon("external")}</a>`;
  }

  function safeTopicTab(value) {
    return TOPIC_TABS.includes(value) ? value : "explanation";
  }

  function difficultySlug(value) {
    return String(value || "").toLowerCase();
  }

  function difficultyChip(value) {
    const label = String(value || "Unrated");
    return `<span class="chip difficulty difficulty-${escapeHtml(difficultySlug(label))}">${escapeHtml(label)}</span>`;
  }

  function chipList(values, className = "chip") {
    const list = Array.isArray(values) ? values : values ? [values] : [];
    return list.map((value) => `<span class="${className}">${escapeHtml(value)}</span>`).join("");
  }

  function typeChips(values) {
    const list = Array.isArray(values) ? values : values ? [values] : [];
    return list.map((value) => `<span class="chip">${escapeHtml(value)}</span>`).join("");
  }

  function formatDate(value, options) {
    if (!value) return "—";
    const date = value instanceof Date ? value : new Date(value);
    if (Number.isNaN(date.getTime())) return String(value);
    return new Intl.DateTimeFormat(undefined, options || {
      month: "short",
      day: "numeric",
      year: "numeric"
    }).format(date);
  }

  function formatDateTime(value) {
    if (!value) return "—";
    const date = value instanceof Date ? value : new Date(value);
    if (Number.isNaN(date.getTime())) return String(value);
    return new Intl.DateTimeFormat(undefined, {
      month: "short",
      day: "numeric",
      year: "numeric",
      hour: "numeric",
      minute: "2-digit"
    }).format(date);
  }

  function timeAgo(value) {
    if (!value) return "Not started";
    const time = new Date(value).getTime();
    if (!Number.isFinite(time)) return "Not started";
    const seconds = Math.max(0, Math.round((Date.now() - time) / 1000));
    if (seconds < 60) return "Just now";
    const minutes = Math.round(seconds / 60);
    if (minutes < 60) return `${minutes}m ago`;
    const hours = Math.round(minutes / 60);
    if (hours < 24) return `${hours}h ago`;
    const days = Math.round(hours / 24);
    if (days < 7) return `${days}d ago`;
    return formatDate(time);
  }

  function sessionExpiryMs(session) {
    const match = /_exp=(\d+)/.exec(session?.apiKey || "");
    if (match) return Number(match[1]) * 1000;
    const parsed = Date.parse(session?.expiry || "");
    return Number.isFinite(parsed) ? parsed : 0;
  }

  function sessionIsExpired(session) {
    const expiry = sessionExpiryMs(session);
    return Boolean(expiry && expiry <= Date.now() + 60 * 1000);
  }

  function maskKey(value) {
    if (!value) return "Not available";
    if (value.length < 28) return "••••••••";
    return `${value.slice(0, 14)}…${value.slice(-10)}`;
  }

  function initials(value) {
    const parts = String(value || "Demo Project").trim().split(/[^a-z0-9]+/i).filter(Boolean);
    if (!parts.length) return "ML";
    if (parts.length === 1) return parts[0].slice(0, 2).toUpperCase();
    return `${parts[0][0]}${parts[1][0]}`.toUpperCase();
  }

  function normalizeLatex(value) {
    let latex = String(value ?? "").trim();
    if (latex.startsWith("$$") && latex.endsWith("$$") && latex.length >= 4) {
      latex = latex.slice(2, -2);
    } else if (latex.startsWith("$") && latex.endsWith("$") && latex.length >= 2) {
      latex = latex.slice(1, -1);
    } else if (latex.startsWith("\\[") && latex.endsWith("\\]")) {
      latex = latex.slice(2, -2);
    } else if (latex.startsWith("\\(") && latex.endsWith("\\)")) {
      latex = latex.slice(2, -2);
    }
    return latex.trim();
  }

  function mathBlock(value) {
    const latex = normalizeLatex(value);
    if (!latex) return "";
    if (window.katex) {
      try {
        return window.katex.renderToString(latex, {
          displayMode: true,
          throwOnError: false,
          strict: "ignore",
          trust: false
        });
      } catch (error) {
        return `<code class="formula-raw">${escapeHtml(value)}</code>`;
      }
    }
    return `<code class="formula-raw">${escapeHtml(value)}</code>`;
  }

  function renderMath(root = document) {
    if (!window.renderMathInElement || !root) return;
    try {
      window.renderMathInElement(root, {
        delimiters: [
          { left: "$$", right: "$$", display: true },
          { left: "\\[", right: "\\]", display: true },
          { left: "\\(", right: "\\)", display: false },
          { left: "$", right: "$", display: false }
        ],
        ignoredTags: ["script", "noscript", "style", "textarea", "pre", "code", "option"],
        throwOnError: false,
        strict: "ignore",
        trust: false
      });
    } catch (error) {
      return;
    }
  }

  function defaultState() {
    return {
      bookmarks: [],
      progress: Object.create(null),
      history: [],
      lastTopic: null
    };
  }

  function normalizeProgress(value) {
    if (!value || typeof value !== "object" || Array.isArray(value)) return {};
    const normalized = Object.create(null);
    Object.entries(value).forEach(([key, entry]) => {
      if (!entry || typeof entry !== "object") return;
      normalized[String(key)] = {
        attempted: Math.max(0, Number(entry.attempted) || 0),
        correct: Math.max(0, Number(entry.correct) || 0),
        lastAttempt: typeof entry.lastAttempt === "string" ? entry.lastAttempt : null
      };
    });
    return normalized;
  }

  function loadState() {
    const fallback = defaultState();
    try {
      const raw = sessionStorage.getItem(STORAGE_KEYS.state);
      if (!raw) return fallback;
      const parsed = JSON.parse(raw);
      return {
        bookmarks: Array.isArray(parsed.bookmarks)
          ? [...new Set(parsed.bookmarks.filter((item) => typeof item === "string"))]
          : [],
        progress: normalizeProgress(parsed.progress),
        history: Array.isArray(parsed.history)
          ? parsed.history.filter((item) => item && typeof item === "object").slice(0, 40)
          : [],
        lastTopic: parsed.lastTopic && typeof parsed.lastTopic === "object" && typeof parsed.lastTopic.id === "string"
          ? parsed.lastTopic
          : null
      };
    } catch (error) {
      return fallback;
    }
  }

  function saveState() {
    try {
      sessionStorage.setItem(STORAGE_KEYS.state, JSON.stringify(state));
    } catch (error) {
      toast("Session progress could not be saved.", "error");
    }
  }

  function isBookmarked(topicId) {
    return state.bookmarks.includes(topicId);
  }

  function toggleBookmark(topicId) {
    if (!topicId) return false;
    if (isBookmarked(topicId)) {
      state.bookmarks = state.bookmarks.filter((item) => item !== topicId);
      saveState();
      return false;
    }
    state.bookmarks = [topicId, ...state.bookmarks];
    saveState();
    return true;
  }

  function recordAnswer(topicId, correct) {
    const key = topicId || "unknown";
    const current = state.progress[key] || { attempted: 0, correct: 0, lastAttempt: null };
    current.attempted += 1;
    if (correct) current.correct += 1;
    current.lastAttempt = new Date().toISOString();
    state.progress[key] = current;
    saveState();
  }

  function recordQuizHistory(session) {
    if (!session || session.historyRecorded) return;
    session.historyRecorded = true;
    state.history = [{
      label: session.config.modeLabel || "Practice",
      topicId: session.config.topicId || "",
      topicName: session.config.topicName || "",
      attempted: session.attempted,
      correct: session.score,
      total: session.questions.length,
      completedAt: new Date().toISOString()
    }, ...state.history].slice(0, 40);
    saveState();
  }

  function resetProgress() {
    state.progress = Object.create(null);
    state.history = [];
    saveState();
  }

  function clearBookmarks() {
    state.bookmarks = [];
    saveState();
  }

  function resetLearningState() {
    state = defaultState();
    saveState();
  }

  function loadSession() {
    try {
      const raw = sessionStorage.getItem(STORAGE_KEYS.session);
      if (!raw) return null;
      const parsed = JSON.parse(raw);
      if (!parsed || typeof parsed.apiKey !== "string" || !parsed.apiKey) return null;
      return {
        username: typeof parsed.username === "string" ? parsed.username : DEMO_IDENTITY.username,
        email: typeof parsed.email === "string" ? parsed.email : DEMO_IDENTITY.email,
        apiKey: parsed.apiKey,
        expiry: typeof parsed.expiry === "string" ? parsed.expiry : "",
        savedAt: typeof parsed.savedAt === "string" ? parsed.savedAt : null
      };
    } catch (error) {
      return null;
    }
  }

  function saveSession(session) {
    try {
      sessionStorage.setItem(STORAGE_KEYS.session, JSON.stringify(session));
    } catch (error) {
      toast("The demo session could not be stored.", "error");
    }
  }

  function clearSession() {
    app.session = null;
    app.authenticated = false;
    try {
      sessionStorage.removeItem(STORAGE_KEYS.session);
    } catch (error) {
      return;
    }
  }

  class ApiError extends Error {
    constructor(message, options = {}) {
      super(message);
      this.name = "ApiError";
      this.status = Number(options.status) || 0;
      this.detail = options.detail || message;
      this.data = options.data || null;
    }
  }

  function setApiStatus(kind, text) {
    const pill = document.getElementById("api-status");
    const label = document.getElementById("api-status-text");
    if (kind === "online") app.online = true;
    else if (kind === "offline") app.online = false;
    if (!pill || !label) return;
    pill.classList.remove("is-online", "is-offline", "is-checking");
    if (kind) pill.classList.add(`is-${kind}`);
    label.textContent = text;
    pill.title = text;
  }

  function setLoadingMessage(text) {
    const message = document.getElementById("loading-message");
    if (message && text) message.textContent = text;
  }

  function hideLoadingScreen() {
    const screen = document.getElementById("loading-screen");
    if (screen) screen.classList.add("is-hidden");
  }

  function updateSessionUI() {
    const session = app.session;
    const username = document.getElementById("session-username");
    const expiry = document.getElementById("session-expiry");
    const key = document.getElementById("session-key");
    const avatar = document.getElementById("session-avatar");
    if (username) username.textContent = session?.username || DEMO_IDENTITY.username;
    if (avatar) avatar.textContent = initials(session?.username || DEMO_IDENTITY.username);
    if (expiry) {
      if (!session) {
        expiry.textContent = "Not connected";
      } else if (sessionIsExpired(session)) {
        expiry.textContent = "Session expired";
      } else {
        const expiresAt = sessionExpiryMs(session);
        expiry.textContent = expiresAt ? `Expires ${formatDate(expiresAt)}` : "Session active";
      }
    }
    if (key) key.textContent = session ? maskKey(session.apiKey) : "Not available";
  }

  function apiErrorMessage(data, status) {
    const detail = data?.detail;
    if (Array.isArray(detail)) {
      return detail.map((item) => item?.msg || String(item)).join("; ");
    }
    if (typeof detail === "string" && detail.trim()) return detail;
    if (typeof data?.message === "string" && data.message.trim()) return data.message;
    if (status === 401) return "The demo API key was rejected.";
    if (status === 404) return "The requested item was not found.";
    if (status === 429) return "The hourly MathAPI rate limit was reached.";
    if (status === 503) return "MathAPI could not reach its database.";
    return status ? `MathAPI returned an error (${status}).` : "MathAPI is not reachable.";
  }

  async function request(path, options = {}) {
    const {
      method = "GET",
      body,
      auth = true,
      timeout = 25000,
      retry = true
    } = options;
    const controller = new AbortController();
    const timer = window.setTimeout(() => controller.abort(), timeout);
    const headers = { Accept: "application/json" };
    if (body !== undefined) headers["Content-Type"] = "application/json";
    if (auth && app.session?.apiKey) headers["X-API-Key"] = app.session.apiKey;
    let response;
    try {
      response = await fetch(`${API_BASE}${path}`, {
        method,
        headers,
        body: body === undefined ? undefined : JSON.stringify(body),
        signal: controller.signal
      });
    } catch (error) {
      if (error.name === "AbortError") {
        setApiStatus("offline", "API timed out");
        throw new ApiError("MathAPI did not respond in time.", { status: 0 });
      }
      setApiStatus("offline", "API offline");
      throw new ApiError("MathAPI is not reachable on 127.0.0.1:3000.", { status: 0 });
    } finally {
      window.clearTimeout(timer);
    }

    const raw = await response.text();
    let data = null;
    if (raw) {
      try {
        data = JSON.parse(raw);
      } catch (error) {
        if (response.ok) {
          throw new ApiError("MathAPI returned an unreadable response.", {
            status: response.status,
            data
          });
        }
      }
    }

    if (!response.ok) {
      const detail = apiErrorMessage(data, response.status);
      if (response.status === 401 && auth && retry) {
        try {
          await authenticate({ force: true });
          return request(path, { ...options, retry: false });
        } catch (error) {
          throw new ApiError("The demo session could not be renewed.", {
            status: 401,
            detail: "The demo session could not be renewed."
          });
        }
      }
      if (response.status === 429) setApiStatus("checking", "Rate limited");
      else if (response.status === 503) setApiStatus("offline", "Database offline");
      else if (response.status >= 500) setApiStatus("offline", "API unavailable");
      throw new ApiError(detail, {
        status: response.status,
        detail,
        data
      });
    }

    setApiStatus("online", "API online");
    return data;
  }

  async function checkHealth(options = {}) {
    const timeout = options.timeout || 6000;
    const controller = new AbortController();
    const timer = window.setTimeout(() => controller.abort(), timeout);
    setApiStatus("checking", "Checking API");
    try {
      const response = await fetch(`${API_BASE}/`, {
        headers: { Accept: "application/json" },
        signal: controller.signal
      });
      if (!response.ok) {
        throw new ApiError(`Health check failed (${response.status}).`, {
          status: response.status
        });
      }
      const data = await response.json();
      app.health = data;
      app.healthAt = Date.now();
      setApiStatus("online", "API online");
      return data;
    } catch (error) {
      app.health = null;
      app.healthAt = Date.now();
      setApiStatus("offline", "API offline");
      if (error instanceof ApiError) throw error;
      throw new ApiError("MathAPI is not reachable on 127.0.0.1:3000.", { status: 0 });
    } finally {
      window.clearTimeout(timer);
    }
  }

  async function authenticate(options = {}) {
    const force = Boolean(options.force);
    if (app.authPromise) return app.authPromise;
    if (!force) {
      const existing = loadSession();
      if (existing && !sessionIsExpired(existing)) {
        app.session = existing;
        app.authenticated = true;
        updateSessionUI();
        return existing;
      }
    }

    app.authPromise = (async () => {
      setLoadingMessage("Registering the demo session…");
      const data = await request("/auth", {
        method: "POST",
        body: DEMO_IDENTITY,
        auth: false,
        retry: false,
        timeout: 12000
      });
      const keyData = data?.api_key_data;
      if (!keyData?.api_key) {
        throw new ApiError("MathAPI did not return a demo API key.", { status: 0 });
      }
      const session = {
        username: keyData.username || DEMO_IDENTITY.username,
        email: DEMO_IDENTITY.email,
        apiKey: keyData.api_key,
        expiry: keyData.expiry || "",
        savedAt: new Date().toISOString()
      };
      app.session = session;
      app.authenticated = true;
      saveSession(session);
      updateSessionUI();
      return session;
    })().finally(() => {
      app.authPromise = null;
    });

    return app.authPromise;
  }

  async function refreshSession(options = {}) {
    const session = await authenticate({ force: true });
    if (options.notify !== false) toast("Demo session refreshed.", "success");
    return session;
  }

  async function fetchData(path, params = {}, cacheType = null) {
    const query = new URLSearchParams();
    Object.entries(params).forEach(([key, value]) => {
      if (value !== undefined && value !== null && value !== "") {
        query.set(key, String(value));
      }
    });
    const suffix = query.toString() ? `?${query.toString()}` : "";
    const key = `${path}${suffix}`;
    const ttl = cacheType ? CACHE_TTL[cacheType] || 0 : 0;
    if (ttl) {
      const cached = app.cache.get(key);
      if (cached && cached.expires > Date.now()) return cached.value;
    }
    if (app.inflight.has(key)) return app.inflight.get(key);
    const promise = request(key)
      .then((data) => {
        if (ttl) app.cache.set(key, { value: data, expires: Date.now() + ttl });
        return data;
      })
      .finally(() => {
        app.inflight.delete(key);
      });
    app.inflight.set(key, promise);
    return promise;
  }

  async function getTopics() {
    const data = await fetchData("/api/v1/topics", {}, "topics");
    app.topics = Array.isArray(data?.topics) ? data.topics : [];
    return data && typeof data === "object"
      ? { ...data, topics: app.topics }
      : { topics: app.topics };
  }

  function getTopicName(topicId) {
    return app.topics.find((topic) => topic.topic_id === topicId)?.topic_name || topicId || "Mathematics";
  }

  function isNotFound(error) {
    return error instanceof ApiError && error.status === 404;
  }

  function clearCache() {
    app.cache.clear();
  }

  function toast(message, type = "info") {
    const stack = document.getElementById("toast-stack");
    if (!stack) return;
    const toastId = `toast-${++toastSequence}`;
    const iconName = type === "success" ? "check-circle" : type === "error" ? "alert" : "sparkles";
    const element = document.createElement("div");
    element.className = `toast${type === "success" ? " is-success" : type === "error" ? " is-error" : ""}`;
    element.id = toastId;
    element.innerHTML = `${icon(iconName)}<span>${escapeHtml(message)}</span>`;
    element.addEventListener("click", () => element.remove());
    stack.appendChild(element);
    while (stack.children.length > 4) stack.firstElementChild.remove();
    window.setTimeout(() => element.remove(), type === "error" ? 6500 : 4200);
  }

  function openModal(options = {}) {
    const root = document.getElementById("modal-root");
    if (!root) return Promise.resolve(false);
    if (modalResolve) {
      const previousResolve = modalResolve;
      modalResolve = null;
      previousResolve(false);
    }
    const title = options.title || "Are you sure?";
    const message = options.message || "";
    const confirmLabel = options.confirmLabel || "Confirm";
    const cancelLabel = options.cancelLabel || "Cancel";
    const danger = Boolean(options.danger);
    root.innerHTML = `
      <div class="modal" role="dialog" aria-modal="true" aria-labelledby="modal-title" aria-describedby="modal-copy">
        <h3 id="modal-title">${escapeHtml(title)}</h3>
        <p id="modal-copy">${escapeHtml(message)}</p>
        <div class="modal-actions">
          <button class="btn btn-ghost" type="button" data-modal-cancel>${escapeHtml(cancelLabel)}</button>
          <button class="btn ${danger ? "btn-danger" : "btn-primary"}" type="button" data-modal-confirm>${escapeHtml(confirmLabel)}</button>
        </div>
      </div>`;
    root.classList.add("is-open");
    document.body.style.overflow = "hidden";
    const cancel = root.querySelector("[data-modal-cancel]");
    if (cancel) cancel.focus();
    return new Promise((resolve) => {
      modalResolve = resolve;
    });
  }

  function closeModal(value) {
    const root = document.getElementById("modal-root");
    if (!root) return;
    root.classList.remove("is-open");
    root.innerHTML = "";
    const sidebarOpen = document.getElementById("sidebar")?.classList.contains("is-open");
    document.body.style.overflow = sidebarOpen ? "hidden" : "";
    const resolve = modalResolve;
    modalResolve = null;
    if (resolve) resolve(Boolean(value));
  }

  function applyTheme(theme, persist = true) {
    const next = theme === "light" ? "light" : "dark";
    document.documentElement.dataset.theme = next;
    const toggle = document.getElementById("theme-toggle");
    if (toggle) {
      const isLight = next === "light";
      toggle.setAttribute("aria-label", isLight ? "Switch to dark theme" : "Switch to light theme");
      toggle.setAttribute("aria-pressed", String(isLight));
    }
    const meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.setAttribute("content", next === "light" ? "#fff8ef" : "#171513");
    if (persist) {
      try {
        localStorage.setItem(STORAGE_KEYS.theme, next);
      } catch (error) {
        return next;
      }
    }
    return next;
  }

  function toggleTheme() {
    const next = document.documentElement.dataset.theme === "light" ? "dark" : "light";
    applyTheme(next);
    toast(`${next === "light" ? "Light" : "Dark"} theme enabled.`, "success");
  }

  function setSidebarOpen(open) {
    const sidebar = document.getElementById("sidebar");
    const button = document.getElementById("menu-toggle");
    sidebar?.classList.toggle("is-open", open);
    button?.setAttribute("aria-expanded", String(open));
    if (open) {
      document.body.style.overflow = "hidden";
    } else {
      document.body.style.overflow = modalResolve ? "hidden" : "";
    }
  }

  function closeSidebar() {
    setSidebarOpen(false);
  }

  function onViewportResize() {
    if (window.innerWidth <= 980) return;
    const sidebar = document.getElementById("sidebar");
    if (sidebar?.classList.contains("is-open")) closeSidebar();
  }

  function updateChrome(route, override = {}) {
    const base = ROUTES[route.name] || ROUTES.dashboard;
    const meta = { ...base };
    Object.entries(override).forEach(([key, value]) => {
      if (value !== undefined) meta[key] = value;
    });
    const title = document.getElementById("page-title");
    const eyebrow = document.getElementById("page-eyebrow");
    if (title) title.textContent = meta.title;
    if (eyebrow) eyebrow.textContent = meta.eyebrow;
    document.title = `${meta.title} · MathLabs`;
    const active = route.name === "topic" ? "topics" : route.name;
    document.querySelectorAll(".nav-link[data-route]").forEach((link) => {
      const isActive = link.dataset.route === active;
      link.classList.toggle("is-active", isActive);
      if (isActive) link.setAttribute("aria-current", "page");
      else link.removeAttribute("aria-current");
    });
  }

  function pageHead(options = {}) {
    return `
      <section class="page-head">
        <div class="page-head-copy">
          <span class="eyebrow">${escapeHtml(options.eyebrow || "MathLabs")}</span>
          <h2>${escapeHtml(options.title || "")}</h2>
          ${options.text ? `<p class="lede">${escapeHtml(options.text)}</p>` : ""}
        </div>
        ${options.actions ? `<div class="page-actions">${options.actions}</div>` : ""}
      </section>`;
  }

  function routeSkeleton() {
    return `
      <div class="page-loading">
        <div class="skeleton skeleton-line skeleton-short"></div>
        <div class="skeleton skeleton-title"></div>
        <div class="skeleton skeleton-line"></div>
        <div class="skeleton-grid">
          <div class="skeleton-card"><div class="skeleton skeleton-line skeleton-title"></div><div class="skeleton skeleton-line"></div><div class="skeleton skeleton-line skeleton-short"></div></div>
          <div class="skeleton-card"><div class="skeleton skeleton-line skeleton-title"></div><div class="skeleton skeleton-line"></div><div class="skeleton skeleton-line skeleton-short"></div></div>
          <div class="skeleton-card"><div class="skeleton skeleton-line skeleton-title"></div><div class="skeleton skeleton-line"></div><div class="skeleton skeleton-line skeleton-short"></div></div>
        </div>
      </div>`;
  }

  function miniSkeleton() {
    return `
      <div class="page-loading">
        <div class="skeleton skeleton-title"></div>
        <div class="skeleton skeleton-line"></div>
        <div class="skeleton skeleton-line"></div>
        <div class="skeleton skeleton-line skeleton-short"></div>
      </div>`;
  }

  function emptyState(options = {}) {
    return `
      <div class="empty-state">
        <span class="empty-icon">${icon(options.iconName || "sparkles")}</span>
        <h3>${escapeHtml(options.title || "Nothing here yet")}</h3>
        <p>${escapeHtml(options.text || "")}</p>
        ${options.action || ""}
      </div>`;
  }

  function errorState(error, options = {}) {
    const status = error instanceof ApiError ? error.status : 0;
    const message = error instanceof Error ? error.message : String(error || "Something went wrong.");
    const extra = status === 0
      ? "Start the API with uv run uvs dev, then try again."
      : status === 429
        ? "MathAPI allows 100 authenticated requests per hour and 300 per IP. Try again later."
        : "";
    const action = options.action || "retry-route";
    const label = options.actionLabel || "Try again";
    return `
      <div class="error-state">
        <span class="error-icon">${icon("alert")}</span>
        <h3>${escapeHtml(options.title || "This section could not load")}</h3>
        <p>${escapeHtml(message)}</p>
        ${extra ? `<p class="muted">${escapeHtml(extra)}</p>` : ""}
        ${status ? `<code class="error-code">MathAPI status ${status}</code>` : ""}
        <button class="btn btn-primary" type="button" data-action="${escapeHtml(action)}">${escapeHtml(label)}</button>
      </div>`;
  }

  function bookmarkButton(topicId) {
    const saved = isBookmarked(topicId);
    return `
      <button class="bookmark-btn${saved ? " is-saved" : ""}" type="button"
        data-action="toggle-bookmark" data-topic-id="${escapeHtml(topicId)}"
        aria-label="${saved ? "Remove bookmark" : "Save topic"}" aria-pressed="${saved}">
        ${icon("bookmark")}
      </button>`;
  }

  function syncBookmarkButtons(topicId) {
    const saved = isBookmarked(topicId);
    document.querySelectorAll('[data-action="toggle-bookmark"]').forEach((button) => {
      if (button.dataset.topicId !== topicId) return;
      button.classList.toggle("is-saved", saved);
      button.setAttribute("aria-pressed", String(saved));
      button.setAttribute("aria-label", saved ? "Remove bookmark" : "Save topic");
    });
  }

  function resourceRow(topic) {
    return `
      <div class="resource-row">
        <span class="resource">${icon("file-text")}${Number(topic.examples_available) || 0}</span>
        <span class="resource">${icon("target")}${Number(topic.questions_available) || 0}</span>
        <span class="resource">${icon("formula")}${Number(topic.formulae_available) || 0}</span>
        <span class="resource">${icon("link")}${Number(topic.sources_available) || 0}</span>
      </div>`;
  }

  function topicCard(topic) {
    const topics = Array.isArray(topic.sub_topics) ? topic.sub_topics.slice(0, 3) : [];
    const topicHref = `#/topic/${encodeURIComponent(topic.topic_id)}/explanation`;
    return `
      <article class="topic-card" data-topic-id="${escapeHtml(topic.topic_id)}">
        <div class="topic-card-top">
          <h3 class="topic-title"><a href="${topicHref}">${escapeHtml(topic.topic_name)}</a></h3>
          ${bookmarkButton(topic.topic_id)}
        </div>
        <p class="topic-id">${escapeHtml(topic.topic_id)}</p>
        <p>${topics.length ? escapeHtml(topics.join(" · ")) : escapeHtml((topic.prerequisites || []).length ? `Prerequisites: ${topic.prerequisites.join(", ")}` : "A focused topic in the MathAPI catalog.")}</p>
        <div class="chip-row">
          ${(topic.branch || []).map((branch) => `<span class="chip">${escapeHtml(branch)}</span>`).join("")}
          ${difficultyChip(topic.difficulty)}
        </div>
        <div class="topic-card-footer">
          ${resourceRow(topic)}
          <a class="btn btn-soft btn-sm" href="${topicHref}">Open ${icon("arrow-right")}</a>
        </div>
      </article>`;
  }

  function formulaCard(formula) {
    const raw = normalizeLatex(formula?.code);
    return `
      <article class="formula-card">
        <div class="formula-card-head">
          <h4>${escapeHtml(formula?.title || "Formula")}</h4>
          <button class="btn btn-ghost btn-sm" type="button" data-action="copy-formula">${icon("copy")} Copy</button>
        </div>
        <div class="formula">${mathBlock(formula?.code)}</div>
        <span data-latex hidden>${escapeHtml(raw)}</span>
      </article>`;
  }

  function sourceCard(source) {
    const type = String(source?.type || "Resource");
    return `
      <article class="source-card">
        <span class="chip chip-orange">${escapeHtml(type)}</span>
        <h4>${escapeHtml(source?.title || "Learning source")}</h4>
        <p>${escapeHtml(source?.link || "")}</p>
        ${externalLink(source?.link, "Open source", "source-link")}
      </article>`;
  }

  function detailSection(title, body) {
    return `
      <section class="detail-section">
        <h3>${escapeHtml(title)}</h3>
        ${body}
      </section>`;
  }

  function createQuiz(questions, config = {}) {
    const list = Array.isArray(questions)
      ? questions.filter((question) => question && typeof question.question === "string")
      : [];
    return {
      questions: list,
      index: 0,
      selected: null,
      revealed: false,
      showHint: false,
      score: 0,
      attempted: 0,
      completed: false,
      historyRecorded: false,
      config: {
        mode: "practice",
        kicker: "Practice",
        modeLabel: "Practice",
        topicId: "",
        topicName: "",
        ...config
      }
    };
  }

  function quizResultActions(session) {
    const mode = session.config.mode;
    if (mode === "practice") {
      return `
        <button class="btn btn-primary" type="button" data-action="practice-restart">${icon("rotate")} New practice set</button>
        <a class="btn btn-secondary" href="#/topics">Explore topics</a>`;
    }
    if (mode === "random") {
      return `
        <button class="btn btn-primary" type="button" data-action="random-new">${icon("shuffle")} Another question</button>
        <a class="btn btn-secondary" href="#/practice">Practice Arena</a>`;
    }
    if (mode === "daily") {
      return `
        <a class="btn btn-primary" href="#/random">${icon("shuffle")} Try a random question</a>
        <button class="btn btn-secondary" type="button" data-action="retry-route">${icon("refresh")} Refresh challenge</button>`;
    }
    const topicLink = session.config.topicId
      ? `#/topic/${encodeURIComponent(session.config.topicId)}/${safeTopicTab(session.config.returnTab)}`
      : "#/practice";
    return `
      <a class="btn btn-primary" href="#/practice">${icon("target")} Practice Arena</a>
      <a class="btn btn-secondary" href="${topicLink}">${icon("arrow-left")} Back to topic</a>`;
  }

  function renderQuizResult(session) {
    const attempted = session.attempted;
    const percent = attempted ? Math.round((session.score / attempted) * 100) : 0;
    const heading = percent === 100
      ? "Flawless work."
      : percent >= 80
        ? "Strong finish."
        : percent >= 60
          ? "Good progress."
          : "Keep building.";
    return `
      <div class="quiz-result">
        <div class="score-ring">${percent}%<span>accuracy</span></div>
        <h3>${heading}</h3>
        <p>You answered ${session.score} of ${attempted} attempted questions correctly.</p>
        <div class="quiz-actions">${quizResultActions(session)}</div>
      </div>`;
  }

  function renderQuizQuestion(session) {
    const question = session.questions[session.index];
    const options = question.options && typeof question.options === "object"
      ? Object.keys(question.options).sort()
      : [];
    const types = Array.isArray(question.question_type) ? question.question_type : [];
    const topicName = getTopicName(question.topic_id || session.config.topicId);
    const percent = Math.round(((session.index + 1) / session.questions.length) * 100);
    const selected = session.selected;
    const optionMarkup = options.map((key) => {
      let className = "option-btn";
      if (session.revealed) {
        if (key === question.answer) className += " is-correct";
        else if (key === selected) className += " is-wrong";
      } else if (key === selected) {
        className += " is-selected";
      }
      return `
        <button class="${className}" type="button" data-action="quiz-option" data-option="${escapeHtml(key)}"
          ${session.revealed ? "disabled" : ""} aria-pressed="${key === selected}">
          <span class="option-letter">${escapeHtml(key)}</span>
          <span class="option-text">${escapeHtml(question.options[key]).replace(/\n/g, "<br>")}</span>
        </button>`;
    }).join("");
    const correctOption = question.options?.[question.answer];
    const sources = Array.isArray(question.solution_sources) ? question.solution_sources : [];
    const feedback = session.revealed
      ? `<div class="quiz-feedback ${selected === question.answer ? "is-success" : "is-error"}">
          <strong>${selected === question.answer ? "Correct." : "Not quite."}</strong>
          <span>${selected === question.answer
            ? "The selected option is correct."
            : `The correct answer is ${escapeHtml(question.answer)}${correctOption ? ` — ${escapeHtml(correctOption)}` : ""}.`}</span>
          ${sources.length ? `<ul class="source-list">
            ${sources.map((source) => `<li>${externalLink(source.link, source.source || source.type || "Solution source")}</li>`).join("")}
          </ul>` : ""}
        </div>`
      : "";
    return `
      <div class="quiz-top">
        <span class="quiz-kicker">${escapeHtml(session.config.kicker)}</span>
        <span class="quiz-counter">Question ${session.index + 1} of ${session.questions.length}</span>
      </div>
      <div class="progress-bar"><div class="progress-fill" style="width: ${percent}%"></div></div>
      <div class="quiz-meta">
        <span class="chip chip-orange">${escapeHtml(topicName)}</span>
        ${difficultyChip(question.difficulty)}
        ${typeChips(types)}
        ${question.expected_time_limit ? `<span class="chip">${icon("clock")} ${escapeHtml(question.expected_time_limit)}</span>` : ""}
      </div>
      <h3 class="quiz-question">${escapeHtml(question.question).replace(/\n/g, "<br>")}</h3>
      <div class="options-grid">${optionMarkup}</div>
      ${question.hint && !session.showHint ? `<div class="quiz-actions"><button class="btn btn-ghost btn-sm" type="button" data-action="quiz-hint">${icon("lightbulb")} Show hint</button></div>` : ""}
      ${question.hint && session.showHint ? `<div class="observation"><strong>Hint</strong>${escapeHtml(question.hint).replace(/\n/g, "<br>")}</div>` : ""}
      ${feedback}
      <div class="quiz-actions">
        ${session.revealed
          ? `<button class="btn btn-primary" type="button" data-action="quiz-next">
              ${session.index + 1 >= session.questions.length ? "See results" : "Next question"} ${icon("arrow-right")}
            </button>`
          : `<button class="btn btn-primary" type="button" data-action="quiz-check" ${session.selected ? "" : "disabled"}>
              Check answer ${icon("check")}
            </button>`}
      </div>`;
  }

  function renderQuizInner(session) {
    if (!session || !session.questions.length) {
      return emptyState({
        title: "No questions available",
        text: "This selection does not have any questions yet.",
        iconName: "target"
      });
    }
    if (session.completed) return renderQuizResult(session);
    return renderQuizQuestion(session);
  }

  function renderQuizShell(session) {
    return `<div class="quiz-shell" id="quiz-container">${renderQuizInner(session)}</div>`;
  }

  function mountQuiz(container, session) {
    if (!container) return;
    quizSession = session;
    container.innerHTML = renderQuizShell(session);
    hydrateIcons(container);
    renderMath(container);
  }

  function updateQuizView(session) {
    const container = document.getElementById("quiz-container");
    if (!container || !session) return;
    container.innerHTML = renderQuizInner(session);
    hydrateIcons(container);
    renderMath(container);
  }

  function finalizeQuiz(session) {
    recordQuizHistory(session);
    if (session.config.topicId && session.config.topicName) {
      state.lastTopic = {
        id: session.config.topicId,
        name: session.config.topicName,
        tab: safeTopicTab(session.config.returnTab)
      };
      saveState();
    }
  }

  function handleQuizAction(action, element) {
    if (!quizSession) return;
    const session = quizSession;
    if (action === "quiz-option" && !session.revealed && !session.completed) {
      session.selected = element.dataset.option || null;
      updateQuizView(session);
      return;
    }
    if (action === "quiz-hint" && !session.completed) {
      session.showHint = true;
      updateQuizView(session);
      return;
    }
    if (action === "quiz-check" && !session.revealed && !session.completed) {
      const question = session.questions[session.index];
      if (!question || !session.selected) return;
      session.revealed = true;
      session.attempted += 1;
      const correct = session.selected === question.answer;
      if (correct) session.score += 1;
      recordAnswer(question.topic_id || session.config.topicId, correct);
      updateQuizView(session);
      return;
    }
    if (action === "quiz-next" && session.revealed && !session.completed) {
      if (session.index + 1 >= session.questions.length) {
        session.completed = true;
        finalizeQuiz(session);
      } else {
        session.index += 1;
        session.selected = null;
        session.revealed = false;
        session.showHint = false;
      }
      updateQuizView(session);
    }
  }

  function statCard(iconName, value, label) {
    return `
      <article class="stat-card">
        <span class="stat-icon">${icon(iconName)}</span>
        <div>
          <span class="stat-value">${escapeHtml(value)}</span>
          <span class="stat-label">${escapeHtml(label)}</span>
        </div>
      </article>`;
  }

  function selectedAttr(value, current) {
    return value === current ? " selected" : "";
  }

  function topicResourceTotal(topic) {
    return (Number(topic.formulae_available) || 0)
      + (Number(topic.examples_available) || 0)
      + (Number(topic.questions_available) || 0)
      + (Number(topic.sources_available) || 0);
  }

  function filteredTopics() {
    const query = ui.topicSearch.trim().toLowerCase();
    const difficultyOrder = { Beginner: 0, Intermediate: 1, Advanced: 2 };
    const list = app.topics.filter((topic) => {
      if (ui.topicBranch && !(topic.branch || []).includes(ui.topicBranch)) return false;
      if (ui.topicDifficulty && topic.difficulty !== ui.topicDifficulty) return false;
      if (!query) return true;
      return [
        topic.topic_id,
        topic.topic_name,
        topic.difficulty,
        ...(topic.branch || []),
        ...(topic.sub_topics || []),
        ...(topic.prerequisites || [])
      ].join(" ").toLowerCase().includes(query);
    });
    return list.sort((left, right) => {
      if (ui.topicSort === "resources") return topicResourceTotal(right) - topicResourceTotal(left);
      if (ui.topicSort === "difficulty") {
        return (difficultyOrder[left.difficulty] ?? 9) - (difficultyOrder[right.difficulty] ?? 9);
      }
      return left.topic_name.localeCompare(right.topic_name);
    });
  }

  function topicResultsMarkup() {
    const topics = filteredTopics();
    if (!topics.length) {
      return emptyState({
        title: "No topics match those filters",
        text: "Try a broader search or clear the branch and difficulty filters.",
        iconName: "search",
        action: '<button class="btn btn-secondary" type="button" data-action="clear-topic-filters">Clear filters</button>'
      });
    }
    return `<div class="topic-grid">${topics.map(topicCard).join("")}</div>`;
  }

  function refreshTopicResults() {
    const results = document.getElementById("topic-results");
    const count = document.getElementById("topic-result-count");
    if (!results) return;
    const topics = filteredTopics();
    results.innerHTML = topicResultsMarkup();
    if (count) count.textContent = `${topics.length} of ${app.topics.length} topics`;
    hydrateIcons(results);
    renderMath(results);
  }

  async function viewDashboard(route, sequence) {
    const data = await getTopics();
    if (sequence !== renderSequence) return null;
    const topics = data.topics || [];
    if (!topics.length) {
      return {
        html: pageHead({
          eyebrow: "Workspace",
          title: "Your local mathematics workspace",
          text: "No topics were returned by MathAPI."
        }) + emptyState({
          title: "The catalog is empty",
          text: "Add topic data to the local MathAPI database, then refresh.",
          iconName: "book-open"
        })
      };
    }
    const branchCounts = new Map(BRANCHES.map((branch) => [branch, 0]));
    topics.forEach((topic) => {
      (topic.branch || []).forEach((branch) => {
        branchCounts.set(branch, (branchCounts.get(branch) || 0) + 1);
      });
    });
    const totalResources = topics.reduce((sum, topic) => sum + topicResourceTotal(topic), 0);
    const totalQuestions = topics.reduce((sum, topic) => sum + (Number(topic.questions_available) || 0), 0);
    const last = state.lastTopic && topics.find((topic) => topic.topic_id === state.lastTopic.id);
    const savedTopics = state.bookmarks
      .map((topicId) => topics.find((topic) => topic.topic_id === topicId))
      .filter(Boolean)
      .slice(0, 3);
    const continueMarkup = last
      ? `<div class="continue-card">
          <div>
            <span class="eyebrow">Last opened</span>
            <h3>${escapeHtml(last.topic_name)}</h3>
            <p>${escapeHtml(last.difficulty)} · ${escapeHtml((last.branch || [])[0] || "Mathematics")} · ${topicResourceTotal(last)} learning assets</p>
          </div>
          <a class="btn btn-primary btn-sm" href="#/topic/${encodeURIComponent(last.topic_id)}/${safeTopicTab(state.lastTopic.tab)}">Continue ${icon("arrow-right")}</a>
        </div>`
      : `<div class="continue-card">
          <div>
            <span class="eyebrow">First step</span>
            <h3>Pick a topic to begin</h3>
            <p>Browse the catalog, then follow explanations, examples, and practice questions.</p>
          </div>
          <a class="btn btn-primary btn-sm" href="#/topics">Explore topics ${icon("arrow-right")}</a>
        </div>`;
    const savedMarkup = savedTopics.length
      ? `<div class="topic-progress-list">
          ${savedTopics.map((topic) => `<div class="progress-row">
            <div><strong>${escapeHtml(topic.topic_name)}</strong><br><span>${escapeHtml((topic.branch || []).join(", ") || "Mathematics")}</span></div>
            <a class="btn btn-ghost btn-sm" href="#/topic/${encodeURIComponent(topic.topic_id)}/explanation">Open</a>
          </div>`).join("")}
        </div>`
      : `<p class="muted">Save topics with the bookmark button to keep a shortlist here.</p>`;
    const html = `
      <section class="hero">
        <div class="hero-copy">
          <span class="badge"><span class="badge-dot"></span>Local mathematics workspace</span>
          <h2>Build intuition, <span>one idea at a time.</span></h2>
          <p class="hero-text">MathLabs turns the local MathAPI catalog into a focused study space: explore concepts, work through examples, and check your understanding with guided practice.</p>
          <div class="hero-actions">
            <a class="btn btn-primary" href="#/topics">${icon("book-open")} Explore topics</a>
            <a class="btn btn-secondary" href="#/practice">${icon("target")} Start practicing</a>
          </div>
        </div>
        <div class="hero-visual" aria-hidden="true">
          <div class="formula-chip">${mathBlock("e^{i\\pi} + 1 = 0")}</div>
          <div class="formula-chip">${mathBlock("\\int_0^1 x^2\\,dx = \\frac{1}{3}")}</div>
          <div class="formula-chip">${mathBlock("\\binom{n}{k} = \\frac{n!}{k!(n-k)!}")}</div>
        </div>
      </section>
      <div class="stats-grid">
        ${statCard("book", topics.length, "Topics in the catalog")}
        ${statCard("layers", latestBranchCount(branchCounts), "Mathematics branches")}
        ${statCard("target", totalQuestions, "Practice questions")}
        ${statCard("file-text", totalResources, "Learning assets")}
      </div>
      <section class="section">
        <div class="dashboard-grid">
          <article class="panel daily-card">
            <span class="daily-date">${icon("calendar")} Daily ritual</span>
            <h3>Three problems. One shared challenge.</h3>
            <p>Beginner, intermediate, and advanced questions selected for today. Compare your reasoning with the solution sources when you are ready.</p>
            <a class="btn btn-primary" href="#/daily">${icon("sparkles")} Open daily challenge</a>
          </article>
          <article class="panel">
            <div class="panel-head">
              <div>
                <h3 class="panel-title">Continue learning</h3>
                <p class="panel-caption">Your session picks up where you left it.</p>
              </div>
            </div>
            ${continueMarkup}
          </article>
        </div>
      </section>
      <section class="section">
        <div class="section-head">
          <div>
            <h3 class="section-title">Explore by branch</h3>
            <p class="section-subtitle">Move from foundations to specialist territory.</p>
          </div>
          <a class="section-link" href="#/topics">All topics ${icon("arrow-right")}</a>
        </div>
        <div class="branch-grid">
          ${BRANCHES.map((branch) => `<a class="branch-card" href="#/topics?branch=${encodeURIComponent(branch)}">
            <strong>${escapeHtml(branch)}</strong>
            <span>${branchCounts.get(branch) || 0} topics</span>
          </a>`).join("")}
        </div>
      </section>
      <section class="section">
        <div class="section-head">
          <div>
            <h3 class="section-title">Your bookmarks</h3>
            <p class="section-subtitle">A short list of topics worth returning to.</p>
          </div>
          <a class="section-link" href="#/saved">Saved &amp; progress ${icon("arrow-right")}</a>
        </div>
        ${savedMarkup}
      </section>`;
    return {
      html,
      title: "Dashboard",
      eyebrow: "Workspace"
    };
  }

  function latestBranchCount(branchCounts) {
    return [...branchCounts.values()].filter((count) => count > 0).length;
  }

  async function viewTopics(route, sequence) {
    const data = await getTopics();
    if (sequence !== renderSequence) return null;
    const branchQuery = route.query.get("branch");
    ui.topicBranch = branchQuery && BRANCHES.includes(branchQuery) ? branchQuery : "";
    const list = filteredTopics();
    const html = `
      ${pageHead({
        eyebrow: "Library",
        title: "The whole map, minus the noise.",
        text: "Search by topic, branch, or prerequisite. Open a topic studio to read, work through examples, and practice.",
        actions: `<a class="btn btn-secondary" href="#/practice">${icon("target")} Practice Arena</a>`
      })}
      <div class="filter-bar">
        <label class="field field-grow">
          <span class="field-label">Search topics</span>
          <span class="search-field">
            <span class="search-icon">${icon("search")}</span>
            <input class="input" id="topic-search" type="search" value="${escapeHtml(ui.topicSearch)}" placeholder="Try algebra, proof, circle…" autocomplete="off">
          </span>
        </label>
        <label class="field">
          <span class="field-label">Branch</span>
          <select class="select" id="topic-branch">
            <option value="">All branches</option>
            ${BRANCHES.map((branch) => `<option value="${escapeHtml(branch)}"${selectedAttr(branch, ui.topicBranch)}>${escapeHtml(branch)}</option>`).join("")}
          </select>
        </label>
        <label class="field">
          <span class="field-label">Difficulty</span>
          <select class="select" id="topic-difficulty">
            <option value="">All levels</option>
            ${DIFFICULTIES.map((level) => `<option value="${escapeHtml(level)}"${selectedAttr(level, ui.topicDifficulty)}>${escapeHtml(level)}</option>`).join("")}
          </select>
        </label>
        <label class="field">
          <span class="field-label">Sort</span>
          <select class="select" id="topic-sort">
            <option value="name"${selectedAttr("name", ui.topicSort)}>Name A–Z</option>
            <option value="resources"${selectedAttr("resources", ui.topicSort)}>Most resources</option>
            <option value="difficulty"${selectedAttr("difficulty", ui.topicSort)}>Easiest first</option>
          </select>
        </label>
        <button class="btn btn-ghost" type="button" data-action="clear-topic-filters">${icon("x")} Clear</button>
      </div>
      <div class="section-head">
        <p class="result-count" id="topic-result-count">${list.length} of ${data.topics.length} topics</p>
      </div>
      <div id="topic-results">${topicResultsMarkup()}</div>`;
    return {
      html,
      title: "Explore Topics",
      eyebrow: "Library"
    };
  }

  async function viewTopic(route, sequence) {
    const data = await getTopics();
    if (sequence !== renderSequence) return null;
    const topicId = route.id;
    const topic = data.topics.find((item) => item.topic_id === topicId);
    if (!topic) {
      throw new ApiError("That topic is not available in the MathAPI catalog.", { status: 404 });
    }
    const tab = safeTopicTab(route.tab);
    state.lastTopic = { id: topic.topic_id, name: topic.topic_name, tab };
    saveState();
    const topicHref = (nextTab) => `#/topic/${encodeURIComponent(topic.topic_id)}/${nextTab}`;
    const html = `
      <section class="topic-hero">
        <nav class="breadcrumbs" aria-label="Breadcrumb">
          <a href="#/topics">Topics</a>
          ${icon("chevron-right")}
          <span>${escapeHtml(topic.topic_name)}</span>
        </nav>
        <div class="topic-hero-main">
          <div>
            <span class="eyebrow">${escapeHtml((topic.branch || [])[0] || "Mathematics")}</span>
            <h2>${escapeHtml(topic.topic_name)}</h2>
            <div class="topic-meta">
              ${difficultyChip(topic.difficulty)}
              ${(topic.branch || []).map((branch) => `<span class="chip">${escapeHtml(branch)}</span>`).join("")}
            </div>
          </div>
          ${bookmarkButton(topic.topic_id)}
        </div>
        <div class="topic-stats">
          <div class="topic-stat"><strong>${Number(topic.examples_available) || 0}</strong><span>Worked examples</span></div>
          <div class="topic-stat"><strong>${Number(topic.questions_available) || 0}</strong><span>Practice questions</span></div>
          <div class="topic-stat"><strong>${Number(topic.formulae_available) || 0}</strong><span>Formulae</span></div>
          <div class="topic-stat"><strong>${Number(topic.sources_available) || 0}</strong><span>Learning sources</span></div>
        </div>
        <div class="topic-hero-actions">
          <a class="btn btn-primary" href="${topicHref("questions")}">${icon("target")} Practice questions</a>
          <a class="btn btn-secondary" href="${topicHref("formulae")}">${icon("formula")} Formula sheet</a>
          <a class="btn btn-ghost" href="${topicHref("sources")}">${icon("link")} Sources</a>
        </div>
      </section>
      <nav class="tabs" aria-label="Topic sections">
        ${TOPIC_TABS.map((item) => `<a class="tab${item === tab ? " is-active" : ""}" href="${topicHref(item)}"${item === tab ? ' aria-current="page"' : ""}>${escapeHtml(item[0].toUpperCase() + item.slice(1))}</a>`).join("")}
      </nav>
      <div id="topic-tab-content">${miniSkeleton()}</div>`;
    return {
      html,
      title: topic.topic_name,
      eyebrow: (topic.branch || [])[0] || "Topic studio",
      after: () => loadTopicTab(topic, tab, sequence)
    };
  }

  function topicReference(value) {
    const topic = app.topics.find((item) => item.topic_id === value || item.topic_name === value);
    if (topic) {
      return `<a class="chip chip-orange" href="#/topic/${encodeURIComponent(topic.topic_id)}/explanation">${escapeHtml(value)}</a>`;
    }
    return `<span class="chip">${escapeHtml(value)}</span>`;
  }

  function explanationTabMarkup(explanation, topic) {
    const sections = Array.isArray(explanation.explanation) ? explanation.explanation : [];
    const applications = Array.isArray(explanation.applications) ? explanation.applications : [];
    const prerequisites = Array.isArray(topic.prerequisites) ? topic.prerequisites : [];
    const related = Array.isArray(topic.related_topics) ? topic.related_topics : [];
    return `
      ${detailSection("Definition", `<div class="prose">${prose(explanation.definition) || '<p class="muted">No definition supplied.</p>'}</div>`)}
      ${explanation.origin ? detailSection("Origin", `<div class="prose">${prose(explanation.origin)}</div>`) : ""}
      ${applications.length ? detailSection("Real-world applications", `<ul class="application-list">${applications.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ul>`) : ""}
      ${sections.length ? detailSection("How it works", `<div class="explanation-list">${sections.map((section) => `<article class="explanation-block"><h4>${escapeHtml(section.title)}</h4><div class="prose">${prose(section.content)}</div></article>`).join("")}</div>`) : ""}
      ${prerequisites.length || related.length ? `<div class="settings-grid">
        ${prerequisites.length ? `<div class="info-card"><h3>Prerequisites</h3><p>Ideas worth knowing before this topic.</p><div class="chip-row">${prerequisites.map(topicReference).join("")}</div></div>` : ""}
        ${related.length ? `<div class="info-card"><h3>Related topics</h3><p>Continue the thread into nearby ideas.</p><div class="chip-row">${related.map(topicReference).join("")}</div></div>` : ""}
      </div>` : ""}`;
  }

  function examplesTabMarkup(data) {
    const examples = Array.isArray(data?.examples) ? data.examples : [];
    if (!examples.length) {
      return emptyState({
        title: "No worked examples yet",
        text: "MathAPI has no examples for this topic right now.",
        iconName: "file-text"
      });
    }
    return examples.map((example, index) => `
      <article class="example-card">
        <div class="example-top">
          <span class="example-index">Example ${index + 1}</span>
          ${difficultyChip(example.difficulty)}
        </div>
        <div class="example-question">${prose(example.question)}</div>
        ${example.key_observation ? `<div class="observation"><strong>Key observation</strong>${escapeHtml(example.key_observation).replace(/\n/g, "<br>")}</div>` : ""}
        ${(example.concept_used || []).length ? `<div class="chip-row" style="margin-top: 12px">${chipList(example.concept_used)}${typeChips(example.question_type)}</div>` : ""}
        ${(example.formulae_used || []).length ? `<div class="formula-stack">${example.formulae_used.map(formulaCard).join("")}</div>` : ""}
        ${(example.steps || []).length ? `<ol class="step-list">${example.steps.map((step) => `<li>${escapeHtml(step).replace(/\n/g, "<br>")}</li>`).join("")}</ol>` : ""}
        <div class="answer-box">
          <strong>Final answer</strong>
          <div class="prose">${prose(example.answer)}</div>
          ${example.interpretation ? `<div class="prose">${prose(example.interpretation)}</div>` : ""}
        </div>
      </article>`).join("");
  }

  function formulaeTabMarkup(data) {
    const formulae = Array.isArray(data?.formulae) ? data.formulae : [];
    if (!formulae.length) {
      return emptyState({
        title: "No formulae for this topic",
        text: "The formula sheet for this topic is still empty.",
        iconName: "formula"
      });
    }
    return `<div class="formula-grid">${formulae.map(formulaCard).join("")}</div>`;
  }

  function sourcesTabMarkup(data) {
    const sources = Array.isArray(data?.sources) ? data.sources : [];
    if (!sources.length) {
      return emptyState({
        title: "No learning sources yet",
        text: "MathAPI has no source links for this topic right now.",
        iconName: "link"
      });
    }
    return `<div class="source-grid">${sources.map(sourceCard).join("")}</div>`;
  }

  async function loadTopicTab(topic, tab, sequence) {
    const mount = document.getElementById("topic-tab-content");
    if (!mount) return;
    try {
      if (tab === "explanation") {
        const data = await fetchData("/api/v1/explanation", { topic_id: topic.topic_id }, "explanation");
        if (sequence !== renderSequence) return;
        mount.innerHTML = explanationTabMarkup(data?.explanation || {}, topic);
      } else if (tab === "examples") {
        const data = await fetchData("/api/v1/examples", { topic_id: topic.topic_id, limit: 12 }, "content");
        if (sequence !== renderSequence) return;
        mount.innerHTML = examplesTabMarkup(data);
      } else if (tab === "questions") {
        const data = await fetchData("/api/v1/questions", { topic_id: topic.topic_id, limit: 10 }, "content");
        if (sequence !== renderSequence) return;
        const questions = Array.isArray(data?.questions) ? data.questions : [];
        if (!questions.length) {
          mount.innerHTML = emptyState({
            title: "No questions for this topic",
            text: "Try the Practice Arena with a different topic or difficulty.",
            iconName: "target",
            action: '<a class="btn btn-primary" href="#/practice">Open Practice Arena</a>'
          });
          hydrateIcons(mount);
          return;
        }
        mountQuiz(mount, createQuiz(questions, {
          mode: "topic",
          modeLabel: "Topic practice",
          kicker: `${topic.topic_name} · Practice`,
          topicId: topic.topic_id,
          topicName: topic.topic_name,
          returnTab: "questions"
        }));
        return;
      } else if (tab === "formulae") {
        const data = await fetchData("/api/v1/formulae", { topic_id: topic.topic_id }, "content");
        if (sequence !== renderSequence) return;
        mount.innerHTML = formulaeTabMarkup(data);
      } else if (tab === "sources") {
        const data = await fetchData("/api/v1/sources", { topic_id: topic.topic_id }, "content");
        if (sequence !== renderSequence) return;
        mount.innerHTML = sourcesTabMarkup(data);
      }
      hydrateIcons(mount);
      renderMath(mount);
    } catch (error) {
      if (sequence !== renderSequence) return;
      if (isNotFound(error)) {
        mount.innerHTML = emptyState({
          title: "Nothing has been added here yet",
          text: "Try another tab or explore a different topic.",
          iconName: "layers"
        });
      } else {
        mount.innerHTML = errorState(error);
      }
    }
  }

  function practiceTopicOptions(selectedId) {
    return app.topics.map((topic) => (
      `<option value="${escapeHtml(topic.topic_id)}"${selectedAttr(topic.topic_id, selectedId)}>${escapeHtml(topic.topic_name)} · ${Number(topic.questions_available) || 0} questions</option>`
    )).join("");
  }

  function practiceIntroMarkup() {
    return `
      <div class="panel">
        <div class="panel-head">
          <div>
            <h3 class="panel-title">Build a practice set</h3>
            <p class="panel-caption">Choose a topic and narrow the question pool before you begin.</p>
          </div>
          <span class="chip chip-orange">${icon("target")} Quiz mode</span>
        </div>
        <div class="info-list">
          <div class="info-row"><span class="info-label">Hints</span><span class="info-value plain">Available before checking an answer</span></div>
          <div class="info-row"><span class="info-label">Difficulty</span><span class="info-value plain">Beginner, Intermediate, or Advanced</span></div>
          <div class="info-row"><span class="info-label">Question types</span><span class="info-value plain">Conceptual, numerical, proof, word, case, HOTS</span></div>
        </div>
      </div>`;
  }

  function readPracticeFilters() {
    const topic = document.getElementById("practice-topic");
    const difficulty = document.getElementById("practice-difficulty");
    const questionType = document.getElementById("practice-type");
    const limit = document.getElementById("practice-limit");
    ui.practice.topicId = topic?.value || ui.practice.topicId;
    ui.practice.difficulty = difficulty?.value || "";
    ui.practice.questionType = questionType?.value || "";
    ui.practice.limit = limit?.value || "10";
    return { ...ui.practice };
  }

  async function startPractice() {
    const filters = readPracticeFilters();
    const mount = document.getElementById("practice-stage");
    if (!mount || !filters.topicId) {
      toast("Choose a topic before starting practice.", "error");
      return;
    }
    const sequence = renderSequence;
    const startButton = document.querySelector('[data-action="practice-start"]');
    if (startButton) startButton.disabled = true;
    ui.practice.stage = "loading";
    mount.innerHTML = `<div class="quiz-shell">${miniSkeleton()}</div>`;
    try {
      const data = await fetchData("/api/v1/questions", {
        topic_id: filters.topicId,
        limit: filters.limit,
        difficulty: filters.difficulty,
        question_type: filters.questionType
      }, "content");
      if (sequence !== renderSequence || currentRoute?.name !== "practice") return;
      const topic = app.topics.find((item) => item.topic_id === filters.topicId);
      const questions = Array.isArray(data?.questions) ? data.questions : [];
      if (!questions.length) {
        ui.practice.stage = "idle";
        mount.innerHTML = emptyState({
          title: "No questions match this set",
          text: "Try another topic, difficulty, or question type.",
          iconName: "search"
        });
        return;
      }
      const quiz = createQuiz(questions, {
        mode: "practice",
        modeLabel: "Practice Arena",
        kicker: `${topic?.topic_name || "Practice"} · Practice`,
        topicId: filters.topicId,
        topicName: topic?.topic_name || "",
        returnTab: "questions"
      });
      if (topic) {
        state.lastTopic = { id: topic.topic_id, name: topic.topic_name, tab: "questions" };
        saveState();
      }
      ui.practice.stage = "quiz";
      mountQuiz(mount, quiz);
      mount.scrollIntoView({ behavior: "smooth", block: "start" });
    } catch (error) {
      if (sequence !== renderSequence || currentRoute?.name !== "practice") return;
      ui.practice.stage = "idle";
      mount.innerHTML = isNotFound(error)
        ? emptyState({
            title: "No questions found",
            text: "MathAPI returned no questions for this combination.",
            iconName: "target"
          })
        : errorState(error, { action: "practice-start", actionLabel: "Try this set again" });
      hydrateIcons(mount);
      renderMath(mount);
    } finally {
      if (startButton) startButton.disabled = false;
    }
  }

  async function viewPractice(route, sequence) {
    const data = await getTopics();
    if (sequence !== renderSequence) return null;
    if (!data.topics.length) {
      return {
        html: pageHead({
          eyebrow: "Workspace",
          title: "Practice Arena",
          text: "Build custom practice sets from the local topic catalog."
        }) + emptyState({
          title: "No topics available",
          text: "The practice arena needs topics and questions in MathAPI.",
          iconName: "target"
        })
      };
    }
    const requestedTopic = route.query.get("topic");
    if (requestedTopic && data.topics.some((topic) => topic.topic_id === requestedTopic)) {
      ui.practice.topicId = requestedTopic;
    }
    if (!data.topics.some((topic) => topic.topic_id === ui.practice.topicId)) {
      ui.practice.topicId = state.lastTopic?.id
        && data.topics.some((topic) => topic.topic_id === state.lastTopic.id)
        ? state.lastTopic.id
        : data.topics[0].topic_id;
    }
    ui.practice.stage = "idle";
    const html = `
      ${pageHead({
        eyebrow: "Workspace",
        title: "Practice Arena",
        text: "Choose the topic, difficulty, and question style. Every attempt updates your session accuracy.",
        actions: '<a class="btn btn-secondary" href="#/daily">Daily Challenge</a>'
      })}
      <div class="filter-bar">
        <label class="field field-grow">
          <span class="field-label">Topic</span>
          <select class="select" id="practice-topic">${practiceTopicOptions(ui.practice.topicId)}</select>
        </label>
        <label class="field">
          <span class="field-label">Difficulty</span>
          <select class="select" id="practice-difficulty">
            <option value="">Any level</option>
            ${DIFFICULTIES.map((level) => `<option value="${escapeHtml(level)}"${selectedAttr(level, ui.practice.difficulty)}>${escapeHtml(level)}</option>`).join("")}
          </select>
        </label>
        <label class="field">
          <span class="field-label">Question type</span>
          <select class="select" id="practice-type">
            <option value="">Any type</option>
            ${QUESTION_TYPES.map((type) => `<option value="${escapeHtml(type)}"${selectedAttr(type, ui.practice.questionType)}>${escapeHtml(type)}</option>`).join("")}
          </select>
        </label>
        <label class="field">
          <span class="field-label">Questions</span>
          <select class="select" id="practice-limit">
            ${[5, 10, 15, 20].map((count) => `<option value="${count}"${selectedAttr(String(count), ui.practice.limit)}>${count}</option>`).join("")}
          </select>
        </label>
        <button class="btn btn-primary" type="button" data-action="practice-start">${icon("play")} Start practice</button>
      </div>
      <div id="practice-stage">${practiceIntroMarkup()}</div>`;
    return {
      html,
      title: "Practice Arena",
      eyebrow: "Workspace"
    };
  }

  function challengeDate(value) {
    const match = /^(\d{4})-(\d{2})-(\d{2})/.exec(String(value || ""));
    if (match) {
      return formatDate(new Date(Number(match[1]), Number(match[2]) - 1, Number(match[3])));
    }
    return formatDate(value);
  }

  async function viewDaily(route, sequence) {
    await getTopics().catch(() => null);
    const data = await fetchData("/api/v1/daily-challenge", {}, "daily");
    if (sequence !== renderSequence) return null;
    const questions = Array.isArray(data?.questions) ? data.questions : [];
    if (!questions.length) {
      return {
        html: pageHead({
          eyebrow: "Discover",
          title: "Daily Challenge",
          text: "Three questions selected for everyone using this local API today."
        }) + emptyState({
          title: "No challenge today",
          text: "MathAPI did not return a daily challenge.",
          iconName: "calendar"
        })
      };
    }
    const quiz = createQuiz(questions, {
      mode: "daily",
      modeLabel: "Daily Challenge",
      kicker: "Daily challenge · Shared set"
    });
    return {
      html: `
        ${pageHead({
          eyebrow: "Discover",
          title: "Three problems for today.",
          text: `One beginner, one intermediate, and one advanced problem · ${challengeDate(data?.challenge_date)}`,
          actions: '<a class="btn btn-secondary" href="#/practice">Practice Arena</a>'
        })}
        <div id="daily-stage">${renderQuizShell(quiz)}</div>`,
      title: "Daily Challenge",
      eyebrow: "Discover",
      quiz
    };
  }

  async function loadRandomQuestion(sequence) {
    const mount = document.getElementById("random-stage");
    if (!mount) return;
    const token = ++randomRequest;
    mount.innerHTML = `<div class="quiz-shell">${miniSkeleton()}</div>`;
    try {
      if (!app.topics.length) await getTopics().catch(() => null);
      const data = await fetchData("/api/v1/random-question", {}, null);
      if (token !== randomRequest || sequence !== renderSequence || currentRoute?.name !== "random") return;
      if (!data?.question) {
        mount.innerHTML = emptyState({
          title: "No question available",
          text: "MathAPI returned no random question.",
          iconName: "shuffle"
        });
        hydrateIcons(mount);
        return;
      }
      const quiz = createQuiz([data.question], {
        mode: "random",
        modeLabel: "Random question",
        kicker: "Random question · Any topic"
      });
      mountQuiz(mount, quiz);
    } catch (error) {
      if (token !== randomRequest || sequence !== renderSequence || currentRoute?.name !== "random") return;
      mount.innerHTML = errorState(error, { action: "random-new", actionLabel: "Try another question" });
      hydrateIcons(mount);
    }
  }

  async function viewRandom(route, sequence) {
    if (!app.topics.length) await getTopics().catch(() => null);
    const data = await fetchData("/api/v1/random-question", {}, null);
    if (sequence !== renderSequence) return null;
    const question = data?.question;
    if (!question) {
      return {
        html: pageHead({
          eyebrow: "Discover",
          title: "Random Question",
          text: "Pull one question from anywhere in the catalog."
        }) + emptyState({
          title: "No question available",
          text: "MathAPI returned no random question.",
          iconName: "shuffle"
        })
      };
    }
    const quiz = createQuiz([question], {
      mode: "random",
      modeLabel: "Random question",
      kicker: "Random question · Any topic"
    });
    return {
      html: `
        ${pageHead({
          eyebrow: "Discover",
          title: "A question from anywhere.",
          text: "A fresh random prompt from any topic, difficulty, or question type.",
          actions: `<button class="btn btn-primary" type="button" data-action="random-new">${icon("shuffle")} Shuffle again</button>`
        })}
        <div id="random-stage">${renderQuizShell(quiz)}</div>`,
      title: "Random Question",
      eyebrow: "Discover",
      quiz
    };
  }

  async function loadFormulaSheet(topic, sequence) {
    const mount = document.getElementById("formula-stage");
    if (!mount) return;
    try {
      const data = await fetchData("/api/v1/formulae", { topic_id: topic.topic_id }, "content");
      if (sequence !== renderSequence) return;
      const formulae = Array.isArray(data?.formulae) ? data.formulae : [];
      if (!formulae.length) {
        mount.innerHTML = emptyState({
          title: "No formulae for this topic",
          text: "Pick another topic from the selector above.",
          iconName: "formula"
        });
      } else {
        mount.innerHTML = `
          <div class="section-head">
            <div>
              <h3 class="section-title">${escapeHtml(topic.topic_name)}</h3>
              <p class="section-subtitle">${Number(data?.total_formulae) || formulae.length} formulae · rendered with KaTeX</p>
            </div>
            <a class="section-link" href="#/topic/${encodeURIComponent(topic.topic_id)}/formulae">Open topic studio ${icon("arrow-right")}</a>
          </div>
          <div class="formula-grid">${formulae.map(formulaCard).join("")}</div>`;
      }
      hydrateIcons(mount);
      renderMath(mount);
    } catch (error) {
      if (sequence !== renderSequence) return;
      mount.innerHTML = isNotFound(error)
        ? emptyState({
            title: "No formulae for this topic",
            text: "Choose a different topic or try again later.",
            iconName: "formula"
          })
        : errorState(error);
      hydrateIcons(mount);
    }
  }

  async function viewFormulas(route, sequence) {
    const data = await getTopics();
    if (sequence !== renderSequence) return null;
    if (!data.topics.length) {
      return {
        html: pageHead({
          eyebrow: "Library",
          title: "Formula Vault",
          text: "Concise, LaTeX-rendered formula sheets from the local catalog."
        }) + emptyState({
          title: "No topics available",
          text: "The formula vault needs topics in MathAPI.",
          iconName: "formula"
        })
      };
    }
    const requested = route.query.get("topic");
    if (requested && data.topics.some((topic) => topic.topic_id === requested)) {
      ui.formulaTopicId = requested;
    }
    if (!data.topics.some((topic) => topic.topic_id === ui.formulaTopicId)) {
      ui.formulaTopicId = state.lastTopic?.id
        && data.topics.some((topic) => topic.topic_id === state.lastTopic.id)
        ? state.lastTopic.id
        : (data.topics.find((topic) => Number(topic.formulae_available) > 0) || data.topics[0]).topic_id;
    }
    const topic = data.topics.find((item) => item.topic_id === ui.formulaTopicId) || data.topics[0];
    const html = `
      ${pageHead({
        eyebrow: "Library",
        title: "Formula Vault",
        text: "Scan a single well-curated sheet, copy the LaTeX, and get back to the reasoning.",
        actions: `<a class="btn btn-secondary" href="#/topic/${encodeURIComponent(topic.topic_id)}/formulae">${icon("book-open")} Topic studio</a>`
      })}
      <div class="filter-bar">
        <label class="field field-grow">
          <span class="field-label">Formula sheet</span>
          <select class="select" id="formula-topic">
            ${data.topics.map((item) => `<option value="${escapeHtml(item.topic_id)}"${selectedAttr(item.topic_id, topic.topic_id)}>${escapeHtml(item.topic_name)} · ${Number(item.formulae_available) || 0} formulae</option>`).join("")}
          </select>
        </label>
        <span class="result-count">${Number(topic.formulae_available) || 0} formulae available</span>
      </div>
      <div id="formula-stage">${miniSkeleton()}</div>`;
    return {
      html,
      title: "Formula Vault",
      eyebrow: "Library",
      after: () => loadFormulaSheet(topic, sequence)
    };
  }

  function viewSaved(route, sequence) {
    return getTopics().then((data) => {
      if (sequence !== renderSequence) return null;
      const savedTopics = state.bookmarks
        .map((topicId) => data.topics.find((topic) => topic.topic_id === topicId))
        .filter(Boolean);
      const progressEntries = Object.entries(state.progress)
        .filter(([, entry]) => entry && entry.attempted > 0)
        .sort((left, right) => new Date(right[1].lastAttempt || 0) - new Date(left[1].lastAttempt || 0));
      const attempted = progressEntries.reduce((sum, [, entry]) => sum + entry.attempted, 0);
      const correct = progressEntries.reduce((sum, [, entry]) => sum + entry.correct, 0);
      const accuracy = attempted ? Math.round((correct / attempted) * 100) : 0;
      const actions = `
        ${progressEntries.length ? '<button class="btn btn-ghost" type="button" data-action="reset-progress">' + icon("rotate") + " Reset progress</button>" : ""}
        ${savedTopics.length ? '<button class="btn btn-ghost" type="button" data-action="clear-bookmarks">' + icon("trash") + " Clear bookmarks</button>" : ""}`;
      const savedMarkup = savedTopics.length
        ? `<div class="topic-grid">${savedTopics.map(topicCard).join("")}</div>`
        : emptyState({
            title: "No saved topics",
            text: "Tap the bookmark icon on any topic to keep it here for this browser session.",
            iconName: "bookmark",
            action: '<a class="btn btn-primary" href="#/topics">Browse topics</a>'
          });
      const progressMarkup = progressEntries.length
        ? `<div class="topic-progress-list">
            ${progressEntries.map(([topicId, entry]) => {
              const topicAccuracy = entry.attempted ? Math.round((entry.correct / entry.attempted) * 100) : 0;
              return `<div class="progress-row">
                <div>
                  <strong>${escapeHtml(getTopicName(topicId))}</strong><br>
                  <span>${entry.attempted} attempted · ${topicAccuracy}% accuracy · ${escapeHtml(timeAgo(entry.lastAttempt))}</span>
                </div>
                <div class="progress-bar" aria-label="${topicAccuracy}% accuracy"><div class="progress-fill" style="width: ${topicAccuracy}%"></div></div>
                <a class="btn btn-ghost btn-sm" href="#/topic/${encodeURIComponent(topicId)}/questions">Practice</a>
              </div>`;
            }).join("")}
          </div>`
        : emptyState({
            title: "No attempts yet",
            text: "Answer a practice question and your session accuracy will appear here.",
            iconName: "target",
            action: '<a class="btn btn-primary" href="#/practice">Start practicing</a>'
          });
      const historyMarkup = state.history.length
        ? `<div class="topic-progress-list">
            ${state.history.slice(0, 6).map((entry) => `<div class="progress-row">
              <div>
                <strong>${escapeHtml(entry.label || "Practice session")}</strong><br>
                <span>${escapeHtml(entry.topicName || getTopicName(entry.topicId))} · ${escapeHtml(timeAgo(entry.completedAt))}</span>
              </div>
              <span>${Number(entry.correct) || 0} / ${Number(entry.attempted) || 0}</span>
            </div>`).join("")}
          </div>`
        : "";
      return {
        html: `
          ${pageHead({
            eyebrow: "Account",
            title: "Saved work, session by session.",
            text: "Bookmarks and accuracy are stored in this tab's sessionStorage. Closing the tab clears the learning record.",
            actions
          })}
          <div class="progress-grid">
            ${statCard("bookmark", savedTopics.length, "Saved topics")}
            ${statCard("target", attempted, "Questions attempted")}
            ${statCard("check-circle", `${accuracy}%`, "Overall accuracy")}
            ${statCard("layers", progressEntries.length, "Topics touched")}
          </div>
          <section class="section">
            <div class="section-head">
              <div>
                <h3 class="section-title">Saved topics</h3>
                <p class="section-subtitle">Your current shortlist.</p>
              </div>
              <a class="section-link" href="#/topics">Add topics ${icon("plus")}</a>
            </div>
            ${savedMarkup}
          </section>
          <section class="section">
            <div class="section-head">
              <div>
                <h3 class="section-title">Topic progress</h3>
                <p class="section-subtitle">Accuracy from answered quiz questions.</p>
              </div>
            </div>
            ${progressMarkup}
          </section>
          ${historyMarkup ? `<section class="section">
            <div class="section-head">
              <div>
                <h3 class="section-title">Recent sessions</h3>
                <p class="section-subtitle">The latest completed quiz sets in this tab.</p>
              </div>
            </div>
            ${historyMarkup}
          </section>` : ""}`,
        title: "Saved & Progress",
        eyebrow: "Account"
      };
    });
  }

  function settingsInfoRow(label, value, plain = false) {
    return `<div class="info-row"><span class="info-label">${escapeHtml(label)}</span><span class="info-value${plain ? " plain" : ""}">${escapeHtml(value)}</span></div>`;
  }

  function viewSettings(route, sequence) {
    const session = app.session;
    const expiry = sessionExpiryMs(session);
    const online = Boolean(app.online);
    const attempted = Object.values(state.progress).reduce((sum, entry) => sum + (entry.attempted || 0), 0);
    const healthMessage = online
      ? (app.health?.message || "The local API responded successfully.")
      : "Start MathAPI with uv run uvs dev, then test the connection.";
    const html = `
      ${pageHead({
        eyebrow: "Account",
        title: "Settings & local session.",
        text: "MathLabs is a local-only demo. Authentication, progress, and bookmarks stay in this browser tab.",
        actions: `<button class="btn btn-secondary" type="button" data-action="test-connection">${icon("wifi")} Test connection</button>`
      })}
      <div class="settings-grid">
        <article class="info-card">
          <h3>Demo session</h3>
          <p>The identity is fixed and read-only. A key is requested automatically when needed.</p>
          <div class="info-list">
            ${settingsInfoRow("Username", session?.username || DEMO_IDENTITY.username, true)}
            ${settingsInfoRow("Email", session?.email || DEMO_IDENTITY.email, true)}
            ${settingsInfoRow("API key", session ? maskKey(session.apiKey) : "Not connected")}
            ${settingsInfoRow("Expires", expiry ? formatDateTime(expiry) : session?.expiry || "—", true)}
          </div>
          <div class="actions-row">
            <button class="btn btn-primary btn-sm" type="button" data-action="refresh-session">${icon("refresh")} Refresh session</button>
            <button class="btn btn-ghost btn-sm" type="button" data-action="clear-cache">${icon("database")} Clear cache</button>
          </div>
        </article>
        <article class="info-card">
          <h3>Local MathAPI</h3>
          <p>The frontend talks only to the API running on this machine.</p>
          <div class="health-card ${online ? "is-online" : "is-offline"}">
            <span class="health-icon">${icon(online ? "wifi" : "server")}</span>
            <div>
              <strong>${online ? "API reachable" : "API offline"}</strong>
              <p>${escapeHtml(healthMessage)}</p>
            </div>
          </div>
          <div class="info-list" style="margin-top: 14px">
            ${settingsInfoRow("Endpoint", API_BASE)}
            ${settingsInfoRow("API key header", "X-API-Key")}
            ${settingsInfoRow("Rate limit", "100/hour per key · 300/hour per IP", true)}
            ${settingsInfoRow("Docs", `${API_BASE}/docs`)}
          </div>
          <div class="actions-row">
            ${externalLink(`${API_BASE}/docs`, "Open API docs", "btn btn-secondary btn-sm")}
          </div>
        </article>
        <article class="info-card span-2">
          <h3>Appearance & local data</h3>
          <p>Theme persists in localStorage; bookmarks and quiz progress use sessionStorage.</p>
          <div class="info-list">
            ${settingsInfoRow("Theme", document.documentElement.dataset.theme === "light" ? "Light" : "Dark", true)}
            ${settingsInfoRow("Bookmarked topics", String(state.bookmarks.length), true)}
            ${settingsInfoRow("Questions attempted", String(attempted), true)}
            ${settingsInfoRow("Cached API responses", String(app.cache.size), true)}
            ${settingsInfoRow("Static app", "uv run uvs demo_app")}
          </div>
          <div class="actions-row">
            <button class="btn btn-secondary btn-sm" type="button" data-action="theme">${icon("sun")} Toggle theme</button>
            <button class="btn btn-danger btn-sm" type="button" data-action="reset-learning-data">${icon("trash")} Reset learning data</button>
          </div>
        </article>
      </div>`;
    return {
      html,
      title: "Settings",
      eyebrow: "Account"
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
    const [pathPart, queryPart = ""] = raw.split("?");
    const segments = pathPart.split("/").filter(Boolean).map(safeDecode);
    const name = Object.prototype.hasOwnProperty.call(ROUTES, segments[0]) ? segments[0] : "dashboard";
    return {
      name,
      id: name === "topic" ? segments[1] || "" : "",
      tab: name === "topic" ? segments[2] || "explanation" : "",
      query: new URLSearchParams(queryPart)
    };
  }

  async function renderRoute() {
    const sequence = ++renderSequence;
    const route = parseHash();
    currentRoute = route;
    closeSidebar();
    quizSession = null;
    updateChrome(route);
    const view = document.getElementById("view");
    if (!view) return;
    view.innerHTML = routeSkeleton();
    window.scrollTo({ top: 0, left: 0, behavior: "auto" });
    try {
      let result = null;
      if (route.name === "dashboard") result = await viewDashboard(route, sequence);
      else if (route.name === "topics") result = await viewTopics(route, sequence);
      else if (route.name === "topic") result = await viewTopic(route, sequence);
      else if (route.name === "practice") result = await viewPractice(route, sequence);
      else if (route.name === "daily") result = await viewDaily(route, sequence);
      else if (route.name === "random") result = await viewRandom(route, sequence);
      else if (route.name === "formulas") result = await viewFormulas(route, sequence);
      else if (route.name === "saved") result = await viewSaved(route, sequence);
      else if (route.name === "settings") result = viewSettings(route, sequence);
      if (!result || sequence !== renderSequence) return;
      updateChrome(route, { title: result.title, eyebrow: result.eyebrow });
      if (result.quiz) quizSession = result.quiz;
      view.dataset.route = route.name;
      view.innerHTML = result.html;
      hydrateIcons(view);
      renderMath(view);
      if (typeof result.after === "function") {
        try {
          await result.after();
        } catch (error) {
          if (sequence === renderSequence) toast(error.message || "This section could not load.", "error");
        }
      }
    } catch (error) {
      if (sequence !== renderSequence) return;
      view.innerHTML = errorState(error);
      hydrateIcons(view);
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
      if (action === "refresh-session") {
        if (element) element.disabled = true;
        try {
          await refreshSession();
          if (currentRoute?.name === "settings") await renderRoute();
        } finally {
          if (element) element.disabled = false;
        }
        return;
      }
      if (action === "clear-cache") {
        clearCache();
        toast("Cached MathAPI responses cleared.", "success");
        if (currentRoute?.name === "settings") await renderRoute();
        return;
      }
      if (action === "toggle-bookmark") {
        const topicId = element?.dataset.topicId;
        if (!topicId) return;
        const saved = toggleBookmark(topicId);
        toast(saved ? "Topic saved for this session." : "Bookmark removed.", "success");
        syncBookmarkButtons(topicId);
        if (currentRoute?.name === "saved") await renderRoute();
        return;
      }
      if (action === "copy-formula") {
        const card = element?.closest(".formula-card");
        const latex = card?.querySelector("[data-latex]")?.textContent?.trim();
        if (!latex) {
          toast("There is no LaTeX code to copy.", "error");
          return;
        }
        await copyText(latex);
        toast("LaTeX copied to the clipboard.", "success");
        return;
      }
      if (action.startsWith("quiz-")) {
        handleQuizAction(action, element);
        return;
      }
      if (action === "retry-route") {
        await renderRoute();
        return;
      }
      if (action === "clear-topic-filters") {
        ui.topicSearch = "";
        ui.topicBranch = "";
        ui.topicDifficulty = "";
        ui.topicSort = "name";
        if (window.location.hash.includes("?")) history.replaceState(null, "", "#/topics");
        await renderRoute();
        return;
      }
      if (action === "practice-start" || action === "practice-restart") {
        await startPractice();
        return;
      }
      if (action === "practice-reset") {
        await renderRoute();
        return;
      }
      if (action === "random-new") {
        await loadRandomQuestion(renderSequence);
        return;
      }
      if (action === "test-connection") {
        if (element) element.disabled = true;
        try {
          await checkHealth();
          toast("MathAPI is reachable.", "success");
          if (currentRoute?.name === "settings") await renderRoute();
        } catch (error) {
          toast(error.message || "MathAPI is not reachable.", "error");
          if (currentRoute?.name === "settings") await renderRoute();
        } finally {
          if (element) element.disabled = false;
        }
        return;
      }
      if (action === "reset-progress") {
        const confirmed = await openModal({
          title: "Reset quiz progress?",
          message: "This clears session accuracy and recent quiz history. Your bookmarks stay intact.",
          confirmLabel: "Reset progress",
          danger: true
        });
        if (!confirmed) return;
        resetProgress();
        toast("Quiz progress reset.", "success");
        await renderRoute();
        return;
      }
      if (action === "clear-bookmarks") {
        const confirmed = await openModal({
          title: "Clear saved topics?",
          message: "This removes every bookmark from this browser session.",
          confirmLabel: "Clear bookmarks",
          danger: true
        });
        if (!confirmed) return;
        clearBookmarks();
        toast("Saved topics cleared.", "success");
        await renderRoute();
        return;
      }
      if (action === "reset-learning-data") {
        const confirmed = await openModal({
          title: "Reset all local learning data?",
          message: "Bookmarks, progress, recent sessions, and the last-opened topic will be cleared from sessionStorage.",
          confirmLabel: "Reset everything",
          danger: true
        });
        if (!confirmed) return;
        resetLearningState();
        toast("Local learning data reset.", "success");
        await renderRoute();
        return;
      }
      if (action === "theme") {
        toggleTheme();
        if (currentRoute?.name === "settings") await renderRoute();
      }
    } catch (error) {
      toast(error.message || "That action could not be completed.", "error");
    }
  }

  async function onDocumentClick(event) {
    if (event.target.closest("[data-modal-confirm]")) {
      event.preventDefault();
      closeModal(true);
      return;
    }
    if (event.target.closest("[data-modal-cancel]")) {
      event.preventDefault();
      closeModal(false);
      return;
    }
    if (event.target.id === "modal-root") {
      closeModal(false);
      return;
    }
    if (event.target.closest("#theme-toggle")) {
      event.preventDefault();
      toggleTheme();
      return;
    }
    if (event.target.closest("#menu-toggle")) {
      event.preventDefault();
      const sidebar = document.getElementById("sidebar");
      setSidebarOpen(!sidebar?.classList.contains("is-open"));
      return;
    }
    if (event.target.closest("#sidebar-backdrop")) {
      closeSidebar();
      return;
    }
    if (event.target.closest("[data-skip-link]")) {
      event.preventDefault();
      const view = document.getElementById("view");
      if (view) {
        view.focus();
        view.scrollIntoView({ block: "start" });
      }
      return;
    }
    const routeLink = event.target.closest('a[href^="#/"]');
    if (routeLink) closeSidebar();
    const actionElement = event.target.closest("[data-action]");
    if (actionElement) {
      event.preventDefault();
      await handleAction(actionElement.dataset.action || "", actionElement);
    }
  }

  function onDocumentInput(event) {
    if (event.target.id === "topic-search") {
      ui.topicSearch = event.target.value;
      refreshTopicResults();
    }
  }

  function onDocumentChange(event) {
    const targetId = event.target.id;
    if (targetId === "topic-branch") {
      ui.topicBranch = event.target.value;
      refreshTopicResults();
    } else if (targetId === "topic-difficulty") {
      ui.topicDifficulty = event.target.value;
      refreshTopicResults();
    } else if (targetId === "topic-sort") {
      ui.topicSort = event.target.value;
      refreshTopicResults();
    } else if (targetId === "formula-topic") {
      const topicId = event.target.value;
      if (topicId) window.location.hash = `#/formulas?topic=${encodeURIComponent(topicId)}`;
    } else if (targetId === "practice-topic") {
      ui.practice.topicId = event.target.value;
    } else if (targetId === "practice-difficulty") {
      ui.practice.difficulty = event.target.value;
    } else if (targetId === "practice-type") {
      ui.practice.questionType = event.target.value;
    } else if (targetId === "practice-limit") {
      ui.practice.limit = event.target.value;
    }
  }

  function onDocumentKeydown(event) {
    if (event.key !== "Escape") return;
    if (modalResolve) {
      closeModal(false);
      return;
    }
    const sidebar = document.getElementById("sidebar");
    if (sidebar?.classList.contains("is-open")) closeSidebar();
  }

  function bindEvents() {
    document.addEventListener("click", onDocumentClick);
    document.addEventListener("input", onDocumentInput);
    document.addEventListener("change", onDocumentChange);
    document.addEventListener("keydown", onDocumentKeydown);
    window.addEventListener("hashchange", renderRoute);
    window.addEventListener("resize", onViewportResize);
  }

  async function boot() {
    applyTheme(document.documentElement.dataset.theme === "light" ? "light" : "dark", false);
    hydrateIcons(document);
    bindEvents();
    app.session = loadSession();
    updateSessionUI();
    setApiStatus("checking", "Checking API");
    setLoadingMessage(app.session ? "Restoring the demo session…" : "Registering the demo session…");
    if (!window.location.hash || window.location.hash === "#/") {
      history.replaceState(null, "", "#/dashboard");
    }
    const healthPromise = checkHealth().catch(() => null);
    try {
      await authenticate();
    } catch (error) {
      toast(error.message || "The demo session could not be created.", "error");
    }
    hideLoadingScreen();
    await renderRoute();
    healthPromise.then(() => {
      if (currentRoute?.name === "settings") renderRoute();
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot, { once: true });
  } else {
    boot();
  }
})();