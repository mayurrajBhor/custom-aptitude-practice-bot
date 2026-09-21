const MODE_CONFIG = {
  quick: { label: "Quick 10", targetCount: 10 },
  focused: { label: "Focused 20", targetCount: 20 },
  full: { label: "All Variants", targetCount: null },
};

const AUTO_ADVANCE_MS = 600;
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
  mistakes: [],
  mistakePatternIds: [],
  reminderSettings: null,
  webConfig: null,
  webAccessKey: null,
  webAccessDenied: false,
  progressCategoryId: null,
  progressTopicId: null,
  progressPatternId: null,
  currentStreak: 0,
  bestStreak: 0,
  soundEnabled: true,
  profileStats: {
    total_attempts: 0,
    total_correct: 0,
    accuracy: 0,
    mastery: 0,
    today_solved: 0,
    mistake_count: 0,
  },
  answerMode: "numpad",
  numpadValue: "",
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

function readAnswerModePreference() {
  try {
    const stored = window.localStorage?.getItem("aptitudeAnswerMode");
    return stored === "mcq" ? "mcq" : "numpad";
  } catch {
    return "numpad";
  }
}

function writeAnswerModePreference(mode) {
  try {
    window.localStorage?.setItem("aptitudeAnswerMode", mode === "mcq" ? "mcq" : "numpad");
  } catch {
    // Best-effort
  }
}

function setAnswerMode(mode) {
  state.answerMode = mode === "mcq" ? "mcq" : "numpad";
  writeAnswerModePreference(state.answerMode);

  document.querySelectorAll("[data-answer-mode]").forEach((btn) => {
    const isActive = btn.dataset.answerMode === state.answerMode;
    btn.classList.toggle("is-active", isActive);
    btn.setAttribute("aria-pressed", isActive ? "true" : "false");
  });

  syncQuestionModeDisplay(state.activeQuestion);
}

let autoSubmitTimer = null;

function clearAutoSubmitTimer() {
  if (autoSubmitTimer) {
    window.clearTimeout(autoSubmitTimer);
    autoSubmitTimer = null;
  }
}

function parseAnswerNumber(val) {
  if (val === null || val === undefined) {
    return null;
  }
  const s = String(val).trim().replace(/,/g, "").replace(/%$/, "");
  const mixed = s.match(/^(\d+)\s*(?:\(|\s)?(\d+)\/(\d+)\)?$/);
  if (mixed) {
    const w = parseInt(mixed[1], 10);
    const n = parseInt(mixed[2], 10);
    const d = parseInt(mixed[3], 10);
    return d ? w + (n / d) : null;
  }
  const frac = s.match(/^(-?\d+)\/(\d+)$/);
  if (frac) {
    const n = parseInt(frac[1], 10);
    const d = parseInt(frac[2], 10);
    return d ? n / d : null;
  }
  const f = parseFloat(s);
  return isNaN(f) ? null : f;
}

function isAnswerCorrect(typed, question) {
  if (!typed || !question) {
    return false;
  }
  const rawTyped = String(typed).trim();
  if (!rawTyped || rawTyped === "-") {
    return false;
  }
  const cleanTyped = rawTyped.toLowerCase().replace(/[%$,\s]/g, "");
  if (!cleanTyped) {
    return false;
  }

  const options = question.options || [];
  const correctIdx = question.correct_option_index;
  if (correctIdx === undefined || correctIdx === null || options[correctIdx] === undefined) {
    return false;
  }

  const correctOption = String(options[correctIdx]);
  const cleanCorrect = correctOption.toLowerCase().replace(/[%$,\s]/g, "");

  // 1. Direct string match
  if (cleanTyped === cleanCorrect) {
    return true;
  }

  // 2. Numeric / fraction value equivalence
  const typedNum = parseAnswerNumber(rawTyped);
  const correctNum = parseAnswerNumber(correctOption);
  if (typedNum !== null && correctNum !== null) {
    if (Math.abs(typedNum - correctNum) < 0.001) {
      return true;
    }
  }

  // 3. Categorical chip index (e.g. user pressed 1..N matching 1-based index)
  const isNumeric = options.every((opt) => {
    const s = String(opt).trim().replace(/[%$,\s]/g, "");
    return !isNaN(Number(s)) || s.includes("/");
  });
  if (!isNumeric && cleanTyped.match(/^\d+$/)) {
    const chosenIdx = parseInt(cleanTyped, 10) - 1;
    if (chosenIdx === correctIdx) {
      return true;
    }
  }

  return false;
}

function checkDigitInput() {
  if (state.answered || !state.numpadValue.trim() || !state.activeQuestion) {
    return;
  }

  // Check on every digit entered:
  // If the answer is correct, PASS IMMEDIATELY!
  if (isAnswerCorrect(state.numpadValue, state.activeQuestion)) {
    submitTypedAnswer();
  }
  // If false, DO NOT SUBMIT, DO NOT FAIL!
  // The user still has the rest of the 30-second timer to enter the correct answer.
}

function checkAutoSubmit() {
  checkDigitInput();
}

function handleManualSubmitAttempt() {
  if (state.answered || !state.activeQuestion) {
    return;
  }
  const typed = state.numpadValue.trim();
  if (!typed) {
    return;
  }

  if (isAnswerCorrect(typed, state.activeQuestion)) {
    submitTypedAnswer();
  } else {
    // Answer is not correct yet. DO NOT FAIL!
    // Give feedback that user should keep trying before the 15s timer runs out
    const display = $("#numpadDisplay");
    if (display) {
      replayAnimation(display, "numpad-wrong-shake");
    }
    playTone("wrong");
    triggerHaptic("error");
    const indicatorSub = $("#autoIndicatorSub");
    if (indicatorSub) {
      indicatorSub.textContent = "• Not correct yet! Keep trying";
    }
  }
}

function updateNumpadDisplay() {
  const displayVal = $("#numpadValue");
  const placeholder = $("#numpadPlaceholder");
  const clearBtn = $("#numpadClearBtn");
  const submitBtn = $("#numpadSubmitBtn");
  const indicatorTitle = $("#autoIndicatorTitle");
  const indicatorSub = $("#autoIndicatorSub");

  const val = state.numpadValue;
  if (displayVal) {
    displayVal.textContent = val;
  }
  if (placeholder) {
    placeholder.hidden = val.length > 0;
  }
  if (clearBtn) {
    clearBtn.style.display = val.length > 0 ? "grid" : "none";
  }
  if (submitBtn) {
    submitBtn.disabled = state.answered || !val.trim();
  }

  if (indicatorTitle && indicatorSub) {
    if (state.answered) {
      indicatorTitle.textContent = "Answer Locked";
      indicatorSub.textContent = "• Moving to next question...";
    } else if (val.trim().length > 0) {
      indicatorTitle.textContent = "Checking on digit...";
      indicatorSub.textContent = "• Auto-passes instantly when correct";
    } else {
      indicatorTitle.textContent = "15s Timer Active";
      indicatorSub.textContent = "• Auto-passes on correct answer";
    }
  }
}

function appendNumpadKey(key) {
  if (state.answered) {
    return;
  }
  if (state.numpadValue.length >= 14) {
    return;
  }

  if (key === "." && state.numpadValue.includes(".")) {
    return;
  }
  if (key === "%" && state.numpadValue.includes("%")) {
    return;
  }
  if (key === "/" && state.numpadValue.includes("/")) {
    return;
  }

  if (key === "-") {
    if (state.numpadValue.startsWith("-")) {
      state.numpadValue = state.numpadValue.slice(1);
    } else {
      state.numpadValue = "-" + state.numpadValue;
    }
  } else {
    state.numpadValue += key;
  }

  playTone("tap");
  triggerHaptic("light");
  updateNumpadDisplay();
  checkAutoSubmit();
  checkDigitInput();
}

function backspaceNumpad() {
  clearAutoSubmitTimer();
  if (state.answered) {
    return;
  }
  if (!state.numpadValue.length) {
    return;
  }
  state.numpadValue = state.numpadValue.slice(0, -1);
  playTone("tap");
  triggerHaptic("light");
  updateNumpadDisplay();
  checkDigitInput();
}

function clearNumpad() {
  clearAutoSubmitTimer();
  if (state.answered) {
    return;
  }
  if (!state.numpadValue.length) {
    return;
  }
  state.numpadValue = "";
  playTone("tap");
  triggerHaptic("light");
  updateNumpadDisplay();
}

function clearTypedAnswer() {
  clearAutoSubmitTimer();
  state.numpadValue = "";
  resetTypedAnswerPending();
  updateNumpadDisplay();
}

function highlightKeyElement(key) {
  const btn = document.querySelector(`[data-numpad-key="${key}"]`);
  if (btn) {
    replayAnimation(btn, "is-pressing");
  }
}

function markTypedAnswerPending(typed) {
  const display = $("#numpadDisplay");
  if (display) {
    display.classList.remove("is-correct", "is-wrong");
    display.classList.add("is-pending");
  }
  const submitBtn = $("#numpadSubmitBtn");
  if (submitBtn) {
    submitBtn.disabled = true;
  }
  document.querySelectorAll(".numpad-key").forEach((key) => {
    key.disabled = true;
  });

  const feedbackPanel = $("#feedbackPanel");
  if (feedbackPanel) {
    feedbackPanel.classList.remove("is-correct", "is-wrong");
    feedbackPanel.classList.add("is-checking");
  }
  $("#feedbackTitle").textContent = "Locked";
  $("#feedbackText").textContent = `Checking ${typed}...`;
  const burst = $("#answerBurst");
  if (burst) {
    burst.textContent = "Answer locked";
    burst.hidden = false;
    replayAnimation(burst, "answer-burst");
  }
}

function resetTypedAnswerPending() {
  const display = $("#numpadDisplay");
  if (display) {
    display.classList.remove("is-pending", "is-correct", "is-wrong");
  }
  document.querySelectorAll(".numpad-key").forEach((key) => {
    key.disabled = false;
  });
  updateNumpadDisplay();
  clearAnswerFeedback();
}

function syncQuestionModeDisplay(question = state.activeQuestion) {
  const optionsGrid = $("#optionsGrid");
  const numpadPanel = $("#numpadPanel");
  const isNumpad = state.answerMode === "numpad";

  if (optionsGrid) {
    optionsGrid.hidden = isNumpad;
  }
  if (numpadPanel) {
    numpadPanel.hidden = !isNumpad;
  }

  if (isNumpad && question) {
    const catOptions = $("#numpadCategoricalOptions");
    const options = question.options || [];
    const isNumeric = options.every((opt) => {
      const s = String(opt).trim().replace(/[%$,]/g, "");
      return !isNaN(Number(s)) || s.includes("/");
    });

    if (!isNumeric && catOptions) {
      catOptions.hidden = false;
      catOptions.innerHTML = options.map((opt, idx) => `
        <div class="numpad-categorical-chip">
          <strong>${idx + 1}</strong>
          <span>${escapeHtml(String(opt))}</span>
        </div>
      `).join("");
    } else if (catOptions) {
      catOptions.hidden = true;
      catOptions.innerHTML = "";
    }

    updateNumpadDisplay();
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
    const frequency = type === "correct" ? 620 : type === "wrong" ? 190 : 360;
    oscillator.type = type === "wrong" ? "sawtooth" : "sine";
    oscillator.frequency.setValueAtTime(frequency, context.currentTime);
    gain.gain.setValueAtTime(0.0001, context.currentTime);
    gain.gain.exponentialRampToValueAtTime(type === "tap" ? 0.018 : 0.045, context.currentTime + 0.02);
    gain.gain.exponentialRampToValueAtTime(0.0001, context.currentTime + 0.16);
    oscillator.connect(gain);
    gain.connect(context.destination);
    oscillator.start();
    oscillator.stop(context.currentTime + 0.18);
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
  const colors = ["#088475", "#126fb4", "#dff5f0", "#f7c66a"];
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

function initInternalProfile() {
  const userId = parseUserId(state.webConfig?.single_user_id) || 1;
  state.telegramUser = { id: userId };
  $("#userChip").textContent = "Personal";
  updateProfileNote("Personal profile synced automatically.");
}

function parseUserId(value) {
  const parsed = Number(value);
  return Number.isSafeInteger(parsed) && parsed > 0 ? parsed : null;
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
  const navTarget = name === "progress" ? "progress" : (name === "english" ? "english" : "practice");
  document.querySelector(`[data-screen-target="${navTarget}"]`)?.classList.add("is-active");
  try {
    window.localStorage?.setItem("aptitudeActiveScreen", name);
  } catch (e) {}
  if (name === "progress") {
    void renderAdvancedProgressDashboard();
    void renderLocalJournal();
  } else if (name === "english") {
    window.EnglishApp?.init();
    if (window.EnglishApp && typeof window.EnglishApp.init === "function") {
      window.EnglishApp.init();
    }
  }
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
    });
    renderUnlockProgress({ topics: [], patterns: [] });
    renderMistakes([], []);
    renderReminder(null);
    updateProfileNote("Personal profile is temporarily unavailable. Practice still works locally.");
    return;
  }

  updateProfileNote("Loading fast profile summary.");
  try {
    const profile = await api(`/api/profile/${state.telegramUser.id}/summary`, { timeoutMs: 12000 });
    renderProfileSummary(profile);
    updateProfileNote(profile.offline
      ? "Database is unavailable from this server, so live progress cannot be loaded here."
      : "Stats loaded. Syncing coach, mistakes, and progress map in the background.");
    if (profile.offline) {
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
    const recommendations = await api(`/api/profile/${state.telegramUser.id}/recommendations`, { timeoutMs: 24000 });
    applyRecommendationsPayload(recommendations);
    updateProfileNote(recommendations.offline ? "Recommendations are offline. Practice still works with local data." : "Recommendations loaded. Progress map is syncing.");
  } catch (error) {
    updateProfileNote(`Recommendations sync is delayed: ${error.message}`);
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
  applyRecommendationsPayload(profile);
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
  const todaySolved = $("#todaySolved");
  if (todaySolved) todaySolved.textContent = profile.today_solved || 0;
  const accuracyStat = $("#accuracyStat");
  if (accuracyStat) accuracyStat.textContent = `${profile.accuracy || 0}%`;
  const masteryStat = $("#masteryStat");
  if (masteryStat) masteryStat.textContent = `${profile.mastery || 0}%`;
  const totalSolved = $("#totalSolved");
  if (totalSolved) totalSolved.textContent = profile.total_attempts || 0;
  const totalCorrect = $("#totalCorrect");
  if (totalCorrect) totalCorrect.textContent = profile.total_correct || 0;
  const avgTime = $("#avgTime");
  if (avgTime) avgTime.textContent = `${profile.avg_time || 0}s`;
  const practiceMistakesButton = $("#practiceMistakesButton");
  if (practiceMistakesButton && typeof profile.mistake_count !== "undefined") {
    practiceMistakesButton.disabled = Number(profile.mistake_count || 0) === 0;
  }
  renderProgressVisuals();
}

function applyRecommendationsPayload(profile) {
  state.recommendedPatternIds = (profile.recommended_pattern_ids || state.recommendedPatternIds || []).map(Number).filter(Boolean);
  if (typeof profile.mistake_count !== "undefined") {
    state.profileStats.mistake_count = Number(profile.mistake_count || 0);
  }
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
    const mistakeList = $("#mistakeList");
    if (mistakeList) mistakeList.innerHTML = `<div class="empty-state">${escapeHtml(error.message)}</div>`;
    state.mistakePatternIds = [];
    const practiceMistakesButton = $("#practiceMistakesButton");
    if (practiceMistakesButton) practiceMistakesButton.disabled = true;
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
    const reminderText = $("#reminderText");
    if (reminderText) reminderText.textContent = error.message;
  }
}

function renderReminder(settings) {
  state.reminderSettings = settings || { enabled: false, reminder_time: "20:00", timezone: "Asia/Kolkata" };
  const reminderEnabled = $("#reminderEnabled");
  if (reminderEnabled) reminderEnabled.checked = Boolean(state.reminderSettings.enabled);
  const reminderTime = $("#reminderTime");
  if (reminderTime) reminderTime.value = state.reminderSettings.reminder_time || "20:00";
  const reminderText = $("#reminderText");
  if (reminderText) {
    reminderText.textContent = state.reminderSettings.enabled
      ? `Reminder active at ${state.reminderSettings.reminder_time || "20:00"}.`
      : "Telegram can remind you if you miss practice.";
  }
}

async function saveReminder() {
  if (!state.telegramUser?.id) {
    updateProfileNote("Connect a personal web profile before saving reminders.");
    return;
  }

  const saveReminderButton = $("#saveReminderButton");
  if (saveReminderButton) {
    saveReminderButton.disabled = true;
    saveReminderButton.textContent = "Saving";
  }
  try {
    const settings = await api(`/api/reminders/${state.telegramUser.id}`, {
      method: "POST",
      body: JSON.stringify({
        enabled: Boolean($("#reminderEnabled")?.checked),
        reminder_time: $("#reminderTime")?.value || "20:00",
        timezone: "Asia/Kolkata",
      }),
    });
    renderReminder(settings);
  } catch (error) {
    const reminderText = $("#reminderText");
    if (reminderText) reminderText.textContent = error.message;
  } finally {
    if (saveReminderButton) {
      saveReminderButton.disabled = false;
      saveReminderButton.textContent = "Save";
    }
  }
}

function renderUnlockProgress(progress) {
  const unlockList = $("#unlockList");
  if (!unlockList) return;
  const topics = progress?.topics || [];
  if (!topics.length) {
    unlockList.innerHTML = `<div class="empty-state">Start practicing to unlock progress.</div>`;
    return;
  }

  unlockList.innerHTML = topics.slice(0, 6).map((topic) => {
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
  void renderLocalJournal();
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
  const practiceMistakesButton = $("#practiceMistakesButton");
  if (practiceMistakesButton) {
    practiceMistakesButton.disabled = state.mistakePatternIds.length === 0;
  }
  renderProgressVisuals();

  const mistakeList = $("#mistakeList");
  if (!mistakeList) return;

  if (!mistakes.length) {
    mistakeList.innerHTML = `<div class="empty-state">No mistakes saved yet.</div>`;
    return;
  }

  mistakeList.innerHTML = mistakes.slice(0, 5).map((item) => `
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
  const left = window.innerWidth / 2;
  const top = window.innerHeight / 2;

  host.hidden = false;
  host.innerHTML = `
    <div class="variant-picker-backdrop" data-variant-picker-close="true"></div>
    <div class="variant-picker-modal" role="dialog" aria-modal="true" aria-label="Choose variants for ${escapeHtml(pattern.name)}" style="left: ${left}px; top: ${top}px; transform: translate(-50%, -50%);">
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
  state.numpadValue = "";
  resetTypedAnswerPending();
  $("#nextButton").disabled = true;
  $("#nextButton").textContent = "Next question";
  $("#feedbackTitle").textContent = "Answer";
  $("#feedbackText").textContent = "Choose an option or type your answer.";
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

  const rfBanner = $("#reinforcementBanner");
  if (rfBanner) {
    if (question.is_reinforcement) {
      const reasonText = question.reinforcement_reason === "hesitation"
        ? "You hesitated (&gt;10s) on this question earlier"
        : "You missed this question earlier";
      rfBanner.innerHTML = `
        <span class="rf-badge">🔁 REINFORCEMENT LOOP</span>
        <span>${reasonText}. <strong>Can you recall it in &lt; 5s now?</strong></span>
      `;
      rfBanner.hidden = false;
    } else {
      rfBanner.hidden = true;
      rfBanner.innerHTML = "";
    }
  }

  $("#optionsGrid").innerHTML = question.options.map((option, index) => `
    <button class="option-button" data-answer-index="${index}">
      <span class="option-label">${String.fromCharCode(65 + index)}</span>
      <span class="option-value">${escapeHtml(String(option))}</span>
    </button>
  `).join("");
  state.numpadValue = "";
  resetTypedAnswerPending();
  syncQuestionModeDisplay(question);
  replayAnimation(document.querySelector(".question-panel"), "is-entering");
  if (state.answerMode === "mcq") {
    replayAnimation($("#optionsGrid"), "is-entering");
  } else {
    replayAnimation($("#numpadPanel"), "is-entering");
  }
  startQuestionTimer();
  syncGameQuestion(question);
}

function finalizeAnswerResponse(result, effectiveIndex) {
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
    if (result.total_questions) {
      state.session.total_questions = result.total_questions;
    }
  }
  $("#progressBar").style.width = `${(result.answered / result.total_questions) * 100}%`;
  updateQuestionHud({ ...state.activeQuestion, question_number: result.answered + 1, total_questions: result.total_questions });
  $("#feedbackTitle").textContent = result.is_correct ? "Correct" : "Review";
  $("#feedbackText").textContent = result.explanation || `Correct answer: ${result.correct_option}`;
  const totalQs = result.total_questions || state.session?.total_questions || 1;
  $("#progressBar").style.width = `${(result.answered / totalQs) * 100}%`;
  updateQuestionHud({ ...state.activeQuestion, question_number: result.answered + 1, total_questions: totalQs });

  const timeTaken = Number(result.time_taken || 0);
  let speedBadgeHtml = "";
  if (result.speed_tier === "gmat_ready" || timeTaken < 5.0) {
    speedBadgeHtml = `<span class="recall-tier-badge badge-gmat-ready">⚡ GMAT-Ready (${timeTaken.toFixed(1)}s)</span>`;
  } else if (result.speed_tier === "acceptable" || timeTaken <= 12.0) {
    speedBadgeHtml = `<span class="recall-tier-badge badge-acceptable">🎯 Acceptable (${timeTaken.toFixed(1)}s)</span>`;
  } else {
    speedBadgeHtml = `<span class="recall-tier-badge badge-hesitation">🐢 Hesitation (${timeTaken.toFixed(1)}s)</span>`;
  }

  let loopbackNoticeHtml = "";
  if (result.repetition_queued) {
    const noticeText = result.repetition_reason === "hesitation"
      ? "Hesitation detected (&gt;10s): Queued to loop back in 3 questions for reinforcement!"
      : "Missed question: Queued to loop back in 3 questions &amp; at session end!";
    loopbackNoticeHtml = `<div class="loopback-notice"><span class="loopback-icon">🔁</span> ${noticeText}</div>`;
  }

  $("#feedbackTitle").innerHTML = `${result.is_correct ? "✓ Correct" : "✗ Review"} ${speedBadgeHtml}`;
  $("#feedbackText").innerHTML = `
    ${result.explanation ? `<div>${escapeHtml(result.explanation)}</div>` : `<div>Correct answer: <strong>${escapeHtml(String(result.correct_option))}</strong></div>`}
    ${loopbackNoticeHtml}
  `;
  playAnswerFeedback(result.is_correct);
  syncGameAnswer(result, effectiveIndex);
  const gameComplete = Boolean(state.activeGameMode?.isComplete?.(state.gameState));

  const advanceDelay = (result.repetition_queued || !result.is_correct) ? 2000 : AUTO_ADVANCE_MS;

  if (result.complete || gameComplete) {
    const finishEarly = gameComplete && !result.complete;
    $("#nextButton").textContent = finishEarly ? "View game report" : "View result";
    $("#nextButton").onclick = finishEarly ? finishGameSessionEarly : () => showResults(result.summary);
    $("#autoAdvanceText").textContent = finishEarly ? "Showing game report automatically..." : "Showing result automatically...";
    $("#autoAdvanceText").hidden = false;
    state.autoAdvanceId = window.setTimeout(finishEarly ? finishGameSessionEarly : () => showResults(result.summary), AUTO_ADVANCE_MS);
    state.autoAdvanceId = window.setTimeout(finishEarly ? finishGameSessionEarly : () => showResults(result.summary), advanceDelay);
  } else {
    $("#nextButton").textContent = "Next question";
    $("#nextButton").onclick = loadNextQuestion;
    $("#autoAdvanceText").textContent = "Next question loading automatically...";
    $("#autoAdvanceText").hidden = false;
    state.autoAdvanceId = window.setTimeout(loadNextQuestion, AUTO_ADVANCE_MS);
    state.autoAdvanceId = window.setTimeout(loadNextQuestion, advanceDelay);
  }
  $("#nextButton").disabled = false;
  if (result.complete) {
    window.setTimeout(() => loadProfile(), 250);
  }

  if (window.AptitudeLocalDB && state.activeQuestion) {
    const q = state.activeQuestion;
    const patternId = Number(q.pattern_id || 0);
    const ctx = findPatternContext(patternId);
    const category_name = ctx?.category?.name || "Quantitative Aptitude";
    const topic_name = ctx?.topic?.name || "General";
    const pattern_name = ctx?.pattern?.name || (patternId ? `Pattern #${patternId}` : "General Practice");

    let userAnswer = result.typed_answer;
    if (userAnswer === null || userAnswer === undefined) {
      if (effectiveIndex !== null && effectiveIndex !== undefined && Array.isArray(q.options)) {
        userAnswer = q.options[effectiveIndex];
      }
    }

    let correctAnswer = result.correct_option;
    if (correctAnswer === null || correctAnswer === undefined) {
      const cIdx = result.correct_option_index !== undefined ? result.correct_option_index : q.correct_option_index;
      if (cIdx !== null && cIdx !== undefined && Array.isArray(q.options)) {
        correctAnswer = q.options[cIdx];
      }
    }

    const attempt = {
      date: new Date().toISOString().slice(0, 10),
      timestamp: Date.now(),
      session_id: state.session?.session_id || "",
      category_name,
      topic_name,
      pattern_id: patternId,
      pattern_name,
      hybrid_type: q.hybrid_type || "",
      question_text: q.question_text || "",
      options: Array.isArray(q.options) ? q.options : [],
      selected_answer: effectiveIndex !== null && effectiveIndex !== undefined ? (q.options?.[effectiveIndex] ?? null) : null,
      typed_answer: result.typed_answer ?? null,
      correct_answer: correctAnswer ?? null,
      correct_option_index: result.correct_option_index !== undefined ? result.correct_option_index : (q.correct_option_index ?? null),
      is_correct: Boolean(result.is_correct),
      is_timeout: Boolean(result.is_timeout || (result.time_taken >= QUESTION_TIME_LIMIT_SECONDS && !result.is_correct)),
      is_skipped: false,
      time_taken: typeof result.time_taken === "number" ? result.time_taken : Number(result.time_taken) || 0,
      explanation: result.explanation || "",
      difficulty: q.difficulty !== undefined ? q.difficulty : 3,
      user_id: state.telegramUser?.id || null,
    };

    window.AptitudeLocalDB.recordLocalAttempt(attempt).catch((err) => {
      console.warn("Failed to record local attempt:", err);
    });
  }
}

async function submitAnswer(answerIndex) {
  if (state.answered) {
    return;
  }

  // If the clicked option is wrong, mark it and give feedback without failing the question yet
  if (state.activeQuestion && state.activeQuestion.correct_option_index !== undefined) {
    if (answerIndex !== state.activeQuestion.correct_option_index) {
      const clickedBtn = document.querySelector(`[data-answer-index="${answerIndex}"]`);
      if (clickedBtn) {
        clickedBtn.classList.add("is-wrong");
        clickedBtn.disabled = true;
      }
      playTone("wrong");
      triggerHaptic("error");
      const indicatorSub = $("#autoIndicatorSub");
      if (indicatorSub) {
        indicatorSub.textContent = "• Not correct yet! Keep trying";
      }
      return;
    }
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

  finalizeAnswerResponse(result, answerIndex);
}

async function submitTypedAnswer(customVal) {
  clearAutoSubmitTimer();
  if (state.answered) {
    return;
  }
  const typed = String(customVal ?? state.numpadValue ?? "").trim();
  if (!typed) {
    return;
  }
  state.answered = true;
  clearQuestionTimer();
  clearAutoAdvance();
  markTypedAnswerPending(typed);

  let result;
  try {
    result = await api(`/api/session/${state.session.session_id}/answer`, {
      method: "POST",
      body: JSON.stringify({ typed_answer: typed }),
    });
  } catch (error) {
    state.answered = false;
    resetTypedAnswerPending();
    startQuestionTimer();
    showStatus(error.message);
    return;
  }

  const display = $("#numpadDisplay");
  if (display) {
    display.classList.remove("is-pending");
    display.classList.add(result.is_correct ? "is-correct" : "is-wrong");
  }

  document.querySelectorAll(".option-button").forEach((button) => {
    const index = Number(button.dataset.answerIndex);
    button.disabled = true;
    button.classList.remove("is-pending", "is-dimmed");
    if (index === result.correct_option_index) {
      button.classList.add("is-correct");
    } else if (result.selected_option_index !== null && index === result.selected_option_index) {
      button.classList.add("is-wrong");
    }
  });

  finalizeAnswerResponse(result, result.selected_option_index ?? result.correct_option_index);
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

  // Display Average Time & Weak Questions Count
  const avgTime = summary.avg_time !== undefined ? summary.avg_time : 0.0;
  const weakCount = summary.weak_count !== undefined ? summary.weak_count : 0;
  const avgElem = $("#resultAvgTime");
  if (avgElem) avgElem.textContent = `${avgTime}s`;
  const weakElem = $("#resultWeakCount");
  if (weakElem) weakElem.textContent = `${weakCount}`;

  // Configure Re-Practice Weak Banner
  const banner = $("#weakRepracticeBanner");
  const rePracticeCount = $("#rePracticeWeakCount");
  const targetTotal = summary.total_questions || summary.planned_total_questions || 10;
  if (banner && rePracticeCount) {
    if (weakCount > 0) {
      banner.hidden = false;
      rePracticeCount.textContent = weakCount;
      rePracticeCount.textContent = `${weakCount} (${targetTotal}-Q Drill)`;
      const note = $("#weakRepracticeNote");
      if (note) {
        note.textContent = `${weakCount} question(s) took longer than average (${avgTime}s) or missed. Drill them across a full ${targetTotal}-question set!`;
      }
    } else {
      banner.hidden = true;
    }
  }

  renderGameResult(summary);
  setScreen("result");
  replayAnimation($("#resultPanel"), "is-complete");
  if (!summary.stopped && summary.total_questions && Number(summary.accuracy || 0) >= 80) {
    triggerConfetti("success");
    playTone("mission");
  }

  if (window.AptitudeLocalDB && summary) {
    window.AptitudeLocalDB.recordLocalSession({
      session_id: state.session?.session_id || summary.session_id,
      score: summary.score || 0,
      total_questions: summary.total_questions || summary.planned_total_questions || 0,
      accuracy: summary.accuracy || 0,
      avg_time: summary.avg_time || 0,
      weak_count: summary.weak_count || 0,
      stopped: Boolean(summary.stopped),
      user_id: state.telegramUser?.id || null,
      date: new Date().toISOString().slice(0, 10),
      timestamp: Date.now(),
    }).catch((err) => console.warn("Failed to record local session:", err));
  }
}

async function rePracticeWeakQuestions() {
  if (!state.session?.session_id) {
    showStatus("No active session to re-practice from.");
    return;
  }
  const sessionId = state.session.session_id;
  clearAutoAdvance();
  clearQuestionTimer();
  showStatus("Building weak questions drill session...");
  try {
    let clientHistory = [];
    if (window.AptitudeLocalDB) {
      try {
        const attempts = await window.AptitudeLocalDB.getAllLocalAttempts();
        clientHistory = (attempts || []).slice(0, 30);
      } catch {
        // best effort fallback
      }
    }
    const payload = await api(`/api/session/${sessionId}/re-practice-weak`, {
      method: "POST",
      body: JSON.stringify({
        history: clientHistory,
        target_count: state.session?.total_questions || undefined,
      }),
    });
    if (!payload?.session) {
      throw new Error("Failed to create weak questions session.");
    }
    state.session = payload.session;
    state.activeQuestion = null;
    state.currentQuestion = null;
    state.answered = false;
    state.selectedOptionIndex = null;
    clearTypedAnswer();
    clearStatus();
    updateQuestionHud({ question_number: 1, total_questions: state.session.total_questions });
    setScreen("question");
    await loadNextQuestion();
  } catch (error) {
    showStatus(`Cannot start weak practice: ${error.message}`);
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
    renderReview(review.questions || [], review.summary || {});
  } catch (error) {
    $("#reviewList").innerHTML = `<div class="empty-state">${escapeHtml(error.message)}</div>`;
  }
}

function renderReview(questions, summary = {}) {
  // Update review header with average time and slow count
  const metaElem = $("#reviewSpeedMeta");
  if (metaElem && summary.avg_time !== undefined) {
    metaElem.innerHTML = `<span>Avg Time: <strong class="badge">${summary.avg_time}s</strong></span> <span>Slow: <strong class="badge">${summary.slow_count || 0}</strong></span>`;
  }

  const reviewRePracticeBtn = $("#reviewRePracticeWeakButton");
  if (reviewRePracticeBtn) {
    const weakCount = summary.weak_count || 0;
    const drillTotal = summary.total_questions || summary.planned_total_questions || (questions.length || 10);
    if (weakCount > 0) {
      reviewRePracticeBtn.hidden = false;
      reviewRePracticeBtn.textContent = `⚡ Re-Practice Weak (${weakCount})`;
      reviewRePracticeBtn.textContent = `⚡ Re-Practice Weak (${drillTotal}-Q Drill)`;
    } else {
      reviewRePracticeBtn.hidden = true;
    }
  }

  if (!questions.length) {
    $("#reviewList").innerHTML = `<div class="empty-state">No answered questions to review yet.</div>`;
    return;
  }

  const avg = summary.avg_time || 0;

  $("#reviewList").innerHTML = questions.map((question) => {
    const skipped = question.is_skipped || (question.selected_option_index === null && !question.typed_answer && question.selected_option === null);
    const hasOptionIndex = question.selected_option_index !== null && question.selected_option_index !== undefined;
    const selectedLabel = hasOptionIndex ? `${String.fromCharCode(65 + question.selected_option_index)}. ` : "";
    const correctPrefix = (question.options?.length > 1 && !question.typed_answer) ? `${String.fromCharCode(65 + question.correct_option_index)}. ` : "";
    const statusClass = skipped ? "is-skipped" : question.is_correct ? "is-correct" : "is-wrong";
    const statusText = skipped ? "Skipped" : question.is_correct ? "Correct" : "Incorrect";
    const selectedAnswer = skipped
      ? "Skipped"
      : question.typed_answer
        ? escapeHtml(String(question.typed_answer))
        : `${selectedLabel}${escapeHtml(String(question.selected_option ?? ""))}`;
    const correctAnswer = `${correctPrefix}${escapeHtml(String(question.correct_option ?? ""))}`;

    // Compute time badge
    const timeTaken = question.time_taken !== undefined && question.time_taken !== null ? Number(question.time_taken) : null;
    let timeBadge = "";
    if (timeTaken !== null && !skipped) {
      if (avg > 0 && timeTaken > avg) {
        timeBadge = `<span class="time-badge is-slow" title="Took ${timeTaken}s (Slower than average ${avg}s)">⏱️ ${timeTaken}s (Slow)</span>`;
      } else if (avg > 0) {
        timeBadge = `<span class="time-badge is-fast" title="Took ${timeTaken}s (Faster than average ${avg}s)">⚡ ${timeTaken}s (Fast)</span>`;
      } else {
        timeBadge = `<span class="time-badge">${timeTaken}s</span>`;
      }
    }

    return `
      <article class="review-card ${statusClass}">
        <div class="review-card-header">
          <span>Question ${question.question_number}</span>
          <div style="display:flex;align-items:center;gap:8px;">
            ${timeBadge}
            <strong>${statusText}</strong>
          </div>
        </div>
        <h3>${escapeHtml(question.question_text)}</h3>
        <div class="review-answer-grid">
          <div>
            <span>Your answer</span>
            <strong>${selectedAnswer}</strong>
          </div>
          <div>
            <span>Correct answer</span>
            <strong>${correctAnswer}</strong>
          </div>
        </div>
        <p>${escapeHtml(question.explanation || "No explanation available.")}</p>
      </article>
    `;
  }).join("");
}

const QUESTION_TIME_LIMIT_SECONDS = 15;

function updateTimerDisplay(remaining, elapsed = 0) {
  const timerElem = $("#questionTimer");
  if (!timerElem) return;
  timerElem.textContent = `${remaining}s`;

  // Urgency check (final 5s alert)
  if (remaining <= 5) {
    timerElem.classList.add("is-urgent");
    timerElem.classList.remove("is-warning");
  } else if (remaining <= 10) {
    timerElem.classList.add("is-warning");
    timerElem.classList.remove("is-urgent");
  } else {
    timerElem.classList.remove("is-warning", "is-urgent");
  }

  // GMAT Recall Speed Zone Benchmarks
  if (elapsed < 5) {
    timerElem.classList.add("timer-zone-emerald");
    timerElem.classList.remove("timer-zone-blue", "timer-zone-amber");
    timerElem.title = "⚡ GMAT-Ready Recall Zone (< 5s)";
  } else if (elapsed <= 12) {
    timerElem.classList.add("timer-zone-blue");
    timerElem.classList.remove("timer-zone-emerald", "timer-zone-amber");
    timerElem.title = "🎯 Acceptable Pace Zone (5–12s)";
  } else {
    timerElem.classList.add("timer-zone-amber");
    timerElem.classList.remove("timer-zone-emerald", "timer-zone-blue");
    timerElem.title = "🐢 Hesitation Zone (> 12s)";
  }
}

function startQuestionTimer() {
  clearQuestionTimer();
  state.questionStartedAt = Date.now();
  $("#questionTimer").textContent = `${QUESTION_TIME_LIMIT_SECONDS}s`;
  updateTimerDisplay(QUESTION_TIME_LIMIT_SECONDS, 0);

  state.timerId = window.setInterval(() => {
    if (state.answered) {
      clearQuestionTimer();
      return;
    }
    const elapsed = Math.floor((Date.now() - state.questionStartedAt) / 1000);
    const remaining = Math.max(0, QUESTION_TIME_LIMIT_SECONDS - elapsed);
    updateTimerDisplay(remaining, elapsed);

    if (state.activeGameMode && state.gameState && !state.answered) {
      renderGamePanels();
    }

    if (remaining <= 0) {
      clearQuestionTimer();
      handleQuestionTimeout();
    }
  }, 250);
}

function clearQuestionTimer() {
  clearAutoSubmitTimer();
  if (state.timerId) {
    window.clearInterval(state.timerId);
    state.timerId = null;
  }
  const timerElem = $("#questionTimer");
  if (timerElem) {
    timerElem.classList.remove("is-warning", "is-urgent");
    timerElem.classList.remove("is-warning", "is-urgent", "timer-zone-emerald", "timer-zone-blue", "timer-zone-amber");
  }
}

async function handleQuestionTimeout() {
  if (state.answered || !state.session?.session_id) {
    return;
  }
  state.answered = true;
  clearQuestionTimer();
  clearAutoAdvance();

  const display = $("#numpadDisplay");
  if (display) {
    display.classList.remove("is-pending", "is-correct");
    display.classList.add("is-wrong");
  }

  document.querySelectorAll(".numpad-key").forEach((key) => {
    key.disabled = true;
  });
  const submitBtn = $("#numpadSubmitBtn");
  if (submitBtn) {
    submitBtn.disabled = true;
  }

  const feedbackPanel = $("#feedbackPanel");
  if (feedbackPanel) {
    feedbackPanel.classList.remove("is-correct", "is-checking");
    feedbackPanel.classList.add("is-wrong");
  }
  $("#feedbackTitle").textContent = "Time's Up (Failed)";
  $("#feedbackText").textContent = `${QUESTION_TIME_LIMIT_SECONDS} seconds expired. Showing correct answer...`;
  playTone("wrong");
  triggerHaptic("error");

  let result;
  try {
    result = await api(`/api/session/${state.session.session_id}/answer`, {
      method: "POST",
      body: JSON.stringify({
        is_timeout: true,
        typed_answer: state.numpadValue.trim() || undefined,
      }),
    });
    result.is_timeout = true;
  } catch (error) {
    showStatus(error.message);
    return;
  }

  document.querySelectorAll(".option-button").forEach((button) => {
    const index = Number(button.dataset.answerIndex);
    button.disabled = true;
    button.classList.remove("is-pending", "is-dimmed");
    if (index === result.correct_option_index) {
      button.classList.add("is-correct");
    }
  });

  finalizeAnswerResponse(result, null);
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
      if (screenButton.dataset.screenTarget === "english") {
        window.EnglishApp?.init();
      }
      return;
    }

    const answerModeBtn = event.target.closest("[data-answer-mode]");
    if (answerModeBtn) {
      event.preventDefault();
      setAnswerMode(answerModeBtn.dataset.answerMode);
      return;
    }

    const numpadKey = event.target.closest("[data-numpad-key]");
    if (numpadKey) {
      event.preventDefault();
      if (Date.now() - lastNumpadPointerTime < 350) {
        return;
      }
      const key = numpadKey.dataset.numpadKey;
      if (key === "backspace") {
        backspaceNumpad();
      } else if (key === "clear") {
        clearNumpad();
      } else {
        appendNumpadKey(key);
      }
      return;
    }

    if (event.target.closest("#numpadClearBtn")) {
      event.preventDefault();
      clearNumpad();
      return;
    }

    const numpadSubmitBtn = event.target.closest("#numpadSubmitBtn");
    if (numpadSubmitBtn && !numpadSubmitBtn.disabled) {
      event.preventDefault();
      submitTypedAnswer();
      handleManualSubmitAttempt();
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

  let lastNumpadPointerTime = 0;
  const numpadGrid = $("#numpadGrid");
  if (numpadGrid) {
    numpadGrid.addEventListener("pointerdown", (event) => {
      const keyBtn = event.target.closest("[data-numpad-key]");
      if (keyBtn && !keyBtn.disabled) {
        event.preventDefault();
        lastNumpadPointerTime = Date.now();
        const key = keyBtn.dataset.numpadKey;
        if (key === "backspace") {
          backspaceNumpad();
        } else if (key === "clear") {
          clearNumpad();
        } else {
          appendNumpadKey(key);
        }
      }
    });
  }

  window.addEventListener("keydown", (event) => {
    if (event.target.tagName === "INPUT" || event.target.tagName === "TEXTAREA") {
      return;
    }
    const questionScreen = $("#questionScreen");
    if (!questionScreen || !questionScreen.classList.contains("is-active")) {
      return;
    }
    if (!state.session || !state.activeQuestion || state.answered) {
      return;
    }

    if (state.answerMode === "numpad") {
      if ((event.key >= "0" && event.key <= "9") || event.key === "." || event.key === "-" || event.key === "/" || event.key === "%") {
        event.preventDefault();
        appendNumpadKey(event.key);
        highlightKeyElement(event.key);
      } else if (event.key === "Backspace") {
        event.preventDefault();
        backspaceNumpad();
        highlightKeyElement("backspace");
      } else if (event.key === "Escape" || event.key === "Delete") {
        event.preventDefault();
        clearNumpad();
        highlightKeyElement("clear");
      } else if (event.key === "Enter") {
        event.preventDefault();
        submitTypedAnswer();
        handleManualSubmitAttempt();
      }
    } else if (state.answerMode === "mcq") {
      const key = event.key.toUpperCase();
      if (["A", "B", "C", "D"].includes(key)) {
        event.preventDefault();
        const idx = key.charCodeAt(0) - 65;
        if (idx < (state.activeQuestion.options?.length || 0)) {
          submitAnswer(idx);
        }
      } else if (["1", "2", "3", "4"].includes(event.key)) {
        event.preventDefault();
        const idx = Number(event.key) - 1;
        if (idx < (state.activeQuestion.options?.length || 0)) {
          submitAnswer(idx);
        }
      }
    }
  });

  $("#selectTopicButton")?.addEventListener("click", selectWholeTopic);
  $("#startButton")?.addEventListener("click", startPractice);
  $("#practiceAgainButton")?.addEventListener("click", () => {
    startPractice();
  });
  $("#backToSetupButton")?.addEventListener("click", () => {
    setScreen("practice");
  });
  $("#reviewAnswersButton")?.addEventListener("click", showReview);
  $("#reviewBackButton")?.addEventListener("click", () => setScreen("result"));
  $("#saveReminderButton")?.addEventListener("click", saveReminder);
  $("#reminderEnabled")?.addEventListener("change", saveReminder);
  $("#practiceMistakesButton")?.addEventListener("click", startAllMistakeRetry);
  $("#stopPracticeButton")?.addEventListener("click", stopPractice);

  document.querySelectorAll("[data-screen-target]").forEach((tabBtn) => {
    tabBtn.addEventListener("click", () => {
      const target = tabBtn.dataset.screenTarget;
      if (target) {
        setScreen(target);
      }
    });
  });

  const rePracticeBtn = $("#rePracticeWeakButton");
  if (rePracticeBtn) {
    rePracticeBtn.addEventListener("click", rePracticeWeakQuestions);
  }
  const reviewRePracticeBtn = $("#reviewRePracticeWeakButton");
  if (reviewRePracticeBtn) {
    reviewRePracticeBtn.addEventListener("click", rePracticeWeakQuestions);
  }

  const downloadJsonBtn = $("#downloadJsonBtn");
  if (downloadJsonBtn) {
    downloadJsonBtn.addEventListener("click", async () => {
      if (window.AptitudeLocalDB) {
        try {
          await window.AptitudeLocalDB.exportLocalDataJSON();
          showStatus("Downloaded JSON backup of your practice data.", "info");
        } catch (err) {
          showStatus(`Failed to export JSON: ${err.message}`);
        }
      }
    });
  }

  const downloadCsvBtn = $("#downloadCsvBtn");
  if (downloadCsvBtn) {
    downloadCsvBtn.addEventListener("click", async () => {
      if (window.AptitudeLocalDB) {
        try {
          await window.AptitudeLocalDB.exportLocalDataCSV();
          showStatus("Exported CSV of your question attempts.", "info");
        } catch (err) {
          showStatus(`Failed to export CSV: ${err.message}`);
        }
      }
    });
  }

  const downloadQuestionCsvBtn = $("#downloadQuestionCsvBtn");
  if (downloadQuestionCsvBtn) {
    downloadQuestionCsvBtn.addEventListener("click", async () => {
      if (window.AptitudeLocalDB?.exportQuestionStatsCSV) {
        try {
          await window.AptitudeLocalDB.exportQuestionStatsCSV();
          showStatus("Exported Question Frequency & Repetition CSV.", "info");
        } catch (err) {
          showStatus(`Failed to export Question CSV: ${err.message}`);
        }
      }
    });
  }

  const importBackupFile = $("#importBackupFile");
  if (importBackupFile) {
    importBackupFile.addEventListener("change", async (event) => {
      const file = event.target.files?.[0];
      if (!file || !window.AptitudeLocalDB) {
        return;
      }
      try {
        const text = await file.text();
        const res = await window.AptitudeLocalDB.importLocalDataJSON(text);
        showStatus(`Imported ${res.attemptsImported} attempts and ${res.sessionsImported} sessions successfully!`, "info");
        void renderLocalJournal();
      } catch (err) {
        showStatus(`Failed to import backup: ${err.message}`);
      } finally {
        importBackupFile.value = "";
      }
    });
  }

  const chartDayBtn = $("#chartViewDayBtn");
  const chartSessionBtn = $("#chartViewSessionBtn");
  const chartTimeScale = $("#chartTimeScale");
  if (chartDayBtn && chartSessionBtn) {
    chartDayBtn.addEventListener("click", () => {
      currentTrendMode = "day";
      chartDayBtn.classList.add("is-active");
      chartSessionBtn.classList.remove("is-active");
      renderPerformanceTrendSvg();
    });
    chartSessionBtn.addEventListener("click", () => {
      currentTrendMode = "session";
      chartSessionBtn.classList.add("is-active");
      chartDayBtn.classList.remove("is-active");
      renderPerformanceTrendSvg();
    });
  }
  if (chartTimeScale) {
    chartTimeScale.addEventListener("change", (event) => {
      currentChartTimeScale = Math.max(1, Number(event.target.value) || 15);
      renderPerformanceTrendSvg();
    });
  }
  const chartVariantFilter = $("#chartVariantFilter");
  if (chartVariantFilter) {
    chartVariantFilter.addEventListener("change", (event) => {
      currentChartVariant = event.target.value || "";
      renderPerformanceTrendSvg();
    });
  }

  document.querySelectorAll(".journal-tab-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".journal-tab-btn").forEach((b) => b.classList.remove("is-active"));
      btn.classList.add("is-active");
      const view = btn.dataset.journalView || "day";
      void renderLocalJournal(view);
    });
  });

  const journalSearchInput = $("#journalSearchInput");
  if (journalSearchInput) {
    journalSearchInput.addEventListener("input", (event) => {
      void renderLocalJournal(journalState.activeView, journalState.filterStatus, event.target.value.trim());
    });
  }

  const journalStatusFilter = $("#journalStatusFilter");
  if (journalStatusFilter) {
    journalStatusFilter.addEventListener("change", (event) => {
      void renderLocalJournal(journalState.activeView, event.target.value, journalState.searchQuery);
    });
  }

  ["#progressDayFilter", "#progressCategoryFilter", "#progressTopicFilter", "#progressPatternFilter"].forEach((selector) => {
    const filter = $(selector);
    if (filter) {
      filter.addEventListener("change", (event) => {
        const key = {
          "#progressDayFilter": "day",
          "#progressCategoryFilter": "category",
          "#progressTopicFilter": "topic",
          "#progressPatternFilter": "pattern",
        }[selector];
        journalState[key] = event.target.value;
        if (key === "day") {
          journalState.category = "all";
          journalState.topic = "all";
          journalState.pattern = "all";
        } else if (key === "category") {
          journalState.topic = "all";
          journalState.pattern = "all";
        } else if (key === "topic") {
          journalState.pattern = "all";
        }
        void renderLocalJournal(journalState.activeView, journalState.filterStatus, journalState.searchQuery);
      });
    }
  });

  $("#clearProgressFilters")?.addEventListener("click", () => {
    journalState.day = "all";
    journalState.category = "all";
    journalState.topic = "all";
    journalState.pattern = "all";
    void renderLocalJournal(journalState.activeView, journalState.filterStatus, journalState.searchQuery);
  });

  const drillAllMistakesBtn = $("#drillAllMistakesBtn");
  if (drillAllMistakesBtn) {
    drillAllMistakesBtn.addEventListener("click", () => {
      void startAllMistakeRetry();
    });
  }

  document.querySelectorAll(".root-pill").forEach((pill) => {
    pill.addEventListener("click", () => {
      document.querySelectorAll(".root-pill").forEach((p) => p.classList.remove("is-active"));
      pill.classList.add("is-active");
      currentMistakeFilter = pill.dataset.mistakeFilter || "all";
      void renderAdvancedProgressDashboard();
    });
  });

  document.addEventListener("click", async (event) => {
    const drillBtn = event.target.closest("[data-drill-pattern]");
    if (drillBtn) {
      const patId = drillBtn.dataset.drillPattern;
      const drillType = drillBtn.dataset.drillType;
      if (drillType === "mistake" || !patId) {
        await startAllMistakeRetry();
      } else {
        await startPracticeWithPatternIds([Number(patId)]);
      }
    }
  });
}

const journalState = {
  activeView: "day",
  filterStatus: "all",
  searchQuery: "",
  day: "all",
  category: "all",
  topic: "all",
  pattern: "all",
};

function scopedProgressAttempts(attempts) {
  return (attempts || []).filter((attempt) => {
    const date = attempt.date || (attempt.timestamp ? new Date(attempt.timestamp).toISOString().slice(0, 10) : "");
    return (journalState.day === "all" || date === journalState.day)
      && (journalState.category === "all" || (attempt.category_name || "General") === journalState.category)
      && (journalState.topic === "all" || (attempt.topic_name || "General") === journalState.topic)
      && (journalState.pattern === "all" || (attempt.pattern_name || "General Pattern") === journalState.pattern);
  });
}

function setProgressSelectOptions(id, values, current, allLabel) {
  const select = $(id);
  if (!select) return current;
  const uniqueValues = [...new Set(values.filter(Boolean).map(String))].sort((a, b) => a.localeCompare(b));
  const nextCurrent = current !== "all" && uniqueValues.includes(current) ? current : "all";
  select.innerHTML = `<option value="all">${allLabel}</option>${uniqueValues.map((value) => `<option value="${escapeHtml(value)}">${escapeHtml(value)}</option>`).join("")}`;
  select.value = nextCurrent;
  return nextCurrent;
}

function renderProgressExplorer(attempts) {
  const dayFiltered = (attempts || []).filter((attempt) => {
    const date = attempt.date || (attempt.timestamp ? new Date(attempt.timestamp).toISOString().slice(0, 10) : "");
    return journalState.day === "all" || date === journalState.day;
  });
  journalState.day = setProgressSelectOptions("#progressDayFilter", (attempts || []).map((attempt) => attempt.date || (attempt.timestamp ? new Date(attempt.timestamp).toISOString().slice(0, 10) : "")), journalState.day, "All days");

  const categoryFiltered = dayFiltered.filter((attempt) => journalState.category === "all" || (attempt.category_name || "General") === journalState.category);
  journalState.category = setProgressSelectOptions("#progressCategoryFilter", dayFiltered.map((attempt) => attempt.category_name || "General"), journalState.category, "All categories");
  journalState.topic = setProgressSelectOptions("#progressTopicFilter", categoryFiltered.map((attempt) => attempt.topic_name || "General"), journalState.topic, "All sub-topics");

  const topicFiltered = categoryFiltered.filter((attempt) => journalState.topic === "all" || (attempt.topic_name || "General") === journalState.topic);
  journalState.pattern = setProgressSelectOptions("#progressPatternFilter", topicFiltered.map((attempt) => attempt.pattern_name || "General Pattern"), journalState.pattern, "All patterns");
  const explorer = $("#progressExplorer");
  if (explorer) explorer.hidden = journalState.activeView === "diagnostics";
}

function renderProgressScopeSummary(attempts) {
  const total = attempts.length;
  const correct = attempts.filter((attempt) => Boolean(attempt.is_correct)).length;
  const totalTime = attempts.reduce((sum, attempt) => sum + Number(attempt.time_taken || 0), 0);
  const uniqueQuestions = new Set(attempts.map((attempt) => `${attempt.pattern_id || 0}::${attempt.question_text || ""}`)).size;
  const setText = (id, value) => { const target = $(id); if (target) target.textContent = value; };
  setText("#scopeAttemptCount", String(total));
  setText("#scopeAccuracy", `${total ? Math.round((correct / total) * 100) : 0}%`);
  setText("#scopeAvgTime", `${total ? (totalTime / total).toFixed(1) : "0.0"}s`);
  setText("#scopeUniqueQuestions", String(total ? uniqueQuestions : 0));
}

function buildScopedQuestionStats(attempts) {
  const questionMap = new Map();
  (attempts || []).forEach((attempt) => {
    const questionText = String(attempt.question_text || "").trim() || "Unnamed question";
    const key = `${attempt.pattern_id || 0}::${questionText}`;
    if (!questionMap.has(key)) {
      questionMap.set(key, {
        question_text: questionText,
        category_name: attempt.category_name || "General",
        topic_name: attempt.topic_name || "General",
        pattern_id: Number(attempt.pattern_id || 0),
        pattern_name: attempt.pattern_name || "General Pattern",
        options: Array.isArray(attempt.options) ? attempt.options : [],
        correct_answer: attempt.correct_answer ?? null,
        correct_option_index: attempt.correct_option_index,
        explanation: attempt.explanation || "",
        total_seen: 0,
        correct_count: 0,
        wrong_count: 0,
        timeout_count: 0,
        total_time: 0,
        last_timestamp: 0,
        last_date: "",
        attempts: [],
      });
    }
    const item = questionMap.get(key);
    item.total_seen += 1;
    if (attempt.is_correct) item.correct_count += 1;
    else item.wrong_count += 1;
    if (attempt.is_timeout) item.timeout_count += 1;
    item.total_time += Number(attempt.time_taken || 0);
    item.attempts.push(attempt);
    if (Number(attempt.timestamp || 0) >= item.last_timestamp) {
      item.last_timestamp = Number(attempt.timestamp || 0);
      item.last_date = attempt.date || (attempt.timestamp ? new Date(attempt.timestamp).toISOString().slice(0, 10) : "");
    }
  });
  return [...questionMap.values()]
    .map((item) => ({
      ...item,
      accuracy: item.total_seen ? Math.round((item.correct_count / item.total_seen) * 100) : 0,
      avg_time: item.total_seen ? Number((item.total_time / item.total_seen).toFixed(1)) : 0,
    }))
    .sort((a, b) => b.total_seen - a.total_seen || a.question_text.localeCompare(b.question_text));
}

function renderJournalAttemptCard(attempt, overallAvgTime = 15) {
  const isCorrect = Boolean(attempt.is_correct);
  const isTimeout = Boolean(attempt.is_timeout);
  const isSlow = attempt.time_taken > (overallAvgTime || 15) || isTimeout;
  const timeSec = Number(attempt.time_taken || 0).toFixed(1);

  let userAnswerText = attempt.typed_answer;
  if (userAnswerText === null || userAnswerText === undefined || userAnswerText === "") {
    userAnswerText = attempt.selected_answer;
  }
  if (userAnswerText === null || userAnswerText === undefined || userAnswerText === "") {
    userAnswerText = isTimeout ? "(Timed out)" : "(None)";
  }

  let correctAnswerText = attempt.correct_answer;
  if ((correctAnswerText === null || correctAnswerText === undefined || correctAnswerText === "") && Array.isArray(attempt.options) && attempt.correct_option_index !== null && attempt.correct_option_index !== undefined) {
    correctAnswerText = attempt.options[attempt.correct_option_index];
  }
  if (correctAnswerText === null || correctAnswerText === undefined) {
    correctAnswerText = "";
  }

  let optionsHtml = "";
  if (Array.isArray(attempt.options) && attempt.options.length > 0) {
    optionsHtml = `
      <div class="journal-attempt-options">
        ${attempt.options.map((opt, idx) => {
          const isUserPicked = (attempt.selected_answer === opt) || (attempt.typed_answer && String(attempt.typed_answer).trim() === String(opt).trim()) || (attempt.selected_option_index === idx);
          const isCorrectTarget = (idx === attempt.correct_option_index) || (String(correctAnswerText).trim() === String(opt).trim());
          let cls = "journal-option-item";
          if (isCorrectTarget) cls += " is-correct-target";
          if (isUserPicked) cls += " is-user-picked";
          return `<div class="${cls}"><span>${String.fromCharCode(65 + idx)}.</span> <span>${escapeHtml(opt)}</span></div>`;
        }).join("")}
      </div>
    `;
  }

  const dateDisplay = attempt.timestamp ? new Date(attempt.timestamp).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }) : "";

  return `
    <article class="journal-attempt-card">
      <div class="journal-attempt-header">
        <div class="journal-attempt-meta">
          <strong>${escapeHtml(attempt.pattern_name || "General")}</strong>
          <span>•</span>
          <span>${escapeHtml(attempt.category_name || "")} › ${escapeHtml(attempt.topic_name || "")}</span>
          ${attempt.date ? `<span>• ${escapeHtml(attempt.date)} ${dateDisplay}</span>` : ""}
        </div>
        <div style="display:flex;gap:6px;align-items:center;">
          ${isCorrect ? '<span class="journal-badge badge-correct">✓ Correct</span>' : '<span class="journal-badge badge-wrong">✗ Wrong</span>'}
          ${isTimeout ? `<span class="journal-badge badge-timeout">⏰ ${QUESTION_TIME_LIMIT_SECONDS}s Timeout</span>` : ""}
          <span class="journal-badge ${isSlow ? "badge-slow" : "badge-fast"}">${isSlow ? "🐢" : "⚡"} ${timeSec}s</span>
        </div>
      </div>
      <div class="journal-attempt-qtext">${escapeHtml(attempt.question_text)}</div>
      ${optionsHtml}
      <div class="journal-attempt-answers">
        <span><strong>Your Answer:</strong> <span style="color:${isCorrect ? "var(--success)" : "var(--danger)"};font-weight:600;">${escapeHtml(userAnswerText)}</span></span>
        <span><strong>Correct Answer:</strong> <span style="color:var(--success);font-weight:600;">${escapeHtml(correctAnswerText)}</span></span>
      </div>
      ${attempt.explanation ? `<div class="journal-attempt-explanation"><strong>Explanation:</strong> ${escapeHtml(attempt.explanation)}</div>` : ""}
    </article>
  `;
}

function renderQuestionFrequencyCard(q, overallAvgTime = 15) {
  const seen = Number(q.total_seen || 1);
  const correct = Number(q.correct_count || 0);
  const accuracy = Number(q.accuracy || 0);
  const avgTime = Number(q.avg_time || 0);
  const isSlow = avgTime > (overallAvgTime || 15) || Number(q.timeout_count || 0) > 0;

  let freqBadgeClass = "badge-seen-once";
  let freqIcon = "👁️";
  if (seen >= 4) {
    freqBadgeClass = "badge-seen-high";
    freqIcon = "🔥";
  } else if (seen >= 2) {
    freqBadgeClass = "badge-seen-multi";
    freqIcon = "🔁";
  }

  const accBadgeClass = accuracy >= 75 ? "badge-correct" : accuracy < 50 ? "badge-wrong" : "badge-slow";
  const speedBadgeClass = isSlow ? "badge-slow" : "badge-fast";

  let correctAnswerText = q.correct_answer;
  if ((correctAnswerText === null || correctAnswerText === undefined || correctAnswerText === "") && Array.isArray(q.options) && q.correct_option_index !== null && q.correct_option_index !== undefined) {
    correctAnswerText = q.options[q.correct_option_index];
  }
  if (!correctAnswerText) correctAnswerText = "—";

  const attemptRows = (q.attempts || []).map((att, idx) => {
    const isAttCorr = Boolean(att.is_correct);
    const attTime = Number(att.time_taken || 0).toFixed(1);
    const attAns = att.typed_answer || att.selected_answer || (att.is_timeout ? "Timed out" : "—");
    const attDate = att.date || (att.timestamp ? new Date(att.timestamp).toISOString().slice(0, 10) : "");
    const attTimeStr = att.timestamp ? new Date(att.timestamp).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }) : "";
    return `
      <div class="question-attempt-row ${isAttCorr ? "is-correct" : "is-wrong"}">
        <span class="attempt-idx">#${q.attempts.length - idx}</span>
        <span class="attempt-date">${escapeHtml(attDate)} ${escapeHtml(attTimeStr)}</span>
        <span class="attempt-user-answer">Answer: <strong>${escapeHtml(attAns)}</strong></span>
        <span class="journal-badge ${isAttCorr ? "badge-correct" : "badge-wrong"}">${isAttCorr ? "✓ Correct" : "✗ Wrong"}</span>
        <span class="journal-badge ${Number(att.time_taken || 0) > (overallAvgTime || 15) ? "badge-slow" : "badge-fast"}">${att.is_timeout ? `⏰ ${QUESTION_TIME_LIMIT_SECONDS}s Timeout` : `⏱️ ${attTime}s`}</span>
      </div>
    `;
  }).join("");

  return `
    <article class="question-frequency-card">
      <div class="question-freq-header">
        <div class="question-freq-meta">
          <span class="journal-badge ${freqBadgeClass}">${freqIcon} Seen ${seen} ${seen === 1 ? "time" : "times"}</span>
          <strong class="question-pattern-title">${escapeHtml(q.pattern_name || "General Pattern")}</strong>
          <span class="question-topic-sub">(${escapeHtml(q.category_name || "")} › ${escapeHtml(q.topic_name || "")})</span>
        </div>
        <div class="question-freq-badges">
          <span class="journal-badge ${accBadgeClass}">${accuracy}% Accuracy (${correct}/${seen})</span>
          <span class="journal-badge ${speedBadgeClass}">${isSlow ? "🐢" : "⚡"} Avg ${avgTime}s</span>
          ${q.timeout_count > 0 ? `<span class="journal-badge badge-timeout">⏰ ${q.timeout_count} Timed Out</span>` : ""}
        </div>
      </div>
      <div class="question-freq-text">${escapeHtml(q.question_text)}</div>
      <div class="question-metrics-grid">
        <div><span>Times seen</span><strong>${seen}</strong></div>
        <div><span>Accuracy</span><strong>${accuracy}%</strong><small>${correct}/${seen} correct</small></div>
        <div><span>Average time</span><strong>${avgTime}s</strong><small>${isSlow ? "Needs speed work" : "On pace"}</small></div>
        <div><span>Wrong / timeout</span><strong>${Number(q.wrong_count || 0)} / ${Number(q.timeout_count || 0)}</strong><small>attempts</small></div>
      </div>
      <div class="question-freq-answer-strip">
        <span><strong>Target Correct Answer:</strong> <span class="correct-ans-highlight">${escapeHtml(correctAnswerText)}</span></span>
        ${q.last_date ? `<span class="question-last-practiced">Last Practiced: <strong>${escapeHtml(q.last_date)}</strong></span>` : ""}
      </div>
      ${q.explanation ? `<div class="journal-attempt-explanation" style="margin-top:8px;"><strong>Explanation:</strong> ${escapeHtml(q.explanation)}</div>` : ""}
      <details class="question-history-details">
        <summary class="question-history-summary">
          <span>📜 View all ${seen} ${seen === 1 ? "attempt" : "attempts"} for this exact question</span>
          <span class="summary-hint">Click to expand</span>
        </summary>
        <div class="question-history-drawer">
          ${attemptRows}
        </div>
      </details>
    </article>
  `;
}

let currentMistakeFilter = "all";
let currentTrendMode = "day";
let currentChartTimeScale = 15;
let cachedTrendDays = [];
let cachedSessions = [];
let cachedVariantTrends = {};
let cachedVariantSessions = {};
let currentChartVariant = "";

function renderPerformanceTrendSvg(trendDays = cachedTrendDays, sessions = cachedSessions) {
  if (trendDays && Array.isArray(trendDays)) cachedTrendDays = trendDays;
  if (sessions && Array.isArray(sessions)) cachedSessions = sessions;

  const svgGrid = $("#svgGridLines");
  const svgAccArea = $("#svgAccArea");
  const svgAccLine = $("#svgAccLine");
  const svgSpeedLine = $("#svgSpeedLine");
  const svgPoints = $("#svgDataPoints");
  const summaryBadge = $("#chartSummaryBadge");

  if (!svgAccLine) return;

  const activeTrendDays = currentChartVariant ? (cachedVariantTrends[currentChartVariant] || []) : cachedTrendDays;
  const activeSessions = currentChartVariant ? (cachedVariantSessions[currentChartVariant] || []) : cachedSessions;

  let points = [];
  if (currentTrendMode === "session" && activeSessions.length > 0) {
    points = activeSessions.slice(0, 15).reverse().map((s, idx) => ({
      label: `S${idx + 1}`,
      tooltip: `Session #${idx + 1} (${s.date || ""}): ${s.accuracy || 0}% Acc • ${s.avg_time || 0}s (${s.total_questions || 0} Qs)`,
      accuracy: Number(s.accuracy || 0),
      avg_time: Number(s.avg_time || 0),
      total: Number(s.total_questions || 0),
    }));
  } else if (activeTrendDays && activeTrendDays.length > 0) {
    points = activeTrendDays.slice(-14).map((d) => ({
      label: d.display_date || d.date?.slice(5) || "Day",
      tooltip: `${d.date}: ${d.accuracy}% Acc • ${d.avg_time}s (${d.total} Qs)`,
      accuracy: Number(d.accuracy || 0),
      avg_time: Number(d.avg_time || 0),
      total: Number(d.total || 0),
    }));
  } else if (activeSessions.length > 0) {
    points = activeSessions.slice(0, 15).reverse().map((s, idx) => ({
      label: `S${idx + 1}`,
      tooltip: `Session #${idx + 1}: ${s.accuracy || 0}% Acc • ${s.avg_time || 0}s`,
      accuracy: Number(s.accuracy || 0),
      avg_time: Number(s.avg_time || 0),
      total: Number(s.total_questions || 0),
    }));
  }

  if (!points.length) {
    if (svgGrid) svgGrid.innerHTML = `<text x="250" y="95" text-anchor="middle" fill="var(--muted)" font-size="13">Complete practice sets to see your accuracy & speed curve</text>`;
    if (svgAccArea) svgAccArea.setAttribute("d", "");
    if (svgAccLine) svgAccLine.setAttribute("d", "");
    if (svgSpeedLine) svgSpeedLine.setAttribute("d", "");
    if (svgPoints) svgPoints.innerHTML = "";
    if (summaryBadge) summaryBadge.textContent = "No data yet";
    renderSessionProgressInsight(activeSessions);
    return;
  }

  const width = 560;
  const height = 180;
  const padLeft = 35;
  const padRight = 45;
  const padTop = 20;
  const padBottom = 30;

  const chartW = width - padLeft - padRight;
  const chartH = height - padTop - padBottom;

  // Grid lines
  let gridHtml = "";
  [0, 25, 50, 75, 100].forEach((pct) => {
    const y = padTop + chartH - (pct / 100) * chartH;
    gridHtml += `<line x1="${padLeft}" y1="${y.toFixed(1)}" x2="${(width - padRight).toFixed(1)}" y2="${y.toFixed(1)}" stroke="rgba(120,120,120,0.15)" stroke-width="1"/>`;
    gridHtml += `<text x="${padLeft - 6}" y="${(y + 3.5).toFixed(1)}" font-size="10" fill="var(--muted)" text-anchor="end">${pct}%</text>`;
  });
  gridHtml += `<text x="${padLeft}" y="11" font-size="10" font-weight="700" fill="#059669">Accuracy %</text>`;
  gridHtml += `<text x="${width - padRight}" y="11" font-size="10" font-weight="700" fill="#d97706" text-anchor="end">Avg time (seconds)</text>`;
  const timeStep = currentChartTimeScale <= 5 ? 1 : currentChartTimeScale <= 10 ? 2 : 3;
  for (let seconds = currentChartTimeScale; seconds >= 0; seconds -= timeStep) {
    const y = padTop + chartH - (seconds / currentChartTimeScale) * chartH;
    gridHtml += `<text x="${width - padRight + 6}" y="${(y + 3.5).toFixed(1)}" font-size="10" fill="#d97706">${seconds}s</text>`;
  }
  if (svgGrid) svgGrid.innerHTML = gridHtml;

  const n = points.length;
  const stepX = n > 1 ? chartW / (n - 1) : 0;

  const accCoords = [];
  const speedCoords = [];
  let pointsHtml = "";

  points.forEach((item, idx) => {
    const x = n > 1 ? padLeft + idx * stepX : padLeft + chartW / 2;
    const yAcc = padTop + chartH - (Math.max(0, Math.min(100, item.accuracy)) / 100) * chartH;
    accCoords.push({ x, y: yAcc });

    const speedClamped = Math.min(currentChartTimeScale, Math.max(0, item.avg_time));
    const ySpeed = padTop + chartH - (speedClamped / currentChartTimeScale) * chartH;
    speedCoords.push({ x, y: ySpeed });

    pointsHtml += `
      <g class="chart-point-group">
        <circle cx="${x.toFixed(1)}" cy="${yAcc.toFixed(1)}" r="4.5" fill="#10b981" stroke="#ffffff" stroke-width="1.5">
          <title>${escapeHtml(item.tooltip)}</title>
        </circle>
        <circle cx="${x.toFixed(1)}" cy="${ySpeed.toFixed(1)}" r="3.5" fill="#f59e0b" stroke="#ffffff" stroke-width="1">
          <title>${escapeHtml(item.tooltip)}</title>
        </circle>
        <text x="${x.toFixed(1)}" y="${height - 10}" font-size="10" font-weight="600" fill="var(--muted)" text-anchor="middle">${escapeHtml(item.label)}</text>
      </g>
    `;
  });

  let accD = "";
  let areaD = "";
  let speedD = "";

  if (n === 1) {
    const p = accCoords[0];
    const sp = speedCoords[0];
    accD = `M ${padLeft} ${p.y.toFixed(1)} L ${(width - padRight).toFixed(1)} ${p.y.toFixed(1)}`;
    areaD = `M ${padLeft} ${p.y.toFixed(1)} L ${(width - padRight).toFixed(1)} ${p.y.toFixed(1)} L ${(width - padRight).toFixed(1)} ${(padTop + chartH).toFixed(1)} L ${padLeft} ${(padTop + chartH).toFixed(1)} Z`;
    speedD = `M ${padLeft} ${sp.y.toFixed(1)} L ${(width - padRight).toFixed(1)} ${sp.y.toFixed(1)}`;
  } else {
    accD = accCoords.map((p, i) => `${i === 0 ? "M" : "L"} ${p.x.toFixed(1)} ${p.y.toFixed(1)}`).join(" ");
    areaD = `${accD} L ${accCoords[accCoords.length - 1].x.toFixed(1)} ${(padTop + chartH).toFixed(1)} L ${accCoords[0].x.toFixed(1)} ${(padTop + chartH).toFixed(1)} Z`;
    speedD = speedCoords.map((p, i) => `${i === 0 ? "M" : "L"} ${p.x.toFixed(1)} ${p.y.toFixed(1)}`).join(" ");
  }

  if (svgAccArea) svgAccArea.setAttribute("d", areaD);
  if (svgAccLine) svgAccLine.setAttribute("d", accD);
  if (svgSpeedLine) svgSpeedLine.setAttribute("d", speedD);
  if (svgPoints) svgPoints.innerHTML = pointsHtml;

  if (summaryBadge) {
    const latest = points[points.length - 1];
    summaryBadge.textContent = `${latest.accuracy}% Accuracy • ${latest.avg_time}s Avg`;
  }
}

function syncChartVariantFilter(variants) {
  const select = $("#chartVariantFilter");
  if (!select) return;
  const available = Array.isArray(variants) ? variants : Object.keys(cachedVariantTrends);
  if (!available.length) {
    select.innerHTML = `<option value="">All attempts</option>`;
    currentChartVariant = "";
    return;
  }
  if (!currentChartVariant || !available.includes(currentChartVariant)) currentChartVariant = available[0];
  select.innerHTML = available.map((variant) => `<option value="${escapeHtml(variant)}">${escapeHtml(variant)}</option>`).join("");
  select.value = currentChartVariant;
}

async function syncServerHistory() {
  if (!state.telegramUser?.id || !window.AptitudeLocalDB?.syncRemoteHistory) return;
  try {
    const history = await api(`/api/history/${state.telegramUser.id}`, { timeoutMs: 3000 });
    if (!history.offline) {
      await window.AptitudeLocalDB.syncRemoteHistory(history);
    }
  } catch (error) {
    console.warn("Historical data sync unavailable:", error);
  }
}

function renderSessionProgressInsight(sessions = cachedSessions) {
  const target = $("#sessionProgressInsightText");
  if (!target) return;

  const ordered = (Array.isArray(sessions) ? sessions : [])
    .filter((session) => Number(session.total_questions || 0) > 0)
    .sort((a, b) => Number(a.timestamp || 0) - Number(b.timestamp || 0));

  if (ordered.length < 2) {
    target.textContent = "Complete two sessions to see whether your calculation time is improving.";
    return;
  }

  const first = ordered[0];
  const latest = ordered[ordered.length - 1];
  const timeChange = Number(first.avg_time || 0) - Number(latest.avg_time || 0);
  const accuracyChange = Number(latest.accuracy || 0) - Number(first.accuracy || 0);
  const speedText = timeChange > 0
    ? `${timeChange.toFixed(1)}s faster per question`
    : timeChange < 0
      ? `${Math.abs(timeChange).toFixed(1)}s slower per question`
      : "the same average time";
  const accuracyText = accuracyChange > 0
    ? `accuracy is up ${accuracyChange} points`
    : accuracyChange < 0
      ? `accuracy is down ${Math.abs(accuracyChange)} points`
      : "accuracy is unchanged";
  const coaching = Number(latest.avg_time || 0) > 15
    ? "For your next session, estimate first and write only the essential calculation steps."
    : "Keep this pace and focus on accuracy before trying to go even faster.";
  target.textContent = `Compared with your first session: ${speedText}; ${accuracyText}. ${coaching}`;
}

function renderRootCauseMistakes(mistakes, filter = "all") {
  const container = $("#rootCauseMistakeList");
  if (!container) return;

  const filtered = (mistakes || []).filter((m) => {
    if (filter === "all") return true;
    return m.root_cause === filter;
  });

  if (!filtered.length) {
    container.innerHTML = `<div class="empty-state">No mistakes in this category. You are mastering these patterns!</div>`;
    return;
  }

  container.innerHTML = filtered.slice(0, 25).map((m) => {
    const timeSec = Number(m.time_taken || 0).toFixed(1);
    let userAns = m.typed_answer || m.selected_answer || (m.is_timeout ? "(Timed Out)" : "(None)");
    let corrAns = m.correct_answer || (m.options && m.options[m.correct_option_index]) || "";

    return `
      <article class="mistake-classified-card is-${m.root_cause}">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:8px;flex-wrap:wrap;">
          <div>
            <strong>${escapeHtml(m.pattern_name || "General")}</strong>
            <span style="font-size:12px;color:var(--muted);margin-left:6px;">(${escapeHtml(m.category_name)} › ${escapeHtml(m.topic_name)})</span>
          </div>
          <div style="display:flex;gap:6px;align-items:center;">
            <span class="journal-badge ${m.root_cause_badge}">${escapeHtml(m.root_cause_label)}</span>
            <span class="journal-badge badge-slow">${timeSec}s</span>
          </div>
        </div>
        <div style="font-size:14px;color:var(--text);font-weight:600;margin:6px 0;">${escapeHtml(m.question_text)}</div>
        <div style="font-size:13px;display:flex;gap:16px;color:var(--muted);flex-wrap:wrap;">
          <span>Your Answer: <strong style="color:var(--danger);">${escapeHtml(userAns)}</strong></span>
          <span>Correct Answer: <strong style="color:var(--success);">${escapeHtml(corrAns)}</strong></span>
        </div>
        ${m.explanation ? `<div style="font-size:12px;color:var(--muted);line-height:1.45;background:var(--surface-muted);padding:8px 10px;border-radius:6px;margin-top:6px;"><strong>Explanation:</strong> ${escapeHtml(m.explanation)}</div>` : ""}
      </article>
    `;
  }).join("");
}

async function renderAdvancedProgressDashboard() {
  if (!window.AptitudeLocalDB || typeof window.AptitudeLocalDB.getAdvancedLocalAnalytics !== "function") {
    return;
  }

  let adv;
  try {
    adv = await window.AptitudeLocalDB.getAdvancedLocalAnalytics();
  } catch (err) {
    console.warn("Failed to load advanced analytics:", err);
    return;
  }

  // 1. Executive Readiness Cockpit
  const scoreElem = $("#readinessScore");
  const gaugeElem = $("#readinessGaugeRing");
  const tierElem = $("#readinessTier");
  const summaryElem = $("#readinessSummary");

  if (scoreElem) scoreElem.textContent = String(adv.readiness.score);
  if (gaugeElem) {
    gaugeElem.style.setProperty("--gauge-fill", `${adv.readiness.score}%`);
    gaugeElem.style.setProperty("--readiness-color", adv.readiness.color);
  }
  if (tierElem) {
    tierElem.textContent = adv.readiness.tier;
    tierElem.style.borderColor = adv.readiness.color;
    tierElem.style.color = adv.readiness.color;
  }
  if (summaryElem && adv.totals.total_attempts > 0) {
    summaryElem.textContent = `Analyzed ${adv.totals.total_attempts} attempts across ${Object.keys(adv.patterns).length} patterns. Accuracy: ${adv.totals.accuracy}%, Average Speed: ${adv.totals.avg_time}s.`;
  }

  // Pillar Bars
  const pAcc = $("#pillarAccuracyBar");
  const pAccVal = $("#pillarAccuracyVal");
  if (pAcc) pAcc.style.width = `${Math.min(100, (adv.readiness.components.accuracy / 35) * 100)}%`;
  if (pAccVal) pAccVal.textContent = `${adv.totals.accuracy}%`;

  const pSpeed = $("#pillarSpeedBar");
  const pSpeedVal = $("#pillarSpeedVal");
  if (pSpeed) pSpeed.style.width = `${Math.min(100, (adv.readiness.components.speed / 25) * 100)}%`;
  if (pSpeedVal) pSpeedVal.textContent = `${adv.totals.avg_time}s`;

  const pCov = $("#pillarCoverageBar");
  const pCovVal = $("#pillarCoverageVal");
  if (pCov) pCov.style.width = `${Math.min(100, (adv.readiness.components.coverage / 20) * 100)}%`;
  if (pCovVal) pCovVal.textContent = `${Math.min(100, adv.readiness.components.coverage * 5)}%`;

  const pCon = $("#pillarConsistencyBar");
  const pConVal = $("#pillarConsistencyVal");
  if (pCon) pCon.style.width = `${Math.min(100, (adv.readiness.components.consistency / 10) * 100)}%`;
  if (pConVal) pConVal.textContent = `${Math.min(100, adv.readiness.components.consistency * 10)}%`;

  const pRec = $("#pillarRecoveryBar");
  const pRecVal = $("#pillarRecoveryVal");
  if (pRec) pRec.style.width = `${Math.min(100, (adv.readiness.components.liquidation / 10) * 100)}%`;
  if (pRecVal) pRecVal.textContent = `${Math.min(100, adv.readiness.components.liquidation * 10)}%`;

  // Make the first dashboard action obvious without hiding the detailed analytics.
  const focusTitle = $("#progressFocusTitle");
  const focusText = $("#progressFocusText");
  const focusBadge = $("#progressFocusBadge");
  const focusButton = $("#progressFocusButton");
  const topPrescription = adv.prescriptions?.[0];
  const totalAttempts = Number(adv.totals?.total_attempts || 0);
  if (focusTitle && focusText && focusBadge && focusButton) {
    focusButton.hidden = true;
    focusButton.onclick = null;
    focusButton.removeAttribute("data-drill-pattern");
    focusButton.removeAttribute("data-drill-type");

    if (topPrescription?.pattern_id) {
      focusTitle.textContent = topPrescription.title || "Practice your next focus area";
      focusText.textContent = topPrescription.description || topPrescription.subtitle || "A short targeted drill will help improve this area.";
      focusBadge.textContent = topPrescription.metric || "Recommended";
      focusButton.textContent = topPrescription.action_label || "Practice now";
      focusButton.dataset.drillPattern = String(topPrescription.pattern_id);
      focusButton.dataset.drillType = topPrescription.type || "pattern";
      focusButton.hidden = false;
    } else if (totalAttempts > 0) {
      focusTitle.textContent = "Keep your momentum going";
      focusText.textContent = `You have completed ${totalAttempts} question${totalAttempts === 1 ? "" : "s"}. Continue practicing to make your trend more reliable.`;
      focusBadge.textContent = `${adv.totals.accuracy || 0}% accuracy`;
      focusButton.textContent = "Practice again";
      focusButton.onclick = () => startPractice();
      focusButton.hidden = false;
    } else {
      focusTitle.textContent = "Build your baseline";
      focusText.textContent = "Complete a practice session to unlock personalized strengths, weak areas, and recommendations.";
      focusBadge.textContent = "Getting started";
    }
  }

  // KPI Ribbon
  const todayStr = new Date().toISOString().slice(0, 10);
  const todayCount = (adv.days[todayStr]?.total) || 0;
  const todayElem = $("#todaySolved");
  if (todayElem) todayElem.textContent = String(todayCount);

  const accElem = $("#accuracyStat");
  if (accElem) accElem.textContent = `${adv.totals.accuracy}%`;

  const masteryElem = $("#masteryStat");
  if (masteryElem) masteryElem.textContent = `${adv.readiness.score}%`;

  const solvedElem = $("#totalSolved");
  if (solvedElem) solvedElem.textContent = String(adv.totals.total_attempts);

  const corrElem = $("#totalCorrect");
  if (corrElem) corrElem.textContent = String(adv.totals.total_correct);

  const avgElem = $("#avgTime");
  if (avgElem) avgElem.textContent = `${adv.totals.avg_time}s`;

  const timeoutRateElem = $("#kpiTimeoutRate");
  if (timeoutRateElem) timeoutRateElem.textContent = `${adv.pacing.timeout_rate}%`;

  const streakElem = $("#kpiStreak");
  if (streakElem) streakElem.textContent = `${adv.streak} ${adv.streak === 1 ? "Day" : "Days"}`;

  // 2. AI Prescriptions
  const prescContainer = $("#aiPrescriptionsContainer");
  if (prescContainer) {
    if (!adv.prescriptions.length) {
      prescContainer.innerHTML = `<div class="empty-state">No critical bottlenecks detected yet! Practice any topic to generate recommendations.</div>`;
    } else {
      prescContainer.innerHTML = adv.prescriptions.map((p) => `
        <div class="prescription-card presc-${p.type}">
          <div>
            <div class="prescription-header">
              <span class="prescription-badge">${p.badge}</span>
            </div>
            <h3>${escapeHtml(p.title)}</h3>
            <div class="prescription-subtitle">${escapeHtml(p.subtitle)}</div>
            <div class="prescription-metric">${escapeHtml(p.metric)}</div>
            <p class="prescription-desc">${escapeHtml(p.description)}</p>
          </div>
          <button class="prescription-action-btn" data-drill-pattern="${p.pattern_id || ''}" data-drill-type="${p.type}" type="button">
            ${escapeHtml(p.action_label)}
          </button>
        </div>
      `).join("");
    }
  }

  // 3. 4-Quadrant Strategic Matrix
  const mastersCount = $("#quadMastersCount");
  if (mastersCount) mastersCount.textContent = `${adv.quadrants.speed_masters.length} Patterns`;
  const trapsCount = $("#quadTrapsCount");
  if (trapsCount) trapsCount.textContent = `${adv.quadrants.speed_traps.length} Patterns`;
  const rushersCount = $("#quadRushersCount");
  if (rushersCount) rushersCount.textContent = `${adv.quadrants.rushers.length} Patterns`;
  const bottlenecksCount = $("#quadBottlenecksCount");
  if (bottlenecksCount) bottlenecksCount.textContent = `${adv.quadrants.bottlenecks.length} Patterns`;

  const renderChips = (list) => {
    if (!list.length) return `<div class="empty-mini">No patterns in this quadrant yet.</div>`;
    return list.map((p) => `
      <div class="quad-chip" title="${escapeHtml(p.pattern_name)} (${escapeHtml(p.topic_name)})">
        <strong>${escapeHtml(p.pattern_name)}</strong>
        <span>${p.accuracy}% • ${p.avg_time}s</span>
        <button class="chip-drill-btn" data-drill-pattern="${p.pattern_id}" type="button">⚡ Drill</button>
      </div>
    `).join("");
  };

  const mastersList = $("#quadMastersList");
  if (mastersList) mastersList.innerHTML = renderChips(adv.quadrants.speed_masters);
  const trapsList = $("#quadTrapsList");
  if (trapsList) trapsList.innerHTML = renderChips(adv.quadrants.speed_traps);
  const rushersList = $("#quadRushersList");
  if (rushersList) rushersList.innerHTML = renderChips(adv.quadrants.rushers);
  const bottlenecksList = $("#quadBottlenecksList");
  if (bottlenecksList) bottlenecksList.innerHTML = renderChips(adv.quadrants.bottlenecks);

  // 4. Pacing Spectrum
  const totalAnalyzed = $("#pacingTotalAnalyzed");
  if (totalAnalyzed) totalAnalyzed.textContent = `${adv.totals.total_attempts} Attempts Analyzed`;

  const barL = $("#paceBarLightning");
  if (barL) barL.style.width = `${adv.pacing.lightning.pct}%`;
  const valL = $("#paceValLightning");
  if (valL) valL.textContent = `${adv.pacing.lightning.pct}% (${adv.pacing.lightning.count})`;

  const barO = $("#paceBarOptimal");
  if (barO) barO.style.width = `${adv.pacing.optimal.pct}%`;
  const valO = $("#paceValOptimal");
  if (valO) valO.textContent = `${adv.pacing.optimal.pct}% (${adv.pacing.optimal.count})`;

  const barS = $("#paceBarSlow");
  if (barS) barS.style.width = `${adv.pacing.slow.pct}%`;
  const valS = $("#paceValSlow");
  if (valS) valS.textContent = `${adv.pacing.slow.pct}% (${adv.pacing.slow.count})`;

  const barT = $("#paceBarTimeout");
  if (barT) barT.style.width = `${adv.pacing.timeout.pct}%`;
  const valT = $("#paceValTimeout");
  if (valT) valT.textContent = `${adv.pacing.timeout.pct}% (${adv.pacing.timeout.count})`;

  // Cognitive Stamina
  const sEarlyAcc = $("#staminaEarlyAcc");
  if (sEarlyAcc) sEarlyAcc.textContent = `${adv.stamina.early.accuracy}%`;
  const sEarlySpeed = $("#staminaEarlySpeed");
  if (sEarlySpeed) sEarlySpeed.textContent = `${adv.stamina.early.avg_time}s`;
  const sEarlyCount = $("#staminaEarlyCount");
  if (sEarlyCount) sEarlyCount.textContent = String(adv.stamina.early.count);

  const sMidAcc = $("#staminaMidAcc");
  if (sMidAcc) sMidAcc.textContent = `${adv.stamina.mid.accuracy}%`;
  const sMidSpeed = $("#staminaMidSpeed");
  if (sMidSpeed) sMidSpeed.textContent = `${adv.stamina.mid.avg_time}s`;
  const sMidCount = $("#staminaMidCount");
  if (sMidCount) sMidCount.textContent = String(adv.stamina.mid.count);

  const sLateAcc = $("#staminaLateAcc");
  if (sLateAcc) sLateAcc.textContent = `${adv.stamina.late.accuracy}%`;
  const sLateSpeed = $("#staminaLateSpeed");
  if (sLateSpeed) sLateSpeed.textContent = `${adv.stamina.late.avg_time}s`;
  const sLateCount = $("#staminaLateCount");
  if (sLateCount) sLateCount.textContent = String(adv.stamina.late.count);

  // Performance Trend SVG Chart
  cachedVariantTrends = adv.variant_trends || {};
  cachedVariantSessions = adv.variant_sessions || {};
  syncChartVariantFilter(adv.variants || Object.keys(cachedVariantTrends));
  renderPerformanceTrendSvg(adv.trend_days, adv.sessions || cachedSessions);

  // 5. Root Cause Mistake Book
  const rootAll = $("#rootCountAll");
  if (rootAll) rootAll.textContent = String(adv.mistakes.total);
  const rootTimeout = $("#rootCountTimeout");
  if (rootTimeout) rootTimeout.textContent = String(adv.mistakes.timeout.count);
  const rootCalc = $("#rootCountCalc");
  if (rootCalc) rootCalc.textContent = String(adv.mistakes.calculation.count);
  const rootConcept = $("#rootCountConcept");
  if (rootConcept) rootConcept.textContent = String(adv.mistakes.conceptual.count);

  renderRootCauseMistakes(adv.mistakes.mistakes, currentMistakeFilter);
}

async function renderLocalJournal(activeView = journalState.activeView, filterStatus = journalState.filterStatus, searchQuery = journalState.searchQuery) {
  void renderAdvancedProgressDashboard();
  const container = $("#localJournalContent");
  if (!container) {
    return;
  }

  journalState.activeView = activeView;
  journalState.filterStatus = filterStatus;
  journalState.searchQuery = searchQuery;

  if (!window.AptitudeLocalDB) {
    container.innerHTML = `<div class="empty-state">Local database is not available on this device.</div>`;
    return;
  }

  let analytics;
  let attempts;
  try {
    analytics = await window.AptitudeLocalDB.getLocalAnalytics();
    attempts = await window.AptitudeLocalDB.getAllLocalAttempts();
    const localSessions = await window.AptitudeLocalDB.getAllLocalSessions();
    if (localSessions && localSessions.length > 0) {
      cachedSessions = localSessions;
    }
    if (analytics && analytics.days) {
      const localDays = Object.values(analytics.days).sort((a, b) => (a.date > b.date ? 1 : -1));
      if (localDays.length > 0 && (!cachedTrendDays || cachedTrendDays.length === 0)) {
        cachedTrendDays = localDays.map((d) => ({
          date: d.date,
          display_date: d.date.slice(5),
          accuracy: d.accuracy,
          avg_time: d.avg_time,
          total: d.total,
        }));
      }
    }
    renderPerformanceTrendSvg();
  } catch (err) {
    console.error("Failed to load local journal analytics:", err);
    container.innerHTML = `<div class="empty-state">Unable to read local database: ${escapeHtml(err.message)}</div>`;
    return;
  }

  const badge = $("#totalAttemptsBadge");
  if (badge) {
    badge.textContent = String(analytics.totals.total_unique_questions || analytics.question_list?.length || 0);
  }

  if (analytics && analytics.totals && analytics.totals.total_attempts > 0) {
    const solved = $("#totalSolved");
    if (solved) solved.textContent = String(analytics.totals.total_attempts);
    const acc = $("#accuracyStat");
    if (acc) acc.textContent = `${analytics.totals.accuracy}%`;
    const avg = $("#avgTime");
    if (avg) avg.textContent = `${analytics.totals.avg_time}s`;
    const streak = $("#kpiStreak");
    if (streak && (!streak.textContent || streak.textContent === "0d" || streak.textContent === "0")) {
      const dayCount = Object.keys(analytics.days || {}).length;
      streak.textContent = `${dayCount} ${dayCount === 1 ? "Day" : "Days"}`;
    }
  }

  document.querySelectorAll(".journal-tab-btn").forEach((b) => {
    b.classList.toggle("is-active", b.dataset.journalView === journalState.activeView);
  });

  const filterBar = $("#journalFilterBar");
  const deepDiag = $("#deepDiagnosticsContainer");
  if (filterBar) {
    filterBar.style.display = (journalState.activeView === "diagnostics") ? "none" : "flex";
  }
  if (deepDiag) {
    deepDiag.hidden = (journalState.activeView !== "diagnostics");
  }

  let overallAvgTime = analytics.totals.avg_time || 0;
  renderProgressExplorer(attempts);
  const scopedAttempts = scopedProgressAttempts(attempts);
  renderProgressScopeSummary(scopedAttempts);
  const scopeAvgTime = scopedAttempts.length
    ? scopedAttempts.reduce((sum, attempt) => sum + Number(attempt.time_taken || 0), 0) / scopedAttempts.length
    : overallAvgTime;
  overallAvgTime = scopeAvgTime;

  if (journalState.activeView === "diagnostics") {
    container.innerHTML = `
      <div class="diagnostics-intro-banner" style="padding:14px 18px; background:var(--surface-muted); border:1px solid var(--line); border-radius:10px; margin-bottom:12px;">
        <h4 style="margin:0 0 4px; font-size:15px; color:var(--text); font-weight:700;">🔬 Diagnostic Intelligence Hub</h4>
        <p style="margin:0; font-size:13px; color:var(--muted);">
          In-depth strategic evaluation of your Exam Readiness Index, AI-generated prescriptions, and 4-Quadrant speed vs accuracy classification below.
        </p>
      </div>
    `;
    return;
  }

  if (!attempts.length) {
    container.innerHTML = `
      <div class="empty-state" style="padding: 36px 20px; text-align: center;">
        <div style="font-size: 42px; margin-bottom: 12px;">📊</div>
        <h3 style="font-size: 17px; margin-bottom: 8px; color: var(--text);">No practice attempts recorded yet</h3>
        <p style="color: var(--muted); font-size: 14px; max-width: 440px; margin: 0 auto 18px;">
          Practice any aptitude topic to start generating your day-wise history, speed analysis, and mistake book on this device.
        </p>
        <button class="primary-button" type="button" onclick="document.querySelector('[data-screen-target=practice]')?.click()">
          🚀 Start Practice Now
        </button>
      </div>
    `;
    return;
  }

  if (journalState.activeView === "mistakes") {
    const mistakes = attempts.filter((a) => !a.is_correct || a.is_timeout);
    const timeoutCount = mistakes.filter((m) => m.is_timeout).length;
    const calcCount = mistakes.filter((m) => !m.is_timeout && m.typed_answer !== null && m.typed_answer !== "").length;
    const otherCount = mistakes.length - timeoutCount - calcCount;

    const filteredMistakes = mistakes.filter((a) => {
      if (journalState.filterStatus === "slow" && !a.is_timeout && a.time_taken <= (overallAvgTime || 15)) return false;
      if (journalState.filterStatus === "timeout" && !a.is_timeout) return false;
      if (journalState.searchQuery) {
        const q = journalState.searchQuery.toLowerCase();
        const qText = (a.question_text || "").toLowerCase();
        const patName = (a.pattern_name || "").toLowerCase();
        const topName = (a.topic_name || "").toLowerCase();
        if (!qText.includes(q) && !patName.includes(q) && !topName.includes(q)) return false;
      }
      return true;
    });

    if (!mistakes.length) {
      container.innerHTML = `
        <div class="empty-state" style="padding: 32px 20px; text-align: center;">
          <div style="font-size: 40px; margin-bottom: 12px;">🎉</div>
          <h3 style="font-size: 17px; margin-bottom: 8px; color: var(--text);">Zero Mistakes Logged!</h3>
          <p style="color: var(--muted); font-size: 14px;">Great work! You haven't made any mistakes in your recorded practice sessions.</p>
        </div>
      `;
      return;
    }

    const cardsHtml = filteredMistakes.map((a) => renderJournalAttemptCard(a, overallAvgTime)).join("");

    container.innerHTML = `
      <div class="mistake-book-header" style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; margin-bottom:14px; padding:12px 16px; background:var(--surface-muted); border:1px solid var(--line); border-radius:10px;">
        <div style="display:flex; gap:8px; align-items:center; flex-wrap:wrap;">
          <span class="journal-badge badge-wrong" style="font-size:13px; font-weight:700;">🥊 ${mistakes.length} Total Mistakes</span>
          <span class="journal-badge badge-timeout">⏱️ ${timeoutCount} Timed Out</span>
          <span class="journal-badge badge-calc">🧮 ${calcCount} Calculation</span>
          <span class="journal-badge badge-concept">❓ ${otherCount} Conceptual</span>
        </div>
        <button class="accent-button pulse-button" id="journalDrillMistakesBtn" type="button">
          ⚡ Drill Mistake Book
        </button>
      </div>
      <div class="mistake-cards-list" style="display:flex; flex-direction:column; gap:12px;">
        ${cardsHtml}
      </div>
    `;

    const drillBtn = $("#journalDrillMistakesBtn");
    if (drillBtn) {
      drillBtn.addEventListener("click", () => {
        void startAllMistakeRetry();
      });
    }
    return;
  }

  const filteredAttempts = scopedAttempts.filter((a) => {
    if (journalState.filterStatus === "correct" && !a.is_correct) return false;
    if (journalState.filterStatus === "wrong" && a.is_correct) return false;
    if (journalState.filterStatus === "slow") {
      const isSlow = a.time_taken > (overallAvgTime || 15) || Boolean(a.is_timeout);
      if (!isSlow) return false;
    }
    if (journalState.filterStatus === "timeout" && !a.is_timeout) return false;

    if (journalState.searchQuery) {
      const q = journalState.searchQuery.toLowerCase();
      const qText = (a.question_text || "").toLowerCase();
      const patName = (a.pattern_name || "").toLowerCase();
      const topName = (a.topic_name || "").toLowerCase();
      const catName = (a.category_name || "").toLowerCase();
      if (!qText.includes(q) && !patName.includes(q) && !topName.includes(q) && !catName.includes(q)) {
        return false;
      }
    }
    return true;
  });

  if (!attempts.length) {
    container.innerHTML = `<div class="empty-state">No practice attempts recorded yet on this device. Practice any topic to see your journal grow!</div>`;
    return;
  }

  if (!filteredAttempts.length) {
    container.innerHTML = `<div class="empty-state">No attempts match your search or filter criteria.</div>`;
    return;
  }

  // View 1: Day-Wise
  if (journalState.activeView === "day") {
    const dayGroups = new Map();
    filteredAttempts.forEach((a) => {
      const d = a.date || (a.timestamp ? new Date(a.timestamp).toISOString().slice(0, 10) : "Unknown Date");
      if (!dayGroups.has(d)) {
        dayGroups.set(d, []);
      }
      dayGroups.get(d).push(a);
    });

    const dayCards = Array.from(dayGroups.entries()).map(([d, dayAttempts], idx) => {
      const count = dayAttempts.length;
      const correct = dayAttempts.filter((a) => a.is_correct).length;
      const accuracy = count > 0 ? Math.round((correct / count) * 100) : 0;
      const sumTime = dayAttempts.reduce((acc, a) => acc + Number(a.time_taken || 0), 0);
      const avgTime = count > 0 ? (sumTime / count).toFixed(1) : 0;
      const slowCount = dayAttempts.filter((a) => a.time_taken > (overallAvgTime || 15) || a.is_timeout).length;

      const attemptsHtml = dayAttempts.map((a) => renderJournalAttemptCard(a, overallAvgTime)).join("");

      return `
        <details class="journal-group" ${idx === 0 ? "open" : ""}>
          <summary class="journal-group-header">
            <div><strong>📅 ${escapeHtml(d)}</strong></div>
            <div class="journal-group-stats">
              <span><strong>${count}</strong> Questions</span>
              <span>•</span>
              <span class="journal-badge ${accuracy >= 75 ? "badge-correct" : accuracy < 50 ? "badge-wrong" : "badge-slow"}">${accuracy}% Accuracy</span>
              <span>•</span>
              <span>Avg <strong>${avgTime}s</strong></span>
              ${slowCount > 0 ? `<span>• <strong class="badge-slow" style="padding:1px 6px;border-radius:4px;">${slowCount} Slow</strong></span>` : ""}
            </div>
          </summary>
          <div class="journal-group-body">
            ${attemptsHtml}
          </div>
        </details>
      `;
    }).join("");

    container.innerHTML = dayCards;
    return;
  }

  // View 2: Category-Wise
  if (journalState.activeView === "category") {
    const cats = Object.values(analytics.categories);
    if (!cats.length) {
      container.innerHTML = `<div class="empty-state">No category data available.</div>`;
      return;
    }

    const catCards = cats.map((cat) => {
      const catAttempts = filteredAttempts.filter((a) => a.category_name === cat.category);
      const topics = Object.values(cat.topics || {});

      const topicsHtml = topics.map((t) => `
        <div style="display:flex;justify-content:space-between;align-items:center;padding:8px 12px;background:var(--surface);border:1px solid var(--line);border-radius:6px;margin-top:6px;">
          <div>
            <strong style="font-size:13px;color:var(--text);">${escapeHtml(t.topic)}</strong>
            <span style="font-size:12px;color:var(--muted);margin-left:8px;">${t.total} attempts</span>
          </div>
          <div style="display:flex;gap:8px;align-items:center;">
            <span class="journal-badge ${t.accuracy >= 75 ? "badge-correct" : t.accuracy < 50 ? "badge-wrong" : "badge-slow"}">${t.accuracy}%</span>
            <span style="font-size:12px;color:var(--muted);">Avg ${t.avg_time}s</span>
          </div>
        </div>
      `).join("");

      return `
        <details class="journal-group" open>
          <summary class="journal-group-header">
            <div><strong>📚 ${escapeHtml(cat.category)}</strong></div>
            <div class="journal-group-stats">
              <span><strong>${cat.total}</strong> Solved</span>
              <span>•</span>
              <span class="journal-badge ${cat.accuracy >= 75 ? "badge-correct" : cat.accuracy < 50 ? "badge-wrong" : "badge-slow"}">${cat.accuracy}% Accuracy</span>
              <span>•</span>
              <span>Avg <strong>${cat.avg_time}s</strong></span>
            </div>
          </summary>
          <div class="journal-group-body">
            <div style="font-size:13px;font-weight:600;color:var(--muted);margin-bottom:4px;">Sub-Topics in this Category:</div>
            ${topicsHtml || `<div class="empty-state" style="padding:8px;">No topics recorded.</div>`}
            ${catAttempts.length > 0 ? `
              <div style="margin-top:10px;font-size:13px;font-weight:600;color:var(--muted);">Recent Filtered Questions (${catAttempts.length}):</div>
              ${catAttempts.slice(0, 10).map((a) => renderJournalAttemptCard(a, overallAvgTime)).join("")}
            ` : ""}
          </div>
        </details>
      `;
    }).join("");

    container.innerHTML = catCards;
    return;
  }

  // View 3: Sub-Topic (Pattern)
  if (journalState.activeView === "pattern") {
    const patterns = Object.values(analytics.patterns);
    if (!patterns.length) {
      container.innerHTML = `<div class="empty-state">No pattern data available.</div>`;
      return;
    }

    patterns.sort((a, b) => b.total - a.total);

    const patternCards = patterns.map((p) => {
      const isWeak = p.accuracy < 60 || p.slow_count > 0;
      const patternAttempts = filteredAttempts.filter((a) => Number(a.pattern_id) === Number(p.pattern_id));
      const patQuestions = p.question_list || [];

      const questionsTableHtml = patQuestions.length > 0 ? `
        <div class="pattern-questions-section">
          <div class="pattern-questions-header">
            <span>🔍 Specific Questions Tested (<strong>${patQuestions.length}</strong> unique)</span>
            <span style="font-size:11px;font-weight:normal;color:var(--muted);">Repetition &amp; performance breakdown</span>
          </div>
          <div class="pattern-q-list">
            ${patQuestions.map((q) => {
              const isCorr = q.accuracy >= 75;
              const isSlow = q.avg_time > (overallAvgTime || 15) || q.timeout_count > 0;
              return `
                <div class="pattern-q-row">
                  <div class="pattern-q-info">
                    <span class="badge-frequency">👁️ Seen ${q.total_seen} ${q.total_seen === 1 ? "time" : "times"}</span>
                    <span class="pattern-q-text">${escapeHtml(q.question_text || "Question")}</span>
                  </div>
                  <div class="pattern-q-metrics">
                    <span class="journal-badge ${isCorr ? "badge-correct" : q.accuracy < 50 ? "badge-wrong" : "badge-slow"}">${q.accuracy}% (${q.correct_count}/${q.total_seen})</span>
                    <span class="journal-badge ${isSlow ? "badge-slow" : "badge-fast"}">${isSlow ? "🐢" : "⚡"} ${q.avg_time}s</span>
                    <span class="pattern-q-date">Last: ${escapeHtml(q.last_date || "—")}</span>
                  </div>
                </div>
              `;
            }).join("")}
          </div>
        </div>
      ` : "";

      return `
        <details class="journal-group">
          <summary class="journal-group-header">
            <div>
              <strong>🎯 ${escapeHtml(p.pattern_name)}</strong>
              <span style="font-size:12px;color:var(--muted);margin-left:6px;">(${escapeHtml(p.category_name)} › ${escapeHtml(p.topic_name)})</span>
            </div>
            <div class="journal-group-stats">
              <span><strong>${p.total}</strong> Solved</span>
              <span>•</span>
              <span><strong>${p.unique_questions_count || patQuestions.length}</strong> Unique Questions</span>
              <span>•</span>
              <span class="journal-badge ${p.accuracy >= 75 ? "badge-correct" : p.accuracy < 50 ? "badge-wrong" : "badge-slow"}">${p.accuracy}%</span>
              <span>•</span>
              <span>Avg <strong>${p.avg_time}s</strong></span>
              ${isWeak ? `<span class="journal-badge badge-wrong">Needs Focus</span>` : `<span class="journal-badge badge-correct">Strong</span>`}
            </div>
          </summary>
          <div class="journal-group-body">
            ${patternAttempts.length > 0
              ? patternAttempts.map((a) => renderJournalAttemptCard(a, overallAvgTime)).join("")
              : `<div class="empty-state" style="padding:8px;">No matching attempts in current filter.</div>`
            }
            ${questionsTableHtml}
            ${patternAttempts.length > 0 ? `
              <details class="pattern-raw-attempts-details" style="margin-top:12px;border-top:1px solid var(--line);padding-top:10px;">
                <summary style="cursor:pointer;font-size:12px;font-weight:600;color:var(--accent);user-select:none;">
                  <span>📝 View Chronological Attempt Stream (${patternAttempts.length} attempts)</span>
                </summary>
                <div style="margin-top:8px;display:flex;flex-direction:column;gap:8px;">
                  ${patternAttempts.map((a) => renderJournalAttemptCard(a, overallAvgTime)).join("")}
                </div>
              </details>
            ` : `<div class="empty-state" style="padding:8px;">No matching attempts in current filter.</div>`}
          </div>
        </details>
      `;
    }).join("");

    container.innerHTML = patternCards;
    return;
  }

  // View 4: All Questions
  // View 4: Question Frequency & Stats
  if (journalState.activeView === "questions") {
    const attemptsHtml = filteredAttempts.map((a) => renderJournalAttemptCard(a, overallAvgTime)).join("");
    container.innerHTML = attemptsHtml;
    let qList = buildScopedQuestionStats(scopedAttempts);

    if (journalState.filterStatus === "correct") {
      qList = qList.filter((q) => q.accuracy === 100);
    } else if (journalState.filterStatus === "wrong") {
      qList = qList.filter((q) => q.wrong_count > 0);
    } else if (journalState.filterStatus === "slow") {
      qList = qList.filter((q) => q.slow_count > 0 || q.avg_time > (overallAvgTime || 15));
    } else if (journalState.filterStatus === "timeout") {
      qList = qList.filter((q) => q.timeout_count > 0);
    }

    if (journalState.searchQuery) {
      const query = journalState.searchQuery.toLowerCase();
      qList = qList.filter((q) => {
        const qText = (q.question_text || "").toLowerCase();
        const pName = (q.pattern_name || "").toLowerCase();
        const cName = (q.category_name || "").toLowerCase();
        const tName = (q.topic_name || "").toLowerCase();
        return qText.includes(query) || pName.includes(query) || cName.includes(query) || tName.includes(query);
      });
    }

    if (!qList.length) {
      container.innerHTML = `<div class="empty-state">No questions match your search or filter criteria.</div>`;
      return;
    }

    const cardsHtml = qList.map((q) => renderQuestionFrequencyCard(q, overallAvgTime)).join("");

    container.innerHTML = `
      <div class="questions-view-summary-bar">
        <div>
          <strong>Showing ${qList.length} Unique Questions</strong>
          <span style="color:var(--muted);margin-left:6px;">(${filteredAttempts.length} total attempts)</span>
        </div>
        <div style="font-size:12px;color:var(--muted);">
          Each card tracks one exact question • Ranked by: <strong>Times Seen</strong>
        </div>
      </div>
      <div class="questions-frequency-list">
        ${cardsHtml}
      </div>
    `;
    return;
  }
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
  if (window.AptitudeLocalDB) {
    try {
      await window.AptitudeLocalDB.initLocalDB();
    } catch (e) {
      console.warn("IndexedDB initialization warning:", e);
    }
  }
  await initWebConfig();
  initInternalProfile();
  setSoundEnabled(readSoundPreference());
  setAnswerMode(readAnswerModePreference());
  bindEvents();
  renderProgressVisuals();
  void loadCatalog();
  void loadProfile();
  void renderLocalJournal();
  // Pre-initialize English section in background so DOM is ready immediately
  try {
    if (window.EnglishApp && typeof window.EnglishApp.init === "function") {
      window.EnglishApp.init();
    }
  } catch (e) {
    console.warn("EnglishApp initial pre-render warning:", e);
  }
  // Local IndexedDB is the primary history source. Server history, when
  // available, is only a background enhancement and never blocks the journal.
  void syncServerHistory().then(() => renderLocalJournal());

  // Restore screen preference or hash
  const initialHash = (window.location.hash || "").replace(/^#/, "");
  const savedScreen = (function () {
    try {
      return window.localStorage?.getItem("aptitudeActiveScreen");
    } catch (e) {
      return null;
    }
  })();
  if (initialHash === "english" || (!initialHash && savedScreen === "english")) {
    setScreen("english");
  } else if (initialHash === "progress" || (!initialHash && savedScreen === "progress")) {
    setScreen("progress");
  }

  window.addEventListener("hashchange", () => {
    const hash = (window.location.hash || "").replace(/^#/, "");
    if (hash === "english" || hash === "progress" || hash === "practice") {
      setScreen(hash);
    }
  });
}

boot();

