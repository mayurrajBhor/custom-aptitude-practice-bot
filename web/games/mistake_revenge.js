(function () {
  "use strict";

  window.AptitudeGameModes = window.AptitudeGameModes || {};

  const MODE_ID = "mistakeRevenge";
  const MAX_EVIDENCE = 5;

  function escapeHtml(value) {
    return String(value ?? "")
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#039;");
  }

  function clamp(value, min, max) {
    return Math.max(min, Math.min(max, value));
  }

  function ensureState(state) {
    if (!state) {
      return {
        mistakeRevenge: createInitialState(),
      };
    }

    if (!state.mistakeRevenge) {
      state.mistakeRevenge = createInitialState();
    }

    return state;
  }

  function createInitialState() {
    return {
      repairedMistakes: 0,
      riskLevel: 42,
      streak: 0,
      bestStreak: 0,
      reviewed: 0,
      openCases: 0,
      totalAnswered: 0,
      correctAnswered: 0,
      currentQuestion: null,
      currentPattern: "Unclassified",
      lastOutcome: "intake",
      startedAt: Date.now(),
      stopped: false,
      evidence: [],
    };
  }

  function getGameState(state) {
    return ensureState(state).mistakeRevenge;
  }

  function getPatternName(question, result) {
    return (
      result?.pattern_name ||
      result?.patternName ||
      question?.pattern_name ||
      question?.patternName ||
      question?.pattern ||
      question?.topic_name ||
      question?.topicName ||
      "Unclassified"
    );
  }

  function getQuestionText(question, result) {
    return (
      result?.question_text ||
      result?.questionText ||
      question?.question_text ||
      question?.questionText ||
      question?.text ||
      "Question evidence pending"
    );
  }

  function getCorrectOption(result, question) {
    if (result?.correct_option !== undefined) {
      return result.correct_option;
    }
    const index = result?.correct_option_index ?? question?.correct_option_index;
    if (Array.isArray(question?.options) && Number.isInteger(index)) {
      return question.options[index];
    }
    return "Correct answer recorded";
  }

  function getSelectedOption(result, question) {
    if (result?.selected_option !== undefined) {
      return result.selected_option;
    }
    const index = result?.selected_option_index ?? result?.answer_index ?? result?.answerIndex;
    if (Array.isArray(question?.options) && Number.isInteger(index)) {
      return question.options[index];
    }
    return result?.is_skipped ? "Skipped" : "Response recorded";
  }

  function getAccuracy(game) {
    if (!game.totalAnswered) {
      return 0;
    }
    return Math.round((game.correctAnswered / game.totalAnswered) * 100);
  }

  function getRiskLabel(riskLevel) {
    if (riskLevel >= 72) {
      return "Critical";
    }
    if (riskLevel >= 46) {
      return "Elevated";
    }
    if (riskLevel >= 22) {
      return "Controlled";
    }
    return "Contained";
  }

  function pushEvidence(game, item) {
    game.evidence.unshift(item);
    game.evidence = game.evidence.slice(0, MAX_EVIDENCE);
  }

  function renderEvidence(game) {
    if (!game.evidence.length) {
      return `
        <div class="game-revenge-empty">
          <span></span>
          <p>No evidence logged yet. First response opens the correction board.</p>
        </div>
      `;
    }

    return game.evidence.map((item, index) => `
      <article class="game-revenge-evidence ${item.correct ? "is-repaired" : "is-open"}">
        <div class="game-revenge-evidence-index">${String(index + 1).padStart(2, "0")}</div>
        <div>
          <div class="game-revenge-evidence-head">
            <strong>${escapeHtml(item.pattern)}</strong>
            <span>${item.correct ? "Repaired" : "Open defect"}</span>
          </div>
          <p>${escapeHtml(item.question)}</p>
          <div class="game-revenge-answer-row">
            <span>Selected: ${escapeHtml(item.selected)}</span>
            <span>Correct: ${escapeHtml(item.correctOption)}</span>
          </div>
          ${item.explanation ? `<small>${escapeHtml(item.explanation)}</small>` : ""}
        </div>
      </article>
    `).join("");
  }

  function renderIntro() {
    return `
      <section class="game-revenge-shell">
        <div class="game-revenge-hero">
          <div>
            <p class="game-revenge-kicker">Recovery lab</p>
            <h2>Mistake Revenge</h2>
            <p>Re-open weak patterns, isolate the failure signal, and close each case with a verified correction.</p>
          </div>
          <div class="game-revenge-case-stamp" aria-hidden="true">
            <span>MR</span>
            <strong>Forensic Board</strong>
          </div>
        </div>
        <div class="game-revenge-intro-grid">
          <div>
            <span>Objective</span>
            <strong>Repair prior misses</strong>
            <p>Best used with saved mistake patterns or weak-area selections.</p>
          </div>
          <div>
            <span>Scoring lens</span>
            <strong>Risk reduction</strong>
            <p>Correct answers lower risk; repeated misses keep cases open.</p>
          </div>
          <div>
            <span>Review style</span>
            <strong>Evidence trail</strong>
            <p>Each answer is logged as a case note for post-run review.</p>
          </div>
        </div>
      </section>
    `;
  }

  function renderHud(state) {
    const game = getGameState(state);
    const risk = clamp(game.riskLevel, 0, 100);
    const accuracy = getAccuracy(game);

    return `
      <section class="game-revenge-hud" aria-label="Mistake Revenge status">
        <div class="game-revenge-meter">
          <span>Risk</span>
          <strong>${getRiskLabel(risk)}</strong>
          <div class="game-revenge-track"><div style="width: ${risk}%"></div></div>
        </div>
        <div class="game-revenge-stat">
          <span>Repaired</span>
          <strong>${game.repairedMistakes}</strong>
        </div>
        <div class="game-revenge-stat">
          <span>Streak</span>
          <strong>${game.streak}</strong>
        </div>
        <div class="game-revenge-stat">
          <span>Accuracy</span>
          <strong>${accuracy}%</strong>
        </div>
      </section>
    `;
  }

  function renderScene(state) {
    const game = getGameState(state);
    const currentText = getQuestionText(game.currentQuestion);

    return `
      <section class="game-revenge-board">
        <div class="game-revenge-board-main">
          <div class="game-revenge-board-header">
            <div>
              <p class="game-revenge-kicker">Active case</p>
              <h2>${escapeHtml(game.currentPattern)}</h2>
            </div>
            <span class="game-revenge-status ${game.lastOutcome === "repaired" ? "is-repaired" : ""}">
              ${game.lastOutcome === "repaired" ? "Case repaired" : game.lastOutcome === "missed" ? "Defect isolated" : "Evidence intake"}
            </span>
          </div>
          <div class="game-revenge-question-file">
            <span></span>
            <p>${escapeHtml(currentText)}</p>
          </div>
          <div class="game-revenge-scanline" aria-hidden="true"></div>
        </div>
        <aside class="game-revenge-dossier">
          <div class="game-revenge-dossier-head">
            <p class="game-revenge-kicker">Evidence review</p>
            <strong>${game.reviewed} logged</strong>
          </div>
          <div class="game-revenge-evidence-list">
            ${renderEvidence(game)}
          </div>
        </aside>
      </section>
    `;
  }

  function onQuestion(question, state) {
    const game = getGameState(state);
    game.currentQuestion = question || null;
    game.currentPattern = getPatternName(question);
    game.openCases += 1;
    game.lastOutcome = "intake";
    game.stopped = false;
  }

  function onAnswer(result, state) {
    const game = getGameState(state);
    const question = game.currentQuestion || state?.activeQuestion || null;
    const correct = Boolean(result?.is_correct ?? result?.correct);

    game.totalAnswered += 1;
    game.reviewed += 1;
    game.currentPattern = getPatternName(question, result);

    if (correct) {
      game.correctAnswered += 1;
      game.repairedMistakes += 1;
      game.streak += 1;
      game.bestStreak = Math.max(game.bestStreak, game.streak);
      game.openCases = Math.max(0, game.openCases - 1);
      game.riskLevel = clamp(game.riskLevel - 12 - Math.min(game.streak, 4), 0, 100);
      game.lastOutcome = "repaired";
    } else {
      game.streak = 0;
      game.riskLevel = clamp(game.riskLevel + 16, 0, 100);
      game.lastOutcome = "missed";
    }

    pushEvidence(game, {
      correct,
      pattern: game.currentPattern,
      question: getQuestionText(question, result),
      selected: getSelectedOption(result, question),
      correctOption: getCorrectOption(result, question),
      explanation: result?.explanation || "",
    });
  }

  function onStop(state) {
    const game = getGameState(state);
    game.stopped = true;
    game.lastOutcome = "stopped";
  }

  function getSummaryLines(summary, state) {
    const game = getGameState(state);
    const total = summary?.total_questions || summary?.answered || game.totalAnswered || 0;
    const accuracy = summary?.accuracy ?? getAccuracy(game);

    return [
      `${game.repairedMistakes} mistake${game.repairedMistakes === 1 ? "" : "s"} repaired`,
      `${getRiskLabel(game.riskLevel)} residual risk at ${clamp(game.riskLevel, 0, 100)}%`,
      `Best correction streak: ${game.bestStreak}`,
      `Evidence reviewed: ${game.reviewed || total} item${(game.reviewed || total) === 1 ? "" : "s"}`,
      `Session accuracy: ${accuracy}%`,
    ];
  }

  window.AptitudeGameModes.mistakeRevenge = {
    id: MODE_ID,
    title: "Mistake Revenge",
    shortTitle: "Revenge",
    subtitle: "Forensic correction board for repairing prior misses.",
    category: "mistake-pattern-practice",
    recommendedPatternNames: [
      "Careless calculation",
      "Misread condition",
      "Wrong formula selection",
      "Trap answer elimination",
      "Time-pressure mistake",
    ],
    targetCount: 8,
    accent: "#d6a85a",
    renderIntro,
    renderHud,
    renderScene,
    onQuestion,
    onAnswer,
    onStop,
    getSummaryLines,
  };
})();
