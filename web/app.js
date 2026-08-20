const MODE_CONFIG = {
  quick: { label: "Quick 10", targetCount: 10 },
  focused: { label: "Focused 20", targetCount: 20 },
  full: { label: "All Variants", targetCount: null },
};

const AUTO_ADVANCE_MS = 600;
const GAME_MODE_KEYS = [
  "vedicSprint",
  "cricketChase",
  "mistakeRevenge",
  "directionMaze",
  "discountShop",
  "aptitudeHeist",
  "marketTrader",
  "trainControl",
  "escapeGrid",
  "auctionBattle",
];
const GAME_TARGET_CAP = 30;

const state = {
  telegramUser: null,
  catalog: [],
  activeCategoryId: null,
  activeTopicId: null,
  selectedPatternIds: new Set(),
  patternVariantSelection: {},
  variantPickerPatternId: null,
  variantPickerDraft: [],
  variantPickerAnchor: null,
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
  unlockProgress: { topics: [], patterns: [] },
  recommendedPatternIds: [],
  smartPlan: null,
  mistakes: [],
  mistakePatternIds: [],
  reminderSettings: null,
  webConfig: null,
  webAccessKey: null,
  webAccessDenied: false,
  progressCategoryId: null,
  progressTopicId: null,
  progressPatternId: null,
  activeGameId: null,
  activeGameMode: null,
  gameState: null,
  launchingGameId: null,
  finishingGameEarly: false,
  currentStreak: 0,
  bestStreak: 0,
  soundEnabled: true,
  renderedSmartPlanOnce: false,
  celebratedMissionKeys: new Set(),
  profileStats: {
    total_attempts: 0,
    total_correct: 0,
    accuracy: 0,
    mastery: 0,
    today_solved: 0,
    mistake_count: 0,
  },
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
  $("#feedbackPanel")?.classList.remove("is-checking", "is-correct", "is-wrong");
  const burst = $("#answerBurst");
  if (burst) {
    burst.hidden = true;
    burst.textContent = "";
  }
}

function playAnswerFeedback(isCorrect) {
  const panel = $("#feedbackPanel");
  if (panel) {
    panel.classList.remove("is-checking", "is-correct", "is-wrong");
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

function markAnswerPending(answerIndex) {
  document.querySelectorAll(".option-button").forEach((button) => {
    const index = Number(button.dataset.answerIndex);
    button.disabled = true;
    button.classList.remove("is-correct", "is-wrong", "is-dimmed", "is-pending");
    button.classList.toggle("is-pending", index === answerIndex);
    button.classList.toggle("is-dimmed", index !== answerIndex);
  });

  const feedbackPanel = $("#feedbackPanel");
  if (feedbackPanel) {
    feedbackPanel.classList.remove("is-correct", "is-wrong");
    feedbackPanel.classList.add("is-checking");
  }
  $("#feedbackTitle").textContent = "Locked";
  $("#feedbackText").textContent = "Checking instantly...";
  const burst = $("#answerBurst");
  if (burst) {
    burst.textContent = "Answer locked";
    burst.hidden = false;
    replayAnimation(burst, "answer-burst");
  }
}

function resetAnswerPending() {
  document.querySelectorAll(".option-button").forEach((button) => {
    button.disabled = false;
    button.classList.remove("is-pending", "is-dimmed", "is-correct", "is-wrong");
  });
  clearAnswerFeedback();
}

function readSoundPreference() {
  try {
    const stored = window.localStorage?.getItem("aptitudePracticeSound");
    return stored === null ? true : stored === "on";
  } catch {
    return true;
  }
}

function writeSoundPreference(enabled) {
  try {
    window.localStorage?.setItem("aptitudePracticeSound", enabled ? "on" : "off");
  } catch {
    // Some embedded webviews block localStorage.
  }
}

function setSoundEnabled(enabled) {
  state.soundEnabled = Boolean(enabled);
  writeSoundPreference(state.soundEnabled);
  const button = $("#soundToggleButton");
  if (button) {
    button.textContent = state.soundEnabled ? "Sound On" : "Sound Off";
    button.setAttribute("aria-pressed", state.soundEnabled ? "true" : "false");
  }
}

function playTone(type = "tap") {
  if (!state.soundEnabled) {
    return;
  }
  try {
    const AudioContext = window.AudioContext || window.webkitAudioContext;
    if (!AudioContext) {
      return;
    }
    const context = new AudioContext();
    const oscillator = context.createOscillator();
    const gain = context.createGain();
    const frequency = type === "correct" ? 620 : type === "wrong" ? 190 : type === "mission" ? 760 : 360;
    oscillator.type = type === "wrong" ? "sawtooth" : "sine";
    oscillator.frequency.setValueAtTime(frequency, context.currentTime);
    gain.gain.setValueAtTime(0.0001, context.currentTime);
    gain.gain.exponentialRampToValueAtTime(type === "tap" ? 0.018 : 0.045, context.currentTime + 0.02);
    gain.gain.exponentialRampToValueAtTime(0.0001, context.currentTime + (type === "mission" ? 0.28 : 0.16));
    oscillator.connect(gain);
    gain.connect(context.destination);
    oscillator.start();
    oscillator.stop(context.currentTime + (type === "mission" ? 0.32 : 0.18));
    window.setTimeout(() => context.close?.(), 420);
  } catch {
    // Audio is best-effort only.
  }
}

function triggerHaptic(type = "light") {
  try {
    const haptics = window.Telegram?.WebApp?.HapticFeedback;
    if (!haptics) {
      return;
    }
    if (type === "success" || type === "error") {
      haptics.notificationOccurred(type);
    } else {
      haptics.impactOccurred(type);
    }
  } catch {
    // Haptics are only available inside Telegram.
  }
}

function triggerConfetti(tone = "success") {
  const layer = $("#confettiLayer");
  if (!layer) {
    return;
  }
  const colors = tone === "mission"
    ? ["#f7c66a", "#088475", "#126fb4", "#ffffff"]
    : ["#088475", "#126fb4", "#dff5f0", "#f7c66a"];
  layer.innerHTML = Array.from({ length: 26 }, (_, index) => {
    const left = 5 + Math.random() * 90;
    const delay = Math.random() * 160;
    const drift = -42 + Math.random() * 84;
    const color = colors[index % colors.length];
    return `<span style="--x:${left}%;--delay:${delay}ms;--drift:${drift}px;--color:${color}"></span>`;
  }).join("");
  layer.hidden = false;
  replayAnimation(layer, "is-bursting");
  window.setTimeout(() => {
    layer.hidden = true;
    layer.innerHTML = "";
  }, 1300);
}

function tapFeedback(element, event) {
  if (!element) {
    return;
  }
  const rect = element.getBoundingClientRect();
  const x = event?.clientX ? event.clientX - rect.left : rect.width / 2;
  const y = event?.clientY ? event.clientY - rect.top : rect.height / 2;
  element.style.setProperty("--tap-x", `${Math.round(x)}px`);
  element.style.setProperty("--tap-y", `${Math.round(y)}px`);
  replayAnimation(element, "is-tapping");
  replayAnimation(element, "is-rippling");
  window.setTimeout(() => {
    element.classList.remove("is-rippling", "is-tapping");
  }, 620);
  triggerHaptic("light");
  if (!element.matches("[data-answer-index]")) {
    playTone("tap");
  }
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

function updateQuestionHud(question = state.activeQuestion) {
  const score = Number(state.session?.score || 0);
  const total = Number(question?.total_questions || state.session?.total_questions || 0);
  const answered = Math.max(0, Number(question?.question_number || state.session?.answered || 1) - 1);
  const scoreTarget = $("#questionScore");
  const streakTarget = $("#questionStreak");
  const comboTarget = $("#questionCombo");
  const progressTarget = $("#questionProgressText");
  if (scoreTarget) {
    scoreTarget.textContent = `${score}`;
  }
  if (streakTarget) {
    streakTarget.textContent = `${state.currentStreak}x`;
  }
  if (comboTarget) {
    comboTarget.textContent = state.currentStreak >= 5 ? "Hot" : state.currentStreak >= 3 ? "Combo" : "Ready";
  }
  if (progressTarget) {
    progressTarget.textContent = total ? `${Math.min(answered, total)}/${total}` : "0/0";
  }
}

function renderProgressVisuals() {
  const mastery = Number(state.profileStats.mastery || 0);
  const total = Number(state.profileStats.total_attempts || 0);
  const correct = Number(state.profileStats.total_correct || 0);
  const mistakeCount = Number(state.profileStats.mistake_count || state.mistakes.length || 0);
  const ring = $("#masteryRingSummary");
  const masteryText = $("#masteryVisualText");
  if (ring) {
    ring.style.setProperty("--ring", `${Math.max(0, Math.min(100, mastery))}%`);
    ring.innerHTML = `<strong>${Math.round(mastery)}%</strong><span>mastery</span>`;
  }
  if (masteryText) {
    masteryText.textContent = total
      ? `${correct}/${total} correct with ${Math.round(Number(state.profileStats.accuracy || 0))}% accuracy.`
      : "Start practicing to build mastery.";
  }

  const heatmap = $("#weeklyHeatmap");
  if (heatmap) {
    const today = Number(state.profileStats.today_solved || 0);
    const values = Array.from({ length: 7 }, (_, index) => {
      const weight = index === 6 ? today : Math.max(0, Math.round((today * (index + 2)) / 12) - (index % 2));
      return Math.min(4, Math.max(0, weight ? Math.ceil(weight / 5) : 0));
    });
    const labels = ["M", "T", "W", "T", "F", "S", "Today"];
    heatmap.innerHTML = values.map((value, index) => `
      <span class="heat-cell heat-${value}" title="${labels[index]}">
        <em>${escapeHtml(labels[index])}</em>
      </span>
    `).join("");
  }

  const radar = $("#weakRadar");
  if (radar) {
    const rows = [...state.patternProgress.values()]
      .sort((a, b) => Number(b.weakness_score || 0) - Number(a.weakness_score || 0))
      .slice(0, 4);
    radar.innerHTML = rows.length
      ? rows.map((item) => {
          const score = Math.max(8, Math.min(100, Number(item.weakness_score || 0)));
          return `
            <div class="weak-radar-row">
              <span>${escapeHtml(item.name || "Pattern")}</span>
              <div><b style="width:${score}%"></b></div>
              <strong>${Math.round(score)}</strong>
            </div>
          `;
        }).join("")
      : `<div class="empty-mini">Practice a set to map risk patterns.</div>`;
  }

  const recovery = $("#recoveryStats");
  if (recovery) {
    const openMistakes = Math.max(mistakeCount, state.mistakes.length);
    const recovered = Math.max(0, total - openMistakes);
    const recoveryRate = total ? Math.round((recovered / total) * 100) : 0;
    recovery.innerHTML = `
      <div><span>Open misses</span><strong>${openMistakes}</strong></div>
      <div><span>Recovery rate</span><strong>${recoveryRate}%</strong></div>
      <div><span>Best streak</span><strong>${state.bestStreak}x</strong></div>
    `;
  }
}

async function loadCatalog() {
  clearStatus();
  setCatalogLoading();
  $("#catalogStatus").textContent = "Fast";
  try {
    const fastData = await api("/api/catalog/fast", { timeoutMs: 8000 });
    applyCatalogPayload(fastData);
    if (fastData.source !== "database" || fastData.fast) {
      void refreshCatalogFromDatabase();
    }
  } catch (error) {
    $("#catalogStatus").textContent = "Offline";
    $("#topicList").innerHTML = `<div class="empty-state">${escapeHtml(error.message)}</div>`;
    $("#patternList").innerHTML = `<div class="empty-state">Catalog unavailable.</div>`;
    showStatus(error.message);
  }
}

function applyCatalogPayload(data) {
  const previousCategoryId = state.activeCategoryId;
  const previousTopicId = state.activeTopicId;
  state.catalog = data.categories || [];
  const firstCategory = state.catalog[0];
  const matchingCategory = state.catalog.find((category) => Number(category.id) === Number(previousCategoryId));
  state.activeCategoryId = matchingCategory?.id || firstCategory?.id || null;
  const activeCategory = getActiveCategory();
  const matchingTopic = (activeCategory?.topics || []).find((topic) => Number(topic.id) === Number(previousTopicId));
  state.activeTopicId = matchingTopic?.id || activeCategory?.topics?.[0]?.id || null;
  $("#catalogStatus").textContent = data.source === "database"
    ? data.cached ? "Cached" : "Ready"
    : data.fast ? "Fast"
    : "Local";
  if (data.source === "local" && data.warning) {
    showStatus(data.warning, "info");
  }
  renderCatalog();
  renderGameModes();
  renderProgressTracker();
}

async function refreshCatalogFromDatabase() {
  try {
    const data = await api("/api/catalog", { timeoutMs: 30000 });
    applyCatalogPayload(data);
    if (data.source === "database") {
      clearStatus();
    }
  } catch (error) {
    if (!state.catalog.length) {
      showStatus(error.message);
    } else {
      updateProfileNote("Practice is ready. Full database catalog is still syncing in the background.");
    }
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
      smart_plan: null,
    });
    renderUnlockProgress({ topics: [], patterns: [] });
    renderMistakes([], []);
    renderReminder(null);
    updateProfileNote("Set WEB_SINGLE_USER_ID on the server to sync progress across devices without login.");
    return;
  }

  renderSmartPlan(null);
  updateProfileNote("Loading fast profile summary.");
  try {
    const profile = await api(`/api/profile/${state.telegramUser.id}/summary`, { timeoutMs: 12000 });
    renderProfileSummary(profile);
    updateProfileNote(profile.offline
      ? "Database is unavailable from this server, so live progress cannot be loaded here."
      : "Stats loaded. Syncing coach, mistakes, and progress map in the background.");
    if (profile.offline) {
      applySmartPlanPayload(profile);
      applyProgressPayload(profile);
      renderMistakes([], []);
      renderReminder(null);
      return;
    }
    if (!profile.offline) {
      void loadProfileChunks();
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
      smart_plan: null,
    });
    renderUnlockProgress({ topics: [], patterns: [] });
    renderMistakes([], []);
    renderReminder(null);
    updateProfileNote(`Could not load profile: ${error.message}`);
  }
}

async function loadProfileChunks() {
  if (!state.telegramUser?.id) {
    return;
  }

  try {
    const smart = await api(`/api/profile/${state.telegramUser.id}/smart-plan`, { timeoutMs: 24000 });
    applySmartPlanPayload(smart);
    updateProfileNote(smart.offline ? "Coach is offline. Practice still works with local data." : "Coach loaded. Progress map is syncing.");
  } catch (error) {
    updateProfileNote(`Coach sync is delayed: ${error.message}`);
  }

  try {
    const progress = await api(`/api/profile/${state.telegramUser.id}/progress`, { timeoutMs: 30000 });
    applyProgressPayload(progress);
    updateProfileNote(progress.offline ? "Progress map is offline right now." : "Personal profile synced across devices.");
  } catch (error) {
    updateProfileNote(`Progress sync is delayed: ${error.message}`);
  }

  await Promise.allSettled([loadMistakes(), loadReminder()]);
}

function renderProfile(profile) {
  renderProfileSummary(profile);
  applySmartPlanPayload(profile);
  applyProgressPayload(profile);
}

function renderProfileSummary(profile) {
  state.profileStats = {
    ...state.profileStats,
    total_attempts: Number(profile.total_attempts || 0),
    total_correct: Number(profile.total_correct || 0),
    accuracy: Number(profile.accuracy || 0),
    mastery: Number(profile.mastery || 0),
    today_solved: Number(profile.today_solved || 0),
    mistake_count: Number(profile.mistake_count || state.profileStats.mistake_count || 0),
  };
  renderSmartPlan(profile.smart_plan);
  $("#todaySolved").textContent = profile.today_solved || 0;
  $("#accuracyStat").textContent = `${profile.accuracy || 0}%`;
  $("#masteryStat").textContent = `${profile.mastery || 0}%`;
  $("#totalSolved").textContent = profile.total_attempts || 0;
  $("#totalCorrect").textContent = profile.total_correct || 0;
  $("#avgTime").textContent = `${profile.avg_time || 0}s`;
  if (typeof profile.mistake_count !== "undefined") {
    $("#practiceMistakesButton").disabled = Number(profile.mistake_count || 0) === 0;
  }
  renderProgressVisuals();
}

function applySmartPlanPayload(profile) {
  state.recommendedPatternIds = (profile.recommended_pattern_ids || state.recommendedPatternIds || []).map(Number).filter(Boolean);
  if (typeof profile.mistake_count !== "undefined") {
    state.profileStats.mistake_count = Number(profile.mistake_count || 0);
  }
  renderSmartPlan(profile.smart_plan || state.smartPlan);
  const weak = profile.weak_patterns || [];
  $("#weakList").innerHTML = weak.length
    ? weak.map((item) => `
        <div class="weak-item">
          <strong>${escapeHtml(item.name)}</strong>
          <span>${escapeHtml(item.topic_name)} - ${Math.round((item.mastery_score || 0) * 100)}% mastery - ${Number(item.wrong_attempts || 0)} wrong</span>
          <button class="quiet-button" type="button" data-adaptive-practice="${Number(item.id)}">Practice</button>
        </div>
      `).join("")
    : `<div class="empty-state">No weak patterns yet.</div>`;
  renderGameModes();
  renderProgressVisuals();
}

function applyProgressPayload(profile) {
  const unlockProgress = profile.unlock_progress || { topics: [], patterns: [] };
  state.unlockProgress = unlockProgress;
  state.patternProgress = new Map((unlockProgress.patterns || []).map((item) => [Number(item.id), item]));
  renderUnlockProgress(unlockProgress);
  renderProgressTracker();
  renderPatterns();
  renderProgressVisuals();
}

function defaultSmartPlan() {
  return {
    coach_line: state.telegramUser?.id
      ? "Solve a few questions today so the coach can rank your weak patterns."
      : "Connect your profile to unlock smart revision and daily missions.",
    revision_queue: [],
    missions: [
      {
        key: "solve_20",
        title: "Solve 20 questions",
        description: "Daily volume mission.",
        progress: 0,
        target: 20,
        unit: "questions",
        percent: 0,
        completed: false,
        reward: { xp: 120, coins: 40, streak_shields: 0 },
        action: { type: "practice", label: "Start", pattern_ids: [], mode: "focused", target_count: 20 },
      },
      {
        key: "improve_weak",
        title: "Improve one weak pattern",
        description: "Win 3 answers from one weak pattern.",
        progress: 0,
        target: 3,
        unit: "wins",
        percent: 0,
        completed: false,
        reward: { xp: 180, coins: 55, streak_shields: 0 },
        action: { type: "practice", label: "Drill", pattern_ids: [], mode: "quick", target_count: 10 },
      },
      {
        key: "retry_5_mistakes",
        title: "Retry 5 mistakes",
        description: "Clear saved mistakes.",
        progress: 0,
        target: 5,
        unit: "mistakes",
        percent: 0,
        completed: false,
        reward: { xp: 150, coins: 45, streak_shields: 1 },
        action: { type: "mistakes", label: "Open mistakes", pattern_ids: [], mode: "quick", target_count: 5 },
      },
    ],
    wallet: { xp: 0, coins: 0, streak_shields: 0, level: 1, next_level_xp: 500, today_xp: 0, today_coins: 0 },
  };
}

function renderSmartPlan(plan) {
  const coachLine = $("#coachLine");
  const revisionQueue = $("#revisionQueue");
  const dailyMissions = $("#dailyMissions");
  const coachWallet = $("#coachWallet");
  if (!coachLine || !revisionQueue || !dailyMissions || !coachWallet) {
    return;
  }

  state.smartPlan = plan || defaultSmartPlan();
  const activePlan = state.smartPlan;
  const wallet = activePlan.wallet || {};
  coachLine.textContent = activePlan.coach_line || defaultSmartPlan().coach_line;
  coachWallet.innerHTML = `
    <span>Lv ${Number(wallet.level || 1)}</span>
    <strong>${Number(wallet.xp || 0)} XP</strong>
    <span>${Number(wallet.coins || 0)} coins</span>
  `;

  const queue = activePlan.revision_queue || [];
  revisionQueue.innerHTML = queue.length
    ? `
      <button class="revision-start" type="button" data-smart-revision-all>
        <span>Start Queue</span>
        <strong>${queue.length} patterns</strong>
      </button>
      ${queue.map((item, index) => `
        <button class="revision-chip" type="button" data-smart-revision="${Number(item.id)}">
          <span>${index + 1}</span>
          <strong>${escapeHtml(item.name)}</strong>
          <em>${escapeHtml(item.reason || `${Number(item.mastery || 0)}% mastery`)}</em>
        </button>
      `).join("")}
    `
    : `<div class="smart-empty">No weak queue yet. Start a quick set to create your first signal.</div>`;

  const missions = activePlan.missions?.length ? activePlan.missions : defaultSmartPlan().missions;
  dailyMissions.innerHTML = missions.map((mission) => {
    const reward = mission.reward || {};
    const percent = clampProgressPercent(mission.percent ?? ((Number(mission.progress || 0) / Number(mission.target || 1)) * 100));
    const rewardText = [
      reward.xp ? `${reward.xp} XP` : "",
      reward.coins ? `${reward.coins} coins` : "",
      reward.streak_shields ? `${reward.streak_shields} shield` : "",
    ].filter(Boolean).join(" + ");
    return `
      <article class="mission-row ${mission.completed ? "is-complete" : ""}">
        <div class="mission-main">
          <div class="mission-title-line">
            <strong>${escapeHtml(mission.title)}</strong>
            <span>${Number(mission.progress || 0)}/${Number(mission.target || 0)} ${escapeHtml(mission.unit || "")}</span>
          </div>
          <p>${escapeHtml(mission.description || "")}</p>
          <div class="mission-track"><div style="width: ${percent}%"></div></div>
          <span class="mission-reward">${mission.reward_claimed ? "Reward earned" : escapeHtml(rewardText || "Reward")}</span>
        </div>
        <button class="mission-action" type="button" data-mission-key="${escapeHtml(mission.key)}">
          ${mission.completed ? "Review" : escapeHtml(mission.action?.label || "Start")}
        </button>
      </article>
    `;
  }).join("");

  if (state.renderedSmartPlanOnce) {
    const newlyCompleted = missions.find((mission) =>
      mission.completed
      && mission.reward_claimed
      && !state.celebratedMissionKeys.has(mission.key)
    );
    if (newlyCompleted) {
      state.celebratedMissionKeys.add(newlyCompleted.key);
      triggerConfetti("mission");
      triggerHaptic("success");
      playTone("mission");
    }
  }
  missions.forEach((mission) => {
    if (mission.completed && mission.reward_claimed) {
      state.celebratedMissionKeys.add(mission.key);
    }
  });
  state.renderedSmartPlanOnce = true;
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

function clampProgressPercent(value) {
  const number = Number(value);
  if (!Number.isFinite(number)) {
    return 0;
  }
  return Math.max(0, Math.min(100, Math.round(number)));
}

function allCatalogPatternsWithContext() {
  return state.catalog.flatMap((category) =>
    (category.topics || []).flatMap((topic) =>
      (topic.patterns || []).map((pattern) => ({ category, topic, pattern }))
    )
  );
}

function progressForPattern(pattern) {
  const saved = state.patternProgress.get(Number(pattern?.id)) || {};
  const attempts = Number(saved.total_attempts || 0);
  const correct = Number(saved.correct_attempts || 0);
  const wrong = Number(saved.wrong_attempts ?? Math.max(attempts - correct, 0));
  const avgTime = Number(saved.avg_time_seconds || 0);
  const weaknessScore = Number(saved.weakness_score || 0);
  const mastery = clampProgressPercent(Number(saved.mastery_score || 0) * 100);
  const accuracy = attempts ? clampProgressPercent((correct / attempts) * 100) : 0;
  const statusKey = saved.status || (attempts === 0 ? "locked" : mastery >= 80 ? "mastered" : mastery >= 55 ? "improving" : "learning");
  const status = {
    locked: "Locked",
    learning: "Learning",
    improving: "Improving",
    mastered: "Mastered",
  }[statusKey] || "Learning";

  return {
    attempts,
    correct,
    wrong,
    avgTime,
    weaknessScore,
    lastPracticedAt: saved.last_practiced_at || null,
    openMistakes: Number(saved.open_mistakes || 0),
    mastery,
    accuracy,
    status,
    statusKey,
  };
}

function summarizePatternContexts(contexts) {
  const total = contexts.length;
  const rows = contexts.map(({ pattern }) => progressForPattern(pattern));
  const practiced = rows.filter((item) => item.attempts > 0).length;
  const mastered = rows.filter((item) => item.mastery >= 80).length;
  const attempts = rows.reduce((sum, item) => sum + item.attempts, 0);
  const correct = rows.reduce((sum, item) => sum + item.correct, 0);
  const wrong = rows.reduce((sum, item) => sum + item.wrong, 0);
  const avgMastery = total
    ? clampProgressPercent(rows.reduce((sum, item) => sum + item.mastery, 0) / total)
    : 0;
  const coverage = total ? clampProgressPercent((practiced / total) * 100) : 0;
  const accuracy = attempts ? clampProgressPercent((correct / attempts) * 100) : 0;

  return {
    total,
    practiced,
    mastered,
    attempts,
    correct,
    wrong,
    avgMastery,
    coverage,
    accuracy,
  };
}

function summarizeTopic(topic) {
  return summarizePatternContexts((topic?.patterns || []).map((pattern) => ({ pattern })));
}

function summarizeCategory(category) {
  return summarizePatternContexts(
    (category?.topics || []).flatMap((topic) =>
      (topic.patterns || []).map((pattern) => ({ topic, pattern }))
    )
  );
}

function summarizeAllProgress() {
  return summarizePatternContexts(allCatalogPatternsWithContext());
}

function formatLastPracticed(value) {
  if (!value) {
    return "Never";
  }
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return "Recent";
  }
  const diffMs = Date.now() - date.getTime();
  const diffDays = Math.max(0, Math.floor(diffMs / 86400000));
  if (diffDays === 0) {
    return "Today";
  }
  if (diffDays === 1) {
    return "Yesterday";
  }
  return `${diffDays}d ago`;
}

function statusClass(statusKey) {
  return `is-${String(statusKey || "learning").replace(/[^a-z0-9-]/gi, "")}`;
}

function progressCategories() {
  return state.catalog.filter((category) => (category.topics || []).some((topic) => (topic.patterns || []).length));
}

function getProgressCategory() {
  return progressCategories().find((category) => Number(category.id) === Number(state.progressCategoryId)) || null;
}

function getProgressTopic() {
  return (getProgressCategory()?.topics || []).find((topic) => Number(topic.id) === Number(state.progressTopicId)) || null;
}

function getProgressPattern() {
  return (getProgressTopic()?.patterns || []).find((pattern) => Number(pattern.id) === Number(state.progressPatternId)) || null;
}

function findPatternContext(patternId) {
  return allCatalogPatternsWithContext().find(({ pattern }) => Number(pattern.id) === Number(patternId)) || null;
}

function ensureProgressSelection() {
  const categories = progressCategories();
  if (!categories.length) {
    state.progressCategoryId = null;
    state.progressTopicId = null;
    state.progressPatternId = null;
    return;
  }

  if (!categories.some((category) => Number(category.id) === Number(state.progressCategoryId))) {
    const activeCategory = categories.find((category) => Number(category.id) === Number(state.activeCategoryId));
    state.progressCategoryId = (activeCategory || categories[0]).id;
  }

  const category = getProgressCategory();
  const topics = (category?.topics || []).filter((topic) => (topic.patterns || []).length);
  if (!topics.some((topic) => Number(topic.id) === Number(state.progressTopicId))) {
    state.progressTopicId = topics[0]?.id || null;
  }

  const topic = getProgressTopic();
  const patterns = topic?.patterns || [];
  if (!patterns.some((pattern) => Number(pattern.id) === Number(state.progressPatternId))) {
    state.progressPatternId = patterns[0]?.id || null;
  }
}

function renderProgressTracker() {
  const categoryTabs = $("#progressCategoryTabs");
  const topicList = $("#progressTopicList");
  const patternList = $("#progressPatternList");
  const detail = $("#progressPatternDetail");
  const snapshot = $("#progressSnapshot");
  if (!categoryTabs || !topicList || !patternList || !detail || !snapshot) {
    return;
  }

  ensureProgressSelection();
  const categories = progressCategories();
  if (!categories.length) {
    snapshot.innerHTML = "";
    categoryTabs.innerHTML = `<div class="empty-state">No progress catalog available.</div>`;
    topicList.innerHTML = "";
    patternList.innerHTML = "";
    detail.innerHTML = `<div class="empty-state">Load the catalog to track patterns.</div>`;
    return;
  }

  const overall = summarizeAllProgress();
  snapshot.innerHTML = `
    <div class="progress-ring" style="--ring:${overall.avgMastery}%">
      <strong>${overall.avgMastery}%</strong>
      <span>Mastery</span>
    </div>
    <div class="progress-snapshot-stack">
      <div class="progress-snapshot-row">
        <span>Coverage</span>
        <strong>${overall.practiced}/${overall.total}</strong>
        <div class="mini-track"><div style="width: ${overall.coverage}%"></div></div>
      </div>
      <div class="progress-snapshot-row">
        <span>Mastered</span>
        <strong>${overall.mastered}/${overall.total}</strong>
        <div class="mini-track"><div style="width: ${overall.total ? Math.round((overall.mastered / overall.total) * 100) : 0}%"></div></div>
      </div>
      <div class="progress-snapshot-row">
        <span>Accuracy</span>
        <strong>${overall.accuracy}%</strong>
        <div class="mini-track"><div style="width: ${overall.accuracy}%"></div></div>
      </div>
    </div>
  `;

  categoryTabs.innerHTML = categories.map((category) => {
    const summary = summarizeCategory(category);
    const active = Number(category.id) === Number(state.progressCategoryId);
    return `
      <button class="progress-category-tab ${active ? "is-active" : ""}" type="button" data-progress-category-id="${category.id}">
        <strong>${escapeHtml(category.name)}</strong>
        <span>${summary.mastered}/${summary.total} mastered</span>
        <div class="mini-track"><div style="width: ${summary.coverage}%"></div></div>
      </button>
    `;
  }).join("");

  const category = getProgressCategory();
  const topics = (category?.topics || []).filter((topic) => (topic.patterns || []).length);
  topicList.innerHTML = topics.length
    ? topics.map((topic) => {
        const summary = summarizeTopic(topic);
        const active = Number(topic.id) === Number(state.progressTopicId);
        return `
          <button class="progress-topic-button ${active ? "is-active" : ""}" type="button" data-progress-topic-id="${topic.id}">
            <strong>${escapeHtml(topic.name)}</strong>
            <span>${summary.coverage}% unlocked - ${summary.avgMastery}% mastery</span>
          </button>
        `;
      }).join("")
    : `<div class="empty-state">No topics in this category.</div>`;

  const topic = getProgressTopic();
  const patterns = topic?.patterns || [];
  patternList.innerHTML = patterns.length
    ? patterns.map((pattern) => {
        const progress = progressForPattern(pattern);
        const active = Number(pattern.id) === Number(state.progressPatternId);
        return `
          <button class="progress-pattern-card ${active ? "is-active" : ""} ${statusClass(progress.statusKey)}" type="button" data-progress-pattern-id="${pattern.id}">
            <span class="progress-pattern-topline">
              <strong>${escapeHtml(pattern.name)}</strong>
              <em>${progress.status}</em>
            </span>
            <span>${progress.attempts} tried - ${progress.correct} correct - ${progress.wrong} wrong</span>
            <div class="mini-track"><div style="width: ${progress.mastery}%"></div></div>
          </button>
        `;
      }).join("")
    : `<div class="empty-state">No patterns in this topic.</div>`;

  renderProgressPatternDetail();
}

function renderProgressPatternDetail() {
  const detail = $("#progressPatternDetail");
  if (!detail) {
    return;
  }

  const pattern = getProgressPattern();
  const topic = getProgressTopic();
  const category = getProgressCategory();
  if (!pattern) {
    detail.innerHTML = `<div class="empty-state">Select a pattern to see its progress.</div>`;
    return;
  }

  const progress = progressForPattern(pattern);
  const variantCount = Number(pattern.variant_count || 0);
  const weakLabel = progress.weaknessScore ? `${Math.round(progress.weaknessScore)}/100` : "New";
  detail.innerHTML = `
    <div class="progress-detail-head">
      <span>${escapeHtml(category?.name || "Category")} / ${escapeHtml(topic?.name || "Topic")}</span>
      <strong>${escapeHtml(progress.status)}</strong>
    </div>
    <h3>${escapeHtml(pattern.name)}</h3>
    <p>${escapeHtml(pattern.description || "Practice pattern")}</p>
    <div class="progress-detail-gauge" style="--ring:${progress.mastery}%">
      <strong>${progress.mastery}%</strong>
      <span>mastery</span>
    </div>
    <div class="progress-detail-grid">
      <div><span>Practiced</span><strong>${progress.attempts}</strong></div>
      <div><span>Correct</span><strong>${progress.correct}</strong></div>
      <div><span>Wrong</span><strong>${progress.wrong}</strong></div>
      <div><span>Accuracy</span><strong>${progress.accuracy}%</strong></div>
      <div><span>Speed</span><strong>${progress.avgTime ? `${Math.round(progress.avgTime)}s` : "0s"}</strong></div>
      <div><span>Last</span><strong>${escapeHtml(formatLastPracticed(progress.lastPracticedAt))}</strong></div>
      <div><span>Weak Score</span><strong>${escapeHtml(weakLabel)}</strong></div>
      <div><span>Variants</span><strong>${variantCount}</strong></div>
    </div>
    <div class="progress-action-row">
      <button class="primary-button full-width" type="button" data-progress-practice-pattern="${pattern.id}">Practice this pattern</button>
      <button class="quiet-button full-width" type="button" data-adaptive-practice="${pattern.id}">Smart weak drill</button>
    </div>
  `;
}

function preparePatternPracticeFromProgress(patternId) {
  const context = findPatternContext(patternId);
  if (!context) {
    showStatus("This pattern is not available in the current catalog.");
    return;
  }

  clearGameMode();
  state.activeCategoryId = context.category.id;
  state.activeTopicId = context.topic.id;
  state.selectedPatternIds = new Set([Number(context.pattern.id)]);
  state.selectedMode = "quick";
  document.querySelectorAll("[data-mode]").forEach((button) => {
    button.classList.toggle("is-active", button.dataset.mode === "quick");
  });
  renderCatalog();
  setScreen("practice");
}

function renderMistakes(mistakes, patternIds) {
  state.mistakes = mistakes || [];
  state.mistakePatternIds = patternIds.map(Number).filter(Boolean);
  state.profileStats.mistake_count = state.mistakes.length;
  $("#practiceMistakesButton").disabled = state.mistakePatternIds.length === 0;
  renderProgressVisuals();

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
      <div class="mistake-answer-grid">
        <div>
          <span>Your answer</span>
          <strong>${escapeHtml(item.selected_option ?? "Not answered")}</strong>
        </div>
        <div>
          <span>Correct</span>
          <strong>${escapeHtml(item.correct_option ?? "Check options")}</strong>
        </div>
      </div>
      <div class="mistake-why">
        <span>Why this went wrong</span>
        <p>${escapeHtml(item.explanation || "Review the setup, then solve one similar question immediately.")}</p>
      </div>
      <div class="mistake-actions">
        <button class="primary-button" type="button" data-mistake-retry="${item.id}">Retry exact</button>
        <button class="quiet-button" type="button" data-mistake-similar="${item.pattern_id}">Similar</button>
        <button class="quiet-button" type="button" data-mistake-pattern="${item.pattern_id}">Pattern</button>
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

function getPatternVariantNames(pattern) {
  return Array.isArray(pattern?.variant_names) ? pattern.variant_names : [];
}

function getPatternVariantSelection(patternId) {
  const key = Number(patternId);
  return state.patternVariantSelection[key] || null;
}

function getPatternById(patternId) {
  const id = Number(patternId);
  return state.catalog
    .flatMap((category) => category.topics || [])
    .flatMap((topic) => topic.patterns || [])
    .find((pattern) => Number(pattern.id) === id) || null;
}

function getVariantSelectionLabel(pattern, selectedVariant) {
  const variantNames = getPatternVariantNames(pattern);
  const variants = Array.isArray(selectedVariant)
    ? selectedVariant.filter((name) => variantNames.includes(name))
    : [];

  if (!variants.length) {
    return "All variants";
  }

  const labels = variants.map((variant) => (variant.includes("::") ? variant.split("::").pop() : variant));
  if (labels.length <= 2) {
    return labels.join(", ");
  }
  return `${labels.length} selected`;
}

function renderVariantPickerModal() {
  const host = document.getElementById("variantPickerHost");
  if (!host) {
    return;
  }

  const patternId = Number(state.variantPickerPatternId);
  if (!patternId) {
    host.hidden = true;
    host.innerHTML = "";
    return;
  }

  const pattern = getPatternById(patternId);
  const variantNames = getPatternVariantNames(pattern);
  if (!pattern || variantNames.length <= 1) {
    host.hidden = true;
    host.innerHTML = "";
    return;
  }

  const draft = Array.isArray(state.variantPickerDraft) ? state.variantPickerDraft : [];
  const selectedSet = new Set(draft);
  const summary = draft.length
    ? (() => {
        const labels = draft.map((variant) => (variant.includes("::") ? variant.split("::").pop() : variant));
        if (labels.length <= 2) {
          return labels.join(", ");
        }
        return `${labels.length} selected`;
      })()
    : "All variants";
  const anchor = state.variantPickerAnchor || { x: window.innerWidth / 2, y: window.innerHeight / 2 };
  const left = Math.min(Math.max(anchor.x, 120), window.innerWidth - 120);
  const top = Math.min(Math.max(anchor.y + 4, 80), window.innerHeight - 80);

  host.hidden = false;
  host.innerHTML = `
    <div class="variant-picker-backdrop" data-variant-picker-close="true"></div>
    <div class="variant-picker-modal" role="dialog" aria-modal="true" aria-label="Choose variants for ${escapeHtml(pattern.name)}" style="left: ${left}px; top: ${top}px; transform: translateX(-50%);">
      <div class="variant-picker-header">
        <div>
          <div class="variant-picker-kicker">Variants</div>
          <strong>${escapeHtml(pattern.name)}</strong>
        </div>
        <button type="button" class="variant-picker-close" data-variant-picker-close="true" aria-label="Close variant picker">×</button>
      </div>
      <div class="variant-picker-summary">${escapeHtml(summary)}</div>
      <div class="variant-picker-list">
        ${variantNames.map((variant) => {
          const label = variant.includes("::") ? variant.split("::").pop() : variant;
          const checked = selectedSet.has(variant) ? "checked" : "";
          return `
            <label class="variant-option-row">
              <input type="checkbox" data-variant-option="true" data-pattern-id="${pattern.id}" data-variant-name="${escapeHtml(variant)}" ${checked}>
              <span>${escapeHtml(label)}</span>
            </label>
          `;
        }).join("")}
      </div>
      <div class="variant-picker-actions">
        <button type="button" class="quiet-button variant-picker-cancel" data-variant-picker-close="true">Cancel</button>
        <button type="button" class="primary-button variant-picker-done" data-variant-picker-done="true" data-pattern-id="${pattern.id}">Done</button>
      </div>
    </div>
  `;
}

function patternEffectiveVariantCount(pattern) {
  const names = getPatternVariantNames(pattern);
  const selected = getPatternVariantSelection(pattern.id);
  if (!names.length || !Array.isArray(selected) || selected.length === 0) {
    return Number(pattern.variant_count || 0);
  }
  return Math.min(
    names.filter((name) => selected.includes(name)).length,
    names.length
  );
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

  const patternList = $("#patternList");
  patternList.innerHTML = topicPatterns.map((pattern) => {
    const selected = state.selectedPatternIds.has(pattern.id);
    const variantNames = getPatternVariantNames(pattern);
    const selectedVariant = getPatternVariantSelection(pattern.id);
    const variantSummary = variantNames.length > 1
      ? getVariantSelectionLabel(pattern, selectedVariant)
      : "Default";

    const variantPicker = variantNames.length > 1
      ? `<div class="variant-action-wrap"><button class="variant-button" type="button" data-variant-button="true" data-pattern-id="${pattern.id}">${escapeHtml(variantSummary)}</button>${Array.isArray(selectedVariant) && selectedVariant.length ? `<div class="selected-variant-inline">${escapeHtml(getVariantSelectionLabel(pattern, selectedVariant))}</div>` : ""}</div>`
      : "";

    return `
      <div class="pattern-button ${selected ? "is-selected" : ""}" data-pattern-id="${pattern.id}" tabindex="0" role="button" aria-pressed="${selected ? "true" : "false"}">
        <span class="pattern-check">${selected ? "OK" : ""}</span>
        <div class="pattern-copy">
          <strong>${escapeHtml(pattern.name)}</strong>
          <span>${escapeHtml(pattern.description || "Practice pattern")}</span>
        </div>
        <div class="pattern-meta-row">
          <span class="variant-pill">${patternEffectiveVariantCount(pattern)} / ${pattern.variant_count} variants</span>
          ${renderPatternProgress(pattern.id)}
        </div>
        ${variantPicker}
      </div>
    `;
  }).join("");

  let host = document.getElementById("variantPickerHost");
  if (!host) {
    host = document.createElement("div");
    host.id = "variantPickerHost";
    host.setAttribute("aria-live", "polite");
    document.body.appendChild(host);
  }
  renderVariantPickerModal();
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
  const variantCount = selected.reduce((sum, pattern) => sum + patternEffectiveVariantCount(pattern), 0);
  $("#variantCount").textContent = `${variantCount} variants`;
  $("#selectedPatternCount").textContent = selected.length;
  $("#selectedModeLabel").textContent = MODE_CONFIG[state.selectedMode].label;
  $("#startButton").disabled = selected.length === 0;

  $("#selectionList").innerHTML = selected.length
    ? selected.map((pattern) => `
        <div class="selection-item">
          <strong>${escapeHtml(pattern.name)}</strong>
          <span>${patternEffectiveVariantCount(pattern)} / ${pattern.variant_count} variants</span>
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

function getGameTargetCount(game) {
  const requested = Number(game?.targetCount || MODE_CONFIG.quick.targetCount);
  return Math.max(3, Math.min(Number.isFinite(requested) ? requested : MODE_CONFIG.quick.targetCount, GAME_TARGET_CAP));
}

function gameModeTileIcon(key) {
  return {
    vedicSprint: "x2",
    cricketChase: "6",
    mistakeRevenge: "!",
    directionMaze: "N",
    discountShop: "%",
    aptitudeHeist: "VH",
    marketTrader: "MT",
    trainControl: "TC",
    escapeGrid: "EG",
    auctionBattle: "AB",
  }[key] || "GO";
}

function gameDifficultyLabel(mode) {
  const range = mode?.difficultyRange || mode?.adaptiveDifficultyRange;
  if (Array.isArray(range) && range.length >= 2) {
    const avg = (Number(range[0]) + Number(range[1])) / 2;
    if (avg <= 2) {
      return "Easy";
    }
    if (avg <= 3.5) {
      return "Medium";
    }
    return "Hard";
  }
  return mode?.flagship ? "Elite" : "Mixed";
}

function gameRewardText(mode, targetCount) {
  const base = Math.max(40, targetCount * (mode?.flagship ? 18 : 12));
  return `${base} XP`;
}

function gameThumbnailClass(key) {
  return `thumb-${String(key || "default").replace(/[^a-z0-9-]/gi, "")}`;
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

  const orderedGames = games.slice().sort((a, b) => Number(Boolean(b.mode.flagship)) - Number(Boolean(a.mode.flagship)));
  grid.innerHTML = orderedGames.map(({ key, mode }) => {
    const patternCount = resolveGamePatternIds(mode).length;
    const targetCount = getGameTargetCount(mode);
    const launching = state.launchingGameId === key;
    const unavailable = key === "mistakeRevenge" && patternCount === 0;
    const continuing = state.activeGameId === key && state.session && !state.finishingGameEarly;
    const actionText = unavailable ? "Need misses" : launching ? "Loading" : continuing ? "Continue" : "Play";
    const patternText = unavailable ? "Mistake book" : `${patternCount || "Auto"} patterns`;
    const classes = ["game-mode-card", mode.flagship ? "is-flagship" : "", continuing ? "is-continuing" : "", gameThumbnailClass(key)].filter(Boolean).join(" ");
    return `
      <button class="${classes}" type="button" data-game-id="${escapeHtml(key)}" style="--game-accent: ${escapeHtml(mode.accent || "#0f766e")}" aria-label="${escapeHtml(actionText)} ${escapeHtml(mode.title)}" ${launching || unavailable ? "disabled" : ""}>
        <div class="game-mode-glow" aria-hidden="true"></div>
        <div class="game-mode-thumb" aria-hidden="true"><span>${escapeHtml(gameModeTileIcon(key))}</span></div>
        <div class="game-mode-card-head">
          <span class="game-mode-icon" aria-hidden="true">${escapeHtml(gameModeTileIcon(key))}</span>
          <span class="game-mode-label">
            <strong>${escapeHtml(mode.shortTitle || mode.title)}</strong>
            <small>${escapeHtml(mode.category || "Aptitude")}</small>
          </span>
        </div>
        <p>${escapeHtml(mode.subtitle || "A timed aptitude game mode.")}</p>
        <div class="game-mode-badges">
          <span>${escapeHtml(gameDifficultyLabel(mode))}</span>
          <span>${escapeHtml(gameRewardText(mode, targetCount))}</span>
          ${mode.flagship ? "<strong>Flagship</strong>" : continuing ? "<strong>Continue mission</strong>" : ""}
        </div>
        <div class="game-mode-meta">
          <span>${targetCount}Q</span>
          <span>${escapeHtml(patternText)}</span>
          <strong>${escapeHtml(actionText)}</strong>
        </div>
      </button>
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
  const configuredTerms = [
    ...(game.adaptivePatternTerms || []),
    ...(game.adaptiveTopicTerms || []),
    ...(game.adaptiveCategoryTerms || []),
  ];
  if (key === "vedicSprint") {
    return [...configuredTerms, "vedic math", "speed", "addition", "subtraction", "multiplication", "division", "tables", "squares", "cubes"];
  }
  if (key === "cricketChase") {
    return [...configuredTerms, "vedic math", "percentage", "calculation", "tables", "speed", "discount", "average", "ratio"];
  }
  if (key === "mistakeRevenge") {
    return [...configuredTerms, "mistake", "weak", "review"];
  }
  if (key === "directionMaze") {
    return [...configuredTerms, "direction", "distance", "turns", "clockwise", "shadow", "movement", "seating", "coded"];
  }
  if (key === "discountShop") {
    return [...configuredTerms, "percentage", "discount", "successive", "marked price", "selling price", "profit", "loss"];
  }
  if (key === "aptitudeHeist") {
    return [...configuredTerms, "percentage", "ratio", "average", "series", "direction", "speed", "number sense", "logic"];
  }
  if (key === "marketTrader") {
    return [...configuredTerms, "percentage", "profit", "loss", "average", "ratio", "change", "growth", "approximation"];
  }
  if (key === "trainControl") {
    return [...configuredTerms, "speed", "distance", "time", "direction", "movement", "relative", "schedule", "average"];
  }
  if (key === "escapeGrid") {
    return [...configuredTerms, "direction", "coded", "series", "arrangement", "logic", "percentage", "number"];
  }
  if (key === "auctionBattle") {
    return [...configuredTerms, "percentage", "discount", "profit", "loss", "ratio", "average", "marked price", "selling price"];
  }
  return configuredTerms;
}

function difficultyLevel(pattern) {
  const value = Number(pattern.difficulty_level ?? pattern.difficulty ?? 2);
  return Number.isFinite(value) ? value : 2;
}

function progressProfileForPattern(patternId) {
  const progress = state.patternProgress.get(Number(patternId)) || {};
  const attempts = Number(progress.total_attempts || 0);
  const mastery = Number(progress.mastery_score || 0);
  const correct = Number(progress.correct_attempts || 0);
  return { attempts, mastery, correct };
}

function adaptivePatternLimit(game) {
  const requested = Number(game?.adaptivePatternLimit || game?.patternPoolSize || getGameTargetCount(game));
  if (!Number.isFinite(requested)) {
    return Math.min(12, GAME_TARGET_CAP);
  }
  return Math.max(4, Math.min(Math.round(requested), GAME_TARGET_CAP));
}

function gameDifficultyScore(game, pattern) {
  const difficulty = difficultyLevel(pattern);
  const range = game.difficultyRange || game.adaptiveDifficultyRange;
  if (Array.isArray(range) && range.length >= 2) {
    const min = Number(range[0]);
    const max = Number(range[1]);
    if (Number.isFinite(min) && Number.isFinite(max)) {
      if (difficulty >= min && difficulty <= max) {
        return 2;
      }
      return -Math.min(2, Math.abs(difficulty - ((min + max) / 2)));
    }
  }
  return 0;
}

function patternWeaknessScore(pattern) {
  const progress = progressProfileForPattern(pattern.id);
  if (state.mistakePatternIds.map(Number).includes(Number(pattern.id))) {
    return 6;
  }
  if (!progress.attempts) {
    return 1.5;
  }
  if (progress.mastery < 0.45) {
    return 5;
  }
  if (progress.mastery < 0.7) {
    return 3;
  }
  if (progress.mastery >= 0.85) {
    return -1;
  }
  return 0.5;
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

  const naturalFit = terms.reduce((score, term) => {
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

  const selectedBoost = state.selectedPatternIds.has(Number(pattern.id)) ? 4 : 0;
  const weakBoost = game.adaptiveUseWeakAreas === false ? 0 : patternWeaknessScore(pattern);
  const difficultyBoost = gameDifficultyScore(game, pattern);
  const broadSupport = game.adaptiveBroadMatch ? 1 : 0;

  return naturalFit + selectedBoost + weakBoost + difficultyBoost + broadSupport;
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
  if (key === "mistakeRevenge") {
    return [];
  }

  const scored = available
    .map((pattern) => ({ pattern, score: patternScoreForGame(game, pattern) }))
    .filter((entry) => entry.score > 0 || game.adaptiveBroadMatch)
    .sort((a, b) => b.score - a.score || Number(a.pattern.id) - Number(b.pattern.id));

  if (scored.length) {
    const limit = adaptivePatternLimit(game);
    const chosen = [];
    const topicCounts = new Map();
    const maxPerTopic = Math.max(2, Number(game.maxPatternsPerTopic || 5));

    scored.forEach((entry) => {
      if (chosen.length >= limit) {
        return;
      }
      const topicName = entry.pattern.topic_name || "topic";
      const used = topicCounts.get(topicName) || 0;
      if (used >= maxPerTopic && scored.length > limit) {
        return;
      }
      chosen.push(Number(entry.pattern.id));
      topicCounts.set(topicName, used + 1);
    });

    if (chosen.length < Math.min(limit, scored.length)) {
      scored.forEach((entry) => {
        const id = Number(entry.pattern.id);
        if (chosen.length < limit && !chosen.includes(id)) {
          chosen.push(id);
        }
      });
    }

    return chosen;
  }

  const selected = getSelectedPatterns().map((pattern) => Number(pattern.id));
  if (selected.length) {
    return selected.slice(0, adaptivePatternLimit(game));
  }

  return available.slice(0, adaptivePatternLimit(game)).map((pattern) => Number(pattern.id));
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

  const gameKey = gameModeKey(game);
  state.launchingGameId = gameKey;
  state.activeGameId = gameModeKey(game);
  state.activeGameMode = game;
  state.gameState = {
    modeId: game.id,
    modeKey: state.activeGameId,
    startedAt: Date.now(),
  };
  state.activeGameMode.onLaunch?.(state.gameState);
  state.selectedPatternIds = new Set(patternIds);
  state.selectedMode = "quick";
  document.querySelectorAll("[data-mode]").forEach((button) => {
    button.classList.toggle("is-active", button.dataset.mode === "quick");
  });
  renderSelection();
  renderGameModes();
  clearStatus();
  setScreen("question");
  renderGameIntro();
  $("#questionCounter").textContent = `${game.shortTitle || game.title}`;
  $("#questionTimer").textContent = "Ready";
  $("#progressBar").style.width = "0%";
  $("#questionText").textContent = "Preparing game questions";
  $("#optionsGrid").innerHTML = "";
  $("#feedbackTitle").textContent = "Loading";
  $("#feedbackText").textContent = "Building a fast playable set. The first question will appear automatically.";
  $("#nextButton").disabled = true;
  $("#nextButton").textContent = "Preparing";

  try {
    const started = await startPractice({
      gameMode: game,
      patternIds,
      mode: "quick",
      targetCount: getGameTargetCount(game),
    });
    if (!started) {
      setScreen("arcade");
    }
  } finally {
    state.launchingGameId = null;
    renderGameModes();
  }
}

async function finishGameSessionEarly() {
  if (!state.session?.session_id || state.finishingGameEarly) {
    return;
  }

  state.finishingGameEarly = true;
  clearAutoAdvance();
  clearQuestionTimer();
  $("#nextButton").disabled = true;
  $("#nextButton").textContent = "Preparing report";

  try {
    const result = await api(`/api/session/${state.session.session_id}/stop`, { method: "POST" });
    syncGameStop();
    showResults(result.summary);
  } catch (error) {
    showStatus(error.message);
    $("#nextButton").disabled = false;
    $("#nextButton").textContent = "View game report";
    $("#nextButton").onclick = finishGameSessionEarly;
  } finally {
    state.finishingGameEarly = false;
  }
}

function clearGameMode() {
  state.activeGameId = null;
  state.activeGameMode = null;
  state.gameState = null;
  state.finishingGameEarly = false;
  document.body.classList.remove("is-game-active", "is-heist-immersive");
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
  document.body.classList.toggle("is-game-active", Boolean(state.activeGameMode));
  document.body.classList.toggle("is-heist-immersive", state.activeGameId === "aptitudeHeist");
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
  state.gameState.answered = false;
  state.gameState.lastAnswer = null;
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
  state.gameState.answered = true;
  state.gameState.lastAnswer = gameResult;
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
  state.currentStreak = 0;
  state.bestStreak = Math.max(state.bestStreak || 0, 0);
  updateQuestionHud(null);

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
    const variantSelection = Object.fromEntries(
      Object.entries(state.patternVariantSelection).map(([patternId, variants]) => [String(patternId), variants])
    );
    state.session = await api("/api/session/start", {
      method: "POST",
      timeoutMs: 120000,
      body: JSON.stringify({
        pattern_ids: patternIds,
        mode: modeKey,
        target_count: targetCount,
        telegram_user: state.telegramUser,
        variant_selection: variantSelection,
      }),
    });
    updateQuestionHud({ question_number: 1, total_questions: state.session.total_questions });
    setScreen("question");
    renderGameIntro();
    await loadNextQuestion();
    return true;
  } catch (error) {
    $("#selectionList").innerHTML = `<div class="empty-state">${escapeHtml(error.message)}</div>`;
    showStatus(error.message);
    return false;
  } finally {
    $("#startButton").disabled = false;
    $("#startButton").textContent = "Start practice";
  }
}

async function startPracticeWithPatternIds(patternIds, options = {}) {
  const available = new Set(
    state.catalog
      .flatMap((category) => category.topics || [])
      .flatMap((topic) => topic.patterns || [])
      .map((pattern) => Number(pattern.id))
  );
  const usableIds = patternIds.map(Number).filter((id) => available.has(id));
  if (!usableIds.length) {
    showStatus("No matching practice patterns are available in the current catalog.");
    return;
  }
  const modeKey = options.mode || "quick";
  state.selectedPatternIds = new Set(usableIds);
  state.selectedMode = modeKey;
  document.querySelectorAll("[data-mode]").forEach((button) => {
    button.classList.toggle("is-active", button.dataset.mode === modeKey);
  });
  renderSelection();
  setScreen("practice");
  await startPractice({
    patternIds: usableIds,
    mode: modeKey,
    targetCount: options.targetCount,
  });
}

async function startAdaptivePractice(patternIds = []) {
  const ids = patternIds.length ? patternIds : state.recommendedPatternIds;
  if (!ids.length) {
    showStatus("Practice a few questions first so the app can detect weak patterns.", "info");
    return;
  }
  await startPracticeWithPatternIds(ids);
}

async function startSmartRevision(patternIds = [], options = {}) {
  const queueIds = (state.smartPlan?.revision_queue || []).map((item) => Number(item.id)).filter(Boolean);
  const ids = patternIds.length ? patternIds : queueIds.length ? queueIds : state.recommendedPatternIds;
  if (!ids.length) {
    showStatus("Start one quick practice set first so the coach can build your revision queue.", "info");
    return;
  }
  await startPracticeWithPatternIds(ids, {
    mode: options.mode || (ids.length > 1 ? "focused" : "quick"),
    targetCount: options.targetCount ?? (ids.length > 1 ? 15 : 5),
  });
}

async function startMission(missionKey) {
  const mission = (state.smartPlan?.missions || []).find((item) => item.key === missionKey);
  if (!mission) {
    showStatus("Mission is not available yet.", "info");
    return;
  }
  const action = mission.action || {};
  if (action.type === "mistakes") {
    await startAllMistakeRetry();
    return;
  }
  const ids = (action.pattern_ids || []).map(Number).filter(Boolean);
  await startSmartRevision(ids, {
    mode: action.mode || "quick",
    targetCount: action.target_count ?? action.targetCount,
  });
}

async function startMistakeRetry(mistakeId) {
  if (!state.telegramUser?.id) {
    showStatus("Connect your personal profile before retrying saved mistakes.");
    return;
  }
  const mistake = state.mistakes.find((item) => Number(item.id) === Number(mistakeId));
  const patternId = Number(mistake?.pattern_id || 0);
  if (!patternId) {
    showStatus("This mistake is missing a practice pattern.");
    return;
  }

  clearGameMode();
  clearStatus();
  state.currentStreak = 0;
  updateQuestionHud(null);
  state.selectedPatternIds = new Set([patternId]);
  state.selectedMode = "quick";
  setScreen("question");
  $("#questionCounter").textContent = "Mistake retry";
  $("#questionTimer").textContent = "Ready";
  $("#questionText").textContent = "Loading saved mistake";
  $("#optionsGrid").innerHTML = "";
  $("#feedbackTitle").textContent = "Review";
  $("#feedbackText").textContent = "Retry the exact question from your mistake book.";
  $("#nextButton").disabled = true;

  try {
    state.session = await api("/api/session/start", {
      method: "POST",
      timeoutMs: 45000,
      body: JSON.stringify({
        pattern_ids: [patternId],
        mode: "quick",
        target_count: 1,
        telegram_user: state.telegramUser,
        retry_mistakes: true,
        mistake_ids: [Number(mistakeId)],
      }),
    });
    await loadNextQuestion();
  } catch (error) {
    showStatus(error.message);
    setScreen("progress");
  }
}

async function startMistakePatternRetry(patternId) {
  const id = Number(patternId);
  if (!id || !state.telegramUser?.id) {
    showStatus("Connect your personal profile before retrying saved mistakes.");
    return;
  }

  clearGameMode();
  clearStatus();
  state.currentStreak = 0;
  updateQuestionHud(null);
  setScreen("question");
  $("#questionCounter").textContent = "Pattern mistakes";
  $("#questionText").textContent = "Loading mistakes from this pattern";
  $("#optionsGrid").innerHTML = "";
  $("#feedbackTitle").textContent = "Review";
  $("#feedbackText").textContent = "Only open mistakes from this pattern will appear.";
  $("#nextButton").disabled = true;

  try {
    state.session = await api("/api/session/start", {
      method: "POST",
      timeoutMs: 45000,
      body: JSON.stringify({
        pattern_ids: [id],
        mode: "quick",
        target_count: 5,
        telegram_user: state.telegramUser,
        retry_mistakes: true,
        mistake_pattern_id: id,
      }),
    });
    await loadNextQuestion();
  } catch (error) {
    showStatus(error.message);
    setScreen("progress");
  }
}

async function startAllMistakeRetry() {
  if (!state.telegramUser?.id) {
    showStatus("Connect your personal profile before retrying saved mistakes.");
    return;
  }
  if (!state.mistakePatternIds.length) {
    showStatus("No open mistakes to retry.", "info");
    return;
  }

  clearGameMode();
  clearStatus();
  state.currentStreak = 0;
  updateQuestionHud(null);
  setScreen("question");
  $("#questionCounter").textContent = "Mistake book";
  $("#questionText").textContent = "Loading open mistakes";
  $("#optionsGrid").innerHTML = "";
  $("#feedbackTitle").textContent = "Review";
  $("#feedbackText").textContent = "Only open mistake-book questions will appear.";
  $("#nextButton").disabled = true;

  try {
    state.session = await api("/api/session/start", {
      method: "POST",
      timeoutMs: 45000,
      body: JSON.stringify({
        pattern_ids: state.mistakePatternIds,
        mode: "quick",
        target_count: 5,
        telegram_user: state.telegramUser,
        retry_mistakes: true,
      }),
    });
    await loadNextQuestion();
  } catch (error) {
    showStatus(error.message);
    setScreen("progress");
  }
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
  updateQuestionHud(null);

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
  updateQuestionHud(question);
  $("#optionsGrid").innerHTML = question.options.map((option, index) => `
    <button class="option-button" data-answer-index="${index}">
      <span class="option-label">${String.fromCharCode(65 + index)}</span>
      <span class="option-value">${escapeHtml(String(option))}</span>
    </button>
  `).join("");
  replayAnimation(document.querySelector(".question-panel"), "is-entering");
  replayAnimation($("#optionsGrid"), "is-entering");
  startQuestionTimer();
  syncGameQuestion(question);
}

async function submitAnswer(answerIndex) {
  if (state.answered) {
    return;
  }
  state.answered = true;
  clearQuestionTimer();
  clearAutoAdvance();
  markAnswerPending(answerIndex);

  let result;
  try {
    result = await api(`/api/session/${state.session.session_id}/answer`, {
      method: "POST",
      body: JSON.stringify({ answer_index: answerIndex }),
    });
  } catch (error) {
    state.answered = false;
    resetAnswerPending();
    startQuestionTimer();
    showStatus(error.message);
    return;
  }

  document.querySelectorAll(".option-button").forEach((button) => {
    const index = Number(button.dataset.answerIndex);
    button.disabled = true;
    button.classList.remove("is-pending", "is-dimmed");
    if (index === result.correct_option_index) {
      button.classList.add("is-correct");
    } else if (index === answerIndex) {
      button.classList.add("is-wrong");
    }
  });

  if (result.is_correct) {
    state.currentStreak += 1;
    state.bestStreak = Math.max(state.bestStreak, state.currentStreak);
    triggerHaptic("success");
    playTone("correct");
  } else {
    state.currentStreak = 0;
    triggerHaptic("error");
    playTone("wrong");
  }
  if (state.session) {
    state.session.score = result.score;
    state.session.answered = result.answered;
  }
  $("#progressBar").style.width = `${(result.answered / result.total_questions) * 100}%`;
  updateQuestionHud({ ...state.activeQuestion, question_number: result.answered + 1, total_questions: result.total_questions });
  $("#feedbackTitle").textContent = result.is_correct ? "Correct" : "Review";
  $("#feedbackText").textContent = result.explanation || `Correct answer: ${result.correct_option}`;
  playAnswerFeedback(result.is_correct);
  syncGameAnswer(result, answerIndex);
  const gameComplete = Boolean(state.activeGameMode?.isComplete?.(state.gameState));

  if (result.complete || gameComplete) {
    const finishEarly = gameComplete && !result.complete;
    $("#nextButton").textContent = finishEarly ? "View game report" : "View result";
    $("#nextButton").onclick = finishEarly ? finishGameSessionEarly : () => showResults(result.summary);
    $("#autoAdvanceText").textContent = finishEarly ? "Showing game report automatically..." : "Showing result automatically...";
    $("#autoAdvanceText").hidden = false;
    state.autoAdvanceId = window.setTimeout(finishEarly ? finishGameSessionEarly : () => showResults(result.summary), AUTO_ADVANCE_MS);
  } else {
    $("#nextButton").textContent = "Next question";
    $("#nextButton").onclick = loadNextQuestion;
    $("#autoAdvanceText").textContent = "Next question loading automatically...";
    $("#autoAdvanceText").hidden = false;
    state.autoAdvanceId = window.setTimeout(loadNextQuestion, AUTO_ADVANCE_MS);
  }
  $("#nextButton").disabled = false;
  if (result.complete) {
    window.setTimeout(() => loadProfile(), 250);
  }
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
  if (!summary.stopped && summary.total_questions && Number(summary.accuracy || 0) >= 80) {
    triggerConfetti("success");
    playTone("mission");
  }
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
    if (state.activeGameMode && state.gameState && !state.answered) {
      renderGamePanels();
    }
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
  document.addEventListener("change", (event) => {
    const variantToggle = event.target.closest("[data-variant-option]");
    if (!variantToggle) {
      return;
    }

    event.preventDefault();
    event.stopPropagation();

    const patternId = Number(variantToggle.dataset.patternId);
    const variantName = variantToggle.dataset.variantName;
    const current = Array.isArray(state.variantPickerDraft) ? state.variantPickerDraft : [];
    const next = current.includes(variantName)
      ? current.filter((name) => name !== variantName)
      : [...current, variantName];

    state.variantPickerDraft = next;
    renderVariantPickerModal();
    renderSelection();
  });

  document.addEventListener("click", (event) => {
    const tappedButton = event.target.closest("button");
    if (tappedButton && !tappedButton.disabled) {
      tapFeedback(tappedButton, event);
    }

    const soundToggleButton = event.target.closest("#soundToggleButton");
    if (soundToggleButton) {
      event.preventDefault();
      setSoundEnabled(!state.soundEnabled);
      playTone("tap");
      return;
    }

    const variantCloseButton = event.target.closest("[data-variant-picker-close]");
    if (variantCloseButton) {
      event.preventDefault();
      state.variantPickerPatternId = null;
      state.variantPickerDraft = [];
      state.variantPickerAnchor = null;
      renderVariantPickerModal();
      return;
    }

    const variantDoneButton = event.target.closest("[data-variant-picker-done]");
    if (variantDoneButton) {
      event.preventDefault();
      const patternId = Number(variantDoneButton.dataset.patternId);
      const selected = Array.isArray(state.variantPickerDraft) ? state.variantPickerDraft : [];
      if (!selected.length) {
        delete state.patternVariantSelection[patternId];
      } else {
        state.patternVariantSelection[patternId] = selected;
      }
      state.variantPickerPatternId = null;
      state.variantPickerDraft = [];
      state.variantPickerAnchor = null;
      renderPatterns();
      renderSelection();
      return;
    }

    const variantButton = event.target.closest("[data-variant-button]");
    if (variantButton) {
      event.preventDefault();
      event.stopPropagation();
      const patternId = Number(variantButton.dataset.patternId);
      const pattern = getPatternById(patternId);
      const variantNames = getPatternVariantNames(pattern);
      if (!pattern || variantNames.length <= 1) {
        return;
      }
      const rect = variantButton.getBoundingClientRect();
      state.variantPickerPatternId = patternId;
      state.variantPickerDraft = Array.isArray(getPatternVariantSelection(patternId)) ? [...getPatternVariantSelection(patternId)] : [];
      state.variantPickerAnchor = { x: rect.left + rect.width / 2, y: rect.bottom + 8 };
      renderVariantPickerModal();
      return;
    }

    const smartRevisionAllButton = event.target.closest("[data-smart-revision-all]");
    if (smartRevisionAllButton) {
      event.preventDefault();
      startSmartRevision();
      return;
    }

    const smartRevisionButton = event.target.closest("[data-smart-revision]");
    if (smartRevisionButton) {
      event.preventDefault();
      startSmartRevision([Number(smartRevisionButton.dataset.smartRevision)]);
      return;
    }

    const missionButton = event.target.closest("[data-mission-key]");
    if (missionButton) {
      event.preventDefault();
      startMission(missionButton.dataset.missionKey);
      return;
    }

    const progressPracticeButton = event.target.closest("[data-progress-practice-pattern]");
    if (progressPracticeButton) {
      event.preventDefault();
      preparePatternPracticeFromProgress(Number(progressPracticeButton.dataset.progressPracticePattern));
      return;
    }

    const adaptivePracticeButton = event.target.closest("[data-adaptive-practice]");
    if (adaptivePracticeButton) {
      event.preventDefault();
      const patternId = Number(adaptivePracticeButton.dataset.adaptivePractice);
      startAdaptivePractice(patternId ? [patternId] : []);
      return;
    }

    const progressPatternButton = event.target.closest("[data-progress-pattern-id]");
    if (progressPatternButton) {
      state.progressPatternId = Number(progressPatternButton.dataset.progressPatternId);
      renderProgressTracker();
      return;
    }

    const progressTopicButton = event.target.closest("[data-progress-topic-id]");
    if (progressTopicButton) {
      state.progressTopicId = Number(progressTopicButton.dataset.progressTopicId);
      const topic = getProgressTopic();
      state.progressPatternId = topic?.patterns?.[0]?.id || null;
      renderProgressTracker();
      return;
    }

    const progressCategoryButton = event.target.closest("[data-progress-category-id]");
    if (progressCategoryButton) {
      state.progressCategoryId = Number(progressCategoryButton.dataset.progressCategoryId);
      const category = getProgressCategory();
      const topic = (category?.topics || []).find((item) => (item.patterns || []).length);
      state.progressTopicId = topic?.id || null;
      state.progressPatternId = topic?.patterns?.[0]?.id || null;
      renderProgressTracker();
      return;
    }

    const gameButton = event.target.closest("[data-game-id]");
    if (gameButton) {
      event.preventDefault();
      launchGameMode(gameButton.dataset.gameId);
      return;
    }

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
    if (patternButton && !event.target.closest("[data-variant-button]") && !event.target.closest("[data-variant-option]") && !event.target.closest("[data-variant-picker-close]") && !event.target.closest("[data-variant-picker-done]") && !event.target.closest(".variant-picker-modal")) {
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

    const answerButton = event.target.closest("[data-answer-index]");
    if (answerButton) {
      submitAnswer(Number(answerButton.dataset.answerIndex));
      return;
    }

    const mistakeRetryButton = event.target.closest("[data-mistake-retry]");
    if (mistakeRetryButton) {
      event.preventDefault();
      startMistakeRetry(Number(mistakeRetryButton.dataset.mistakeRetry));
      return;
    }

    const mistakeSimilarButton = event.target.closest("[data-mistake-similar]");
    if (mistakeSimilarButton) {
      event.preventDefault();
      startPracticeWithPatternIds([Number(mistakeSimilarButton.dataset.mistakeSimilar)]);
      return;
    }

    const mistakePatternButton = event.target.closest("[data-mistake-pattern]");
    if (mistakePatternButton) {
      event.preventDefault();
      startMistakePatternRetry(Number(mistakePatternButton.dataset.mistakePattern));
      return;
    }

    const mistakeReviewButton = event.target.closest("[data-mistake-review]");
    if (mistakeReviewButton) {
      markMistakeReviewed(Number(mistakeReviewButton.dataset.mistakeReview));
    }
  });

  $("#selectTopicButton").addEventListener("click", selectWholeTopic);
  $("#gameModeGrid")?.addEventListener("click", (event) => {
    const gameButton = event.target.closest("[data-game-id]");
    if (!gameButton) {
      return;
    }
    event.preventDefault();
    event.stopPropagation();
    launchGameMode(gameButton.dataset.gameId);
  });
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
  $("#practiceMistakesButton").addEventListener("click", startAllMistakeRetry);
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
  setSoundEnabled(readSoundPreference());
  bindEvents();
  renderSmartPlan(null);
  renderProgressVisuals();
  void loadCatalog();
  void loadProfile();
  renderGameModes();
}

boot();
