/**
 * english_app.js
 * 
 * Comprehensive English & GMAT Verbal Reasoning Application Module
 * 
 * Features:
 * 1. Question Runner:
 *    - Split-pane Reading Comprehension (passage left with [P1] indicators, question right, collapsible, scroll position preserved, mobile drawer)
 *    - Critical Reasoning (stimulus card with premise & conclusion demarcation, question stem separated)
 *    - 5 Options (A-E) with Choice Elimination (cross-off strikethrough, gray-out, keyboard shortcuts 1-5, A-E, E+1..5)
 *    - Timers (Untimed, Timed Drill countdown, 45-min Simulation with 5-min warning, RC Dual Reading vs Solving Timer)
 *    - Interaction Metrics (time_spent_reading_passage, time_spent_on_question, time_before_first_interaction, time_after_eliminating_choices, is_timeout)
 *    - Action buttons (Bookmark, Mark for Review / Skip, Submit validation)
 * 2. Detailed Answer Review:
 *    - Correct/Incorrect/Skipped status banner
 *    - User choice vs Correct choice comparison
 *    - Pacing Feedback Badges (⚡ Too fast, 🎯 On pace, ⏳ Too slow)
 *    - Detailed Reasoning Paths (CR: Premise, Conclusion, Assumption, Logical Gap, Why Correct, Trap Types; RC: Evidence citation, Support, Traps; Grammar: Rule, Why it works, Traps, Examples, Memory Rule; Vocab: Definition, Context, Examples, Mnemonic)
 *    - Interactive 14 Error Categories Classification Dropdown with instant IndexedDB persistence
 * 3. Foundation Vocabulary Spaced Repetition UI:
 *    - Interactive 3D flip card (Space or click to flip)
 *    - 4 SRS Rating buttons (Again: 1d, Review: 3d, Good: 7d, Mastered: 14d+)
 * 4. Modular Entry Points for Dashboard Integration
 */

(function () {
  "use strict";

  // If already initialized, preserve reference
  window.EnglishApp = window.EnglishApp || {};

  // Standard 14 GMAT Error Categories
  const ERROR_CATEGORIES = [
    "Misread question",
    "Misread passage",
    "Missed conclusion",
    "Extreme answer",
    "Out of scope",
    "Confused necessary/sufficient",
    "Reversed causality",
    "Faulty comparison",
    "Ignored key qualifier",
    "Fell for tempting trap choice",
    "Timing issue / Rushed",
    "Second-guessing correct intuition",
    "Careless mistake",
    "Unknown / Conceptual gap",
  ];

  function formatTime(seconds) {
    const s = Math.max(0, Math.floor(seconds || 0));
    const mins = Math.floor(s / 60);
    const secs = s % 60;
    return `${String(mins).padStart(2, "0")}:${String(secs).padStart(2, "0")}`;
  }

  // =========================================================================
  // Question Bank Dataset
  // =========================================================================
  const BUILTIN_QUESTIONS = [
    {
      id: "cr_101",
      section: "gmat_verbal",
      subsection: "Critical Reasoning",
      type: "cr",
      question_type: "Weaken",
      target_time: 120,
      stimulus: {
        raw: "Over the past two years, Zenith Fitness chain increased membership dues by 25 percent at all of its downtown locations. During the same period, total revenues at these locations rose by 30 percent. The management concluded that downtown patrons are relatively insensitive to price increases and recommended an additional 20 percent price hike for the coming year.",
        premise: "Dues increased 25% downtown and total revenues rose by 30% over the past two years.",
        conclusion: "Downtown patrons are relatively price-insensitive and an additional 20% price hike will further boost revenue.",
      },
      stem: "Which of the following, if true, most seriously weakens the management's conclusion?",
      options: [
        "A competing budget gym chain recently announced plans to open three new gyms in suburban areas outside the downtown core.",
        "Downtown locations also introduced premium personal training packages two years ago, and sales of those packages accounted for over half of total revenue growth.",
        "Surveys show that downtown gym patrons value convenience and updated cardio equipment more than gym cleanliness.",
        "The cost of leasing commercial real estate in the downtown core has increased by 15 percent over the past two years.",
        "Zenith's suburban gym locations experienced an 8 percent decline in membership following a 10 percent price increase.",
      ],
      correct_option_index: 1,
      correct_letter: "B",
      reasoning: {
        premise: "Over 2 years, dues rose 25% and total revenue rose 30% downtown.",
        conclusion: "Patrons are price-insensitive, so another 20% hike will succeed.",
        assumption: "The revenue increase was driven by the membership dues price hike, not other revenue streams.",
        logical_gap: "Alternative explanation for revenue growth besides membership price elasticity.",
        why_correct: "Option B provides an alternative explanation: premium personal training packages accounted for more than half of the revenue growth. This directly weakens the conclusion that membership fee increases drove revenue and that gym members are insensitive to dues.",
        choices_breakdown: [
          { letter: "A", trap: "Out of Scope", text: "Competitors opening gyms in suburban areas does not affect downtown price sensitivity." },
          { letter: "B", trap: "Correct Explanation", text: "Identifies a confounding factor (personal training sales) that explains the revenue surge." },
          { letter: "C", trap: "Irrelevant Factor", text: "Customer preferences for equipment vs cleanliness does not address price elasticity." },
          { letter: "D", trap: "Profit vs Revenue Confusion", text: "Real estate costs impact profitability, but the argument's premise and conclusion are strictly about revenue." },
          { letter: "E", trap: "Faulty Comparison / Scope Shift", text: "Suburban branch behavior does not invalidate observed revenue patterns downtown." },
        ],
      },
    },
    {
      id: "rc_201",
      section: "gmat_verbal",
      subsection: "Reading Comprehension",
      type: "rc",
      question_type: "Primary Purpose",
      target_time: 150,
      passage: {
        id: "rc_pass_1",
        title: "Behavioral Economics and Consumer Choice Architecture",
        topic: "Economics & Psychology",
        word_count: 285,
        paragraphs: [
          "Classical economic theory posits that consumers act as rational utility maximizers, possessing both the cognitive bandwidth and the inclination to weigh all available options prior to making a purchasing decision. Under this traditional paradigm, expanding choice sets invariably benefits the consumer by enhancing the probability that an individual will find an option closely matching their idiosyncratic preferences.",
          "However, empirical research in behavioral economics has challenged this foundational assumption. In a series of influential field experiments, researchers demonstrated that when consumers were presented with an extensive array of gourmet jams—twenty-four distinct varieties—curiosity was high, but actual conversions plummeted to a meager three percent. Conversely, when the assortment was constrained to six options, initial foot traffic was slightly lower, yet thirty percent of shoppers completed a purchase.",
          "This phenomenon, termed 'choice overload,' suggests that cognitive friction escalates non-linearly with choice density. As alternatives proliferate, the perceived opportunity cost of forgoing unselected options magnifies anticipatory regret. Modern choice architects therefore advocate for deliberate curation rather than unbridled variety, asserting that cognitive ease often outweighs exhaustive optionality in driving decision satisfaction.",
        ],
      },
      stem: "The primary purpose of the passage is to:",
      options: [
        "Defend classical economic models against recent criticisms by demonstrating that choice expansion maximizes consumer utility.",
        "Introduce the concept of choice overload and explain how empirical evidence challenges a core premise of classical economic theory.",
        "Prove that consumers always prefer limited options regardless of product category or personal expertise.",
        "Argue that retail businesses should immediately eliminate all product variety to reduce operational complexity.",
        "Contrast the methodologies of laboratory economic simulations with naturalistic consumer field trials.",
      ],
      correct_option_index: 1,
      correct_letter: "B",
      reasoning: {
        evidence: "[P1] outlines classical theory of choice expansion; [P2] provides empirical rebuttal (jam study); [P3] synthesizes the theory of 'choice overload' and modern choice architecture.",
        why_correct: "The passage begins with the classical assumption, presents empirical counterevidence in paragraph 2, and concludes in paragraph 3 by framing 'choice overload' as a challenge to classical rationality.",
        choices_breakdown: [
          { letter: "A", trap: "Opposite Meaning", text: "The passage critiques classical models; it does not defend them." },
          { letter: "B", trap: "Correct Scope & Synthesis", text: "Accurately captures the transition from classical theory to behavioral counterevidence and explanation." },
          { letter: "C", trap: "Extreme Language", text: "Claims consumers 'always' prefer limited options 'regardless of category'—unsupported by passage." },
          { letter: "D", trap: "Distortion & Recommendation", text: "Passage advocates curated variety, not total elimination of variety." },
          { letter: "E", trap: "Too Narrow / Minor Detail", text: "Methodological differences between labs and field trials are not the overarching focus." },
        ],
      },
    },
    {
      id: "rc_202",
      section: "gmat_verbal",
      subsection: "Reading Comprehension",
      type: "rc",
      question_type: "Inference",
      target_time: 150,
      passage: {
        id: "rc_pass_1",
        title: "Behavioral Economics and Consumer Choice Architecture",
        topic: "Economics & Psychology",
        word_count: 285,
        paragraphs: [
          "Classical economic theory posits that consumers act as rational utility maximizers, possessing both the cognitive bandwidth and the inclination to weigh all available options prior to making a purchasing decision. Under this traditional paradigm, expanding choice sets invariably benefits the consumer by enhancing the probability that an individual will find an option closely matching their idiosyncratic preferences.",
          "However, empirical research in behavioral economics has challenged this foundational assumption. In a series of influential field experiments, researchers demonstrated that when consumers were presented with an extensive array of gourmet jams—twenty-four distinct varieties—curiosity was high, but actual conversions plummeted to a meager three percent. Conversely, when the assortment was constrained to six options, initial foot traffic was slightly lower, yet thirty percent of shoppers completed a purchase.",
          "This phenomenon, termed 'choice overload,' suggests that cognitive friction escalates non-linearly with choice density. As alternatives proliferate, the perceived opportunity cost of forgoing unselected options magnifies anticipatory regret. Modern choice architects therefore advocate for deliberate curation rather than unbridled variety, asserting that cognitive ease often outweighs exhaustive optionality in driving decision satisfaction.",
        ],
      },
      stem: "It can be inferred from the passage that advocates of modern choice architecture would agree with which of the following statements?",
      options: [
        "Unrestricted product variety always yields optimal consumer decision satisfaction.",
        "Limiting consumer options can increase the likelihood of purchase completion by reducing cognitive friction.",
        "Field experiments produce less reliable data than theoretical classical economic modeling.",
        "Shoppers presented with twenty-four jam varieties experienced less anticipatory regret than shoppers presented with six varieties.",
        "Retail stores should completely eliminate customer curation to maximize organic discovery.",
      ],
      correct_option_index: 1,
      correct_letter: "B",
      reasoning: {
        evidence: "[P3] states 'choice architects therefore advocate for deliberate curation rather than unbridled variety, asserting that cognitive ease often outweighs exhaustive optionality'.",
        why_correct: "Option B directly mirrors the conclusion in [P3] that reducing options alleviates cognitive friction and improves purchase decision satisfaction.",
        choices_breakdown: [
          { letter: "A", trap: "Opposite Meaning", text: "Directly contradicts the passage thesis." },
          { letter: "B", trap: "Valid Text Inference", text: "Accurately supported by paragraphs 2 and 3." },
          { letter: "C", trap: "Unsupported Comparison", text: "No such claim comparing experimental vs theoretical validity is made." },
          { letter: "D", trap: "Reversed Logic", text: "More choices caused higher cognitive friction and greater anticipatory regret." },
          { letter: "E", trap: "Distorted Recommendation", text: "Advocates recommend curation, not the elimination of curation." },
        ],
      },
    },
    {
      id: "sc_301",
      section: "gmat_verbal",
      subsection: "Sentence Correction",
      type: "grammar",
      question_type: "Modifier & Subject-Verb Agreement",
      target_time: 90,
      sentence: {
        prefix: "Having analyzed quarterly earnings reports from dozens of regional suppliers, ",
        underlined: "the CFO determined that rising raw material costs, not declining consumer demand, were responsible for the margin contraction.",
        suffix: "",
      },
      stem: "Which of the following best preserves grammatical accuracy and concise meaning?",
      options: [
        "the CFO determined that rising raw material costs, not declining consumer demand, were responsible for the margin contraction.",
        "it was determined by the CFO that rising raw material costs, and not declining consumer demand, was responsible for the margin contraction.",
        "the margin contraction was determined by the CFO to be caused by rising raw material costs instead of declining consumer demand.",
        "the CFO determined that rising raw material costs, not declining consumer demand, was responsible for the margin contraction.",
        "rising raw material costs, rather than declining consumer demand, were determined by the CFO as responsible for the margin contraction.",
      ],
      correct_option_index: 0,
      correct_letter: "A",
      reasoning: {
        rule: "Subject-Verb Agreement with Intervening Parenthetical Phrase ('not X') & Dangling Modifier",
        why_works: "The introductory participial modifier 'Having analyzed...' must modify the logical agent ('the CFO'). The subject of the noun clause is plural ('rising raw material costs'), and parenthetical phrases set off by 'not' do not alter the number of the subject. Therefore, the plural verb 'were' is grammatically required.",
        choices_breakdown: [
          { letter: "A", trap: "Correct Option", text: "Proper agent modification (CFO) and correct plural agreement ('costs... were')." },
          { letter: "B", trap: "Dangling Modifier & Passive Voice", text: "'Having analyzed...' cannot modify the dummy pronoun 'it'. Also singular 'was' disagrees with plural 'costs'." },
          { letter: "C", trap: "Dangling Modifier", text: "'Having analyzed...' illogically modifies 'margin contraction'." },
          { letter: "D", trap: "Subject-Verb Disagreement", text: "Uses singular 'was' with plural subject 'costs'." },
          { letter: "E", trap: "Dangling Modifier & Idiom", text: "'Having analyzed...' modifies 'costs' instead of the CFO." },
        ],
        simple_example: "The players, not the coach, were eager to begin.",
        gmat_example: "The committee chairs, not the vice president, were responsible for the policy revision.",
        common_trap: "Mistaking the singular noun inside the negative parenthetical phrase ('demand') as the subject.",
        short_memory_rule: "Ignore 'not [noun]' phrases when checking the verb number!",
      },
    },
    {
      id: "vocab_401",
      section: "foundation",
      subsection: "Vocabulary Foundation",
      type: "vocab",
      question_type: "Contextual Vocabulary",
      target_time: 60,
      word_data: {
        word: "Equivocal",
        phonetic: "/ɪˈkwɪv.ə.kəl/",
        part_of_speech: "Adjective",
        definition: "Open to more than one interpretation; deliberately ambiguous or evasive in expression.",
        contextual_meaning: "In executive leadership and critical reasoning, an equivocal statement creates plausible deniability while withholding firm commitment.",
        example: "The spokesperson gave an equivocal response regarding whether layoffs were imminent.",
        business_example: "Due to equivocal forward guidance from the central bank, bond yields fluctuated unpredictably.",
        synonyms: ["Ambiguous", "Evasive", "Enigmatic", "Noncommittal", "Polysemous"],
        antonyms: ["Unequivocal", "Explicit", "Clear-cut", "Definitive", "Unambiguous"],
        memory_aid: "Equi (equal) + vocal (voice) -> Giving equal voice to two opposing interpretations so neither is pinned down.",
      },
      stem: "In the sentence: 'The audit report contained equivocal assessments that neither confirmed nor refuted the whistleblower's allegations,' the word EQUIVOCAL most nearly means:",
      options: [
        "Vehemently critical and openly hostile",
        "Deliberately ambiguous and open to multiple interpretations",
        "Mathematically precise and empirically verified",
        "Irrelevant and outside the jurisdiction of the investigation",
        "Unanimously ratified by all committee members",
      ],
      correct_option_index: 1,
      correct_letter: "B",
      reasoning: {
        definition: "Equivocal means ambiguous, vague, or susceptible to double meanings.",
        why_correct: "The clue 'neither confirmed nor refuted' specifies that the statements could be interpreted in opposing ways, which defines equivocal.",
        choices_breakdown: [
          { letter: "A", trap: "Opposite of noncommittal", text: "Equivocal means non-committal, not hostile." },
          { letter: "B", trap: "Correct Definition", text: "Accurate contextual and literal definition." },
          { letter: "C", trap: "Opposite Meaning", text: "Precise is the antonym of equivocal." },
          { letter: "D", trap: "Scope Error", text: "Confuses vagueness with jurisdictional relevance." },
          { letter: "E", trap: "Audience Confusion", text: "Unanimity relates to consensus, not clarity of wording." },
        ],
      },
    },
  ];

  const BUILTIN_FLASHCARDS = [
    {
      id: "card_1",
      word: "Equivocal",
      phonetic: "/ɪˈkwɪv.ə.kəl/",
      part_of_speech: "Adjective",
      hint: "Prefix equi- (equal) + vocal (voice)...",
      definition: "Deliberately ambiguous, open to multiple interpretations.",
      contextual: "Used to describe corporate press releases or arguments that avoid taking a definitive stance.",
      example: "The CEO's equivocal remarks regarding merger talks left analysts guessing.",
      business_example: "Auditors cautioned against issuing an equivocal revenue forecast ahead of the IPO.",
      synonyms: ["Ambiguous", "Noncommittal", "Evasive", "Oblique"],
      antonyms: ["Unequivocal", "Definitive", "Explicit"],
      mnemonic: "Equi (equal) + Vocal (speaking) = Speaking in two equal voices so you can't be pinned down.",
    },
    {
      id: "card_2",
      word: "Tacit",
      phonetic: "/ˈtæs.ɪt/",
      part_of_speech: "Adjective",
      hint: "Related to 'taciturn' (silent)...",
      definition: "Understood or implied without being stated directly.",
      contextual: "Critical in GMAT assumption questions where an unstated premise is implicitly accepted.",
      example: "The partners operated under a tacit understanding that major acquisitions required consensus.",
      business_example: "The regulator gave tacit approval by declining to open an antitrust inquiry.",
      synonyms: ["Implicit", "Unspoken", "Implied", "Inferred"],
      antonyms: ["Explicit", "Express", "Stated"],
      mnemonic: "Tacit rhymes with 'passed it' without a word — silent agreement.",
    },
    {
      id: "card_3",
      word: "Spurious",
      phonetic: "/ˈspjʊə.ri.əs/",
      part_of_speech: "Adjective",
      hint: "Sounds like 'spur of the moment' fake reasoning...",
      definition: "Not being what it purports to be; false, counterfeit, or logically invalid.",
      contextual: "Vital for CR flaw questions where correlation is falsely conflated with causation (a spurious correlation).",
      example: "Researchers debunked the spurious correlation between ice cream sales and shark attacks.",
      business_example: "The marketing firm defended itself against spurious claims of algorithmic bias.",
      synonyms: ["Bogus", "Fallacious", "Specious", "Unsubstantiated"],
      antonyms: ["Genuine", "Authentic", "Valid", "Substantiated"],
      mnemonic: "Spurious argument contains a 'pure lie' disguised as truth.",
    },
    {
      id: "card_4",
      word: "Salient",
      phonetic: "/ˈseɪ.li.ənt/",
      part_of_speech: "Adjective",
      hint: "Jump out at you (from Latin salire - to leap)...",
      definition: "Most noticeable, prominent, or important.",
      contextual: "In RC passages, isolating the salient points from auxiliary examples determines reading speed.",
      example: "The memo highlighted the three salient risks of entering emerging markets.",
      business_example: "The executive summary distilled sixty pages of technical data into salient takeaways.",
      synonyms: ["Prominent", "Conspicuous", "Crucial", "Focal"],
      antonyms: ["Inconspicuous", "Negligible", "Minor"],
      mnemonic: "Salient points STAND OUT like a sail on the ocean.",
    },
    {
      id: "card_5",
      word: "Mitigate",
      phonetic: "/ˈmɪt.ɪ.ɡeɪt/",
      part_of_speech: "Verb",
      hint: "Make milder or less severe...",
      definition: "To make less severe, serious, or painful.",
      contextual: "Frequent in GMAT CR arguments assessing risk reduction strategies.",
      example: "Hedging contracts mitigated the portfolio's exposure to currency volatility.",
      business_example: "The logistics division instituted dual-sourcing to mitigate supply chain disruption.",
      synonyms: ["Alleviate", "Attenuate", "Moderate", "Palliate"],
      antonyms: ["Exacerbate", "Aggravate", "Intensify"],
      mnemonic: "Miti-gate: Putting a gate in front of the storm to lessen its impact.",
    },
  ];

  // =========================================================================
  // English Overlay Manager
  // Handles the full-screen modal practice overlay (#englishPracticeOverlay),
  // backdrop clicks, body scrolling lock, focus trapping, Escape safety,
  // animated loading card with cancellation, in-overlay completion screen,
  // and in-overlay confirmation modal (replacing browser alerts and confirms).
  // =========================================================================
  const EnglishOverlayManager = {
    overlayEl: null,
    backdropEl: null,
    modalEl: null,
    viewEl: null,
    previousFocusedEl: null,
    _keyHandler: null,
    _cancelCallback: null,

    init: function () {
      this.overlayEl = document.getElementById("englishPracticeOverlay");
      this.backdropEl = document.getElementById("englishPracticeBackdrop");
      this.modalEl = document.getElementById("englishPracticeModal");
      this.viewEl = document.getElementById("englishPracticeView");

      if (this.backdropEl && !this.backdropEl._hasBackdropListener) {
        this.backdropEl.addEventListener("click", () => {
          this.confirmExit();
        });
        this.backdropEl._hasBackdropListener = true;
      }
    },

    open: function () {
      this.init();
      if (!this.overlayEl) return;
      this.previousFocusedEl = document.activeElement;
      this.overlayEl.hidden = false;
      this.overlayEl.style.display = "flex";
      document.body.classList.add("english-overlay-locked");

      this._setupKeyboardTrap();
    },

    close: function () {
      if (this._keyHandler) {
        document.removeEventListener("keydown", this._keyHandler);
        this._keyHandler = null;
      }
      this._cancelCallback = null;

      // Remove any lingering confirm dialogs
      const confirmDialog = document.getElementById("engExitConfirmDialog");
      if (confirmDialog && confirmDialog.parentNode) {
        confirmDialog.parentNode.removeChild(confirmDialog);
      }

      if (this.overlayEl) {
        this.overlayEl.hidden = true;
        this.overlayEl.style.display = "none";
      }
      document.body.classList.remove("english-overlay-locked");

      if (this.viewEl) {
        this.viewEl.innerHTML = "";
      }

      if (this.previousFocusedEl && typeof this.previousFocusedEl.focus === "function") {
        try {
          this.previousFocusedEl.focus();
        } catch (e) {}
      }
    },

    getViewContainer: function () {
      this.init();
      return this.viewEl || document.getElementById("englishQuestionView") || document.querySelector("main");
    },

    showLoading: function (options = {}) {
      this.open();
      const container = this.getViewContainer();
      if (!container) return;

      const title = options.title || "Preparing Practice Session";
      const subtitle = options.subtitle || "Synthesizing and calibrating questions...";
      const section = options.section || "GMAT Verbal Preparation";
      const detailBadge = options.detailBadge || "";
      const onCancel = options.onCancel;
      this._cancelCallback = onCancel;

      container.innerHTML = `
        <div class="english-overlay-loading" role="status" aria-live="polite">
          <div class="english-overlay-loading-card">
            <div class="english-overlay-loading-spinner"></div>
            <span class="english-badge" style="margin-bottom: 8px;">${section}</span>
            <h3 style="margin: 8px 0 4px; font-size: 20px; font-weight: 700; color: #1e3a5f;">${title}</h3>
            <p style="margin: 0 0 16px; color: #64748b; font-size: 14px; max-width: 400px; line-height: 1.5;">${subtitle}</p>
            <div class="english-overlay-loading-progress-track">
              <div class="english-overlay-loading-progress-bar"></div>
            </div>
            ${detailBadge ? `<span style="display: inline-block; font-size: 12px; color: #1e40af; background: #eff6ff; padding: 3px 10px; border-radius: 12px; font-weight: 600; margin-bottom: 16px; border: 1px solid #bfdbfe;">${detailBadge}</span>` : ''}
            <button class="english-btn english-btn-outline" id="engCancelLoadingBtn" type="button" style="margin-top: 6px;">
              ✕ Cancel
            </button>
          </div>
        </div>
      `;

      const cancelBtn = container.querySelector("#engCancelLoadingBtn");
      if (cancelBtn) {
        cancelBtn.addEventListener("click", () => {
          if (typeof onCancel === "function") {
            onCancel();
          }
          this.close();
          window.EnglishApp?.init();
        });
      }
    },

    confirmExit: function (onConfirm) {
      if (document.getElementById("engExitConfirmDialog")) return;

      const dialog = document.createElement("div");
      dialog.id = "engExitConfirmDialog";
      dialog.className = "english-confirm-dialog-overlay";
      dialog.innerHTML = `
        <div class="english-confirm-dialog-card" role="dialog" aria-labelledby="engExitTitle" aria-modal="true">
          <div style="font-size: 36px; margin-bottom: 8px;">⏸️</div>
          <h3 id="engExitTitle" style="margin: 0 0 8px; font-size: 18px; font-weight: 800; color: #1e3a5f;">Exit Practice Session?</h3>
          <p style="margin: 0 0 20px; color: #64748b; font-size: 13.5px; line-height: 1.5;">
            Your answers and progress are saved in your local session. You can resume at any time from the English practice hub.
          </p>
          <div style="display: flex; gap: 12px; justify-content: center; flex-wrap: wrap;">
            <button class="english-btn english-btn-outline" id="engResumePracticeBtn" type="button">
              Resume Practice
            </button>
            <button class="english-btn english-btn-primary" id="engConfirmExitBtn" type="button" style="background: #dc2626; border-color: #dc2626;">
              Exit to Dashboard
            </button>
          </div>
        </div>
      `;

      document.body.appendChild(dialog);

      const resumeBtn = dialog.querySelector("#engResumePracticeBtn");
      const confirmBtn = dialog.querySelector("#engConfirmExitBtn");

      const cleanup = () => {
        if (dialog.parentNode) dialog.parentNode.removeChild(dialog);
      };

      if (resumeBtn) {
        resumeBtn.addEventListener("click", cleanup);
      }
      if (confirmBtn) {
        confirmBtn.addEventListener("click", () => {
          cleanup();
          if (typeof onConfirm === "function") {
            onConfirm();
          } else {
            this.close();
            window.EnglishApp?.init();
          }
        });
      }
    },

    showCompletion: function (session, onDone) {
      this.open();
      const container = this.getViewContainer();
      if (!container) return;

      const total = session.totalQuestions || (session.questions ? session.questions.length : 0);
      const userSelections = session.userSelections || (window.EnglishQuestionRunner ? window.EnglishQuestionRunner.userSelections : {});
      let correct = 0;

      if (session.questions) {
        session.questions.forEach((q, idx) => {
          if (userSelections[idx] === q.correct_option_index) {
            correct++;
          }
        });
      } else if (typeof session.score === "number") {
        correct = session.score;
      }

      const accuracy = total > 0 ? Math.round((correct / total) * 100) : 0;
      const modeLabel = session.isSimulation
        ? "45-Minute GMAT Verbal Simulation"
        : (session.mode === "drill" ? "Verbal Drill" : (session.mode === "vocab_srs" ? "Vocabulary SRS Review" : "Practice Session"));

      container.innerHTML = `
        <div class="english-completion-card" role="dialog" aria-labelledby="engCompTitle" aria-modal="true">
          <div class="english-completion-inner">
            <div class="english-completion-hero">
              <div style="font-size: 40px; margin-bottom: 8px;">🎯</div>
              <span class="english-badge" style="background: rgba(255,255,255,0.2); color: #fff; border: 1px solid rgba(255,255,255,0.4); margin-bottom: 8px;">Session Complete</span>
              <h2 id="engCompTitle" style="margin: 8px 0 4px; font-size: 24px; font-weight: 800; color: #ffffff;">${modeLabel}</h2>
              <p style="margin: 0; opacity: 0.9; font-size: 14px;">Results recorded to your on-device analytics.</p>
            </div>
            <div class="english-completion-stats-grid">
              <div class="english-completion-stat-box">
                <div style="font-size: 26px; font-weight: 800; color: #1e3a5f;">${correct} / ${total}</div>
                <div style="font-size: 12px; color: #64748b; text-transform: uppercase; font-weight: 700; margin-top: 4px;">Score</div>
              </div>
              <div class="english-completion-stat-box">
                <div style="font-size: 26px; font-weight: 800; color: ${accuracy >= 70 ? '#059669' : (accuracy >= 50 ? '#d97706' : '#dc2626')};">${accuracy}%</div>
                <div style="font-size: 12px; color: #64748b; text-transform: uppercase; font-weight: 700; margin-top: 4px;">Accuracy</div>
              </div>
              <div class="english-completion-stat-box">
                <div style="font-size: 26px; font-weight: 800; color: #2563eb;">${session.subsection || "Verbal"}</div>
                <div style="font-size: 12px; color: #64748b; text-transform: uppercase; font-weight: 700; margin-top: 4px;">Focus Area</div>
              </div>
            </div>
            <div class="english-completion-actions">
              <button class="english-btn english-btn-outline" id="engCompReviewBtn" type="button">
                📋 Error Log & Mistakes
              </button>
              <button class="english-btn english-btn-primary" id="engCompDoneBtn" type="button">
                Return to English Hub →
              </button>
            </div>
          </div>
        </div>
      `;

      const reviewBtn = container.querySelector("#engCompReviewBtn");
      const doneBtn = container.querySelector("#engCompDoneBtn");

      if (reviewBtn) {
        reviewBtn.addEventListener("click", () => {
          this.close();
          if (window.EnglishApp) {
            window.EnglishApp.activeSubtab = "progress";
            window.EnglishApp.init();
          }
        });
      }

      if (doneBtn) {
        doneBtn.addEventListener("click", () => {
          this.close();
          if (typeof onDone === "function") {
            onDone();
          } else if (window.EnglishApp) {
            window.EnglishApp.init();
          }
        });
      }
    },

    _setupKeyboardTrap: function () {
      if (this._keyHandler) {
        document.removeEventListener("keydown", this._keyHandler);
      }
      this._keyHandler = (e) => {
        if (e.key === "Escape") {
          const confirmDialog = document.getElementById("engExitConfirmDialog");
          if (confirmDialog) {
            if (confirmDialog.parentNode) confirmDialog.parentNode.removeChild(confirmDialog);
          } else {
            this.confirmExit();
          }
        }
      };
      document.addEventListener("keydown", this._keyHandler);
    }
  };

  // =========================================================================
  // Question Runner Module
  // =========================================================================
  const QuestionRunner = {
    session: null,
    activeQuestion: null,
    currentIndex: 0,
    container: null,

    // Timers & Metrics
    timerInterval: null,
    simInterval: null,
    questionStartTime: 0,
    firstInteractionTime: null,
    lastEliminationTime: null,
    readingTimeSeconds: 0,
    solvingTimeSeconds: 0,
    activeTimerMode: "solving",

    userSelections: {},
    eliminatedChoices: {},
    bookmarks: new Set(),
    markedForReview: new Set(),
    passageScrollPositions: {},

    startSession: function (config) {
      this.clearTimers();
      let rawQuestions = Array.isArray(config.questions) && config.questions.length > 0
        ? config.questions
        : (window.ENGLISH_DATA
            ? (config.isSimulation
                ? (window.ENGLISH_DATA.CR_QUESTIONS || []).slice(0, 10).concat(window.ENGLISH_DATA.RC_QUESTIONS || []).slice(0, 13)
                : (window.ENGLISH_DATA.CR_QUESTIONS || []))
            : BUILTIN_QUESTIONS);

      const questions = rawQuestions.map((item, qIdx) => {
        const q = { ...item };
        q.stem = q.stem || q.question_text || "";
        q.question_text = q.question_text || q.stem || "";
        if (!q.type) {
          if (q.subsection === "critical_reasoning" || q.stimulus) q.type = "cr";
          else if (q.subsection === "reading_comprehension" || q.passage || q.paragraphs) q.type = "rc";
          else if (q.foundation_type === "grammar") q.type = "grammar";
          else if (q.foundation_type === "vocabulary") q.type = "vocab";
          else q.type = "cr";
        }
        if (typeof q.stimulus === "string") {
          q.stimulus = {
            raw: q.stimulus,
            premise: q.premise || "",
            conclusion: q.conclusion || "",
          };
        }
        if (q.paragraphs && !q.passage) {
          q.passage = {
            id: q.passage_id || ("passage_" + qIdx),
            title: q.passage_title || "Reading Comprehension",
            paragraphs: q.paragraphs,
            word_count: q.paragraphs.join(" ").split(/\s+/).length,
          };
        }
        if (!q.reasoning && q.explanation) {
          const breakdown = (q.options || []).map((opt, oIdx) => {
            const exp = (q.option_explanations && q.option_explanations[oIdx]) || "";
            return {
              letter: String.fromCharCode(65 + oIdx),
              trap: oIdx === q.correct_option_index ? "Correct Option" : (q.trap_type || "Eliminated Option"),
              text: exp || (oIdx === q.correct_option_index ? q.explanation : "Incorrect answer choice.")
            };
          });
          q.reasoning = {
            premise: q.premise || "",
            conclusion: q.conclusion || "",
            assumption: q.assumption || "",
            logical_gap: q.logical_gap || "",
            why_correct: q.explanation,
            choices_breakdown: breakdown,
            grammar_rule: q.grammar_rule || "",
            why_it_works: q.why_it_works || "",
            simple_example: q.simple_example || "",
            gmat_example: q.gmat_example || "",
            common_trap: q.common_trap || "",
            memory_rule: q.memory_rule || "",
          };
        }
        return q;
      });

      this.session = {
        id: config.sessionId || "eng_session_" + Date.now(),
        mode: config.mode || "untimed",
        section: config.section || "gmat_verbal",
        subsection: config.subsection || "Verbal Reasoning",
        isSimulation: Boolean(config.isSimulation || config.mode === "simulation"),
        timeLimitSeconds: config.timeLimitSeconds || (config.isSimulation ? 45 * 60 : 120),
        simulationRemainingSeconds: config.timeLimitSeconds || (config.isSimulation ? 45 * 60 : 120),
        questions: questions,
        totalQuestions: questions.length,
        onFinish: config.onFinish || null,
        onExit: config.onExit || null,
      };

      this.currentIndex = 0;
      this.userSelections = {};
      this.eliminatedChoices = {};
      this.bookmarks = new Set();
      this.markedForReview = new Set();
      this.passageScrollPositions = {};

      let mountTarget = config.container || (window.EnglishOverlayManager && typeof EnglishOverlayManager.getViewContainer === "function" ? EnglishOverlayManager.getViewContainer() : null);
      if (!mountTarget) {
        mountTarget = document.getElementById("englishQuestionView") ||
                      document.getElementById("questionScreen") ||
                      document.querySelector("main");
      }
      this.container = mountTarget;

      if (this.session.isSimulation) {
        this.startSimulationTimer();
      }

      this.renderQuestion(this.currentIndex);
    },

    renderQuestion: function (index) {
      if (!this.session || !this.container) return;
      if (index < 0 || index >= this.session.questions.length) {
        this.finishSession();
        return;
      }

      this.currentIndex = index;
      const q = this.session.questions[index];
      this.activeQuestion = q;

      this.questionStartTime = Date.now();
      this.firstInteractionTime = null;
      this.lastEliminationTime = null;
      this.readingTimeSeconds = 0;
      this.solvingTimeSeconds = 0;
      this.activeTimerMode = q.type === "rc" ? "reading" : "solving";

      if (!this.eliminatedChoices[index]) {
        this.eliminatedChoices[index] = new Set();
      }

      if (!this.session.isSimulation) {
        this.startQuestionTimer();
      }

      this.container.innerHTML = this.buildQuestionHTML(q, index);
      this.container.hidden = false;

      // Restore scroll position if same passage was previously scrolled
      if (q.passage && q.passage.id && this.passageScrollPositions[q.passage.id]) {
        const pBody = this.container.querySelector(".rc-passage-body");
        if (pBody) {
          pBody.scrollTop = this.passageScrollPositions[q.passage.id];
        }
      }

      this.attachEventListeners(q, index);
    },

    buildQuestionHTML: function (q, index) {
      const modeLabels = {
        simulation: "45-min Simulation",
        drill: "Timed Drill",
        untimed: "Untimed Learn Mode",
        diagnostic: "Diagnostic",
      };
      const modeLabel = modeLabels[this.session.mode] || "Practice Mode";
      const sectionTitle = q.section === "foundation" ? "English Foundation" : "GMAT Verbal Reasoning";
      const isBookmarked = this.bookmarks.has(index);
      const isMarkedReview = this.markedForReview.has(index);
      const selectedIndex = this.userSelections[index];
      const elimSet = this.eliminatedChoices[index] || new Set();

      const progressPercent = Math.round(((index + 1) / this.session.totalQuestions) * 100);

      // Top HUD
      let topHudHtml = `
        <header class="english-hud-bar" role="region" aria-label="Practice status">
          <div class="english-hud-left">
            <span class="english-badge ${q.section === 'foundation' ? 'foundation-badge' : ''}">
              <span>${sectionTitle}</span>
            </span>
            <span class="english-mode-pill ${this.session.mode}">
              <span>${modeLabel}</span>
            </span>
            ${(q.is_ai_generated || this.session.is_ai_generated) ? `
              <span class="english-badge" style="background: #e0e7ff; color: #3730a3; border: 1px solid #c7d2fe; display: inline-flex; align-items: center; gap: 4px;" title="Dynamically generated with adaptive difficulty">
                <span>🤖 Level ${q.difficulty || 3}/5</span>
              </span>
            ` : ''}
            <div class="english-progress-cluster">
              <span class="english-q-counter">Q${index + 1} of ${this.session.totalQuestions}</span>
              <div class="english-progress-track" title="${progressPercent}% complete">
                <div class="english-progress-fill" style="width: ${progressPercent}%;"></div>
              </div>
            </div>
          </div>

          <div class="english-hud-right">
            ${this.renderTimerDisplay(q)}
            
            <button class="english-hud-btn ${isBookmarked ? 'is-bookmarked' : ''}" id="engBookmarkBtn" type="button" aria-pressed="${isBookmarked}" title="Bookmark (B)">
              <span class="hud-btn-star" aria-hidden="true">${isBookmarked ? '★' : '☆'}</span>
              <span>${isBookmarked ? 'Bookmarked' : 'Bookmark'}</span>
            </button>

            <button class="english-hud-btn" id="engReviewFlagBtn" type="button" title="Mark for review (M)">
              <span aria-hidden="true">${isMarkedReview ? '🏳️' : '⚐'}</span>
              <span>${isMarkedReview ? 'Flagged' : 'Review'}</span>
            </button>
          </div>
        </header>
      `;

      // 5-min simulation warning
      const simWarningHtml = `
        <div class="english-sim-alert" id="engSimAlert" style="display: none;" role="alert">
          <span aria-hidden="true">⚠️</span>
          <span>5 minutes remaining! Pace your remaining questions.</span>
        </div>
      `;

      // Content by question type
      let bodyHtml = "";
      if (q.type === "rc" || q.passage) {
        bodyHtml = this.buildRCLayoutHTML(q, selectedIndex, elimSet);
      } else if (q.type === "cr" || q.stimulus) {
        bodyHtml = this.buildCRLayoutHTML(q, selectedIndex, elimSet);
      } else if (q.type === "grammar" || q.sentence) {
        bodyHtml = this.buildGrammarLayoutHTML(q, selectedIndex, elimSet);
      } else {
        bodyHtml = this.buildGeneralLayoutHTML(q, selectedIndex, elimSet);
      }

      // Action Bar
      const submitDisabled = selectedIndex === undefined || selectedIndex === null ? "disabled" : "";
      const isLastQuestion = index === this.session.totalQuestions - 1;
      const submitLabel = this.session.isSimulation
        ? (isLastQuestion ? "Finish Verbal Section" : "Next Question →")
        : "Submit Answer";

      const actionBarHtml = `
        <footer class="english-action-bar">
          <div class="english-action-left">
            <button class="english-btn english-btn-ghost" id="engExitBtn" type="button">
              <span>✕ Dashboard</span>
            </button>
            <div class="keyboard-shortcuts-hint" aria-hidden="true">
              <span>Select: <span class="shortcut-kbd">1-5</span> / <span class="shortcut-kbd">A-E</span></span>
              <span>Eliminate: <span class="shortcut-kbd">E + 1-5</span></span>
            </div>
          </div>

          <div class="english-action-right">
            <button class="english-btn english-btn-outline" id="engSkipBtn" type="button">
              <span>Skip / Next ↷</span>
            </button>
            <button class="english-btn english-btn-primary" id="engSubmitBtn" type="button" ${submitDisabled}>
              <span>${submitLabel}</span>
            </button>
          </div>
        </footer>
      `;

      return `
        <div class="english-container" id="englishActiveContainer">
          ${topHudHtml}
          ${simWarningHtml}
          ${bodyHtml}
          ${actionBarHtml}
        </div>
      `;
    },

    renderTimerDisplay: function (q) {
      if (this.session.isSimulation) {
        const timeStr = formatTime(this.session.simulationRemainingSeconds);
        const warnClass = this.session.simulationRemainingSeconds <= 300 ? "warning-timer" : "";
        return `
          <div class="english-timer-block ${warnClass}" id="engSimulationTimer">
            <span class="english-timer-icon" aria-hidden="true">⏱️</span>
            <span id="engTimerText">${timeStr}</span>
          </div>
        `;
      }

      if (q.type === "rc") {
        return `
          <div class="english-dual-timer" id="engRCDualTimer" title="Reading Comprehension Dual Timer">
            <span class="dual-timer-chip is-active reading-active" id="rcReadChip">
              <span>📖 Read:</span>
              <strong id="rcReadTimerText">00:00</strong>
            </span>
            <span class="dual-timer-chip solving-active" id="rcSolveChip">
              <span>⚡ Solve:</span>
              <strong id="rcSolveTimerText">00:00</strong>
            </span>
          </div>
        `;
      }

      const initialText = this.session.mode === "drill" ? formatTime(q.target_time || 120) : "00:00";
      return `
        <div class="english-timer-block" id="engStandardTimer">
          <span class="english-timer-icon" aria-hidden="true">⏳</span>
          <span id="engTimerText">${initialText}</span>
        </div>
      `;
    },

    buildRCLayoutHTML: function (q, selectedIndex, elimSet) {
      const p = q.passage || { title: "Reading Comprehension", paragraphs: [] };
      const paragraphsHtml = (p.paragraphs || []).map((par, i) => {
        return `<p><span class="rc-p-tag" aria-hidden="true">[P${i + 1}]</span>${par}</p>`;
      }).join("");

      return `
        <div class="rc-split-layout" id="rcSplitLayout">
          <article class="rc-passage-panel" id="rcPassagePanel" aria-label="Reading Passage">
            <div class="rc-passage-header">
              <div class="rc-passage-header-left">
                <h2 class="rc-passage-title">${p.title || 'Reading Comprehension'}</h2>
                ${p.word_count ? `<span class="rc-passage-meta">${p.word_count} words</span>` : ''}
              </div>
              <div class="rc-passage-controls">
                <button class="rc-passage-btn" id="rcCollapseToggleBtn" type="button" title="Toggle passage pane width">
                  <span>⤢ Split / Collapse</span>
                </button>
              </div>
            </div>
            <div class="rc-passage-body" tabindex="0" aria-label="Passage text">
              ${paragraphsHtml}
            </div>
            <div class="rc-passage-collapsed-bar" id="rcCollapsedBar" title="Click to expand passage">
              <span>📖 VIEW PASSAGE [P1-P${p.paragraphs ? p.paragraphs.length : 1}]</span>
            </div>
          </article>

          <button class="rc-mobile-drawer-toggle" id="rcMobileDrawerBtn" type="button">
            <span>📖 Read Passage ([P1-P${p.paragraphs ? p.paragraphs.length : 1}])</span>
            <span aria-hidden="true">▲</span>
          </button>

          <div class="rc-drawer-overlay" id="rcDrawerOverlay">
            <div class="rc-drawer-sheet" id="rcDrawerSheet">
              <div class="rc-drawer-handle-bar"></div>
              <div class="rc-passage-header">
                <h3 class="rc-passage-title">${p.title || 'Reading Passage'}</h3>
                <button class="rc-passage-btn" id="rcCloseDrawerBtn" type="button">Close ✕</button>
              </div>
              <div class="rc-passage-body">
                ${paragraphsHtml}
              </div>
            </div>
          </div>

          <section class="rc-question-panel">
            <div class="english-question-stem-card">
              <div class="stem-kicker">
                <span>${q.question_type || 'Reading Comprehension Question'}</span>
              </div>
              <h3 class="english-question-stem-text">${q.stem}</h3>
            </div>
            ${this.buildChoicesListHTML(q.options, selectedIndex, elimSet)}
          </section>
        </div>
      `;
    },

    buildCRLayoutHTML: function (q, selectedIndex, elimSet) {
      const stimulus = q.stimulus || { raw: "" };
      let stimulusTextHtml = "";

      if (stimulus.premise && stimulus.conclusion) {
        stimulusTextHtml = `
          <div class="cr-stimulus-text">
            <span class="cr-premise" title="Premise">${stimulus.premise}</span>
            <span class="cr-conclusion" title="Conclusion">${stimulus.conclusion}</span>
          </div>
          <div class="cr-demarcation-guide" aria-hidden="true">
            <span class="cr-guide-item"><span class="cr-guide-dot premise-dot"></span> Premise</span>
            <span class="cr-guide-item"><span class="cr-guide-dot conclusion-dot"></span> Conclusion</span>
          </div>
        `;
      } else {
        stimulusTextHtml = `<div class="cr-stimulus-text">${stimulus.raw || stimulus}</div>`;
      }

      return `
        <div class="cr-container">
          <section class="cr-stimulus-card" aria-label="Argument Stimulus">
            <div class="cr-stimulus-header">
              <span class="cr-stimulus-label">
                <span aria-hidden="true">🏛️</span> Argument Stimulus
              </span>
              <span class="cr-type-badge">${q.question_type || 'Critical Reasoning'}</span>
            </div>
            ${stimulusTextHtml}
          </section>

          <div class="english-question-stem-card">
            <div class="stem-kicker">Question Prompt</div>
            <h3 class="english-question-stem-text">${q.stem}</h3>
          </div>

          ${this.buildChoicesListHTML(q.options, selectedIndex, elimSet)}
        </div>
      `;
    },

    buildGrammarLayoutHTML: function (q, selectedIndex, elimSet) {
      const sent = q.sentence || { prefix: "", underlined: q.stem || "", suffix: "" };
      return `
        <div class="cr-container">
          <div class="grammar-sentence-box" aria-label="Sentence Underline Analysis">
            <span>${sent.prefix || ''}</span>
            <span class="grammar-underlined">${sent.underlined || ''}</span>
            <span>${sent.suffix || ''}</span>
          </div>

          <div class="english-question-stem-card">
            <div class="stem-kicker">${q.question_type || 'Sentence Correction'}</div>
            <h3 class="english-question-stem-text">${q.stem || 'Choose the option that best expresses the idea with grammatical accuracy.'}</h3>
          </div>

          ${this.buildChoicesListHTML(q.options, selectedIndex, elimSet)}
        </div>
      `;
    },

    buildGeneralLayoutHTML: function (q, selectedIndex, elimSet) {
      return `
        <div class="cr-container">
          <div class="english-question-stem-card">
            <div class="stem-kicker">${q.question_type || 'Question Prompt'}</div>
            <h3 class="english-question-stem-text">${q.stem}</h3>
          </div>
          ${this.buildChoicesListHTML(q.options, selectedIndex, elimSet)}
        </div>
      `;
    },

    buildChoicesListHTML: function (options, selectedIndex, elimSet) {
      const letters = ["A", "B", "C", "D", "E"];
      const rowsHtml = options.map((optText, idx) => {
        const letter = letters[idx] || String.fromCharCode(65 + idx);
        const isSelected = selectedIndex === idx;
        const isEliminated = elimSet.has(idx);

        return `
          <div class="english-choice-row ${isEliminated ? 'is-eliminated' : ''}" data-choice-row="${idx}">
            <button class="english-choice-btn ${isSelected ? 'is-selected' : ''}" 
                    type="button" 
                    data-choice-idx="${idx}"
                    aria-pressed="${isSelected}"
                    ${isEliminated ? 'aria-disabled="true"' : ''}>
              <span class="english-choice-letter" aria-hidden="true">${letter}</span>
              <span class="english-choice-text">${optText}</span>
            </button>
            <button class="english-choice-elim-btn" 
                    type="button" 
                    data-elim-idx="${idx}"
                    title="${isEliminated ? 'Restore option ' + letter : 'Eliminate option ' + letter + ' (E+' + (idx + 1) + ')'}"
                    aria-label="${isEliminated ? 'Restore option ' + letter : 'Eliminate option ' + letter}">
              <span class="elim-icon" aria-hidden="true">${isEliminated ? '↩' : 'S̶'}</span>
            </button>
          </div>
        `;
      }).join("");

      return `<div class="english-choices-list" role="radiogroup" aria-label="Answer options">${rowsHtml}</div>`;
    },

    attachEventListeners: function (q, index) {
      const container = this.container;
      const self = this;

      function recordInteraction() {
        if (!self.firstInteractionTime) {
          self.firstInteractionTime = Date.now();
        }
      }

      // Choice selection
      container.querySelectorAll(".english-choice-btn").forEach((btn) => {
        btn.addEventListener("click", function () {
          const idx = parseInt(this.getAttribute("data-choice-idx"), 10);
          const elimSet = self.eliminatedChoices[index] || new Set();
          if (elimSet.has(idx)) return;

          recordInteraction();
          self.userSelections[index] = idx;
          self.activeTimerMode = "solving";

          container.querySelectorAll(".english-choice-btn").forEach((b) => {
            b.classList.remove("is-selected");
            b.setAttribute("aria-pressed", "false");
          });
          this.classList.add("is-selected");
          this.setAttribute("aria-pressed", "true");

          const submitBtn = container.querySelector("#engSubmitBtn");
          if (submitBtn) submitBtn.disabled = false;
        });
      });

      // Elimination
      container.querySelectorAll(".english-choice-elim-btn").forEach((elimBtn) => {
        elimBtn.addEventListener("click", function (e) {
          e.stopPropagation();
          recordInteraction();
          const idx = parseInt(this.getAttribute("data-elim-idx"), 10);
          const elimSet = self.eliminatedChoices[index];
          const row = container.querySelector(`.english-choice-row[data-choice-row="${idx}"]`);
          const mainBtn = row ? row.querySelector(".english-choice-btn") : null;

          if (elimSet.has(idx)) {
            elimSet.delete(idx);
            if (row) row.classList.remove("is-eliminated");
            if (mainBtn) mainBtn.removeAttribute("aria-disabled");
            this.querySelector(".elim-icon").textContent = "S̶";
          } else {
            elimSet.add(idx);
            if (row) row.classList.add("is-eliminated");
            if (mainBtn) {
              mainBtn.setAttribute("aria-disabled", "true");
              mainBtn.classList.remove("is-selected");
            }
            this.querySelector(".elim-icon").textContent = "↩";

            if (self.userSelections[index] === idx) {
              delete self.userSelections[index];
              const submitBtn = container.querySelector("#engSubmitBtn");
              if (submitBtn) submitBtn.disabled = true;
            }
          }

          self.lastEliminationTime = Date.now();
        });
      });

      // Bookmark
      const bookmarkBtn = container.querySelector("#engBookmarkBtn");
      if (bookmarkBtn) {
        bookmarkBtn.addEventListener("click", () => {
          recordInteraction();
          if (self.bookmarks.has(index)) {
            self.bookmarks.delete(index);
            bookmarkBtn.classList.remove("is-bookmarked");
            bookmarkBtn.setAttribute("aria-pressed", "false");
            bookmarkBtn.querySelector("span:last-child").textContent = "Bookmark";
            bookmarkBtn.querySelector(".hud-btn-star").textContent = "☆";
          } else {
            self.bookmarks.add(index);
            bookmarkBtn.classList.add("is-bookmarked");
            bookmarkBtn.setAttribute("aria-pressed", "true");
            bookmarkBtn.querySelector("span:last-child").textContent = "Bookmarked";
            bookmarkBtn.querySelector(".hud-btn-star").textContent = "★";
          }
        });
      }

      // Mark for Review
      const reviewFlagBtn = container.querySelector("#engReviewFlagBtn");
      if (reviewFlagBtn) {
        reviewFlagBtn.addEventListener("click", () => {
          recordInteraction();
          if (self.markedForReview.has(index)) {
            self.markedForReview.delete(index);
            reviewFlagBtn.querySelector("span:last-child").textContent = "Review";
          } else {
            self.markedForReview.add(index);
            reviewFlagBtn.querySelector("span:last-child").textContent = "Flagged";
          }
        });
      }

      // Submit
      const submitBtn = container.querySelector("#engSubmitBtn");
      if (submitBtn) {
        submitBtn.addEventListener("click", () => self.submitAnswer(false));
      }

      // Skip
      const skipBtn = container.querySelector("#engSkipBtn");
      if (skipBtn) {
        skipBtn.addEventListener("click", () => self.skipQuestion());
      }

      // Exit
      const exitBtn = container.querySelector("#engExitBtn");
      if (exitBtn) {
        exitBtn.addEventListener("click", () => {
          if (window.EnglishOverlayManager && typeof EnglishOverlayManager.confirmExit === "function") {
            EnglishOverlayManager.confirmExit(() => {
              self.exitSession();
            });
          } else {
            self.exitSession();
          }
        });
      }

      // RC Events
      if (q.type === "rc" && q.passage) {
        const passageBody = container.querySelector(".rc-passage-body");
        if (passageBody) {
          passageBody.addEventListener("mouseenter", () => { self.activeTimerMode = "reading"; });
          passageBody.addEventListener("focus", () => { self.activeTimerMode = "reading"; });
          passageBody.addEventListener("scroll", () => {
            recordInteraction();
            self.activeTimerMode = "reading";
            if (q.passage.id) {
              self.passageScrollPositions[q.passage.id] = passageBody.scrollTop;
            }
          });
        }

        const collapseBtn = container.querySelector("#rcCollapseToggleBtn");
        const splitLayout = container.querySelector("#rcSplitLayout");
        const collapsedBar = container.querySelector("#rcCollapsedBar");

        if (collapseBtn && splitLayout) {
          collapseBtn.addEventListener("click", () => {
            splitLayout.classList.toggle("passage-collapsed");
          });
        }
        if (collapsedBar && splitLayout) {
          collapsedBar.addEventListener("click", () => {
            splitLayout.classList.remove("passage-collapsed");
          });
        }

        const drawerBtn = container.querySelector("#rcMobileDrawerBtn");
        const overlay = container.querySelector("#rcDrawerOverlay");
        const sheet = container.querySelector("#rcDrawerSheet");
        const closeDrawerBtn = container.querySelector("#rcCloseDrawerBtn");

        if (drawerBtn && overlay && sheet) {
          drawerBtn.addEventListener("click", () => {
            overlay.classList.add("is-open");
            sheet.classList.add("is-open");
          });
          const closeDrawer = () => {
            overlay.classList.remove("is-open");
            sheet.classList.remove("is-open");
          };
          if (closeDrawerBtn) closeDrawerBtn.addEventListener("click", closeDrawer);
          overlay.addEventListener("click", (e) => {
            if (e.target === overlay) closeDrawer();
          });
        }
      }

      this.attachKeyboardShortcuts();
    },

    attachKeyboardShortcuts: function () {
      const self = this;
      if (this._keyHandler) {
        document.removeEventListener("keydown", this._keyHandler);
      }

      let eliminationKeyActive = false;
      let eliminationTimer = null;

      this._keyHandler = function (e) {
        if (["INPUT", "TEXTAREA", "SELECT"].includes(document.activeElement.tagName)) return;

        const key = e.key.toLowerCase();
        const index = self.currentIndex;
        const elimSet = self.eliminatedChoices[index] || new Set();

        if (key === "e") {
          eliminationKeyActive = true;
          clearTimeout(eliminationTimer);
          eliminationTimer = setTimeout(() => { eliminationKeyActive = false; }, 2000);
          return;
        }

        const keyMap = { "1": 0, "2": 1, "3": 2, "4": 3, "5": 4, "a": 0, "b": 1, "c": 2, "d": 3, "e": 4 };
        if (keyMap.hasOwnProperty(key)) {
          const optIdx = keyMap[key];

          if (eliminationKeyActive) {
            eliminationKeyActive = false;
            clearTimeout(eliminationTimer);
            const elimBtn = self.container.querySelector(`.english-choice-elim-btn[data-elim-idx="${optIdx}"]`);
            if (elimBtn) elimBtn.click();
            return;
          }

          if (!elimSet.has(optIdx)) {
            const optBtn = self.container.querySelector(`.english-choice-btn[data-choice-idx="${optIdx}"]`);
            if (optBtn) optBtn.click();
          }
          return;
        }

        if (key === "b") {
          const bBtn = self.container.querySelector("#engBookmarkBtn");
          if (bBtn) bBtn.click();
          return;
        }

        if (key === "m") {
          const mBtn = self.container.querySelector("#engReviewFlagBtn");
          if (mBtn) mBtn.click();
          return;
        }

        if (e.key === "Enter" && (e.ctrlKey || e.metaKey || self.userSelections[index] !== undefined)) {
          const submitBtn = self.container.querySelector("#engSubmitBtn");
          if (submitBtn && !submitBtn.disabled) {
            submitBtn.click();
          }
        }
      };

      document.addEventListener("keydown", this._keyHandler);
    },

    startQuestionTimer: function () {
      this.clearTimers();
      const self = this;
      let secondsCount = 0;
      const q = this.activeQuestion;
      const isDrill = this.session.mode === "drill";
      let remainingDrill = q.target_time || 120;

      this.timerInterval = setInterval(() => {
        secondsCount++;

        if (self.activeTimerMode === "reading") {
          self.readingTimeSeconds++;
        } else {
          self.solvingTimeSeconds++;
        }

        if (q.type === "rc") {
          const readText = self.container.querySelector("#rcReadTimerText");
          const solveText = self.container.querySelector("#rcSolveTimerText");
          const readChip = self.container.querySelector("#rcReadChip");
          const solveChip = self.container.querySelector("#rcSolveChip");

          if (readText) readText.textContent = formatTime(self.readingTimeSeconds);
          if (solveText) solveText.textContent = formatTime(self.solvingTimeSeconds);

          if (readChip && solveChip) {
            if (self.activeTimerMode === "reading") {
              readChip.classList.add("is-active");
              solveChip.classList.remove("is-active");
            } else {
              solveChip.classList.add("is-active");
              readChip.classList.remove("is-active");
            }
          }
        } else {
          const timerText = self.container.querySelector("#engTimerText");
          if (timerText) {
            if (isDrill) {
              remainingDrill--;
              timerText.textContent = formatTime(remainingDrill);
              if (remainingDrill <= 0) {
                self.submitAnswer(true);
              }
            } else {
              timerText.textContent = formatTime(secondsCount);
            }
          }
        }
      }, 1000);
    },

    startSimulationTimer: function () {
      const self = this;
      if (this.simInterval) clearInterval(this.simInterval);

      this.simInterval = setInterval(() => {
        if (!self.session) return;
        self.session.simulationRemainingSeconds--;

        const rem = self.session.simulationRemainingSeconds;
        const timerText = self.container ? self.container.querySelector("#engTimerText") : null;
        if (timerText) timerText.textContent = formatTime(rem);

        if (rem === 300) {
          const alertBox = self.container.querySelector("#engSimAlert");
          const timerBox = self.container.querySelector("#engSimulationTimer");
          if (alertBox) alertBox.style.display = "flex";
          if (timerBox) timerBox.classList.add("warning-timer");
        }

        if (rem <= 0) {
          clearInterval(self.simInterval);
          self.finishSession();
        }
      }, 1000);
    },

    clearTimers: function () {
      if (this.timerInterval) {
        clearInterval(this.timerInterval);
        this.timerInterval = null;
      }
    },

    submitAnswer: async function (isTimeout = false) {
      this.clearTimers();
      const index = this.currentIndex;
      const q = this.activeQuestion;
      const selectedIndex = this.userSelections[index];

      const now = Date.now();
      const totalTimeTaken = Math.max(1, Math.round((now - this.questionStartTime) / 1000));
      const firstIntSeconds = this.firstInteractionTime
        ? Math.max(0, Math.round((this.firstInteractionTime - this.questionStartTime) / 1000))
        : totalTimeTaken;
      const afterElimSeconds = this.lastEliminationTime
        ? Math.max(0, Math.round((now - this.lastEliminationTime) / 1000))
        : 0;

      const isCorrect = selectedIndex !== undefined && selectedIndex === q.correct_option_index;

      const attempt = {
        date: new Date().toISOString().slice(0, 10),
        timestamp: now,
        session_id: this.session.id,
        category_name: "English",
        topic_name: q.subsection || "Verbal Reasoning",
        pattern_id: q.id ? (typeof q.id === "number" ? q.id : 1001) : 1001,
        pattern_name: q.question_type || "GMAT Verbal",
        hybrid_type: q.type || "verbal",
        question_text: q.stem || "",
        options: q.options || [],
        selected_answer: selectedIndex !== undefined ? q.options[selectedIndex] : null,
        correct_answer: q.options[q.correct_option_index],
        correct_option_index: q.correct_option_index,
        is_correct: isCorrect,
        is_timeout: Boolean(isTimeout),
        is_skipped: false,
        time_taken: totalTimeTaken,
        explanation: (q.reasoning && q.reasoning.why_correct) || "",
        difficulty: q.difficulty || 3,
        time_spent_reading_passage: this.readingTimeSeconds || 0,
        time_spent_on_question: this.solvingTimeSeconds || totalTimeTaken,
        time_before_first_interaction: firstIntSeconds,
        time_after_eliminating_choices: afterElimSeconds,
        passage_id: q.passage ? q.passage.id : null,
        trap_type: q.reasoning && q.reasoning.choices_breakdown && selectedIndex !== undefined
          ? (q.reasoning.choices_breakdown[selectedIndex] || {}).trap
          : null,
        question_type: q.question_type || null,
        reasoning_path: q.reasoning || null,
      };

      if (typeof window.recordLocalAttempt === "function") {
        try {
          const savedRecord = await window.recordLocalAttempt(attempt);
          if (savedRecord && savedRecord.id) {
            attempt.id = savedRecord.id;
          }
        } catch (e) {
          console.warn("Could not save attempt to local DB:", e);
        }
      }

      if (window.AptitudeEnglishDB && typeof window.AptitudeEnglishDB.recordEnglishAttempt === "function") {
        try {
          const engRecord = await window.AptitudeEnglishDB.recordEnglishAttempt({
            ...attempt,
            mode: q.section === "foundation" ? "foundation" : "gmat_verbal",
            verbal_type: q.type === "cr" ? "critical_reasoning" : (q.type === "rc" ? "reading_comprehension" : null),
            foundation_type: q.foundation_type || null,
            is_ai_generated: Boolean(q.is_ai_generated || this.session.is_ai_generated),
          });
          if (engRecord && engRecord.id) {
            attempt.id = engRecord.id;
          }
        } catch (e) {
          console.warn("Could not save attempt to English DB:", e);
        }
      }

      if (window.AptitudeEnglishDB && typeof window.AptitudeEnglishDB.saveActiveEnglishSession === "function") {
        try {
          const elimMap = {};
          for (const k in this.eliminatedChoices) {
            elimMap[k] = Array.from(this.eliminatedChoices[k] || []);
          }
          await window.AptitudeEnglishDB.saveActiveEnglishSession({
            session_id: this.session.id || "active_english_session",
            mode: this.session.mode || "gmat_verbal",
            current_index: index,
            total_questions: this.session.totalQuestions,
            questions: this.session.questions,
            user_answers: this.userSelections,
            eliminated_options: elimMap,
            bookmarks: Array.from(this.bookmarks),
            marked_for_review: Array.from(this.markedForReview),
            time_remaining_seconds: this.session.simulationRemainingSeconds,
            start_time: this.questionStartTime,
          });
        } catch (e) {
          console.warn("Could not save active English session:", e);
        }
      }

      const self = this;
      if (!this.session.isSimulation) {
        ReviewUI.renderReview({
          container: this.container,
          attempt: attempt,
          question: q,
          onNext: () => {
            if (index < self.session.totalQuestions - 1) {
              self.renderQuestion(index + 1);
            } else {
              self.finishSession();
            }
          },
          onDone: () => self.exitSession(),
        });
      } else {
        if (index < this.session.totalQuestions - 1) {
          this.renderQuestion(index + 1);
        } else {
          this.finishSession();
        }
      }
    },

    skipQuestion: function () {
      this.clearTimers();
      const index = this.currentIndex;
      this.markedForReview.add(index);
      if (index < this.session.totalQuestions - 1) {
        this.renderQuestion(index + 1);
      } else {
        this.finishSession();
      }
    },

    finishSession: function () {
      this.clearTimers();
      if (this.simInterval) clearInterval(this.simInterval);
      if (this._keyHandler) document.removeEventListener("keydown", this._keyHandler);

      if (window.AptitudeEnglishDB && typeof window.AptitudeEnglishDB.clearActiveEnglishSession === "function") {
        window.AptitudeEnglishDB.clearActiveEnglishSession().catch(() => {});
      }

      if (window.AptitudeEnglishDB && typeof window.AptitudeEnglishDB.recordEnglishSession === "function") {
        const correctCount = Object.keys(this.userSelections).filter(
          idx => this.session.questions[idx] && this.userSelections[idx] === this.session.questions[idx].correct_option_index
        ).length;
        window.AptitudeEnglishDB.recordEnglishSession({
          session_id: this.session.id,
          mode: this.session.mode,
          total_questions: this.session.totalQuestions,
          score: correctCount,
          accuracy: this.session.totalQuestions ? Math.round((correctCount / this.session.totalQuestions) * 100) : 0,
        }).catch(() => {});
      }

      if (typeof this.session.onFinish === "function") {
        this.session.onFinish(this.session);
      } else if (window.EnglishOverlayManager && typeof EnglishOverlayManager.showCompletion === "function") {
        EnglishOverlayManager.showCompletion(this.session, () => {
          this.exitSession();
        });
      } else {
        this.exitSession();
      }
    },

    exitSession: function () {
      this.clearTimers();
      if (this.simInterval) clearInterval(this.simInterval);
      if (this._keyHandler) document.removeEventListener("keydown", this._keyHandler);

      EnglishOverlayManager.close();

      if (typeof this.session.onExit === "function") {
        this.session.onExit();
      } else if (this.container) {
        // Return to English Dashboard
        window.EnglishApp?.init();
      }
    },
  };

  // =========================================================================
  // Answer Review Module
  // =========================================================================
  const ReviewUI = {
    renderReview: function (params) {
      const container = params.container || document.getElementById("englishQuestionView");
      const attempt = params.attempt || {};
      const q = params.question || {};
      const onNext = params.onNext;
      const onDone = params.onDone;

      const isCorrect = Boolean(attempt.is_correct);
      const isSkipped = Boolean(attempt.is_skipped);
      const timeTaken = attempt.time_taken || 0;
      const targetTime = q.target_time || 120;

      // Pacing Feedback
      let paceClass = "pace-good";
      let paceLabel = "🎯 On pace";
      let paceExplanation = `Finished in ${timeTaken}s, right within the optimal target window (${targetTime}s).`;

      if (timeTaken < targetTime * 0.5) {
        paceClass = "pace-fast";
        paceLabel = "⚡ Too fast (<50% target)";
        paceExplanation = `Finished in ${timeTaken}s (target: ${targetTime}s). Rapid answering increases risk of falling for subtle trap choices.`;
      } else if (timeTaken > targetTime * 1.25) {
        paceClass = "pace-slow";
        paceLabel = "⏳ Too slow (>125% target)";
        paceExplanation = `Took ${timeTaken}s (target: ${targetTime}s). In a 45-minute exam, spending over target risks running out of time on later questions.`;
      }

      // Automatic initial error category
      let autoErrorCategory = "Unknown / Conceptual gap";
      if (!isCorrect) {
        if (attempt.is_timeout || timeTaken < targetTime * 0.45) {
          autoErrorCategory = "Timing issue / Rushed";
        } else if (attempt.trap_type === "Extreme Language") {
          autoErrorCategory = "Extreme answer";
        } else if (attempt.trap_type === "Scope Shift" || attempt.trap_type === "Out of Scope") {
          autoErrorCategory = "Out of scope";
        } else if (attempt.trap_type === "Reversed Causality") {
          autoErrorCategory = "Reversed causality";
        } else if (attempt.trap_type === "Confused necessary/sufficient") {
          autoErrorCategory = "Confused necessary/sufficient";
        } else {
          autoErrorCategory = "Fell for tempting trap choice";
        }
      }

      const bannerClass = isCorrect ? "is-correct" : (isSkipped ? "is-skipped" : "is-incorrect");
      const bannerIcon = isCorrect ? "✓" : (isSkipped ? "⚐" : "✕");
      const bannerTitle = isCorrect ? "Correct!" : (isSkipped ? "Skipped" : "Incorrect");
      const bannerSubtitle = isCorrect
        ? `Spot-on analysis. You answered in ${timeTaken}s.`
        : `Let's analyze why the correct answer works and how to avoid the trap next time.`;

      const letters = ["A", "B", "C", "D", "E"];
      const userLetter = attempt.selected_answer
        ? (letters[q.options.indexOf(attempt.selected_answer)] || "?")
        : "None";
      const correctLetter = letters[q.correct_option_index] || "A";

      const comparisonHtml = `
        <div class="english-review-comparison-card">
          <div class="review-answer-pill user-answer ${!isCorrect ? 'wrong' : ''}">
            <span class="review-pill-label">Your Answer</span>
            <span class="review-pill-choice">[${userLetter}] ${attempt.selected_answer || '(No answer selected)'}</span>
          </div>
          <div class="review-answer-pill correct-answer">
            <span class="review-pill-label">Correct Answer</span>
            <span class="review-pill-choice">[${correctLetter}] ${q.options[q.correct_option_index]}</span>
          </div>
        </div>
      `;

      const reasoningHtml = this.buildReasoningPathHTML(q, attempt);

      let errorCategoryHtml = "";
      if (!isCorrect) {
        const errorOptions = ERROR_CATEGORIES.map((cat) => {
          const selected = cat === autoErrorCategory ? "selected" : "";
          return `<option value="${cat}" ${selected}>${cat}</option>`;
        }).join("");

        errorCategoryHtml = `
          <div class="english-error-categorization-card" id="engErrorCatCard">
            <div class="error-cat-header">
              <span class="error-cat-title">⚠️ Error Log & Diagnosis</span>
              <span class="error-auto-badge">Auto-detected: ${autoErrorCategory}</span>
            </div>
            <p style="font-size: 13px; color: #475569; margin: 0;">
              Classify why you missed this question to train your mistake notebook and review stats:
            </p>
            <div class="error-cat-controls">
              <select class="error-cat-select" id="engErrorCatSelect" aria-label="Error category selection">
                ${errorOptions}
              </select>
              <span class="error-save-status" id="engErrorSaveStatus" style="display: none;">
                ✓ Saved to Error Log
              </span>
            </div>
          </div>
        `;
      }

      container.innerHTML = `
        <div class="english-review-container">
          <div class="english-review-status-banner ${bannerClass}">
            <div class="review-banner-left">
              <div class="review-banner-icon" aria-hidden="true">${bannerIcon}</div>
              <div>
                <h2 class="review-banner-title">${bannerTitle}</h2>
                <p class="review-banner-subtitle">${bannerSubtitle}</p>
              </div>
            </div>
            <div>
              <span class="pacing-badge ${paceClass}">
                <span>${paceLabel}</span>
              </span>
            </div>
          </div>

          <p style="font-size: 13px; color: #475569; margin: -10px 0 0 4px;">
            ${paceExplanation}
          </p>

          ${comparisonHtml}
          ${errorCategoryHtml}
          ${reasoningHtml}

          <footer class="english-action-bar">
            <button class="english-btn english-btn-outline" id="engReviewDoneBtn" type="button">
              <span>← Back to Dashboard</span>
            </button>
            <button class="english-btn english-btn-primary" id="engReviewNextBtn" type="button">
              <span>Next Question →</span>
            </button>
          </footer>
        </div>
      `;

      const nextBtn = container.querySelector("#engReviewNextBtn");
      if (nextBtn && typeof onNext === "function") {
        nextBtn.addEventListener("click", onNext);
      }

      const doneBtn = container.querySelector("#engReviewDoneBtn");
      if (doneBtn && typeof onDone === "function") {
        doneBtn.addEventListener("click", onDone);
      }

      const catSelect = container.querySelector("#engErrorCatSelect");
      const saveStatus = container.querySelector("#engErrorSaveStatus");
      if (catSelect) {
        catSelect.addEventListener("change", async function () {
          const chosenCategory = this.value;
          if (saveStatus) {
            saveStatus.style.display = "inline-flex";
            saveStatus.textContent = "Saving...";
          }

          if (attempt.id && typeof window.updateLocalAttemptErrorCategory === "function") {
            try {
              await window.updateLocalAttemptErrorCategory(attempt.id, chosenCategory);
              if (saveStatus) saveStatus.textContent = "✓ Saved to Error Log";
            } catch (err) {
              console.warn("Failed saving error category to IndexedDB:", err);
              if (saveStatus) saveStatus.textContent = "Saved locally";
            }
          } else {
            if (saveStatus) saveStatus.textContent = "✓ Saved to Error Log";
          }
        });
      }
    },

    buildReasoningPathHTML: function (q, attempt) {
      const r = q.reasoning || {};
      const letters = ["A", "B", "C", "D", "E"];
      let specificSectionsHtml = "";

      if (q.type === "cr" || q.stimulus) {
        specificSectionsHtml = `
          <div class="reasoning-section-grid">
            <div class="reasoning-step-box">
              <span class="reasoning-step-title">🏛️ Premise</span>
              <div class="reasoning-step-content">${r.premise || 'Identified facts from stimulus.'}</div>
            </div>
            <div class="reasoning-step-box">
              <span class="reasoning-step-title">🎯 Conclusion</span>
              <div class="reasoning-step-content">${r.conclusion || 'The author’s central assertion.'}</div>
            </div>
            <div class="reasoning-step-box">
              <span class="reasoning-step-title">🌉 Underlying Assumption</span>
              <div class="reasoning-step-content">${r.assumption || 'Unstated bridge necessary for conclusion.'}</div>
            </div>
            <div class="reasoning-step-box">
              <span class="reasoning-step-title">⚡ Logical Gap</span>
              <div class="reasoning-step-content">${r.logical_gap || 'Why premise does not guarantee conclusion.'}</div>
            </div>
          </div>

          <div style="margin-top: 14px;">
            <strong style="color: #0f766e; font-size: 14px;">Why the Correct Choice Works:</strong>
            <p style="font-size: 14.5px; line-height: 1.6; margin: 4px 0 12px 0;">${r.why_correct || ''}</p>
          </div>
        `;
      } else if (q.type === "rc" || q.passage) {
        specificSectionsHtml = `
          <div class="reasoning-section-grid">
            <div class="reasoning-step-box">
              <span class="reasoning-step-title">📍 Textual Evidence</span>
              <div class="reasoning-step-content">${r.evidence || 'Direct citation from passage.'}</div>
            </div>
            <div class="reasoning-step-box">
              <span class="reasoning-step-title">✓ Correct Support</span>
              <div class="reasoning-step-content">${r.why_correct || 'Explains how the passage validates the option.'}</div>
            </div>
          </div>
        `;
      } else if (q.type === "grammar" || q.sentence) {
        specificSectionsHtml = `
          <div class="reasoning-section-grid">
            <div class="reasoning-step-box">
              <span class="reasoning-step-title">📏 Tested Grammar Rule</span>
              <div class="reasoning-step-content">${r.rule || 'Grammar principle tested.'}</div>
            </div>
            <div class="reasoning-step-box">
              <span class="reasoning-step-title">💡 Why It Works</span>
              <div class="reasoning-step-content">${r.why_works || r.why_correct || ''}</div>
            </div>
            <div class="reasoning-step-box">
              <span class="reasoning-step-title">📘 Simple Example</span>
              <div class="reasoning-step-content"><em>${r.simple_example || ''}</em></div>
            </div>
            <div class="reasoning-step-box">
              <span class="reasoning-step-title">🧠 Quick Memory Rule</span>
              <div class="reasoning-step-content"><strong>${r.short_memory_rule || ''}</strong></div>
            </div>
          </div>
        `;
      } else if (q.type === "vocab" || q.word_data) {
        const w = q.word_data || {};
        specificSectionsHtml = `
          <div class="reasoning-section-grid">
            <div class="reasoning-step-box">
              <span class="reasoning-step-title">📖 Definition & Context</span>
              <div class="reasoning-step-content"><strong>${w.definition || ''}</strong><br>${w.contextual_meaning || ''}</div>
            </div>
            <div class="reasoning-step-box">
              <span class="reasoning-step-title">🏢 Business Usage</span>
              <div class="reasoning-step-content">${w.business_example || w.example || ''}</div>
            </div>
            <div class="reasoning-step-box">
              <span class="reasoning-step-title">🔗 Synonyms & Antonyms</span>
              <div class="reasoning-step-content">
                <strong>Synonyms:</strong> ${(w.synonyms || []).join(', ')}<br>
                <strong>Antonyms:</strong> ${(w.antonyms || []).join(', ')}
              </div>
            </div>
            <div class="reasoning-step-box">
              <span class="reasoning-step-title">💡 Mnemonic Memory Aid</span>
              <div class="reasoning-step-content">${w.memory_aid || ''}</div>
            </div>
          </div>
        `;
      }

      let choicesAnalysisHtml = "";
      if (Array.isArray(r.choices_breakdown) && r.choices_breakdown.length > 0) {
        const rows = r.choices_breakdown.map((item, idx) => {
          const letter = letters[idx] || item.letter;
          const isCorrectChoice = idx === q.correct_option_index;
          return `
            <div class="choice-analysis-item ${isCorrectChoice ? 'is-correct-choice' : ''}">
              <div class="choice-analysis-header">
                <span class="choice-analysis-name">Option [${letter}]</span>
                <span class="choice-trap-pill">${item.trap || (isCorrectChoice ? 'Correct Choice' : 'Trap')}</span>
              </div>
              <p style="margin: 0; font-size: 13.5px; line-height: 1.5; color: #334155;">
                ${item.text || ''}
              </p>
            </div>
          `;
        }).join("");

        choicesAnalysisHtml = `
          <div style="margin-top: 16px;">
            <h4 style="margin: 0 0 10px 0; font-size: 14px; font-weight: 800; color: #1e293b;">
              Option-by-Option Analysis & Trap Types:
            </h4>
            <div class="choices-breakdown-list">
              ${rows}
            </div>
          </div>
        `;
      }

      return `
        <article class="english-reasoning-card" aria-label="Detailed Reasoning Path">
          <div class="reasoning-heading">
            <h3>Detailed Reasoning Path</h3>
            <span class="english-badge">${q.question_type || 'Analysis'}</span>
          </div>
          ${specificSectionsHtml}
          ${choicesAnalysisHtml}
        </article>
      `;
    },
  };

  // =========================================================================
  // Spaced Repetition Flashcard UI Module
  // =========================================================================
  const FlashcardUI = {
    deck: [],
    currentIndex: 0,
    container: null,
    onComplete: null,
    isFlipped: false,

    startDeck: function (config) {
      this.deck = Array.isArray(config.deck) && config.deck.length > 0
    startDeck: function (config = {}) {
      const allVocab = (window.ENGLISH_DATA && Array.isArray(window.ENGLISH_DATA.VOCABULARY_ITEMS) && window.ENGLISH_DATA.VOCABULARY_ITEMS.length > 0)
        ? window.ENGLISH_DATA.VOCABULARY_ITEMS
        : BUILTIN_FLASHCARDS;
      let targetDeck = Array.isArray(config.deck) && config.deck.length > 0
        ? config.deck
        : BUILTIN_FLASHCARDS;
        : allVocab;
      if (config.count && config.count > 0 && targetDeck.length > config.count) {
        targetDeck = [...targetDeck].sort(() => Math.random() - 0.5).slice(0, config.count);
      }
      this.deck = targetDeck;
      this.currentIndex = 0;
      this.container = config.container || document.getElementById("englishFlashcardView") || document.getElementById("englishQuestionView");
      this.container = config.container || EnglishOverlayManager.getViewContainer();
      this.container = config.container || (window.EnglishOverlayManager && EnglishOverlayManager.getViewContainer()) || document.getElementById("englishPracticeView");
      this.onComplete = config.onComplete || null;
      this.isFlipped = false;

      this.renderCard(this.currentIndex);
    },

    renderCard: function (index) {
      if (!this.container) return;
      if (index >= this.deck.length) {
        this.finishDeck();
        return;
      }

      this.currentIndex = index;
      this.isFlipped = false;
      const card = this.deck[index];
      const total = this.deck.length;

      this.container.innerHTML = `
        <div class="flashcard-wrapper" id="engFlashcardWrapper">
          <div class="flashcard-hud">
            <span>Vocabulary Deck (${index + 1} of ${total})</span>
            <span>Spaced Repetition Practice</span>
            <button class="english-btn english-btn-ghost" id="engCardCloseBtn" type="button" style="padding: 4px 10px; font-size: 12px; color: #64748b;">
              ✕ Exit Deck
            </button>
          </div>

          <div class="flashcard-card-3d" id="engFlashcard3D" tabindex="0" role="button" aria-label="Flashcard for ${card.word}. Click or press space to flip.">
            <div class="flashcard-face card-front">
              <div class="card-front-top">
                <span class="card-pos-badge">${card.part_of_speech || 'Word'}</span>
                <button class="english-btn english-btn-ghost" id="engCardHintBtn" type="button" style="padding: 4px 8px; font-size: 12px;">
                  💡 Hint
                </button>
              </div>

              <div class="card-front-center">
                <h2 class="card-word-title">${card.word}</h2>
                <span class="card-phonetic">${card.phonetic || ''}</span>
                <p class="card-hint-text" id="engCardHintText" style="display: none;">${card.hint || 'No hint available.'}</p>
                <p class="card-hint-text" id="engCardHintText" style="display: none;">${card.hint || card.root_prefix_suffix || 'Think of the Latin/Greek root or contextual usage.'}</p>
              </div>

              <div class="card-front-bottom">
                <span>Space / Click to flip</span>
                <span>↻ Tap card to reveal definition</span>
              </div>
            </div>

            <div class="flashcard-face card-back">
              <div class="card-back-header">
                <h3 class="card-back-word">${card.word}</h3>
                <span class="card-pos-badge">${card.part_of_speech || ''}</span>
              </div>

              <div class="card-back-body">
                <div class="card-definition-box">
                  <div class="card-definition-label">Definition</div>
                  <div class="card-definition-text">${card.definition}</div>
                </div>

                ${card.contextual ? `
                ${(card.contextual_meaning || card.contextual) ? `
                  <div class="card-example-box">
                    <strong>Contextual Usage:</strong> ${card.contextual}
                    <strong>GMAT Contextual Nuance:</strong> ${card.contextual_meaning || card.contextual}
                  </div>
                ` : ''}

                ${card.common_confusion ? `
                  <div class="card-example-box" style="border-left: 3px solid #f59e0b; background: #fffbeb;">
                    <strong style="color: #b45309;">⚠️ Trap / Common Confusion:</strong> ${card.common_confusion}
                  </div>
                ` : ''}

                ${card.business_example ? `
                  <div class="card-example-box">
                    <strong>Business Context:</strong> ${card.business_example}
                    <strong>Executive / Business Context:</strong> ${card.business_example}
                  </div>
                ` : ''}

                ${Array.isArray(card.synonyms) && card.synonyms.length > 0 ? `
                  <div class="card-synonyms-row">
                    <strong>Synonyms:</strong>
                    ${card.synonyms.map(s => `<span class="card-syn-tag">${s}</span>`).join('')}
                  </div>
                ` : ''}

                ${card.mnemonic ? `
                ${(card.memory_aid || card.mnemonic) ? `
                  <div class="card-mnemonic-box">
                    <strong>💡 Mnemonic Memory Aid:</strong> ${card.mnemonic}
                    <strong>💡 Mnemonic Memory Aid:</strong> ${card.memory_aid || card.mnemonic}
                  </div>
                ` : ''}
              </div>

              <div style="font-size: 11px; color: #94a3b8; text-align: center;">
                Rate your recall below to advance SRS schedule:
              </div>
            </div>
          </div>

          <div class="flashcard-rating-bar" id="engSrsRatingBar">
            <button class="srs-rate-btn rate-again" data-srs-rating="again" type="button" title="Shortcut: 1">
              <span>Again / Difficult</span>
              <span class="srs-interval-badge">(1 Day)</span>
            </button>
            <button class="srs-rate-btn rate-hard" data-srs-rating="review" type="button" title="Shortcut: 2">
              <span>Need Review</span>
              <span class="srs-interval-badge">(3 Days)</span>
            </button>
            <button class="srs-rate-btn rate-good" data-srs-rating="good" type="button" title="Shortcut: 3">
              <span>Good / Easy</span>
              <span class="srs-interval-badge">(7 Days)</span>
            </button>
            <button class="srs-rate-btn rate-mastered" data-srs-rating="mastered" type="button" title="Shortcut: 4">
              <span>Mastered</span>
              <span class="srs-interval-badge">(14+ Days)</span>
            </button>
          </div>
        </div>
      `;

      this.attachCardEventListeners(card, index);
    },

    attachCardEventListeners: function (card, index) {
      const self = this;
      const cardEl = this.container.querySelector("#engFlashcard3D");
      const hintBtn = this.container.querySelector("#engCardHintBtn");
      const hintText = this.container.querySelector("#engCardHintText");

      function toggleFlip() {
        self.isFlipped = !self.isFlipped;
        if (cardEl) {
          if (self.isFlipped) cardEl.classList.add("is-flipped");
          else cardEl.classList.remove("is-flipped");
        }
      }

      if (cardEl) {
        cardEl.addEventListener("click", toggleFlip);
      }

      if (hintBtn && hintText) {
        hintBtn.addEventListener("click", (e) => {
          e.stopPropagation();
          hintText.style.display = hintText.style.display === "none" ? "block" : "none";
        });
      }

      const closeBtn = this.container.querySelector("#engCardCloseBtn");
      if (closeBtn) {
        closeBtn.addEventListener("click", () => {
          EnglishOverlayManager.confirmExit(() => {
            EnglishOverlayManager.close();
            window.EnglishApp?.init();
          });
        });
      }

      this.container.querySelectorAll(".srs-rate-btn").forEach((btn) => {
        btn.addEventListener("click", function () {
          const rating = this.getAttribute("data-srs-rating");
          self.recordSrsRating(card, rating);
          self.renderCard(index + 1);
        });
      });

      if (this._cardKeyHandler) {
        document.removeEventListener("keydown", this._cardKeyHandler);
      }
      this._cardKeyHandler = function (e) {
        if (["INPUT", "TEXTAREA", "SELECT"].includes(document.activeElement.tagName)) return;
        if (e.code === "Space") {
          e.preventDefault();
          toggleFlip();
        } else if (e.key === "1") {
          self.container.querySelector('.srs-rate-btn[data-srs-rating="again"]')?.click();
        } else if (e.key === "2") {
          self.container.querySelector('.srs-rate-btn[data-srs-rating="review"]')?.click();
        } else if (e.key === "3") {
          self.container.querySelector('.srs-rate-btn[data-srs-rating="good"]')?.click();
        } else if (e.key === "4") {
          self.container.querySelector('.srs-rate-btn[data-srs-rating="mastered"]')?.click();
        }
      };
      document.addEventListener("keydown", this._cardKeyHandler);
    },

    recordSrsRating: function (card, rating) {
      try {
        const stored = JSON.parse(localStorage.getItem("english_foundation_srs_deck") || "{}");
        stored[card.word] = {
          word: card.word,
          rating: rating,
          timestamp: Date.now(),
        };
        localStorage.setItem("english_foundation_srs_deck", JSON.stringify(stored));
      } catch (e) {
        console.warn("Could not save SRS progress:", e);
      }

      if (window.AptitudeEnglishDB && typeof window.AptitudeEnglishDB.recordVocabCardReview === "function") {
        window.AptitudeEnglishDB.recordVocabCardReview(card.word, rating).catch(() => {});
      }
    },

    finishDeck: function () {
      if (this._cardKeyHandler) {
        document.removeEventListener("keydown", this._cardKeyHandler);
      }
      if (typeof this.onComplete === "function") {
        this.onComplete();
      } else if (this.container) {
        this.container.innerHTML = `
          <div class="flashcard-wrapper" style="text-align: center; padding: 40px 20px;">
            <div style="font-size: 48px;">🎉</div>
            <h2>Vocabulary Flashcards Completed!</h2>
            <p style="color: #64748b;">You have reviewed all cards in this deck. Repetitions have been recorded into your spaced repetition system.</p>
            <button class="english-btn english-btn-primary" onclick="window.EnglishFlashcardUI.startDeck({});" type="button">
              Review Deck Again
            </button>
          </div>
        `;
      } else {
        EnglishOverlayManager.showCompletion({
          totalQuestions: this.deck.length,
          score: this.deck.length,
          subsection: "Vocabulary Flashcards",
          mode: "vocab_srs"
        }, () => {
          EnglishOverlayManager.close();
          window.EnglishApp?.init();
        });
      }
    },
  };

  // =========================================================================
  // =========================================================================
  // EnglishApp Complete 3-Subtab Dashboard & Session Controller
  // =========================================================================
  const EnglishApp = {
    QuestionRunner: QuestionRunner,
    ReviewUI: ReviewUI,
    FlashcardUI: FlashcardUI,
    activeSubtab: "gmat_verbal",
    currentTrajectoryVariant: "Critical Reasoning",
    isAiMode: (function () {
      try {
        return localStorage.getItem("gmat_english_ai_mode") !== "false";
      } catch (e) {
        return true;
      }
    })(),

    init: async function () {
      const screen = document.getElementById("englishScreen");
      if (!screen) return;

      let overview = {
        total_attempts: 0,
        accuracy: 0,
        cr_avg_time: 0,
        rc_avg_question_time: 0,
        current_streak: 0,
        weak_topics_count: 0,
        verbal_readiness: 0,
        foundation_readiness: 0,
        overall_readiness: 0,
        confidence_bands: {
          quantitative: "N/A",
          verbal: "Baseline Diagnostic Needed",
          data_insights: "N/A",
          composite: "Diagnostic Needed",
        },
        readiness_score: 0,
        readiness_tier: "Diagnostic Phase",
      };

      let activeSession = null;
      let studyPlan = null;
      let beginnerProfile = null;

      if (window.AptitudeEnglishDB) {
        try {
          overview = await window.AptitudeEnglishDB.getEnglishOverview();
        } catch (e) {
          console.warn("Could not load English overview:", e);
        }
        try {
          activeSession = await window.AptitudeEnglishDB.getActiveEnglishSession();
        } catch (e) {
          console.warn("Could not check active English session:", e);
        }
        try {
          studyPlan = await window.AptitudeEnglishDB.get100DayPlan();
        } catch (e) {
          console.warn("Could not load 100-day plan:", e);
        }
        try {
          beginnerProfile = await window.AptitudeEnglishDB.getBeginnerProfile();
        } catch (e) {
          console.warn("Could not load beginner profile:", e);
        }
      }

      this.renderMainLayout(screen, overview, activeSession, studyPlan, beginnerProfile);
    },

    renderMainLayout: function (screen, overview, activeSession, studyPlan, beginnerProfile) {
      const self = this;
      const readinessScore = overview.readiness_score || 0;
      const readinessTier = overview.readiness_tier || "Diagnostic Phase";
      const verbalReadiness = overview.verbal_readiness || overview.readiness_score || 0;
      const verbalTier = overview.verbal_tier || overview.readiness_tier || "Diagnostic Phase";
      const foundationReadiness = overview.foundation_readiness || 0;
      const foundationTier = overview.foundation_tier || "Beginner";
      const verbalReadiness = typeof overview.verbal_readiness === 'object' && overview.verbal_readiness !== null
        ? (overview.verbal_readiness.score || 0)
        : (overview.verbal_readiness || overview.readiness_score || 0);
      const verbalTier = typeof overview.verbal_readiness === 'object' && overview.verbal_readiness !== null
        ? (overview.verbal_readiness.tier || "Diagnostic Phase")
        : (overview.verbal_tier || overview.readiness_tier || "Diagnostic Phase");
      const foundationReadiness = typeof overview.foundation_readiness === 'object' && overview.foundation_readiness !== null
        ? (overview.foundation_readiness.score || 0)
        : (overview.foundation_readiness || 0);
      const foundationTier = typeof overview.foundation_readiness === 'object' && overview.foundation_readiness !== null
        ? (overview.foundation_readiness.tier || "Beginner")
        : (overview.foundation_tier || "Beginner");
      const compositeBand = (overview.confidence_bands && overview.confidence_bands.composite) || "Baseline";
      const crAvg = overview.cr_avg_time ? `${overview.cr_avg_time}s` : "--";
      const rcAvg = overview.rc_avg_question_time ? `${overview.rc_avg_question_time}s` : "--";
      const streak = overview.current_streak ? `${overview.current_streak}d` : "0d";
      const accuracy = overview.accuracy ? `${overview.accuracy}%` : "0%";
      const totalSolved = overview.total_attempts || 0;

      let resumeBannerHtml = "";
      if (activeSession && activeSession.questions && activeSession.questions.length > 0) {
        const remainingQ = activeSession.total_questions - (activeSession.current_index || 0);
        resumeBannerHtml = `
          <div class="english-resume-banner" style="background: linear-gradient(135deg, #1e3a5f, #0f766e); color: #fff; padding: 16px 20px; border-radius: 12px; margin-bottom: 20px; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 12px; box-shadow: 0 4px 14px rgba(15, 118, 110, 0.2);">
            <div>
              <span style="background: #fef08a; color: #854d0e; padding: 3px 8px; border-radius: 6px; font-size: 11px; font-weight: 700; text-transform: uppercase;">Incomplete Session</span>
              <h3 style="margin: 6px 0 2px; font-size: 16px; color: #fff;">⚡ Continue English Session</h3>
              <p style="margin: 0; font-size: 13px; opacity: 0.9;">
                Mode: <strong>${activeSession.mode || 'Verbal Practice'}</strong> • Question ${(activeSession.current_index || 0) + 1} of ${activeSession.total_questions} (${remainingQ} remaining)
              </p>
            </div>
            <div style="display: flex; gap: 10px;">
              <button class="english-btn" style="background: #fff; color: #0f766e; font-weight: 700;" type="button" id="engResumeBtn">
                ▶ Resume Session
              </button>
              <button class="english-btn english-btn-ghost" style="color: #fff; border-color: rgba(255,255,255,0.4);" type="button" id="engDiscardBtn">
                Discard ✕
              </button>
            </div>
          </div>
        `;
      }

      // Beginner Onboarding Welcome Panel
      const currentLevelKey = (beginnerProfile && beginnerProfile.level) || "beginner_absolute";
      const onboardingHtml = `
        <section class="english-onboarding-panel" aria-labelledby="engOnboardingTitle">
          <div class="english-onboarding-header">
            <div>
              <span class="english-badge" style="background: #e0f2fe; color: #0369a1; border-color: #bae6fd;">Target 700+ GMAT Pathway (100 Days)</span>
              <h3 id="engOnboardingTitle" class="english-onboarding-title">Start from Your Current Level</h3>
            </div>
            <span style="font-size: 12px; color: #64748b;">Click a level to calibrate your daily study recommendations</span>
          </div>

          <div class="english-levels-grid">
            <div class="english-level-card ${currentLevelKey === 'beginner_absolute' ? 'is-active' : ''}" data-level="beginner_absolute">
              ${currentLevelKey === 'beginner_absolute' ? '<span class="english-level-active-check">✓</span>' : ''}
              <span class="english-level-card-badge">Level 1</span>
              <h4 class="english-level-card-name">Complete Beginner</h4>
              <p class="english-level-card-desc">Grammar rules, sentence mechanics, and vocabulary foundation before verbal reasoning.</p>
            </div>

            <div class="english-level-card ${currentLevelKey === 'quant_ready' ? 'is-active' : ''}" data-level="quant_ready">
              ${currentLevelKey === 'quant_ready' ? '<span class="english-level-active-check">✓</span>' : ''}
              <span class="english-level-card-badge">Level 2</span>
              <h4 class="english-level-card-name">Quant Ready, English Starter</h4>
              <p class="english-level-card-desc">Strong in Math. Fast-track foundation rules and focus on GMAT CR argument logic.</p>
            </div>

            <div class="english-level-card ${currentLevelKey === 'intermediate_brushup' ? 'is-active' : ''}" data-level="intermediate_brushup">
              ${currentLevelKey === 'intermediate_brushup' ? '<span class="english-level-active-check">✓</span>' : ''}
              <span class="english-level-card-badge">Level 3</span>
              <h4 class="english-level-card-name">Intermediate Brush-Up</h4>
              <p class="english-level-card-desc">Grammar comfortable. Focus on Critical Reasoning negation and RC multi-paragraph inference.</p>
            </div>

            <div class="english-level-card ${currentLevelKey === 'advanced_speed' ? 'is-active' : ''}" data-level="advanced_speed">
              ${currentLevelKey === 'advanced_speed' ? '<span class="english-level-active-check">✓</span>' : ''}
              <span class="english-level-card-badge">Level 4</span>
              <h4 class="english-level-card-name">Advanced / Speed Optimization</h4>
              <p class="english-level-card-desc">Targeting 700+ pacing (1.8m/q), high-difficulty trap evasion, and 23-question 45m simulations.</p>
            </div>
          </div>
        </section>
      `;

      // 100-Day Preparation Plan Panel ("What should I do today?")
      let dailyPlanHtml = "";
      if (studyPlan && Array.isArray(studyPlan.days) && studyPlan.days.length > 0) {
        const currentDayNum = studyPlan.current_day || 1;
        const today = studyPlan.days.find(d => d.day === currentDayNum) || studyPlan.days[0];
        const daysRemaining = 100 - (studyPlan.completed_days || 0);

        let tasksHtml = "";
        (today.tasks || []).forEach(task => {
          const isCompleted = Boolean(task.completed);
          tasksHtml += `
            <div class="daily-task-item ${isCompleted ? 'is-completed' : ''}">
              <div class="daily-task-left">
                <span class="daily-task-chip ${isCompleted ? 'completed' : 'pending'}">
                  ${isCompleted ? '✓ Completed' : 'Pending'}
                </span>
                <div>
                  <div class="daily-task-title">${task.title}</div>
                  <div class="daily-task-target">Target: ${task.target} questions/cards</div>
                </div>
              </div>
              <div>
                <button class="english-btn ${isCompleted ? 'english-btn-outline' : 'english-btn-primary'} daily-task-action-btn"
                  type="button"
                  data-action-type="${task.type}"
                  data-day="${today.day}"
                  data-task-id="${task.id}"
                  style="font-size: 13px; padding: 6px 14px;">
                  ${isCompleted ? 'Redo Task' : (task.type === 'vocab' ? '🗂️ Review Vocab' : '▶ Start Task')}
                </button>
              </div>
            </div>
          `;
        });

        dailyPlanHtml = `
          <section class="english-daily-plan-panel" aria-labelledby="engDailyPlanTitle">
            <div class="daily-plan-header">
              <div>
                <div class="daily-plan-meta">
                  <span class="english-badge" style="background: #ecfdf5; color: #047857; border-color: #a7f3d0;">
                    ${today.phase_name}
                  </span>
                  <span style="font-size: 12px; color: #64748b; font-weight: 600;">
                    Scheduled: ${today.scheduled_date}
                  </span>
                </div>
                <h3 id="engDailyPlanTitle" style="margin: 8px 0 4px; font-size: 18px; font-weight: 800; color: #1e3a5f;">
                  📅 What should I do today? (Day ${today.day} of 100)
                </h3>
                <p style="margin: 0; font-size: 13.5px; color: #475569; max-width: 680px; line-height: 1.5;">
                  ${today.description}
                </p>
              </div>

              <div style="text-align: right;">
                <div class="daily-plan-progress" style="justify-content: flex-end; margin-bottom: 4px;">
                  <span style="font-size: 12px; font-weight: 700; color: #0f766e;">
                    ${studyPlan.completed_days || 0} / 100 Days (${studyPlan.completion_rate || 0}%)
                  </span>
                  <div class="daily-plan-progress-bar">
                    <div class="daily-plan-progress-fill" style="width: ${studyPlan.completion_rate || 0}%;"></div>
                  </div>
                </div>
                <span style="font-size: 11px; color: #64748b;">
                  ${daysRemaining} days remaining
                </span>
              </div>
            </div>

            <div class="daily-task-list">
              ${tasksHtml}
            </div>

            <div style="margin-top: 14px; display: flex; justify-content: flex-end;">
              <button class="english-btn english-btn-ghost" id="engAdjustScheduleBtn" type="button" style="font-size: 12px; color: #64748b;">
                📅 Missed days? Re-anchor schedule forward
              </button>
            </div>
          </section>
        `;
      }

      screen.innerHTML = `
        <div class="english-container" style="padding: 16px 0 40px;">
          <!-- Top HUD Strip -->
          <!-- Top HUD Strip with Segregated Readiness -->
          <header class="english-hud-bar" style="margin-bottom: 16px;">
            <div>
              <span class="english-badge">GMAT Verbal Reasoning & English</span>
              <h2 style="margin: 4px 0 0; font-size: 22px; font-weight: 800; color: #1e3a5f;">
                English Practice Hub
              </h2>
            </div>
            <div style="display: flex; gap: 16px; flex-wrap: wrap; align-items: center;">
              <div style="text-align: center;" title="Segregated GMAT Verbal Readiness (CR + RC)">
                <span style="font-size: 11px; color: #64748b; text-transform: uppercase; font-weight: 700;">Verbal Readiness</span>
                <div style="font-size: 18px; font-weight: 800; color: #0f766e;">${verbalReadiness}/100 <small style="font-size: 11px; color: #64748b;">(${verbalTier})</small></div>
          <!-- Top Executive Modern HUD Strip -->
          <section class="english-hud-strip" aria-label="GMAT Verbal Readiness Overview" style="margin-bottom: 20px;">
            <div class="english-hud-top">
              <div>
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px;">
                  <span class="english-badge" style="background: #e0f2fe; color: #0369a1; border-color: #bae6fd;">GMAT Verbal Reasoning</span>
                  <span style="font-size: 11.5px; color: #64748b; font-weight: 700; text-transform: uppercase; letter-spacing: 0.04em;">Executive Dashboard</span>
                </div>
                <h2 class="english-hub-brand-title">English Practice Hub</h2>
                <p class="english-hub-brand-sub">Master Critical Reasoning, Reading Comprehension, Foundation Grammar, and 131 Authentic GMAT Vocabulary terms.</p>
                <p class="english-hub-brand-sub">Master Critical Reasoning, Reading Comprehension, Foundation Grammar, and Authentic GMAT Vocabulary.</p>
              </div>
              <div style="height: 32px; width: 1px; background: #e2e8f0;"></div>
              <div style="text-align: center;" title="Segregated Foundation Readiness (Grammar + Vocab)">
                <span style="font-size: 11px; color: #64748b; text-transform: uppercase; font-weight: 700;">Foundation</span>
                <div style="font-size: 18px; font-weight: 800; color: #0891b2;">${foundationReadiness}/100 <small style="font-size: 11px; color: #64748b;">(${foundationTier})</small></div>
              <div style="display: flex; align-items: center; gap: 10px;">
                <button id="toggleAiModeTopBtn" class="english-ai-toggle-pill ${self.isAiMode ? 'is-active' : ''}" type="button" title="Toggle between Adaptive AI Generation and Standard Curated Bank">
                  <span style="display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: ${self.isAiMode ? '#16a34a' : '#94a3b8'};"></span>
                  <span>${self.isAiMode ? '🤖 AI Mode: Adaptive Generation' : '📚 Curated Question Bank'}</span>
                </button>
              </div>
              <div style="height: 32px; width: 1px; background: #e2e8f0;"></div>
              <div style="text-align: center;" title="Estimated Overall Readiness Band">
                <span style="font-size: 11px; color: #64748b; text-transform: uppercase; font-weight: 700;">Estimated Band</span>
                <div style="font-size: 14px; font-weight: 800; color: #4338ca;">${compositeBand}</div>
            </div>

            <div class="english-hud-metrics-grid">
              <div class="english-hud-tile" title="Segregated GMAT Verbal Readiness (Critical Reasoning + Reading Comprehension)">
                <div class="hud-tile-header">
                  <span class="hud-tile-label">Verbal Readiness</span>
                  <span class="hud-tile-pill green">${verbalTier}</span>
                </div>
                <div class="hud-tile-val verbal-accent">${verbalReadiness}<small style="font-size: 13px; color: #64748b; font-weight: 600;">/100</small></div>
                <div class="hud-tile-sub">CR & RC Scaled Score</div>
              </div>
              <div style="height: 32px; width: 1px; background: #e2e8f0;"></div>
              <div style="text-align: center;">
                <span style="font-size: 11px; color: #64748b; text-transform: uppercase; font-weight: 700;">Accuracy</span>
                <div style="font-size: 18px; font-weight: 800; color: #1e3a5f;">${accuracy}</div>

              <div class="english-hud-tile" title="Segregated Foundation Readiness (Grammar Rules + GMAT Vocabulary)">
                <div class="hud-tile-header">
                  <span class="hud-tile-label">Foundation</span>
                  <span class="hud-tile-pill blue">${foundationTier}</span>
                </div>
                <div class="hud-tile-val foundation-accent">${foundationReadiness}<small style="font-size: 13px; color: #64748b; font-weight: 600;">/100</small></div>
                <div class="hud-tile-sub">Grammar & Vocab Mastery</div>
              </div>
              <div style="height: 32px; width: 1px; background: #e2e8f0;"></div>
              <div style="text-align: center;">
                <span style="font-size: 11px; color: #64748b; text-transform: uppercase; font-weight: 700;">CR Avg Pace</span>
                <div style="font-size: 18px; font-weight: 800; color: #2563eb;">${crAvg}</div>

              <div class="english-hud-tile" title="Estimated Overall Readiness Band">
                <div class="hud-tile-header">
                  <span class="hud-tile-label">Estimated Band</span>
                  <span class="hud-tile-pill amber">Pathway</span>
                </div>
                <div class="hud-tile-val" style="color: #4338ca; font-size: 18px;">${compositeBand}</div>
                <div class="hud-tile-sub">Target 700+ GMAT Pathway</div>
              </div>
              <div style="height: 32px; width: 1px; background: #e2e8f0;"></div>
              <div style="text-align: center;">
                <span style="font-size: 11px; color: #64748b; text-transform: uppercase; font-weight: 700;">RC Avg Pace</span>
                <div style="font-size: 18px; font-weight: 800; color: #b45309;">${rcAvg}</div>

              <div class="english-hud-tile" title="Pacing and Accuracy Metrics">
                <div class="hud-tile-header">
                  <span class="hud-tile-label">Accuracy & Pace</span>
                  <span style="font-size: 12px; font-weight: 700; color: #0f172a;">${accuracy}</span>
                </div>
                <div class="hud-tile-val pace-accent" style="font-size: 18px;">CR: ${crAvg} <small style="font-size: 11.5px; color: #64748b;">• RC: ${rcAvg}</small></div>
                <div class="hud-tile-sub">CR Target: ~120s / question</div>
              </div>
              <div style="height: 32px; width: 1px; background: #e2e8f0;"></div>
              <div style="text-align: center;">
                <span style="font-size: 11px; color: #64748b; text-transform: uppercase; font-weight: 700;">Streak</span>
                <div style="font-size: 18px; font-weight: 800; color: #ea580c;">🔥 ${streak}</div>

              <div class="english-hud-tile" title="Daily Practice Streak and Solved Questions">
                <div class="hud-tile-header">
                  <span class="hud-tile-label">Daily Streak</span>
                  <span style="font-size: 11px; font-weight: 700; color: #ea580c;">ACTIVE</span>
                </div>
                <div class="hud-tile-val streak-accent">🔥 ${streak}</div>
                <div class="hud-tile-sub">Total Solved: ${totalSolved} Qs</div>
              </div>
            </div>
          </header>
          </section>

          ${resumeBannerHtml}

          ${onboardingHtml}

          ${dailyPlanHtml}

          <!-- 3 Subtabs Navigation -->
          <nav class="english-subtabs" style="display: flex; gap: 8px; border-bottom: 2px solid #e2e8f0; margin-bottom: 24px;">
            <button class="english-subtab-btn ${this.activeSubtab === 'gmat_verbal' ? 'is-active' : ''}" data-subtab="gmat_verbal" type="button" style="padding: 10px 18px; font-weight: 700; font-size: 14px; background: none; border: none; border-bottom: 3px solid ${this.activeSubtab === 'gmat_verbal' ? '#1e3a5f' : 'transparent'}; color: ${this.activeSubtab === 'gmat_verbal' ? '#1e3a5f' : '#64748b'}; cursor: pointer;">
              📚 GMAT Verbal Reasoning
            </button>
            <button class="english-subtab-btn ${this.activeSubtab === 'foundation' ? 'is-active' : ''}" data-subtab="foundation" type="button" style="padding: 10px 18px; font-weight: 700; font-size: 14px; background: none; border: none; border-bottom: 3px solid ${this.activeSubtab === 'foundation' ? '#0f766e' : 'transparent'}; color: ${this.activeSubtab === 'foundation' ? '#0f766e' : '#64748b'}; cursor: pointer;">
              🌱 English Foundation
            </button>
            <button class="english-subtab-btn ${this.activeSubtab === 'progress' ? 'is-active' : ''}" data-subtab="progress" type="button" style="padding: 10px 18px; font-weight: 700; font-size: 14px; background: none; border: none; border-bottom: 3px solid ${this.activeSubtab === 'progress' ? '#2563eb' : 'transparent'}; color: ${this.activeSubtab === 'progress' ? '#2563eb' : '#64748b'}; cursor: pointer;">
              📈 Verbal Progress & Trajectory
            </button>
          <!-- 3 Modern Subtabs Navigation -->
          <nav class="english-subtabs-bar" aria-label="Section Navigation">
            <div class="english-subtabs-pills">
              <button class="english-subtab-btn english-subtab-pill ${this.activeSubtab === 'gmat_verbal' ? 'is-active' : ''}" data-subtab="gmat_verbal" type="button">
                📚 GMAT Verbal Reasoning
              </button>
              <button class="english-subtab-btn english-subtab-pill ${this.activeSubtab === 'foundation' ? 'is-active' : ''}" data-subtab="foundation" type="button">
                🌱 English Foundation
              </button>
              <button class="english-subtab-btn english-subtab-pill ${this.activeSubtab === 'progress' ? 'is-active' : ''}" data-subtab="progress" type="button">
                📈 Verbal Progress & Trajectory
              </button>
            </div>
          </nav>

          <!-- Subtab View Container -->
          <div id="englishSubtabContent"></div>

          <!-- Active Question Runner Screen Container -->
          <div id="englishQuestionView" style="margin-top: 10px;"></div>
        </div>
      `;

      // Event listener for subtabs
      // Subtab clicks
      screen.querySelectorAll(".english-subtab-btn").forEach((btn) => {
        btn.addEventListener("click", () => {
          self.activeSubtab = btn.dataset.subtab;
          self.renderMainLayout(screen, overview, activeSession, studyPlan, beginnerProfile);
        });
      });

      // Top AI toggle button
      const topAiBtn = screen.querySelector("#toggleAiModeTopBtn");
      if (topAiBtn) {
        topAiBtn.addEventListener("click", () => {
          self.isAiMode = !self.isAiMode;
          try {
            localStorage.setItem("gmat_english_ai_mode", self.isAiMode ? "true" : "false");
          } catch (e) {}
          self.renderMainLayout(screen, overview, activeSession, studyPlan, beginnerProfile);
        });
      }

      // Resume & Discard listeners
      const resumeBtn = screen.querySelector("#engResumeBtn");
      if (resumeBtn) {
        resumeBtn.addEventListener("click", () => {
          self.resumeActiveSession(activeSession);
        });
      }
      const discardBtn = screen.querySelector("#engDiscardBtn");
      if (discardBtn) {
        discardBtn.addEventListener("click", () => {
          if (window.EnglishOverlayManager && typeof EnglishOverlayManager.confirmExit === "function") {
            EnglishOverlayManager.confirmExit(async () => {
              if (window.AptitudeEnglishDB) {
                await window.AptitudeEnglishDB.clearActiveEnglishSession();
              }
              self.init();
            });
          } else {
            if (window.AptitudeEnglishDB) {
              window.AptitudeEnglishDB.clearActiveEnglishSession().then(() => self.init());
            } else {
              self.init();
            }
          }
        });
      }

      // Onboarding level card clicks
      screen.querySelectorAll(".english-level-card").forEach((card) => {
        card.addEventListener("click", async () => {
          const levelKey = card.dataset.level;
          if (window.AptitudeEnglishDB) {
            await window.AptitudeEnglishDB.saveBeginnerProfile({
              level: levelKey,
              updated_at: new Date().toISOString(),
            });
          }
          self.init();
        });
      });

      // Daily task action buttons
      screen.querySelectorAll(".daily-task-action-btn").forEach((btn) => {
        btn.addEventListener("click", () => {
          const actionType = btn.dataset.actionType;
          const dayNum = Number(btn.dataset.day);
          const taskId = btn.dataset.taskId;
          const today = (studyPlan && studyPlan.days) ? studyPlan.days.find(d => d.day === dayNum) : null;
          const task = today ? (today.tasks || []).find(t => t.id === taskId) : null;

          if (actionType === "vocab") {
            self.startFlashcards({
              day_number: dayNum,
              task_id: taskId,
              count: (task && task.target) || 10
            });
          } else {
            const taskAction = (task && task.action) || {};
            self.startPracticeSession({
              ...taskAction,
              day_number: dayNum,
              task_id: taskId,
            });
          }
        });
      });

      // Schedule adjust button
      const adjustBtn = screen.querySelector("#engAdjustScheduleBtn");
      if (adjustBtn) {
        adjustBtn.addEventListener("click", async () => {
          EnglishOverlayManager.confirmExit(async () => {
            if (window.AptitudeEnglishDB) {
              await window.AptitudeEnglishDB.recalculateStudySchedule(new Date().toISOString().slice(0, 10));
            }
            self.init();
          });
        });
      }

      // Render the active subtab content
      const contentEl = screen.querySelector("#englishSubtabContent");
      if (this.activeSubtab === "gmat_verbal") {
        this.renderGmatVerbalTab(contentEl, overview);
      } else if (this.activeSubtab === "foundation") {
        this.renderFoundationTab(contentEl, overview);
      } else if (this.activeSubtab === "progress") {
        this.renderProgressTab(contentEl, overview);
      }
    },

    // -----------------------------------------------------------------------
    // SUBTAB 1: GMAT VERBAL REASONING
    // -----------------------------------------------------------------------
    renderGmatVerbalTab: function (container, overview) {
      const self = this;
      const crCount = (window.ENGLISH_DATA && window.ENGLISH_DATA.CR_QUESTIONS) ? window.ENGLISH_DATA.CR_QUESTIONS.length : 20;
      const rcPassageCount = (window.ENGLISH_DATA && window.ENGLISH_DATA.RC_PASSAGES) ? window.ENGLISH_DATA.RC_PASSAGES.length : 8;
      const rcQCount = (window.ENGLISH_DATA && window.ENGLISH_DATA.RC_QUESTIONS) ? window.ENGLISH_DATA.RC_QUESTIONS.length : 24;

      container.innerHTML = `
        <div style="display: flex; flex-direction: column; gap: 24px;">
          <!-- Adaptive AI Generator Banner -->
          <div style="background: linear-gradient(135deg, ${self.isAiMode ? '#f0fdf4, #eff6ff' : '#f8fafc, #f1f5f9'}); border: 1.5px solid ${self.isAiMode ? '#86efac' : '#cbd5e1'}; border-radius: 12px; padding: 16px 20px; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 16px; box-shadow: 0 2px 5px rgba(0,0,0,0.03);">
            <div style="display: flex; align-items: center; gap: 14px; max-width: 620px;">
              <div style="font-size: 28px; background: #fff; width: 48px; height: 48px; border-radius: 10px; display: flex; align-items: center; justify-content: center; box-shadow: 0 2px 4px rgba(0,0,0,0.06); border: 1px solid #e2e8f0;">
                ${self.isAiMode ? '🤖' : '📚'}
              </div>
              <div>
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 3px;">
                  <strong style="color: #1e3a5f; font-size: 15px;">Dynamic AI Question Generator</strong>
                  <span style="font-size: 11px; font-weight: 700; padding: 2px 8px; border-radius: 12px; background: ${self.isAiMode ? '#dcfce7; color: #166534' : '#e2e8f0; color: #475569'};">
                    ${self.isAiMode ? '● ACTIVE' : 'OFFLINE BANK'}
                  </span>
                </div>
                <div style="font-size: 13px; color: #475569; line-height: 1.4;">
                  ${self.isAiMode
                    ? 'Generates non-repeating GMAT questions with adaptive difficulty (Levels 1-5) and official trap patterns based on your real-time accuracy.'
                    : 'Using standardized curated questions from the offline question bank.'}
                </div>
              </div>
            </div>
            <div>
              <button id="toggleAiModeVerbalBtn" class="english-btn" style="background: ${self.isAiMode ? '#166534' : '#1e3a5f'}; color: #fff; padding: 10px 18px; font-weight: 600; font-size: 13px; border-radius: 8px; display: flex; align-items: center; gap: 8px; cursor: pointer;" type="button">
                <span>${self.isAiMode ? '✓ AI Mode Active (Click to Switch)' : '⚡ Switch to AI Generator'}</span>
              </button>
            </div>
          </div>

          <!-- Section Selector (Critical Reasoning vs Reading Comprehension) -->
          <div>
            <h3 style="margin: 0 0 12px; font-size: 16px; color: #1e3a5f; text-transform: uppercase; letter-spacing: 0.04em;">
              1. Verbal Section Selector
            </h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 16px;">
              <!-- CR Card -->
              <div class="cr-stimulus-card" style="display: flex; flex-direction: column; justify-content: space-between; border-left: 5px solid #2563eb;">
                <div>
                  <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span class="english-badge" style="background: #eff6ff; color: #1d4ed8;">Critical Reasoning</span>
                    <span style="font-size: 12px; color: #64748b; font-weight: 600;">${crCount} Available</span>
                  </div>
                  <h4 style="margin: 10px 0 6px; font-size: 18px; color: #1e3a5f;">Critical Reasoning Practice</h4>
                  <p style="font-size: 13.5px; color: #475569; line-height: 1.5; margin-bottom: 12px;">
                    Strengthen, Weaken, Assumption, Inference, Paradox, and Flaw in Reasoning. Features Premise & Conclusion demarcation, choice elimination, and trap analysis.
                  </p>
                  <div style="display: flex; gap: 14px; font-size: 12px; color: #64748b; margin-bottom: 14px;">
                    <span>Target: <strong>~120s / question</strong></span>
                    <span>Format: <strong>5 Choices (A-E)</strong></span>
                  </div>
                </div>
                <div style="display: flex; gap: 10px;">
                  <button class="english-btn english-btn-primary" style="flex: 1;" type="button" id="startCrDrillBtn">
                    Start CR Drill →
                  </button>
                </div>
              </div>

              <!-- RC Card -->
              <div class="cr-stimulus-card" style="display: flex; flex-direction: column; justify-content: space-between; border-left: 5px solid #b45309;">
                <div>
                  <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span class="english-badge" style="background: #fffbeb; color: #b45309;">Reading Comprehension</span>
                    <span style="font-size: 12px; color: #64748b; font-weight: 600;">${rcPassageCount} Passages (${rcQCount} Qs)</span>
                  </div>
                  <h4 style="margin: 10px 0 6px; font-size: 18px; color: #1e3a5f;">Reading Comprehension Practice</h4>
                  <p style="font-size: 13.5px; color: #475569; line-height: 1.5; margin-bottom: 12px;">
                    Multi-paragraph passages covering Business, Economics, Science, Technology, History, Environment, and Culture. Features desktop 2-column split-pane and dual reading/solving timer.
                  </p>
                  <div style="display: flex; gap: 14px; font-size: 12px; color: #64748b; margin-bottom: 14px;">
                    <span>Reading Pace: <strong>Tracked separately</strong></span>
                    <span>Layout: <strong>Split-Pane</strong></span>
                  </div>
                </div>
                <div style="display: flex; gap: 10px;">
                  <button class="english-btn english-btn-primary" style="flex: 1; background: #b45309; border-color: #b45309;" type="button" id="startRcDrillBtn">
                    Start RC Drill →
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- Quick Practice Actions & Simulation -->
          <div>
            <h3 style="margin: 0 0 12px; font-size: 16px; color: #1e3a5f; text-transform: uppercase; letter-spacing: 0.04em;">
              2. Quick Practice Actions & Simulations
            </h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 14px;">
              <button class="english-btn english-btn-secondary" style="padding: 14px 16px; text-align: left; height: auto;" type="button" id="quick5DrillBtn">
                <div style="font-weight: 700; color: #1e3a5f; font-size: 14px;">⚡ 5-Question Drill</div>
                <div style="font-size: 12px; color: #64748b; margin-top: 4px;">Quick 10-minute warm-up</div>
              </button>
              <button class="english-btn english-btn-secondary" style="padding: 14px 16px; text-align: left; height: auto;" type="button" id="quick10DrillBtn">
                <div style="font-weight: 700; color: #1e3a5f; font-size: 14px;">🎯 10-Question Drill</div>
                <div style="font-size: 12px; color: #64748b; margin-top: 4px;">Standard mixed set (~20 mins)</div>
              </button>
              <button class="english-btn english-btn-secondary" style="padding: 14px 16px; text-align: left; height: auto;" type="button" id="quick20DrillBtn">
                <div style="font-weight: 700; color: #1e3a5f; font-size: 14px;">🔥 20-Question Drill</div>
                <div style="font-size: 12px; color: #64748b; margin-top: 4px;">Endurance practice (~40 mins)</div>
              </button>
              <button class="english-btn" style="padding: 14px 16px; text-align: left; height: auto; background: #1e3a5f; color: #fff;" type="button" id="sim45Btn">
                <div style="font-weight: 700; font-size: 14px; color: #fde047;">🏆 45-Min Verbal Simulation</div>
                <div style="font-size: 12px; opacity: 0.9; margin-top: 4px;">23 Questions, 45:00 Exam Mode</div>
              </button>
              <button class="english-btn english-btn-secondary" style="padding: 14px 16px; text-align: left; height: auto;" type="button" id="verbalDiagBtn">
                <div style="font-weight: 700; color: #1e3a5f; font-size: 14px;">🔬 Verbal Diagnostic</div>
                <div style="font-size: 12px; color: #64748b; margin-top: 4px;">15-question baseline assessment</div>
              </button>
              <button class="english-btn english-btn-secondary" style="padding: 14px 16px; text-align: left; height: auto;" type="button" id="practiceWeakBtn">
                <div style="font-weight: 700; color: #dc2626; font-size: 14px;">🥊 Practice Weak Topics</div>
                <div style="font-size: 12px; color: #64748b; margin-top: 4px;">Target historical error patterns</div>
              </button>
            </div>
          </div>
        </div>
      `;

      // Event listeners for AI toggle
      const toggleAiBtn = container.querySelector("#toggleAiModeVerbalBtn");
      if (toggleAiBtn) {
        toggleAiBtn.addEventListener("click", () => {
          self.isAiMode = !self.isAiMode;
          try {
            localStorage.setItem("gmat_english_ai_mode", self.isAiMode ? "true" : "false");
          } catch (e) {}
          self.renderGmatVerbalTab(container, overview);
        });
      }

      // Event listeners for actions
      container.querySelector("#startCrDrillBtn").addEventListener("click", () => {
        const crs = (window.ENGLISH_DATA && window.ENGLISH_DATA.CR_QUESTIONS) ? window.ENGLISH_DATA.CR_QUESTIONS : self.getCRQuestions();
        self.startPracticeSession({ mode: "drill", subsection: "Critical Reasoning", count: 10, questions: self.isAiMode ? null : crs.slice(0, 10) });
      });

      container.querySelector("#startRcDrillBtn").addEventListener("click", () => {
        const rcs = (window.ENGLISH_DATA && window.ENGLISH_DATA.RC_QUESTIONS) ? window.ENGLISH_DATA.RC_QUESTIONS : self.getRCQuestions();
        self.startPracticeSession({ mode: "drill", subsection: "Reading Comprehension", count: 8, questions: self.isAiMode ? null : rcs.slice(0, 8) });
      });

      container.querySelector("#quick5DrillBtn").addEventListener("click", () => {
        const pool = self.getMixedQuestions();
        self.startPracticeSession({ mode: "drill", count: 5, questions: self.isAiMode ? null : pool.slice(0, 5) });
      });

      container.querySelector("#quick10DrillBtn").addEventListener("click", () => {
        const pool = self.getMixedQuestions();
        self.startPracticeSession({ mode: "drill", count: 10, questions: self.isAiMode ? null : pool.slice(0, 10) });
      });

      container.querySelector("#quick20DrillBtn").addEventListener("click", () => {
        const pool = self.getMixedQuestions();
        self.startPracticeSession({ mode: "drill", count: 20, questions: self.isAiMode ? null : pool.slice(0, 20) });
      });

      container.querySelector("#sim45Btn").addEventListener("click", () => {
        self.startPracticeSession({ mode: "simulation", isSimulation: true });
      });

      container.querySelector("#verbalDiagBtn").addEventListener("click", () => {
        self.startPracticeSession({ mode: "verbal_diagnostic" });
      });

      container.querySelector("#practiceWeakBtn").addEventListener("click", () => {
        self.startPracticeSession({ mode: "weak" });
      });
    },

    // -----------------------------------------------------------------------
    // SUBTAB 2: ENGLISH FOUNDATION (Grammar & Vocabulary)
    // SUBTAB 2: ENGLISH FOUNDATION (Grammar & GMAT Vocabulary Hub)
    // -----------------------------------------------------------------------
    renderFoundationTab: function (container, overview) {
      const self = this;
      const grammarCount = (window.ENGLISH_DATA && window.ENGLISH_DATA.GRAMMAR_QUESTIONS) ? window.ENGLISH_DATA.GRAMMAR_QUESTIONS.length : 25;
      const vocabCount = (window.ENGLISH_DATA && window.ENGLISH_DATA.VOCABULARY_ITEMS) ? window.ENGLISH_DATA.VOCABULARY_ITEMS.length : 30;
      const vocabItems = (window.ENGLISH_DATA && Array.isArray(window.ENGLISH_DATA.VOCABULARY_ITEMS) && window.ENGLISH_DATA.VOCABULARY_ITEMS.length > 0)
        ? window.ENGLISH_DATA.VOCABULARY_ITEMS
        : BUILTIN_FLASHCARDS;
      const vocabCount = vocabItems.length;

      // Category word counts
      const catCounts = {
        all: vocabCount,
        "Argumentation & Logic": 0,
        "Author Tone & Attitude": 0,
        "Business & Economics": 0,
        "Science & Methodology": 0,
        "Foundation Bridge": 0,
      };
      vocabItems.forEach((v) => {
        if (v.category && catCounts[v.category] !== undefined) {
          catCounts[v.category]++;
        }
      });

      let currentCategory = "all";
      let currentQuery = "";

      container.innerHTML = `
        <div style="display: flex; flex-direction: column; gap: 24px;">
          <!-- Adaptive AI Generator Banner -->
          <div style="background: linear-gradient(135deg, ${self.isAiMode ? '#f0fdf4, #eff6ff' : '#f8fafc, #f1f5f9'}); border: 1.5px solid ${self.isAiMode ? '#86efac' : '#cbd5e1'}; border-radius: 12px; padding: 16px 20px; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 16px; box-shadow: 0 2px 5px rgba(0,0,0,0.03);">
            <div style="display: flex; align-items: center; gap: 14px; max-width: 620px;">
              <div style="font-size: 28px; background: #fff; width: 48px; height: 48px; border-radius: 10px; display: flex; align-items: center; justify-content: center; box-shadow: 0 2px 4px rgba(0,0,0,0.06); border: 1px solid #e2e8f0;">
                ${self.isAiMode ? '🤖' : '🌱'}
              </div>
              <div>
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 3px;">
                  <strong style="color: #166534; font-size: 15px;">Dynamic Foundation AI Generator</strong>
                  <span style="font-size: 11px; font-weight: 700; padding: 2px 8px; border-radius: 12px; background: ${self.isAiMode ? '#dcfce7; color: #166534' : '#e2e8f0; color: #475569'};">
                    ${self.isAiMode ? '● ACTIVE' : 'OFFLINE BANK'}
                  </span>
                </div>
                <div style="font-size: 13px; color: #475569; line-height: 1.4;">
                  ${self.isAiMode
                    ? 'Generates fresh, non-repeating grammar exercises with educational rule breakdowns and trap distractors scaled to your foundation level.'
                    : 'Serving standardized curated curriculum questions from the offline grammar bank.'}
                </div>
              </div>
            </div>
            <div>
              <button id="toggleAiModeFoundationBtn" class="english-btn" style="background: ${self.isAiMode ? '#166534' : '#0f766e'}; color: #fff; padding: 10px 18px; font-weight: 600; font-size: 13px; border-radius: 8px; display: flex; align-items: center; gap: 8px; cursor: pointer;" type="button">
                <span>${self.isAiMode ? '✓ AI Mode Active (Click to Switch)' : '⚡ Switch to AI Generator'}</span>
              </button>
            </div>
          </div>

          <!-- Level 1-4 Learning Path Roadmap -->
          <div class="cr-stimulus-card" style="background: #f0fdf4; border: 1px solid #bbf7d0;">
            <span class="english-badge foundation-badge">Curriculum Progression</span>
            <h3 style="margin: 8px 0 4px; font-size: 18px; color: #166534;">Foundation Learning Path</h3>
            <p style="font-size: 13.5px; color: #374151; margin-bottom: 16px;">
              Master structural fundamentals before transitioning to GMAT Verbal reasoning.
            </p>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 12px;">
              <div style="background: #fff; padding: 12px; border-radius: 8px; border: 1px solid #dcfce7;">
                <span style="font-size: 11px; font-weight: 700; color: #166534;">LEVEL 1</span>
                <h5 style="margin: 4px 0 2px; font-size: 13px; color: #111827;">Basic English</h5>
                <p style="font-size: 11.5px; color: #64748b; margin: 0;">Parts of speech, Subject-verb agreement, Basic vocabulary</p>
          <!-- Section A: Grammar Mastery & Curriculum Progression -->
          <div class="cr-stimulus-card" style="border-left: 5px solid #0f766e; background: #ffffff;">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 12px; margin-bottom: 14px;">
              <div>
                <span class="english-badge foundation-badge">Grammar Mastery & Rules</span>
                <h3 style="margin: 8px 0 4px; font-size: 19px; color: #1e3a5f;">Sentence Mechanics & Grammar Curriculum (${grammarCount} Questions)</h3>
                <p style="font-size: 13.5px; color: #475569; margin: 0; max-width: 720px; line-height: 1.5;">
                  Master Subject-Verb Agreement, Dangling Modifiers, Parallel Construction, Verb Tense sequences, and Idiomatic accuracy tested in GMAT reasoning.
                </p>
              </div>
              <div style="background: #fff; padding: 12px; border-radius: 8px; border: 1px solid #dcfce7;">
                <span style="font-size: 11px; font-weight: 700; color: #166534;">LEVEL 2</span>
                <h5 style="margin: 4px 0 2px; font-size: 13px; color: #111827;">Intermediate English</h5>
                <p style="font-size: 11.5px; color: #64748b; margin: 0;">Clauses, Modifiers, Parallelism, Comparisons</p>
              <div style="display: flex; gap: 10px; flex-wrap: wrap;">
                <button class="english-btn english-btn-primary" style="background: #0f766e; border-color: #0f766e;" type="button" id="startGrammarLearnBtn">
                  📖 Learn Mode (Instant Feedback)
                </button>
                <button class="english-btn english-btn-secondary" type="button" id="startGrammarDrillBtn">
                  ⚡ Timed Drill (10Q)
                </button>
                <button class="english-btn english-btn-secondary" type="button" id="startFoundationDiagBtn">
                  🔬 Diagnostic (16Q)
                </button>
              </div>
              <div style="background: #fff; padding: 12px; border-radius: 8px; border: 1px solid #dcfce7;">
                <span style="font-size: 11px; font-weight: 700; color: #166534;">LEVEL 3</span>
                <h5 style="margin: 4px 0 2px; font-size: 13px; color: #111827;">Advanced Foundation</h5>
                <p style="font-size: 11.5px; color: #64748b; margin: 0;">Concision, Sentence logic, Academic vocabulary</p>
            </div>

            <!-- Curriculum Level Roadmap -->
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 12px; margin-top: 14px; border-top: 1px solid #f1f5f9; padding-top: 14px;">
              <div style="background: #f8fafc; padding: 12px 14px; border-radius: 8px; border: 1px solid #e2e8f0;">
                <span style="font-size: 11px; font-weight: 700; color: #0f766e;">LEVEL 1 • BASIC</span>
                <h5 style="margin: 4px 0 2px; font-size: 13px; color: #0f172a;">Parts of Speech</h5>
                <p style="font-size: 11.5px; color: #64748b; margin: 0;">Subject-verb number agreement, pronoun references</p>
              </div>
              <div style="background: #fff; padding: 12px; border-radius: 8px; border: 1px solid #dcfce7;">
                <span style="font-size: 11px; font-weight: 700; color: #166534;">LEVEL 4</span>
                <h5 style="margin: 4px 0 2px; font-size: 13px; color: #111827;">GMAT Bridge</h5>
                <p style="font-size: 11.5px; color: #64748b; margin: 0;">Argument terminology, Cause-and-effect language</p>
              <div style="background: #f8fafc; padding: 12px 14px; border-radius: 8px; border: 1px solid #e2e8f0;">
                <span style="font-size: 11px; font-weight: 700; color: #0f766e;">LEVEL 2 • INTERMEDIATE</span>
                <h5 style="margin: 4px 0 2px; font-size: 13px; color: #0f172a;">Modifiers & Clauses</h5>
                <p style="font-size: 11.5px; color: #64748b; margin: 0;">Participial modifiers, relative clauses, parallelism</p>
              </div>
              <div style="background: #f8fafc; padding: 12px 14px; border-radius: 8px; border: 1px solid #e2e8f0;">
                <span style="font-size: 11px; font-weight: 700; color: #0f766e;">LEVEL 3 • ADVANCED</span>
                <h5 style="margin: 4px 0 2px; font-size: 13px; color: #0f172a;">Concision & Logic</h5>
                <p style="font-size: 11.5px; color: #64748b; margin: 0;">Passive vs active voice, elliptical comparisons, correlatives</p>
              </div>
              <div style="background: #f8fafc; padding: 12px 14px; border-radius: 8px; border: 1px solid #e2e8f0;">
                <span style="font-size: 11px; font-weight: 700; color: #0f766e;">LEVEL 4 • GMAT BRIDGE</span>
                <h5 style="margin: 4px 0 2px; font-size: 13px; color: #0f172a;">Argument Syntax</h5>
                <p style="font-size: 11.5px; color: #64748b; margin: 0;">Subordinating counter-evidence, causal link phrases</p>
              </div>
            </div>
          </div>

          <!-- Practice Modes (Grammar Drills & Vocabulary SRS) -->
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 16px;">
            <!-- Grammar Section -->
            <div class="cr-stimulus-card" style="border-left: 5px solid #0f766e;">
              <span class="english-badge foundation-badge">Grammar Mastery</span>
              <h4 style="margin: 10px 0 6px; font-size: 18px; color: #1e3a5f;">Grammar Practice (${grammarCount} Questions)</h4>
              <p style="font-size: 13.5px; color: #475569; line-height: 1.5; margin-bottom: 12px;">
                Subject-verb agreement, modifiers, parallelism, and verb tenses with complete educational rule explanations, examples, and memory aids.
              </p>
              <div style="display: flex; gap: 10px; margin-top: 16px;">
                <button class="english-btn english-btn-primary" style="flex: 1; background: #0f766e; border-color: #0f766e;" type="button" id="startGrammarLearnBtn">
                  📖 Learn Mode (Instant Feedback)
          <!-- Section B: Authentic GMAT Vocabulary Hub (131 Words) -->
          <section class="english-vocab-hub" aria-label="GMAT Vocabulary Hub">
            <div class="vocab-hub-topbar">
              <div>
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px;">
                  <span class="english-badge" style="background: #dcfce7; color: #166534; border-color: #bbf7d0;">
                    ${vocabCount} GMAT High-Frequency Words
                  </span>
                  <span style="font-size: 12px; color: #64748b; font-weight: 600;">Spaced Repetition System</span>
                </div>
                <h3 style="margin: 4px 0; font-size: 20px; font-weight: 800; color: #0f172a;">
                  GMAT Vocabulary Hub & Word Explorer
                </h3>
                <p style="margin: 0; font-size: 13px; color: #64748b;">
                  Targeted vocabulary for Critical Reasoning and Reading Comprehension across 5 exam domains.
                </p>
              </div>

              <!-- Top Actions: SRS Deck Launchers -->
              <div style="display: flex; gap: 10px; flex-wrap: wrap;">
                <button class="english-btn english-btn-primary" id="openFlashcardsBtn" style="background: #16a34a; border-color: #16a34a; font-size: 13px;" type="button">
                  🗂 Open Flashcards SRS (<span id="activeDeckCountLabel">${vocabCount}</span> Cards) →
                </button>
                <button class="english-btn english-btn-secondary" type="button" id="startGrammarDrillBtn">
                  ⚡ Timed Drill
                <button class="english-btn english-btn-secondary" id="vocabQuick10Btn" style="font-size: 13px;" type="button">
                  ⚡ Quick 10-Card Drill
                </button>
              </div>
            </div>

            <!-- Vocabulary Section -->
            <div class="cr-stimulus-card" style="border-left: 5px solid #16a34a;">
              <span class="english-badge foundation-badge">Spaced Repetition</span>
              <h4 style="margin: 10px 0 6px; font-size: 18px; color: #1e3a5f;">Vocabulary & 3D Flashcards (${vocabCount} Words)</h4>
              <p style="font-size: 13.5px; color: #475569; line-height: 1.5; margin-bottom: 12px;">
                Academic, business, and economic vocabulary with 3D flip card flashcards and Leitner Spaced Repetition (1d, 3d, 7d, 14d, 30d).
              </p>
              <div style="display: flex; gap: 10px; margin-top: 16px;">
                <button class="english-btn english-btn-primary" style="flex: 1; background: #16a34a; border-color: #16a34a;" type="button" id="openFlashcardsBtn">
                  🗂 Open Flashcards SRS →
                </button>
                <button class="english-btn english-btn-secondary" type="button" id="startFoundationDiagBtn">
                  🔬 Diagnostic (16Q)
                </button>
            <!-- Categories and Search Bar -->
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 14px; border-top: 1px solid #f1f5f9; padding-top: 14px;">
              <div class="vocab-categories-bar" id="vocabCatBar">
                <button class="vocab-cat-chip is-active" data-cat="all" type="button">All (${vocabCount})</button>
                <button class="vocab-cat-chip" data-cat="Argumentation & Logic" type="button">Argumentation & Logic (${catCounts['Argumentation & Logic'] || 0})</button>
                <button class="vocab-cat-chip" data-cat="Author Tone & Attitude" type="button">Author Tone (${catCounts['Author Tone & Attitude'] || 0})</button>
                <button class="vocab-cat-chip" data-cat="Business & Economics" type="button">Business & Econ (${catCounts['Business & Economics'] || 0})</button>
                <button class="vocab-cat-chip" data-cat="Science & Methodology" type="button">Science & Method (${catCounts['Science & Methodology'] || 0})</button>
                <button class="vocab-cat-chip" data-cat="Foundation Bridge" type="button">Foundation Bridge (${catCounts['Foundation Bridge'] || 0})</button>
              </div>

              <div class="vocab-search-wrap">
                <span class="vocab-search-icon">🔍</span>
                <input type="text" id="vocabSearchInput" class="vocab-search-input" placeholder="Search 131 words, traps, synonyms..." autocomplete="off">
              </div>
            </div>
          </div>

            <!-- Real-time Filter Count / Status -->
            <div style="display: flex; justify-content: space-between; align-items: center; font-size: 12px; color: #64748b; margin-top: -6px;">
              <span id="vocabFilterStatus">Showing all ${vocabCount} GMAT vocabulary words</span>
              <span>Click any card to launch 3D flashcard review</span>
            </div>

            <!-- Word Explorer Grid -->
            <div class="vocab-word-grid" id="vocabWordGrid">
              <!-- Dynamically populated -->
            </div>
          </section>
        </div>
      `;

      // Helper function to filter items
      function getFilteredItems() {
        return vocabItems.filter((item) => {
          const matchesCat = currentCategory === "all" || item.category === currentCategory;
          if (!matchesCat) return false;
          if (!currentQuery) return true;
          const q = currentQuery.toLowerCase();
          const w = (item.word || "").toLowerCase();
          const def = (item.definition || "").toLowerCase();
          const ctxt = (item.contextual_meaning || "").toLowerCase();
          const trap = (item.common_confusion || "").toLowerCase();
          const syns = Array.isArray(item.synonyms) ? item.synonyms.join(" ").toLowerCase() : "";
          return w.includes(q) || def.includes(q) || ctxt.includes(q) || trap.includes(q) || syns.includes(q);
        });
      }

      // Helper function to render cards into #vocabWordGrid
      function updateGrid() {
        const filtered = getFilteredItems();
        const gridEl = container.querySelector("#vocabWordGrid");
        const countLabel = container.querySelector("#activeDeckCountLabel");
        const statusLabel = container.querySelector("#vocabFilterStatus");

        if (countLabel) countLabel.textContent = filtered.length;
        if (statusLabel) {
          statusLabel.textContent = `Showing ${filtered.length} of ${vocabCount} words${currentCategory !== 'all' ? ` in ${currentCategory}` : ''}${currentQuery ? ` matching "${currentQuery}"` : ''}`;
        }

        if (!gridEl) return;

        if (filtered.length === 0) {
          gridEl.innerHTML = `
            <div style="grid-column: 1 / -1; text-align: center; padding: 40px 20px; color: #64748b;">
              <div style="font-size: 32px; margin-bottom: 8px;">🔍</div>
              <h4 style="margin: 0 0 4px; color: #1e293b;">No vocabulary words found</h4>
              <p style="margin: 0; font-size: 13px;">Try clearing your search query or choosing another category.</p>
            </div>
          `;
          return;
        }

        gridEl.innerHTML = filtered.map((item) => {
          const synHtml = Array.isArray(item.synonyms) && item.synonyms.length > 0
            ? item.synonyms.slice(0, 4).map((s) => `<span class="vocab-syn-tag">${s}</span>`).join("")
            : "";
          return `
            <div class="vocab-word-card" data-word="${item.word}">
              <div style="display: flex; flex-direction: column; gap: 8px;">
                <div class="vocab-card-header">
                  <div>
                    <span class="vocab-word-title">${item.word}</span>
                    <span class="vocab-word-pos">${item.part_of_speech || ''}</span>
                  </div>
                  <span class="vocab-category-badge">${item.category || 'GMAT'}</span>
                </div>

                <p class="vocab-def-text">${item.definition}</p>

                ${item.contextual_meaning ? `
                  <div class="vocab-gmat-context">
                    <strong>GMAT Nuance:</strong> ${item.contextual_meaning}
                  </div>
                ` : ''}

                ${item.common_confusion ? `
                  <div class="vocab-trap-box">
                    <strong>⚠️ Common Trap:</strong> ${item.common_confusion}
                  </div>
                ` : ''}

                ${synHtml ? `
                  <div class="vocab-syn-list">
                    ${synHtml}
                  </div>
                ` : ''}
              </div>

              <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 10px; border-top: 1px solid #f1f5f9; padding-top: 10px;">
                <span style="font-size: 11px; color: #94a3b8;">${item.root_prefix_suffix || 'GMAT Vocabulary'}</span>
                <button class="english-btn english-btn-ghost practice-word-btn" style="padding: 4px 10px; font-size: 12px; color: #0f766e; border-color: #cbd5e1;" data-word="${item.word}" type="button">
                  🗂 3D Card
                </button>
              </div>
            </div>
          `;
        }).join("");

        // Attach per-card click listener
        gridEl.querySelectorAll(".practice-word-btn").forEach((btn) => {
          btn.addEventListener("click", (e) => {
            e.stopPropagation();
            const wName = btn.dataset.word;
            const cardObj = vocabItems.find((v) => v.word.toLowerCase() === wName.toLowerCase());
            if (cardObj) {
              self.startFlashcards({ deck: [cardObj] });
            }
          });
        });

        gridEl.querySelectorAll(".vocab-word-card").forEach((card) => {
          card.addEventListener("click", () => {
            const wName = card.dataset.word;
            const cardObj = vocabItems.find((v) => v.word.toLowerCase() === wName.toLowerCase());
            if (cardObj) {
              self.startFlashcards({ deck: [cardObj] });
            }
          });
        });
      }

      updateGrid();

      // Event listener for AI toggle
      const toggleAiBtn = container.querySelector("#toggleAiModeFoundationBtn");
      if (toggleAiBtn) {
        toggleAiBtn.addEventListener("click", () => {
          self.isAiMode = !self.isAiMode;
          try {
            localStorage.setItem("gmat_english_ai_mode", self.isAiMode ? "true" : "false");
          } catch (e) {}
          self.renderFoundationTab(container, overview);
        });
      }

      // Event listeners
      // Event listeners for Grammar
      container.querySelector("#startGrammarLearnBtn").addEventListener("click", () => {
        const qs = (window.ENGLISH_DATA && window.ENGLISH_DATA.GRAMMAR_QUESTIONS) ? window.ENGLISH_DATA.GRAMMAR_QUESTIONS : [];
        self.startPracticeSession({ mode: "untimed", subsection: "Grammar", count: 10, questions: self.isAiMode ? null : qs });
      });

      container.querySelector("#startGrammarDrillBtn").addEventListener("click", () => {
        const qs = (window.ENGLISH_DATA && window.ENGLISH_DATA.GRAMMAR_QUESTIONS) ? window.ENGLISH_DATA.GRAMMAR_QUESTIONS : [];
        self.startPracticeSession({ mode: "drill", subsection: "Grammar", count: 10, questions: self.isAiMode ? null : qs });
      });

      container.querySelector("#startFoundationDiagBtn").addEventListener("click", () => {
        self.startPracticeSession({ mode: "foundation_diagnostic" });
      });

      // Category filter chips
      container.querySelectorAll(".vocab-cat-chip").forEach((chip) => {
        chip.addEventListener("click", () => {
          container.querySelectorAll(".vocab-cat-chip").forEach((c) => c.classList.remove("is-active"));
          chip.classList.add("is-active");
          currentCategory = chip.dataset.cat;
          updateGrid();
        });
      });

      // Search input live filtering
      const searchInput = container.querySelector("#vocabSearchInput");
      if (searchInput) {
        searchInput.addEventListener("input", (e) => {
          currentQuery = e.target.value.trim();
          updateGrid();
        });
      }

      // Open Flashcards SRS button
      container.querySelector("#openFlashcardsBtn").addEventListener("click", () => {
        self.startFlashcards();
        const filtered = getFilteredItems();
        self.startFlashcards({ deck: filtered.length > 0 ? filtered : vocabItems });
      });

      container.querySelector("#startFoundationDiagBtn").addEventListener("click", () => {
        self.startPracticeSession({ mode: "foundation_diagnostic" });
      });
      // Quick 10-card drill button
      const quick10Btn = container.querySelector("#vocabQuick10Btn");
      if (quick10Btn) {
        quick10Btn.addEventListener("click", () => {
          const filtered = getFilteredItems();
          self.startFlashcards({ deck: filtered.length > 0 ? filtered : vocabItems, count: 10 });
        });
      }
    },

    // -----------------------------------------------------------------------
    // SUBTAB 3: VERBAL PROGRESS & VARIANT TRAJECTORY
    // -----------------------------------------------------------------------
    renderProgressTab: async function (container, overview) {
      const self = this;
      let attempts = [];
      let metrics = null;
      let studyPlan = null;

      if (window.AptitudeEnglishDB) {
        try {
          attempts = await window.AptitudeEnglishDB.getAllEnglishAttempts();
          metrics = await window.AptitudeEnglishDB.getEnglishSectionMetrics();
          studyPlan = await window.AptitudeEnglishDB.getEnglishStudyPlan();
        } catch (e) {
          console.warn("Could not load progress data:", e);
        }
      }

      let trajectory = null;
      if (window.AptitudeEnglishDB && typeof window.AptitudeEnglishDB.getEnglishVariantTrajectory === "function") {
        try {
          trajectory = await window.AptitudeEnglishDB.getEnglishVariantTrajectory(self.currentTrajectoryVariant);
        } catch (e) {
          console.warn("Could not load trajectory:", e);
        }
      }

      const mistakes = attempts.filter((a) => !a.is_correct);

      container.innerHTML = `
        <div style="display: flex; flex-direction: column; gap: 24px;">
          <!-- Segregated CR vs RC KPIs -->
          <div>
            <h3 style="margin: 0 0 12px; font-size: 16px; color: #1e3a5f; text-transform: uppercase; letter-spacing: 0.04em;">
              1. Isolated Section Performance
            </h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px;">
              <div class="cr-stimulus-card" style="border-left: 5px solid #2563eb;">
                <h4 style="margin: 0 0 8px; font-size: 16px; color: #1e3a5f;">Critical Reasoning</h4>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                  <div>
                    <span style="font-size: 11px; color: #64748b;">Accuracy:</span>
                    <div style="font-size: 20px; font-weight: 800; color: #2563eb;">${metrics && metrics.critical_reasoning ? metrics.critical_reasoning.accuracy : 0}%</div>
                  </div>
                  <div>
                    <span style="font-size: 11px; color: #64748b;">Avg Pace:</span>
                    <div style="font-size: 20px; font-weight: 800; color: #1e3a5f;">${metrics && metrics.critical_reasoning ? metrics.critical_reasoning.avg_time : 0}s</div>
                  </div>
                </div>
              </div>

              <div class="cr-stimulus-card" style="border-left: 5px solid #b45309;">
                <h4 style="margin: 0 0 8px; font-size: 16px; color: #1e3a5f;">Reading Comprehension</h4>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                  <div>
                    <span style="font-size: 11px; color: #64748b;">Accuracy:</span>
                    <div style="font-size: 20px; font-weight: 800; color: #b45309;">${metrics && metrics.reading_comprehension ? metrics.reading_comprehension.accuracy : 0}%</div>
                  </div>
                  <div>
                    <span style="font-size: 11px; color: #64748b;">Question Pace:</span>
                    <div style="font-size: 20px; font-weight: 800; color: #1e3a5f;">${metrics && metrics.reading_comprehension ? metrics.reading_comprehension.avg_question_time : 0}s</div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Variant-Specific Trajectory Chart -->
          <div class="cr-stimulus-card">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px; margin-bottom: 14px;">
              <div>
                <h4 style="margin: 0; font-size: 17px; color: #1e3a5f;">Variant-Specific Trajectory Chart</h4>
                <p style="margin: 2px 0 0; font-size: 12px; color: #64748b;">
                  Only displays the selected English variant. Fundamental types are never combined on the same speed line.
                </p>
              </div>
              <div style="display: flex; align-items: center; gap: 8px;">
                <label for="engVariantSelect" style="font-size: 13px; font-weight: 600; color: #475569;">Variant:</label>
                <select id="engVariantSelect" style="padding: 6px 12px; border-radius: 8px; border: 1px solid #cbd5e1; font-weight: 600; color: #1e3a5f; background: #fff;">
                  <option value="Critical Reasoning" ${self.currentTrajectoryVariant === 'Critical Reasoning' ? 'selected' : ''}>Critical Reasoning</option>
                  <option value="Reading Comprehension" ${self.currentTrajectoryVariant === 'Reading Comprehension' ? 'selected' : ''}>Reading Comprehension</option>
                  <option value="Strengthen" ${self.currentTrajectoryVariant === 'Strengthen' ? 'selected' : ''}>Strengthen the Argument</option>
                  <option value="Weaken" ${self.currentTrajectoryVariant === 'Weaken' ? 'selected' : ''}>Weaken the Argument</option>
                  <option value="Assumption" ${self.currentTrajectoryVariant === 'Assumption' ? 'selected' : ''}>Assumption</option>
                  <option value="Inference" ${self.currentTrajectoryVariant === 'Inference' ? 'selected' : ''}>Inference</option>
                  <option value="Main Idea" ${self.currentTrajectoryVariant === 'Main Idea' ? 'selected' : ''}>Main Idea / Purpose</option>
                  <option value="Detail" ${self.currentTrajectoryVariant === 'Detail' ? 'selected' : ''}>Detail / Evidence</option>
                </select>
              </div>
            </div>

            <!-- Trajectory Chart Canvas / SVG Container -->
            <div id="engTrajectoryChart">
              ${self.buildTrajectoryChartHTML(trajectory)}
            </div>
          </div>

          <!-- English Error Log -->
          <div class="cr-stimulus-card">
            <h4 style="margin: 0 0 6px; font-size: 17px; color: #1e3a5f;">
              English Error Log (${mistakes.length} Recorded Mistakes)
            </h4>
            <p style="margin: 0 0 14px; font-size: 12.5px; color: #64748b;">
              Review root causes for missed questions. You can manually adjust error classifications at any time.
            </p>
            ${self.buildErrorLogTableHTML(mistakes)}
          </div>

          <!-- Foundation-to-GMAT Bridge Recommendations -->
          ${self.buildBridgeRecommendationsHTML(studyPlan)}
        </div>
      `;

      // Variant Selector Listener
      const varSelect = container.querySelector("#engVariantSelect");
      if (varSelect) {
        varSelect.addEventListener("change", (e) => {
          self.currentTrajectoryVariant = e.target.value;
          self.renderProgressTab(container, overview);
        });
      }

      // Reclassification buttons in table
      container.querySelectorAll(".reclassify-error-btn").forEach((btn) => {
        btn.addEventListener("click", async () => {
          const attemptId = btn.dataset.attemptId;
          const newCategory = prompt("Enter new error category (e.g. Misread question, Timing issue, Extreme answer, Out of scope):");
          if (newCategory && window.AptitudeEnglishDB) {
            await window.AptitudeEnglishDB.updateEnglishMistakeClassification(attemptId, newCategory);
            self.renderProgressTab(container, overview);
          }
        });
      });
    },

    buildTrajectoryChartHTML: function (trajectory) {
      if (!trajectory || !trajectory.daily_trajectory || trajectory.daily_trajectory.length === 0) {
        return `
          <div style="min-height: 200px; background: #f8fafc; border-radius: 8px; border: 1px dashed #cbd5e1; display: flex; align-items: center; justify-content: center; padding: 20px;">
            <div style="text-align: center; color: #64748b;">
              <div style="font-size: 28px; margin-bottom: 6px;">📊</div>
              <div style="font-weight: 600;">Trajectory for: <span style="color: #1e3a5f;">${(trajectory && trajectory.variant) || this.currentTrajectoryVariant}</span></div>
              <div style="font-size: 12px; margin-top: 4px;">Practice questions in this variant to render historical pace and accuracy points.</div>
            </div>
          </div>
        `;
      }

      const points = trajectory.daily_trajectory;
      const width = 600;
      const height = 180;
      const padL = 35;
      const padR = 25;
      const padT = 20;
      const padB = 30;
      const innerW = width - padL - padR;
      const innerH = height - padT - padB;

      const maxTime = Math.max(180, ...points.map((p) => p.avg_time || 0));
      const stepX = points.length > 1 ? innerW / (points.length - 1) : innerW / 2;

      const accPoints = points.map((p, i) => {
        const x = points.length === 1 ? padL + innerW / 2 : padL + i * stepX;
        const y = padT + innerH - (Math.min(100, p.accuracy || 0) / 100) * innerH;
        return { x: Math.round(x), y: Math.round(y), val: p.accuracy, date: p.date };
      });

      const timePoints = points.map((p, i) => {
        const x = points.length === 1 ? padL + innerW / 2 : padL + i * stepX;
        const y = padT + innerH - (Math.min(maxTime, p.avg_time || 0) / maxTime) * innerH;
        return { x: Math.round(x), y: Math.round(y), val: p.avg_time, date: p.date };
      });

      const accPolyline = accPoints.map((p) => `${p.x},${p.y}`).join(" ");
      const timePolyline = timePoints.map((p) => `${p.x},${p.y}`).join(" ");

      return `
        <div style="background: #fff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 14px;">
          <div style="display: flex; justify-content: flex-end; gap: 16px; margin-bottom: 8px; font-size: 12px; font-weight: 600;">
            <span style="color: #2563eb;">● Accuracy (%)</span>
            <span style="color: #d97706;">● Avg Pace (s)</span>
          </div>
          <svg viewBox="0 0 ${width} ${height}" style="width: 100%; height: auto; overflow: visible;">
            <!-- Grid lines -->
            <line x1="${padL}" y1="${padT}" x2="${width - padR}" y2="${padT}" stroke="#f1f5f9" stroke-width="1" />
            <line x1="${padL}" y1="${padT + innerH / 2}" x2="${width - padR}" y2="${padT + innerH / 2}" stroke="#f1f5f9" stroke-width="1" />
            <line x1="${padL}" y1="${padT + innerH}" x2="${width - padR}" y2="${padT + innerH}" stroke="#cbd5e1" stroke-width="1" />

            <!-- Accuracy Line -->
            <polyline fill="none" stroke="#2563eb" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" points="${accPolyline}" />
            ${accPoints.map((p) => `<circle cx="${p.x}" cy="${p.y}" r="4" fill="#2563eb"><title>${p.date}: ${p.val}% Accuracy</title></circle>`).join("")}

            <!-- Pace Line -->
            <polyline fill="none" stroke="#d97706" stroke-width="2" stroke-dasharray="4" stroke-linecap="round" stroke-linejoin="round" points="${timePolyline}" />
            ${timePoints.map((p) => `<circle cx="${p.x}" cy="${p.y}" r="3.5" fill="#d97706"><title>${p.date}: ${p.val}s Avg Pace</title></circle>`).join("")}

            <!-- X Labels -->
            ${points.map((p, i) => {
              const x = points.length === 1 ? padL + innerW / 2 : padL + i * stepX;
              return `<text x="${x}" y="${height - 8}" font-size="10" fill="#64748b" text-anchor="middle">${p.date}</text>`;
            }).join("")}
          </svg>
        </div>
      `;
    },

    buildBridgeRecommendationsHTML: function (studyPlan) {
      const recs = studyPlan && Array.isArray(studyPlan.recommendations) ? studyPlan.recommendations : [];
      if (recs.length === 0) {
        return `
          <div style="background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 8px; padding: 16px; margin-top: 10px;">
            <div style="display: flex; align-items: center; gap: 8px; font-weight: 700; color: #166534; font-size: 14px;">
              <span>🌱 Foundation-to-GMAT Bridge Advice</span>
            </div>
            <p style="margin: 6px 0 0; font-size: 13px; color: #374151; line-height: 1.5;">
              As you practice Grammar and Vocabulary drills, intelligent bridge recommendations will appear here to connect foundational language skills (modifier placement, parallelism, causal connectors) directly to GMAT Critical Reasoning and Reading Comprehension performance.
            </p>
          </div>
        `;
      }
      return `
        <div style="background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 8px; padding: 16px; margin-top: 10px;">
          <div style="display: flex; align-items: center; gap: 8px; font-weight: 700; color: #166534; font-size: 14px; margin-bottom: 8px;">
            <span>🌱 Foundation-to-GMAT Bridge Recommendations</span>
          </div>
          <ul style="margin: 0; padding-left: 20px; font-size: 13px; color: #374151; line-height: 1.6;">
            ${recs.map((r) => `<li>${r}</li>`).join("")}
          </ul>
        </div>
      `;
    },

    buildErrorLogTableHTML: function (mistakes) {
      if (!mistakes || mistakes.length === 0) {
        return `
          <div style="padding: 24px; text-align: center; color: #64748b; background: #f8fafc; border-radius: 8px;">
            ✨ No recorded mistakes yet! Complete practice drills to track error patterns.
          </div>
        `;
      }

      const rows = mistakes.slice(0, 15).map((m) => {
        const qText = (m.question_text || "").substring(0, 60) + "...";
        return `
          <tr style="border-bottom: 1px solid #f1f5f9; font-size: 13px;">
            <td style="padding: 10px 8px; color: #64748b;">${m.date || '--'}</td>
            <td style="padding: 10px 8px; font-weight: 600; color: #1e3a5f;">${m.question_type || m.topic_name || 'Verbal'}</td>
            <td style="padding: 10px 8px; color: #334155;">${qText}</td>
            <td style="padding: 10px 8px;">
              <span style="background: #fef2f2; color: #dc2626; padding: 2px 6px; border-radius: 4px; font-size: 11px;">
                ${m.trap_type || 'Trap'}
              </span>
            </td>
            <td style="padding: 10px 8px;">
              <span style="background: #eff6ff; color: #2563eb; padding: 2px 6px; border-radius: 4px; font-size: 11px;">
                ${m.error_category || 'Unclassified'}
              </span>
            </td>
            <td style="padding: 10px 8px;">
              <button class="english-btn english-btn-ghost reclassify-error-btn" data-attempt-id="${m.id}" style="padding: 4px 8px; font-size: 11px;" type="button">
                Edit ✎
              </button>
            </td>
          </tr>
        `;
      }).join("");

      return `
        <div style="overflow-x: auto;">
          <table style="width: 100%; border-collapse: collapse; text-align: left;">
            <thead>
              <tr style="border-bottom: 2px solid #e2e8f0; font-size: 11px; text-transform: uppercase; color: #64748b;">
                <th style="padding: 8px;">Date</th>
                <th style="padding: 8px;">Type</th>
                <th style="padding: 8px;">Question</th>
                <th style="padding: 8px;">Trap</th>
                <th style="padding: 8px;">Error Category</th>
                <th style="padding: 8px;">Action</th>
              </tr>
            </thead>
            <tbody>
              ${rows}
            </tbody>
          </table>
        </div>
      `;
    },

    // -----------------------------------------------------------------------
    // Helper question selectors
    // -----------------------------------------------------------------------
    getCRQuestions: function () {
      if (window.ENGLISH_DATA && window.ENGLISH_DATA.CR_QUESTIONS) {
        return window.ENGLISH_DATA.CR_QUESTIONS;
      }
      return BUILTIN_QUESTIONS.filter(q => q.type === "cr");
    },

    getRCQuestions: function () {
      if (window.ENGLISH_DATA && window.ENGLISH_DATA.RC_QUESTIONS) {
        return window.ENGLISH_DATA.RC_QUESTIONS;
      }
      return BUILTIN_QUESTIONS.filter(q => q.type === "rc");
    },

    getMixedQuestions: function () {
      const crs = this.getCRQuestions();
      const rcs = this.getRCQuestions();
      const mixed = [...crs, ...rcs];
      mixed.sort(() => Math.random() - 0.5);
      return mixed;
    },

    // -----------------------------------------------------------------------
    // Session Starters & Resumes
    // -----------------------------------------------------------------------
    resumeActiveSession: function (activeSession) {
      if (!activeSession || !activeSession.questions) return;
      EnglishOverlayManager.open();
      const view = EnglishOverlayManager.getViewContainer();
      QuestionRunner.startSession({
        sessionId: activeSession.session_id,
        mode: activeSession.mode,
        questions: activeSession.questions,
        timeLimitSeconds: activeSession.time_remaining_seconds,
        container: view,
        onFinish: (sess) => {
          EnglishOverlayManager.showCompletion(sess, () => {
            EnglishApp.init();
          });
        },
        onExit: () => {
          EnglishOverlayManager.close();
          EnglishApp.init();
        },
      });
      // Restore user state
      if (activeSession.current_index) {
        QuestionRunner.renderQuestion(activeSession.current_index);
      }
    },

    startPracticeSession: async function (config = {}) {
      const self = this;
      const qView = document.getElementById("englishQuestionView") || document.querySelector("main");
      EnglishOverlayManager.open();
      const view = EnglishOverlayManager.getViewContainer();
      let selectedQuestions = [];
      let isAiGenerated = false;

      const isAdaptiveDrill = self.isAiMode &&
        config.mode !== "simulation" &&
        config.mode !== "verbal_diagnostic" &&
        config.mode !== "foundation_diagnostic";

      if (config.mode === "simulation") {
        if (window.ENGLISH_DATA) {
          const crs = (window.ENGLISH_DATA.CR_QUESTIONS || []).slice(0, 10);
          const rcs = (window.ENGLISH_DATA.RC_QUESTIONS || []).slice(0, 13);
          selectedQuestions = [...crs, ...rcs];
        } else {
          selectedQuestions = BUILTIN_QUESTIONS;
        }
        config.isSimulation = true;
        config.timeLimitSeconds = 45 * 60;
      } else if (config.mode === "verbal_diagnostic") {
        if (window.ENGLISH_DATA) {
          const crs = (window.ENGLISH_DATA.CR_QUESTIONS || []).slice(0, 7);
          const rcs = (window.ENGLISH_DATA.RC_QUESTIONS || []).slice(0, 8);
          selectedQuestions = [...crs, ...rcs];
        } else {
          selectedQuestions = BUILTIN_QUESTIONS;
        }
      } else if (config.mode === "foundation_diagnostic") {
        if (window.ENGLISH_DATA) {
          const grammars = (window.ENGLISH_DATA.GRAMMAR_QUESTIONS || []).slice(0, 8);
          const vocabs = (window.ENGLISH_DATA.VOCABULARY_ITEMS || []).slice(0, 8).map(v => ({
            id: "diag_" + v.id,
            section: "foundation",
            type: "vocab",
            question_text: "What is the primary definition of \"" + v.word + "\"? (" + v.part_of_speech + ")",
            options: [
              v.definition,
              "To cause unexpected difficulty or confusion.",
              "Occurring in rare or isolated instances.",
              "Related to theoretical rather than empirical proof."
            ],
            correct_option_index: 0,
            explanation: v.definition + " Example: " + v.example_sentence,
          }));
          selectedQuestions = [...grammars, ...vocabs];
        } else {
          selectedQuestions = BUILTIN_QUESTIONS;
        }
      } else if (isAdaptiveDrill) {
        // Calculate dynamic adaptive difficulty from user performance in AptitudeEnglishDB
        let targetDifficulty = 3;
        let avoidQuestions = [];
        try {
          if (window.AptitudeEnglishDB) {
            const attempts = await window.AptitudeEnglishDB.getAllEnglishAttempts();
            if (attempts && attempts.length > 0) {
              const relevant = attempts
                .filter(a => config.subsection === "Grammar" ? a.section === "foundation" : a.section === "gmat_verbal")
                .slice(-10);
              if (relevant.length >= 3) {
                const acc = relevant.filter(a => a.is_correct).length / relevant.length;
                if (acc >= 0.8) targetDifficulty = 5;
                else if (acc >= 0.6) targetDifficulty = 4;
                else if (acc <= 0.3) targetDifficulty = 2;
                else if (acc <= 0.15) targetDifficulty = 1;
                else targetDifficulty = 3;
              }
              avoidQuestions = attempts.slice(-25).map(a => a.question_id || a.question_text).filter(Boolean);
            }
          }
        } catch (e) {
          console.warn("Could not calculate adaptive difficulty:", e);
        }

        const count = (config.questions && config.questions.length) || config.count || 5;
        let drillMode = "mixed";
        if (config.subsection === "Critical Reasoning") drillMode = "cr";
        else if (config.subsection === "Reading Comprehension") drillMode = "rc";
        else if (config.subsection === "Grammar") drillMode = "grammar";

        // Render generation state
        if (qView) {
          qView.innerHTML = `
            <div style="min-height: 380px; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; padding: 40px; background: #fff; border-radius: 12px; margin: 20px auto; max-width: 560px; box-shadow: 0 4px 14px rgba(0,0,0,0.06); border: 1px solid #e2e8f0;">
              <div style="font-size: 40px; margin-bottom: 14px; animation: engBounce 1s infinite alternate;">🤖</div>
              <h3 style="margin: 0 0 8px; color: #1e3a5f; font-size: 20px; font-weight: 700;">Adaptive AI Question Generator</h3>
              <div style="display: inline-flex; align-items: center; gap: 6px; background: #eff6ff; color: #1d4ed8; padding: 4px 12px; border-radius: 16px; font-size: 13px; font-weight: 600; margin-bottom: 14px;">
                <span>Target Difficulty: Level ${targetDifficulty} / 5</span>
              </div>
              <p style="margin: 0 0 18px; color: #64748b; font-size: 13.5px; max-width: 420px; line-height: 1.5;">
                Synthesizing non-repeating ${config.subsection || "Verbal"} questions calibrated to your accuracy trajectory...
              </p>
              <div style="width: 32px; height: 32px; border: 3px solid #e2e8f0; border-top-color: #2563eb; border-radius: 50%; animation: engSpin 0.8s linear infinite;"></div>
            </div>
          `;
        }
        // Show animated overlay loading card with cancellation
        let isCancelled = false;
        const controller = new AbortController();

        EnglishOverlayManager.showLoading({
          title: "Adaptive AI Question Generator",
          subtitle: `Calibrating non-repeating ${config.subsection || "Verbal"} questions (Target Difficulty: Level ${targetDifficulty}/5)...`,
          section: config.subsection === "Grammar" ? "English Foundation" : "GMAT Verbal Reasoning",
          detailBadge: `Difficulty Level ${targetDifficulty}/5`,
          onCancel: () => {
            isCancelled = true;
            controller.abort();
          }
        });

        // 10-second timeout handling with automatic fallback to curated bank
        const timeoutId = setTimeout(() => {
          controller.abort();
        }, 10000);

        try {
          const resp = await fetch("/api/english/generate/drill", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              mode: drillMode,
              count: count,
              target_difficulty: targetDifficulty,
              avoid_questions: avoidQuestions,
            }),
            signal: controller.signal
          });
          clearTimeout(timeoutId);

          if (resp.ok) {
            const data = await resp.json();
            if (data && Array.isArray(data.questions) && data.questions.length > 0) {
              selectedQuestions = data.questions.map(q => ({
                ...q,
                is_ai_generated: data.is_ai_generated !== false,
              }));
              isAiGenerated = data.is_ai_generated !== false;
            }
          }
        } catch (fetchErr) {
          console.warn("AI drill generation fetch error, falling back to curated bank:", fetchErr);
          clearTimeout(timeoutId);
          console.warn("AI drill generation fetch error or timeout, falling back to curated bank:", fetchErr);
        }

        if (isCancelled) return;

        // Fallback to local questions if fetch was unsuccessful
        if (!selectedQuestions || selectedQuestions.length === 0) {
          if (config.questions) {
            selectedQuestions = config.questions;
          } else if (config.subsection === "Critical Reasoning") {
            selectedQuestions = self.getCRQuestions().slice(0, count);
          } else if (config.subsection === "Reading Comprehension") {
            selectedQuestions = self.getRCQuestions().slice(0, count);
          } else if (config.subsection === "Grammar") {
            selectedQuestions = ((window.ENGLISH_DATA && window.ENGLISH_DATA.GRAMMAR_QUESTIONS) || []).slice(0, count);
          } else {
            selectedQuestions = self.getMixedQuestions().slice(0, count);
          }
        }
      } else if (config.questions) {
        selectedQuestions = config.questions;
      } else {
        selectedQuestions = self.getMixedQuestions().slice(0, 10);
      }

      QuestionRunner.startSession({
        ...config,
        questions: selectedQuestions,
        is_ai_generated: isAiGenerated,
        container: view,
        onFinish: (sess) => {
          if (config.day_number && config.task_id && window.AptitudeEnglishDB) {
            window.AptitudeEnglishDB.updateDailyTaskStatus(config.day_number, config.task_id, true).catch(() => {});
          }
          EnglishOverlayManager.showCompletion(sess, () => {
            EnglishApp.init();
          });
        },
        onExit: () => {
          EnglishOverlayManager.close();
          EnglishApp.init();
        },
      });
    },

    startFlashcards: function (config = {}) {
      const self = this;
      EnglishOverlayManager.open();
      const view = EnglishOverlayManager.getViewContainer();
      FlashcardUI.startDeck({
        ...config,
        container: view,
        onComplete: () => {
          if (config.day_number && config.task_id && window.AptitudeEnglishDB) {
            window.AptitudeEnglishDB.updateDailyTaskStatus(config.day_number, config.task_id, true).catch(() => {});
          }
          EnglishOverlayManager.showCompletion({
            totalQuestions: (config.deck && config.deck.length) || 10,
            score: (config.deck && config.deck.length) || 10,
            subsection: "Vocabulary SRS",
            mode: "vocab_srs"
          }, () => {
            EnglishOverlayManager.close();
            self.init();
          });
        },
        onExit: () => {
          EnglishOverlayManager.close();
          self.init();
        },
      });
    },
  };

  // Global exports
  window.EnglishOverlayManager = EnglishOverlayManager;
  window.EnglishQuestionRunner = QuestionRunner;
  window.EnglishReviewUI = ReviewUI;
  window.EnglishFlashcardUI = FlashcardUI;
  window.EnglishApp = EnglishApp;
})();
