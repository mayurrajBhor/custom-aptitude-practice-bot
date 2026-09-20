/**
 * AptitudeEnglishDB - Persistent On-Device Storage & Analytics for the English Section
 * Database Name: AptitudeEnglishDB
 * Fully isolated from Quantitative AptitudeLocalDB to ensure zero data collisions or schema overwrites.
 * Provides offline persistence, session state continuation, spaced repetition vocabulary,
 * and high-resolution English analytics (CR vs RC isolated pacing, trajectories, and study plans).
 */

const DB_NAME = "AptitudeEnglishDB";
const DB_VERSION = 1;

const STORES = {
  ATTEMPTS: "english_attempts",
  SESSIONS: "english_sessions",
  ACTIVE_SESSION: "english_active_session",
  VOCAB_SRS: "english_vocab_srs",
};

const ACTIVE_SESSION_KEY = "current_active_session";

let dbInstance = null;
let dbPromise = null;

// Standard SRS Intervals ladder in days
const SRS_INTERVALS = [1, 3, 7, 14, 30, 60];

// Question type guidance map for actionable study plan prescriptions
const QUESTION_TYPE_PRESCRIPTIONS = {
  Strengthen: {
    tip: "Identify the conclusion and premises; find an option that validates an unstated assumption or introduces new facts that make the conclusion more plausible.",
    drill: "Strengthen Drills: Practice identifying unstated assumptions before looking at options."
  },
  Weaken: {
    tip: "Locate the logical leap between premise and conclusion; pick the option that provides an alternative explanation or exposes an unconsidered vulnerability.",
    drill: "Weaken Drills: Search for unaddressed variables and alternative causes."
  },
  Assumption: {
    tip: "Apply the Negation Test: If the negated option causes the argument's conclusion to fall apart, that option is the necessary assumption.",
    drill: "Assumption Drills: Practice the Negation Test on all close 50/50 options."
  },
  Inference: {
    tip: "Stick strictly to the stimulus facts without making outside leaps. The correct inference must be 100% true based solely on the text.",
    drill: "Inference Drills: Avoid extreme qualifiers (always, never, only) unless backed by the text."
  },
  Evaluate: {
    tip: "Use the Variance Test: Answer the question with extreme yes/no answers; if one strengthens and the other weakens, it is the correct evaluate choice.",
    drill: "Evaluate Drills: Test extreme outcomes on the conclusion."
  },
  "Bold Face": {
    tip: "Analyze argument architecture: Determine whether each bolded segment is a premise, conclusion, intermediate conclusion, or counter-premise.",
    drill: "Bold Face Drills: Map argument roles without reading answer choices first."
  },
  Flaw: {
    tip: "Spot common reasoning fallacies: confusing correlation with causation, false dilemmas, ad hominem, or shifting definitions.",
    drill: "Flaw Drills: Categorize typical GMAT reasoning flaws."
  },
  "Main Idea": {
    tip: "Synthesize the primary purpose across all paragraphs. Avoid choices that are too narrow (single paragraph) or too broad.",
    drill: "Main Idea Drills: Write a one-sentence summary after finishing the initial passage read."
  },
  Detail: {
    tip: "Return to the specific passage paragraph and verify exact wording. Beware of distortion and opposite traps.",
    drill: "Detail Drills: Cite line/paragraph evidence before confirming your answer."
  },
  "Passage Function": {
    tip: "Ask 'Why did the author include this paragraph/sentence?' rather than just 'What does it say?'.",
    drill: "Function Drills: Connect each paragraph's role back to the passage's primary purpose."
  },
  "Author Tone": {
    tip: "Look for nuance words (e.g., guarded optimism, critical appraisal, neutral reporting). GMAT tones are rarely extreme.",
    drill: "Tone Drills: Circle attitude adjectives in passage topic sentences."
  }
};

// Default high-frequency GMAT vocabulary list for seeding if store is empty
const DEFAULT_GMAT_VOCAB = [
  { word: "anomalous", definition: "Deviating from what is standard, normal, or expected; irregular.", level: "advanced", synonyms: ["aberrant", "atypical", "irregular"] },
  { word: "equivocal", definition: "Open to more than one interpretation; ambiguous; uncertain.", level: "advanced", synonyms: ["ambiguous", "vague", "evasive"] },
  { word: "lucid", definition: "Expressed clearly; easy to understand; completely intelligible.", level: "foundation", synonyms: ["coherent", "articulate", "transparent"] },
  { word: "precipitate", definition: "Cause an event or situation to happen suddenly, unexpectedly, or prematurely.", level: "advanced", synonyms: ["hasten", "trigger", "instigate"] },
  { word: "assuage", definition: "Make an unpleasant feeling less intense; satisfy or appease.", level: "intermediate", synonyms: ["alleviate", "mitigate", "placate"] },
  { word: "erudite", definition: "Having or showing great knowledge or learning; scholarly.", level: "intermediate", synonyms: ["scholarly", "learned", "pedantic"] },
  { word: "opaque", definition: "Not transparent; hard or impossible to understand.", level: "foundation", synonyms: ["obscure", "cryptic", "inscrutable"] },
  { word: "prodigal", definition: "Spending money or resources freely and recklessly; wastefully extravagant.", level: "advanced", synonyms: ["profligate", "spendthrift", "improvident"] },
  { word: "enigma", definition: "A person or thing that is mysterious, puzzling, or difficult to understand.", level: "foundation", synonyms: ["mystery", "riddle", "conundrum"] },
  { word: "fervid", definition: "Intensely enthusiastic or passionate, especially to an excessive degree.", level: "advanced", synonyms: ["fervent", "impassioned", "vehement"] },
  { word: "placate", definition: "Make someone less angry or hostile; pacify.", level: "intermediate", synonyms: ["mollify", "conciliate", "appease"] },
  { word: "laconic", definition: "Using very few words; concise to the point of seeming rude or mysterious.", level: "advanced", synonyms: ["terse", "succinct", "curt"] },
  { word: "mitigate", definition: "Make less severe, serious, or painful.", level: "foundation", synonyms: ["lessen", "attenuate", "palliate"] },
  { word: "pedantic", definition: "Excessively concerned with minor details and rules or with displaying academic learning.", level: "advanced", synonyms: ["scrupulous", "meticulous", "over-exact"] },
  { word: "pragmatic", definition: "Dealing with things sensibly and realistically in a way based on practical rather than theoretical considerations.", level: "foundation", synonyms: ["practical", "expedient", "sensible"] },
  { word: "vacillate", definition: "Alternate or waver between different opinions or actions; be indecisive.", level: "advanced", synonyms: ["dither", "oscillate", "hesitate"] },
  { word: "venerate", definition: "Regard with great respect; revere.", level: "intermediate", synonyms: ["revere", "idolize", "esteem"] },
  { word: "waver", definition: "Shake with a quivering motion; be undecided between two opinions or courses of action.", level: "foundation", synonyms: ["falter", "fluctuate", "vacillate"] },
  { word: "ephemeral", definition: "Lasting for a very short time; transitory.", level: "intermediate", synonyms: ["fleeting", "transient", "evanescent"] },
  { word: "garrulous", definition: "Excessively talkative, especially on trivial matters.", level: "advanced", synonyms: ["loquacious", "voluble", "verbose"] }
];

/**
 * Open or initialize the English IndexedDB database.
 * Returns a Promise that resolves with the IDBDatabase instance.
 */
function initEnglishDB() {
  if (dbInstance) {
    return Promise.resolve(dbInstance);
  }
  if (dbPromise) {
    return dbPromise;
  }

  if (typeof indexedDB === "undefined") {
    return Promise.reject(new Error("IndexedDB is not supported in this environment"));
  }

  dbPromise = new Promise((resolve, reject) => {
    const request = indexedDB.open(DB_NAME, DB_VERSION);

    request.onupgradeneeded = (event) => {
      const db = event.target.result;

      // 1. Store: english_attempts
      if (!db.objectStoreNames.contains(STORES.ATTEMPTS)) {
        const attemptStore = db.createObjectStore(STORES.ATTEMPTS, {
          keyPath: "id",
          autoIncrement: true,
        });
        attemptStore.createIndex("date", "date", { unique: false });
        attemptStore.createIndex("timestamp", "timestamp", { unique: false });
        attemptStore.createIndex("session_id", "session_id", { unique: false });
        attemptStore.createIndex("mode", "mode", { unique: false });
        attemptStore.createIndex("verbal_type", "verbal_type", { unique: false });
        attemptStore.createIndex("foundation_type", "foundation_type", { unique: false });
        attemptStore.createIndex("question_type", "question_type", { unique: false });
        attemptStore.createIndex("topic", "topic", { unique: false });
        attemptStore.createIndex("difficulty", "difficulty", { unique: false });
        attemptStore.createIndex("is_correct", "is_correct", { unique: false });
        attemptStore.createIndex("error_category", "error_category", { unique: false });
        attemptStore.createIndex("trap_type", "trap_type", { unique: false });
      }

      // 2. Store: english_sessions
      if (!db.objectStoreNames.contains(STORES.SESSIONS)) {
        const sessionStore = db.createObjectStore(STORES.SESSIONS, {
          keyPath: "session_id",
        });
        sessionStore.createIndex("date", "date", { unique: false });
        sessionStore.createIndex("timestamp", "timestamp", { unique: false });
        sessionStore.createIndex("mode", "mode", { unique: false });
      }

      // 3. Store: english_active_session (Stores incomplete session under "current_active_session")
      if (!db.objectStoreNames.contains(STORES.ACTIVE_SESSION)) {
        db.createObjectStore(STORES.ACTIVE_SESSION, { keyPath: "id" });
      }

      // 4. Store: english_vocab_srs
      if (!db.objectStoreNames.contains(STORES.VOCAB_SRS)) {
        const vocabStore = db.createObjectStore(STORES.VOCAB_SRS, {
          keyPath: "word",
        });
        vocabStore.createIndex("next_review_date", "next_review_date", { unique: false });
        vocabStore.createIndex("retention_score", "retention_score", { unique: false });
        vocabStore.createIndex("user_rating", "user_rating", { unique: false });
      }
    };

    request.onsuccess = (event) => {
      dbInstance = event.target.result;
      resolve(dbInstance);
    };

    request.onerror = (event) => {
      dbPromise = null;
      reject(event.target.error || new Error("Failed to open AptitudeEnglishDB"));
    };
  });

  return dbPromise;
}

// ---------------------------------------------------------------------------
// Internal Utility Functions
// ---------------------------------------------------------------------------

function getTodayString() {
  return new Date().toISOString().slice(0, 10);
}

function roundDecimals(val, decimals = 1) {
  if (typeof val !== "number" || isNaN(val)) return 0;
  const factor = Math.pow(10, decimals);
  return Math.round(val * factor) / factor;
}

function calculateMedian(arr) {
  if (!Array.isArray(arr) || arr.length === 0) return 0;
  const sorted = arr.filter((n) => typeof n === "number" && !isNaN(n)).sort((a, b) => a - b);
  if (sorted.length === 0) return 0;
  const mid = Math.floor(sorted.length / 2);
  return sorted.length % 2 !== 0
    ? sorted[mid]
    : roundDecimals((sorted[mid - 1] + sorted[mid]) / 2, 1);
}

function triggerBrowserDownload(blob, filename) {
  if (typeof document === "undefined" || typeof window === "undefined" || !window.URL) {
    return;
  }
  const url = window.URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = filename;
  document.body.appendChild(anchor);
  anchor.click();
  window.setTimeout(() => {
    document.body.removeChild(anchor);
    window.URL.revokeObjectURL(url);
  }, 150);
}

// ---------------------------------------------------------------------------
// 1. Persistence APIs
// ---------------------------------------------------------------------------

/**
 * Record a single English question attempt.
 * @param {Object} attempt
 * @returns {Promise<Object>} The saved attempt record with its autoIncrement id.
 */
async function recordEnglishAttempt(attempt) {
  const db = await initEnglishDB();
  const now = new Date();
  const dateStr = attempt.date || now.toISOString().slice(0, 10);
  const timestamp = typeof attempt.timestamp === "number" ? attempt.timestamp : now.getTime();

  // Normalize attempt fields
  const record = {
    date: dateStr,
    timestamp: timestamp,
    session_id: String(attempt.session_id || ""),
    mode: attempt.mode === "foundation" ? "foundation" : "gmat_verbal",
    verbal_type: attempt.verbal_type || null, // 'critical_reasoning' | 'reading_comprehension' | null
    foundation_type: attempt.foundation_type || null, // 'grammar' | 'vocabulary' | null
    question_id: attempt.question_id !== undefined ? attempt.question_id : null,
    question_type: String(attempt.question_type || "General"),
    topic: String(attempt.topic || "General"),
    difficulty: attempt.difficulty !== undefined ? attempt.difficulty : "medium",
    trap_type: attempt.trap_type || null,
    error_category: attempt.error_category || null,
    passage_id: attempt.passage_id || null,
    user_answer: attempt.user_answer !== undefined ? attempt.user_answer : null,
    correct_answer: attempt.correct_answer !== undefined ? attempt.correct_answer : null,
    is_correct: Boolean(attempt.is_correct),
    is_timeout: Boolean(attempt.is_timeout),
    is_skipped: Boolean(attempt.is_skipped),
    time_taken: typeof attempt.time_taken === "number" ? attempt.time_taken : Number(attempt.time_taken) || 0,
    reading_time: typeof attempt.reading_time === "number" ? attempt.reading_time : Number(attempt.reading_time) || 0,
    question_solving_time:
      typeof attempt.question_solving_time === "number"
        ? attempt.question_solving_time
        : Number(attempt.question_solving_time) || 0,
    first_interaction_time:
      typeof attempt.first_interaction_time === "number"
        ? attempt.first_interaction_time
        : Number(attempt.first_interaction_time) || 0,
    elimination_time:
      typeof attempt.elimination_time === "number"
        ? attempt.elimination_time
        : Number(attempt.elimination_time) || 0,
    bookmark_state: Boolean(attempt.bookmark_state),
    review_status: attempt.review_status || null,
  };

  // Preserve extra metadata if present (options, prompt, explanation, notes)
  if (attempt.question_text) record.question_text = String(attempt.question_text);
  if (Array.isArray(attempt.options)) record.options = attempt.options;
  if (attempt.passage_text) record.passage_text = String(attempt.passage_text);
  if (attempt.explanation) record.explanation = String(attempt.explanation);
  if (attempt.notes) record.notes = String(attempt.notes);

  return new Promise((resolve, reject) => {
    const tx = db.transaction(STORES.ATTEMPTS, "readwrite");
    const store = tx.objectStore(STORES.ATTEMPTS);
    const req = store.add(record);

    req.onsuccess = () => {
      record.id = req.result;
      resolve(record);
    };

    req.onerror = (e) => reject(e.target.error);
  });
}

/**
 * Record a completed English session.
 * @param {Object} session
 * @returns {Promise<Object>} The saved session record.
 */
async function recordEnglishSession(session) {
  const db = await initEnglishDB();
  const now = new Date();
  const dateStr = session.date || now.toISOString().slice(0, 10);
  const timestamp = typeof session.timestamp === "number" ? session.timestamp : now.getTime();
  const sessionId = String(session.session_id || `eng_sess_${timestamp}`);

  const totalQ = Number(session.total_questions) || 0;
  const correctCount = Number(session.correct_count) || 0;
  const accuracy =
    session.accuracy !== undefined
      ? Number(session.accuracy)
      : totalQ > 0
      ? roundDecimals((correctCount / totalQ) * 100, 1)
      : 0;

  const record = {
    session_id: sessionId,
    date: dateStr,
    timestamp: timestamp,
    mode: session.mode === "foundation" ? "foundation" : "gmat_verbal",
    verbal_type: session.verbal_type || null,
    foundation_type: session.foundation_type || null,
    total_questions: totalQ,
    correct_count: correctCount,
    accuracy: accuracy,
    total_time_taken: Number(session.total_time_taken) || 0,
    avg_time_per_question:
      Number(session.avg_time_per_question) ||
      (totalQ > 0 ? roundDecimals(Number(session.total_time_taken) / totalQ, 1) : 0),
    cr_avg_time: session.cr_avg_time !== undefined ? Number(session.cr_avg_time) : null,
    rc_avg_time: session.rc_avg_time !== undefined ? Number(session.rc_avg_time) : null,
    questions: Array.isArray(session.questions) ? session.questions : [],
    completed_at: session.completed_at || now.toISOString(),
  };

  // Preserve any additional session properties
  Object.keys(session).forEach((key) => {
    if (record[key] === undefined) {
      record[key] = session[key];
    }
  });

  return new Promise((resolve, reject) => {
    const tx = db.transaction(STORES.SESSIONS, "readwrite");
    const store = tx.objectStore(STORES.SESSIONS);
    const req = store.put(record);

    req.onsuccess = () => resolve(record);
    req.onerror = (e) => reject(e.target.error);
  });
}

/**
 * Save active incomplete session state for the "Continue English session" feature.
 * @param {Object} sessionState
 * @returns {Promise<Object>}
 */
async function saveActiveEnglishSession(sessionState) {
  const db = await initEnglishDB();
  if (!sessionState || typeof sessionState !== "object") {
    throw new Error("Invalid sessionState provided to saveActiveEnglishSession");
  }

  const record = {
    ...sessionState,
    id: ACTIVE_SESSION_KEY,
    session_id: String(sessionState.session_id || `active_eng_${Date.now()}`),
    mode: sessionState.mode === "foundation" ? "foundation" : "gmat_verbal",
    verbal_type: sessionState.verbal_type || null,
    foundation_type: sessionState.foundation_type || null,
    questions: Array.isArray(sessionState.questions) ? sessionState.questions : [],
    current_index: Number(sessionState.current_index) || 0,
    user_answers: sessionState.user_answers || {},
    eliminated_options: sessionState.eliminated_options || {},
    bookmarks: sessionState.bookmarks || {},
    time_remaining_seconds:
      sessionState.time_remaining_seconds !== undefined
        ? Number(sessionState.time_remaining_seconds)
        : null,
    passage_scroll_positions: sessionState.passage_scroll_positions || {},
    start_time: sessionState.start_time || Date.now(),
    updated_at: Date.now(),
  };

  return new Promise((resolve, reject) => {
    const tx = db.transaction(STORES.ACTIVE_SESSION, "readwrite");
    const store = tx.objectStore(STORES.ACTIVE_SESSION);
    const req = store.put(record);

    req.onsuccess = () => resolve(record);
    req.onerror = (e) => reject(e.target.error);
  });
}

/**
 * Retrieve active incomplete session, or null if none is in progress.
 * @returns {Promise<Object|null>}
 */
async function getActiveEnglishSession() {
  const db = await initEnglishDB();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(STORES.ACTIVE_SESSION, "readonly");
    const store = tx.objectStore(STORES.ACTIVE_SESSION);
    const req = store.get(ACTIVE_SESSION_KEY);

    req.onsuccess = () => resolve(req.result || null);
    req.onerror = (e) => reject(e.target.error);
  });
}

/**
 * Clear active incomplete session when finished or cancelled.
 * @returns {Promise<boolean>}
 */
async function clearActiveEnglishSession() {
  const db = await initEnglishDB();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(STORES.ACTIVE_SESSION, "readwrite");
    const store = tx.objectStore(STORES.ACTIVE_SESSION);
    const req = store.delete(ACTIVE_SESSION_KEY);

    req.onsuccess = () => resolve(true);
    req.onerror = (e) => reject(e.target.error);
  });
}

/**
 * Get all English attempts from IndexedDB.
 * @returns {Promise<Array<Object>>}
 */
async function getAllEnglishAttempts() {
  const db = await initEnglishDB();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(STORES.ATTEMPTS, "readonly");
    const store = tx.objectStore(STORES.ATTEMPTS);
    const req = store.getAll();

    req.onsuccess = () => {
      const records = req.result || [];
      records.sort((a, b) => (b.timestamp || 0) - (a.timestamp || 0));
      resolve(records);
    };
    req.onerror = (e) => reject(e.target.error);
  });
}

/**
 * Get all English sessions from IndexedDB.
 * @returns {Promise<Array<Object>>}
 */
async function getAllEnglishSessions() {
  const db = await initEnglishDB();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(STORES.SESSIONS, "readonly");
    const store = tx.objectStore(STORES.SESSIONS);
    const req = store.getAll();

    req.onsuccess = () => {
      const records = req.result || [];
      records.sort((a, b) => (b.timestamp || 0) - (a.timestamp || 0));
      resolve(records);
    };
    req.onerror = (e) => reject(e.target.error);
  });
}

/**
 * Get attempts by session_id.
 * @param {string} sessionId
 * @returns {Promise<Array<Object>>}
 */
async function getEnglishAttemptsBySession(sessionId) {
  const db = await initEnglishDB();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(STORES.ATTEMPTS, "readonly");
    const store = tx.objectStore(STORES.ATTEMPTS);
    const index = store.index("session_id");
    const req = index.getAll(IDBKeyRange.only(String(sessionId)));

    req.onsuccess = () => {
      const res = req.result || [];
      res.sort((a, b) => (a.timestamp || 0) - (b.timestamp || 0));
      resolve(res);
    };
    req.onerror = (e) => reject(e.target.error);
  });
}

// ---------------------------------------------------------------------------
// 2. Analytics APIs
// ---------------------------------------------------------------------------

/**
 * Calculate consecutive activity streak in days.
 * @param {Array<string>} dates YYYY-MM-DD strings
 * @returns {number}
 */
function calculateStreakFromDates(dates) {
  if (!Array.isArray(dates) || dates.length === 0) return 0;
  const daySet = new Set(dates);
  let currentStreak = 0;
  let checkDate = new Date();

  while (true) {
    const ds = checkDate.toISOString().slice(0, 10);
    if (daySet.has(ds)) {
      currentStreak++;
      checkDate.setDate(checkDate.getDate() - 1);
    } else {
      if (currentStreak === 0) {
        const yesterday = new Date();
        yesterday.setDate(yesterday.getDate() - 1);
        const yds = yesterday.toISOString().slice(0, 10);
        if (daySet.has(yds)) {
          currentStreak++;
          checkDate = yesterday;
          checkDate.setDate(checkDate.getDate() - 1);
          continue;
        }
      }
      break;
    }
  }

  return currentStreak;
}

/**
 * Get high-level English overview metrics.
 * - Total English questions attempted
 * - Overall English accuracy
 * - Average English solving time (NOTE: clearly scopes separate CR avg time and RC avg time)
 * - Current English streak (consecutive active days with English attempts)
 * - Weak English topics count (<60% accuracy with at least 2 attempts)
 * - Last practice date
 * - Estimated Verbal readiness score (0-100 index based on CR accuracy, RC accuracy, pace, coverage)
 * @returns {Promise<Object>}
 */
async function getEnglishOverview() {
  const attempts = await getAllEnglishAttempts();

  if (attempts.length === 0) {
    return {
      total_attempts: 0,
      correct_attempts: 0,
      overall_accuracy: 0,
      avg_solving_time: {
        cr_avg_time: 0,
        rc_avg_question_time: 0,
        rc_avg_passage_time: 0,
        foundation_avg_time: 0,
        overall_avg_time: 0,
        display_summary: "No attempts recorded yet",
      },
      current_streak: 0,
      weak_topics_count: 0,
      weak_topics: [],
      last_practice_date: null,
      verbal_readiness: {
        score: 0,
        tier: "Diagnostic Stage",
        description: "Start practicing Critical Reasoning and Reading Comprehension to estimate your Verbal Readiness score.",
        breakdown: { cr_points: 0, rc_points: 0, pace_points: 0, coverage_points: 0 },
      },
    };
  }

  const totalAttempts = attempts.length;
  const correctAttempts = attempts.filter((a) => a.is_correct).length;
  const overallAccuracy = roundDecimals((correctAttempts / totalAttempts) * 100, 1);

  // Group attempts by section type
  const crAttempts = attempts.filter(
    (a) => a.verbal_type === "critical_reasoning" || a.mode === "gmat_verbal" && a.passage_id === null && !a.foundation_type
  );
  const rcAttempts = attempts.filter(
    (a) => a.verbal_type === "reading_comprehension" || Boolean(a.passage_id)
  );
  const foundationAttempts = attempts.filter((a) => a.mode === "foundation");

  // CR Solving Time: CR is isolated argument analysis (~100-120s target)
  const crTimes = crAttempts.map((a) => a.time_taken).filter((t) => typeof t === "number" && t > 0);
  const crAvgTime = crTimes.length > 0 ? roundDecimals(crTimes.reduce((acc, t) => acc + t, 0) / crTimes.length, 1) : 0;

  // RC Solving Time: Segregate passage reading time vs question answering time
  const rcQuestionTimes = rcAttempts
    .map((a) => (a.question_solving_time > 0 ? a.question_solving_time : a.time_taken))
    .filter((t) => typeof t === "number" && t > 0);
  const rcAvgQuestionTime =
    rcQuestionTimes.length > 0
      ? roundDecimals(rcQuestionTimes.reduce((acc, t) => acc + t, 0) / rcQuestionTimes.length, 1)
      : 0;

  const rcPassageTimes = rcAttempts
    .map((a) => a.reading_time)
    .filter((t) => typeof t === "number" && t > 0);
  const rcAvgPassageTime =
    rcPassageTimes.length > 0
      ? roundDecimals(rcPassageTimes.reduce((acc, t) => acc + t, 0) / rcPassageTimes.length, 1)
      : 0;

  // Foundation Solving Time:
  const foundationTimes = foundationAttempts
    .map((a) => a.time_taken)
    .filter((t) => typeof t === "number" && t > 0);
  const foundationAvgTime =
    foundationTimes.length > 0
      ? roundDecimals(foundationTimes.reduce((acc, t) => acc + t, 0) / foundationTimes.length, 1)
      : 0;

  // Overall avg solving time across all attempts
  const allTimes = attempts.map((a) => a.time_taken).filter((t) => typeof t === "number" && t > 0);
  const overallAvgTime =
    allTimes.length > 0 ? roundDecimals(allTimes.reduce((acc, t) => acc + t, 0) / allTimes.length, 1) : 0;

  // Distinct dates for streak
  const distinctDates = Array.from(new Set(attempts.map((a) => a.date).filter(Boolean)));
  distinctDates.sort().reverse();
  const currentStreak = calculateStreakFromDates(distinctDates);
  const lastPracticeDate = distinctDates.length > 0 ? distinctDates[0] : null;

  // Weak English topics count (<60% accuracy with at least 2 attempts)
  const topicMap = {};
  attempts.forEach((a) => {
    const topic = a.topic || "General";
    if (!topicMap[topic]) {
      topicMap[topic] = { attempts: 0, correct: 0 };
    }
    topicMap[topic].attempts++;
    if (a.is_correct) topicMap[topic].correct++;
  });

  const weakTopics = [];
  Object.keys(topicMap).forEach((topic) => {
    const stat = topicMap[topic];
    if (stat.attempts >= 2) {
      const acc = roundDecimals((stat.correct / stat.attempts) * 100, 1);
      if (acc < 60) {
        weakTopics.push({
          topic,
          attempts: stat.attempts,
          correct: stat.correct,
          accuracy: acc,
        });
      }
    }
  });
  weakTopics.sort((a, b) => a.accuracy - b.accuracy);

  // Estimated Verbal Readiness Score (0-100 index)
  // Components:
  // 1. CR Accuracy: up to 35 points
  // 2. RC Accuracy: up to 35 points
  // 3. Pacing Management: up to 15 points (Target: CR 80-120s, RC 60-100s)
  // 4. Coverage / Volume: up to 15 points (Scales with question diversity and volume up to 40 attempts)
  let crPoints = 0;
  if (crAttempts.length > 0) {
    const crAcc = crAttempts.filter((a) => a.is_correct).length / crAttempts.length;
    crPoints = roundDecimals(crAcc * 35, 1);
  } else if (foundationAttempts.length > 0) {
    // If no CR yet, give credit from foundation grammar/vocab
    const foundAcc = foundationAttempts.filter((a) => a.is_correct).length / foundationAttempts.length;
    crPoints = roundDecimals(foundAcc * 20, 1);
  }

  let rcPoints = 0;
  if (rcAttempts.length > 0) {
    const rcAcc = rcAttempts.filter((a) => a.is_correct).length / rcAttempts.length;
    rcPoints = roundDecimals(rcAcc * 35, 1);
  } else if (foundationAttempts.length > 0) {
    const foundAcc = foundationAttempts.filter((a) => a.is_correct).length / foundationAttempts.length;
    rcPoints = roundDecimals(foundAcc * 15, 1);
  }

  // Pace score calculation:
  // Benchmark: CR between 70s and 125s, RC question between 60s and 95s
  let pacePoints = 15;
  if (crTimes.length > 0) {
    if (crAvgTime > 120) {
      const penalty = Math.min(7.5, (crAvgTime - 120) / 10);
      pacePoints -= penalty;
    }
  }
  if (rcQuestionTimes.length > 0) {
    if (rcAvgQuestionTime > 95) {
      const penalty = Math.min(7.5, (rcAvgQuestionTime - 95) / 10);
      pacePoints -= penalty;
    }
  }
  pacePoints = Math.max(0, roundDecimals(pacePoints, 1));

  // Coverage score calculation:
  // Scales up to 40 questions and diverse types
  const uniqueTypes = new Set(attempts.map((a) => a.question_type).filter(Boolean));
  const volumeFactor = Math.min(10, (totalAttempts / 40) * 10);
  const varietyFactor = Math.min(5, (uniqueTypes.size / 6) * 5);
  const coveragePoints = roundDecimals(volumeFactor + varietyFactor, 1);

  const rawReadiness = crPoints + rcPoints + pacePoints + coveragePoints;
  const readinessScore = Math.min(100, Math.max(0, Math.round(rawReadiness)));

  let readinessTier = "Diagnostic Stage";
  let readinessDescription = "Early practice; continue with foundational and targeted question sets.";
  if (readinessScore >= 90) {
    readinessTier = "GMAT Ready (Target 85th+ percentile)";
    readinessDescription = "Excellent verbal command across CR argument structure and RC synthesis.";
  } else if (readinessScore >= 75) {
    readinessTier = "Advanced Competency";
    readinessDescription = "Strong accuracy and pace; fine-tune trap answer elimination on 700+ level questions.";
  } else if (readinessScore >= 60) {
    readinessTier = "Developing Competency";
    readinessDescription = "Solid foundation; focus on reducing slow/overtime questions and mastering assumption negation.";
  } else if (readinessScore >= 40) {
    readinessTier = "Foundation Building";
    readinessDescription = "Good baseline; bridge grammar and vocabulary mastery into complex CR and RC passages.";
  }

  return {
    total_attempts: totalAttempts,
    correct_attempts: correctAttempts,
    overall_accuracy: overallAccuracy,
    avg_solving_time: {
      cr_avg_time: crAvgTime,
      rc_avg_question_time: rcAvgQuestionTime,
      rc_avg_passage_time: rcAvgPassageTime,
      foundation_avg_time: foundationAvgTime,
      overall_avg_time: overallAvgTime,
      display_summary: `CR: ${crAvgTime}s | RC Q: ${rcAvgQuestionTime}s (Passage: ${rcAvgPassageTime}s) | Foundation: ${foundationAvgTime}s`,
    },
    current_streak: currentStreak,
    weak_topics_count: weakTopics.length,
    weak_topics: weakTopics,
    last_practice_date: lastPracticeDate,
    verbal_readiness: {
      score: readinessScore,
      tier: readinessTier,
      description: readinessDescription,
      breakdown: {
        cr_points: crPoints,
        rc_points: rcPoints,
        pace_points: pacePoints,
        coverage_points: coveragePoints,
      },
    },
  };
}

/**
 * Get isolated section metrics for Critical Reasoning and Reading Comprehension.
 * CR metrics: attempts, correct, accuracy, avg_time, median_time, slow_count, timeout_count, type_breakdown, topic_breakdown.
 * RC metrics: attempts, correct, accuracy, avg_passage_reading_time, avg_question_time, type_breakdown, topic_breakdown.
 * CR and RC speed metrics are strictly isolated and NEVER combined!
 * @returns {Promise<Object>}
 */
async function getEnglishSectionMetrics() {
  const attempts = await getAllEnglishAttempts();

  // Helper to build breakdown by key
  function buildBreakdown(list, key, timeField = "time_taken") {
    const result = {};
    list.forEach((item) => {
      const val = item[key] || "General";
      if (!result[val]) {
        result[val] = {
          attempts: 0,
          correct: 0,
          accuracy: 0,
          total_time: 0,
          avg_time: 0,
          times: [],
          slow_count: 0,
          timeout_count: 0,
          error_categories: {},
        };
      }
      const b = result[val];
      b.attempts++;
      if (item.is_correct) b.correct++;
      if (item.is_timeout) b.timeout_count++;

      const t = typeof item[timeField] === "number" ? item[timeField] : 0;
      if (t > 0) {
        b.total_time += t;
        b.times.push(t);
      }
      if (t > 120) b.slow_count++;

      if (!item.is_correct && item.error_category) {
        b.error_categories[item.error_category] = (b.error_categories[item.error_category] || 0) + 1;
      }
    });

    Object.keys(result).forEach((val) => {
      const b = result[val];
      b.accuracy = b.attempts > 0 ? roundDecimals((b.correct / b.attempts) * 100, 1) : 0;
      b.avg_time = b.times.length > 0 ? roundDecimals(b.total_time / b.times.length, 1) : 0;
      b.median_time = calculateMedian(b.times);
      delete b.total_time;
      delete b.times;
    });

    return result;
  }

  // Filter CR attempts
  const crAttempts = attempts.filter(
    (a) =>
      a.verbal_type === "critical_reasoning" ||
      (a.mode === "gmat_verbal" && !a.passage_id && a.foundation_type === null)
  );

  const crTimes = crAttempts.map((a) => a.time_taken).filter((t) => typeof t === "number" && t > 0);
  const crTotal = crAttempts.length;
  const crCorrect = crAttempts.filter((a) => a.is_correct).length;
  const crMetrics = {
    attempts: crTotal,
    correct: crCorrect,
    accuracy: crTotal > 0 ? roundDecimals((crCorrect / crTotal) * 100, 1) : 0,
    avg_time: crTimes.length > 0 ? roundDecimals(crTimes.reduce((a, b) => a + b, 0) / crTimes.length, 1) : 0,
    median_time: calculateMedian(crTimes),
    slow_count: crAttempts.filter((a) => a.time_taken > 120).length,
    timeout_count: crAttempts.filter((a) => a.is_timeout).length,
    type_breakdown: buildBreakdown(crAttempts, "question_type", "time_taken"),
    topic_breakdown: buildBreakdown(crAttempts, "topic", "time_taken"),
  };

  // Filter RC attempts
  const rcAttempts = attempts.filter(
    (a) => a.verbal_type === "reading_comprehension" || Boolean(a.passage_id)
  );

  const rcTotal = rcAttempts.length;
  const rcCorrect = rcAttempts.filter((a) => a.is_correct).length;

  const rcPassageTimes = rcAttempts
    .map((a) => a.reading_time)
    .filter((t) => typeof t === "number" && t > 0);
  const rcAvgPassageTime =
    rcPassageTimes.length > 0
      ? roundDecimals(rcPassageTimes.reduce((a, b) => a + b, 0) / rcPassageTimes.length, 1)
      : 0;

  const rcQuestionTimes = rcAttempts
    .map((a) => (a.question_solving_time > 0 ? a.question_solving_time : a.time_taken))
    .filter((t) => typeof t === "number" && t > 0);
  const rcAvgQuestionTime =
    rcQuestionTimes.length > 0
      ? roundDecimals(rcQuestionTimes.reduce((a, b) => a + b, 0) / rcQuestionTimes.length, 1)
      : 0;

  const rcMetrics = {
    attempts: rcTotal,
    correct: rcCorrect,
    accuracy: rcTotal > 0 ? roundDecimals((rcCorrect / rcTotal) * 100, 1) : 0,
    avg_passage_reading_time: rcAvgPassageTime,
    avg_question_time: rcAvgQuestionTime,
    median_question_time: calculateMedian(rcQuestionTimes),
    slow_count: rcAttempts.filter((a) => (a.question_solving_time || a.time_taken) > 100).length,
    timeout_count: rcAttempts.filter((a) => a.is_timeout).length,
    type_breakdown: buildBreakdown(rcAttempts, "question_type", "question_solving_time"),
    topic_breakdown: buildBreakdown(rcAttempts, "topic", "question_solving_time"),
  };

  // Foundation Grammar & Vocabulary Metrics
  const grammarAttempts = attempts.filter(
    (a) => a.foundation_type === "grammar" || (a.mode === "foundation" && a.topic && a.topic.toLowerCase().includes("grammar"))
  );
  const grammarTotal = grammarAttempts.length;
  const grammarCorrect = grammarAttempts.filter((a) => a.is_correct).length;
  const grammarTimes = grammarAttempts.map((a) => a.time_taken).filter((t) => t > 0);
  const grammarMetrics = {
    attempts: grammarTotal,
    correct: grammarCorrect,
    accuracy: grammarTotal > 0 ? roundDecimals((grammarCorrect / grammarTotal) * 100, 1) : 0,
    avg_time: grammarTimes.length > 0 ? roundDecimals(grammarTimes.reduce((a, b) => a + b, 0) / grammarTimes.length, 1) : 0,
    type_breakdown: buildBreakdown(grammarAttempts, "question_type", "time_taken"),
    topic_breakdown: buildBreakdown(grammarAttempts, "topic", "time_taken"),
  };

  const vocabAttempts = attempts.filter(
    (a) => a.foundation_type === "vocabulary" || (a.mode === "foundation" && a.topic && a.topic.toLowerCase().includes("vocab"))
  );
  const vocabTotal = vocabAttempts.length;
  const vocabCorrect = vocabAttempts.filter((a) => a.is_correct).length;
  const vocabTimes = vocabAttempts.map((a) => a.time_taken).filter((t) => t > 0);
  const vocabMetrics = {
    attempts: vocabTotal,
    correct: vocabCorrect,
    accuracy: vocabTotal > 0 ? roundDecimals((vocabCorrect / vocabTotal) * 100, 1) : 0,
    avg_time: vocabTimes.length > 0 ? roundDecimals(vocabTimes.reduce((a, b) => a + b, 0) / vocabTimes.length, 1) : 0,
    type_breakdown: buildBreakdown(vocabAttempts, "question_type", "time_taken"),
    topic_breakdown: buildBreakdown(vocabAttempts, "topic", "time_taken"),
  };

  return {
    cr_rc_speed_isolated: true,
    cr_metrics: crMetrics,
    rc_metrics: rcMetrics,
    foundation_metrics: {
      grammar: grammarMetrics,
      vocabulary: vocabMetrics,
    },
  };
}

/**
 * Normalizes a variant identifier and checks if an attempt matches it.
 * Supports: 'Critical Reasoning', 'Reading Comprehension', 'Strengthen', 'Weaken',
 * 'Assumption', 'Inference', 'Main Idea', 'Detail', 'Passage Function', 'Grammar', 'Vocabulary', etc.
 * @param {string} variant
 * @returns {Function} Matcher predicate (attempt) => boolean
 */
function createVariantMatcher(variant) {
  if (!variant || typeof variant !== "string") {
    return () => true;
  }
  const clean = variant.trim().toLowerCase().replace(/[_\s-]+/g, " ");

  if (clean === "critical reasoning" || clean === "cr") {
    return (a) =>
      a.verbal_type === "critical_reasoning" ||
      (a.mode === "gmat_verbal" && !a.passage_id && a.foundation_type === null);
  }
  if (clean === "reading comprehension" || clean === "rc") {
    return (a) => a.verbal_type === "reading_comprehension" || Boolean(a.passage_id);
  }
  if (clean === "foundation") {
    return (a) => a.mode === "foundation";
  }
  if (clean === "grammar") {
    return (a) =>
      a.foundation_type === "grammar" ||
      (a.topic && a.topic.toLowerCase().includes("grammar")) ||
      (a.question_type && a.question_type.toLowerCase().includes("grammar"));
  }
  if (clean === "vocabulary" || clean === "vocab") {
    return (a) =>
      a.foundation_type === "vocabulary" ||
      (a.topic && a.topic.toLowerCase().includes("vocab")) ||
      (a.question_type && a.question_type.toLowerCase().includes("vocab"));
  }

  // Exact or substring match across question_type or topic
  return (a) => {
    const qType = String(a.question_type || "").toLowerCase().replace(/[_\s-]+/g, " ");
    const topic = String(a.topic || "").toLowerCase().replace(/[_\s-]+/g, " ");
    return qType === clean || topic === clean || qType.includes(clean) || topic.includes(clean);
  };
}

/**
 * Get trend points (day-by-day and session-by-session) FOR THE SELECTED VARIANT ONLY.
 * @param {string} variant Identifier e.g. 'Critical Reasoning', 'Reading Comprehension', 'Strengthen', 'Weaken', 'Assumption', 'Inference', 'Main Idea', etc.
 * @returns {Promise<Object>}
 */
async function getEnglishVariantTrajectory(variant) {
  const attempts = await getAllEnglishAttempts();
  const matcher = createVariantMatcher(variant);
  const matchedAttempts = attempts.filter(matcher);

  if (matchedAttempts.length === 0) {
    return {
      variant: String(variant || "All"),
      total_attempts: 0,
      correct_attempts: 0,
      accuracy: 0,
      avg_time: 0,
      daily_trajectory: [],
      session_trajectory: [],
    };
  }

  // 1. Daily trajectory: group by date
  const dayGroups = {};
  matchedAttempts.forEach((a) => {
    const d = a.date || "Unknown";
    if (!dayGroups[d]) {
      dayGroups[d] = { date: d, total: 0, correct: 0, times: [] };
    }
    dayGroups[d].total++;
    if (a.is_correct) dayGroups[d].correct++;
    if (typeof a.time_taken === "number" && a.time_taken > 0) {
      dayGroups[d].times.push(a.time_taken);
    }
  });

  const dailyTrajectory = Object.keys(dayGroups)
    .sort()
    .map((d) => {
      const g = dayGroups[d];
      return {
        date: g.date,
        total: g.total,
        correct: g.correct,
        accuracy: g.total > 0 ? roundDecimals((g.correct / g.total) * 100, 1) : 0,
        avg_time: g.times.length > 0 ? roundDecimals(g.times.reduce((a, b) => a + b, 0) / g.times.length, 1) : 0,
      };
    });

  // 2. Session trajectory: group by session_id
  const sessionGroups = {};
  matchedAttempts.forEach((a) => {
    const sid = a.session_id || "single_attempt";
    if (!sessionGroups[sid]) {
      sessionGroups[sid] = {
        session_id: sid,
        date: a.date,
        timestamp: a.timestamp || 0,
        total: 0,
        correct: 0,
        times: [],
      };
    }
    sessionGroups[sid].total++;
    if (a.is_correct) sessionGroups[sid].correct++;
    if (typeof a.time_taken === "number" && a.time_taken > 0) {
      sessionGroups[sid].times.push(a.time_taken);
    }
    if (a.timestamp && a.timestamp > sessionGroups[sid].timestamp) {
      sessionGroups[sid].timestamp = a.timestamp;
    }
  });

  const sessionTrajectory = Object.values(sessionGroups)
    .sort((a, b) => a.timestamp - b.timestamp)
    .map((s) => ({
      session_id: s.session_id,
      date: s.date,
      timestamp: s.timestamp,
      total: s.total,
      correct: s.correct,
      accuracy: s.total > 0 ? roundDecimals((s.correct / s.total) * 100, 1) : 0,
      avg_time: s.times.length > 0 ? roundDecimals(s.times.reduce((a, b) => a + b, 0) / s.times.length, 1) : 0,
    }));

  const total = matchedAttempts.length;
  const correct = matchedAttempts.filter((a) => a.is_correct).length;
  const allTimes = matchedAttempts.map((a) => a.time_taken).filter((t) => typeof t === "number" && t > 0);

  return {
    variant: String(variant || "All"),
    total_attempts: total,
    correct_attempts: correct,
    accuracy: total > 0 ? roundDecimals((correct / total) * 100, 1) : 0,
    avg_time: allTimes.length > 0 ? roundDecimals(allTimes.reduce((a, b) => a + b, 0) / allTimes.length, 1) : 0,
    daily_trajectory: dailyTrajectory,
    session_trajectory: sessionTrajectory,
  };
}

/**
 * Generates an actionable English study plan:
 * - Lowest accuracy question types
 * - Highest average time question types
 * - Most frequent error categories
 * - Spaced repetition vocabulary due
 * - Bridge recommendations (e.g. from Foundation to GMAT)
 * @returns {Promise<Object>}
 */
async function getEnglishStudyPlan() {
  const attempts = await getAllEnglishAttempts();
  const vocabDue = await getVocabCardsForReview();

  if (attempts.length === 0) {
    return {
      status: "insufficient_data",
      message: "Complete at least one practice set to generate personalized study recommendations.",
      lowest_accuracy_types: [],
      highest_time_types: [],
      frequent_error_categories: [],
      vocab_due: {
        count: vocabDue.length,
        cards: vocabDue.slice(0, 10),
      },
      bridge_recommendations: [
        {
          id: "bridge_init_1",
          title: "Diagnostic Verbal Assessment",
          priority: "high",
          reason: "No attempts logged yet.",
          action: "Start with a 10-question mixed Critical Reasoning & Foundation set to establish your baseline accuracy and pacing.",
        },
      ],
      summary_text: "Begin practicing to unlock targeted diagnostic prescriptions and bridge recommendations.",
    };
  }

  // 1. Group by Question Type
  const qTypeMap = {};
  attempts.forEach((a) => {
    const qt = a.question_type || "General";
    if (!qTypeMap[qt]) {
      qTypeMap[qt] = { type: qt, attempts: 0, correct: 0, times: [], error_counts: {} };
    }
    qTypeMap[qt].attempts++;
    if (a.is_correct) qTypeMap[qt].correct++;
    if (typeof a.time_taken === "number" && a.time_taken > 0) {
      qTypeMap[qt].times.push(a.time_taken);
    }
    if (!a.is_correct && a.error_category) {
      qTypeMap[qt].error_counts[a.error_category] = (qTypeMap[qt].error_counts[a.error_category] || 0) + 1;
    }
  });

  const qTypeStats = Object.values(qTypeMap).map((item) => {
    const acc = item.attempts > 0 ? roundDecimals((item.correct / item.attempts) * 100, 1) : 0;
    const avgT = item.times.length > 0 ? roundDecimals(item.times.reduce((a, b) => a + b, 0) / item.times.length, 1) : 0;
    const prescription = QUESTION_TYPE_PRESCRIPTIONS[item.type] || {
      tip: "Review core premises and conclusion identification.",
      drill: "Practice targeted drills on this question type.",
    };
    return {
      question_type: item.type,
      attempts: item.attempts,
      correct: item.correct,
      accuracy: acc,
      avg_time: avgT,
      tip: prescription.tip,
      recommended_drill: prescription.drill,
    };
  });

  // Lowest accuracy question types (prioritize types with at least 2 attempts or sorted lowest)
  const lowestAccuracyTypes = [...qTypeStats]
    .sort((a, b) => {
      if (a.attempts >= 2 && b.attempts >= 2) return a.accuracy - b.accuracy;
      if (a.attempts >= 2) return -1;
      if (b.attempts >= 2) return 1;
      return a.accuracy - b.accuracy;
    })
    .slice(0, 5);

  // Highest average time question types
  const highestTimeTypes = [...qTypeStats]
    .filter((a) => a.attempts >= 2 && a.avg_time > 0)
    .sort((a, b) => b.avg_time - a.avg_time)
    .slice(0, 5);

  // 2. Error categories frequency
  const errorMap = {};
  let totalErrors = 0;
  attempts.forEach((a) => {
    if (!a.is_correct) {
      totalErrors++;
      const cat = a.error_category || "unclassified";
      errorMap[cat] = (errorMap[cat] || 0) + 1;
    }
  });

  const frequentErrorCategories = Object.keys(errorMap)
    .map((cat) => ({
      category: cat,
      count: errorMap[cat],
      percentage: totalErrors > 0 ? roundDecimals((errorMap[cat] / totalErrors) * 100, 1) : 0,
    }))
    .sort((a, b) => b.count - a.count);

  // 3. Bridge Recommendations (Foundation -> GMAT Verbal)
  const bridgeRecommendations = [];
  const foundationAttempts = attempts.filter((a) => a.mode === "foundation");
  const crAttempts = attempts.filter(
    (a) => a.verbal_type === "critical_reasoning" || a.mode === "gmat_verbal" && !a.passage_id
  );
  const rcAttempts = attempts.filter(
    (a) => a.verbal_type === "reading_comprehension" || Boolean(a.passage_id)
  );

  const foundationAcc =
    foundationAttempts.length > 0
      ? roundDecimals(
          (foundationAttempts.filter((a) => a.is_correct).length / foundationAttempts.length) * 100,
          1
        )
      : null;

  const crAcc =
    crAttempts.length > 0
      ? roundDecimals((crAttempts.filter((a) => a.is_correct).length / crAttempts.length) * 100, 1)
      : null;

  const rcAcc =
    rcAttempts.length > 0
      ? roundDecimals((rcAttempts.filter((a) => a.is_correct).length / rcAttempts.length) * 100, 1)
      : null;

  // Bridge Rule 1: High Foundation accuracy -> Ready for GMAT CR Assumption & Bold Face
  if (foundationAcc !== null && foundationAcc >= 75) {
    bridgeRecommendations.push({
      id: "bridge_grammar_to_cr",
      title: "Syntactic Mastery Bridge -> GMAT Critical Reasoning",
      priority: "high",
      reason: `High Foundation accuracy (${foundationAcc}%). You have mastered sentence syntax and core grammar rules.`,
      action:
        "Transition to GMAT Critical Reasoning: Focus on Assumption and Bold Face question types, applying your grammatical parsing skills to analyze complex multi-clause argument structures.",
    });
  } else if (foundationAcc !== null && foundationAcc < 60) {
    bridgeRecommendations.push({
      id: "bridge_grammar_reinforce",
      title: "Grammar Foundation Drill -> Clause & Modifier Rules",
      priority: "high",
      reason: `Foundation accuracy is ${foundationAcc}%. Incomplete mastery of sentence boundaries causes reading comprehension confusion.`,
      action:
        "Review Subject-Verb Agreement, Dangling Modifiers, and Parallelism before tackling dense 700+ GMAT arguments.",
    });
  }

  // Bridge Rule 2: Vocabulary -> Reading Comprehension speed
  if (vocabDue.length > 0) {
    bridgeRecommendations.push({
      id: "bridge_srs_vocab_due",
      title: "Spaced Repetition Vocabulary Review",
      priority: vocabDue.length > 5 ? "high" : "medium",
      reason: `You have ${vocabDue.length} vocabulary card(s) due for review today.`,
      action:
        "Complete your SRS flashcard review before your next reading comprehension session to enhance reading fluency and reduce contextual pauses.",
    });
  }

  // Bridge Rule 3: CR Assumption Negation Drill
  const assumptionStat = qTypeStats.find((s) => s.question_type.toLowerCase().includes("assumption"));
  if (assumptionStat && assumptionStat.accuracy < 70) {
    bridgeRecommendations.push({
      id: "bridge_assumption_negation",
      title: "Master the Negation Test for Assumptions",
      priority: "high",
      reason: `Assumption accuracy is ${assumptionStat.accuracy}%. Most assumption mistakes stem from confusing sufficient assumptions with necessary assumptions.`,
      action:
        "Apply the Negation Technique: Negate your shortlisted choice. If the argument's conclusion completely collapses, that option is the necessary assumption.",
    });
  }

  // Bridge Rule 4: RC Pacing & Skimming
  const rcTimes = rcAttempts
    .map((a) => a.question_solving_time || a.time_taken)
    .filter((t) => t > 0);
  const rcAvgQTime =
    rcTimes.length > 0 ? roundDecimals(rcTimes.reduce((a, b) => a + b, 0) / rcTimes.length, 1) : 0;
  if (rcAvgQTime > 105) {
    bridgeRecommendations.push({
      id: "bridge_rc_pacing",
      title: "RC Active Skimming & Mental Roadmapping",
      priority: "medium",
      reason: `Average RC question solving time is ${rcAvgQTime}s (GMAT target: 75-90s).`,
      action:
        "Adopt a 2.5-minute initial passage roadmap: Note paragraph purpose and author tone transitions, and only dive into details when direct questions cite them.",
    });
  }

  // Default fallback recommendation if few flags triggered
  if (bridgeRecommendations.length === 0) {
    bridgeRecommendations.push({
      id: "bridge_general_progress",
      title: "Consistent Mixed Practice",
      priority: "medium",
      reason: "Balanced verbal performance observed.",
      action: "Maintain daily practice sets alternating between Critical Reasoning arguments and 3-question Reading Comprehension passages.",
    });
  }

  // Summary Text
  let summaryText = `Your English practice spans ${attempts.length} attempts with ${lowestAccuracyTypes.length > 0 ? lowestAccuracyTypes[0].question_type : "core topics"} being your primary growth lever.`;
  if (lowestAccuracyTypes.length > 0 && lowestAccuracyTypes[0].accuracy < 60) {
    summaryText += ` Prioritize targeted drills on ${lowestAccuracyTypes[0].question_type} questions (${lowestAccuracyTypes[0].accuracy}% accuracy) and clear ${vocabDue.length} due vocabulary cards.`;
  }

  return {
    status: "active",
    total_analyzed: attempts.length,
    lowest_accuracy_types: lowestAccuracyTypes,
    highest_time_types: highestTimeTypes,
    frequent_error_categories: frequentErrorCategories,
    vocab_due: {
      count: vocabDue.length,
      cards: vocabDue.slice(0, 15),
    },
    bridge_recommendations: bridgeRecommendations,
    summary_text: summaryText,
  };
}

/**
 * Updates the error_category (and optionally trap_type) on a specific attempt in english_attempts.
 * @param {number} attemptId
 * @param {string} newErrorCategory
 * @param {string|null} [newTrapType=null]
 * @returns {Promise<Object>} The updated attempt record.
 */
async function updateEnglishMistakeClassification(attemptId, newErrorCategory, newTrapType = null) {
  const db = await initEnglishDB();
  const idNum = Number(attemptId);

  return new Promise((resolve, reject) => {
    const tx = db.transaction(STORES.ATTEMPTS, "readwrite");
    const store = tx.objectStore(STORES.ATTEMPTS);
    const getReq = store.get(idNum);

    getReq.onsuccess = () => {
      const record = getReq.result;
      if (!record) {
        reject(new Error(`Attempt with id ${attemptId} not found in ${STORES.ATTEMPTS}`));
        return;
      }

      record.error_category = String(newErrorCategory || "");
      if (newTrapType !== null && newTrapType !== undefined) {
        record.trap_type = String(newTrapType);
      }
      record.updated_at = Date.now();

      const putReq = store.put(record);
      putReq.onsuccess = () => resolve(record);
      putReq.onerror = (e) => reject(e.target.error);
    };

    getReq.onerror = (e) => reject(e.target.error);
  });
}

// ---------------------------------------------------------------------------
// 3. Spaced Repetition (SRS) Vocabulary APIs
// ---------------------------------------------------------------------------

/**
 * Retrieve vocabulary cards that are due for review (next_review_date <= today OR review_count === 0).
 * @returns {Promise<Array<Object>>}
 */
async function getVocabCardsForReview() {
  const db = await initEnglishDB();
  const todayStr = getTodayString();

  return new Promise((resolve, reject) => {
    const tx = db.transaction(STORES.VOCAB_SRS, "readonly");
    const store = tx.objectStore(STORES.VOCAB_SRS);
    const req = store.getAll();

    req.onsuccess = () => {
      const allCards = req.result || [];
      const dueCards = allCards.filter((card) => {
        if (!card.next_review_date || card.review_count === 0) return true;
        return card.next_review_date <= todayStr;
      });

      // Sort by next_review_date ascending (oldest overdue first), then unreviewed
      dueCards.sort((a, b) => {
        if (!a.next_review_date) return 1;
        if (!b.next_review_date) return -1;
        return a.next_review_date.localeCompare(b.next_review_date);
      });

      resolve(dueCards);
    };

    req.onerror = (e) => reject(e.target.error);
  });
}

/**
 * Record a spaced repetition review for a vocabulary card.
 * @param {string} word The vocabulary word
 * @param {string} userRating in ['easy', 'difficult', 'need_review', 'mastered']
 * @returns {Promise<Object>} The updated vocabulary card record.
 */
async function recordVocabCardReview(word, userRating) {
  if (!word || typeof word !== "string") {
    throw new Error("Valid word string is required for recordVocabCardReview");
  }
  const cleanWord = word.trim().toLowerCase();
  const validRatings = ["easy", "difficult", "need_review", "mastered"];
  const rating = validRatings.includes(userRating) ? userRating : "need_review";

  const db = await initEnglishDB();
  const todayStr = getTodayString();
  const nowMs = Date.now();

  return new Promise((resolve, reject) => {
    const tx = db.transaction(STORES.VOCAB_SRS, "readwrite");
    const store = tx.objectStore(STORES.VOCAB_SRS);
    const getReq = store.get(cleanWord);

    getReq.onsuccess = () => {
      let card = getReq.result;

      if (!card) {
        // Find in default vocab if available
        const defaultDef = DEFAULT_GMAT_VOCAB.find((v) => v.word.toLowerCase() === cleanWord);
        card = {
          word: cleanWord,
          definition: defaultDef ? defaultDef.definition : "",
          examples: defaultDef ? defaultDef.examples || [] : [],
          synonyms: defaultDef ? defaultDef.synonyms || [] : [],
          level: defaultDef ? defaultDef.level : "intermediate",
          review_count: 0,
          correct_recall_count: 0,
          retention_score: 50,
          current_interval_days: 1,
          last_reviewed_date: null,
          last_reviewed_timestamp: null,
          next_review_date: null,
          user_rating: null,
          history: [],
        };
      }

      card.review_count = (card.review_count || 0) + 1;
      card.last_reviewed_date = todayStr;
      card.last_reviewed_timestamp = nowMs;
      card.user_rating = rating;

      if (!Array.isArray(card.history)) {
        card.history = [];
      }

      let intervalDays = 1;
      let retention = typeof card.retention_score === "number" ? card.retention_score : 50;

      // Intervals progression logic:
      // Intervals: [1, 3, 7, 14, 30, 60]
      const currentInterval = card.current_interval_days || 1;
      let currentIndex = SRS_INTERVALS.indexOf(currentInterval);
      if (currentIndex === -1) {
        currentIndex = 0;
      }

      if (rating === "mastered") {
        intervalDays = 30;
        if (currentInterval >= 30) intervalDays = 60;
        retention = 100;
        card.correct_recall_count = (card.correct_recall_count || 0) + 1;
      } else if (rating === "easy") {
        // Advance to next interval step
        const nextIndex = Math.min(SRS_INTERVALS.length - 1, currentIndex + 1);
        intervalDays = SRS_INTERVALS[nextIndex];
        retention = Math.min(100, retention + 15);
        card.correct_recall_count = (card.correct_recall_count || 0) + 1;
      } else if (rating === "need_review") {
        // Reset or mild fallback (1-2 days)
        intervalDays = Math.max(1, Math.min(3, Math.floor(currentInterval / 2)));
        retention = Math.max(15, retention - 5);
      } else if (rating === "difficult") {
        // Reset to initial interval
        intervalDays = 1;
        retention = Math.max(0, retention - 25);
      }

      card.current_interval_days = intervalDays;
      card.retention_score = retention;

      // Calculate next review date string
      const nextDate = new Date();
      nextDate.setDate(nextDate.getDate() + intervalDays);
      card.next_review_date = nextDate.toISOString().slice(0, 10);

      // Record in history log
      card.history.push({
        date: todayStr,
        timestamp: nowMs,
        rating: rating,
        interval_days: intervalDays,
        retention_score: retention,
      });

      const putReq = store.put(card);
      putReq.onsuccess = () => resolve(card);
      putReq.onerror = (e) => reject(e.target.error);
    };

    getReq.onerror = (e) => reject(e.target.error);
  });
}

/**
 * Add or update a vocabulary card in english_vocab_srs.
 * @param {Object} card
 * @returns {Promise<Object>}
 */
async function addVocabCard(card) {
  if (!card || !card.word) {
    throw new Error("Card must contain a 'word' property");
  }
  const db = await initEnglishDB();
  const cleanWord = String(card.word).trim().toLowerCase();

  const record = {
    word: cleanWord,
    definition: String(card.definition || ""),
    examples: Array.isArray(card.examples) ? card.examples : card.examples ? [String(card.examples)] : [],
    synonyms: Array.isArray(card.synonyms) ? card.synonyms : [],
    level: String(card.level || "intermediate"),
    review_count: Number(card.review_count) || 0,
    correct_recall_count: Number(card.correct_recall_count) || 0,
    retention_score: typeof card.retention_score === "number" ? card.retention_score : 50,
    current_interval_days: Number(card.current_interval_days) || 1,
    last_reviewed_date: card.last_reviewed_date || null,
    last_reviewed_timestamp: card.last_reviewed_timestamp || null,
    next_review_date: card.next_review_date || getTodayString(),
    user_rating: card.user_rating || null,
    history: Array.isArray(card.history) ? card.history : [],
  };

  return new Promise((resolve, reject) => {
    const tx = db.transaction(STORES.VOCAB_SRS, "readwrite");
    const store = tx.objectStore(STORES.VOCAB_SRS);
    const req = store.put(record);

    req.onsuccess = () => resolve(record);
    req.onerror = (e) => reject(e.target.error);
  });
}

/**
 * Bulk add vocabulary cards into english_vocab_srs.
 * @param {Array<Object>} cards
 * @returns {Promise<number>} Count of cards added.
 */
async function bulkAddVocabCards(cards) {
  if (!Array.isArray(cards) || cards.length === 0) return 0;
  const db = await initEnglishDB();

  return new Promise((resolve, reject) => {
    const tx = db.transaction(STORES.VOCAB_SRS, "readwrite");
    const store = tx.objectStore(STORES.VOCAB_SRS);
    let count = 0;

    cards.forEach((c) => {
      if (c && c.word) {
        const cleanWord = String(c.word).trim().toLowerCase();
        const record = {
          word: cleanWord,
          definition: String(c.definition || ""),
          examples: Array.isArray(c.examples) ? c.examples : c.examples ? [String(c.examples)] : [],
          synonyms: Array.isArray(c.synonyms) ? c.synonyms : [],
          level: String(c.level || "intermediate"),
          review_count: Number(c.review_count) || 0,
          correct_recall_count: Number(c.correct_recall_count) || 0,
          retention_score: typeof c.retention_score === "number" ? c.retention_score : 50,
          current_interval_days: Number(c.current_interval_days) || 1,
          last_reviewed_date: c.last_reviewed_date || null,
          last_reviewed_timestamp: c.last_reviewed_timestamp || null,
          next_review_date: c.next_review_date || getTodayString(),
          user_rating: c.user_rating || null,
          history: Array.isArray(c.history) ? c.history : [],
        };
        store.put(record);
        count++;
      }
    });

    tx.oncomplete = () => resolve(count);
    tx.onerror = (e) => reject(e.target.error);
  });
}

/**
 * Retrieve all vocabulary cards stored in english_vocab_srs.
 * @returns {Promise<Array<Object>>}
 */
async function getAllVocabCards() {
  const db = await initEnglishDB();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(STORES.VOCAB_SRS, "readonly");
    const store = tx.objectStore(STORES.VOCAB_SRS);
    const req = store.getAll();

    req.onsuccess = () => resolve(req.result || []);
    req.onerror = (e) => reject(e.target.error);
  });
}

/**
 * Seed the default GMAT vocabulary cards if the store is currently empty.
 * @returns {Promise<number>} Number of seeded cards.
 */
async function seedDefaultVocabCards() {
  const existing = await getAllVocabCards();
  if (existing.length > 0) {
    return 0; // Already initialized
  }
  return await bulkAddVocabCards(DEFAULT_GMAT_VOCAB);
}

/**
 * Get vocabulary statistics (total cards, mastered, due, average retention).
 * @returns {Promise<Object>}
 */
async function getVocabStats() {
  const cards = await getAllVocabCards();
  const todayStr = getTodayString();

  const total = cards.length;
  const mastered = cards.filter((c) => c.user_rating === "mastered" || c.retention_score >= 95).length;
  const due = cards.filter((c) => !c.next_review_date || c.next_review_date <= todayStr).length;
  const avgRetention =
    total > 0
      ? roundDecimals(cards.reduce((acc, c) => acc + (c.retention_score || 50), 0) / total, 1)
      : 0;

  return {
    total_cards: total,
    mastered_count: mastered,
    due_count: due,
    average_retention_score: avgRetention,
  };
}

// ---------------------------------------------------------------------------
// 4. Backup & Export APIs
// ---------------------------------------------------------------------------

/**
 * Export complete English data as a JSON payload string.
 * Optionally triggers browser download if triggerDownload is true.
 * @param {boolean} [triggerDownload=false]
 * @returns {Promise<string>} Formatted JSON string.
 */
async function exportEnglishDataJSON(triggerDownload = false) {
  const attempts = await getAllEnglishAttempts();
  const sessions = await getAllEnglishSessions();
  const activeSession = await getActiveEnglishSession();
  const vocabCards = await getAllVocabCards();

  const exportPayload = {
    export_timestamp: new Date().toISOString(),
    version: DB_VERSION,
    db_name: DB_NAME,
    stats: {
      total_attempts: attempts.length,
      total_sessions: sessions.length,
      total_vocab_cards: vocabCards.length,
      has_active_session: Boolean(activeSession),
    },
    attempts: attempts,
    sessions: sessions,
    active_session: activeSession,
    vocab_srs: vocabCards,
  };

  const jsonString = JSON.stringify(exportPayload, null, 2);

  if (triggerDownload && typeof window !== "undefined") {
    const pad = (n) => String(n).padStart(2, "0");
    const d = new Date();
    const stamp = `${d.getFullYear()}${pad(d.getMonth() + 1)}${pad(d.getDate())}_${pad(d.getHours())}${pad(d.getMinutes())}${pad(d.getSeconds())}`;
    const filename = `aptitude_english_backup_${stamp}.json`;
    const blob = new Blob([jsonString], { type: "application/json;charset=utf-8" });
    triggerBrowserDownload(blob, filename);
  }

  return jsonString;
}

/**
 * Import English data from a JSON string or object payload.
 * Restores attempts, sessions, vocab cards, and active session state.
 * @param {string|Object} payload
 * @returns {Promise<Object>} Import summary counts.
 */
async function importEnglishDataJSON(payload) {
  let data;
  if (typeof payload === "string") {
    try {
      data = JSON.parse(payload);
    } catch (e) {
      throw new Error(`Failed to parse JSON payload: ${e.message}`);
    }
  } else if (payload && typeof payload === "object") {
    data = payload;
  } else {
    throw new Error("Invalid payload provided to importEnglishDataJSON");
  }

  const db = await initEnglishDB();
  let attemptsImported = 0;
  let sessionsImported = 0;
  let vocabCardsImported = 0;
  let activeSessionRestored = false;

  const rawSessions = Array.isArray(data.sessions) ? data.sessions : [];
  const rawAttempts = Array.isArray(data.attempts) ? data.attempts : [];
  const rawVocab = Array.isArray(data.vocab_srs) ? data.vocab_srs : [];
  const rawActive = data.active_session;

  // 1. Import sessions
  if (rawSessions.length > 0) {
    await new Promise((resolve, reject) => {
      const tx = db.transaction(STORES.SESSIONS, "readwrite");
      const store = tx.objectStore(STORES.SESSIONS);
      rawSessions.forEach((s) => {
        if (s && s.session_id) {
          store.put(s);
          sessionsImported++;
        }
      });
      tx.oncomplete = () => resolve();
      tx.onerror = (e) => reject(e.target.error);
    });
  }

  // 2. Import attempts
  if (rawAttempts.length > 0) {
    await new Promise((resolve, reject) => {
      const tx = db.transaction(STORES.ATTEMPTS, "readwrite");
      const store = tx.objectStore(STORES.ATTEMPTS);
      rawAttempts.forEach((a) => {
        if (a) {
          const toAdd = { ...a };
          // Remove old numeric id so autoIncrement assigns a fresh clean key if needed, or preserve
          delete toAdd.id;
          store.add(toAdd);
          attemptsImported++;
        }
      });
      tx.oncomplete = () => resolve();
      tx.onerror = (e) => reject(e.target.error);
    });
  }

  // 3. Import vocab cards
  if (rawVocab.length > 0) {
    await new Promise((resolve, reject) => {
      const tx = db.transaction(STORES.VOCAB_SRS, "readwrite");
      const store = tx.objectStore(STORES.VOCAB_SRS);
      rawVocab.forEach((card) => {
        if (card && card.word) {
          store.put(card);
          vocabCardsImported++;
        }
      });
      tx.oncomplete = () => resolve();
      tx.onerror = (e) => reject(e.target.error);
    });
  }

  // 4. Restore active session if present
  if (rawActive && typeof rawActive === "object" && rawActive.session_id) {
    await saveActiveEnglishSession(rawActive);
    activeSessionRestored = true;
  }

  return {
    attemptsImported,
    sessionsImported,
    vocabCardsImported,
    activeSessionRestored,
  };
}

/**
 * Delete a single attempt by numeric id.
 * @param {number} attemptId
 * @returns {Promise<boolean>}
 */
async function deleteEnglishAttempt(attemptId) {
  const db = await initEnglishDB();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(STORES.ATTEMPTS, "readwrite");
    const store = tx.objectStore(STORES.ATTEMPTS);
    const req = store.delete(Number(attemptId));

    req.onsuccess = () => resolve(true);
    req.onerror = (e) => reject(e.target.error);
  });
}

/**
 * Clear all records from AptitudeEnglishDB (useful for testing or full reset).
 * @returns {Promise<boolean>}
 */
async function clearAllEnglishData() {
  const db = await initEnglishDB();
  const stores = [STORES.ATTEMPTS, STORES.SESSIONS, STORES.ACTIVE_SESSION, STORES.VOCAB_SRS];

  await new Promise((resolve, reject) => {
    const tx = db.transaction(stores, "readwrite");
    stores.forEach((s) => tx.objectStore(s).clear());
    tx.oncomplete = () => resolve();
    tx.onerror = (e) => reject(e.target.error);
  });

  return true;
}

// ---------------------------------------------------------------------------
// 5. Global & Window Exposure
// ---------------------------------------------------------------------------

const AptitudeEnglishDB = {
  // Initialization
  initEnglishDB,

  // Persistence APIs
  recordEnglishAttempt,
  recordEnglishSession,
  saveActiveEnglishSession,
  getActiveEnglishSession,
  clearActiveEnglishSession,
  getAllEnglishAttempts,
  getAllEnglishSessions,
  getEnglishAttemptsBySession,
  deleteEnglishAttempt,
  clearAllEnglishData,

  // Analytics APIs
  getEnglishOverview,
  getEnglishSectionMetrics,
  getEnglishVariantTrajectory,
  getEnglishStudyPlan,
  updateEnglishMistakeClassification,

  // Spaced Repetition (SRS) Vocabulary APIs
  getVocabCardsForReview,
  recordVocabCardReview,
  addVocabCard,
  bulkAddVocabCards,
  getAllVocabCards,
  seedDefaultVocabCards,
  getVocabStats,

  // Backup & Export
  exportEnglishDataJSON,
  importEnglishDataJSON,
};

if (typeof window !== "undefined") {
  window.AptitudeEnglishDB = AptitudeEnglishDB;
  window.initEnglishDB = initEnglishDB;
  window.recordEnglishAttempt = recordEnglishAttempt;
  window.recordEnglishSession = recordEnglishSession;
  window.saveActiveEnglishSession = saveActiveEnglishSession;
  window.getActiveEnglishSession = getActiveEnglishSession;
  window.clearActiveEnglishSession = clearActiveEnglishSession;
  window.getAllEnglishAttempts = getAllEnglishAttempts;
  window.getAllEnglishSessions = getAllEnglishSessions;
  window.getEnglishAttemptsBySession = getEnglishAttemptsBySession;
  window.deleteEnglishAttempt = deleteEnglishAttempt;
  window.clearAllEnglishData = clearAllEnglishData;
  window.getEnglishOverview = getEnglishOverview;
  window.getEnglishSectionMetrics = getEnglishSectionMetrics;
  window.getEnglishVariantTrajectory = getEnglishVariantTrajectory;
  window.getEnglishStudyPlan = getEnglishStudyPlan;
  window.updateEnglishMistakeClassification = updateEnglishMistakeClassification;
  window.getVocabCardsForReview = getVocabCardsForReview;
  window.recordVocabCardReview = recordVocabCardReview;
  window.addVocabCard = addVocabCard;
  window.bulkAddVocabCards = bulkAddVocabCards;
  window.getAllVocabCards = getAllVocabCards;
  window.seedDefaultVocabCards = seedDefaultVocabCards;
  window.getVocabStats = getVocabStats;
  window.exportEnglishDataJSON = exportEnglishDataJSON;
  window.importEnglishDataJSON = importEnglishDataJSON;
}

if (typeof module !== "undefined" && module.exports) {
  module.exports = AptitudeEnglishDB;
}
