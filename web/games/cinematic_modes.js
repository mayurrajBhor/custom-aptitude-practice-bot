(function () {
  "use strict";

  window.AptitudeGameModes = window.AptitudeGameModes || {};

  const MODES = {
    aptitudeHeist: {
      id: "aptitudeHeist",
      title: "Aptitude Heist",
      shortTitle: "Heist",
      subtitle: "Break into a high-security vault by clearing mixed aptitude lock layers under trace pressure.",
      category: "Mixed Aptitude",
      accent: "#58d6ff",
      targetCount: 18,
      adaptivePatternLimit: 18,
      adaptiveBroadMatch: true,
      difficultyRange: [1, 4],
      maxPatternsPerTopic: 5,
      recommendedPatternNames: ["Percentage", "Ratio", "Average", "Direction", "Vedic Math", "Number Sense"],
      adaptivePatternTerms: ["percentage", "ratio", "average", "direction", "speed", "series", "number", "calculation", "logic"],
      scene: "vault",
      kicker: "Private vault breach",
      introTitle: "Decode the building before the alarm stack reaches red.",
      introCopy: "Every answer disables one security layer. Weak areas and recent mistakes get extra weight so the route adapts to your actual practice gaps.",
      objective: "Security layer",
      scoreLabel: "Vault cash",
      riskLabel: "Trace",
      streakLabel: "Clean hacks",
      successVerb: "Layer opened",
      failVerb: "Alarm spike",
      unit: "cr",
      flagship: true,
      gameOverRisk: 100,
      levels: [
        { name: "Street Entry", target: 3, threat: "CCTV sweep", cash: 1 },
        { name: "Lobby Ghost", target: 6, threat: "Motion grid", cash: 1.25 },
        { name: "Server Spine", target: 10, threat: "Thermal trace", cash: 1.55 },
        { name: "Vault Core", target: 14, threat: "Laser lock", cash: 1.9 },
        { name: "Extraction", target: 18, threat: "Response team", cash: 2.35 },
      ],
    },
    marketTrader: {
      id: "marketTrader",
      title: "Market Trader",
      shortTitle: "Trader",
      subtitle: "Trade volatile positions using percentages, averages, profit-loss, ratios, and fast estimates.",
      category: "Quant Strategy",
      accent: "#5ff0a5",
      targetCount: 12,
      adaptivePatternLimit: 16,
      difficultyRange: [1, 4],
      maxPatternsPerTopic: 5,
      recommendedPatternNames: ["Percentage", "Profit and Loss", "Averages", "Ratio", "Approximation"],
      adaptivePatternTerms: ["percentage", "profit", "loss", "average", "ratio", "change", "growth", "discount", "approximation"],
      scene: "market",
      kicker: "Live trading desk",
      introTitle: "Protect the book while the market moves against you.",
      introCopy: "Correct answers become profitable fills. Wrong calls raise exposure and force the desk into defensive mode.",
      objective: "Trade signal",
      scoreLabel: "P&L",
      riskLabel: "Risk",
      streakLabel: "Winning fills",
      successVerb: "Trade filled",
      failVerb: "Slippage hit",
      unit: "k",
    },
    trainControl: {
      id: "trainControl",
      title: "Train Control Room",
      shortTitle: "Trains",
      subtitle: "Route high-speed trains using speed, distance, time, direction, and scheduling pressure.",
      category: "Logic + Quant",
      accent: "#ffcf5c",
      targetCount: 12,
      adaptivePatternLimit: 16,
      difficultyRange: [1, 4],
      maxPatternsPerTopic: 6,
      recommendedPatternNames: ["Speed", "Distance", "Time", "Direction", "Average", "Movement"],
      adaptivePatternTerms: ["speed", "distance", "time", "direction", "movement", "turn", "average", "relative", "schedule"],
      adaptiveTopicTerms: ["direction", "vedic math"],
      scene: "rail",
      kicker: "Metro command center",
      introTitle: "Keep the network moving without a signal conflict.",
      introCopy: "Every answer clears a route segment. Slow or wrong decisions increase delay load across the control map.",
      objective: "Route segment",
      scoreLabel: "On-time",
      riskLabel: "Delay",
      streakLabel: "Green signals",
      successVerb: "Signal cleared",
      failVerb: "Delay added",
      unit: "%",
    },
    escapeGrid: {
      id: "escapeGrid",
      title: "Escape Grid",
      shortTitle: "Escape",
      subtitle: "Unlock a serious escape-room grid with reasoning, series, directions, and mixed quant clues.",
      category: "Reasoning",
      accent: "#b78cff",
      targetCount: 12,
      adaptivePatternLimit: 16,
      adaptiveBroadMatch: true,
      difficultyRange: [1, 4],
      maxPatternsPerTopic: 5,
      recommendedPatternNames: ["Direction", "Coded", "Series", "Arrangement", "Percentage", "Number Sense"],
      adaptivePatternTerms: ["direction", "coded", "seating", "arrangement", "logic", "series", "percentage", "number", "instruction"],
      scene: "escape",
      kicker: "Locked facility",
      introTitle: "Solve the grid before the room seals itself.",
      introCopy: "Reasoning patterns open doors, quant patterns power panels, and weak areas are pulled into the next lock sequence.",
      objective: "Door lock",
      scoreLabel: "Keys",
      riskLabel: "Seal",
      streakLabel: "Clean unlocks",
      successVerb: "Door opened",
      failVerb: "Lock reset",
      unit: "",
    },
    auctionBattle: {
      id: "auctionBattle",
      title: "Auction Battle",
      shortTitle: "Auction",
      subtitle: "Outbid rival buyers using discounts, marked price, profit-loss, ratios, and fast valuation.",
      category: "Commercial Quant",
      accent: "#ff8f5f",
      targetCount: 12,
      adaptivePatternLimit: 14,
      difficultyRange: [1, 4],
      maxPatternsPerTopic: 5,
      recommendedPatternNames: ["Discount", "Marked Price", "Profit and Loss", "Ratio", "Average", "Percentage"],
      adaptivePatternTerms: ["discount", "marked price", "selling price", "profit", "loss", "percentage", "ratio", "average", "successive"],
      scene: "auction",
      kicker: "Private auction floor",
      introTitle: "Win the lot without overpaying the room.",
      introCopy: "Each correct answer is a disciplined bid. Misses burn reputation and let competitors raise the hammer price.",
      objective: "Bid decision",
      scoreLabel: "Won value",
      riskLabel: "Overpay",
      streakLabel: "Smart bids",
      successVerb: "Lot won",
      failVerb: "Bid pressure",
      unit: "k",
    },
  };

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

  function questionText(question) {
    return String(question?.question_text || question?.question || question?.text || question?.prompt || "");
  }

  function hashText(text) {
    let hash = 2166136261;
    const source = String(text || "");
    for (let index = 0; index < source.length; index += 1) {
      hash ^= source.charCodeAt(index);
      hash = Math.imul(hash, 16777619) >>> 0;
    }
    return hash;
  }

  function isCorrectResult(result) {
    return Boolean(result?.isCorrect ?? result?.correct ?? result?.is_correct ?? result?.success);
  }

  function elapsedSeconds(result) {
    return Math.max(1, Math.round(Number(result?.elapsed_seconds || result?.time_taken || 0) || 1));
  }

  function heistLevelForIndex(config, index) {
    const levels = config.levels || [];
    return levels.find((level) => index <= level.target) || levels[levels.length - 1] || {
      name: "Vault Core",
      target: index,
      threat: "Trace",
      cash: 1,
    };
  }

  function heistPhaseForRun(config, run) {
    if (run.extracted) {
      return "extracted";
    }
    if (run.failed) {
      return "compromised";
    }
    const total = Math.max(1, Number(config.targetCount || 18));
    const progress = run.total / total;
    if (progress >= 0.78) {
      return "extract";
    }
    if (progress >= 0.54) {
      return "vault";
    }
    if (progress >= 0.28) {
      return "inside";
    }
    return "breach";
  }

  function heistComboLabel(streak) {
    if (streak >= 8) {
      return "Ghost chain";
    }
    if (streak >= 5) {
      return "Silent run";
    }
    if (streak >= 3) {
      return "Clean stack";
    }
    return "No combo";
  }

  function getHeistAudio() {
    const AudioContext = window.AudioContext || window.webkitAudioContext;
    if (!AudioContext) {
      return null;
    }
    window.AptitudeHeistAudio = window.AptitudeHeistAudio || {};
    const audio = window.AptitudeHeistAudio;
    if (!audio.context) {
      audio.context = new AudioContext();
      audio.master = audio.context.createGain();
      audio.master.gain.value = 0.08;
      audio.master.connect(audio.context.destination);
    }
    return audio;
  }

  function tone(audio, frequency, duration, type = "sine", gain = 0.08, delay = 0) {
    if (!audio?.context || !audio.master) {
      return;
    }
    const now = audio.context.currentTime + delay;
    const oscillator = audio.context.createOscillator();
    const envelope = audio.context.createGain();
    oscillator.type = type;
    oscillator.frequency.setValueAtTime(frequency, now);
    envelope.gain.setValueAtTime(0.0001, now);
    envelope.gain.exponentialRampToValueAtTime(gain, now + 0.018);
    envelope.gain.exponentialRampToValueAtTime(0.0001, now + duration);
    oscillator.connect(envelope);
    envelope.connect(audio.master);
    oscillator.start(now);
    oscillator.stop(now + duration + 0.03);
  }

  function heistSound(event) {
    const audio = getHeistAudio();
    if (!audio) {
      return;
    }
    const resume = audio.context.resume?.();
    if (resume?.catch) {
      resume.catch(() => {});
    }
    if (event === "launch") {
      tone(audio, 92, 0.16, "sawtooth", 0.04, 0);
      tone(audio, 138, 0.2, "triangle", 0.045, 0.08);
      tone(audio, 220, 0.18, "sine", 0.035, 0.2);
    } else if (event === "question") {
      tone(audio, 440, 0.05, "square", 0.025, 0);
      tone(audio, 660, 0.05, "square", 0.018, 0.06);
    } else if (event === "success") {
      tone(audio, 523.25, 0.07, "triangle", 0.055, 0);
      tone(audio, 783.99, 0.09, "triangle", 0.05, 0.08);
      tone(audio, 1046.5, 0.11, "sine", 0.045, 0.16);
    } else if (event === "fail") {
      tone(audio, 196, 0.16, "sawtooth", 0.07, 0);
      tone(audio, 123.47, 0.22, "square", 0.05, 0.1);
    } else if (event === "level") {
      tone(audio, 330, 0.08, "triangle", 0.05, 0);
      tone(audio, 495, 0.08, "triangle", 0.046, 0.08);
      tone(audio, 742, 0.14, "triangle", 0.04, 0.16);
    } else if (event === "gameover") {
      tone(audio, 176, 0.18, "sawtooth", 0.065, 0);
      tone(audio, 148, 0.24, "sawtooth", 0.055, 0.18);
      tone(audio, 98, 0.34, "square", 0.045, 0.42);
    }
  }

  function getRun(state, config) {
    state[config.id] = state[config.id] || {};
    const run = state[config.id];
    run.startedAt = run.startedAt || Date.now();
    run.score = Number.isFinite(run.score) ? run.score : 0;
    run.risk = Number.isFinite(run.risk) ? run.risk : 34;
    run.streak = Number.isFinite(run.streak) ? run.streak : 0;
    run.bestStreak = Number.isFinite(run.bestStreak) ? run.bestStreak : 0;
    run.correct = Number.isFinite(run.correct) ? run.correct : 0;
    run.total = Number.isFinite(run.total) ? run.total : 0;
    run.fast = Number.isFinite(run.fast) ? run.fast : 0;
    run.comboMultiplier = Number.isFinite(run.comboMultiplier) ? run.comboMultiplier : 1;
    run.heat = Number.isFinite(run.heat) ? run.heat : run.risk;
    run.integrity = Number.isFinite(run.integrity) ? run.integrity : 100;
    run.lastEvent = run.lastEvent || "Crew standing by";
    run.levelIndex = Number.isFinite(run.levelIndex) ? run.levelIndex : 0;
    run.phase = run.phase || "breach";
    run.failed = Boolean(run.failed);
    run.extracted = Boolean(run.extracted);
    run.current = run.current || missionFromQuestion(null, config, 1);
    run.timeline = Array.isArray(run.timeline) ? run.timeline : [];
    return run;
  }

  function sessionIndex(state) {
    return Number(state?.session?.currentIndex || state?.session?.answeredCount || state?.answeredCount || 0) + 1;
  }

  function missionFromQuestion(question, config, index) {
    const seed = hashText(questionText(question) + config.id + index);
    const levels = ["North wing", "Core room", "Control deck", "Lower bay", "Glass floor", "Service tunnel"];
    const pressure = 28 + (seed % 58);
    const value = 3 + (seed % 17);
    return {
      id: config.id + "-" + index + "-" + seed,
      label: config.objective + " " + String(index).padStart(2, "0"),
      zone: levels[seed % levels.length],
      pressure,
      value,
      route: ["A" + ((seed % 7) + 1), "B" + (((seed >> 3) % 7) + 1), "C" + (((seed >> 6) % 7) + 1)],
    };
  }

  function formatScore(config, value) {
    const rounded = Math.round(value);
    return config.unit ? rounded + config.unit : String(rounded);
  }

  function renderIntro(config) {
    if (config.id === "aptitudeHeist") {
      return renderHeistIntro(config);
    }
    return `
      <section class="game-cinema game-cinema-intro game-cinema-${escapeHtml(config.scene)}" style="--game-cinema-accent:${escapeHtml(config.accent)}">
        <div class="game-cinema-bg" aria-hidden="true">
          <span></span><span></span><span></span><span></span>
        </div>
        <div class="game-cinema-copy">
          <p>${escapeHtml(config.kicker)}</p>
          <h2>${escapeHtml(config.introTitle)}</h2>
          <span>${escapeHtml(config.introCopy)}</span>
        </div>
        <div class="game-cinema-brief" aria-hidden="true">
          <div class="game-cinema-scan"></div>
          <strong>${escapeHtml(config.shortTitle)}</strong>
          <span>Adaptive pattern engine</span>
        </div>
      </section>
    `;
  }

  function renderHeistIntro(config) {
    const levels = (config.levels || []).map((level, index) => `
      <span><i>${String(index + 1).padStart(2, "0")}</i>${escapeHtml(level.name)}</span>
    `).join("");
    return `
      <section class="game-heist-intro" style="--game-cinema-accent:${escapeHtml(config.accent)}">
        <div class="game-heist-intro-city" aria-hidden="true">
          <span></span><span></span><span></span><span></span><span></span>
        </div>
        <div class="game-heist-intro-copy">
          <p>Flagship operation</p>
          <h2>Midnight Vault</h2>
          <span>Answer fast to keep the crew invisible. Wrong calls raise heat, damage vault integrity, and can end the run before extraction.</span>
          <div class="game-heist-intro-levels">${levels}</div>
        </div>
        <div class="game-heist-briefcase" aria-hidden="true">
          <span></span><span></span><span></span>
          <strong>₹</strong>
        </div>
      </section>
    `;
  }

  function renderHud(state, config) {
    const run = getRun(state, config);
    if (config.id === "aptitudeHeist") {
      return renderHeistHud(state, config, run);
    }
    const accuracy = run.total ? Math.round((run.correct / run.total) * 100) : 0;
    return `
      <section class="game-cinema-hud" style="--game-cinema-accent:${escapeHtml(config.accent)}">
        <div><span>${escapeHtml(config.scoreLabel)}</span><strong>${formatScore(config, run.score)}</strong></div>
        <div><span>${escapeHtml(config.riskLabel)}</span><strong>${Math.round(run.risk)}%</strong></div>
        <div><span>${escapeHtml(config.streakLabel)}</span><strong>${run.streak}</strong></div>
        <div><span>Accuracy</span><strong>${accuracy}%</strong></div>
      </section>
    `;
  }

  function renderHeistHud(state, config, run) {
    const accuracy = run.total ? Math.round((run.correct / run.total) * 100) : 0;
    const level = heistLevelForIndex(config, run.total + 1);
    const phase = heistPhaseForRun(config, run);
    return `
      <section class="game-heist-side-hud" style="--game-cinema-accent:${escapeHtml(config.accent)}">
        <div class="game-heist-side-card is-primary">
          <span>Take</span>
          <strong>${formatScore(config, run.score)}</strong>
          <small>${escapeHtml(heistComboLabel(run.streak))} x${run.comboMultiplier.toFixed(1)}</small>
        </div>
        <div class="game-heist-side-grid">
          <div><span>Heat</span><strong>${Math.round(run.risk)}%</strong></div>
          <div><span>Integrity</span><strong>${Math.round(run.integrity)}%</strong></div>
          <div><span>Accuracy</span><strong>${accuracy}%</strong></div>
          <div><span>Best</span><strong>${run.bestStreak}</strong></div>
        </div>
        <div class="game-heist-side-objective">
          <span>${escapeHtml(level.threat)}</span>
          <strong>${escapeHtml(level.name)}</strong>
          <p>${escapeHtml(phase.toUpperCase())} / Layer ${run.total + 1}</p>
        </div>
      </section>
    `;
  }

  function renderScene(state, config) {
    if (config.id === "aptitudeHeist") {
      return renderHeistScene(state, config);
    }

    const run = getRun(state, config);
    const current = run.current;
    const safe = clamp(100 - run.risk, 0, 100);
    const pressure = clamp(current.pressure, 0, 100);
    const route = current.route.map((item) => `<span>${escapeHtml(item)}</span>`).join("");

    return `
      <section class="game-cinema game-cinema-scene game-cinema-${escapeHtml(config.scene)}" style="--game-cinema-accent:${escapeHtml(config.accent)}; --game-cinema-safe:${safe}%; --game-cinema-pressure:${pressure}%">
        <div class="game-cinema-bg" aria-hidden="true">
          <span></span><span></span><span></span><span></span>
        </div>
        <div class="game-cinema-main">
          <div class="game-cinema-object">
            <span></span><span></span><span></span>
          </div>
          <div class="game-cinema-mission">
            <p>${escapeHtml(current.zone)}</p>
            <h2>${escapeHtml(current.label)}</h2>
            <div class="game-cinema-route">${route}</div>
          </div>
        </div>
        <aside class="game-cinema-console">
          <div>
            <span>Signal safety</span>
            <strong>${safe}%</strong>
            <div class="game-cinema-track"><i style="width:${safe}%"></i></div>
          </div>
          <div>
            <span>Pressure</span>
            <strong>${pressure}%</strong>
            <div class="game-cinema-track"><i style="width:${pressure}%"></i></div>
          </div>
          <div class="game-cinema-log">
            ${(run.timeline.length ? run.timeline : [{ text: "Awaiting first decision", good: true }]).slice(0, 3).map((item) => `
              <span class="${item.good ? "is-good" : "is-bad"}">${escapeHtml(item.text)}</span>
            `).join("")}
          </div>
        </aside>
      </section>
    `;
  }

  function renderHeistScene(state, config) {
    const run = getRun(state, config);
    const current = run.current;
    const safe = clamp(100 - run.risk, 0, 100);
    const pressure = clamp(current.pressure, 0, 100);
    const question = questionText(state.activeQuestion) || "Waiting for vault intelligence...";
    const level = heistLevelForIndex(config, run.total + 1);
    const phase = heistPhaseForRun(config, run);
    const levelProgress = clamp(((run.total + 1) / Math.max(1, level.target)) * 100, 0, 100);
    const combo = heistComboLabel(run.streak);
    const route = current.route.map((item) => `<span>${escapeHtml(item)}</span>`).join("");

    return `
      <section class="game-heist is-${escapeHtml(phase)} ${run.failed ? "is-compromised" : ""} ${run.lastAnswerCorrect === false ? "is-hit" : ""} ${run.lastAnswerCorrect === true ? "is-clean" : ""}" style="--game-cinema-accent:${escapeHtml(config.accent)}; --game-cinema-safe:${safe}%; --game-cinema-pressure:${pressure}%; --heist-integrity:${clamp(run.integrity, 0, 100)}%; --heist-level:${levelProgress}%">
        <div class="game-heist-sky" aria-hidden="true">
          <span></span><span></span><span></span><span></span><span></span>
        </div>
        <div class="game-heist-alert" aria-hidden="true"></div>
        <div class="game-heist-corridor" aria-hidden="true">
          <div class="game-heist-ceiling"></div>
          <div class="game-heist-floor"></div>
          <div class="game-heist-wall game-heist-wall-left"></div>
          <div class="game-heist-wall game-heist-wall-right"></div>
          <div class="game-heist-vault">
            <span></span><span></span><span></span><span></span>
          </div>
          <div class="game-heist-laser game-heist-laser-one"></div>
          <div class="game-heist-laser game-heist-laser-two"></div>
          <div class="game-heist-laser game-heist-laser-three"></div>
          <div class="game-heist-camera"></div>
          <div class="game-heist-drone"></div>
        </div>
        <div class="game-heist-hud">
          <div><span>Vault cash</span><strong>${formatScore(config, run.score)}</strong></div>
          <div><span>Trace</span><strong>${Math.round(run.risk)}%</strong></div>
          <div><span>Integrity</span><strong>${Math.round(run.integrity)}%</strong></div>
        </div>
        <div class="game-heist-console">
          <div class="game-heist-console-head">
            <span>${escapeHtml(level.name)} / ${escapeHtml(level.threat)}</span>
            <strong>${escapeHtml(current.label)}</strong>
          </div>
          <h2>${escapeHtml(question)}</h2>
          <div class="game-heist-route">${route}</div>
          <div class="game-heist-level-strip">
            <span>Level route</span>
            <strong>${Math.round(levelProgress)}%</strong>
            <div class="game-cinema-track"><i style="width:${levelProgress}%"></i></div>
          </div>
          <div class="game-heist-meter-row">
            <div>
              <span>Signal cover</span>
              <div class="game-cinema-track"><i style="width:${safe}%"></i></div>
            </div>
            <div>
              <span>Thermal pressure</span>
              <div class="game-cinema-track"><i style="width:${pressure}%"></i></div>
            </div>
            <div>
              <span>Vault integrity</span>
              <div class="game-cinema-track"><i style="width:${clamp(run.integrity, 0, 100)}%"></i></div>
            </div>
          </div>
          <div class="game-heist-status-row">
            <span>${escapeHtml(combo)}</span>
            <span>${escapeHtml(run.lastEvent)}</span>
          </div>
        </div>
        <div class="game-heist-feed">
          ${(run.timeline.length ? run.timeline : [{ text: "Enter the first terminal code", good: true }]).slice(0, 3).map((item) => `
            <span class="${item.good ? "is-good" : "is-bad"}">${escapeHtml(item.text)}</span>
          `).join("")}
        </div>
      </section>
    `;
  }

  function onQuestion(question, state, config) {
    const run = getRun(state, config);
    run.current = missionFromQuestion(question, config, sessionIndex(state));
    if (config.id === "aptitudeHeist") {
      const nextLevelIndex = Math.max(0, (config.levels || []).findIndex((level) => run.total + 1 <= level.target));
      if (nextLevelIndex !== -1 && nextLevelIndex !== run.levelIndex) {
        run.levelIndex = nextLevelIndex;
        run.lastEvent = "New level: " + heistLevelForIndex(config, run.total + 1).name;
        run.timeline.unshift({ good: true, text: run.lastEvent });
        heistSound("level");
      } else {
        heistSound("question");
      }
      run.phase = heistPhaseForRun(config, run);
      run.timeline = run.timeline.slice(0, 5);
    }
    return state;
  }

  function onAnswer(result, state, config) {
    const run = getRun(state, config);
    const correct = isCorrectResult(result);
    const fast = elapsedSeconds(result) <= 8;
    const seconds = elapsedSeconds(result);
    run.total += 1;

    if (correct) {
      run.correct += 1;
      run.streak += 1;
      run.bestStreak = Math.max(run.bestStreak, run.streak);
      run.fast += fast ? 1 : 0;
      run.comboMultiplier = config.id === "aptitudeHeist" ? 1 + Math.min(run.streak, 8) * 0.18 : run.comboMultiplier;
      const level = heistLevelForIndex(config, run.total);
      const baseGain = run.current.value + run.streak + (fast ? 3 : 0);
      const heistGain = config.id === "aptitudeHeist" ? Math.round(baseGain * run.comboMultiplier * (level.cash || 1)) : baseGain;
      run.score += heistGain;
      run.risk = clamp(run.risk - (fast ? 9 : 5), 0, 100);
      if (config.id === "aptitudeHeist") {
        run.integrity = clamp(run.integrity + (fast ? 2 : 1), 0, 100);
        run.lastEvent = `${config.successVerb}: +${heistGain}${config.unit}`;
        run.lastAnswerCorrect = true;
        heistSound("success");
      }
      run.timeline.unshift({ good: true, text: config.id === "aptitudeHeist" ? run.lastEvent : config.successVerb + " +" + run.current.value });
    } else {
      run.streak = 0;
      run.comboMultiplier = 1;
      run.score = Math.max(0, run.score - 2);
      run.risk = clamp(run.risk + (config.id === "aptitudeHeist" ? 16 : 12), 0, 100);
      if (config.id === "aptitudeHeist") {
        const damage = clamp(8 + Math.round(seconds / 5), 8, 18);
        run.integrity = clamp(run.integrity - damage, 0, 100);
        run.lastEvent = `${config.failVerb}: integrity -${damage}%`;
        run.lastAnswerCorrect = false;
        heistSound(run.risk >= (config.gameOverRisk || 100) || run.integrity <= 0 ? "gameover" : "fail");
      }
      run.timeline.unshift({ good: false, text: config.id === "aptitudeHeist" ? run.lastEvent : config.failVerb + " +" + Math.round(run.risk) + "%" });
    }

    if (config.id === "aptitudeHeist") {
      run.failed = run.risk >= (config.gameOverRisk || 100) || run.integrity <= 0;
      run.extracted = !run.failed && run.total >= Number(config.targetCount || 18);
      run.phase = heistPhaseForRun(config, run);
      if (run.failed) {
        run.timeline.unshift({ good: false, text: "Crew burned. Extraction aborted." });
      } else if (run.extracted) {
        run.timeline.unshift({ good: true, text: "Extraction clean. Vault route closed." });
        heistSound("level");
      }
    }
    run.timeline = run.timeline.slice(0, 5);
    return state;
  }

  function onStop(state, config) {
    const run = getRun(state, config);
    run.stoppedAt = Date.now();
    return state;
  }

  function getSummaryLines(summary, state, config) {
    const run = getRun(state, config);
    const accuracy = run.total ? Math.round((run.correct / run.total) * 100) : Math.round(Number(summary?.accuracy || 0));
    if (config.id === "aptitudeHeist") {
      return [
        "Operation: " + (run.failed ? "Compromised" : run.extracted ? "Extracted" : "Stopped"),
        "Vault cash: " + formatScore(config, run.score),
        "Heat: " + Math.round(run.risk) + "%; integrity: " + Math.round(run.integrity) + "%",
        "Best combo: " + run.bestStreak + "; fast hacks: " + run.fast,
        "Accuracy: " + accuracy + "%",
      ];
    }
    return [
      config.scoreLabel + ": " + formatScore(config, run.score),
      config.riskLabel + " closed at: " + Math.round(run.risk) + "%",
      "Correct decisions: " + run.correct + "/" + Math.max(run.total, Number(summary?.answered || 0)),
      "Best streak: " + run.bestStreak + "; fast decisions: " + run.fast,
      "Game accuracy: " + accuracy + "%",
    ];
  }

  function register(config) {
    window.AptitudeGameModes[config.id] = {
      id: config.id,
      title: config.title,
      shortTitle: config.shortTitle,
      subtitle: config.subtitle,
      category: config.category,
      recommendedPatternNames: config.recommendedPatternNames,
      adaptivePatternTerms: config.adaptivePatternTerms,
      adaptiveTopicTerms: config.adaptiveTopicTerms,
      adaptiveBroadMatch: config.adaptiveBroadMatch,
      adaptivePatternLimit: config.adaptivePatternLimit,
      adaptiveUseWeakAreas: true,
      difficultyRange: config.difficultyRange,
      maxPatternsPerTopic: config.maxPatternsPerTopic,
      targetCount: config.targetCount,
      accent: config.accent,
      flagship: Boolean(config.flagship),
      onLaunch: (state) => {
        if (config.id === "aptitudeHeist") {
          heistSound("launch");
          const run = getRun(state, config);
          run.lastEvent = "Crew online. Sound engine armed.";
        }
        return state;
      },
      renderIntro: () => renderIntro(config),
      renderHud: (state) => renderHud(state, config),
      renderScene: (state) => renderScene(state, config),
      onQuestion: (question, state) => onQuestion(question, state, config),
      onAnswer: (result, state) => onAnswer(result, state, config),
      onStop: (state) => onStop(state, config),
      isComplete: (state) => {
        if (config.id !== "aptitudeHeist") {
          return false;
        }
        const run = getRun(state, config);
        return Boolean(run.failed || run.extracted);
      },
      getSummaryLines: (summary, state) => getSummaryLines(summary, state, config),
    };
  }

  Object.values(MODES).forEach(register);
})();
