(function () {
  "use strict";

  window.AptitudeGameModes = window.AptitudeGameModes || {};

  const MODULE_ID = "directionMaze";
  const STATE_KEY = "__directionMazeLive";
  const ACCENT = "#38d5ff";
  const GRID_SIZE = 9;
  const CENTER = Math.floor(GRID_SIZE / 2);
  const DIRECTIONS = {
    north: { x: 0, y: -1, deg: 0, label: "N" },
    northeast: { x: 1, y: -1, deg: 45, label: "NE" },
    east: { x: 1, y: 0, deg: 90, label: "E" },
    southeast: { x: 1, y: 1, deg: 135, label: "SE" },
    south: { x: 0, y: 1, deg: 180, label: "S" },
    southwest: { x: -1, y: 1, deg: 225, label: "SW" },
    west: { x: -1, y: 0, deg: 270, label: "W" },
    northwest: { x: -1, y: -1, deg: 315, label: "NW" },
  };
  const ORDER = ["north", "east", "south", "west"];
  const FALLBACK_ROUTE = ["north", "east", "east", "south", "west", "north", "east", "south"];

  function ensureStylesheet() {
    if (document.getElementById("game-direction-maze-css")) {
      return;
    }
    const link = document.createElement("link");
    link.id = "game-direction-maze-css";
    link.rel = "stylesheet";
    link.href = "/static/games/direction_maze.css?v=2";
    document.head.appendChild(link);
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

  function hashText(text) {
    let hash = 2166136261;
    const source = String(text || "");
    for (let index = 0; index < source.length; index += 1) {
      hash ^= source.charCodeAt(index);
      hash = Math.imul(hash, 16777619);
    }
    return hash >>> 0;
  }

  function getQuestionText(question) {
    return question?.question_text || question?.text || question?.prompt || question?.question || "";
  }

  function getGameState(hostState) {
    if (!hostState) {
      return createGameState();
    }
    if (!hostState[STATE_KEY]) {
      hostState[STATE_KEY] = createGameState();
    }
    return hostState[STATE_KEY];
  }

  function createGameState() {
    return {
      active: false,
      step: 0,
      checkpoint: 1,
      totalCheckpoints: 6,
      confidence: 74,
      integrity: 88,
      drift: 0,
      streak: 0,
      heading: "north",
      lastResult: null,
      lastQuestionHash: null,
      cells: buildCells(),
      route: [{ x: CENTER, y: CENTER, type: "start" }],
      signals: [],
    };
  }

  function buildCells() {
    const cells = [];
    for (let y = 0; y < GRID_SIZE; y += 1) {
      for (let x = 0; x < GRID_SIZE; x += 1) {
        const noise = hashText(`${x}:${y}`) % 11;
        const type = noise === 0 ? "blocked" : noise <= 2 ? "scan" : noise === 3 ? "low" : "";
        cells.push({ x, y, type });
      }
    }
    return cells;
  }

  function normalizeDirectionText(value) {
    return String(value || "")
      .toLowerCase()
      .replace(/\bnorth[\s-]+east\b/g, "northeast")
      .replace(/\bsouth[\s-]+east\b/g, "southeast")
      .replace(/\bsouth[\s-]+west\b/g, "southwest")
      .replace(/\bnorth[\s-]+west\b/g, "northwest");
  }

  function parseHeading(question) {
    const text = normalizeDirectionText(getQuestionText(question));
    const compound = [
      ["north east", "northeast"],
      ["north-east", "northeast"],
      ["south east", "southeast"],
      ["south-east", "southeast"],
      ["south west", "southwest"],
      ["south-west", "southwest"],
      ["north west", "northwest"],
      ["north-west", "northwest"],
    ];
    for (const [needle, heading] of compound) {
      if (text.includes(needle)) {
        return heading;
      }
    }
    for (const heading of Object.keys(DIRECTIONS)) {
      if (new RegExp(`\\b${heading}\\b`).test(text)) {
        return heading;
      }
    }
    const hash = hashText(text);
    return FALLBACK_ROUTE[hash % FALLBACK_ROUTE.length];
  }

  function scaleDistance(value) {
    return clamp(Math.round(Number(value) / 20) || 1, 1, 3);
  }

  function parseMoveCount(question) {
    const text = normalizeDirectionText(getQuestionText(question));
    const match = text.match(/\b(\d{1,2})\s*(?:m|meter|meters|km|kilometer|kilometers|step|steps|blocks?)\b/);
    if (!match) {
      return 1;
    }
    return scaleDistance(match[1]);
  }

  function turnHeading(current, turn) {
    const index = ORDER.indexOf(current);
    if (index === -1) {
      return current;
    }
    if (turn === "left") {
      return ORDER[(index + ORDER.length - 1) % ORDER.length];
    }
    if (turn === "right") {
      return ORDER[(index + 1) % ORDER.length];
    }
    return current;
  }

  function deriveHeading(question, game) {
    const text = normalizeDirectionText(getQuestionText(question));
    if (/\bleft\b/.test(text) && !/\bright\b/.test(text)) {
      return turnHeading(game.heading, "left");
    }
    if (/\bright\b/.test(text) && !/\bleft\b/.test(text)) {
      return turnHeading(game.heading, "right");
    }
    return parseHeading(question);
  }

  function parseMoveCounts(question) {
    const text = normalizeDirectionText(getQuestionText(question));
    return Array.from(text.matchAll(/\b(\d{1,3})\s*(?:m|meter|meters|km|kilometer|kilometers|step|steps|blocks?)\b/g))
      .map((match) => scaleDistance(match[1]));
  }

  function deriveRouteMoves(question, game) {
    const text = normalizeDirectionText(getQuestionText(question));
    const cues = Array.from(text.matchAll(/\b(northeast|northwest|southeast|southwest|north|south|east|west|left|right)\b/g))
      .map((match) => match[1]);
    const counts = parseMoveCounts(question);
    let countIndex = 0;
    let heading = game.heading;
    const moves = [];

    cues.forEach((cue) => {
      if (cue === "left" || cue === "right") {
        heading = turnHeading(heading, cue);
      } else {
        heading = cue;
      }
      moves.push({
        heading,
        moveCount: counts[countIndex] || 1,
      });
      countIndex += 1;
    });

    if (!moves.length) {
      moves.push({
        heading: deriveHeading(question, game),
        moveCount: parseMoveCount(question),
      });
    }

    return moves.slice(0, 4);
  }

  function normalizeRouteForTrace(route) {
    return route.map((point, index) => ({
      ...point,
      type: index === 0 && point.type === "start" ? "start" : "trace",
    }));
  }

  function advanceRoute(game, heading, moveCount) {
    const vector = DIRECTIONS[heading] || DIRECTIONS.north;
    const traceRoute = normalizeRouteForTrace(game.route);
    let current = traceRoute[traceRoute.length - 1] || { x: CENTER, y: CENTER };
    const nextPoints = [];
    for (let index = 0; index < moveCount; index += 1) {
      const next = {
        x: clamp(current.x + vector.x, 0, GRID_SIZE - 1),
        y: clamp(current.y + vector.y, 0, GRID_SIZE - 1),
        type: "trace",
      };
      if (next.x === current.x && next.y === current.y) {
        break;
      }
      nextPoints.push(next);
      current = next;
    }
    if (!nextPoints.length) {
      const fallback = DIRECTIONS[FALLBACK_ROUTE[(game.step + game.route.length) % FALLBACK_ROUTE.length]];
      nextPoints.push({
        x: clamp(current.x + fallback.x, 0, GRID_SIZE - 1),
        y: clamp(current.y + fallback.y, 0, GRID_SIZE - 1),
        type: "trace",
      });
    }
    game.route = traceRoute.concat(nextPoints).slice(-18);
    game.route[game.route.length - 1].type = "current";
  }

  function updateSignals(game, question) {
    const seed = hashText(getQuestionText(question) + game.step);
    game.signals = [
      { label: "GPS", value: 72 + (seed % 23) },
      { label: "IMU", value: 64 + ((seed >> 3) % 29) },
      { label: "MAP", value: game.integrity },
    ];
  }

  function readCorrectness(result) {
    if (!result) {
      return null;
    }
    if (typeof result.correct === "boolean") {
      return result.correct;
    }
    if (typeof result.is_correct === "boolean") {
      return result.is_correct;
    }
    if (typeof result.isCorrect === "boolean") {
      return result.isCorrect;
    }
    return null;
  }

  function renderIntro() {
    return `
      <section class="game-direction-shell game-direction-intro">
        <div class="game-direction-hero-map" aria-hidden="true">
          <div class="game-direction-map-grid"></div>
          <div class="game-direction-scanline"></div>
          <div class="game-direction-route-preview">
            <span></span><span></span><span></span><span></span><span></span>
          </div>
        </div>
        <div class="game-direction-intro-copy">
          <p class="game-direction-kicker">Direction Maze Live</p>
          <h2>Navigate under low visibility using bearings, turns, and checkpoint logic.</h2>
          <p>Each direction MCQ drives a tactical route trace. Correct calls stabilize heading confidence; misses create drift and force tighter checkpoint recovery.</p>
        </div>
        <div class="game-direction-intro-panel">
          <div>
            <span>Mode</span>
            <strong>Night navigation</strong>
          </div>
          <div>
            <span>Primary skill</span>
            <strong>Spatial reasoning</strong>
          </div>
          <div>
            <span>Telemetry</span>
            <strong>Compass + route trace</strong>
          </div>
        </div>
      </section>
    `;
  }

  function renderHud(state) {
    const game = getGameState(state);
    const checkpointPercent = Math.round((game.checkpoint / game.totalCheckpoints) * 100);
    return `
      <section class="game-direction-hud" aria-label="Direction Maze telemetry">
        <div class="game-direction-hud-card">
          <span>Checkpoint</span>
          <strong>CP-${String(game.checkpoint).padStart(2, "0")}</strong>
          <div class="game-direction-meter"><i style="width:${checkpointPercent}%"></i></div>
        </div>
        <div class="game-direction-hud-card">
          <span>Heading confidence</span>
          <strong>${game.confidence}%</strong>
          <div class="game-direction-meter"><i style="width:${game.confidence}%"></i></div>
        </div>
        <div class="game-direction-hud-card">
          <span>Route integrity</span>
          <strong>${game.integrity}%</strong>
          <div class="game-direction-meter"><i style="width:${game.integrity}%"></i></div>
        </div>
        <div class="game-direction-hud-card">
          <span>Lateral drift</span>
          <strong>${game.drift} m</strong>
          <div class="game-direction-meter game-direction-is-warning"><i style="width:${clamp(game.drift, 0, 100)}%"></i></div>
        </div>
      </section>
    `;
  }

  function renderScene(state) {
    const game = getGameState(state);
    const current = game.route[game.route.length - 1] || { x: CENTER, y: CENTER };
    const heading = DIRECTIONS[game.heading] || DIRECTIONS.north;
    const routeCells = new Map(game.route.map((point, index) => [`${point.x}:${point.y}`, { ...point, index }]));
    return `
      <section class="game-direction-shell game-direction-scene" aria-label="Live direction maze">
        <div class="game-direction-map">
          <div class="game-direction-map-grid"></div>
          <div class="game-direction-coordinate-strip game-direction-coordinate-top">NIGHT GRID / SECTOR ${String(game.checkpoint).padStart(2, "0")}</div>
          <div class="game-direction-coordinate-strip game-direction-coordinate-bottom">X${current.x + 1} Y${current.y + 1} / DRIFT ${game.drift}M</div>
          <div class="game-direction-cells">
            ${game.cells.map((cell) => renderCell(cell, routeCells.get(`${cell.x}:${cell.y}`))).join("")}
          </div>
        </div>
        <aside class="game-direction-instruments">
          ${renderCompass(game, heading)}
          <div class="game-direction-signal-stack">
            ${game.signals.map((signal) => `
              <div class="game-direction-signal">
                <span>${escapeHtml(signal.label)}</span>
                <strong>${signal.value}%</strong>
                <div class="game-direction-meter"><i style="width:${clamp(signal.value, 0, 100)}%"></i></div>
              </div>
            `).join("")}
          </div>
          <div class="game-direction-status ${game.lastResult === false ? "game-direction-is-alert" : game.lastResult === true ? "game-direction-is-clear" : ""}">
            <span>${game.lastResult === false ? "Correction required" : game.lastResult === true ? "Checkpoint stable" : "Awaiting bearing"}</span>
            <strong>${escapeHtml(heading.label)} / ${heading.deg} deg</strong>
          </div>
        </aside>
      </section>
    `;
  }

  function renderCell(cell, routePoint) {
    const classes = [
      "game-direction-cell",
      cell.type ? `game-direction-is-${cell.type}` : "",
      routePoint ? "game-direction-is-route" : "",
      routePoint?.type === "start" ? "game-direction-is-start" : "",
      routePoint?.type === "current" ? "game-direction-is-current" : "",
    ].filter(Boolean).join(" ");
    const marker = routePoint
      ? `<span class="game-direction-route-node">${routePoint.type === "current" ? "LOC" : routePoint.index + 1}</span>`
      : "";
    return `<div class="${classes}" data-x="${cell.x}" data-y="${cell.y}">${marker}</div>`;
  }

  function renderCompass(game, heading) {
    return `
      <div class="game-direction-compass" aria-label="Compass heading ${escapeHtml(heading.label)}">
        <div class="game-direction-compass-ring">
          <span class="game-direction-compass-cardinal game-direction-is-north">N</span>
          <span class="game-direction-compass-cardinal game-direction-is-east">E</span>
          <span class="game-direction-compass-cardinal game-direction-is-south">S</span>
          <span class="game-direction-compass-cardinal game-direction-is-west">W</span>
          <i class="game-direction-needle" style="transform: translate(-50%, -100%) rotate(${heading.deg}deg)"></i>
          <b></b>
        </div>
        <div class="game-direction-compass-readout">
          <span>Current heading</span>
          <strong>${escapeHtml(heading.label)} ${heading.deg}</strong>
        </div>
      </div>
    `;
  }

  function onQuestion(question, state) {
    const game = getGameState(state);
    const questionHash = hashText(getQuestionText(question));
    if (game.lastQuestionHash === questionHash) {
      return;
    }
    game.active = true;
    game.step += 1;
    game.lastQuestionHash = questionHash;
    const moves = deriveRouteMoves(question, game);
    moves.forEach((move) => {
      game.heading = move.heading;
      advanceRoute(game, move.heading, move.moveCount);
    });
    updateSignals(game, question);
    if (game.step > 1 && game.step % 3 === 1) {
      game.checkpoint = clamp(game.checkpoint + 1, 1, game.totalCheckpoints);
    }
  }

  function onAnswer(result, state) {
    const game = getGameState(state);
    const isCorrect = readCorrectness(result);
    if (isCorrect === null) {
      return;
    }
    game.lastResult = isCorrect;
    if (isCorrect) {
      game.streak += 1;
      game.confidence = clamp(game.confidence + 7 + Math.min(game.streak, 5), 0, 100);
      game.integrity = clamp(game.integrity + 4, 0, 100);
      game.drift = clamp(game.drift - 9, 0, 100);
      if (game.streak > 0 && game.streak % 4 === 0) {
        game.checkpoint = clamp(game.checkpoint + 1, 1, game.totalCheckpoints);
      }
    } else {
      game.streak = 0;
      game.confidence = clamp(game.confidence - 14, 0, 100);
      game.integrity = clamp(game.integrity - 11, 0, 100);
      game.drift = clamp(game.drift + 17, 0, 100);
    }
  }

  function onStop(state) {
    const game = getGameState(state);
    game.active = false;
  }

  function getSummaryLines(summary, state) {
    const game = getGameState(state);
    const accuracy = Number(summary?.accuracy ?? summary?.accuracy_percent ?? 0);
    const solved = Number(summary?.total ?? summary?.answered ?? game.step ?? 0);
    return [
      `Final checkpoint: CP-${String(game.checkpoint).padStart(2, "0")} of ${game.totalCheckpoints}`,
      `Heading confidence closed at ${game.confidence}% with ${game.drift} m drift.`,
      `Route integrity ${game.integrity}% across ${solved || game.step} navigation calls${accuracy ? ` at ${Math.round(accuracy)}% accuracy` : ""}.`,
    ];
  }

  ensureStylesheet();

  window.AptitudeGameModes.directionMaze = {
    id: "direction-maze-live",
    title: "Direction Maze Live",
    shortTitle: "Direction Maze",
    subtitle: "Night navigation map with compass telemetry and checkpoint recovery.",
    category: "Logical Reasoning",
    recommendedPatternNames: [
      "Directions",
      "Direction Sense",
      "Direction Sense Test",
      "Routes and Directions",
      "Navigation",
    ],
    targetCount: 12,
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
