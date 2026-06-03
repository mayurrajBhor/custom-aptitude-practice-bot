const MODE_CONFIG = {
  quick: { label: "Quick 5", targetCount: 5 },
  focused: { label: "Focused 15", targetCount: 15 },
  full: { label: "All Variants", targetCount: null },
};

const AUTO_ADVANCE_MS = 1400;
const GAME_MODE_KEYS = ["vedicSprint", "cricketChase", "mistakeRevenge", "directionMaze", "discountShop"];
const GAME_TARGET_CAP = 15;

const state = {
  telegramUser: null,
  catalog: [],
  activeCategoryId: null,
  activeTopicId: null,
  selectedPatternIds: new Set(),
  selectedMode: "quick",
  session: null,
  activeQuestion: null,
  answered: false,
  timerId: null,
  autoAdvanceId: null,
  questionStartedAt: null,
  lastSelection: [],
  profileOffline: false,
  patternProgress: new Map(),
  mistakePatternIds: [],
  reminderSettings: null,
  webConfig: null,
  webAccessKey: null,
  webAccessDenied: false,
  activeGameId: null,
  activeGameMode: null,
  gameState: null,
};

const $ = (selector) => document.querySelector(selector);

function showStatus(message, tone = "error") {
  const banner = $("#statusBanner");
  banner.textContent = message;
  banner.hidden = false;
  banner.classList.toggle("is-info", tone === "info");
}

function clearStatus() {
  const banner = $("#statusBanner");
  banner.hidden = true;
  banner.textContent = "";
  banner.classList.remove("is-info");
}

function clearAutoAdvance() {
  if (state.autoAdvanceId) {
    window.clearTimeout(state.autoAdvanceId);
    state.autoAdvanceId = null;
  }
  const autoAdvanceText = $("#autoAdvanceText");
  if (autoAdvanceText) {
    autoAdvanceText.hidden = true;
    autoAdvanceText.textContent = "";
  }
}

function replayAnimation(element, className) {
  if (!element) {
    return;
  }
  element.classList.remove(className);
  void element.offsetWidth;
  element.classList.add(className);
}

function clearAnswerFeedback() {
  $("#feedbackPanel")?.classList.remove("is-correct", "is-wrong");
  const burst = $("#answerBurst");
  if (burst) {
    burst.hidden = true;
    burst.textContent = "";
  }
}

function playAnswerFeedback(isCorrect) {
  const panel = $("#feedbackPanel");
  if (panel) {
    panel.classList.remove("is-correct", "is-wrong");
    void panel.offsetWidth;
    panel.classList.add(isCorrect ? "is-correct" : "is-wrong");
  }

  const burst = $("#answerBurst");
  if (!burst) {
    return;
  }
  burst.textContent = isCorrect ? "+1 momentum" : "Pattern locked";
  burst.hidden = false;
  replayAnimation(burst, "answer-burst");
}

function setCatalogLoading() {
  $("#categoryTabs").innerHTML = "";
  $("#topicList").innerHTML = `<div class="loading-block"></div><div class="loading-block"></div>`;
  $("#patternList").innerHTML = `<div class="loading-block"></div><div class="loading-block"></div><div class="loading-block"></div>`;
  $("#selectionList").innerHTML = `<div class="selection-empty">Select patterns to begin.</div>`;
}

function initTelegram() {
  const tg = window.Telegram?.WebApp;
  if (!tg) {
    initBrowserProfile();
    return;
  }
  tg.ready();
  tg.expand();
  const user = tg.initDataUnsafe?.user;
  if (user?.id) {
    state.telegramUser = {
      id: user.id,
      username: user.username || null,
      first_name: user.first_name || null,
      last_name: user.last_name || null,
    };
    $("#userChip").textContent = user.first_name || user.username || "Telegram";
    $("#profileTools").hidden = true;
  } else {
    initBrowserProfile();
  }
}

function initBrowserProfile() {
  if (state.webAccessDenied) {
    $("#profileTools").hidden = true;
    updateProfileNote("Open your private app link to sync progress on this device.");
    return;
  }

  const params = new URLSearchParams(window.location.search);
  const urlUserId = params.get("user_id") || params.get("tg_user_id");
  const configuredUserId = parseUserId(state.webConfig?.single_user_id);
  const storedUserId = readStoredProfileUserId();
  const userId = configuredUserId || parseUserId(urlUserId || storedUserId);
  if (!userId) {
    $("#profileTools").hidden = false;
    updateProfileNote("Set WEB_SINGLE_USER_ID on the server to sync this web app across devices without login.");
    return;
  }
  setBrowserProfileUser(userId);
}

function parseUserId(value) {
  const parsed = Number(value);
  return Number.isSafeInteger(parsed) && parsed > 0 ? parsed : null;
}

function setBrowserProfileUser(userId) {
  state.telegramUser = {
    id: userId,
    username: null,
    first_name: null,
    last_name: null,
  };
  writeStoredProfileUserId(userId);
  $("#userChip").textContent = "Personal";
  const input = $("#devUserIdInput");
  if (input) {
    input.value = String(userId);
  }
  $("#profileTools").hidden = true;
  updateProfileNote("Personal profile synced across devices.");
}

function readStoredProfileUserId() {
  try {
    return window.localStorage?.getItem("aptitudePracticeUserId") || null;
  } catch {
    return null;
  }
}

function writeStoredProfileUserId(userId) {
  try {
    window.localStorage?.setItem("aptitudePracticeUserId", String(userId));
  } catch {
    // Some embedded browser surfaces disable localStorage.
  }
}

function readStoredWebAccessKey() {
  try {
    return window.localStorage?.getItem("aptitudePracticeAccessKey") || null;
  } catch {
    return null;
  }
}

function writeStoredWebAccessKey(accessKey) {
  if (!accessKey) {
    return;
  }
  try {
    window.localStorage?.setItem("aptitudePracticeAccessKey", accessKey);
  } catch {
    // Some embedded browser surfaces disable localStorage.
  }
}

async function initWebConfig() {
  const params = new URLSearchParams(window.location.search);
  const urlAccessKey = params.get("access_key") || params.get("key");
  state.webAccessKey = urlAccessKey || readStoredWebAccessKey();
  writeStoredWebAccessKey(state.webAccessKey);

  try {
    state.webConfig = await api("/api/web-config", { timeoutMs: 10000 });
    state.webAccessDenied = false;
  } catch (error) {
    state.webConfig = null;
    state.webAccessDenied = true;
    showStatus(error.message, "info");
  }
}

function updateProfileNote(message = "") {
  const note = $("#profileNote");
  if (!note) {
    return;
  }
  note.textContent = message;
  note.hidden = !message;
}

async function api(path, options = {}) {
  const controller = new AbortController();
  const timeout = window.setTimeout(() => controller.abort(), options.timeoutMs || 30000);
  const headers = {
    "Content-Type": "application/json",
    ...(options.headers || {}),
  };
  if (state.webAccessKey) {
    headers["X-Web-Access-Key"] = state.webAccessKey;
  }
  const { timeoutMs, headers: _headers, ...fetchOptions } = options;

  try {
    const response = await fetch(path, {
      ...fetchOptions,
      headers,
      signal: controller.signal,
    });

    const contentType = response.headers.get("content-type") || "";
    const data = contentType.includes("application/json") ? await response.json() : await response.text();
    if (!response.ok) {
      const detail = typeof data === "object" ? data.detail : data;
      throw new Error(detail || "Request failed");
    }
    return data;
  } catch (error) {
    if (error.name === "AbortError") {
      throw new Error("Request timed out. Check that the local server is still running.");
    }
    throw error;
  } finally {
    window.clearTimeout(timeout);
  }
}

function setScreen(name) {
  document.querySelectorAll(".screen").forEach((screen) => screen.classList.remove("is-active"));
  document.querySelectorAll(".tab").forEach((tab) => tab.classList.remove("is-active"));

  $(`#${name}Screen`)?.classList.add("is-active");
  const navTarget = name === "progress" || name === "arcade" ? name : "practice";
  document.querySelector(`[data-screen-target="${navTarget}"]`)?.classList.add("is-active");
}

async function loadCatalog() {
  clearStatus();
  setCatalogLoading();
  $("#catalogStatus").textContent = "Syncing";
  try {
    const data = await api("/api/catalog");
    state.catalog = data.categories || [];
    const firstCategory = state.catalog[0];
    state.activeCategoryId = firstCategory?.id || null;
    state.activeTopicId = firstCategory?.topics?.[0]?.id || null;
    $("#catalogStatus").textContent = data.source === "local" ? "Local" : "Ready";
    if (data.source === "local") {
      showStatus(data.warning || "Using local catalog because the database is unavailable.", "info");
    }
    renderCatalog();
    renderGameModes();
  } catch (error) {
    $("#catalogStatus").textContent = "Offline";
    $("#topicList").innerHTML = `<div class="empty-state">${escapeHtml(error.message)}</div>`;
    $("#patternList").innerHTML = `<div class="empty-state">Catalog unavailable.</div>`;
    showStatus(error.message);
  }
}

async function loadProfile() {
  if (!state.telegramUser?.id) {
    renderProfile({
      total_attempts: 0,
      total_correct: 0,
      accuracy: 0,
      mastery: 0,
      avg_time: 0,
      today_solved: 0,
      weak_patterns: [],
    });
    renderUnlockProgress({ topics: [], patterns: [] });
    renderMistakes([], []);
    renderReminder(null);
    updateProfileNote("Set WEB_SINGLE_USER_ID on the server to sync progress across devices without login.");
    return;
  }

  try {
    const profile = await api(`/api/profile/${state.telegramUser.id}`);
    renderProfile(profile);
    updateProfileNote(profile.offline
      ? "Database is unavailable from this server, so live progress cannot be loaded here."
      : "Personal profile synced across devices.");
    if (!profile.offline) {
      await Promise.all([loadMistakes(), loadReminder()]);
    }
  } catch (error) {
    renderProfile({
      total_attempts: 0,
      total_correct: 0,
      accuracy: 0,
      mastery: 0,
      avg_time: 0,
      today_solved: 0,
      weak_patterns: [],
    });
    renderUnlockProgress({ topics: [], patterns: [] });
    renderMistakes([], []);
    renderReminder(null);
    updateProfileNote(`Could not load profile: ${error.message}`);
  }
}

function renderProfile(profile) {
  const unlockProgress = profile.unlock_progress || { topics: [], patterns: [] };
  state.patternProgress = new Map((unlockProgress.patterns || []).map((item) => [Number(item.id), item]));
  $("#todaySolved").textContent = profile.today_solved || 0;
  $("#accuracyStat").textContent = `${profile.accuracy || 0}%`;
  $("#masteryStat").textContent = `${profile.mastery || 0}%`;
  $("#totalSolved").textContent = profile.total_attempts || 0;
  $("#totalCorrect").textContent = profile.total_correct || 0;
  $("#avgTime").textContent = `${profile.avg_time || 0}s`;

  const weak = profile.weak_patterns || [];
  $("#weakList").innerHTML = weak.length
    ? weak.map((item) => `
        <div class="weak-item">
          <strong>${escapeHtml(item.name)}</strong>
          <span>${escapeHtml(item.topic_name)} - ${Math.round((item.mastery_score || 0) * 100)}% mastery</span>
        </div>
      `).join("")
    : `<div class="empty-state">No weak patterns yet.</div>`;

  renderUnlockProgress(unlockProgress);
  renderPatterns();
}

async function loadMistakes() {
  if (!state.telegramUser?.id) {
    renderMistakes([], []);
    return;
  }

  try {
    const data = await api(`/api/mistakes/${state.telegramUser.id}`);
    renderMistakes(data.mistakes || [], data.pattern_ids || []);
    renderGameModes();
  } catch (error) {
    $("#mistakeList").innerHTML = `<div class="empty-state">${escapeHtml(error.message)}</div>`;
    state.mistakePatternIds = [];
    $("#practiceMistakesButton").disabled = true;
  }
}

async function loadReminder() {
  if (!state.telegramUser?.id) {
    renderReminder(null);
    return;
  }

  try {
    renderReminder(await api(`/api/reminders/${state.telegramUser.id}`));
  } catch (error) {
    $("#reminderText").textContent = error.message;
  }
}

function renderReminder(settings) {
  state.reminderSettings = settings || { enabled: false, reminder_time: "20:00", timezone: "Asia/Kolkata" };
  $("#reminderEnabled").checked = Boolean(state.reminderSettings.enabled);
  $("#reminderTime").value = state.reminderSettings.reminder_time || "20:00";
  $("#reminderText").textContent = state.reminderSettings.enabled
    ? `Reminder active at ${state.reminderSettings.reminder_time || "20:00"}.`
    : "Telegram can remind you if you miss practice.";
}

async function saveReminder() {
  if (!state.telegramUser?.id) {
    updateProfileNote("Connect a personal web profile before saving reminders.");
    return;
  }

  $("#saveReminderButton").disabled = true;
  $("#saveReminderButton").textContent = "Saving";
  try {
    const settings = await api(`/api/reminders/${state.telegramUser.id}`, {
      method: "POST",
      body: JSON.stringify({
        enabled: $("#reminderEnabled").checked,
        reminder_time: $("#reminderTime").value || "20:00",
        timezone: "Asia/Kolkata",
      }),
    });
    renderReminder(settings);
  } catch (error) {
    $("#reminderText").textContent = error.message;
  } finally {
    $("#saveReminderButton").disabled = false;
    $("#saveReminderButton").textContent = "Save";
  }
}

function renderUnlockProgress(progress) {
  const topics = progress?.topics || [];
  if (!topics.length) {
    $("#unlockList").innerHTML = `<div class="empty-state">Start practicing to unlock progress.</div>`;
    return;
  }

  $("#unlockList").innerHTML = topics.slice(0, 6).map((topic) => {
    const total = Number(topic.total_patterns || 0);
    const mastered = Number(topic.mastered_patterns || 0);
    const practiced = Number(topic.practiced_patterns || 0);
    const percent = total ? Math.round((mastered / total) * 100) : 0;
    return `
      <div class="unlock-item">
        <div class="unlock-item-header">
          <strong>${escapeHtml(topic.topic_name)}</strong>
          <span>${mastered}/${total} mastered</span>
        </div>
        <div class="mini-track"><div style="width: ${percent}%"></div></div>
        <span>${practiced} practiced - ${Math.round((Number(topic.avg_mastery || 0)) * 100)}% mastery</span>
      </div>
    `;
  }).join("");
}

function renderMistakes(mistakes, patternIds) {
  state.mistakePatternIds = patternIds.map(Number).filter(Boolean);
  $("#practiceMistakesButton").disabled = state.mistakePatternIds.length === 0;

  if (!mistakes.length) {
    $("#mistakeList").innerHTML = `<div class="empty-state">No mistakes saved yet.</div>`;
    return;
  }

  $("#mistakeList").innerHTML = mistakes.slice(0, 5).map((item) => `
    <article class="mistake-item">
      <div class="mistake-item-header">
        <strong>${escapeHtml(item.pattern_name)}</strong>
        <span>${item.missed_count}x missed</span>
      </div>
      <p>${escapeHtml(item.question_text)}</p>
      <div class="mistake-actions">
        <button class="quiet-button" type="button" data-mistake-review="${item.id}">Mark reviewed</button>
      </div>
    </article>
  `).join("");
}

function renderCatalog() {
  renderCategories();
  renderTopics();
  renderPatterns();
  renderSelection();
}

function renderCategories() {
  $("#categoryTabs").innerHTML = state.catalog.length
    ? state.catalog.map((category) => `
        <button class="category-tab ${category.id === state.activeCategoryId ? "is-active" : ""}" data-category-id="${category.id}">
          ${escapeHtml(category.name)}
        </button>
      `).join("")
    : `<div class="empty-state">No categories.</div>`;
}

function renderTopics() {
  const category = getActiveCategory();
  const topics = category?.topics || [];
  $("#topicList").innerHTML = topics.length
    ? topics.map((topic) => `
        <button class="topic-button ${topic.id === state.activeTopicId ? "is-active" : ""}" data-topic-id="${topic.id}">
          <strong>${escapeHtml(topic.name)}</strong>
          <span>${topic.pattern_count} patterns - ${topic.variant_count} variants</span>
        </button>
      `).join("")
    : `<div class="empty-state">No topics available.</div>`;
}

function renderPatterns() {
  const topic = getActiveTopic();
  $("#topicTitle").textContent = topic?.name || "Select a topic";
  const topicPatterns = topic?.patterns || [];
  const allSelected = topicPatterns.length > 0 && topicPatterns.every((pattern) => state.selectedPatternIds.has(pattern.id));
  $("#selectTopicButton").textContent = allSelected ? "Clear topic" : "Select topic";

  if (!topicPatterns.length) {
    $("#patternList").innerHTML = `<div class="empty-state">No patterns available.</div>`;
    return;
  }

  $("#patternList").innerHTML = topicPatterns.map((pattern) => {
    const selected = state.selectedPatternIds.has(pattern.id);
    return `
      <button class="pattern-button ${selected ? "is-selected" : ""}" data-pattern-id="${pattern.id}">
        <span class="pattern-check">${selected ? "OK" : ""}</span>
        <span>
          <strong>${escapeHtml(pattern.name)}</strong>
          <span>${escapeHtml(pattern.description || "Practice pattern")}</span>
        </span>
        <span class="variant-pill">${pattern.variant_count} variants</span>
        ${renderPatternProgress(pattern.id)}
      </button>
    `;
  }).join("");
}

function renderPatternProgress(patternId) {
  const progress = state.patternProgress.get(Number(patternId));
  if (!progress) {
    return `<span class="difficulty-pill">New</span>`;
  }
  const attempts = Number(progress.total_attempts || 0);
  const mastery = Math.round(Number(progress.mastery_score || 0) * 100);
  const label = attempts ? `${mastery}% mastery` : "New";
  return `<span class="difficulty-pill">${label}</span>`;
}

function renderSelection() {
  const selected = getSelectedPatterns();
  state.lastSelection = selected;
  const variantCount = selected.reduce((sum, pattern) => sum + pattern.variant_count, 0);
  $("#variantCount").textContent = `${variantCount} variants`;
  $("#selectedPatternCount").textContent = selected.length;
  $("#selectedModeLabel").textContent = MODE_CONFIG[state.selectedMode].label;
  $("#startButton").disabled = selected.length === 0;

  $("#selectionList").innerHTML = selected.length
    ? selected.map((pattern) => `
        <div class="selection-item">
          <strong>${escapeHtml(pattern.name)}</strong>
          <span>${pattern.variant_count} variants</span>
        </div>
      `).join("")
    : `<div class="selection-empty">Select patterns to begin.</div>`;
}

function getActiveCategory() {
  return state.catalog.find((category) => category.id === state.activeCategoryId);
}

function getActiveTopic() {
  return getActiveCategory()?.topics?.find((topic) => topic.id === state.activeTopicId);
}

function getSelectedPatterns() {
  return state.catalog
    .flatMap((category) => category.topics || [])
    .flatMap((topic) => topic.patterns || [])
    .filter((pattern) => state.selectedPatternIds.has(pattern.id));
}

function selectWholeTopic() {
  const topic = getActiveTopic();
  if (!topic?.patterns?.length) {
    return;
  }
  const allSelected = topic.patterns.every((pattern) => state.selectedPatternIds.has(pattern.id));
  topic.patterns.forEach((pattern) => {
    if (allSelected) {
      state.selectedPatternIds.delete(pattern.id);
    } else {
      state.selectedPatternIds.add(pattern.id);
    }
  });
  renderPatterns();
  renderSelection();
}

function getGameModes() {
  const registry = window.AptitudeGameModes || {};
  return GAME_MODE_KEYS.map((key) => ({ key, mode: registry[key] })).filter((entry) => entry.mode);
}

function getGameMode(gameId) {
  return getGameModes().find((entry) => entry.key === gameId || entry.mode.id === gameId)?.mode || null;
}

function gameModeKey(game) {
  return getGameModes().find((entry) => entry.mode === game || entry.mode.id === game?.id)?.key || game?.id || "";
}

function renderGamePreview(key) {
  return `
    <div class="game-mode-preview-visual game-mode-preview-${escapeHtml(key)}" aria-hidden="true">
      <span></span><span></span><span></span><span></span>
    </div>
  `;
}

function renderGameModes() {
  const grid = $("#gameModeGrid");
  if (!grid) {
    return;
  }

  const games = getGameModes();
  if (!games.length) {
    grid.innerHTML = `<div class="empty-state">Game modes are still loading.</div>`;
    return;
  }

  grid.innerHTML = games.map(({ key, mode }) => {
    const patternCount = resolveGamePatternIds(mode).length;
    const targetCount = Number(mode.targetCount || 5);
    return `
      <article class="game-mode-card" style="--game-accent: ${escapeHtml(mode.accent || "#0f766e")}">
        <div class="game-mode-glow" aria-hidden="true"></div>
        <div class="game-mode-card-head">
          <span>${escapeHtml(mode.category || "Aptitude")}</span>
          <strong>${escapeHtml(mode.shortTitle || mode.title)}</strong>
        </div>
        <h3>${escapeHtml(mode.title)}</h3>
        <p>${escapeHtml(mode.subtitle || "A timed aptitude game mode.")}</p>
        <div class="game-mode-meta">
          <span>${targetCount} questions</span>
          <span>${patternCount || "Auto"} patterns</span>
        </div>
        ${renderGamePreview(key)}
        <button class="primary-button" type="button" data-game-id="${escapeHtml(key)}">Launch mode</button>
      </article>
    `;
  }).join("");
}

function allPatternsWithContext() {
  return state.catalog.flatMap((category) =>
    (category.topics || []).flatMap((topic) =>
      (topic.patterns || []).map((pattern) => ({
        ...pattern,
        category_name: category.name,
        topic_name: topic.name,
      }))
    )
  );
}

function normalizeSearch(value) {
  return String(value || "").toLowerCase().replace(/[^a-z0-9]+/g, " ").trim();
}

function specialGameTerms(game) {
  const key = gameModeKey(game);
  if (key === "vedicSprint") {
    return ["vedic math", "speed", "addition", "subtraction", "multiplication", "division", "tables", "squares", "cubes"];
  }
  if (key === "cricketChase") {
    return ["vedic math", "percentage", "calculation", "tables", "speed", "discount"];
  }
  if (key === "mistakeRevenge") {
    return ["mistake", "weak", "review"];
  }
  if (key === "directionMaze") {
    return ["direction", "distance", "turns", "clockwise", "shadow", "movement"];
  }
  if (key === "discountShop") {
    return ["percentage", "discount", "successive", "marked price", "selling price", "profit", "loss"];
  }
  return [];
}

function patternScoreForGame(game, pattern) {
  const haystack = normalizeSearch([
    pattern.name,
    pattern.description,
    pattern.topic_name,
    pattern.category_name,
  ].join(" "));
  const terms = [
    game.title,
    game.shortTitle,
    game.category,
    ...(game.recommendedPatternNames || []),
    ...specialGameTerms(game),
  ].map(normalizeSearch).filter(Boolean);

  return terms.reduce((score, term) => {
    if (!term) {
      return score;
    }
    if (haystack.includes(term)) {
      return score + Math.max(2, term.split(" ").length + 1);
    }
    const words = term.split(" ").filter((word) => word.length > 3);
    const wordMatches = words.filter((word) => haystack.includes(word)).length;
    return score + wordMatches;
  }, 0);
}

function resolveGamePatternIds(game) {
  const available = allPatternsWithContext();
  const availableIds = new Set(available.map((pattern) => Number(pattern.id)));
  const key = gameModeKey(game);

  if (key === "mistakeRevenge" && state.mistakePatternIds.length) {
    const mistakeIds = state.mistakePatternIds.map(Number).filter((id) => availableIds.has(id));
    if (mistakeIds.length) {
      return mistakeIds.slice(0, 8);
    }
  }

  const scored = available
    .map((pattern) => ({ pattern, score: patternScoreForGame(game, pattern) }))
    .filter((entry) => entry.score > 0)
    .sort((a, b) => b.score - a.score || Number(a.pattern.id) - Number(b.pattern.id));

  if (scored.length) {
    const limit = key === "cricketChase" ? 8 : 6;
    return scored.slice(0, limit).map((entry) => Number(entry.pattern.id));
  }

  const selected = getSelectedPatterns().map((pattern) => Number(pattern.id));
  if (selected.length) {
    return selected.slice(0, 6);
  }

  return available.slice(0, 4).map((pattern) => Number(pattern.id));
}

async function launchGameMode(gameId) {
  const game = getGameMode(gameId);
  if (!game) {
    showStatus("Game mode is not available yet.");
    return;
  }

  const patternIds = resolveGamePatternIds(game);
  if (!patternIds.length) {
    showStatus("No matching practice patterns are available for this game yet.");
    return;
  }

  state.activeGameId = gameModeKey(game);
  state.activeGameMode = game;
  state.gameState = {
    modeId: game.id,
    modeKey: state.activeGameId,
    startedAt: Date.now(),
  };
  state.selectedPatternIds = new Set(patternIds);
  state.selectedMode = "quick";
  document.querySelectorAll("[data-mode]").forEach((button) => {
    button.classList.toggle("is-active", button.dataset.mode === "quick");
  });
  renderSelection();
  setScreen("arcade");
  await startPractice({
    gameMode: game,
    patternIds,
    mode: "quick",
    targetCount: Number(game.targetCount || MODE_CONFIG.quick.targetCount),
  });
}

function clearGameMode() {
  state.activeGameId = null;
  state.activeGameMode = null;
  state.gameState = null;
  $("#gameStage")?.setAttribute("hidden", "");
  $("#gameHud")?.setAttribute("hidden", "");
  $("#gameResultLines")?.setAttribute("hidden", "");
}

function renderGameIntro() {
  if (!state.activeGameMode || !state.gameState) {
    return;
  }
  const stage = $("#gameStage");
  const scene = $("#gameScene");
  const hud = $("#gameHud");
  if (stage && scene) {
    stage.hidden = false;
    scene.innerHTML = state.activeGameMode.renderIntro ? state.activeGameMode.renderIntro() : "";
  }
  if (hud) {
    hud.hidden = false;
    hud.innerHTML = state.activeGameMode.renderHud ? state.activeGameMode.renderHud(state.gameState) : "";
  }
}

function renderGamePanels() {
  if (!state.activeGameMode || !state.gameState) {
    return;
  }
  const stage = $("#gameStage");
  const scene = $("#gameScene");
  const hud = $("#gameHud");
  try {
    if (stage && scene) {
      stage.hidden = false;
      scene.innerHTML = state.activeGameMode.renderScene ? state.activeGameMode.renderScene(state.gameState) : "";
    }
    if (hud) {
      hud.hidden = false;
      hud.innerHTML = state.activeGameMode.renderHud ? state.activeGameMode.renderHud(state.gameState) : "";
    }
  } catch (error) {
    showStatus(`Game display issue: ${error.message}`);
  }
}

function syncGameQuestion(question) {
  if (!state.activeGameMode || !state.gameState) {
    $("#gameStage")?.setAttribute("hidden", "");
    $("#gameHud")?.setAttribute("hidden", "");
    return;
  }
  state.gameState.activeQuestion = question;
  state.gameState.questionStartedAt = state.questionStartedAt;
  state.gameState.session = {
    sessionId: state.session?.session_id,
    currentIndex: Math.max(0, Number(question.question_number || 1) - 1),
    totalQuestions: question.total_questions,
  };
  state.activeGameMode.onQuestion?.(question, state.gameState);
  renderGamePanels();
}

function syncGameAnswer(result, answerIndex) {
  if (!state.activeGameMode || !state.gameState) {
    return;
  }
  const elapsedMs = Number(result.time_taken || 0) * 1000;
  const gameResult = {
    ...result,
    correct: result.is_correct,
    isCorrect: result.is_correct,
    answer_index: answerIndex,
    selected_option_index: answerIndex,
    question: state.activeQuestion,
    elapsed_ms: elapsedMs,
    elapsed_seconds: result.time_taken,
  };
  state.activeGameMode.onAnswer?.(gameResult, state.gameState);
  renderGamePanels();
}

function syncGameStop() {
  if (!state.activeGameMode || !state.gameState) {
    return;
  }
  state.activeGameMode.onStop?.(state.gameState);
  renderGamePanels();
}

function renderGameResult(summary) {
  const target = $("#gameResultLines");
  if (!target || !state.activeGameMode || !state.gameState) {
    target?.setAttribute("hidden", "");
    return;
  }

  const lines = state.activeGameMode.getSummaryLines?.(summary, state.gameState) || [];
  target.hidden = false;
  target.innerHTML = `
    <div class="game-result-heading">
      <span>${escapeHtml(state.activeGameMode.shortTitle || state.activeGameMode.title)}</span>
      <strong>Game report</strong>
    </div>
    <div class="game-result-grid">
      ${lines.map((line) => `<div>${escapeHtml(line)}</div>`).join("")}
    </div>
  `;
}

async function startPractice(options = {}) {
  const gameMode = options.gameMode || null;
  if (!gameMode) {
    clearGameMode();
  }

  const patternIds = options.patternIds ? [...options.patternIds] : [...state.selectedPatternIds];
  if (!patternIds.length) {
    showStatus("Select at least one pattern to start.");
    return;
  }

  clearStatus();
  $("#startButton").disabled = true;
  $("#startButton").textContent = "Preparing questions";

  try {
    const modeKey = options.mode || state.selectedMode;
    const mode = MODE_CONFIG[modeKey] || MODE_CONFIG.quick;
    const targetCount = options.targetCount === undefined ? mode.targetCount : options.targetCount;
    state.session = await api("/api/session/start", {
      method: "POST",
      timeoutMs: 120000,
      body: JSON.stringify({
        pattern_ids: patternIds,
        mode: modeKey,
        target_count: targetCount,
        telegram_user: state.telegramUser,
      }),
    });
    setScreen("question");
    renderGameIntro();
    await loadNextQuestion();
  } catch (error) {
    $("#selectionList").innerHTML = `<div class="empty-state">${escapeHtml(error.message)}</div>`;
    showStatus(error.message);
  } finally {
    $("#startButton").disabled = false;
    $("#startButton").textContent = "Start practice";
  }
}

async function startPracticeWithPatternIds(patternIds) {
  const available = new Set(
    state.catalog
      .flatMap((category) => category.topics || [])
      .flatMap((topic) => topic.patterns || [])
      .map((pattern) => Number(pattern.id))
  );
  const usableIds = patternIds.map(Number).filter((id) => available.has(id));
  if (!usableIds.length) {
    showStatus("No mistake patterns are available in the current catalog.");
    return;
  }
  state.selectedPatternIds = new Set(usableIds);
  state.selectedMode = "quick";
  document.querySelectorAll("[data-mode]").forEach((button) => {
    button.classList.toggle("is-active", button.dataset.mode === "quick");
  });
  renderSelection();
  setScreen("practice");
  await startPractice();
}

async function loadNextQuestion() {
  if (!state.session?.session_id) {
    setScreen("practice");
    showStatus("Start a session first.");
    return;
  }

  clearStatus();
  clearAutoAdvance();
  clearQuestionTimer();
  clearAnswerFeedback();
  state.answered = false;
  $("#nextButton").disabled = true;
  $("#nextButton").textContent = "Next question";
  $("#feedbackTitle").textContent = "Answer";
  $("#feedbackText").textContent = "Choose an option to see the explanation.";
  $("#autoAdvanceText").hidden = true;
  $("#optionsGrid").innerHTML = "";
  $("#questionText").textContent = "Loading question";

  try {
    const data = await api(`/api/session/${state.session.session_id}/next`, { method: "POST", timeoutMs: 45000 });
    if (data.complete) {
      showResults(data.summary);
      return;
    }

    state.activeQuestion = data.question;
    renderQuestion(data.question);
  } catch (error) {
    $("#questionText").textContent = "Could not load the next question.";
    $("#feedbackTitle").textContent = "Connection issue";
    $("#feedbackText").textContent = error.message;
    $("#nextButton").textContent = "Try again";
    $("#nextButton").onclick = loadNextQuestion;
    $("#nextButton").disabled = false;
    showStatus(error.message);
  }
}

function renderQuestion(question) {
  $("#questionCounter").textContent = `Question ${question.question_number} of ${question.total_questions}`;
  $("#questionText").textContent = question.question_text;
  $("#progressBar").style.width = `${((question.question_number - 1) / question.total_questions) * 100}%`;
  $("#optionsGrid").innerHTML = question.options.map((option, index) => `
    <button class="option-button" data-answer-index="${index}">
      ${String.fromCharCode(65 + index)}. ${escapeHtml(String(option))}
    </button>
  `).join("");
  replayAnimation(document.querySelector(".question-panel"), "is-entering");
  startQuestionTimer();
  syncGameQuestion(question);
}

async function submitAnswer(answerIndex) {
  if (state.answered) {
    return;
  }
  state.answered = true;
  clearQuestionTimer();

  let result;
  try {
    result = await api(`/api/session/${state.session.session_id}/answer`, {
      method: "POST",
      body: JSON.stringify({ answer_index: answerIndex }),
    });
  } catch (error) {
    state.answered = false;
    startQuestionTimer();
    showStatus(error.message);
    return;
  }

  document.querySelectorAll(".option-button").forEach((button) => {
    const index = Number(button.dataset.answerIndex);
    button.disabled = true;
    if (index === result.correct_option_index) {
      button.classList.add("is-correct");
    } else if (index === answerIndex) {
      button.classList.add("is-wrong");
    }
  });

  $("#progressBar").style.width = `${(result.answered / result.total_questions) * 100}%`;
  $("#feedbackTitle").textContent = result.is_correct ? "Correct" : "Review";
  $("#feedbackText").textContent = result.explanation || `Correct answer: ${result.correct_option}`;
  playAnswerFeedback(result.is_correct);
  syncGameAnswer(result, answerIndex);

  if (result.complete) {
    $("#nextButton").textContent = "View result";
    $("#nextButton").onclick = () => showResults(result.summary);
    $("#autoAdvanceText").textContent = "Showing result automatically...";
    $("#autoAdvanceText").hidden = false;
    state.autoAdvanceId = window.setTimeout(() => showResults(result.summary), AUTO_ADVANCE_MS);
  } else {
    $("#nextButton").textContent = "Next question";
    $("#nextButton").onclick = loadNextQuestion;
    $("#autoAdvanceText").textContent = "Next question loading automatically...";
    $("#autoAdvanceText").hidden = false;
    state.autoAdvanceId = window.setTimeout(loadNextQuestion, AUTO_ADVANCE_MS);
  }
  $("#nextButton").disabled = false;
  loadProfile();
}

async function stopPractice() {
  if (!state.session?.session_id) {
    clearAutoAdvance();
    clearQuestionTimer();
    setScreen("practice");
    return;
  }

  clearAutoAdvance();
  clearQuestionTimer();
  const stopButton = $("#stopPracticeButton");
  stopButton.disabled = true;
  stopButton.textContent = "Stopping";

  try {
    const result = await api(`/api/session/${state.session.session_id}/stop`, { method: "POST" });
    state.activeQuestion = null;
    state.answered = true;
    syncGameStop();
    showResults(result.summary);
  } catch (error) {
    showStatus(error.message);
  } finally {
    stopButton.disabled = false;
    stopButton.textContent = "Stop practice";
  }
}

function showResults(summary) {
  clearAutoAdvance();
  clearQuestionTimer();
  const total = summary.total_questions || 0;
  $("#resultScore").textContent = `${summary.score} / ${total}`;
  if (summary.stopped) {
    const plannedTotal = summary.planned_total_questions || total;
    const answered = summary.answered || summary.review_count || 0;
    const skipped = summary.skipped_count || 0;
    const skippedText = skipped ? ` - ${skipped} skipped` : "";
    $("#resultAccuracy").textContent = `Stopped after ${answered} of ${plannedTotal} - Accuracy ${summary.accuracy}%${skippedText}`;
  } else {
    $("#resultAccuracy").textContent = `Accuracy ${summary.accuracy}%`;
  }
  renderGameResult(summary);
  setScreen("result");
  replayAnimation($("#resultPanel"), "is-complete");
}

async function showReview() {
  if (!state.session?.session_id) {
    showStatus("No completed session to review.");
    setScreen("practice");
    return;
  }

  clearAutoAdvance();
  clearQuestionTimer();
  $("#reviewList").innerHTML = `<div class="loading-block"></div><div class="loading-block"></div>`;
  setScreen("review");

  try {
    const review = await api(`/api/session/${state.session.session_id}/review`);
    renderReview(review.questions || []);
  } catch (error) {
    $("#reviewList").innerHTML = `<div class="empty-state">${escapeHtml(error.message)}</div>`;
  }
}

function renderReview(questions) {
  if (!questions.length) {
    $("#reviewList").innerHTML = `<div class="empty-state">No answered questions to review yet.</div>`;
    return;
  }

  $("#reviewList").innerHTML = questions.map((question) => {
    const skipped = question.is_skipped || question.selected_option_index === null || question.selected_option_index === undefined;
    const selectedLabel = skipped ? "" : String.fromCharCode(65 + question.selected_option_index);
    const correctLabel = String.fromCharCode(65 + question.correct_option_index);
    const statusClass = skipped ? "is-skipped" : question.is_correct ? "is-correct" : "is-wrong";
    const statusText = skipped ? "Skipped" : question.is_correct ? "Correct" : "Incorrect";
    const selectedAnswer = skipped
      ? "Skipped"
      : `${selectedLabel}. ${escapeHtml(String(question.selected_option))}`;

    return `
      <article class="review-card ${statusClass}">
        <div class="review-card-header">
          <span>Question ${question.question_number}</span>
          <strong>${statusText}</strong>
        </div>
        <h3>${escapeHtml(question.question_text)}</h3>
        <div class="review-answer-grid">
          <div>
            <span>Your answer</span>
            <strong>${selectedAnswer}</strong>
          </div>
          <div>
            <span>Correct answer</span>
            <strong>${correctLabel}. ${escapeHtml(String(question.correct_option))}</strong>
          </div>
        </div>
        <p>${escapeHtml(question.explanation || "No explanation available.")}</p>
      </article>
    `;
  }).join("");
}

function startQuestionTimer() {
  state.questionStartedAt = Date.now();
  $("#questionTimer").textContent = "0s";
  state.timerId = window.setInterval(() => {
    const elapsed = Math.floor((Date.now() - state.questionStartedAt) / 1000);
    $("#questionTimer").textContent = `${elapsed}s`;
  }, 1000);
}

function clearQuestionTimer() {
  if (state.timerId) {
    window.clearInterval(state.timerId);
    state.timerId = null;
  }
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function bindEvents() {
  document.addEventListener("click", (event) => {
    const categoryButton = event.target.closest("[data-category-id]");
    if (categoryButton) {
      state.activeCategoryId = Number(categoryButton.dataset.categoryId);
      state.activeTopicId = getActiveCategory()?.topics?.[0]?.id || null;
      renderCatalog();
      return;
    }

    const topicButton = event.target.closest("[data-topic-id]");
    if (topicButton) {
      state.activeTopicId = Number(topicButton.dataset.topicId);
      renderTopics();
      renderPatterns();
      return;
    }

    const patternButton = event.target.closest("[data-pattern-id]");
    if (patternButton) {
      const patternId = Number(patternButton.dataset.patternId);
      if (state.selectedPatternIds.has(patternId)) {
        state.selectedPatternIds.delete(patternId);
      } else {
        state.selectedPatternIds.add(patternId);
      }
      renderPatterns();
      renderSelection();
      return;
    }

    const modeButton = event.target.closest("[data-mode]");
    if (modeButton) {
      state.selectedMode = modeButton.dataset.mode;
      document.querySelectorAll("[data-mode]").forEach((button) => button.classList.remove("is-active"));
      modeButton.classList.add("is-active");
      replayAnimation(modeButton, "is-pressing");
      renderSelection();
      return;
    }

    const screenButton = event.target.closest("[data-screen-target]");
    if (screenButton) {
      setScreen(screenButton.dataset.screenTarget);
      return;
    }

    const gameButton = event.target.closest("[data-game-id]");
    if (gameButton) {
      launchGameMode(gameButton.dataset.gameId);
      return;
    }

    const answerButton = event.target.closest("[data-answer-index]");
    if (answerButton) {
      submitAnswer(Number(answerButton.dataset.answerIndex));
      return;
    }

    const mistakeReviewButton = event.target.closest("[data-mistake-review]");
    if (mistakeReviewButton) {
      markMistakeReviewed(Number(mistakeReviewButton.dataset.mistakeReview));
    }
  });

  $("#selectTopicButton").addEventListener("click", selectWholeTopic);
  $("#startButton").addEventListener("click", startPractice);
  $("#practiceAgainButton").addEventListener("click", () => {
    if (state.activeGameId) {
      launchGameMode(state.activeGameId);
    } else {
      startPractice();
    }
  });
  $("#backToSetupButton").addEventListener("click", () => {
    clearGameMode();
    setScreen("practice");
  });
  $("#reviewAnswersButton").addEventListener("click", showReview);
  $("#reviewBackButton").addEventListener("click", () => setScreen("result"));
  $("#saveReminderButton").addEventListener("click", saveReminder);
  $("#reminderEnabled").addEventListener("change", saveReminder);
  $("#practiceMistakesButton").addEventListener("click", () => launchGameMode("mistakeRevenge"));
  $("#loadProfileButton").addEventListener("click", () => {
    const userId = parseUserId($("#devUserIdInput").value);
    if (!userId) {
      updateProfileNote("Enter a valid numeric users.user_id.");
      return;
    }
    setBrowserProfileUser(userId);
    loadProfile();
  });
  $("#devUserIdInput").addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
      $("#loadProfileButton").click();
    }
  });
  $("#stopPracticeButton").addEventListener("click", stopPractice);
}

async function markMistakeReviewed(mistakeId) {
  if (!state.telegramUser?.id || !mistakeId) {
    return;
  }
  try {
    await api(`/api/mistakes/${state.telegramUser.id}/${mistakeId}/reviewed`, { method: "POST" });
    await loadMistakes();
  } catch (error) {
    showStatus(error.message);
  }
}

async function boot() {
  await initWebConfig();
  initTelegram();
  bindEvents();
  await Promise.all([loadCatalog(), loadProfile()]);
  renderGameModes();
}

boot();
