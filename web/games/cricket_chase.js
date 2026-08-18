(function () {
  "use strict";

  window.AptitudeGameModes = window.AptitudeGameModes || {};

  var DEFAULT_TARGET = 58;
  var TOTAL_BALLS = 30;
  var STARTING_WICKETS = 3;
  var FAST_BOUNDARY_MS = 9000;
  var FAST_THREE_MS = 15000;

  function clamp(value, min, max) {
    return Math.max(min, Math.min(max, value));
  }

  function toNumber(value, fallback) {
    var parsed = Number(value);
    return Number.isFinite(parsed) ? parsed : fallback;
  }

  function escapeHtml(value) {
    return String(value == null ? "" : value)
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#039;");
  }

  function ensureState(state) {
    state = state || {};
    state.cricketChase = state.cricketChase || {};
    var game = state.cricketChase;

    if (!game.initialized) {
      game.initialized = true;
      game.target = toNumber(game.target, DEFAULT_TARGET);
      game.totalBalls = toNumber(game.totalBalls, TOTAL_BALLS);
      game.wicketsLimit = toNumber(game.wicketsLimit, STARTING_WICKETS);
      game.runs = toNumber(game.runs, 0);
      game.balls = toNumber(game.balls, 0);
      game.wickets = toNumber(game.wickets, 0);
      game.dotBalls = toNumber(game.dotBalls, 0);
      game.boundaries = toNumber(game.boundaries, 0);
      game.sixes = toNumber(game.sixes, 0);
      game.correct = toNumber(game.correct, 0);
      game.wrong = toNumber(game.wrong, 0);
      game.streak = toNumber(game.streak, 0);
      game.bestStreak = toNumber(game.bestStreak, 0);
      game.lastBall = game.lastBall || null;
      game.recentBalls = Array.isArray(game.recentBalls) ? game.recentBalls : [];
      game.timeline = Array.isArray(game.timeline) ? game.timeline : [];
      game.questionStartedAt = game.questionStartedAt || null;
      game.status = game.status || "First innings pressure";
      game.phase = game.phase || "powerplay";
    }

    return game;
  }

  function ballsLeft(game) {
    return Math.max(0, game.totalBalls - game.balls);
  }

  function runsNeeded(game) {
    return Math.max(0, game.target - game.runs);
  }

  function requiredRate(game) {
    var left = ballsLeft(game);
    if (runsNeeded(game) === 0) {
      return "0.00";
    }
    if (!left) {
      return "INF";
    }
    return ((runsNeeded(game) / left) * 6).toFixed(2);
  }

  function currentRate(game) {
    if (!game.balls) {
      return "0.00";
    }
    return ((game.runs / game.balls) * 6).toFixed(2);
  }

  function overText(balls) {
    var overs = Math.floor(balls / 6);
    var ball = balls % 6;
    return overs + "." + ball;
  }

  function chaseProgress(game) {
    return clamp((game.runs / Math.max(1, game.target)) * 100, 0, 100);
  }

  function pressureLabel(game) {
    if (runsNeeded(game) === 0) {
      return "Chase sealed";
    }
    if (game.wickets >= game.wicketsLimit) {
      return "All out";
    }
    var req = Number(requiredRate(game));
    if (!Number.isFinite(req)) {
      return "Final ball review";
    }
    if (req >= 12) {
      return "Red-zone chase";
    }
    if (req >= 8.5) {
      return "High pressure";
    }
    if (req >= 6) {
      return "Balanced chase";
    }
    return "In control";
  }

  function phaseFor(game) {
    var left = ballsLeft(game);
    if (runsNeeded(game) === 0) {
      return "won";
    }
    if (game.wickets >= game.wicketsLimit || left === 0) {
      return "closed";
    }
    if (left <= 6) {
      return "death";
    }
    if (game.balls < 12) {
      return "powerplay";
    }
    return "middle";
  }

  function isTerminal(game) {
    return runsNeeded(game) === 0 || game.wickets >= game.wicketsLimit || ballsLeft(game) === 0;
  }

  function inferElapsedMs(result, state, game) {
    var explicit = result && (
      result.elapsed_ms ||
      result.elapsedMs ||
      result.time_ms ||
      result.answer_time_ms ||
      result.response_time_ms
    );
    if (Number.isFinite(Number(explicit))) {
      return Number(explicit);
    }

    var seconds = result && (
      result.elapsed_seconds ||
      result.elapsedSeconds ||
      result.time_seconds ||
      result.answer_time_seconds ||
      result.response_time_seconds
    );
    if (Number.isFinite(Number(seconds))) {
      return Number(seconds) * 1000;
    }

    var startedAt = game.questionStartedAt || state.questionStartedAt;
    if (startedAt) {
      return Date.now() - Number(startedAt);
    }

    return null;
  }

  function isCorrect(result) {
    return Boolean(result && (
      result.is_correct === true ||
      result.correct === true ||
      result.isCorrect === true
    ));
  }

  function runsForAnswer(result, state, game) {
    if (!isCorrect(result)) {
      return 0;
    }

    var elapsedMs = inferElapsedMs(result, state, game);
    var streakBonus = game.streak >= 2 ? 1 : 0;

    if (elapsedMs !== null && elapsedMs <= FAST_BOUNDARY_MS) {
      return game.streak >= 3 ? 6 : 4;
    }
    if (elapsedMs !== null && elapsedMs <= FAST_THREE_MS) {
      return 3 + streakBonus;
    }
    if (game.streak >= 4) {
      return 4;
    }
    if (game.streak >= 2) {
      return 2;
    }
    return 1;
  }

  function ballLabel(runs, wicket) {
    if (wicket) {
      return "W";
    }
    return String(runs);
  }

  function ballClass(entry) {
    if (!entry) {
      return "";
    }
    if (entry.wicket) {
      return " is-wicket";
    }
    if (entry.runs >= 6) {
      return " is-six";
    }
    if (entry.runs >= 4) {
      return " is-four";
    }
    if (entry.runs === 0) {
      return " is-dot";
    }
    return " is-run";
  }

  function commentaryFor(entry, game) {
    if (entry.wicket) {
      return "Wicket. The chase tightens under the lights.";
    }
    if (entry.runs >= 6) {
      return "Picked up early and launched into the second tier.";
    }
    if (entry.runs >= 4) {
      return "Clean boundary. Required rate takes a visible hit.";
    }
    if (entry.runs >= 3) {
      return "Sharp running. The field is being stretched.";
    }
    if (entry.runs > 0) {
      return "Worked into the gap. Scoreboard keeps moving.";
    }
    if (ballsLeft(game) <= 6) {
      return "Dot ball at the death. Every decision matters now.";
    }
    return "Dot ball. The bowling side buys pressure.";
  }

  function renderRecentBalls(game) {
    var balls = game.recentBalls.slice(-12);
    if (!balls.length) {
      return '<span class="game-cricket-ball is-empty">-</span>'.repeat(6);
    }

    return balls.map(function (entry) {
      return '<span class="game-cricket-ball' + ballClass(entry) + '">' +
        escapeHtml(ballLabel(entry.runs, entry.wicket)) +
        "</span>";
    }).join("");
  }

  function renderWickets(game) {
    var slots = [];
    for (var index = 0; index < game.wicketsLimit; index += 1) {
      slots.push('<span class="game-cricket-wicket ' + (index < game.wickets ? "is-lost" : "is-standing") + '"></span>');
    }
    return slots.join("");
  }

  function outcomeText(game) {
    if (runsNeeded(game) === 0) {
      return "Target chased";
    }
    if (game.wickets >= game.wicketsLimit) {
      return "All out";
    }
    if (ballsLeft(game) === 0) {
      return "Overs complete";
    }
    return pressureLabel(game);
  }

  function renderIntro() {
    return [
      '<section class="game-cricket-intro">',
      '  <div class="game-cricket-floodlights" aria-hidden="true"></div>',
      '  <div class="game-cricket-intro-copy">',
      '    <p class="game-cricket-kicker">Premium chase mode</p>',
      '    <h2>Cricket Chase Deluxe</h2>',
      '    <p>Turn aptitude accuracy into a disciplined T20 pursuit: fast correct answers find the rope, steady answers rotate strike, and mistakes cost wickets under broadcast lights.</p>',
      '  </div>',
      '  <div class="game-cricket-toss-card">',
      '    <span>Target</span>',
      '    <strong>' + DEFAULT_TARGET + '</strong>',
      '    <small>in ' + TOTAL_BALLS + ' balls</small>',
      '  </div>',
      '</section>'
    ].join("");
  }

  function renderHud(state) {
    var game = ensureState(state);
    return [
      '<div class="game-cricket-hud game-cricket-phase-' + escapeHtml(phaseFor(game)) + '">',
      '  <div class="game-cricket-scorebug">',
      '    <span>CHASE</span>',
      '    <strong>' + game.runs + '/' + game.wickets + '</strong>',
      '    <small>' + overText(game.balls) + ' ov</small>',
      '  </div>',
      '  <div class="game-cricket-hud-stat">',
      '    <span>Need</span>',
      '    <strong>' + runsNeeded(game) + '</strong>',
      '    <small>' + ballsLeft(game) + ' balls</small>',
      '  </div>',
      '  <div class="game-cricket-hud-stat">',
      '    <span>Req RR</span>',
      '    <strong>' + requiredRate(game) + '</strong>',
      '    <small>Curr ' + currentRate(game) + '</small>',
      '  </div>',
      '  <div class="game-cricket-hud-stat">',
      '    <span>Streak</span>',
      '    <strong>' + game.streak + '</strong>',
      '    <small>Best ' + game.bestStreak + '</small>',
      '  </div>',
      '</div>'
    ].join("");
  }

  function renderScene(state) {
    var game = ensureState(state);
    var progress = chaseProgress(game);

    return [
      '<section class="game-cricket-scene game-cricket-phase-' + escapeHtml(phaseFor(game)) + '">',
      '  <div class="game-cricket-stadium" aria-hidden="true">',
      '    <div class="game-cricket-light game-cricket-light-left"></div>',
      '    <div class="game-cricket-light game-cricket-light-right"></div>',
      '    <div class="game-cricket-grandstand"></div>',
      '    <div class="game-cricket-boundary"></div>',
      '    <div class="game-cricket-pitch"></div>',
      '  </div>',
      '  <div class="game-cricket-broadcast-panel">',
      '    <div class="game-cricket-panel-topline">',
      '      <span>' + escapeHtml(outcomeText(game)) + '</span>',
      '      <strong>' + escapeHtml(game.status) + '</strong>',
      '    </div>',
      '    <div class="game-cricket-score-row">',
      '      <div>',
      '        <span>Runs</span>',
      '        <strong>' + game.runs + '</strong>',
      '      </div>',
      '      <div>',
      '        <span>Target</span>',
      '        <strong>' + game.target + '</strong>',
      '      </div>',
      '      <div>',
      '        <span>Overs</span>',
      '        <strong>' + overText(game.balls) + '</strong>',
      '      </div>',
      '    </div>',
      '    <div class="game-cricket-progress" aria-label="Chase progress">',
      '      <div style="width: ' + progress.toFixed(1) + '%"></div>',
      '    </div>',
      '    <div class="game-cricket-lower-grid">',
      '      <div class="game-cricket-rate-card">',
      '        <span>Required rate</span>',
      '        <strong>' + requiredRate(game) + '</strong>',
      '        <small>Current ' + currentRate(game) + '</small>',
      '      </div>',
      '      <div class="game-cricket-wickets-card">',
      '        <span>Wickets in hand</span>',
      '        <div class="game-cricket-wickets">' + renderWickets(game) + '</div>',
      '      </div>',
      '    </div>',
      '    <div class="game-cricket-recent">',
      '      <span>Recent balls</span>',
      '      <div>' + renderRecentBalls(game) + '</div>',
      '    </div>',
      '  </div>',
      '</section>'
    ].join("");
  }

  function onQuestion(question, state) {
    var game = ensureState(state);
    if (isTerminal(game)) {
      game.phase = phaseFor(game);
      game.status = outcomeText(game);
      return state;
    }
    game.questionStartedAt = Date.now();
    game.activeQuestionNumber = question && (question.question_number || question.number || question.id) || null;
    game.phase = phaseFor(game);
    game.status = runsNeeded(game) === 0
      ? "The dressing room is already standing."
      : "Set for ball " + (game.balls + 1) + ". Read the field, then commit.";
    return state;
  }

  function onAnswer(result, state) {
    var game = ensureState(state);
    if (isTerminal(game)) {
      game.phase = phaseFor(game);
      game.status = outcomeText(game);
      return state;
    }
    var correct = isCorrect(result);
    var runs = runsForAnswer(result, state, game);
    var wicket = !correct;

    game.balls = clamp(game.balls + 1, 0, game.totalBalls);
    game.runs = clamp(game.runs + runs, 0, 999);
    game.wickets = clamp(game.wickets + (wicket ? 1 : 0), 0, game.wicketsLimit);
    game.correct += correct ? 1 : 0;
    game.wrong += correct ? 0 : 1;
    game.dotBalls += runs === 0 ? 1 : 0;
    game.boundaries += runs >= 4 ? 1 : 0;
    game.sixes += runs >= 6 ? 1 : 0;
    game.streak = correct ? game.streak + 1 : 0;
    game.bestStreak = Math.max(game.bestStreak, game.streak);

    var entry = {
      ball: game.balls,
      over: overText(game.balls),
      runs: runs,
      wicket: wicket,
      correct: correct,
      label: ballLabel(runs, wicket)
    };

    game.lastBall = entry;
    game.recentBalls.push(entry);
    game.timeline.push(entry);
    if (game.recentBalls.length > 18) {
      game.recentBalls = game.recentBalls.slice(-18);
    }
    if (game.timeline.length > 60) {
      game.timeline = game.timeline.slice(-60);
    }

    game.phase = phaseFor(game);
    game.status = commentaryFor(entry, game);

    return state;
  }

  function isComplete(state) {
    return isTerminal(ensureState(state));
  }

  function onStop(state) {
    var game = ensureState(state);
    game.stopped = true;
    game.phase = "closed";
    game.status = runsNeeded(game) === 0
      ? "Chase completed before the halt."
      : "Players called in with " + runsNeeded(game) + " still needed.";
    return state;
  }

  function getSummaryLines(summary, state) {
    var game = ensureState(state);
    var total = summary && toNumber(summary.total_questions, game.balls);
    var accuracy = summary && summary.accuracy != null
      ? summary.accuracy + "%"
      : (total ? Math.round((game.correct / total) * 100) + "%" : "0%");
    var result = runsNeeded(game) === 0
      ? "Won by " + Math.max(0, game.wicketsLimit - game.wickets) + " wickets"
      : "Short by " + runsNeeded(game) + " runs";

    return [
      result + " - " + game.runs + "/" + game.wickets + " in " + overText(game.balls) + " overs.",
      "Required rate finished at " + requiredRate(game) + "; scoring rate was " + currentRate(game) + ".",
      "Boundaries: " + game.boundaries + " including " + game.sixes + " sixes; dot balls: " + game.dotBalls + ".",
      "Accuracy: " + accuracy + "; best scoring streak: " + game.bestStreak + "."
    ];
  }

  window.AptitudeGameModes.cricketChase = {
    id: "cricketChase",
    title: "Cricket Chase Deluxe",
    shortTitle: "Cricket Chase",
    subtitle: "A premium broadcast-style run chase where speed and accuracy become scoreboard pressure.",
    category: "sports-strategy",
    recommendedPatternNames: [
      "Percentages",
      "Ratio and Proportion",
      "Averages",
      "Time and Work",
      "Profit and Loss"
    ],
    targetCount: TOTAL_BALLS,
    accent: "#d6b25e",
    renderIntro: renderIntro,
    renderHud: renderHud,
    renderScene: renderScene,
    onQuestion: onQuestion,
    onAnswer: onAnswer,
    onStop: onStop,
    isComplete: isComplete,
    getSummaryLines: getSummaryLines
  };
})();
