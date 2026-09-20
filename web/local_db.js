/**
 * AptitudeLocalDB - Persistent On-Device Storage using IndexedDB
 * Handles local attempts, sessions, analytics aggregation, and JSON/CSV backup & restore.
 */

const DB_NAME = "AptitudeLocalDB";
const DB_VERSION = 1;

let dbInstance = null;
let dbPromise = null;

function initLocalDB() {
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

      if (!db.objectStoreNames.contains("attempts")) {
        const attemptStore = db.createObjectStore("attempts", { keyPath: "id", autoIncrement: true });
        attemptStore.createIndex("date", "date", { unique: false });
        attemptStore.createIndex("timestamp", "timestamp", { unique: false });
        attemptStore.createIndex("session_id", "session_id", { unique: false });
        attemptStore.createIndex("category_name", "category_name", { unique: false });
        attemptStore.createIndex("topic_name", "topic_name", { unique: false });
        attemptStore.createIndex("pattern_id", "pattern_id", { unique: false });
        attemptStore.createIndex("is_correct", "is_correct", { unique: false });
      }

      if (!db.objectStoreNames.contains("sessions")) {
        const sessionStore = db.createObjectStore("sessions", { keyPath: "session_id" });
        sessionStore.createIndex("date", "date", { unique: false });
        sessionStore.createIndex("timestamp", "timestamp", { unique: false });
      }
    };

    request.onsuccess = (event) => {
      dbInstance = event.target.result;
      resolve(dbInstance);
    };

    request.onerror = (event) => {
      dbPromise = null;
      reject(event.target.error);
    };
  });

  return dbPromise;
}

function getTodayString() {
  return new Date().toISOString().slice(0, 10);
}

function getBackupTimestamp() {
  const now = new Date();
  const pad = (n) => String(n).padStart(2, "0");
  return `${now.getFullYear()}${pad(now.getMonth() + 1)}${pad(now.getDate())}_${pad(now.getHours())}${pad(now.getMinutes())}${pad(now.getSeconds())}`;
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
  }, 100);
}

function escapeCSVField(val) {
  if (val === null || val === undefined) {
    return '""';
  }
  let str;
  if (Array.isArray(val)) {
    str = val.join(" | ");
  } else if (typeof val === "object") {
    str = JSON.stringify(val);
  } else {
    str = String(val);
  }
  return `"${str.replace(/"/g, '""')}"`;
}

async function recordLocalAttempt(attempt) {
  const db = await initLocalDB();
  const now = new Date();
  const dateStr = attempt.date || now.toISOString().slice(0, 10);
  const timestamp = typeof attempt.timestamp === "number" ? attempt.timestamp : now.getTime();

  const record = {
    remote_id: attempt.remote_id !== undefined ? Number(attempt.remote_id) : null,
    date: dateStr,
    timestamp: timestamp,
    session_id: String(attempt.session_id || ""),
    category_name: String(attempt.category_name || "General"),
    topic_name: String(attempt.topic_name || "General"),
    pattern_id: Number(attempt.pattern_id || 0),
    pattern_name: String(attempt.pattern_name || ""),
    hybrid_type: String(attempt.hybrid_type || ""),
    question_text: String(attempt.question_text || ""),
    options: Array.isArray(attempt.options) ? attempt.options : [],
    selected_answer: attempt.selected_answer !== undefined ? attempt.selected_answer : null,
    typed_answer: attempt.typed_answer !== undefined ? attempt.typed_answer : null,
    correct_answer: attempt.correct_answer !== undefined ? attempt.correct_answer : null,
    correct_option_index: attempt.correct_option_index !== undefined ? Number(attempt.correct_option_index) : null,
    is_correct: Boolean(attempt.is_correct),
    is_timeout: Boolean(attempt.is_timeout),
    is_skipped: Boolean(attempt.is_skipped),
    time_taken: typeof attempt.time_taken === "number" ? attempt.time_taken : Number(attempt.time_taken) || 0,
    explanation: String(attempt.explanation || ""),
    difficulty: attempt.difficulty !== undefined ? attempt.difficulty : 3,
    user_id: attempt.user_id !== undefined ? attempt.user_id : null,
  };

  return new Promise((resolve, reject) => {
    const tx = db.transaction("attempts", "readwrite");
    const store = tx.objectStore("attempts");
    const req = store.add(record);

    req.onsuccess = () => {
      record.id = req.result;
      resolve(record);
    };

    req.onerror = (e) => reject(e.target.error);
  });
}

async function recordLocalSession(session) {
  const db = await initLocalDB();
  const now = new Date();
  const dateStr = session.date || now.toISOString().slice(0, 10);
  const timestamp = typeof session.timestamp === "number" ? session.timestamp : now.getTime();

  const record = {
    ...session,
    session_id: String(session.session_id || `session_${timestamp}`),
    date: dateStr,
    timestamp: timestamp,
    score: Number(session.score || 0),
    total_questions: Number(session.total_questions || session.planned_total_questions || 0),
    accuracy: Number(session.accuracy || 0),
    avg_time: Number(session.avg_time || 0),
    weak_count: Number(session.weak_count || 0),
    stopped: Boolean(session.stopped),
    user_id: session.user_id !== undefined ? session.user_id : null,
  };

  return new Promise((resolve, reject) => {
    const tx = db.transaction("sessions", "readwrite");
    const store = tx.objectStore("sessions");
    const req = store.put(record);

    req.onsuccess = () => resolve(record);
    req.onerror = (e) => reject(e.target.error);
  });
}

async function getAllLocalAttempts() {
  const db = await initLocalDB();
  return new Promise((resolve, reject) => {
    const tx = db.transaction("attempts", "readonly");
    const store = tx.objectStore("attempts");
    const req = store.getAll();

    req.onsuccess = () => {
      const records = req.result || [];
      records.sort((a, b) => (b.timestamp || 0) - (a.timestamp || 0));
      resolve(records);
    };

    req.onerror = (e) => reject(e.target.error);
  });
}

async function getAllLocalSessions() {
  const db = await initLocalDB();
  return new Promise((resolve, reject) => {
    const tx = db.transaction("sessions", "readonly");
    const store = tx.objectStore("sessions");
    const req = store.getAll();

    req.onsuccess = () => {
      const records = req.result || [];
      records.sort((a, b) => (b.timestamp || 0) - (a.timestamp || 0));
      resolve(records);
    };

    req.onerror = (e) => reject(e.target.error);
  });
}

async function syncRemoteHistory(history) {
  const remoteAttempts = Array.isArray(history?.attempts) ? history.attempts : [];
  const remoteSessions = Array.isArray(history?.sessions) ? history.sessions : [];
  const existingAttempts = await getAllLocalAttempts();
  const existingRemoteIds = new Set(existingAttempts.map((item) => item.remote_id).filter((id) => id !== null && id !== undefined));
  for (const attempt of remoteAttempts) {
    if (attempt.remote_id !== null && attempt.remote_id !== undefined && existingRemoteIds.has(Number(attempt.remote_id))) continue;
    await recordLocalAttempt(attempt);
  }
  const existingSessions = await getAllLocalSessions();
  const existingSessionIds = new Set(existingSessions.map((item) => String(item.session_id || "")));
  for (const session of remoteSessions) {
    if (existingSessionIds.has(String(session.session_id || ""))) continue;
    await recordLocalSession(session);
  }
  return { attempts: remoteAttempts.length, sessions: remoteSessions.length };
}

async function getLocalAnalytics() {
  const attempts = await getAllLocalAttempts();

  const total_attempts = attempts.length;
  let total_correct = 0;
  let total_time = 0;

  attempts.forEach((a) => {
    if (a.is_correct) total_correct++;
    total_time += Number(a.time_taken || 0);
  });

  const overallAvgTime = total_attempts > 0 ? Number((total_time / total_attempts).toFixed(1)) : 0;
  const overallAccuracy = total_attempts > 0 ? Math.round((total_correct / total_attempts) * 100) : 0;

  const days = {};
  const categories = {};
  const patterns = {};
  const questions = {};

  attempts.forEach((attempt) => {
    const d = attempt.date || (attempt.timestamp ? new Date(attempt.timestamp).toISOString().slice(0, 10) : getTodayString());
    const cat = attempt.category_name || "General";
    const top = attempt.topic_name || "General";
    const patId = Number(attempt.pattern_id || 0);
    const patName = attempt.pattern_name || (patId ? `Pattern #${patId}` : "General Pattern");
    const isCorrect = Boolean(attempt.is_correct);
    const timeTaken = Number(attempt.time_taken || 0);
    const isSlow = timeTaken > (overallAvgTime || 15) || Boolean(attempt.is_timeout);
    const qRaw = String(attempt.question_text || "").trim();
    // Keep identical question text separate when it belongs to different patterns.
    // This makes frequency data accurate for a specific pattern, e.g. Squares -> 21.
    const qKey = `${patId}::${qRaw || (patId ? `Pattern ${patId} Question` : "General Question")}`;

    // Global Question aggregation
    if (!questions[qKey]) {
      questions[qKey] = {
        question_text: qRaw,
        category_name: cat,
        topic_name: top,
        pattern_id: patId,
        pattern_name: patName,
        options: Array.isArray(attempt.options) ? attempt.options : [],
        correct_answer: attempt.correct_answer !== undefined ? attempt.correct_answer : null,
        correct_option_index: attempt.correct_option_index,
        explanation: attempt.explanation || "",
        difficulty: attempt.difficulty || 3,
        total_seen: 0,
        correct_count: 0,
        wrong_count: 0,
        timeout_count: 0,
        slow_count: 0,
        total_time: 0,
        avg_time: 0,
        accuracy: 0,
        first_timestamp: attempt.timestamp || 0,
        last_timestamp: attempt.timestamp || 0,
        last_date: d,
        attempts: [],
      };
    }
    questions[qKey].total_seen++;
    if (isCorrect) questions[qKey].correct_count++;
    else questions[qKey].wrong_count++;
    if (attempt.is_timeout) questions[qKey].timeout_count++;
    if (isSlow) questions[qKey].slow_count++;
    questions[qKey].total_time += timeTaken;
    if ((attempt.timestamp || 0) > questions[qKey].last_timestamp) {
      questions[qKey].last_timestamp = attempt.timestamp || 0;
      questions[qKey].last_date = d;
    }
    questions[qKey].attempts.push(attempt);

    // Day aggregation
    if (!days[d]) {
      days[d] = {
        date: d,
        total: 0,
        correct: 0,
        accuracy: 0,
        avg_time: 0,
        slow_count: 0,
        total_time: 0,
        attempts: [],
      };
    }
    days[d].total++;
    if (isCorrect) days[d].correct++;
    days[d].total_time += timeTaken;
    if (isSlow) days[d].slow_count++;
    days[d].attempts.push(attempt);

    // Category aggregation
    if (!categories[cat]) {
      categories[cat] = {
        category: cat,
        total: 0,
        correct: 0,
        accuracy: 0,
        avg_time: 0,
        total_time: 0,
        topics: {},
      };
    }
    categories[cat].total++;
    if (isCorrect) categories[cat].correct++;
    categories[cat].total_time += timeTaken;

    if (!categories[cat].topics[top]) {
      categories[cat].topics[top] = {
        topic: top,
        total: 0,
        correct: 0,
        accuracy: 0,
        avg_time: 0,
        total_time: 0,
        patterns: {},
      };
    }
    categories[cat].topics[top].total++;
    if (isCorrect) categories[cat].topics[top].correct++;
    categories[cat].topics[top].total_time += timeTaken;

    if (!categories[cat].topics[top].patterns[patId]) {
      categories[cat].topics[top].patterns[patId] = {
        pattern_id: patId,
        pattern_name: patName,
        total: 0,
        correct: 0,
        accuracy: 0,
        avg_time: 0,
        total_time: 0,
      };
    }
    categories[cat].topics[top].patterns[patId].total++;
    if (isCorrect) categories[cat].topics[top].patterns[patId].correct++;
    categories[cat].topics[top].patterns[patId].total_time += timeTaken;

    // Pattern aggregation
    if (!patterns[patId]) {
      patterns[patId] = {
        pattern_id: patId,
        pattern_name: patName,
        topic_name: top,
        category_name: cat,
        total: 0,
        correct: 0,
        accuracy: 0,
        avg_time: 0,
        slow_count: 0,
        total_time: 0,
        questions: {},
      };
    }
    if (!patterns[patId].questions) {
      patterns[patId].questions = {};
    }
    patterns[patId].total++;
    if (isCorrect) patterns[patId].correct++;
    patterns[patId].total_time += timeTaken;
    if (isSlow) patterns[patId].slow_count++;

    if (!patterns[patId].questions[qKey]) {
      patterns[patId].questions[qKey] = {
        question_text: qRaw,
        options: Array.isArray(attempt.options) ? attempt.options : [],
        correct_answer: attempt.correct_answer !== undefined ? attempt.correct_answer : null,
        correct_option_index: attempt.correct_option_index,
        explanation: attempt.explanation || "",
        total_seen: 0,
        correct_count: 0,
        wrong_count: 0,
        timeout_count: 0,
        slow_count: 0,
        total_time: 0,
        avg_time: 0,
        accuracy: 0,
        last_date: d,
        last_timestamp: attempt.timestamp || 0,
        attempts: [],
      };
    }
    patterns[patId].questions[qKey].total_seen++;
    if (isCorrect) patterns[patId].questions[qKey].correct_count++;
    else patterns[patId].questions[qKey].wrong_count++;
    if (attempt.is_timeout) patterns[patId].questions[qKey].timeout_count++;
    if (isSlow) patterns[patId].questions[qKey].slow_count++;
    patterns[patId].questions[qKey].total_time += timeTaken;
    if ((attempt.timestamp || 0) > patterns[patId].questions[qKey].last_timestamp) {
      patterns[patId].questions[qKey].last_timestamp = attempt.timestamp || 0;
      patterns[patId].questions[qKey].last_date = d;
    }
    patterns[patId].questions[qKey].attempts.push(attempt);
  });

  // Calculate averages and accuracies for global questions
  Object.values(questions).forEach((qItem) => {
    qItem.accuracy = qItem.total_seen > 0 ? Math.round((qItem.correct_count / qItem.total_seen) * 100) : 0;
    qItem.avg_time = qItem.total_seen > 0 ? Number((qItem.total_time / qItem.total_seen).toFixed(1)) : 0;
    delete qItem.total_time;
  });

  // Calculate averages and accuracies for days
  Object.values(days).forEach((item) => {
    item.accuracy = item.total > 0 ? Math.round((item.correct / item.total) * 100) : 0;
    item.avg_time = item.total > 0 ? Number((item.total_time / item.total).toFixed(1)) : 0;
    delete item.total_time;
  });

  // Calculate averages and accuracies for categories and sub-topics
  Object.values(categories).forEach((catItem) => {
    catItem.accuracy = catItem.total > 0 ? Math.round((catItem.correct / catItem.total) * 100) : 0;
    catItem.avg_time = catItem.total > 0 ? Number((catItem.total_time / catItem.total).toFixed(1)) : 0;
    delete catItem.total_time;

    Object.values(catItem.topics).forEach((topItem) => {
      topItem.accuracy = topItem.total > 0 ? Math.round((topItem.correct / topItem.total) * 100) : 0;
      topItem.avg_time = topItem.total > 0 ? Number((topItem.total_time / topItem.total).toFixed(1)) : 0;
      delete topItem.total_time;

      Object.values(topItem.patterns).forEach((pItem) => {
        pItem.accuracy = pItem.total > 0 ? Math.round((pItem.correct / pItem.total) * 100) : 0;
        pItem.avg_time = pItem.total > 0 ? Number((pItem.total_time / pItem.total).toFixed(1)) : 0;
        delete pItem.total_time;
      });
    });
  });

  // Calculate averages and accuracies for patterns
  Object.values(patterns).forEach((patItem) => {
    patItem.accuracy = patItem.total > 0 ? Math.round((patItem.correct / patItem.total) * 100) : 0;
    patItem.avg_time = patItem.total > 0 ? Number((patItem.total_time / patItem.total).toFixed(1)) : 0;
    delete patItem.total_time;

    Object.values(patItem.questions || {}).forEach((qItem) => {
      qItem.accuracy = qItem.total_seen > 0 ? Math.round((qItem.correct_count / qItem.total_seen) * 100) : 0;
      qItem.avg_time = qItem.total_seen > 0 ? Number((qItem.total_time / qItem.total_seen).toFixed(1)) : 0;
      delete qItem.total_time;
    });
    patItem.question_list = Object.values(patItem.questions || {}).sort((a, b) => b.total_seen - a.total_seen);
    patItem.unique_questions_count = patItem.question_list.length;
  });

  const question_list = Object.values(questions).sort((a, b) => b.total_seen - a.total_seen);

  return {
    totals: {
      total_attempts,
      total_correct,
      accuracy: overallAccuracy,
      avg_time: overallAvgTime,
      total_unique_questions: question_list.length,
    },
    days,
    categories,
    patterns,
    questions,
    question_list,
  };
}

async function getAdvancedLocalAnalytics() {
  const attempts = await getAllLocalAttempts();
  const sessions = await getAllLocalSessions();
  const basic = await getLocalAnalytics();

  const total_attempts = attempts.length;
  const total_correct = basic.totals.total_correct;
  const overallAccuracy = basic.totals.accuracy;
  const overallAvgTime = basic.totals.avg_time;

  // Keep speed comparisons fair: single-digit and double-digit variants have
  // different natural solve times and must never share one trajectory point.
  const variantLabel = (attempt) => {
    const raw = String(attempt.hybrid_type || "").trim();
    if (raw) return raw.includes("::") ? raw.split("::").pop() : raw;
    return "General / non-variant";
  };
  const variantBuckets = {};
  const variantSessionBuckets = {};
  attempts.forEach((attempt) => {
    const variant = variantLabel(attempt);
    const date = attempt.date || (attempt.timestamp ? new Date(attempt.timestamp).toISOString().slice(0, 10) : getTodayString());
    const dayKey = `${variant}::${date}`;
    if (!variantBuckets[dayKey]) variantBuckets[dayKey] = { variant, date, total: 0, correct: 0, total_time: 0 };
    const day = variantBuckets[dayKey];
    day.total++;
    if (attempt.is_correct) day.correct++;
    day.total_time += Number(attempt.time_taken || 0);

    const sessionId = String(attempt.session_id || `single_${date}`);
    const sessionKey = `${variant}::${sessionId}`;
    if (!variantSessionBuckets[sessionKey]) variantSessionBuckets[sessionKey] = { variant, session_id: sessionId, date, total: 0, correct: 0, total_time: 0, timestamp: 0 };
    const session = variantSessionBuckets[sessionKey];
    session.total++;
    if (attempt.is_correct) session.correct++;
    session.total_time += Number(attempt.time_taken || 0);
    session.timestamp = Math.max(session.timestamp, Number(attempt.timestamp || 0));
    if (String(date) < String(session.date)) session.date = date;
  });
  const variantTrends = {};
  Object.values(variantBuckets).forEach((item) => {
    if (!variantTrends[item.variant]) variantTrends[item.variant] = [];
    variantTrends[item.variant].push({
      date: item.date,
      display_date: item.date.slice(5),
      total: item.total,
      correct: item.correct,
      accuracy: Math.round((item.correct / item.total) * 100),
      avg_time: Number((item.total_time / item.total).toFixed(1)),
    });
  });
  Object.values(variantTrends).forEach((items) => items.sort((a, b) => a.date.localeCompare(b.date)));
  const variantSessions = {};
  Object.values(variantSessionBuckets).forEach((item) => {
    if (!variantSessions[item.variant]) variantSessions[item.variant] = [];
    variantSessions[item.variant].push({
      session_id: item.session_id,
      date: item.date,
      timestamp: item.timestamp,
      total_questions: item.total,
      accuracy: Math.round((item.correct / item.total) * 100),
      avg_time: Number((item.total_time / item.total).toFixed(1)),
    });
  });
  Object.values(variantSessions).forEach((items) => items.sort((a, b) => b.timestamp - a.timestamp));

  // 1. Pacing Time Spectrum
  let lightning = 0;
  let optimal = 0;
  let slow = 0;
  let timeout = 0;

  attempts.forEach((a) => {
    const t = Number(a.time_taken || 0);
    if (a.is_timeout || t >= 15) {
      timeout++;
    } else if (t < 4) {
      lightning++;
    } else if (t <= 10) {
      optimal++;
    } else {
      slow++;
    }
  });

  const pacing = {
    lightning: { count: lightning, pct: total_attempts ? Math.round((lightning / total_attempts) * 100) : 0 },
    optimal: { count: optimal, pct: total_attempts ? Math.round((optimal / total_attempts) * 100) : 0 },
    slow: { count: slow, pct: total_attempts ? Math.round((slow / total_attempts) * 100) : 0 },
    timeout: { count: timeout, pct: total_attempts ? Math.round((timeout / total_attempts) * 100) : 0 },
    timeout_rate: total_attempts ? Number(((timeout / total_attempts) * 100).toFixed(1)) : 0,
  };

  // 2. Cognitive Stamina / Session Fatigue Curve
  const sessionMap = new Map();
  attempts.forEach((a) => {
    const sid = a.session_id || "single";
    if (!sessionMap.has(sid)) sessionMap.set(sid, []);
    sessionMap.get(sid).push(a);
  });

  let earlyCount = 0, earlyCorrect = 0, earlyTime = 0;
  let midCount = 0, midCorrect = 0, midTime = 0;
  let lateCount = 0, lateCorrect = 0, lateTime = 0;

  sessionMap.forEach((sessAttempts) => {
    sessAttempts.sort((x, y) => (x.timestamp || 0) - (y.timestamp || 0));
    sessAttempts.forEach((a, idx) => {
      const isCorr = Boolean(a.is_correct);
      const t = Number(a.time_taken || 0);
      if (idx < 5) {
        earlyCount++;
        if (isCorr) earlyCorrect++;
        earlyTime += t;
      } else if (idx < 10) {
        midCount++;
        if (isCorr) midCorrect++;
        midTime += t;
      } else {
        lateCount++;
        if (isCorr) lateCorrect++;
        lateTime += t;
      }
    });
  });

  const stamina = {
    early: {
      label: "Early Cadence (Q1-5)",
      count: earlyCount,
      accuracy: earlyCount ? Math.round((earlyCorrect / earlyCount) * 100) : 0,
      avg_time: earlyCount ? Number((earlyTime / earlyCount).toFixed(1)) : 0,
    },
    mid: {
      label: "Mid Focus (Q6-10)",
      count: midCount,
      accuracy: midCount ? Math.round((midCorrect / midCount) * 100) : 0,
      avg_time: midCount ? Number((midTime / midCount).toFixed(1)) : 0,
    },
    late: {
      label: "Late Stamina (Q11+)",
      count: lateCount,
      accuracy: lateCount ? Math.round((lateCorrect / lateCount) * 100) : 0,
      avg_time: lateCount ? Number((lateTime / lateCount).toFixed(1)) : 0,
    },
  };

  // 3. Pattern 4-Quadrant Analysis & Recency
  const now = Date.now();
  const patternList = Object.values(basic.patterns || {});
  patternList.forEach((p) => {
    const patAttempts = attempts.filter((a) => Number(a.pattern_id) === Number(p.pattern_id));
    let latestTs = 0;
    patAttempts.forEach((a) => {
      if (a.timestamp && a.timestamp > latestTs) latestTs = a.timestamp;
    });
    p.latest_timestamp = latestTs;
    p.days_since = latestTs ? Math.max(0, Math.floor((now - latestTs) / (1000 * 60 * 60 * 24))) : 99;
  });

  const thresholdTime = overallAvgTime || 15;
  const quadrants = {
    speed_masters: [],
    speed_traps: [],
    rushers: [],
    bottlenecks: [],
  };

  patternList.forEach((p) => {
    if (p.total === 0) return;
    if (p.accuracy >= 75) {
      if (p.avg_time <= thresholdTime) {
        quadrants.speed_masters.push(p);
      } else {
        quadrants.speed_traps.push(p);
      }
    } else {
      if (p.avg_time <= thresholdTime) {
        quadrants.rushers.push(p);
      } else {
        quadrants.bottlenecks.push(p);
      }
    }
  });

  quadrants.speed_masters.sort((a, b) => b.total - a.total);
  quadrants.speed_traps.sort((a, b) => b.avg_time - a.avg_time);
  quadrants.rushers.sort((a, b) => a.accuracy - b.accuracy);
  quadrants.bottlenecks.sort((a, b) => a.accuracy - b.accuracy);

  // 4. Daily Trend Timeline (Past 14 Days)
  const sortedDates = Object.keys(basic.days || {}).sort();
  const trendDays = sortedDates.slice(-14).map((d) => {
    const item = basic.days[d];
    return {
      date: d,
      display_date: d.slice(5),
      total: item.total,
      correct: item.correct,
      accuracy: item.accuracy,
      avg_time: item.avg_time,
      slow_count: item.slow_count,
    };
  });

  // 5. Activity Streak (Consecutive active days)
  let currentStreak = 0;
  const daySet = new Set(sortedDates);
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

  // 6. Mistake Root-Cause Diagnostics
  const mistakeAttempts = attempts.filter((a) => !a.is_correct);
  let rootTimeout = 0;
  let rootCalculation = 0;
  let rootConceptual = 0;

  const parseNumSafe = (val) => {
    if (val === null || val === undefined) return null;
    const s = String(val).trim().replace(/[%$,\s]/g, "");
    const f = parseFloat(s);
    return isNaN(f) ? null : f;
  };

  const classifiedMistakes = mistakeAttempts.map((m) => {
    let cause = "conceptual";
    let label = "Conceptual Trap";
    let badgeClass = "badge-concept";

    if (m.is_timeout || Number(m.time_taken || 0) >= 15) {
      cause = "timeout";
      label = "15s Timeout Panic";
      badgeClass = "badge-timeout";
      rootTimeout++;
    } else {
      const userNum = parseNumSafe(m.typed_answer || m.selected_answer);
      const corrNum = parseNumSafe(m.correct_answer || (m.options && m.options[m.correct_option_index]));
      if (userNum !== null && corrNum !== null && corrNum !== 0) {
        const diffRatio = Math.abs(userNum - corrNum) / Math.abs(corrNum);
        if (diffRatio <= 0.25 || Math.abs(userNum - corrNum) <= 2) {
          cause = "calculation";
          label = "Calculation Near-Miss";
          badgeClass = "badge-calc";
          rootCalculation++;
        } else {
          rootConceptual++;
        }
      } else {
        rootConceptual++;
      }
    }

    return {
      ...m,
      root_cause: cause,
      root_cause_label: label,
      root_cause_badge: badgeClass,
    };
  });

  const mistakeDiagnostics = {
    total: mistakeAttempts.length,
    timeout: { count: rootTimeout, pct: mistakeAttempts.length ? Math.round((rootTimeout / mistakeAttempts.length) * 100) : 0 },
    calculation: { count: rootCalculation, pct: mistakeAttempts.length ? Math.round((rootCalculation / mistakeAttempts.length) * 100) : 0 },
    conceptual: { count: rootConceptual, pct: mistakeAttempts.length ? Math.round((rootConceptual / mistakeAttempts.length) * 100) : 0 },
    mistakes: classifiedMistakes,
  };

  // 7. Executive Readiness Index (0 - 100)
  const accuracyScore = Math.min(35, (overallAccuracy / 100) * 35);

  let speedScore = 15;
  if (total_attempts > 0) {
    if (overallAvgTime <= 5) speedScore = 25;
    else if (overallAvgTime >= 15) speedScore = 5;
    else speedScore = 25 - ((overallAvgTime - 5) / 10) * 20;
  }
  speedScore = Math.max(0, Math.min(25, speedScore));

  const uniquePatterns = patternList.filter((p) => p.total > 0).length;
  const coverageScore = Math.min(20, (uniquePatterns / 15) * 20);

  const recentDays = sortedDates.filter((d) => {
    const diff = (now - new Date(d).getTime()) / (1000 * 60 * 60 * 24);
    return diff <= 14;
  }).length;
  const consistencyScore = Math.min(10, (recentDays / 7) * 10);

  const liquidationRate = total_attempts > 0 ? Math.max(0, total_correct / total_attempts) : 0;
  const liquidationScore = Math.min(10, liquidationRate * 10);

  const readinessScore = total_attempts > 0
    ? Math.round(accuracyScore + speedScore + coverageScore + consistencyScore + liquidationScore)
    : 0;

  let readinessTier = "Foundational Phase";
  let readinessColor = "#f59e0b";
  if (readinessScore >= 90) {
    readinessTier = "Elite Exam Ready (99th %tile)";
    readinessColor = "#10b981";
  } else if (readinessScore >= 75) {
    readinessTier = "Competitive Master";
    readinessColor = "#06b6d4";
  } else if (readinessScore >= 50) {
    readinessTier = "Building Speed & Accuracy";
    readinessColor = "#3b82f6";
  }

  // 8. AI Prescriptions (Prioritized Action Cards)
  const prescriptions = [];

  const worstPattern = quadrants.bottlenecks[0] || quadrants.rushers[0];
  if (worstPattern && worstPattern.total >= 1) {
    prescriptions.push({
      priority: 1,
      type: "bottleneck",
      badge: "🚨 Critical Bottleneck",
      title: worstPattern.pattern_name,
      subtitle: `${worstPattern.category_name} › ${worstPattern.topic_name}`,
      metric: `${worstPattern.accuracy}% Acc • ${worstPattern.avg_time}s Avg`,
      action_label: "⚡ 5-Question Rescue Drill",
      pattern_id: worstPattern.pattern_id,
      description: `You missed ${worstPattern.total - worstPattern.correct} of ${worstPattern.total} attempts. Reinforcing core patterns here provides your fastest score gain.`,
    });
  }

  const speedDragPattern = quadrants.speed_traps[0];
  if (speedDragPattern && speedDragPattern.avg_time > 18) {
    prescriptions.push({
      priority: 2,
      type: "speed",
      badge: "⏳ Speed Optimization",
      title: speedDragPattern.pattern_name,
      subtitle: `${speedDragPattern.category_name} › ${speedDragPattern.topic_name}`,
      metric: `${speedDragPattern.accuracy}% Acc • ${speedDragPattern.avg_time}s Avg (${(speedDragPattern.avg_time - thresholdTime).toFixed(1)}s slow)`,
      action_label: "⚡ Speed Sprint Drill",
      pattern_id: speedDragPattern.pattern_id,
      description: `Concepts are solid (${speedDragPattern.accuracy}% accuracy), but solve time is eating into your exam buffer. Practice numpad speed drills.`,
    });
  }

  const retentionRiskPattern = patternList
    .filter((p) => p.total >= 1 && p.days_since >= 2)
    .sort((a, b) => b.days_since - a.days_since)[0];
  if (retentionRiskPattern) {
    prescriptions.push({
      priority: 3,
      type: "retention",
      badge: "🧠 Retention Decay Warning",
      title: retentionRiskPattern.pattern_name,
      subtitle: `${retentionRiskPattern.category_name} › ${retentionRiskPattern.topic_name}`,
      metric: `Last practiced ${retentionRiskPattern.days_since} days ago`,
      action_label: "⚡ Spaced Refresher Drill",
      pattern_id: retentionRiskPattern.pattern_id,
      description: `Forgetting curve alert: it has been ${retentionRiskPattern.days_since} days since you drilled this pattern. A quick refresher locks in long-term memory.`,
    });
  }

  if (mistakeAttempts.length > 0) {
    prescriptions.push({
      priority: 4,
      type: "mistake",
      badge: "🥊 Mistake Liquidation",
      title: `${mistakeAttempts.length} Questions to Liquidate`,
      subtitle: `${rootTimeout} Timeouts • ${rootCalculation} Calc Near-Misses • ${rootConceptual} Traps`,
      metric: `${mistakeAttempts.length} Recorded Misses`,
      action_label: "⚡ Re-Drill Mistake Book",
      pattern_id: null,
      description: `Liquidating mistakes is the #1 proven driver of test score increases. Practice your unmastered questions now.`,
    });
  }

  return {
    totals: basic.totals,
    readiness: {
      score: readinessScore,
      tier: readinessTier,
      color: readinessColor,
      components: {
        accuracy: Math.round(accuracyScore),
        speed: Math.round(speedScore),
        coverage: Math.round(coverageScore),
        consistency: Math.round(consistencyScore),
        liquidation: Math.round(liquidationScore),
      },
    },
    pacing,
    stamina,
    quadrants,
    trend_days: trendDays,
    variant_trends: variantTrends,
    variant_sessions: variantSessions,
    variants: Object.keys(variantTrends).sort(),
    streak: currentStreak,
    prescriptions,
    mistakes: mistakeDiagnostics,
    days: basic.days,
    categories: basic.categories,
    patterns: basic.patterns,
    questions: basic.questions,
    question_list: basic.question_list,
    sessions,
  };
}

async function exportLocalDataJSON() {
  const attempts = await getAllLocalAttempts();
  const sessions = await getAllLocalSessions();
  const analytics = await getLocalAnalytics();

  const exportPayload = {
    exported_at: new Date().toISOString(),
    version: 1,
    sessions,
    attempts,
    question_summary: analytics.question_list || [],
  };

  const jsonString = JSON.stringify(exportPayload, null, 2);
  if (typeof Blob !== "undefined") {
    const blob = new Blob([jsonString], { type: "application/json;charset=utf-8;" });
    const filename = `aptitude_data_backup_${getBackupTimestamp()}.json`;
    triggerBrowserDownload(blob, filename);
  }

  return exportPayload;
}

async function exportLocalDataCSV() {
  const attempts = await getAllLocalAttempts();

  const headers = [
    "Date",
    "Timestamp",
    "Category",
    "Topic",
    "Pattern_ID",
    "Pattern_Name",
    "Question",
    "Options",
    "User_Answer",
    "Correct_Answer",
    "Is_Correct",
    "Time_Taken_Seconds",
    "Is_Timeout",
    "Is_Skipped",
    "Explanation",
  ];

  const lines = [headers.join(",")];

  attempts.forEach((a) => {
    let userAnswer = a.typed_answer;
    if (!userAnswer && a.selected_answer !== null && a.selected_answer !== undefined) {
      userAnswer = a.selected_answer;
    }
    if (userAnswer === null || userAnswer === undefined) {
      userAnswer = "";
    }

    let correctAnswer = a.correct_answer;
    if (!correctAnswer && Array.isArray(a.options) && a.correct_option_index !== null && a.correct_option_index !== undefined) {
      correctAnswer = a.options[a.correct_option_index];
    }
    if (correctAnswer === null || correctAnswer === undefined) {
      correctAnswer = "";
    }

    const row = [
      escapeCSVField(a.date),
      escapeCSVField(a.timestamp),
      escapeCSVField(a.category_name),
      escapeCSVField(a.topic_name),
      escapeCSVField(a.pattern_id),
      escapeCSVField(a.pattern_name),
      escapeCSVField(a.question_text),
      escapeCSVField(a.options),
      escapeCSVField(userAnswer),
      escapeCSVField(correctAnswer),
      escapeCSVField(a.is_correct ? "TRUE" : "FALSE"),
      escapeCSVField(a.time_taken),
      escapeCSVField(a.is_timeout ? "TRUE" : "FALSE"),
      escapeCSVField(a.is_skipped ? "TRUE" : "FALSE"),
      escapeCSVField(a.explanation),
    ];
    lines.push(row.join(","));
  });

  const csvContent = lines.join("\r\n");
  if (typeof Blob !== "undefined") {
    const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
    const filename = `aptitude_attempts_${getBackupTimestamp()}.csv`;
    triggerBrowserDownload(blob, filename);
  }

  return csvContent;
}

async function exportQuestionStatsCSV() {
  const analytics = await getLocalAnalytics();
  const qList = analytics.question_list || [];

  const headers = [
    "Question",
    "SubTopic_Pattern",
    "Topic",
    "Category",
    "Times_Seen",
    "Times_Correct",
    "Times_Wrong",
    "Timeouts",
    "Accuracy_Pct",
    "Avg_Time_Seconds",
    "Last_Practiced_Date",
  ];

  const lines = [headers.join(",")];

  qList.forEach((q) => {
    const row = [
      escapeCSVField(q.question_text),
      escapeCSVField(q.pattern_name),
      escapeCSVField(q.topic_name),
      escapeCSVField(q.category_name),
      escapeCSVField(q.total_seen),
      escapeCSVField(q.correct_count),
      escapeCSVField(q.wrong_count),
      escapeCSVField(q.timeout_count),
      escapeCSVField(`${q.accuracy}%`),
      escapeCSVField(q.avg_time),
      escapeCSVField(q.last_date),
    ];
    lines.push(row.join(","));
  });

  const csvContent = lines.join("\r\n");
  if (typeof Blob !== "undefined") {
    const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
    const filename = `aptitude_question_frequency_${getBackupTimestamp()}.csv`;
    triggerBrowserDownload(blob, filename);
  }

  return csvContent;
}

async function importLocalDataJSON(jsonStringOrObject) {
  let data;
  if (typeof jsonStringOrObject === "string") {
    data = JSON.parse(jsonStringOrObject);
  } else {
    data = jsonStringOrObject;
  }

  const db = await initLocalDB();
  let attemptsImported = 0;
  let sessionsImported = 0;

  const rawSessions = Array.isArray(data?.sessions) ? data.sessions : [];
  const rawAttempts = Array.isArray(data?.attempts) ? data.attempts : [];

  if (rawSessions.length > 0) {
    await new Promise((resolve, reject) => {
      const tx = db.transaction("sessions", "readwrite");
      const store = tx.objectStore("sessions");

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

  if (rawAttempts.length > 0) {
    await new Promise((resolve, reject) => {
      const tx = db.transaction("attempts", "readwrite");
      const store = tx.objectStore("attempts");

      rawAttempts.forEach((a) => {
        if (a) {
          const toAdd = { ...a };
          delete toAdd.id;
          store.add(toAdd);
          attemptsImported++;
        }
      });

      tx.oncomplete = () => resolve();
      tx.onerror = (e) => reject(e.target.error);
    });
  }

  return { attemptsImported, sessionsImported };
}

const AptitudeLocalDB = {
  initLocalDB,
  recordLocalAttempt,
  recordLocalSession,
  getAllLocalAttempts,
  getAllLocalSessions,
  syncRemoteHistory,
  getLocalAnalytics,
  getAdvancedLocalAnalytics,
  exportLocalDataJSON,
  exportLocalDataCSV,
  exportQuestionStatsCSV,
  importLocalDataJSON,
};

if (typeof window !== "undefined") {
  window.AptitudeLocalDB = AptitudeLocalDB;
  window.initLocalDB = initLocalDB;
  window.recordLocalAttempt = recordLocalAttempt;
  window.recordLocalSession = recordLocalSession;
  window.getAllLocalAttempts = getAllLocalAttempts;
  window.getAllLocalSessions = getAllLocalSessions;
  window.syncRemoteHistory = syncRemoteHistory;
  window.getLocalAnalytics = getLocalAnalytics;
  window.getAdvancedLocalAnalytics = getAdvancedLocalAnalytics;
  window.exportLocalDataJSON = exportLocalDataJSON;
  window.exportLocalDataCSV = exportLocalDataCSV;
  window.exportQuestionStatsCSV = exportQuestionStatsCSV;
  window.importLocalDataJSON = importLocalDataJSON;
}

if (typeof module !== "undefined" && module.exports) {
  module.exports = AptitudeLocalDB;
}
