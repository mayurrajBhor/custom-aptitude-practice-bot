(function () {
  "use strict";

  window.AptitudeGameModes = window.AptitudeGameModes || {};

  const STATE_KEY = "discountShop";
  const PRODUCTS = [
    { name: "Cashmere coat", aisle: "Outerwear", base: 8400, costRate: 0.56 },
    { name: "Italian loafers", aisle: "Footwear", base: 6200, costRate: 0.52 },
    { name: "Leather weekender", aisle: "Travel", base: 9800, costRate: 0.58 },
    { name: "Premium cookware set", aisle: "Home", base: 7600, costRate: 0.5 },
    { name: "Studio headphones", aisle: "Electronics", base: 11400, costRate: 0.61 },
    { name: "Designer lamp", aisle: "Interiors", base: 5400, costRate: 0.48 },
  ];
  const CUSTOMER_TYPES = ["Corporate buyer", "Loyal member", "Walk-in client", "Bulk shopper", "Price watcher"];

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

  function formatMoney(value) {
    const rounded = Math.round(Number(value) || 0);
    if (rounded >= 100000) {
      return "Rs " + (rounded / 100000).toFixed(1) + "L";
    }
    if (rounded >= 1000) {
      return "Rs " + (rounded / 1000).toFixed(1) + "K";
    }
    return "Rs " + rounded;
  }

  function questionText(question) {
    return String(question?.question_text || question?.question || question?.text || question?.prompt || "");
  }

  function hashText(text) {
    let hash = 0;
    for (let index = 0; index < text.length; index += 1) {
      hash = (hash * 31 + text.charCodeAt(index)) >>> 0;
    }
    return hash;
  }

  function extractNumbers(question) {
    const source = [
      questionText(question),
      ...(Array.isArray(question?.options) ? question.options : []),
      question?.answer,
      question?.correct_answer,
    ].join(" ");
    return (source.match(/\d+(?:,\d{2,3})*(?:\.\d+)?/g) || [])
      .map((item) => Number(item.replace(/,/g, "")))
      .filter((item) => Number.isFinite(item) && item > 0);
  }

  function estimateDeal(question, count) {
    const text = questionText(question);
    const seed = hashText(text || String(count));
    const product = PRODUCTS[seed % PRODUCTS.length];
    const numbers = extractNumbers(question);
    const priceCandidate = numbers.find((value) => value >= 300) || product.base + (seed % 1700);
    const discountCandidate = numbers.find((value) => value > 0 && value <= 90) || 10 + (seed % 36);
    const shelfPrice = Math.round(priceCandidate / 50) * 50;
    const markdown = clamp(Math.round(discountCandidate), 5, 75);
    const sellingPrice = Math.round((shelfPrice * (100 - markdown)) / 100);
    const unitCost = Math.round(shelfPrice * product.costRate);
    const grossProfit = Math.max(0, sellingPrice - unitCost);
    const marginRate = sellingPrice > 0 ? Math.round((grossProfit / sellingPrice) * 100) : 0;

    return {
      id: "deal-" + count + "-" + seed,
      product: product.name,
      aisle: product.aisle,
      customer: CUSTOMER_TYPES[seed % CUSTOMER_TYPES.length],
      shelfPrice,
      markdown,
      sellingPrice,
      unitCost,
      grossProfit,
      marginRate,
      pressure: 42 + (seed % 44),
    };
  }

  function ensureState(state) {
    state[STATE_KEY] = state[STATE_KEY] || {};
    const shop = state[STATE_KEY];
    shop.startedAt = shop.startedAt || Date.now();
    shop.revenue = Number.isFinite(shop.revenue) ? shop.revenue : 0;
    shop.margin = Number.isFinite(shop.margin) ? shop.margin : 0;
    shop.customerTrust = Number.isFinite(shop.customerTrust) ? shop.customerTrust : 74;
    shop.dealStreak = Number.isFinite(shop.dealStreak) ? shop.dealStreak : 0;
    shop.bestStreak = Number.isFinite(shop.bestStreak) ? shop.bestStreak : 0;
    shop.transactions = Number.isFinite(shop.transactions) ? shop.transactions : 0;
    shop.correctDeals = Number.isFinite(shop.correctDeals) ? shop.correctDeals : 0;
    shop.missedDeals = Number.isFinite(shop.missedDeals) ? shop.missedDeals : 0;
    shop.queue = Number.isFinite(shop.queue) ? shop.queue : 5;
    shop.currentDeal = shop.currentDeal || estimateDeal(null, 1);
    shop.history = Array.isArray(shop.history) ? shop.history : [];
    return shop;
  }

  function getQuestionIndex(state) {
    return Number(state?.session?.currentIndex || state?.session?.answeredCount || state?.answeredCount || 0) + 1;
  }

  function isCorrectResult(result) {
    return Boolean(
      result?.isCorrect ??
        result?.correct ??
        result?.is_correct ??
        result?.wasCorrect ??
        result?.success
    );
  }

  function renderMetric(label, value, tone) {
    return `
      <div class="game-discount-metric ${tone ? "game-discount-metric-" + tone : ""}">
        <span>${escapeHtml(label)}</span>
        <strong>${escapeHtml(value)}</strong>
      </div>
    `;
  }

  function renderQueue(shop) {
    const count = clamp(shop.queue, 1, 7);
    return Array.from({ length: 7 }, (_, index) => {
      const active = index < count ? " is-active" : "";
      const lead = index === 0 ? " is-lead" : "";
      return `<span class="game-discount-queue-person${active}${lead}"></span>`;
    }).join("");
  }

  function renderFloorLights() {
    return `
      <div class="game-discount-light game-discount-light-left"></div>
      <div class="game-discount-light game-discount-light-mid"></div>
      <div class="game-discount-light game-discount-light-right"></div>
    `;
  }

  window.AptitudeGameModes.discountShop = {
    id: "discountShop",
    title: "Discount Shop Simulator",
    shortTitle: "Discount Shop",
    subtitle: "Run premium retail markdowns while protecting margin, revenue, and customer trust.",
    category: "Percentages",
    recommendedPatternNames: [
      "Percentage change",
      "Discount",
      "Successive discount",
      "Marked price",
      "Profit and loss",
    ],
    targetCount: 12,
    accent: "#c8a45d",

    renderIntro() {
      return `
        <section class="game-discount-intro">
          ${renderFloorLights()}
          <div class="game-discount-intro-copy">
            <p class="game-discount-kicker">Retail operations desk</p>
            <h2>Price the floor without bleeding margin.</h2>
            <p>Every percentage question becomes a markdown decision. Correct calls move inventory, preserve customer trust, and build a clean deal streak.</p>
          </div>
          <div class="game-discount-price-wall" aria-hidden="true">
            <div class="game-discount-tag game-discount-tag-primary">
              <span>Member Event</span>
              <strong>35% OFF</strong>
              <small>margin hold</small>
            </div>
            <div class="game-discount-tag">
              <span>Floor Signal</span>
              <strong>Rs 7.8K</strong>
              <small>ticket value</small>
            </div>
            <div class="game-discount-radar">
              <span></span>
              <b>Margin radar</b>
            </div>
          </div>
        </section>
      `;
    },

    renderHud(state) {
      const shop = ensureState(state);
      const trustTone = shop.customerTrust >= 70 ? "good" : shop.customerTrust >= 45 ? "warn" : "bad";
      return `
        <section class="game-discount-hud">
          ${renderMetric("Revenue", formatMoney(shop.revenue), "money")}
          ${renderMetric("Gross Margin", formatMoney(shop.margin), "margin")}
          ${renderMetric("Trust", Math.round(shop.customerTrust) + "%", trustTone)}
          ${renderMetric("Deal Streak", shop.dealStreak, shop.dealStreak > 2 ? "good" : "")}
        </section>
      `;
    },

    renderScene(state) {
      const shop = ensureState(state);
      const deal = shop.currentDeal;
      const trust = clamp(shop.customerTrust, 0, 100);
      const marginHealth = clamp(36 + deal.marginRate, 0, 100);
      const queueLoad = clamp(shop.queue * 13, 0, 100);
      const queueDot = Math.round(queueLoad * 0.62);

      return `
        <section class="game-discount-scene">
          ${renderFloorLights()}
          <div class="game-discount-dashboard">
            <div class="game-discount-panel game-discount-deal-board">
              <div class="game-discount-panel-head">
                <span>Live Markdown</span>
                <strong>${escapeHtml(deal.aisle)}</strong>
              </div>
              <div class="game-discount-product-row">
                <div>
                  <p>${escapeHtml(deal.product)}</p>
                  <span>${escapeHtml(deal.customer)} at register ${Math.max(1, shop.queue - 1)}</span>
                </div>
                <div class="game-discount-price-tag">
                  <span>Ticket</span>
                  <strong>${formatMoney(deal.shelfPrice)}</strong>
                </div>
              </div>
              <div class="game-discount-tag-strip">
                <div><span>Markdown</span><strong>${deal.markdown}%</strong></div>
                <div><span>Sale Price</span><strong>${formatMoney(deal.sellingPrice)}</strong></div>
                <div><span>Est. Margin</span><strong>${deal.marginRate}%</strong></div>
              </div>
            </div>

            <div class="game-discount-panel game-discount-radar-panel">
              <div class="game-discount-panel-head">
                <span>Margin Radar</span>
                <strong>${shop.correctDeals}/${Math.max(1, shop.transactions)}</strong>
              </div>
              <div class="game-discount-radar-visual" style="--game-discount-margin:${marginHealth}%; --game-discount-trust:${trust}%; --game-discount-queue:${queueDot}%;">
                <div class="game-discount-radar-ring"></div>
                <div class="game-discount-radar-sweep"></div>
                <span class="game-discount-radar-dot game-discount-radar-dot-margin"></span>
                <span class="game-discount-radar-dot game-discount-radar-dot-trust"></span>
                <span class="game-discount-radar-dot game-discount-radar-dot-queue"></span>
              </div>
              <div class="game-discount-radar-legend">
                <span>Margin</span><span>Trust</span><span>Queue</span>
              </div>
            </div>

            <div class="game-discount-panel game-discount-queue-panel">
              <div class="game-discount-panel-head">
                <span>Customer Queue</span>
                <strong>${shop.queue} waiting</strong>
              </div>
              <div class="game-discount-queue">${renderQueue(shop)}</div>
              <div class="game-discount-trust-track">
                <span style="width:${trust}%"></span>
              </div>
            </div>
          </div>
        </section>
      `;
    },

    onQuestion(question, state) {
      const shop = ensureState(state);
      const nextCount = getQuestionIndex(state);
      shop.currentDeal = estimateDeal(question, nextCount);
      shop.queue = clamp(shop.queue + 1, 3, 7);
      return state;
    },

    onAnswer(result, state) {
      const shop = ensureState(state);
      const correct = isCorrectResult(result);
      const deal = shop.currentDeal || estimateDeal(result?.question, shop.transactions + 1);
      shop.transactions += 1;

      if (correct) {
        shop.correctDeals += 1;
        shop.dealStreak += 1;
        shop.bestStreak = Math.max(shop.bestStreak, shop.dealStreak);
        shop.revenue += deal.sellingPrice;
        shop.margin += deal.grossProfit;
        shop.customerTrust = clamp(shop.customerTrust + 4 + Math.min(shop.dealStreak, 4), 0, 100);
        shop.queue = clamp(shop.queue - 1, 1, 7);
      } else {
        shop.missedDeals += 1;
        shop.dealStreak = 0;
        shop.revenue += Math.round(deal.sellingPrice * 0.35);
        shop.margin = Math.max(0, shop.margin - Math.round(deal.unitCost * 0.08));
        shop.customerTrust = clamp(shop.customerTrust - 9, 0, 100);
        shop.queue = clamp(shop.queue + 1, 1, 7);
      }

      shop.history.unshift({
        product: deal.product,
        correct,
        revenue: correct ? deal.sellingPrice : Math.round(deal.sellingPrice * 0.35),
        margin: correct ? deal.grossProfit : -Math.round(deal.unitCost * 0.08),
      });
      shop.history = shop.history.slice(0, 5);
      return state;
    },

    onStop(state) {
      const shop = ensureState(state);
      shop.stoppedAt = Date.now();
      return state;
    },

    getSummaryLines(summary, state) {
      const shop = ensureState(state);
      const accuracy = shop.transactions
        ? Math.round((shop.correctDeals / shop.transactions) * 100)
        : Math.round(Number(summary?.accuracy || 0));
      return [
        "Retail revenue booked: " + formatMoney(shop.revenue),
        "Gross margin protected: " + formatMoney(shop.margin),
        "Customer trust closed at: " + Math.round(shop.customerTrust) + "%",
        "Best deal streak: " + shop.bestStreak,
        "Markdown decision accuracy: " + accuracy + "%",
      ];
    },
  };
})();
