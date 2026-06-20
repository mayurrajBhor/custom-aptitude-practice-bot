(function () {
  "use strict";

  window.AptitudeGameModes = window.AptitudeGameModes || {};

  const MODULE_ID = "vedicSprint";
  const TARGET_COUNT = 20;
  const ACCENT = "#19d3ff";
  const FAST_MS = 9000;
  const STEADY_MS = 16000;

  function ensureState(state) {
    const game = state.vedicSprint || {};
    if (!state.vedicSprint) {
      state.vedicSprint = game;
    }
    game.startedAt = game.startedAt || Date.now();
    game.combo = game.combo || 0;
    game.bestStreak = game.bestStreak || 0;
    game.correct = game.correct || 0;
    game.total = game.total || 0;
    game.fastCorrect = game.fastCorrect || 0;
    game.totalMs = game.totalMs || 0;
    game.heat = typeof game.heat === "number" ? game.heat : 42;
    game.focus = typeof game.focus === "number" ? game.focus : 72;
    game.events = game.events || [];
    game.current = game.current || null;
    return game;
  }

  function escapeHtml(value) {
    return String(value ?? "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  function clamp(value, min, max) {
    return Math.max(min, Math.min(max, value));
  }

  function pct(value) {
    return `${Math.round(clamp(value, 0, 100))}%`;
  }

  function number(value, fallback) {
    const parsed = Number(value);
    return Number.isFinite(parsed) ? parsed : fallback;
  }

  function questionText(question) {
    return (
      question?.question_text ||
      question?.text ||
      question?.question ||
      question?.prompt ||
      question?.stem ||
      question?.title ||
      "Mental calculation lock"
    );
  }

  function questionOptions(question) {
    const options = question?.options || question?.choices || question?.answers || [];
    return Array.isArray(options) ? options : [];
  }

  function questionId(question) {
    return question?.id || question?.question_id || question?.variant_id || questionText(question);
  }

  function isCorrectResult(result) {
    if (typeof result === "boolean") {
      return result;
    }
    if (!result) {
      return false;
    }
    if (typeof result.correct === "boolean") {
      return result.correct;
    }
    if (typeof result.isCorrect === "boolean") {
      return result.isCorrect;
    }
    if (typeof result.is_correct === "boolean") {
      return result.is_correct;
    }
    if (typeof result.status === "string") {
      return result.status.toLowerCase() === "correct";
    }
    return false;
  }

  function renderMetric(label, value, detail) {
    return `
      <div class="game-vedic-metric">
        <span class="game-vedic-metric-label">${escapeHtml(label)}</span>
        <strong class="game-vedic-metric-value">${escapeHtml(value)}</strong>
        <span class="game-vedic-metric-detail">${escapeHtml(detail)}</span>
      </div>
    `;
  }

  function renderMeter(label, value, tone) {
    return `
      <div class="game-vedic-meter game-vedic-meter-${escapeHtml(tone)}">
        <div class="game-vedic-meter-row">
          <span>${escapeHtml(label)}</span>
          <strong>${pct(value)}</strong>
        </div>
        <div class="game-vedic-meter-track">
          <span class="game-vedic-meter-fill" style="width: ${pct(value)}"></span>
        </div>
      </div>
    `;
  }

  function currentAccuracy(game) {
    return game.total ? (game.correct / game.total) * 100 : 0;
  }

  function averageSeconds(game) {
    return game.total ? Math.max(1, Math.round(game.totalMs / game.total / 1000)) : 0;
  }

  function sessionTotal(state) {
    return number(
      state?.session?.totalQuestions ||
      state?.activeQuestion?.total_questions ||
      state?.question?.total_questions,
      TARGET_COUNT
    );
  }

  function renderOption(option, index, state) {
    const answer = state?.lastAnswer || null;
    const selected = Number(answer?.selected_option_index ?? answer?.answer_index);
    const correct = Number(answer?.correct_option_index);
    const classes = [
      "game-vedic-option",
      answer && index === correct ? "is-correct" : "",
      answer && index === selected && selected !== correct ? "is-wrong" : "",
    ].filter(Boolean).join(" ");
    return `
      <button class="${classes}" type="button" data-answer-index="${index}" ${state?.answered ? "disabled" : ""}>
        <span>${String.fromCharCode(65 + index)}</span>
        <strong>${escapeHtml(option?.text ?? option?.label ?? option)}</strong>
      </button>
    `;
  }

  function renderIntro() {
    return `
      <section class="game-vedic-intro" aria-label="Vedic Math Sprint briefing">
        <div class="game-vedic-intro-grid">
          <div class="game-vedic-briefing">
            <p class="game-vedic-kicker">Vedic Math Sprint</p>
            <h2 class="game-vedic-title">Mental speed under tactical timing.</h2>
            <p class="game-vedic-copy">
              A precision sprint for arithmetic shortcuts, ratio moves, percentage turns, squares, and factor recognition.
              Every response updates combo pressure, heat load, and focus discipline.
            </p>
          </div>
          <div class="game-vedic-start-console" aria-hidden="true">
            <div class="game-vedic-scope">
              <span></span><span></span><span></span><span></span>
            </div>
            <div class="game-vedic-readout">
              <span>Target</span>
              <strong>${TARGET_COUNT}</strong>
              <em>questions</em>
            </div>
          </div>
        </div>
        <div class="game-vedic-protocols">
          <div><strong>Combo</strong><span>Correct answers stack acceleration.</span></div>
          <div><strong>Heat</strong><span>Fast hits raise load; misses vent pressure.</span></div>
          <div><strong>Focus</strong><span>Accuracy and steady pacing keep control.</span></div>
        </div>
      </section>
    `;
  }

  function renderHud(state) {
    const game = ensureState(state);
    const elapsed = Math.max(0, Math.round((Date.now() - game.startedAt) / 1000));
    return `
      <section class="game-vedic-hud" aria-label="Vedic sprint dashboard">
        ${renderMetric("Combo", `${game.combo}x`, "active chain")}
        ${renderMetric("Best streak", game.bestStreak, "session peak")}
        ${renderMetric("Accuracy", pct(currentAccuracy(game)), `${game.correct}/${game.total || 0} correct`)}
        ${renderMetric("Avg time", `${averageSeconds(game)}s`, `${elapsed}s elapsed`)}
        <div class="game-vedic-hud-meters">
          ${renderMeter("Heat", game.heat, "heat")}
          ${renderMeter("Focus", game.focus, "focus")}
        </div>
      </section>
    `;
  }

  function renderScene(state) {
    const game = ensureState(state);
    const current = game.current;
    const question = current?.question || state.activeQuestion || state.question || null;
    const options = questionOptions(question);
    const totalQuestions = sessionTotal(state);
    const answeredPct = (game.total / totalQuestions) * 100;
    const timerPct = current?.startedAt ? clamp(((Date.now() - current.startedAt) / STEADY_MS) * 100, 0, 100) : 0;

    return `
      <section class="game-vedic-scene" aria-label="Vedic Math Sprint cockpit">
        <div class="game-vedic-cockpit">
          <div class="game-vedic-topline">
            <span class="game-vedic-status-light"></span>
            <span>Timing cockpit armed</span>
            <strong>${escapeHtml(Math.min(game.total + 1, totalQuestions))} / ${totalQuestions}</strong>
          </div>
          <div class="game-vedic-timer">
            <div class="game-vedic-timer-head">
              <span>Question clock</span>
              <strong>${current ? `${Math.max(0, Math.round((Date.now() - current.startedAt) / 1000))}s` : "Ready"}</strong>
            </div>
            <div class="game-vedic-timer-track">
              <span class="game-vedic-timer-fill" style="width: ${pct(timerPct)}"></span>
            </div>
          </div>
          <div class="game-vedic-question-zone">
            <p class="game-vedic-kicker">Live calculation</p>
            <h2 class="game-vedic-question-text">${escapeHtml(questionText(question))}</h2>
            <div class="game-vedic-options" aria-label="Answer choices">
              ${options.map((option, index) => renderOption(option, index, state)).join("") || `<div class="game-vedic-option game-vedic-option-empty"><span>--</span><strong>Question loading</strong></div>`}
            </div>
          </div>
          <div class="game-vedic-progress-panel">
            <div class="game-vedic-ring" style="--game-vedic-progress: ${pct(answeredPct)}">
              <span>${Math.min(game.total, totalQuestions)}</span>
              <em>cleared</em>
            </div>
            <div class="game-vedic-stack">
              ${renderMeter("Heat load", game.heat, "heat")}
              ${renderMeter("Focus lock", game.focus, "focus")}
            </div>
          </div>
        </div>
      </section>
    `;
  }

  function onQuestion(question, state) {
    const game = ensureState(state);
    game.current = {
      id: questionId(question),
      question,
      startedAt: Date.now(),
    };
    game.lastQuestionText = questionText(question);
    return game;
  }

  function onAnswer(result, state) {
    const game = ensureState(state);
    const correct = isCorrectResult(result);
    const elapsedMs = number(result?.elapsedMs ?? result?.elapsed_ms ?? result?.timeMs ?? result?.time_ms, null) ||
      (game.current?.startedAt ? Date.now() - game.current.startedAt : STEADY_MS);
    const fast = elapsedMs <= FAST_MS;

    game.total += 1;
    game.totalMs += elapsedMs;

    if (correct) {
      game.correct += 1;
      game.combo += 1;
      game.bestStreak = Math.max(game.bestStreak, game.combo);
      if (fast) {
        game.fastCorrect += 1;
      }
      game.heat = clamp(game.heat + (fast ? 12 : 7), 0, 100);
      game.focus = clamp(game.focus + (fast ? 4 : 7), 0, 100);
    } else {
      game.combo = 0;
      game.heat = clamp(game.heat - 16, 0, 100);
      game.focus = clamp(game.focus - 18, 0, 100);
    }

    game.events.push({
      id: game.current?.id || game.total,
      correct,
      elapsedMs,
      fast,
      combo: game.combo,
      heat: game.heat,
      focus: game.focus,
    });
    game.current = null;
    return game;
  }

  function onStop(state) {
    const game = ensureState(state);
    game.stoppedAt = Date.now();
    game.current = null;
    return game;
  }

  function getSummaryLines(summary, state) {
    const game = ensureState(state);
    const total = number(summary?.total, game.total);
    const correct = number(summary?.correct, game.correct);
    const accuracy = total ? Math.round((correct / total) * 100) : 0;
    const avg = averageSeconds(game);
    return [
      `Vedic Sprint: ${correct}/${total} correct (${accuracy}% accuracy).`,
      `Best streak: ${game.bestStreak}; fast correct: ${game.fastCorrect}.`,
      `Average timing: ${avg}s; final heat ${Math.round(game.heat)}%, focus ${Math.round(game.focus)}%.`,
    ];
  }

  window.AptitudeGameModes.vedicSprint = {
    id: MODULE_ID,
    title: "Vedic Math Sprint",
    shortTitle: "Vedic Sprint",
    subtitle: "Premium mental arithmetic speed training with combo pressure and timing control.",
    category: "Quantitative Aptitude",
    recommendedPatternNames: [
      "Vedic Math",
      "Mental Arithmetic",
      "Percentages",
      "Squares and Cubes",
      "Number System",
      "Ratios",
      "Approximation",
    ],
    targetCount: TARGET_COUNT,
    accent: ACCENT,
    renderIntro,
    renderHud,
    renderScene,
    onQuestion,
    onAnswer,
    onStop,
    getSummaryLines,
  };
})();
