/** English Data Catalog for Browser (Offline-First) */
window.ENGLISH_DATA = {
  "CR_QUESTIONS": [
    {
      "id": "cr-001",
      "section": "verbal",
      "subsection": "critical_reasoning",
      "question_type": "weaken",
      "topic": "business_strategy",
      "difficulty": 3,
      "stimulus": "Over the past two years, Zenith Fitness increased membership dues by 25 percent at all downtown locations. During the same period, total revenues at these locations rose by 30 percent. Management concluded that downtown patrons are relatively insensitive to price increases and recommended an additional 20 percent price hike.",
      "premise": "Dues increased 25% and total revenues rose 30% at downtown locations over two years.",
      "conclusion": "Downtown patrons are price-insensitive, so another 20% hike will succeed.",
      "assumption": "The revenue increase was driven by the price hike, not other factors.",
      "logical_gap": "Alternative explanations for revenue growth were not considered.",
      "question_text": "Which of the following, if true, most seriously weakens the management's conclusion?",
      "options": [
        "A competing gym chain plans to open three new locations in suburban areas.",
        "Downtown locations introduced premium personal training packages two years ago, and those packages accounted for over half of revenue growth.",
        "Surveys show downtown patrons value convenience and updated equipment more than cleanliness.",
        "Leasing costs in the downtown core have increased by 15 percent.",
        "Suburban locations experienced an 8 percent membership decline after a 10 percent price increase."
      ],
      "correct_option_index": 1,
      "explanation": "Option B provides an alternative explanation for the revenue increase: personal training packages, not membership dues, drove most of the growth. This undermines the conclusion that patrons are price-insensitive to dues increases.",
      "option_explanations": [
        "Irrelevant: Suburban competition does not address downtown price sensitivity.",
        "Correct: Identifies a confounding factor (training packages) that explains the revenue surge without price insensitivity.",
        "Irrelevant: Patron preferences for equipment vs. cleanliness do not address price elasticity.",
        "Out of scope: Costs affect profitability, not the revenue-based conclusion.",
        "Scope shift: Suburban behavior does not invalidate the downtown observation."
      ],
      "target_time_seconds": 120,
      "trap_type": "correlation_vs_causation",
      "skills": [
        "argument_structure",
        "alternative_explanation"
      ]
    },
    {
      "id": "cr-002",
      "section": "verbal",
      "subsection": "critical_reasoning",
      "question_type": "strengthen",
      "topic": "public_policy",
      "difficulty": 3,
      "stimulus": "City officials propose that installing LED streetlights on all major roads will reduce nighttime traffic accidents by at least 40 percent. They cite a pilot program on Elm Boulevard where LED lights were installed and accidents dropped 45 percent over the following year.",
      "premise": "A pilot on Elm Boulevard saw a 45% accident reduction after LED installation.",
      "conclusion": "LED streetlights citywide will reduce nighttime accidents by at least 40%.",
      "assumption": "The pilot results are generalizable and the LED lights caused the reduction.",
      "logical_gap": "Elm Boulevard may differ from other roads; other factors may have contributed.",
      "question_text": "Which of the following, if true, most strengthens the officials' argument?",
      "options": [
        "LED streetlights consume 60 percent less electricity than traditional sodium lights.",
        "Elm Boulevard has traffic volume and road design characteristics representative of most major city roads.",
        "The city recently increased fines for speeding violations on all major roads.",
        "Nighttime pedestrian traffic on Elm Boulevard decreased by 20 percent during the pilot.",
        "Several neighboring cities have also begun installing LED streetlights."
      ],
      "correct_option_index": 1,
      "explanation": "If Elm Boulevard is representative of most city roads, the pilot results can be generalized, strengthening the conclusion that citywide LED installation will yield similar accident reductions.",
      "option_explanations": [
        "Irrelevant: Energy savings do not address accident reduction.",
        "Correct: Establishes representativeness, supporting generalization of pilot results.",
        "Weakens: Increased fines provide an alternative explanation for fewer accidents.",
        "Weakens: Fewer pedestrians could explain reduced accidents, undermining the LED causal claim.",
        "Irrelevant: Other cities' actions do not validate the pilot's generalizability."
      ],
      "target_time_seconds": 120,
      "trap_type": "irrelevant_information",
      "skills": [
        "generalization",
        "causal_reasoning"
      ]
    },
    {
      "id": "cr-003",
      "section": "verbal",
      "subsection": "critical_reasoning",
      "question_type": "assumption",
      "topic": "scientific_study",
      "difficulty": 4,
      "stimulus": "Researchers found that employees who take at least a 30-minute lunch break away from their desks report higher afternoon productivity than those who eat at their desks. The researchers concluded that taking breaks away from the work area directly improves cognitive function in the afternoon.",
      "premise": "Employees who take 30+ minute breaks away from desks report higher afternoon productivity.",
      "conclusion": "Breaks away from the work area directly improve afternoon cognitive function.",
      "assumption": "Higher reported productivity is not due to pre-existing differences between the two groups.",
      "logical_gap": "Self-selection bias: employees who take breaks may differ from those who don't.",
      "question_text": "The argument depends on which of the following assumptions?",
      "options": [
        "Most employees prefer to eat lunch at their desks rather than in a break room.",
        "Employees who eat at their desks are not inherently less productive than those who take breaks.",
        "A 30-minute break is the minimum duration needed to improve cognitive function.",
        "The study controlled for the type of food consumed during lunch.",
        "Afternoon productivity is more important than morning productivity for overall output."
      ],
      "correct_option_index": 1,
      "explanation": "The argument assumes that the productivity difference is caused by the break location, not pre-existing differences between the groups. If desk-eaters were already less productive, the break is not the cause.",
      "option_explanations": [
        "Irrelevant: Employee preference does not affect the causal claim.",
        "Correct: Necessary assumption\u2014if desk-eaters are inherently less productive, the break is not the cause.",
        "Too extreme: The argument does not require a specific minimum duration threshold.",
        "Irrelevant: Food type is not part of the argument's reasoning.",
        "Out of scope: Relative importance of afternoon vs. morning productivity is not assumed."
      ],
      "target_time_seconds": 120,
      "trap_type": "unsupported_assumption",
      "skills": [
        "assumption_identification",
        "selection_bias"
      ]
    },
    {
      "id": "cr-004",
      "section": "verbal",
      "subsection": "critical_reasoning",
      "question_type": "inference",
      "topic": "economics",
      "difficulty": 3,
      "stimulus": "Country X's central bank raised interest rates by 2 percentage points last quarter. Historically, when interest rates rise by more than 1.5 percentage points in a single quarter, consumer spending in the following quarter drops by 8 to 12 percent. However, Country X's GDP grew by 3 percent last quarter, driven primarily by increased export revenues.",
      "premise": "Interest rates rose 2 points. Historically, >1.5 point raises cause 8-12% spending drops. GDP grew 3% driven by exports.",
      "conclusion": "N/A (inference question)",
      "assumption": "N/A",
      "logical_gap": "N/A",
      "question_text": "If the statements above are true, which of the following can be properly inferred?",
      "options": [
        "Country X's GDP will decline next quarter due to reduced consumer spending.",
        "Export revenues will continue to grow at the same rate next quarter.",
        "The growth in export revenues was large enough to offset any negative effects of the interest rate increase on GDP last quarter.",
        "Consumer spending in Country X did not change last quarter.",
        "The central bank's decision to raise interest rates was economically unwise."
      ],
      "correct_option_index": 2,
      "explanation": "GDP grew 3% despite a rate increase that historically reduces consumer spending. Since exports drove growth, exports must have been sufficient to offset any negative impact on GDP.",
      "option_explanations": [
        "Too strong: We cannot predict next quarter's GDP with certainty.",
        "Unsupported: Nothing indicates export growth will continue at the same rate.",
        "Correct: The GDP growth despite rate increases implies exports offset the negative effects.",
        "Too extreme: Consumer spending may have declined; GDP still grew via exports.",
        "Value judgment: The passage provides no basis for evaluating the wisdom of the decision."
      ],
      "target_time_seconds": 120,
      "trap_type": "extreme_language",
      "skills": [
        "inference",
        "economic_reasoning"
      ]
    },
    {
      "id": "cr-005",
      "section": "verbal",
      "subsection": "critical_reasoning",
      "question_type": "resolve_paradox",
      "topic": "environmental_policy",
      "difficulty": 3,
      "stimulus": "Despite a nationwide ban on single-use plastic bags enacted three years ago, the total volume of plastic waste reaching municipal landfills has increased by 15 percent. Environmental groups expected the ban to significantly reduce plastic waste volumes.",
      "premise": "A nationwide ban on plastic bags was enacted 3 years ago. Plastic waste volume increased 15%.",
      "conclusion": "N/A (paradox)",
      "assumption": "N/A",
      "logical_gap": "N/A",
      "question_text": "Which of the following, if true, best helps to resolve the apparent paradox?",
      "options": [
        "Many consumers switched to thicker reusable bags that they discard after only a few uses, contributing more plastic by weight per bag.",
        "The government invested in new recycling infrastructure during the same period.",
        "Single-use plastic bags constituted only 1 percent of total plastic waste before the ban.",
        "Neighboring countries that did not enact bans saw even larger increases in plastic waste.",
        "Environmental groups had overestimated public compliance with the ban."
      ],
      "correct_option_index": 0,
      "explanation": "If consumers switched to thicker bags that they still discard frequently, each discarded bag contributes more plastic by weight than the banned thin bags, explaining why total plastic waste increased despite the ban.",
      "option_explanations": [
        "Correct: Thicker replacement bags increase total weight of plastic waste despite fewer bags.",
        "Deepens the paradox: Better recycling should reduce waste, not explain an increase.",
        "Partial: This explains why the ban had limited effect but doesn't explain the increase.",
        "Irrelevant: Other countries' waste does not explain the domestic increase.",
        "Partial: Non-compliance would mean waste stays flat, not necessarily increases."
      ],
      "target_time_seconds": 120,
      "trap_type": "partial_answer",
      "skills": [
        "paradox_resolution",
        "causal_mechanism"
      ]
    },
    {
      "id": "cr-006",
      "section": "verbal",
      "subsection": "critical_reasoning",
      "question_type": "main_conclusion",
      "topic": "business_strategy",
      "difficulty": 2,
      "stimulus": "TechStart, a software company, found that its remote employees complete 15 percent more tasks per week than office-based employees. Remote employees also report higher job satisfaction. However, cross-team collaboration scores are 25 percent lower for remote teams. Therefore, TechStart should adopt a hybrid model that allows remote work three days per week while preserving two days for in-person collaboration.",
      "premise": "Remote employees are more productive and satisfied but collaborate less effectively.",
      "conclusion": "TechStart should adopt a hybrid model (3 remote, 2 in-office).",
      "assumption": "A hybrid model can capture productivity gains while preserving collaboration.",
      "logical_gap": "Whether two days of in-person work suffice to restore collaboration.",
      "question_text": "Which of the following best expresses the main conclusion of the argument?",
      "options": [
        "Remote employees complete more tasks and report higher satisfaction.",
        "Cross-team collaboration suffers when employees work remotely.",
        "TechStart should implement a hybrid work arrangement balancing remote and in-person days.",
        "Office-based work is essential for effective team collaboration.",
        "Remote work is generally more productive than office work."
      ],
      "correct_option_index": 2,
      "explanation": "The argument's main conclusion is the recommendation: TechStart should adopt a hybrid model. The other statements are premises or evidence supporting this conclusion.",
      "option_explanations": [
        "Premise, not conclusion: This is evidence supporting the recommendation.",
        "Premise, not conclusion: This is a finding that motivates the recommendation.",
        "Correct: This is the actionable recommendation that the argument builds toward.",
        "Too extreme: The argument does not claim office work is essential, only that collaboration suffers remotely.",
        "Too broad: The argument is specific to TechStart, not a general claim about remote work."
      ],
      "target_time_seconds": 100,
      "trap_type": "restatement_of_premise",
      "skills": [
        "conclusion_identification",
        "argument_structure"
      ]
    },
    {
      "id": "cr-007",
      "section": "verbal",
      "subsection": "critical_reasoning",
      "question_type": "evaluate",
      "topic": "public_health",
      "difficulty": 4,
      "stimulus": "A hospital administrator argues that implementing a mandatory hand-hygiene monitoring system will reduce hospital-acquired infections by 35 percent. She bases this projection on data from a six-month trial in the surgical ward, where infections dropped 38 percent after monitoring was introduced.",
      "premise": "Surgical ward trial showed 38% infection reduction with hygiene monitoring.",
      "conclusion": "Hospital-wide implementation will reduce infections by 35%.",
      "assumption": "Surgical ward results generalize to other wards.",
      "logical_gap": "Whether infection types and hygiene practices vary across wards.",
      "question_text": "The answer to which of the following questions would be most useful in evaluating the administrator's argument?",
      "options": [
        "What is the total cost of implementing the monitoring system hospital-wide?",
        "Do other hospital wards have baseline infection rates and transmission patterns similar to those of the surgical ward?",
        "Has the hospital's overall patient satisfaction improved since the trial began?",
        "Are hand-hygiene monitoring systems used in hospitals in other countries?",
        "Did the surgical ward hire additional cleaning staff during the trial period?"
      ],
      "correct_option_index": 1,
      "explanation": "If other wards have different infection profiles, the surgical ward results may not generalize. Knowing whether wards are comparable is essential for evaluating the projection.",
      "option_explanations": [
        "Irrelevant to effectiveness: Cost does not determine whether the infection reduction will occur.",
        "Correct: Determines whether the trial results can be extended to other wards.",
        "Out of scope: Patient satisfaction does not evaluate infection reduction claims.",
        "Irrelevant: Other countries' usage does not evaluate this specific projection.",
        "Relevant but secondary: Additional staff might explain the trial results, but the key evaluation question is generalizability."
      ],
      "target_time_seconds": 120,
      "trap_type": "out_of_scope",
      "skills": [
        "evaluation",
        "generalization"
      ]
    },
    {
      "id": "cr-008",
      "section": "verbal",
      "subsection": "critical_reasoning",
      "question_type": "flaw_in_reasoning",
      "topic": "scientific_study",
      "difficulty": 4,
      "stimulus": "A nutritionist claims that consuming dark chocolate daily improves cardiovascular health. She points to a study showing that people who eat dark chocolate at least five times per week have 20 percent lower rates of heart disease than those who rarely eat chocolate. Therefore, she recommends that all adults eat dark chocolate daily.",
      "premise": "Study: frequent chocolate eaters have 20% lower heart disease rates.",
      "conclusion": "All adults should eat dark chocolate daily for cardiovascular health.",
      "assumption": "The correlation between chocolate consumption and lower heart disease is causal.",
      "logical_gap": "Confounding factors; healthy-user bias; correlation treated as causation.",
      "question_text": "The nutritionist's reasoning is most vulnerable to which of the following criticisms?",
      "options": [
        "It fails to consider whether dark chocolate has other health benefits beyond cardiovascular improvement.",
        "It assumes that a correlation between chocolate consumption and lower heart disease rates establishes a causal relationship.",
        "It does not specify the optimal daily amount of dark chocolate for health benefits.",
        "It ignores the possibility that some adults are allergic to chocolate.",
        "It relies on a study that was not conducted by medical professionals."
      ],
      "correct_option_index": 1,
      "explanation": "The main flaw is treating a correlational finding as causal evidence. People who eat dark chocolate may differ in other health behaviors (exercise, diet), which could explain the lower disease rates.",
      "option_explanations": [
        "Irrelevant: Additional benefits do not address the flaw in the cardiovascular claim.",
        "Correct: Identifies the correlation-causation flaw central to the argument.",
        "Misses the main flaw: Dosage precision is secondary to the causal reasoning error.",
        "Too narrow: Allergies affect a small population and don't address the reasoning flaw.",
        "Ad hominem: The credentials of researchers do not constitute a logical flaw in the argument structure."
      ],
      "target_time_seconds": 120,
      "trap_type": "correlation_vs_causation",
      "skills": [
        "flaw_identification",
        "causal_reasoning"
      ]
    },
    {
      "id": "cr-009",
      "section": "verbal",
      "subsection": "critical_reasoning",
      "question_type": "necessary_assumption",
      "topic": "economics",
      "difficulty": 4,
      "stimulus": "An economist argues that raising the minimum wage by 15 percent will not lead to significant job losses in the retail sector. She notes that retail profit margins are currently at a ten-year high, which means employers can absorb higher labor costs without reducing headcount.",
      "premise": "Retail profit margins are at a ten-year high.",
      "conclusion": "A 15% minimum wage increase will not cause significant retail job losses.",
      "assumption": "High margins mean employers can and will absorb higher costs rather than cut jobs.",
      "logical_gap": "Employers may cut jobs regardless of margins; margins may erode from other pressures.",
      "question_text": "The argument requires which of the following assumptions?",
      "options": [
        "Retail employees are more productive now than they were ten years ago.",
        "Retail employers will choose to absorb higher labor costs from their margins rather than reduce their workforce.",
        "No other costs in the retail sector are expected to increase in the near future.",
        "The minimum wage has not been increased in the past ten years.",
        "Retail consumers are willing to pay higher prices to support wage increases."
      ],
      "correct_option_index": 1,
      "explanation": "The argument assumes employers will use their high margins to cover wage increases instead of cutting jobs. Without this assumption, high margins alone do not guarantee employment stability.",
      "option_explanations": [
        "Irrelevant: Productivity is not part of the argument's reasoning chain.",
        "Correct: Necessary bridge between high margins and the conclusion of no job losses.",
        "Too extreme: The argument does not require zero other cost increases.",
        "Not required: The argument works regardless of when the last increase occurred.",
        "Not assumed: The argument is about margins, not consumer willingness to pay more."
      ],
      "target_time_seconds": 120,
      "trap_type": "necessary_vs_sufficient",
      "skills": [
        "necessary_assumption",
        "argument_structure"
      ]
    },
    {
      "id": "cr-010",
      "section": "verbal",
      "subsection": "critical_reasoning",
      "question_type": "method_of_reasoning",
      "topic": "public_policy",
      "difficulty": 4,
      "stimulus": "The mayor argues that the city's new bike-lane network will reduce traffic congestion. She points out that Copenhagen, a city of similar size, reduced peak-hour congestion by 18 percent after expanding its bike-lane system. She also notes that surveys show 30 percent of local commuters would consider cycling if safe infrastructure were available.",
      "premise": "Copenhagen (similar size) reduced congestion 18% with bike lanes; 30% of local commuters would consider cycling with safe infrastructure.",
      "conclusion": "The new bike-lane network will reduce traffic congestion.",
      "assumption": "What worked in Copenhagen will work here; surveyed intentions translate to behavior.",
      "logical_gap": "Analogy may be imperfect; survey intentions may not match actions.",
      "question_text": "The mayor's argument proceeds by",
      "options": [
        "establishing a general principle and applying it to a specific case",
        "drawing an analogy with a comparable city and citing survey data to support the predicted outcome",
        "refuting a counterargument against bike-lane expansion",
        "presenting statistical evidence that bike lanes directly reduce car usage",
        "arguing that the benefits of bike lanes outweigh their costs"
      ],
      "correct_option_index": 1,
      "explanation": "The mayor uses two supporting strategies: (1) an analogy with Copenhagen, a city of similar size, and (2) survey data showing local commuter willingness to cycle. This is argument by analogy combined with survey evidence.",
      "option_explanations": [
        "Incorrect: No general principle is stated; the argument uses a specific analogy.",
        "Correct: Accurately describes the two-pronged approach of analogy and survey data.",
        "Incorrect: No counterargument is addressed or refuted.",
        "Incorrect: The Copenhagen data is analogical, not direct statistical evidence about this city.",
        "Incorrect: Cost-benefit analysis is not part of the argument."
      ],
      "target_time_seconds": 120,
      "trap_type": "out_of_scope",
      "skills": [
        "method_of_reasoning",
        "analogy"
      ]
    },
    {
      "id": "cr-011",
      "section": "verbal",
      "subsection": "critical_reasoning",
      "question_type": "sufficient_assumption",
      "topic": "business_strategy",
      "difficulty": 5,
      "stimulus": "All companies that invest more than 10 percent of revenue in R&D achieve above-industry-average profit growth within five years, provided that they also maintain a customer retention rate above 85 percent. MegaCorp has invested 14 percent of its revenue in R&D for each of the past three years.",
      "premise": "If R&D > 10% of revenue AND retention > 85%, then above-average profit growth. MegaCorp has R&D at 14%.",
      "conclusion": "MegaCorp will achieve above-average profit growth.",
      "assumption": "MegaCorp's customer retention rate is above 85%.",
      "logical_gap": "The retention condition is not stated for MegaCorp.",
      "question_text": "Which of the following, if assumed, allows the conclusion to be properly drawn?",
      "options": [
        "MegaCorp's competitors invest less than 10 percent of revenue in R&D.",
        "MegaCorp's customer retention rate has been above 85 percent for each of the past three years.",
        "MegaCorp's R&D spending has increased each year.",
        "Companies in MegaCorp's industry typically invest 8 percent of revenue in R&D.",
        "MegaCorp's profit growth has already been above the industry average."
      ],
      "correct_option_index": 1,
      "explanation": "The conditional requires both R&D > 10% AND retention > 85%. MegaCorp satisfies the R&D condition. If we assume retention > 85%, both conditions are met and the conclusion follows logically.",
      "option_explanations": [
        "Irrelevant: Competitor spending does not fulfill the retention condition.",
        "Correct: Supplies the missing retention condition, completing the sufficient conditions.",
        "Irrelevant: Year-over-year increase is not a condition in the stated rule.",
        "Irrelevant: Industry norms do not address MegaCorp's retention rate.",
        "Circular: If already above average, the conclusion is already true, but this doesn't logically connect the premises."
      ],
      "target_time_seconds": 120,
      "trap_type": "necessary_vs_sufficient",
      "skills": [
        "sufficient_assumption",
        "conditional_reasoning"
      ]
    },
    {
      "id": "cr-012",
      "section": "verbal",
      "subsection": "critical_reasoning",
      "question_type": "explain_discrepancy",
      "topic": "scientific_study",
      "difficulty": 3,
      "stimulus": "A pharmaceutical company's clinical trial showed that Drug X reduced migraine frequency by 50 percent in participants. However, after Drug X was approved and prescribed widely, doctors reported that only 25 percent of patients experienced a comparable reduction in migraine frequency.",
      "premise": "Drug X showed 50% migraine reduction in trials but only 25% in real-world use.",
      "conclusion": "N/A (discrepancy)",
      "assumption": "N/A",
      "logical_gap": "N/A",
      "question_text": "Which of the following, if true, best explains the discrepancy described above?",
      "options": [
        "Drug X has fewer side effects than most competing migraine medications.",
        "Clinical trial participants were screened to exclude those with conditions that reduce drug effectiveness, unlike the general patient population.",
        "The pharmaceutical company conducted the trial at multiple hospital sites.",
        "Many doctors prescribed Drug X at a lower dosage than was used in the clinical trial.",
        "Migraine frequency varies naturally across seasons."
      ],
      "correct_option_index": 1,
      "explanation": "Trial participants were pre-screened, creating a more homogeneous and responsive sample. The general population includes patients with conditions that reduce effectiveness, explaining the lower real-world results.",
      "option_explanations": [
        "Irrelevant: Side effect profile does not explain the efficacy gap.",
        "Correct: Selection criteria created a biased sample that outperformed the general population.",
        "Irrelevant: Multi-site trials are standard and don't explain the gap.",
        "Plausible but secondary: Dosage differences could contribute, but the screening explanation is more direct and comprehensive.",
        "Irrelevant: Seasonal variation would not systematically explain a consistent gap."
      ],
      "target_time_seconds": 120,
      "trap_type": "partial_answer",
      "skills": [
        "discrepancy_resolution",
        "sampling_bias"
      ]
    },
    {
      "id": "cr-013",
      "section": "verbal",
      "subsection": "critical_reasoning",
      "question_type": "principle",
      "topic": "ethics",
      "difficulty": 3,
      "stimulus": "A company discovered that a minor software glitch caused some customers to be overcharged by two dollars on recent transactions. The total overcharges amount to approximately twelve thousand dollars. Fixing the glitch and issuing refunds would cost the company fifty thousand dollars in engineering and administrative expenses. The company's CFO argues that because the cost of remediation far exceeds the total overcharges, the company should not issue refunds.",
      "premise": "Overcharges total $12K. Remediation costs $50K.",
      "conclusion": "The company should not issue refunds because remediation costs exceed overcharges.",
      "assumption": "Financial cost-benefit analysis is the only relevant consideration.",
      "logical_gap": "Ethical obligations and reputational risk are ignored.",
      "question_text": "Which of the following principles, if valid, most seriously undermines the CFO's argument?",
      "options": [
        "Companies should always seek to minimize their operational costs.",
        "A company has an ethical obligation to correct billing errors regardless of remediation costs.",
        "Software glitches are an inevitable part of doing business in the technology sector.",
        "The cost of customer acquisition is typically higher than the cost of customer retention.",
        "Companies should disclose all known software defects to their customers."
      ],
      "correct_option_index": 1,
      "explanation": "If companies have an ethical obligation to correct billing errors regardless of cost, the CFO's cost-benefit reasoning is irrelevant. The principle directly invalidates the CFO's framework for the decision.",
      "option_explanations": [
        "Supports the CFO: Minimizing costs aligns with not issuing refunds.",
        "Correct: Establishes an ethical obligation that overrides cost considerations.",
        "Irrelevant: The inevitability of glitches does not address the refund decision.",
        "Tangential: While relevant to business decisions, this principle doesn't directly undermine the cost-based argument.",
        "Related but insufficient: Disclosure is different from issuing refunds."
      ],
      "target_time_seconds": 120,
      "trap_type": "scope_shift",
      "skills": [
        "principle_application",
        "ethical_reasoning"
      ]
    },
    {
      "id": "cr-014",
      "section": "verbal",
      "subsection": "critical_reasoning",
      "question_type": "weaken",
      "topic": "public_health",
      "difficulty": 3,
      "stimulus": "The health department reports that since the introduction of a free fruit program in public schools two years ago, childhood obesity rates in the district have declined by 12 percent. The department concludes that the free fruit program is responsible for the decline.",
      "premise": "Free fruit program introduced; childhood obesity declined 12% over two years.",
      "conclusion": "The fruit program caused the obesity decline.",
      "assumption": "No other factors contributed to the decline.",
      "logical_gap": "Correlation assumed to be causation; other interventions may exist.",
      "question_text": "Which of the following, if true, most weakens the department's conclusion?",
      "options": [
        "Some children in the program were already consuming adequate amounts of fruit before the program began.",
        "The district also implemented a mandatory daily physical education requirement at the same time as the fruit program.",
        "Childhood obesity rates nationwide have remained stable over the past two years.",
        "The free fruit program costs the district two million dollars per year.",
        "Parents in the district report that their children enjoy the free fruit offerings."
      ],
      "correct_option_index": 1,
      "explanation": "A simultaneous physical education requirement provides an alternative explanation for the obesity decline, weakening the claim that the fruit program alone was responsible.",
      "option_explanations": [
        "Slightly weakens but doesn't provide an alternative cause for the decline.",
        "Correct: Alternative cause\u2014PE requirement could explain the decline independently.",
        "Strengthens: Stable national rates suggest something local (possibly the program) is working.",
        "Irrelevant: Cost does not affect whether the program caused the decline.",
        "Irrelevant: Enjoyment does not address the causal claim about obesity."
      ],
      "target_time_seconds": 120,
      "trap_type": "correlation_vs_causation",
      "skills": [
        "alternative_explanation",
        "causal_reasoning"
      ]
    },
    {
      "id": "cr-015",
      "section": "verbal",
      "subsection": "critical_reasoning",
      "question_type": "strengthen",
      "topic": "technology",
      "difficulty": 3,
      "stimulus": "A tech company claims that its new AI-powered customer service chatbot will reduce average customer wait times by 60 percent while maintaining customer satisfaction above 90 percent. The company's pilot showed that the chatbot resolved 75 percent of inquiries without human intervention during a three-month trial.",
      "premise": "Pilot: chatbot resolved 75% of inquiries without human help in 3 months.",
      "conclusion": "Chatbot will reduce wait times 60% while keeping satisfaction above 90%.",
      "assumption": "Automated resolution correlates with faster service and maintained satisfaction.",
      "logical_gap": "Speed of resolution and customer satisfaction with chatbot are not directly measured.",
      "question_text": "Which of the following, if true, most strengthens the company's claim?",
      "options": [
        "The chatbot uses the same language model technology as competitors' chatbots.",
        "Customer satisfaction surveys during the pilot showed 93 percent satisfaction with chatbot-resolved inquiries, and chatbot resolution times averaged under two minutes.",
        "The company plans to hire additional human agents to handle complex inquiries.",
        "The chatbot is programmed in five languages.",
        "Competing companies have not yet deployed AI chatbots."
      ],
      "correct_option_index": 1,
      "explanation": "Direct evidence that satisfaction was 93% (above 90%) and resolution was fast during the pilot directly supports both claims: reduced wait times and high satisfaction.",
      "option_explanations": [
        "Irrelevant: Using similar technology does not support this company's specific claims.",
        "Correct: Provides direct evidence for both satisfaction and speed claims.",
        "Tangential: Hiring more agents doesn't validate the chatbot's effectiveness.",
        "Irrelevant: Language capability doesn't address wait times or satisfaction.",
        "Irrelevant: Competitor status doesn't validate the company's claims."
      ],
      "target_time_seconds": 120,
      "trap_type": "irrelevant_information",
      "skills": [
        "evidence_evaluation",
        "direct_support"
      ]
    },
    {
      "id": "cr-016",
      "section": "verbal",
      "subsection": "critical_reasoning",
      "question_type": "must_be_true",
      "topic": "business_operations",
      "difficulty": 3,
      "stimulus": "All of DataPrime's senior analysts have completed the advanced certification program. All employees who have completed the advanced certification program are eligible for the international assignment rotation. Maria is a senior analyst at DataPrime.",
      "premise": "All senior analysts completed advanced certification. All certified employees are eligible for international rotation. Maria is a senior analyst.",
      "conclusion": "N/A (must be true)",
      "assumption": "N/A",
      "logical_gap": "N/A",
      "question_text": "If the statements above are true, which of the following must also be true?",
      "options": [
        "Maria has been selected for an international assignment.",
        "Maria is eligible for the international assignment rotation.",
        "Only senior analysts are eligible for international assignments.",
        "Maria has more experience than non-senior analysts.",
        "The advanced certification program is required for all DataPrime employees."
      ],
      "correct_option_index": 1,
      "explanation": "Maria is a senior analyst \u2192 she completed the certification \u2192 she is eligible for international rotation. This chain of deduction makes B necessarily true.",
      "option_explanations": [
        "Too strong: Eligible does not mean selected.",
        "Correct: Follows necessarily from the two conditional statements and Maria's status.",
        "Too broad: Other employees may also be eligible through other paths.",
        "Not stated: Nothing about experience levels is mentioned.",
        "Not stated: The certification is stated for senior analysts only."
      ],
      "target_time_seconds": 100,
      "trap_type": "extreme_language",
      "skills": [
        "deductive_reasoning",
        "conditional_logic"
      ]
    },
    {
      "id": "cr-017",
      "section": "verbal",
      "subsection": "critical_reasoning",
      "question_type": "boldface",
      "topic": "business_strategy",
      "difficulty": 5,
      "stimulus": "Industry analysts predict that streaming services will completely replace traditional cable television within ten years. **However, cable companies still control the physical infrastructure through which most streaming content is delivered.** Some experts argue that cable companies can leverage this infrastructure advantage to remain profitable even as viewership migrates to streaming platforms. **Therefore, the prediction of cable's complete replacement is likely premature.**",
      "premise": "Cable companies control the delivery infrastructure for streaming.",
      "conclusion": "The prediction of cable's complete replacement is premature.",
      "assumption": "Infrastructure control provides a sustainable competitive advantage.",
      "logical_gap": "Whether infrastructure control translates to business survival.",
      "question_text": "In the argument above, the two boldface portions play which of the following roles?",
      "options": [
        "The first is a premise supporting the main conclusion; the second is the main conclusion.",
        "The first is evidence against the initial prediction; the second is the main conclusion drawn from that evidence.",
        "The first is the main conclusion; the second is a premise supporting it.",
        "Both are premises supporting an unstated conclusion.",
        "The first is a concession to the opposing view; the second restates the initial prediction."
      ],
      "correct_option_index": 1,
      "explanation": "The first boldface statement provides evidence (infrastructure control) that counters the prediction. The second boldface statement is the main conclusion\u2014that complete replacement is premature\u2014drawn from that evidence.",
      "option_explanations": [
        "Close but imprecise: The first is specifically evidence against the prediction, not just a generic premise.",
        "Correct: Accurately identifies the evidential role of the first and the concluding role of the second.",
        "Reversed: The conclusion is the second statement, not the first.",
        "Incorrect: The second boldface is clearly a conclusion, not a premise.",
        "Incorrect: Neither is a concession, and the second contradicts the initial prediction."
      ],
      "target_time_seconds": 150,
      "trap_type": "reversed_causality",
      "skills": [
        "boldface_analysis",
        "argument_structure"
      ]
    },
    {
      "id": "cr-018",
      "section": "verbal",
      "subsection": "critical_reasoning",
      "question_type": "weaken",
      "topic": "education",
      "difficulty": 3,
      "stimulus": "A school board argues that eliminating homework for elementary students will improve academic outcomes. The board cites studies from Finland, where elementary students receive minimal homework yet consistently outperform students in countries that assign heavy homework loads on international assessments.",
      "premise": "Finland assigns minimal homework and outperforms countries with heavy homework on assessments.",
      "conclusion": "Eliminating homework for elementary students will improve academic outcomes.",
      "assumption": "Finland's success is due to minimal homework, not other educational factors.",
      "logical_gap": "Multiple confounding factors in Finnish education system.",
      "question_text": "Which of the following, if true, most seriously weakens the school board's argument?",
      "options": [
        "Finnish teachers receive significantly more training than teachers in most other countries and spend more class time on individualized instruction.",
        "Many parents in the school district support the elimination of homework.",
        "Finland also assigns less homework to secondary school students.",
        "International assessment scores have been gradually increasing across all countries.",
        "The school board has previously implemented other successful educational reforms."
      ],
      "correct_option_index": 0,
      "explanation": "If Finnish teachers have superior training and individualized instruction, Finland's success may be due to these factors rather than minimal homework. This provides an alternative explanation that weakens the causal link between no homework and better outcomes.",
      "option_explanations": [
        "Correct: Alternative explanation\u2014teacher quality, not homework policy, drives results.",
        "Irrelevant: Parent support doesn't address whether the policy will improve outcomes.",
        "Irrelevant: Secondary school policies don't affect the elementary argument.",
        "Weakens slightly at best: General improvement doesn't explain Finland's relative advantage.",
        "Irrelevant: Past reform success doesn't validate this specific proposal."
      ],
      "target_time_seconds": 120,
      "trap_type": "unsupported_assumption",
      "skills": [
        "alternative_explanation",
        "comparative_reasoning"
      ]
    },
    {
      "id": "cr-019",
      "section": "verbal",
      "subsection": "critical_reasoning",
      "question_type": "assumption",
      "topic": "environmental_policy",
      "difficulty": 3,
      "stimulus": "An environmental group argues that switching from coal to natural gas for electricity generation will significantly reduce greenhouse gas emissions. They note that burning natural gas produces approximately 50 percent less carbon dioxide per unit of electricity than burning coal.",
      "premise": "Natural gas produces ~50% less CO2 per unit of electricity than coal.",
      "conclusion": "Switching from coal to natural gas will significantly reduce greenhouse gas emissions.",
      "assumption": "CO2 from combustion is the primary greenhouse gas concern; methane leaks do not offset the benefit.",
      "logical_gap": "Methane (CH4) leakage during natural gas extraction and transport may offset CO2 savings.",
      "question_text": "The argument assumes which of the following?",
      "options": [
        "Natural gas is cheaper to extract than coal.",
        "The reduction in CO2 from burning natural gas is not substantially offset by other greenhouse gas emissions associated with natural gas production and distribution.",
        "Coal mining causes more environmental damage than natural gas extraction.",
        "Renewable energy sources are not yet viable alternatives to fossil fuels.",
        "Carbon dioxide is the only greenhouse gas contributing to climate change."
      ],
      "correct_option_index": 1,
      "explanation": "The argument looks only at CO2 from combustion. It assumes that methane leaks during gas extraction and transport don't substantially offset the CO2 savings, making the overall emissions picture still favorable.",
      "option_explanations": [
        "Irrelevant: Cost is not part of the emissions argument.",
        "Correct: Necessary assumption that the full lifecycle emissions still favor natural gas.",
        "Out of scope: Environmental damage beyond emissions is not addressed.",
        "Not assumed: The argument compares coal to gas, not gas to renewables.",
        "Too extreme: The argument doesn't require CO2 to be the only greenhouse gas, just that other emissions don't offset the benefit."
      ],
      "target_time_seconds": 120,
      "trap_type": "scope_shift",
      "skills": [
        "assumption_identification",
        "lifecycle_analysis"
      ]
    },
    {
      "id": "cr-020",
      "section": "verbal",
      "subsection": "critical_reasoning",
      "question_type": "inference",
      "topic": "business_operations",
      "difficulty": 2,
      "stimulus": "FreshMart grocery stores require all produce suppliers to hold an organic certification. GreenFields Farm recently lost its organic certification after an inspection revealed non-compliant pesticide use. FreshMart has a strict policy of immediately terminating supply contracts with any supplier that loses its certification.",
      "premise": "FreshMart requires organic certification. GreenFields lost certification. FreshMart terminates suppliers that lose certification.",
      "conclusion": "N/A (inference)",
      "assumption": "N/A",
      "logical_gap": "N/A",
      "question_text": "If the statements above are true, which of the following can be properly inferred?",
      "options": [
        "FreshMart will need to find a new produce supplier to replace GreenFields.",
        "GreenFields used pesticides intentionally to increase crop yields.",
        "FreshMart's produce prices will increase as a result of the contract termination.",
        "GreenFields will not be able to regain its organic certification.",
        "All of FreshMart's current suppliers maintain organic certification."
      ],
      "correct_option_index": 0,
      "explanation": "GreenFields lost its certification. FreshMart terminates suppliers that lose certification. Therefore, FreshMart will terminate GreenFields' contract and need a replacement supplier.",
      "option_explanations": [
        "Correct: Logically follows from the termination policy and the certification loss.",
        "Unsupported: The intention behind the pesticide use is not stated.",
        "Unsupported: Price effects are not discussed or implied.",
        "Unsupported: Nothing prevents future recertification.",
        "Plausible but not necessarily true: Current suppliers hold certification, but 'all' is too strong without explicit confirmation."
      ],
      "target_time_seconds": 100,
      "trap_type": "extreme_language",
      "skills": [
        "deductive_reasoning",
        "policy_application"
      ]
    }
  ],
  "RC_PASSAGES": [
    {
      "id": "rc-passage-001",
      "title": "Stakeholder Capitalism and Corporate Governance",
      "category": "business",
      "difficulty": 3,
      "estimated_reading_time": 180,
      "paragraphs": [
        "For much of the twentieth century, the dominant paradigm in corporate governance was shareholder primacy\u2014the idea that a corporation's primary obligation is to maximize returns for its shareholders. This view, championed by economist Milton Friedman in his 1970 essay, held that social responsibility beyond profit maximization was tantamount to taxation without representation, as it involved spending shareholders' money on goals they had not endorsed.",
        "In recent decades, however, stakeholder capitalism has gained significant traction. Proponents argue that corporations have obligations not only to shareholders but also to employees, customers, communities, and the environment. The Business Roundtable's 2019 statement, signed by 181 CEOs, redefined the purpose of a corporation to include commitment to all stakeholders. Critics counter that without a single measurable objective, managers lack accountability and can justify virtually any decision as serving some stakeholder interest.",
        "Empirical evidence on the performance implications of stakeholder capitalism remains mixed. Some studies suggest that companies with strong environmental, social, and governance (ESG) practices outperform their peers over the long term, while others find no statistically significant relationship between ESG scores and financial returns. The methodological challenge lies in isolating the causal effect of stakeholder orientation from the many confounding variables that influence corporate performance.",
        "The practical implementation of stakeholder capitalism also presents challenges. Balancing competing stakeholder interests\u2014for example, when wage increases for employees reduce short-term returns for shareholders\u2014requires judgment calls that existing governance frameworks are not designed to adjudicate. Some scholars propose that regulatory reform, rather than voluntary corporate pledges, is the most effective path toward stakeholder accountability."
      ],
      "questions": [
        {
          "id": "rc-q-001",
          "passage_id": "rc-passage-001",
          "section": "verbal",
          "subsection": "reading_comprehension",
          "question_type": "primary_purpose",
          "topic": "business",
          "difficulty": 3,
          "target_solving_time": 90,
          "evidence_paragraphs": [
            1,
            2,
            3,
            4
          ],
          "question_text": "The primary purpose of the passage is to",
          "options": [
            "advocate for the adoption of stakeholder capitalism over shareholder primacy",
            "present the evolution, arguments, evidence, and challenges related to stakeholder capitalism",
            "demonstrate that ESG practices lead to superior financial performance",
            "criticize Milton Friedman's theory of shareholder primacy",
            "propose regulatory reforms to enforce stakeholder accountability"
          ],
          "correct_option_index": 1,
          "explanation": "The passage traces the historical shift from shareholder primacy to stakeholder capitalism, presents arguments from both sides, reviews mixed empirical evidence, and discusses implementation challenges. It is balanced and informational, not advocating a single position.",
          "option_explanations": [
            "Too one-sided: The passage presents both sides without advocating for stakeholder capitalism.",
            "Correct: Captures the passage's balanced, informational approach covering evolution, debate, evidence, and challenges.",
            "Too narrow and inaccurate: The passage notes mixed evidence, not conclusive outperformance.",
            "Too narrow: Friedman is mentioned as context, not as the target of criticism.",
            "Too narrow: Regulatory reform is mentioned in one paragraph as one possible solution, not the passage's main purpose."
          ],
          "trap_type": "too_broad",
          "skills": [
            "primary_purpose",
            "passage_structure"
          ],
          "passage_text": "For much of the twentieth century, the dominant paradigm in corporate governance was shareholder primacy\u2014the idea that a corporation's primary obligation is to maximize returns for its shareholders. This view, championed by economist Milton Friedman in his 1970 essay, held that social responsibility beyond profit maximization was tantamount to taxation without representation, as it involved spending shareholders' money on goals they had not endorsed.\n\nIn recent decades, however, stakeholder capitalism has gained significant traction. Proponents argue that corporations have obligations not only to shareholders but also to employees, customers, communities, and the environment. The Business Roundtable's 2019 statement, signed by 181 CEOs, redefined the purpose of a corporation to include commitment to all stakeholders. Critics counter that without a single measurable objective, managers lack accountability and can justify virtually any decision as serving some stakeholder interest.\n\nEmpirical evidence on the performance implications of stakeholder capitalism remains mixed. Some studies suggest that companies with strong environmental, social, and governance (ESG) practices outperform their peers over the long term, while others find no statistically significant relationship between ESG scores and financial returns. The methodological challenge lies in isolating the causal effect of stakeholder orientation from the many confounding variables that influence corporate performance.\n\nThe practical implementation of stakeholder capitalism also presents challenges. Balancing competing stakeholder interests\u2014for example, when wage increases for employees reduce short-term returns for shareholders\u2014requires judgment calls that existing governance frameworks are not designed to adjudicate. Some scholars propose that regulatory reform, rather than voluntary corporate pledges, is the most effective path toward stakeholder accountability.",
          "passage_title": "Stakeholder Capitalism and Corporate Governance",
          "passage_category": "business",
          "passage_difficulty": 3,
          "estimated_reading_time": 180,
          "paragraphs": [
            "For much of the twentieth century, the dominant paradigm in corporate governance was shareholder primacy\u2014the idea that a corporation's primary obligation is to maximize returns for its shareholders. This view, championed by economist Milton Friedman in his 1970 essay, held that social responsibility beyond profit maximization was tantamount to taxation without representation, as it involved spending shareholders' money on goals they had not endorsed.",
            "In recent decades, however, stakeholder capitalism has gained significant traction. Proponents argue that corporations have obligations not only to shareholders but also to employees, customers, communities, and the environment. The Business Roundtable's 2019 statement, signed by 181 CEOs, redefined the purpose of a corporation to include commitment to all stakeholders. Critics counter that without a single measurable objective, managers lack accountability and can justify virtually any decision as serving some stakeholder interest.",
            "Empirical evidence on the performance implications of stakeholder capitalism remains mixed. Some studies suggest that companies with strong environmental, social, and governance (ESG) practices outperform their peers over the long term, while others find no statistically significant relationship between ESG scores and financial returns. The methodological challenge lies in isolating the causal effect of stakeholder orientation from the many confounding variables that influence corporate performance.",
            "The practical implementation of stakeholder capitalism also presents challenges. Balancing competing stakeholder interests\u2014for example, when wage increases for employees reduce short-term returns for shareholders\u2014requires judgment calls that existing governance frameworks are not designed to adjudicate. Some scholars propose that regulatory reform, rather than voluntary corporate pledges, is the most effective path toward stakeholder accountability."
          ]
        },
        {
          "id": "rc-q-002",
          "passage_id": "rc-passage-001",
          "section": "verbal",
          "subsection": "reading_comprehension",
          "question_type": "detail",
          "topic": "business",
          "difficulty": 2,
          "target_solving_time": 75,
          "evidence_paragraphs": [
            2
          ],
          "question_text": "According to the passage, critics of stakeholder capitalism argue that",
          "options": [
            "corporations should never consider environmental impacts in decision-making",
            "the stakeholder model reduces corporate profitability",
            "without a single measurable objective, managers lack accountability",
            "the Business Roundtable statement was signed by too few CEOs to be meaningful",
            "shareholder primacy leads to better employee satisfaction"
          ],
          "correct_option_index": 2,
          "explanation": "Paragraph 2 explicitly states that critics argue 'without a single measurable objective, managers lack accountability and can justify virtually any decision as serving some stakeholder interest.'",
          "option_explanations": [
            "Distortion: Critics argue about accountability, not a complete ban on environmental consideration.",
            "Not stated: The passage doesn't attribute a profitability claim to the critics.",
            "Correct: Directly stated in paragraph 2.",
            "Not stated: The passage mentions 181 CEOs but critics don't challenge the number.",
            "Not stated: Critics don't make claims about employee satisfaction under shareholder primacy."
          ],
          "trap_type": "distortion",
          "skills": [
            "detail_retrieval",
            "careful_reading"
          ],
          "passage_text": "For much of the twentieth century, the dominant paradigm in corporate governance was shareholder primacy\u2014the idea that a corporation's primary obligation is to maximize returns for its shareholders. This view, championed by economist Milton Friedman in his 1970 essay, held that social responsibility beyond profit maximization was tantamount to taxation without representation, as it involved spending shareholders' money on goals they had not endorsed.\n\nIn recent decades, however, stakeholder capitalism has gained significant traction. Proponents argue that corporations have obligations not only to shareholders but also to employees, customers, communities, and the environment. The Business Roundtable's 2019 statement, signed by 181 CEOs, redefined the purpose of a corporation to include commitment to all stakeholders. Critics counter that without a single measurable objective, managers lack accountability and can justify virtually any decision as serving some stakeholder interest.\n\nEmpirical evidence on the performance implications of stakeholder capitalism remains mixed. Some studies suggest that companies with strong environmental, social, and governance (ESG) practices outperform their peers over the long term, while others find no statistically significant relationship between ESG scores and financial returns. The methodological challenge lies in isolating the causal effect of stakeholder orientation from the many confounding variables that influence corporate performance.\n\nThe practical implementation of stakeholder capitalism also presents challenges. Balancing competing stakeholder interests\u2014for example, when wage increases for employees reduce short-term returns for shareholders\u2014requires judgment calls that existing governance frameworks are not designed to adjudicate. Some scholars propose that regulatory reform, rather than voluntary corporate pledges, is the most effective path toward stakeholder accountability.",
          "passage_title": "Stakeholder Capitalism and Corporate Governance",
          "passage_category": "business",
          "passage_difficulty": 3,
          "estimated_reading_time": 180,
          "paragraphs": [
            "For much of the twentieth century, the dominant paradigm in corporate governance was shareholder primacy\u2014the idea that a corporation's primary obligation is to maximize returns for its shareholders. This view, championed by economist Milton Friedman in his 1970 essay, held that social responsibility beyond profit maximization was tantamount to taxation without representation, as it involved spending shareholders' money on goals they had not endorsed.",
            "In recent decades, however, stakeholder capitalism has gained significant traction. Proponents argue that corporations have obligations not only to shareholders but also to employees, customers, communities, and the environment. The Business Roundtable's 2019 statement, signed by 181 CEOs, redefined the purpose of a corporation to include commitment to all stakeholders. Critics counter that without a single measurable objective, managers lack accountability and can justify virtually any decision as serving some stakeholder interest.",
            "Empirical evidence on the performance implications of stakeholder capitalism remains mixed. Some studies suggest that companies with strong environmental, social, and governance (ESG) practices outperform their peers over the long term, while others find no statistically significant relationship between ESG scores and financial returns. The methodological challenge lies in isolating the causal effect of stakeholder orientation from the many confounding variables that influence corporate performance.",
            "The practical implementation of stakeholder capitalism also presents challenges. Balancing competing stakeholder interests\u2014for example, when wage increases for employees reduce short-term returns for shareholders\u2014requires judgment calls that existing governance frameworks are not designed to adjudicate. Some scholars propose that regulatory reform, rather than voluntary corporate pledges, is the most effective path toward stakeholder accountability."
          ]
        },
        {
          "id": "rc-q-003",
          "passage_id": "rc-passage-001",
          "section": "verbal",
          "subsection": "reading_comprehension",
          "question_type": "inference",
          "topic": "business",
          "difficulty": 4,
          "target_solving_time": 100,
          "evidence_paragraphs": [
            3
          ],
          "question_text": "The passage suggests that the relationship between ESG practices and financial performance is difficult to establish because",
          "options": [
            "most companies with strong ESG scores are relatively new and lack sufficient financial history",
            "ESG scoring methodologies are inconsistent across rating agencies",
            "many variables besides ESG practices affect corporate performance, making it hard to isolate ESG's specific impact",
            "shareholders consistently oppose ESG initiatives, biasing performance data",
            "companies manipulate their ESG scores to attract investors"
          ],
          "correct_option_index": 2,
          "explanation": "Paragraph 3 states 'The methodological challenge lies in isolating the causal effect of stakeholder orientation from the many confounding variables that influence corporate performance.' This directly supports option C.",
          "option_explanations": [
            "Not stated: The passage doesn't mention company age or financial history.",
            "Not stated: Rating methodology inconsistency is not mentioned in the passage.",
            "Correct: Directly supported by the passage's discussion of confounding variables.",
            "Not stated: Shareholder opposition to ESG is not mentioned.",
            "Not stated: ESG score manipulation is not discussed."
          ],
          "trap_type": "unsupported_inference",
          "skills": [
            "inference",
            "causal_reasoning"
          ],
          "passage_text": "For much of the twentieth century, the dominant paradigm in corporate governance was shareholder primacy\u2014the idea that a corporation's primary obligation is to maximize returns for its shareholders. This view, championed by economist Milton Friedman in his 1970 essay, held that social responsibility beyond profit maximization was tantamount to taxation without representation, as it involved spending shareholders' money on goals they had not endorsed.\n\nIn recent decades, however, stakeholder capitalism has gained significant traction. Proponents argue that corporations have obligations not only to shareholders but also to employees, customers, communities, and the environment. The Business Roundtable's 2019 statement, signed by 181 CEOs, redefined the purpose of a corporation to include commitment to all stakeholders. Critics counter that without a single measurable objective, managers lack accountability and can justify virtually any decision as serving some stakeholder interest.\n\nEmpirical evidence on the performance implications of stakeholder capitalism remains mixed. Some studies suggest that companies with strong environmental, social, and governance (ESG) practices outperform their peers over the long term, while others find no statistically significant relationship between ESG scores and financial returns. The methodological challenge lies in isolating the causal effect of stakeholder orientation from the many confounding variables that influence corporate performance.\n\nThe practical implementation of stakeholder capitalism also presents challenges. Balancing competing stakeholder interests\u2014for example, when wage increases for employees reduce short-term returns for shareholders\u2014requires judgment calls that existing governance frameworks are not designed to adjudicate. Some scholars propose that regulatory reform, rather than voluntary corporate pledges, is the most effective path toward stakeholder accountability.",
          "passage_title": "Stakeholder Capitalism and Corporate Governance",
          "passage_category": "business",
          "passage_difficulty": 3,
          "estimated_reading_time": 180,
          "paragraphs": [
            "For much of the twentieth century, the dominant paradigm in corporate governance was shareholder primacy\u2014the idea that a corporation's primary obligation is to maximize returns for its shareholders. This view, championed by economist Milton Friedman in his 1970 essay, held that social responsibility beyond profit maximization was tantamount to taxation without representation, as it involved spending shareholders' money on goals they had not endorsed.",
            "In recent decades, however, stakeholder capitalism has gained significant traction. Proponents argue that corporations have obligations not only to shareholders but also to employees, customers, communities, and the environment. The Business Roundtable's 2019 statement, signed by 181 CEOs, redefined the purpose of a corporation to include commitment to all stakeholders. Critics counter that without a single measurable objective, managers lack accountability and can justify virtually any decision as serving some stakeholder interest.",
            "Empirical evidence on the performance implications of stakeholder capitalism remains mixed. Some studies suggest that companies with strong environmental, social, and governance (ESG) practices outperform their peers over the long term, while others find no statistically significant relationship between ESG scores and financial returns. The methodological challenge lies in isolating the causal effect of stakeholder orientation from the many confounding variables that influence corporate performance.",
            "The practical implementation of stakeholder capitalism also presents challenges. Balancing competing stakeholder interests\u2014for example, when wage increases for employees reduce short-term returns for shareholders\u2014requires judgment calls that existing governance frameworks are not designed to adjudicate. Some scholars propose that regulatory reform, rather than voluntary corporate pledges, is the most effective path toward stakeholder accountability."
          ]
        },
        {
          "id": "rc-q-004",
          "passage_id": "rc-passage-001",
          "section": "verbal",
          "subsection": "reading_comprehension",
          "question_type": "function_of_paragraph",
          "topic": "business",
          "difficulty": 3,
          "target_solving_time": 90,
          "evidence_paragraphs": [
            4
          ],
          "question_text": "The fourth paragraph primarily serves to",
          "options": [
            "summarize the arguments presented in the first three paragraphs",
            "present counterevidence against the claims made in paragraph 3",
            "discuss practical difficulties in implementing stakeholder capitalism and suggest a possible solution",
            "argue that regulatory reform is the only viable approach to corporate governance",
            "provide examples of successful stakeholder capitalism implementations"
          ],
          "correct_option_index": 2,
          "explanation": "Paragraph 4 discusses practical challenges (balancing competing interests, inadequate governance frameworks) and mentions regulatory reform as a possible path forward. It addresses implementation, not theory.",
          "option_explanations": [
            "Incorrect: It introduces new content about implementation, not a summary.",
            "Incorrect: It does not counter paragraph 3's evidence discussion.",
            "Correct: Identifies implementation challenges and suggests regulatory reform.",
            "Too extreme: It mentions regulatory reform as one proposal, not the 'only viable approach.'",
            "Incorrect: No specific success examples are given."
          ],
          "trap_type": "too_narrow",
          "skills": [
            "paragraph_function",
            "passage_structure"
          ],
          "passage_text": "For much of the twentieth century, the dominant paradigm in corporate governance was shareholder primacy\u2014the idea that a corporation's primary obligation is to maximize returns for its shareholders. This view, championed by economist Milton Friedman in his 1970 essay, held that social responsibility beyond profit maximization was tantamount to taxation without representation, as it involved spending shareholders' money on goals they had not endorsed.\n\nIn recent decades, however, stakeholder capitalism has gained significant traction. Proponents argue that corporations have obligations not only to shareholders but also to employees, customers, communities, and the environment. The Business Roundtable's 2019 statement, signed by 181 CEOs, redefined the purpose of a corporation to include commitment to all stakeholders. Critics counter that without a single measurable objective, managers lack accountability and can justify virtually any decision as serving some stakeholder interest.\n\nEmpirical evidence on the performance implications of stakeholder capitalism remains mixed. Some studies suggest that companies with strong environmental, social, and governance (ESG) practices outperform their peers over the long term, while others find no statistically significant relationship between ESG scores and financial returns. The methodological challenge lies in isolating the causal effect of stakeholder orientation from the many confounding variables that influence corporate performance.\n\nThe practical implementation of stakeholder capitalism also presents challenges. Balancing competing stakeholder interests\u2014for example, when wage increases for employees reduce short-term returns for shareholders\u2014requires judgment calls that existing governance frameworks are not designed to adjudicate. Some scholars propose that regulatory reform, rather than voluntary corporate pledges, is the most effective path toward stakeholder accountability.",
          "passage_title": "Stakeholder Capitalism and Corporate Governance",
          "passage_category": "business",
          "passage_difficulty": 3,
          "estimated_reading_time": 180,
          "paragraphs": [
            "For much of the twentieth century, the dominant paradigm in corporate governance was shareholder primacy\u2014the idea that a corporation's primary obligation is to maximize returns for its shareholders. This view, championed by economist Milton Friedman in his 1970 essay, held that social responsibility beyond profit maximization was tantamount to taxation without representation, as it involved spending shareholders' money on goals they had not endorsed.",
            "In recent decades, however, stakeholder capitalism has gained significant traction. Proponents argue that corporations have obligations not only to shareholders but also to employees, customers, communities, and the environment. The Business Roundtable's 2019 statement, signed by 181 CEOs, redefined the purpose of a corporation to include commitment to all stakeholders. Critics counter that without a single measurable objective, managers lack accountability and can justify virtually any decision as serving some stakeholder interest.",
            "Empirical evidence on the performance implications of stakeholder capitalism remains mixed. Some studies suggest that companies with strong environmental, social, and governance (ESG) practices outperform their peers over the long term, while others find no statistically significant relationship between ESG scores and financial returns. The methodological challenge lies in isolating the causal effect of stakeholder orientation from the many confounding variables that influence corporate performance.",
            "The practical implementation of stakeholder capitalism also presents challenges. Balancing competing stakeholder interests\u2014for example, when wage increases for employees reduce short-term returns for shareholders\u2014requires judgment calls that existing governance frameworks are not designed to adjudicate. Some scholars propose that regulatory reform, rather than voluntary corporate pledges, is the most effective path toward stakeholder accountability."
          ]
        }
      ]
    },
    {
      "id": "rc-passage-002",
      "title": "Monetary Policy in the Age of Digital Currencies",
      "category": "economics",
      "difficulty": 4,
      "estimated_reading_time": 190,
      "paragraphs": [
        "Central banks have traditionally managed monetary policy through three primary instruments: setting benchmark interest rates, conducting open market operations, and adjusting reserve requirements for commercial banks. These tools operate through the banking system, influencing the cost and availability of credit to shape economic activity. The effectiveness of these instruments depends on the assumption that the vast majority of economic transactions flow through regulated financial institutions.",
        "The emergence of decentralized digital currencies, particularly those built on blockchain technology, threatens to undermine this assumption. If a significant share of transactions migrates to cryptocurrency networks that operate outside the traditional banking system, central banks may find their monetary policy transmission mechanisms weakened. A consumer who holds savings in Bitcoin rather than a bank deposit is not directly affected by changes in the central bank's interest rate.",
        "Central bank digital currencies (CBDCs) represent one response to this challenge. By issuing their own digital currencies, central banks could maintain direct influence over the money supply even in an increasingly digital economy. China's digital yuan and the European Central Bank's digital euro project are among the most advanced CBDC initiatives. Proponents argue that CBDCs could enhance financial inclusion, reduce transaction costs, and strengthen monetary policy transmission.",
        "However, CBDCs also raise significant concerns. A CBDC that allows the central bank to monitor all transactions could compromise financial privacy. Furthermore, if consumers can hold CBDC balances directly with the central bank, commercial banks could face deposit outflows during periods of financial stress, potentially amplifying bank runs rather than preventing them. Designing a CBDC that balances innovation with stability remains an open challenge for policymakers."
      ],
      "questions": [
        {
          "id": "rc-q-005",
          "passage_id": "rc-passage-002",
          "section": "verbal",
          "subsection": "reading_comprehension",
          "question_type": "main_idea",
          "topic": "economics",
          "difficulty": 3,
          "target_solving_time": 90,
          "evidence_paragraphs": [
            1,
            2,
            3,
            4
          ],
          "question_text": "Which of the following best describes the main idea of the passage?",
          "options": [
            "Central bank digital currencies are superior to decentralized cryptocurrencies.",
            "Digital currencies pose challenges to traditional monetary policy, and CBDCs present both opportunities and risks as a response.",
            "The traditional instruments of monetary policy are no longer effective in the modern economy.",
            "China and Europe are leading the development of central bank digital currencies.",
            "Decentralized cryptocurrencies will inevitably replace traditional banking systems."
          ],
          "correct_option_index": 1,
          "explanation": "The passage explains how digital currencies challenge monetary policy (P1-P2), introduces CBDCs as a response with benefits (P3), and discusses their risks (P4). Option B captures this balanced arc.",
          "option_explanations": [
            "Too one-sided: The passage presents benefits and concerns of CBDCs.",
            "Correct: Captures the challenge, response, and balanced evaluation.",
            "Too extreme: The passage says tools may be weakened, not that they are no longer effective.",
            "Too narrow: Specific CBDC projects are details, not the main idea.",
            "Too extreme: 'Inevitably replace' is not supported by the passage."
          ],
          "trap_type": "too_broad",
          "skills": [
            "main_idea",
            "passage_comprehension"
          ],
          "passage_text": "Central banks have traditionally managed monetary policy through three primary instruments: setting benchmark interest rates, conducting open market operations, and adjusting reserve requirements for commercial banks. These tools operate through the banking system, influencing the cost and availability of credit to shape economic activity. The effectiveness of these instruments depends on the assumption that the vast majority of economic transactions flow through regulated financial institutions.\n\nThe emergence of decentralized digital currencies, particularly those built on blockchain technology, threatens to undermine this assumption. If a significant share of transactions migrates to cryptocurrency networks that operate outside the traditional banking system, central banks may find their monetary policy transmission mechanisms weakened. A consumer who holds savings in Bitcoin rather than a bank deposit is not directly affected by changes in the central bank's interest rate.\n\nCentral bank digital currencies (CBDCs) represent one response to this challenge. By issuing their own digital currencies, central banks could maintain direct influence over the money supply even in an increasingly digital economy. China's digital yuan and the European Central Bank's digital euro project are among the most advanced CBDC initiatives. Proponents argue that CBDCs could enhance financial inclusion, reduce transaction costs, and strengthen monetary policy transmission.\n\nHowever, CBDCs also raise significant concerns. A CBDC that allows the central bank to monitor all transactions could compromise financial privacy. Furthermore, if consumers can hold CBDC balances directly with the central bank, commercial banks could face deposit outflows during periods of financial stress, potentially amplifying bank runs rather than preventing them. Designing a CBDC that balances innovation with stability remains an open challenge for policymakers.",
          "passage_title": "Monetary Policy in the Age of Digital Currencies",
          "passage_category": "economics",
          "passage_difficulty": 4,
          "estimated_reading_time": 190,
          "paragraphs": [
            "Central banks have traditionally managed monetary policy through three primary instruments: setting benchmark interest rates, conducting open market operations, and adjusting reserve requirements for commercial banks. These tools operate through the banking system, influencing the cost and availability of credit to shape economic activity. The effectiveness of these instruments depends on the assumption that the vast majority of economic transactions flow through regulated financial institutions.",
            "The emergence of decentralized digital currencies, particularly those built on blockchain technology, threatens to undermine this assumption. If a significant share of transactions migrates to cryptocurrency networks that operate outside the traditional banking system, central banks may find their monetary policy transmission mechanisms weakened. A consumer who holds savings in Bitcoin rather than a bank deposit is not directly affected by changes in the central bank's interest rate.",
            "Central bank digital currencies (CBDCs) represent one response to this challenge. By issuing their own digital currencies, central banks could maintain direct influence over the money supply even in an increasingly digital economy. China's digital yuan and the European Central Bank's digital euro project are among the most advanced CBDC initiatives. Proponents argue that CBDCs could enhance financial inclusion, reduce transaction costs, and strengthen monetary policy transmission.",
            "However, CBDCs also raise significant concerns. A CBDC that allows the central bank to monitor all transactions could compromise financial privacy. Furthermore, if consumers can hold CBDC balances directly with the central bank, commercial banks could face deposit outflows during periods of financial stress, potentially amplifying bank runs rather than preventing them. Designing a CBDC that balances innovation with stability remains an open challenge for policymakers."
          ]
        },
        {
          "id": "rc-q-006",
          "passage_id": "rc-passage-002",
          "section": "verbal",
          "subsection": "reading_comprehension",
          "question_type": "authors_tone",
          "topic": "economics",
          "difficulty": 3,
          "target_solving_time": 80,
          "evidence_paragraphs": [
            1,
            2,
            3,
            4
          ],
          "question_text": "The author's tone in discussing CBDCs can best be described as",
          "options": [
            "enthusiastically supportive",
            "dismissive and skeptical",
            "analytically balanced, acknowledging both potential and concerns",
            "cautiously optimistic about their inevitable success",
            "deeply alarmed about privacy implications"
          ],
          "correct_option_index": 2,
          "explanation": "The author presents CBDC benefits (P3) and concerns (P4) without advocating for or against them. The tone is analytical and balanced throughout.",
          "option_explanations": [
            "Too positive: The author also raises significant concerns.",
            "Too negative: The author acknowledges potential benefits.",
            "Correct: Balanced analytical tone presenting both sides.",
            "Contradicted: The author does not suggest CBDCs are inevitable.",
            "Too extreme: Privacy is one concern mentioned, not the author's dominant attitude."
          ],
          "trap_type": "distortion",
          "skills": [
            "tone_identification",
            "authorial_perspective"
          ],
          "passage_text": "Central banks have traditionally managed monetary policy through three primary instruments: setting benchmark interest rates, conducting open market operations, and adjusting reserve requirements for commercial banks. These tools operate through the banking system, influencing the cost and availability of credit to shape economic activity. The effectiveness of these instruments depends on the assumption that the vast majority of economic transactions flow through regulated financial institutions.\n\nThe emergence of decentralized digital currencies, particularly those built on blockchain technology, threatens to undermine this assumption. If a significant share of transactions migrates to cryptocurrency networks that operate outside the traditional banking system, central banks may find their monetary policy transmission mechanisms weakened. A consumer who holds savings in Bitcoin rather than a bank deposit is not directly affected by changes in the central bank's interest rate.\n\nCentral bank digital currencies (CBDCs) represent one response to this challenge. By issuing their own digital currencies, central banks could maintain direct influence over the money supply even in an increasingly digital economy. China's digital yuan and the European Central Bank's digital euro project are among the most advanced CBDC initiatives. Proponents argue that CBDCs could enhance financial inclusion, reduce transaction costs, and strengthen monetary policy transmission.\n\nHowever, CBDCs also raise significant concerns. A CBDC that allows the central bank to monitor all transactions could compromise financial privacy. Furthermore, if consumers can hold CBDC balances directly with the central bank, commercial banks could face deposit outflows during periods of financial stress, potentially amplifying bank runs rather than preventing them. Designing a CBDC that balances innovation with stability remains an open challenge for policymakers.",
          "passage_title": "Monetary Policy in the Age of Digital Currencies",
          "passage_category": "economics",
          "passage_difficulty": 4,
          "estimated_reading_time": 190,
          "paragraphs": [
            "Central banks have traditionally managed monetary policy through three primary instruments: setting benchmark interest rates, conducting open market operations, and adjusting reserve requirements for commercial banks. These tools operate through the banking system, influencing the cost and availability of credit to shape economic activity. The effectiveness of these instruments depends on the assumption that the vast majority of economic transactions flow through regulated financial institutions.",
            "The emergence of decentralized digital currencies, particularly those built on blockchain technology, threatens to undermine this assumption. If a significant share of transactions migrates to cryptocurrency networks that operate outside the traditional banking system, central banks may find their monetary policy transmission mechanisms weakened. A consumer who holds savings in Bitcoin rather than a bank deposit is not directly affected by changes in the central bank's interest rate.",
            "Central bank digital currencies (CBDCs) represent one response to this challenge. By issuing their own digital currencies, central banks could maintain direct influence over the money supply even in an increasingly digital economy. China's digital yuan and the European Central Bank's digital euro project are among the most advanced CBDC initiatives. Proponents argue that CBDCs could enhance financial inclusion, reduce transaction costs, and strengthen monetary policy transmission.",
            "However, CBDCs also raise significant concerns. A CBDC that allows the central bank to monitor all transactions could compromise financial privacy. Furthermore, if consumers can hold CBDC balances directly with the central bank, commercial banks could face deposit outflows during periods of financial stress, potentially amplifying bank runs rather than preventing them. Designing a CBDC that balances innovation with stability remains an open challenge for policymakers."
          ]
        },
        {
          "id": "rc-q-007",
          "passage_id": "rc-passage-002",
          "section": "verbal",
          "subsection": "reading_comprehension",
          "question_type": "detail",
          "topic": "economics",
          "difficulty": 2,
          "target_solving_time": 75,
          "evidence_paragraphs": [
            1
          ],
          "question_text": "According to paragraph 1, the effectiveness of traditional monetary policy instruments depends on",
          "options": [
            "the central bank's ability to set negative interest rates",
            "the majority of economic transactions flowing through regulated financial institutions",
            "government fiscal policy working in coordination with monetary policy",
            "commercial banks voluntarily cooperating with central bank directives",
            "consumer confidence in the stability of the national currency"
          ],
          "correct_option_index": 1,
          "explanation": "Paragraph 1 explicitly states: 'The effectiveness of these instruments depends on the assumption that the vast majority of economic transactions flow through regulated financial institutions.'",
          "option_explanations": [
            "Not stated: Negative rates are not mentioned.",
            "Correct: Directly stated in paragraph 1.",
            "Not stated: Fiscal policy coordination is not discussed.",
            "Not stated: Voluntary cooperation is not the stated dependency.",
            "Not stated: Consumer confidence is not mentioned as a dependency."
          ],
          "trap_type": "out_of_scope",
          "skills": [
            "detail_retrieval"
          ],
          "passage_text": "Central banks have traditionally managed monetary policy through three primary instruments: setting benchmark interest rates, conducting open market operations, and adjusting reserve requirements for commercial banks. These tools operate through the banking system, influencing the cost and availability of credit to shape economic activity. The effectiveness of these instruments depends on the assumption that the vast majority of economic transactions flow through regulated financial institutions.\n\nThe emergence of decentralized digital currencies, particularly those built on blockchain technology, threatens to undermine this assumption. If a significant share of transactions migrates to cryptocurrency networks that operate outside the traditional banking system, central banks may find their monetary policy transmission mechanisms weakened. A consumer who holds savings in Bitcoin rather than a bank deposit is not directly affected by changes in the central bank's interest rate.\n\nCentral bank digital currencies (CBDCs) represent one response to this challenge. By issuing their own digital currencies, central banks could maintain direct influence over the money supply even in an increasingly digital economy. China's digital yuan and the European Central Bank's digital euro project are among the most advanced CBDC initiatives. Proponents argue that CBDCs could enhance financial inclusion, reduce transaction costs, and strengthen monetary policy transmission.\n\nHowever, CBDCs also raise significant concerns. A CBDC that allows the central bank to monitor all transactions could compromise financial privacy. Furthermore, if consumers can hold CBDC balances directly with the central bank, commercial banks could face deposit outflows during periods of financial stress, potentially amplifying bank runs rather than preventing them. Designing a CBDC that balances innovation with stability remains an open challenge for policymakers.",
          "passage_title": "Monetary Policy in the Age of Digital Currencies",
          "passage_category": "economics",
          "passage_difficulty": 4,
          "estimated_reading_time": 190,
          "paragraphs": [
            "Central banks have traditionally managed monetary policy through three primary instruments: setting benchmark interest rates, conducting open market operations, and adjusting reserve requirements for commercial banks. These tools operate through the banking system, influencing the cost and availability of credit to shape economic activity. The effectiveness of these instruments depends on the assumption that the vast majority of economic transactions flow through regulated financial institutions.",
            "The emergence of decentralized digital currencies, particularly those built on blockchain technology, threatens to undermine this assumption. If a significant share of transactions migrates to cryptocurrency networks that operate outside the traditional banking system, central banks may find their monetary policy transmission mechanisms weakened. A consumer who holds savings in Bitcoin rather than a bank deposit is not directly affected by changes in the central bank's interest rate.",
            "Central bank digital currencies (CBDCs) represent one response to this challenge. By issuing their own digital currencies, central banks could maintain direct influence over the money supply even in an increasingly digital economy. China's digital yuan and the European Central Bank's digital euro project are among the most advanced CBDC initiatives. Proponents argue that CBDCs could enhance financial inclusion, reduce transaction costs, and strengthen monetary policy transmission.",
            "However, CBDCs also raise significant concerns. A CBDC that allows the central bank to monitor all transactions could compromise financial privacy. Furthermore, if consumers can hold CBDC balances directly with the central bank, commercial banks could face deposit outflows during periods of financial stress, potentially amplifying bank runs rather than preventing them. Designing a CBDC that balances innovation with stability remains an open challenge for policymakers."
          ]
        }
      ]
    },
    {
      "id": "rc-passage-003",
      "title": "Epigenetics and Environmental Influence on Gene Expression",
      "category": "science",
      "difficulty": 4,
      "estimated_reading_time": 200,
      "paragraphs": [
        "The central dogma of molecular biology\u2014that genetic information flows from DNA to RNA to protein\u2014long suggested that an organism's traits are determined primarily by the nucleotide sequences it inherits. Under this view, environmental factors could select among organisms with different genotypes but could not alter the genetic instructions themselves. The discovery of epigenetic mechanisms has fundamentally complicated this picture.",
        "Epigenetic modifications, such as DNA methylation and histone acetylation, can alter gene expression without changing the underlying DNA sequence. These chemical markers act as molecular switches, turning genes on or off in response to environmental signals. A landmark study of Dutch famine survivors demonstrated that individuals exposed to severe caloric restriction in utero exhibited distinct methylation patterns decades later, with corresponding increases in rates of cardiovascular disease and metabolic disorders.",
        "Perhaps most provocatively, some research suggests that epigenetic changes can be transmitted across generations. Studies in rodents have shown that environmental stressors experienced by parents can produce epigenetic alterations that appear in offspring who were never directly exposed to those stressors. If confirmed in humans, transgenerational epigenetic inheritance would imply that environmental experiences can shape the biology of descendants in ways that neither classical genetics nor Darwinian natural selection fully anticipated.",
        "However, the field remains contentious. Critics argue that many transgenerational studies suffer from small sample sizes and fail to rule out confounding factors such as shared environments, maternal behavior, and microbiome transmission. Distinguishing genuine epigenetic inheritance from these alternative mechanisms remains a significant methodological challenge. Nonetheless, the growing body of evidence has prompted a reexamination of the boundary between nature and nurture."
      ],
      "questions": [
        {
          "id": "rc-q-008",
          "passage_id": "rc-passage-003",
          "section": "verbal",
          "subsection": "reading_comprehension",
          "question_type": "main_idea",
          "topic": "science",
          "difficulty": 3,
          "target_solving_time": 90,
          "evidence_paragraphs": [
            1,
            2,
            3,
            4
          ],
          "question_text": "The passage is primarily concerned with",
          "options": [
            "disproving the central dogma of molecular biology",
            "describing how epigenetic mechanisms challenge traditional views of genetic determinism while noting ongoing scientific debates",
            "advocating for increased funding for epigenetic research",
            "explaining the molecular mechanism of DNA methylation in detail",
            "comparing the Dutch famine study with rodent epigenetic studies"
          ],
          "correct_option_index": 1,
          "explanation": "The passage introduces traditional genetics, explains how epigenetics challenges it, discusses transgenerational inheritance, and presents the scientific debate. This balanced overview matches option B.",
          "option_explanations": [
            "Too strong: The passage says epigenetics 'complicated' the picture, not disproved the dogma.",
            "Correct: Captures the challenge to traditional views and the ongoing debates.",
            "Not the purpose: Funding advocacy is not mentioned.",
            "Too narrow: DNA methylation details are supporting evidence, not the main concern.",
            "Too narrow: The studies are examples, not the central comparison."
          ],
          "trap_type": "too_broad",
          "skills": [
            "main_idea",
            "scientific_reasoning"
          ],
          "passage_text": "The central dogma of molecular biology\u2014that genetic information flows from DNA to RNA to protein\u2014long suggested that an organism's traits are determined primarily by the nucleotide sequences it inherits. Under this view, environmental factors could select among organisms with different genotypes but could not alter the genetic instructions themselves. The discovery of epigenetic mechanisms has fundamentally complicated this picture.\n\nEpigenetic modifications, such as DNA methylation and histone acetylation, can alter gene expression without changing the underlying DNA sequence. These chemical markers act as molecular switches, turning genes on or off in response to environmental signals. A landmark study of Dutch famine survivors demonstrated that individuals exposed to severe caloric restriction in utero exhibited distinct methylation patterns decades later, with corresponding increases in rates of cardiovascular disease and metabolic disorders.\n\nPerhaps most provocatively, some research suggests that epigenetic changes can be transmitted across generations. Studies in rodents have shown that environmental stressors experienced by parents can produce epigenetic alterations that appear in offspring who were never directly exposed to those stressors. If confirmed in humans, transgenerational epigenetic inheritance would imply that environmental experiences can shape the biology of descendants in ways that neither classical genetics nor Darwinian natural selection fully anticipated.\n\nHowever, the field remains contentious. Critics argue that many transgenerational studies suffer from small sample sizes and fail to rule out confounding factors such as shared environments, maternal behavior, and microbiome transmission. Distinguishing genuine epigenetic inheritance from these alternative mechanisms remains a significant methodological challenge. Nonetheless, the growing body of evidence has prompted a reexamination of the boundary between nature and nurture.",
          "passage_title": "Epigenetics and Environmental Influence on Gene Expression",
          "passage_category": "science",
          "passage_difficulty": 4,
          "estimated_reading_time": 200,
          "paragraphs": [
            "The central dogma of molecular biology\u2014that genetic information flows from DNA to RNA to protein\u2014long suggested that an organism's traits are determined primarily by the nucleotide sequences it inherits. Under this view, environmental factors could select among organisms with different genotypes but could not alter the genetic instructions themselves. The discovery of epigenetic mechanisms has fundamentally complicated this picture.",
            "Epigenetic modifications, such as DNA methylation and histone acetylation, can alter gene expression without changing the underlying DNA sequence. These chemical markers act as molecular switches, turning genes on or off in response to environmental signals. A landmark study of Dutch famine survivors demonstrated that individuals exposed to severe caloric restriction in utero exhibited distinct methylation patterns decades later, with corresponding increases in rates of cardiovascular disease and metabolic disorders.",
            "Perhaps most provocatively, some research suggests that epigenetic changes can be transmitted across generations. Studies in rodents have shown that environmental stressors experienced by parents can produce epigenetic alterations that appear in offspring who were never directly exposed to those stressors. If confirmed in humans, transgenerational epigenetic inheritance would imply that environmental experiences can shape the biology of descendants in ways that neither classical genetics nor Darwinian natural selection fully anticipated.",
            "However, the field remains contentious. Critics argue that many transgenerational studies suffer from small sample sizes and fail to rule out confounding factors such as shared environments, maternal behavior, and microbiome transmission. Distinguishing genuine epigenetic inheritance from these alternative mechanisms remains a significant methodological challenge. Nonetheless, the growing body of evidence has prompted a reexamination of the boundary between nature and nurture."
          ]
        },
        {
          "id": "rc-q-009",
          "passage_id": "rc-passage-003",
          "section": "verbal",
          "subsection": "reading_comprehension",
          "question_type": "function_of_sentence",
          "topic": "science",
          "difficulty": 4,
          "target_solving_time": 100,
          "evidence_paragraphs": [
            2
          ],
          "question_text": "The reference to the Dutch famine survivors primarily serves to",
          "options": [
            "argue that famine conditions are the primary cause of cardiovascular disease",
            "provide concrete evidence that environmental conditions can produce lasting epigenetic changes in humans",
            "contrast European and Asian epigenetic research methodologies",
            "suggest that epigenetic changes are always harmful",
            "demonstrate that DNA methylation is the only epigenetic mechanism"
          ],
          "correct_option_index": 1,
          "explanation": "The Dutch famine study is cited as 'a landmark study' providing concrete evidence that environmental conditions (caloric restriction in utero) produce measurable epigenetic changes (distinct methylation patterns) decades later.",
          "option_explanations": [
            "Too extreme: The passage does not claim famine is the primary cause.",
            "Correct: Concrete evidence linking environment to lasting epigenetic changes.",
            "Not stated: No methodology comparison is made.",
            "Too broad: The passage discusses one harmful example but doesn't generalize.",
            "Not stated: DNA methylation is one mechanism; the passage also mentions histone acetylation."
          ],
          "trap_type": "too_broad",
          "skills": [
            "function_identification",
            "evidence_evaluation"
          ],
          "passage_text": "The central dogma of molecular biology\u2014that genetic information flows from DNA to RNA to protein\u2014long suggested that an organism's traits are determined primarily by the nucleotide sequences it inherits. Under this view, environmental factors could select among organisms with different genotypes but could not alter the genetic instructions themselves. The discovery of epigenetic mechanisms has fundamentally complicated this picture.\n\nEpigenetic modifications, such as DNA methylation and histone acetylation, can alter gene expression without changing the underlying DNA sequence. These chemical markers act as molecular switches, turning genes on or off in response to environmental signals. A landmark study of Dutch famine survivors demonstrated that individuals exposed to severe caloric restriction in utero exhibited distinct methylation patterns decades later, with corresponding increases in rates of cardiovascular disease and metabolic disorders.\n\nPerhaps most provocatively, some research suggests that epigenetic changes can be transmitted across generations. Studies in rodents have shown that environmental stressors experienced by parents can produce epigenetic alterations that appear in offspring who were never directly exposed to those stressors. If confirmed in humans, transgenerational epigenetic inheritance would imply that environmental experiences can shape the biology of descendants in ways that neither classical genetics nor Darwinian natural selection fully anticipated.\n\nHowever, the field remains contentious. Critics argue that many transgenerational studies suffer from small sample sizes and fail to rule out confounding factors such as shared environments, maternal behavior, and microbiome transmission. Distinguishing genuine epigenetic inheritance from these alternative mechanisms remains a significant methodological challenge. Nonetheless, the growing body of evidence has prompted a reexamination of the boundary between nature and nurture.",
          "passage_title": "Epigenetics and Environmental Influence on Gene Expression",
          "passage_category": "science",
          "passage_difficulty": 4,
          "estimated_reading_time": 200,
          "paragraphs": [
            "The central dogma of molecular biology\u2014that genetic information flows from DNA to RNA to protein\u2014long suggested that an organism's traits are determined primarily by the nucleotide sequences it inherits. Under this view, environmental factors could select among organisms with different genotypes but could not alter the genetic instructions themselves. The discovery of epigenetic mechanisms has fundamentally complicated this picture.",
            "Epigenetic modifications, such as DNA methylation and histone acetylation, can alter gene expression without changing the underlying DNA sequence. These chemical markers act as molecular switches, turning genes on or off in response to environmental signals. A landmark study of Dutch famine survivors demonstrated that individuals exposed to severe caloric restriction in utero exhibited distinct methylation patterns decades later, with corresponding increases in rates of cardiovascular disease and metabolic disorders.",
            "Perhaps most provocatively, some research suggests that epigenetic changes can be transmitted across generations. Studies in rodents have shown that environmental stressors experienced by parents can produce epigenetic alterations that appear in offspring who were never directly exposed to those stressors. If confirmed in humans, transgenerational epigenetic inheritance would imply that environmental experiences can shape the biology of descendants in ways that neither classical genetics nor Darwinian natural selection fully anticipated.",
            "However, the field remains contentious. Critics argue that many transgenerational studies suffer from small sample sizes and fail to rule out confounding factors such as shared environments, maternal behavior, and microbiome transmission. Distinguishing genuine epigenetic inheritance from these alternative mechanisms remains a significant methodological challenge. Nonetheless, the growing body of evidence has prompted a reexamination of the boundary between nature and nurture."
          ]
        },
        {
          "id": "rc-q-010",
          "passage_id": "rc-passage-003",
          "section": "verbal",
          "subsection": "reading_comprehension",
          "question_type": "inference",
          "topic": "science",
          "difficulty": 4,
          "target_solving_time": 100,
          "evidence_paragraphs": [
            3,
            4
          ],
          "question_text": "It can be inferred from the passage that the author views transgenerational epigenetic inheritance in humans as",
          "options": [
            "definitively proven by existing research",
            "an intriguing possibility that has not yet been conclusively established",
            "impossible given the current understanding of molecular biology",
            "relevant only to rodent models and not applicable to humans",
            "a theory that has been thoroughly refuted by recent studies"
          ],
          "correct_option_index": 1,
          "explanation": "Paragraph 3 uses 'if confirmed in humans' and 'would imply,' indicating it's a possibility, not established fact. Paragraph 4 notes the field is 'contentious' with methodological challenges. This supports option B.",
          "option_explanations": [
            "Contradicted: 'If confirmed' indicates it's not yet proven.",
            "Correct: The conditional language and ongoing debates support this characterization.",
            "Contradicted: The author presents it as plausible, not impossible.",
            "Contradicted: The author speculates about human implications ('if confirmed in humans').",
            "Contradicted: Critics raise concerns but the theory has not been refuted."
          ],
          "trap_type": "distortion",
          "skills": [
            "inference",
            "authorial_stance"
          ],
          "passage_text": "The central dogma of molecular biology\u2014that genetic information flows from DNA to RNA to protein\u2014long suggested that an organism's traits are determined primarily by the nucleotide sequences it inherits. Under this view, environmental factors could select among organisms with different genotypes but could not alter the genetic instructions themselves. The discovery of epigenetic mechanisms has fundamentally complicated this picture.\n\nEpigenetic modifications, such as DNA methylation and histone acetylation, can alter gene expression without changing the underlying DNA sequence. These chemical markers act as molecular switches, turning genes on or off in response to environmental signals. A landmark study of Dutch famine survivors demonstrated that individuals exposed to severe caloric restriction in utero exhibited distinct methylation patterns decades later, with corresponding increases in rates of cardiovascular disease and metabolic disorders.\n\nPerhaps most provocatively, some research suggests that epigenetic changes can be transmitted across generations. Studies in rodents have shown that environmental stressors experienced by parents can produce epigenetic alterations that appear in offspring who were never directly exposed to those stressors. If confirmed in humans, transgenerational epigenetic inheritance would imply that environmental experiences can shape the biology of descendants in ways that neither classical genetics nor Darwinian natural selection fully anticipated.\n\nHowever, the field remains contentious. Critics argue that many transgenerational studies suffer from small sample sizes and fail to rule out confounding factors such as shared environments, maternal behavior, and microbiome transmission. Distinguishing genuine epigenetic inheritance from these alternative mechanisms remains a significant methodological challenge. Nonetheless, the growing body of evidence has prompted a reexamination of the boundary between nature and nurture.",
          "passage_title": "Epigenetics and Environmental Influence on Gene Expression",
          "passage_category": "science",
          "passage_difficulty": 4,
          "estimated_reading_time": 200,
          "paragraphs": [
            "The central dogma of molecular biology\u2014that genetic information flows from DNA to RNA to protein\u2014long suggested that an organism's traits are determined primarily by the nucleotide sequences it inherits. Under this view, environmental factors could select among organisms with different genotypes but could not alter the genetic instructions themselves. The discovery of epigenetic mechanisms has fundamentally complicated this picture.",
            "Epigenetic modifications, such as DNA methylation and histone acetylation, can alter gene expression without changing the underlying DNA sequence. These chemical markers act as molecular switches, turning genes on or off in response to environmental signals. A landmark study of Dutch famine survivors demonstrated that individuals exposed to severe caloric restriction in utero exhibited distinct methylation patterns decades later, with corresponding increases in rates of cardiovascular disease and metabolic disorders.",
            "Perhaps most provocatively, some research suggests that epigenetic changes can be transmitted across generations. Studies in rodents have shown that environmental stressors experienced by parents can produce epigenetic alterations that appear in offspring who were never directly exposed to those stressors. If confirmed in humans, transgenerational epigenetic inheritance would imply that environmental experiences can shape the biology of descendants in ways that neither classical genetics nor Darwinian natural selection fully anticipated.",
            "However, the field remains contentious. Critics argue that many transgenerational studies suffer from small sample sizes and fail to rule out confounding factors such as shared environments, maternal behavior, and microbiome transmission. Distinguishing genuine epigenetic inheritance from these alternative mechanisms remains a significant methodological challenge. Nonetheless, the growing body of evidence has prompted a reexamination of the boundary between nature and nurture."
          ]
        }
      ]
    },
    {
      "id": "rc-passage-004",
      "title": "Artificial Intelligence in Medical Diagnostics",
      "category": "technology",
      "difficulty": 3,
      "estimated_reading_time": 180,
      "paragraphs": [
        "The application of artificial intelligence to medical diagnostics has generated considerable excitement in the healthcare community. Deep learning algorithms, particularly convolutional neural networks, have demonstrated remarkable accuracy in identifying certain conditions from medical images. In some controlled studies, these systems have matched or exceeded the diagnostic accuracy of experienced radiologists in detecting specific cancers from mammograms and identifying diabetic retinopathy from fundus photographs.",
        "Despite these impressive results, significant obstacles remain before AI diagnostics can be widely deployed in clinical settings. Most AI systems are trained on datasets from specific populations and imaging equipment, raising concerns about performance when applied to patients with different demographic characteristics or when using different hardware. Additionally, the 'black box' nature of deep learning models\u2014where the reasoning behind a diagnosis is not transparent\u2014creates challenges for regulatory approval and physician trust.",
        "The integration of AI into clinical workflows also requires careful consideration of liability and professional responsibility. If an AI system makes an incorrect diagnosis, the question of whether the physician, the hospital, or the software developer bears responsibility remains legally unsettled. Some healthcare systems have adopted AI as a 'second reader' that flags potential concerns for physician review, rather than as an autonomous diagnostic tool, thereby preserving physician authority and responsibility.",
        "Looking forward, the most promising applications of AI in diagnostics may not be in replacing physicians but in augmenting their capabilities. AI systems that can rapidly screen large volumes of images, prioritize urgent cases, and reduce diagnostic backlogs could improve healthcare access, particularly in underserved regions where specialist physicians are scarce."
      ],
      "questions": [
        {
          "id": "rc-q-011",
          "passage_id": "rc-passage-004",
          "section": "verbal",
          "subsection": "reading_comprehension",
          "question_type": "primary_purpose",
          "topic": "technology",
          "difficulty": 3,
          "target_solving_time": 90,
          "evidence_paragraphs": [
            1,
            2,
            3,
            4
          ],
          "question_text": "The primary purpose of the passage is to",
          "options": [
            "argue that AI will inevitably replace radiologists within a decade",
            "examine the promise, obstacles, and practical considerations surrounding AI in medical diagnostics",
            "warn healthcare providers against adopting AI diagnostic tools",
            "compare the accuracy of AI systems with that of human physicians",
            "propose specific regulatory frameworks for AI medical devices"
          ],
          "correct_option_index": 1,
          "explanation": "The passage presents AI diagnostic capabilities (P1), deployment obstacles (P2), liability issues (P3), and future potential (P4). This balanced examination matches option B.",
          "option_explanations": [
            "Too extreme: The passage discusses augmentation, not replacement.",
            "Correct: Balanced coverage of promise, obstacles, and practical considerations.",
            "Too negative: The passage acknowledges significant promise alongside challenges.",
            "Too narrow: Accuracy comparison is one element of P1, not the primary purpose.",
            "Not done: The passage identifies regulatory challenges but doesn't propose frameworks."
          ],
          "trap_type": "too_broad",
          "skills": [
            "primary_purpose",
            "passage_structure"
          ],
          "passage_text": "The application of artificial intelligence to medical diagnostics has generated considerable excitement in the healthcare community. Deep learning algorithms, particularly convolutional neural networks, have demonstrated remarkable accuracy in identifying certain conditions from medical images. In some controlled studies, these systems have matched or exceeded the diagnostic accuracy of experienced radiologists in detecting specific cancers from mammograms and identifying diabetic retinopathy from fundus photographs.\n\nDespite these impressive results, significant obstacles remain before AI diagnostics can be widely deployed in clinical settings. Most AI systems are trained on datasets from specific populations and imaging equipment, raising concerns about performance when applied to patients with different demographic characteristics or when using different hardware. Additionally, the 'black box' nature of deep learning models\u2014where the reasoning behind a diagnosis is not transparent\u2014creates challenges for regulatory approval and physician trust.\n\nThe integration of AI into clinical workflows also requires careful consideration of liability and professional responsibility. If an AI system makes an incorrect diagnosis, the question of whether the physician, the hospital, or the software developer bears responsibility remains legally unsettled. Some healthcare systems have adopted AI as a 'second reader' that flags potential concerns for physician review, rather than as an autonomous diagnostic tool, thereby preserving physician authority and responsibility.\n\nLooking forward, the most promising applications of AI in diagnostics may not be in replacing physicians but in augmenting their capabilities. AI systems that can rapidly screen large volumes of images, prioritize urgent cases, and reduce diagnostic backlogs could improve healthcare access, particularly in underserved regions where specialist physicians are scarce.",
          "passage_title": "Artificial Intelligence in Medical Diagnostics",
          "passage_category": "technology",
          "passage_difficulty": 3,
          "estimated_reading_time": 180,
          "paragraphs": [
            "The application of artificial intelligence to medical diagnostics has generated considerable excitement in the healthcare community. Deep learning algorithms, particularly convolutional neural networks, have demonstrated remarkable accuracy in identifying certain conditions from medical images. In some controlled studies, these systems have matched or exceeded the diagnostic accuracy of experienced radiologists in detecting specific cancers from mammograms and identifying diabetic retinopathy from fundus photographs.",
            "Despite these impressive results, significant obstacles remain before AI diagnostics can be widely deployed in clinical settings. Most AI systems are trained on datasets from specific populations and imaging equipment, raising concerns about performance when applied to patients with different demographic characteristics or when using different hardware. Additionally, the 'black box' nature of deep learning models\u2014where the reasoning behind a diagnosis is not transparent\u2014creates challenges for regulatory approval and physician trust.",
            "The integration of AI into clinical workflows also requires careful consideration of liability and professional responsibility. If an AI system makes an incorrect diagnosis, the question of whether the physician, the hospital, or the software developer bears responsibility remains legally unsettled. Some healthcare systems have adopted AI as a 'second reader' that flags potential concerns for physician review, rather than as an autonomous diagnostic tool, thereby preserving physician authority and responsibility.",
            "Looking forward, the most promising applications of AI in diagnostics may not be in replacing physicians but in augmenting their capabilities. AI systems that can rapidly screen large volumes of images, prioritize urgent cases, and reduce diagnostic backlogs could improve healthcare access, particularly in underserved regions where specialist physicians are scarce."
          ]
        },
        {
          "id": "rc-q-012",
          "passage_id": "rc-passage-004",
          "section": "verbal",
          "subsection": "reading_comprehension",
          "question_type": "detail",
          "topic": "technology",
          "difficulty": 2,
          "target_solving_time": 75,
          "evidence_paragraphs": [
            3
          ],
          "question_text": "According to paragraph 3, some healthcare systems use AI as a 'second reader' in order to",
          "options": [
            "reduce the number of radiologists needed in the department",
            "ensure that the AI system receives adequate training data",
            "preserve physician authority and responsibility while benefiting from AI capabilities",
            "demonstrate to regulators that AI is safe for autonomous deployment",
            "lower the cost of medical malpractice insurance"
          ],
          "correct_option_index": 2,
          "explanation": "Paragraph 3 explains that the 'second reader' approach 'preserv[es] physician authority and responsibility,' using AI to flag concerns for physician review rather than making autonomous diagnoses.",
          "option_explanations": [
            "Not stated: Reducing radiologist numbers is not mentioned as the purpose.",
            "Not stated: Training data collection is not discussed in this context.",
            "Correct: Directly supported by the passage's explanation of the second-reader model.",
            "Not stated: Autonomous deployment is contrasted with, not supported by, this approach.",
            "Not stated: Insurance costs are not discussed."
          ],
          "trap_type": "out_of_scope",
          "skills": [
            "detail_retrieval",
            "purpose_identification"
          ],
          "passage_text": "The application of artificial intelligence to medical diagnostics has generated considerable excitement in the healthcare community. Deep learning algorithms, particularly convolutional neural networks, have demonstrated remarkable accuracy in identifying certain conditions from medical images. In some controlled studies, these systems have matched or exceeded the diagnostic accuracy of experienced radiologists in detecting specific cancers from mammograms and identifying diabetic retinopathy from fundus photographs.\n\nDespite these impressive results, significant obstacles remain before AI diagnostics can be widely deployed in clinical settings. Most AI systems are trained on datasets from specific populations and imaging equipment, raising concerns about performance when applied to patients with different demographic characteristics or when using different hardware. Additionally, the 'black box' nature of deep learning models\u2014where the reasoning behind a diagnosis is not transparent\u2014creates challenges for regulatory approval and physician trust.\n\nThe integration of AI into clinical workflows also requires careful consideration of liability and professional responsibility. If an AI system makes an incorrect diagnosis, the question of whether the physician, the hospital, or the software developer bears responsibility remains legally unsettled. Some healthcare systems have adopted AI as a 'second reader' that flags potential concerns for physician review, rather than as an autonomous diagnostic tool, thereby preserving physician authority and responsibility.\n\nLooking forward, the most promising applications of AI in diagnostics may not be in replacing physicians but in augmenting their capabilities. AI systems that can rapidly screen large volumes of images, prioritize urgent cases, and reduce diagnostic backlogs could improve healthcare access, particularly in underserved regions where specialist physicians are scarce.",
          "passage_title": "Artificial Intelligence in Medical Diagnostics",
          "passage_category": "technology",
          "passage_difficulty": 3,
          "estimated_reading_time": 180,
          "paragraphs": [
            "The application of artificial intelligence to medical diagnostics has generated considerable excitement in the healthcare community. Deep learning algorithms, particularly convolutional neural networks, have demonstrated remarkable accuracy in identifying certain conditions from medical images. In some controlled studies, these systems have matched or exceeded the diagnostic accuracy of experienced radiologists in detecting specific cancers from mammograms and identifying diabetic retinopathy from fundus photographs.",
            "Despite these impressive results, significant obstacles remain before AI diagnostics can be widely deployed in clinical settings. Most AI systems are trained on datasets from specific populations and imaging equipment, raising concerns about performance when applied to patients with different demographic characteristics or when using different hardware. Additionally, the 'black box' nature of deep learning models\u2014where the reasoning behind a diagnosis is not transparent\u2014creates challenges for regulatory approval and physician trust.",
            "The integration of AI into clinical workflows also requires careful consideration of liability and professional responsibility. If an AI system makes an incorrect diagnosis, the question of whether the physician, the hospital, or the software developer bears responsibility remains legally unsettled. Some healthcare systems have adopted AI as a 'second reader' that flags potential concerns for physician review, rather than as an autonomous diagnostic tool, thereby preserving physician authority and responsibility.",
            "Looking forward, the most promising applications of AI in diagnostics may not be in replacing physicians but in augmenting their capabilities. AI systems that can rapidly screen large volumes of images, prioritize urgent cases, and reduce diagnostic backlogs could improve healthcare access, particularly in underserved regions where specialist physicians are scarce."
          ]
        },
        {
          "id": "rc-q-013",
          "passage_id": "rc-passage-004",
          "section": "verbal",
          "subsection": "reading_comprehension",
          "question_type": "inference",
          "topic": "technology",
          "difficulty": 3,
          "target_solving_time": 90,
          "evidence_paragraphs": [
            4
          ],
          "question_text": "The author would most likely agree that AI diagnostic tools",
          "options": [
            "should not be used in any clinical setting until all regulatory questions are resolved",
            "are most valuable when used to complement physician expertise rather than replace it",
            "have already demonstrated sufficient reliability for autonomous clinical use",
            "are primarily beneficial for wealthy healthcare systems with advanced technology",
            "will be rendered obsolete by future medical breakthroughs"
          ],
          "correct_option_index": 1,
          "explanation": "Paragraph 4 states 'the most promising applications may not be in replacing physicians but in augmenting their capabilities,' directly supporting the view that AI should complement, not replace, physicians.",
          "option_explanations": [
            "Too restrictive: The author doesn't suggest waiting until all issues are resolved.",
            "Correct: Directly aligned with the passage's concluding perspective.",
            "Contradicted: P2 discusses obstacles to autonomous use.",
            "Contradicted: P4 specifically mentions benefits for 'underserved regions.'",
            "Unsupported: No such prediction is made."
          ],
          "trap_type": "distortion",
          "skills": [
            "inference",
            "authorial_perspective"
          ],
          "passage_text": "The application of artificial intelligence to medical diagnostics has generated considerable excitement in the healthcare community. Deep learning algorithms, particularly convolutional neural networks, have demonstrated remarkable accuracy in identifying certain conditions from medical images. In some controlled studies, these systems have matched or exceeded the diagnostic accuracy of experienced radiologists in detecting specific cancers from mammograms and identifying diabetic retinopathy from fundus photographs.\n\nDespite these impressive results, significant obstacles remain before AI diagnostics can be widely deployed in clinical settings. Most AI systems are trained on datasets from specific populations and imaging equipment, raising concerns about performance when applied to patients with different demographic characteristics or when using different hardware. Additionally, the 'black box' nature of deep learning models\u2014where the reasoning behind a diagnosis is not transparent\u2014creates challenges for regulatory approval and physician trust.\n\nThe integration of AI into clinical workflows also requires careful consideration of liability and professional responsibility. If an AI system makes an incorrect diagnosis, the question of whether the physician, the hospital, or the software developer bears responsibility remains legally unsettled. Some healthcare systems have adopted AI as a 'second reader' that flags potential concerns for physician review, rather than as an autonomous diagnostic tool, thereby preserving physician authority and responsibility.\n\nLooking forward, the most promising applications of AI in diagnostics may not be in replacing physicians but in augmenting their capabilities. AI systems that can rapidly screen large volumes of images, prioritize urgent cases, and reduce diagnostic backlogs could improve healthcare access, particularly in underserved regions where specialist physicians are scarce.",
          "passage_title": "Artificial Intelligence in Medical Diagnostics",
          "passage_category": "technology",
          "passage_difficulty": 3,
          "estimated_reading_time": 180,
          "paragraphs": [
            "The application of artificial intelligence to medical diagnostics has generated considerable excitement in the healthcare community. Deep learning algorithms, particularly convolutional neural networks, have demonstrated remarkable accuracy in identifying certain conditions from medical images. In some controlled studies, these systems have matched or exceeded the diagnostic accuracy of experienced radiologists in detecting specific cancers from mammograms and identifying diabetic retinopathy from fundus photographs.",
            "Despite these impressive results, significant obstacles remain before AI diagnostics can be widely deployed in clinical settings. Most AI systems are trained on datasets from specific populations and imaging equipment, raising concerns about performance when applied to patients with different demographic characteristics or when using different hardware. Additionally, the 'black box' nature of deep learning models\u2014where the reasoning behind a diagnosis is not transparent\u2014creates challenges for regulatory approval and physician trust.",
            "The integration of AI into clinical workflows also requires careful consideration of liability and professional responsibility. If an AI system makes an incorrect diagnosis, the question of whether the physician, the hospital, or the software developer bears responsibility remains legally unsettled. Some healthcare systems have adopted AI as a 'second reader' that flags potential concerns for physician review, rather than as an autonomous diagnostic tool, thereby preserving physician authority and responsibility.",
            "Looking forward, the most promising applications of AI in diagnostics may not be in replacing physicians but in augmenting their capabilities. AI systems that can rapidly screen large volumes of images, prioritize urgent cases, and reduce diagnostic backlogs could improve healthcare access, particularly in underserved regions where specialist physicians are scarce."
          ]
        }
      ]
    },
    {
      "id": "rc-passage-005",
      "title": "The Industrial Revolution and Labor Movements",
      "category": "history",
      "difficulty": 3,
      "estimated_reading_time": 180,
      "paragraphs": [
        "The Industrial Revolution, which began in Britain in the late eighteenth century, transformed economic production from agrarian and artisan-based systems to factory-centered manufacturing. This shift brought unprecedented economic growth but also created harsh working conditions: twelve- to sixteen-hour workdays, dangerous machinery, child labor, and wages barely sufficient for subsistence. Workers had little bargaining power as individuals, and early attempts at collective action were often met with legal prosecution under laws that treated labor organizing as criminal conspiracy.",
        "The emergence of organized labor movements in the nineteenth century represented a fundamental shift in the balance of power between workers and employers. Trade unions, initially formed among skilled craftsmen, gradually expanded to include unskilled factory workers. The legal landscape evolved as well: Britain's repeal of the Combination Acts in 1824 and the passage of the Trade Union Act in 1871 progressively legitimized labor organizing. In the United States, the American Federation of Labor, founded in 1886, pursued a strategy of 'pure and simple unionism' focused on wages, hours, and working conditions.",
        "Labor movements achieved significant legislative victories in the early twentieth century, including restrictions on child labor, the establishment of maximum working hours, workplace safety regulations, and the right to collective bargaining. These reforms fundamentally altered the social contract between capital and labor. However, historians debate whether these changes resulted primarily from organized labor's political pressure or from broader social and economic forces, including industrialists' recognition that better-treated workers were more productive.",
        "The legacy of industrial-era labor movements continues to shape contemporary debates about workers' rights. Issues such as minimum wage levels, workplace automation, and the gig economy echo the fundamental tensions between economic efficiency and worker welfare that defined the original labor struggles. Understanding this history provides essential context for evaluating modern proposals to reform labor markets."
      ],
      "questions": [
        {
          "id": "rc-q-014",
          "passage_id": "rc-passage-005",
          "section": "verbal",
          "subsection": "reading_comprehension",
          "question_type": "structure_of_passage",
          "topic": "history",
          "difficulty": 3,
          "target_solving_time": 90,
          "evidence_paragraphs": [
            1,
            2,
            3,
            4
          ],
          "question_text": "Which of the following best describes the organization of the passage?",
          "options": [
            "A problem is identified, a solution is proposed, and the solution's limitations are discussed.",
            "A historical context is established, key developments are traced chronologically, outcomes are assessed, and contemporary relevance is noted.",
            "Two competing theories are presented, evidence for each is evaluated, and one is endorsed.",
            "A phenomenon is described, its causes are analyzed, and future predictions are made.",
            "A controversial claim is stated, objections are raised, and the claim is modified."
          ],
          "correct_option_index": 1,
          "explanation": "P1 establishes context (Industrial Revolution conditions), P2 traces the development of labor movements, P3 assesses legislative outcomes and debates their causes, P4 connects to contemporary relevance. This is a chronological historical narrative.",
          "option_explanations": [
            "Doesn't match: No single solution is proposed.",
            "Correct: Matches the passage's chronological structure from context to contemporary relevance.",
            "Doesn't match: While a debate is mentioned in P3, the passage doesn't endorse one theory.",
            "Doesn't match: The passage discusses historical outcomes, not future predictions.",
            "Doesn't match: No single controversial claim drives the passage."
          ],
          "trap_type": "distortion",
          "skills": [
            "passage_structure",
            "organization"
          ],
          "passage_text": "The Industrial Revolution, which began in Britain in the late eighteenth century, transformed economic production from agrarian and artisan-based systems to factory-centered manufacturing. This shift brought unprecedented economic growth but also created harsh working conditions: twelve- to sixteen-hour workdays, dangerous machinery, child labor, and wages barely sufficient for subsistence. Workers had little bargaining power as individuals, and early attempts at collective action were often met with legal prosecution under laws that treated labor organizing as criminal conspiracy.\n\nThe emergence of organized labor movements in the nineteenth century represented a fundamental shift in the balance of power between workers and employers. Trade unions, initially formed among skilled craftsmen, gradually expanded to include unskilled factory workers. The legal landscape evolved as well: Britain's repeal of the Combination Acts in 1824 and the passage of the Trade Union Act in 1871 progressively legitimized labor organizing. In the United States, the American Federation of Labor, founded in 1886, pursued a strategy of 'pure and simple unionism' focused on wages, hours, and working conditions.\n\nLabor movements achieved significant legislative victories in the early twentieth century, including restrictions on child labor, the establishment of maximum working hours, workplace safety regulations, and the right to collective bargaining. These reforms fundamentally altered the social contract between capital and labor. However, historians debate whether these changes resulted primarily from organized labor's political pressure or from broader social and economic forces, including industrialists' recognition that better-treated workers were more productive.\n\nThe legacy of industrial-era labor movements continues to shape contemporary debates about workers' rights. Issues such as minimum wage levels, workplace automation, and the gig economy echo the fundamental tensions between economic efficiency and worker welfare that defined the original labor struggles. Understanding this history provides essential context for evaluating modern proposals to reform labor markets.",
          "passage_title": "The Industrial Revolution and Labor Movements",
          "passage_category": "history",
          "passage_difficulty": 3,
          "estimated_reading_time": 180,
          "paragraphs": [
            "The Industrial Revolution, which began in Britain in the late eighteenth century, transformed economic production from agrarian and artisan-based systems to factory-centered manufacturing. This shift brought unprecedented economic growth but also created harsh working conditions: twelve- to sixteen-hour workdays, dangerous machinery, child labor, and wages barely sufficient for subsistence. Workers had little bargaining power as individuals, and early attempts at collective action were often met with legal prosecution under laws that treated labor organizing as criminal conspiracy.",
            "The emergence of organized labor movements in the nineteenth century represented a fundamental shift in the balance of power between workers and employers. Trade unions, initially formed among skilled craftsmen, gradually expanded to include unskilled factory workers. The legal landscape evolved as well: Britain's repeal of the Combination Acts in 1824 and the passage of the Trade Union Act in 1871 progressively legitimized labor organizing. In the United States, the American Federation of Labor, founded in 1886, pursued a strategy of 'pure and simple unionism' focused on wages, hours, and working conditions.",
            "Labor movements achieved significant legislative victories in the early twentieth century, including restrictions on child labor, the establishment of maximum working hours, workplace safety regulations, and the right to collective bargaining. These reforms fundamentally altered the social contract between capital and labor. However, historians debate whether these changes resulted primarily from organized labor's political pressure or from broader social and economic forces, including industrialists' recognition that better-treated workers were more productive.",
            "The legacy of industrial-era labor movements continues to shape contemporary debates about workers' rights. Issues such as minimum wage levels, workplace automation, and the gig economy echo the fundamental tensions between economic efficiency and worker welfare that defined the original labor struggles. Understanding this history provides essential context for evaluating modern proposals to reform labor markets."
          ]
        },
        {
          "id": "rc-q-015",
          "passage_id": "rc-passage-005",
          "section": "verbal",
          "subsection": "reading_comprehension",
          "question_type": "relationship_between_ideas",
          "topic": "history",
          "difficulty": 4,
          "target_solving_time": 100,
          "evidence_paragraphs": [
            3
          ],
          "question_text": "The passage presents the debate described in paragraph 3 in order to",
          "options": [
            "argue that industrialists deserve more credit than unions for labor reforms",
            "suggest that the causes of labor reforms are complex and not attributable to a single factor",
            "demonstrate that organized labor was ultimately ineffective in achieving reforms",
            "criticize historians who downplay the role of labor unions",
            "propose a new theory of labor reform based on economic efficiency"
          ],
          "correct_option_index": 1,
          "explanation": "The passage presents the debate between labor pressure and broader forces as an open question, suggesting that the causes are complex and multifaceted rather than attributable to one factor.",
          "option_explanations": [
            "Too one-sided: The passage presents both perspectives without favoring either.",
            "Correct: Captures the nuanced presentation of multiple contributing factors.",
            "Contradicted: The passage credits labor movements with significant victories.",
            "Not the purpose: The passage presents the debate neutrally.",
            "Not done: No new theory is proposed."
          ],
          "trap_type": "too_narrow",
          "skills": [
            "relationship_analysis",
            "authorial_intent"
          ],
          "passage_text": "The Industrial Revolution, which began in Britain in the late eighteenth century, transformed economic production from agrarian and artisan-based systems to factory-centered manufacturing. This shift brought unprecedented economic growth but also created harsh working conditions: twelve- to sixteen-hour workdays, dangerous machinery, child labor, and wages barely sufficient for subsistence. Workers had little bargaining power as individuals, and early attempts at collective action were often met with legal prosecution under laws that treated labor organizing as criminal conspiracy.\n\nThe emergence of organized labor movements in the nineteenth century represented a fundamental shift in the balance of power between workers and employers. Trade unions, initially formed among skilled craftsmen, gradually expanded to include unskilled factory workers. The legal landscape evolved as well: Britain's repeal of the Combination Acts in 1824 and the passage of the Trade Union Act in 1871 progressively legitimized labor organizing. In the United States, the American Federation of Labor, founded in 1886, pursued a strategy of 'pure and simple unionism' focused on wages, hours, and working conditions.\n\nLabor movements achieved significant legislative victories in the early twentieth century, including restrictions on child labor, the establishment of maximum working hours, workplace safety regulations, and the right to collective bargaining. These reforms fundamentally altered the social contract between capital and labor. However, historians debate whether these changes resulted primarily from organized labor's political pressure or from broader social and economic forces, including industrialists' recognition that better-treated workers were more productive.\n\nThe legacy of industrial-era labor movements continues to shape contemporary debates about workers' rights. Issues such as minimum wage levels, workplace automation, and the gig economy echo the fundamental tensions between economic efficiency and worker welfare that defined the original labor struggles. Understanding this history provides essential context for evaluating modern proposals to reform labor markets.",
          "passage_title": "The Industrial Revolution and Labor Movements",
          "passage_category": "history",
          "passage_difficulty": 3,
          "estimated_reading_time": 180,
          "paragraphs": [
            "The Industrial Revolution, which began in Britain in the late eighteenth century, transformed economic production from agrarian and artisan-based systems to factory-centered manufacturing. This shift brought unprecedented economic growth but also created harsh working conditions: twelve- to sixteen-hour workdays, dangerous machinery, child labor, and wages barely sufficient for subsistence. Workers had little bargaining power as individuals, and early attempts at collective action were often met with legal prosecution under laws that treated labor organizing as criminal conspiracy.",
            "The emergence of organized labor movements in the nineteenth century represented a fundamental shift in the balance of power between workers and employers. Trade unions, initially formed among skilled craftsmen, gradually expanded to include unskilled factory workers. The legal landscape evolved as well: Britain's repeal of the Combination Acts in 1824 and the passage of the Trade Union Act in 1871 progressively legitimized labor organizing. In the United States, the American Federation of Labor, founded in 1886, pursued a strategy of 'pure and simple unionism' focused on wages, hours, and working conditions.",
            "Labor movements achieved significant legislative victories in the early twentieth century, including restrictions on child labor, the establishment of maximum working hours, workplace safety regulations, and the right to collective bargaining. These reforms fundamentally altered the social contract between capital and labor. However, historians debate whether these changes resulted primarily from organized labor's political pressure or from broader social and economic forces, including industrialists' recognition that better-treated workers were more productive.",
            "The legacy of industrial-era labor movements continues to shape contemporary debates about workers' rights. Issues such as minimum wage levels, workplace automation, and the gig economy echo the fundamental tensions between economic efficiency and worker welfare that defined the original labor struggles. Understanding this history provides essential context for evaluating modern proposals to reform labor markets."
          ]
        },
        {
          "id": "rc-q-016",
          "passage_id": "rc-passage-005",
          "section": "verbal",
          "subsection": "reading_comprehension",
          "question_type": "application_of_idea",
          "topic": "history",
          "difficulty": 4,
          "target_solving_time": 100,
          "evidence_paragraphs": [
            4
          ],
          "question_text": "Based on the passage, the author would most likely view a contemporary debate about gig economy workers' rights as",
          "options": [
            "irrelevant to the historical labor struggles described in the passage",
            "a modern manifestation of the enduring tension between economic efficiency and worker welfare",
            "evidence that labor movements have completely failed in their mission",
            "a problem that can be solved solely through market forces",
            "a temporary issue that will resolve itself as technology improves"
          ],
          "correct_option_index": 1,
          "explanation": "Paragraph 4 explicitly identifies 'the gig economy' as echoing 'the fundamental tensions between economic efficiency and worker welfare that defined the original labor struggles,' directly supporting option B.",
          "option_explanations": [
            "Contradicted: P4 explicitly connects modern issues to historical struggles.",
            "Correct: Directly supported by P4's identification of contemporary echoes.",
            "Too extreme: The passage notes significant achievements, not complete failure.",
            "Not supported: The passage does not suggest market forces alone are sufficient.",
            "Not supported: No such optimistic prediction is made."
          ],
          "trap_type": "out_of_scope",
          "skills": [
            "application",
            "historical_analogy"
          ],
          "passage_text": "The Industrial Revolution, which began in Britain in the late eighteenth century, transformed economic production from agrarian and artisan-based systems to factory-centered manufacturing. This shift brought unprecedented economic growth but also created harsh working conditions: twelve- to sixteen-hour workdays, dangerous machinery, child labor, and wages barely sufficient for subsistence. Workers had little bargaining power as individuals, and early attempts at collective action were often met with legal prosecution under laws that treated labor organizing as criminal conspiracy.\n\nThe emergence of organized labor movements in the nineteenth century represented a fundamental shift in the balance of power between workers and employers. Trade unions, initially formed among skilled craftsmen, gradually expanded to include unskilled factory workers. The legal landscape evolved as well: Britain's repeal of the Combination Acts in 1824 and the passage of the Trade Union Act in 1871 progressively legitimized labor organizing. In the United States, the American Federation of Labor, founded in 1886, pursued a strategy of 'pure and simple unionism' focused on wages, hours, and working conditions.\n\nLabor movements achieved significant legislative victories in the early twentieth century, including restrictions on child labor, the establishment of maximum working hours, workplace safety regulations, and the right to collective bargaining. These reforms fundamentally altered the social contract between capital and labor. However, historians debate whether these changes resulted primarily from organized labor's political pressure or from broader social and economic forces, including industrialists' recognition that better-treated workers were more productive.\n\nThe legacy of industrial-era labor movements continues to shape contemporary debates about workers' rights. Issues such as minimum wage levels, workplace automation, and the gig economy echo the fundamental tensions between economic efficiency and worker welfare that defined the original labor struggles. Understanding this history provides essential context for evaluating modern proposals to reform labor markets.",
          "passage_title": "The Industrial Revolution and Labor Movements",
          "passage_category": "history",
          "passage_difficulty": 3,
          "estimated_reading_time": 180,
          "paragraphs": [
            "The Industrial Revolution, which began in Britain in the late eighteenth century, transformed economic production from agrarian and artisan-based systems to factory-centered manufacturing. This shift brought unprecedented economic growth but also created harsh working conditions: twelve- to sixteen-hour workdays, dangerous machinery, child labor, and wages barely sufficient for subsistence. Workers had little bargaining power as individuals, and early attempts at collective action were often met with legal prosecution under laws that treated labor organizing as criminal conspiracy.",
            "The emergence of organized labor movements in the nineteenth century represented a fundamental shift in the balance of power between workers and employers. Trade unions, initially formed among skilled craftsmen, gradually expanded to include unskilled factory workers. The legal landscape evolved as well: Britain's repeal of the Combination Acts in 1824 and the passage of the Trade Union Act in 1871 progressively legitimized labor organizing. In the United States, the American Federation of Labor, founded in 1886, pursued a strategy of 'pure and simple unionism' focused on wages, hours, and working conditions.",
            "Labor movements achieved significant legislative victories in the early twentieth century, including restrictions on child labor, the establishment of maximum working hours, workplace safety regulations, and the right to collective bargaining. These reforms fundamentally altered the social contract between capital and labor. However, historians debate whether these changes resulted primarily from organized labor's political pressure or from broader social and economic forces, including industrialists' recognition that better-treated workers were more productive.",
            "The legacy of industrial-era labor movements continues to shape contemporary debates about workers' rights. Issues such as minimum wage levels, workplace automation, and the gig economy echo the fundamental tensions between economic efficiency and worker welfare that defined the original labor struggles. Understanding this history provides essential context for evaluating modern proposals to reform labor markets."
          ]
        }
      ]
    },
    {
      "id": "rc-passage-006",
      "title": "Behavioral Nudges and Public Policy Design",
      "category": "social_science",
      "difficulty": 3,
      "estimated_reading_time": 180,
      "paragraphs": [
        "Traditional economic policy assumes that individuals make rational decisions when provided with accurate information. Under this framework, the role of government is to ensure transparency\u2014clear labeling, accessible data, fair markets\u2014and then step back, trusting citizens to act in their own best interest. Behavioral economics, drawing on decades of psychological research, challenges this assumption by documenting systematic cognitive biases that cause people to make choices inconsistent with their own stated preferences.",
        "The concept of 'nudging,' popularized by Richard Thaler and Cass Sunstein, proposes that policy designers can improve outcomes by structuring choice environments to account for these biases without restricting options. The most widely cited example is automatic enrollment in retirement savings plans: when employees must opt out rather than opt in, participation rates increase dramatically, from roughly 50 percent to over 90 percent in many organizations. The choice to save remains entirely voluntary, but the default option is changed to align with what most employees say they want.",
        "Critics of nudging raise both practical and philosophical concerns. On the practical side, nudges that work in laboratory settings may produce smaller effects in complex real-world environments. On the philosophical side, some argue that nudging represents a form of paternalism that undermines individual autonomy, even when the intent is benevolent. Who determines what constitutes a 'better' choice, and by what criteria? These questions become particularly contentious when governments apply nudging to sensitive domains such as healthcare decisions or dietary choices.",
        "Despite these critiques, nudge-based policies have proliferated globally. The UK's Behavioural Insights Team, established in 2010, has implemented nudges across tax compliance, energy conservation, and public health. The approach's appeal lies in its cost-effectiveness: nudges typically require minimal expenditure compared to traditional regulatory or incentive-based interventions, while producing measurable behavioral change."
      ],
      "questions": [
        {
          "id": "rc-q-017",
          "passage_id": "rc-passage-006",
          "section": "verbal",
          "subsection": "reading_comprehension",
          "question_type": "primary_purpose",
          "topic": "social_science",
          "difficulty": 3,
          "target_solving_time": 90,
          "evidence_paragraphs": [
            1,
            2,
            3,
            4
          ],
          "question_text": "The primary purpose of the passage is to",
          "options": [
            "argue that nudging is the most effective public policy tool available to governments",
            "provide an overview of nudge-based policy design, including its theoretical basis, applications, criticisms, and growing adoption",
            "contrast behavioral economics with classical economic theory",
            "demonstrate that automatic enrollment in retirement plans is the best nudge ever designed",
            "warn governments against the unintended consequences of nudge policies"
          ],
          "correct_option_index": 1,
          "explanation": "The passage provides a balanced overview: theoretical background (P1-P2), criticisms (P3), and global adoption (P4). It neither advocates exclusively nor warns against nudging.",
          "option_explanations": [
            "Too one-sided: The passage presents criticisms as well.",
            "Correct: Captures the balanced, comprehensive overview.",
            "Too narrow: The contrast is context, not the primary purpose.",
            "Too narrow: Retirement enrollment is one example, not the focus.",
            "Too negative: The passage also discusses benefits and adoption."
          ],
          "trap_type": "too_narrow",
          "skills": [
            "primary_purpose",
            "balanced_assessment"
          ],
          "passage_text": "Traditional economic policy assumes that individuals make rational decisions when provided with accurate information. Under this framework, the role of government is to ensure transparency\u2014clear labeling, accessible data, fair markets\u2014and then step back, trusting citizens to act in their own best interest. Behavioral economics, drawing on decades of psychological research, challenges this assumption by documenting systematic cognitive biases that cause people to make choices inconsistent with their own stated preferences.\n\nThe concept of 'nudging,' popularized by Richard Thaler and Cass Sunstein, proposes that policy designers can improve outcomes by structuring choice environments to account for these biases without restricting options. The most widely cited example is automatic enrollment in retirement savings plans: when employees must opt out rather than opt in, participation rates increase dramatically, from roughly 50 percent to over 90 percent in many organizations. The choice to save remains entirely voluntary, but the default option is changed to align with what most employees say they want.\n\nCritics of nudging raise both practical and philosophical concerns. On the practical side, nudges that work in laboratory settings may produce smaller effects in complex real-world environments. On the philosophical side, some argue that nudging represents a form of paternalism that undermines individual autonomy, even when the intent is benevolent. Who determines what constitutes a 'better' choice, and by what criteria? These questions become particularly contentious when governments apply nudging to sensitive domains such as healthcare decisions or dietary choices.\n\nDespite these critiques, nudge-based policies have proliferated globally. The UK's Behavioural Insights Team, established in 2010, has implemented nudges across tax compliance, energy conservation, and public health. The approach's appeal lies in its cost-effectiveness: nudges typically require minimal expenditure compared to traditional regulatory or incentive-based interventions, while producing measurable behavioral change.",
          "passage_title": "Behavioral Nudges and Public Policy Design",
          "passage_category": "social_science",
          "passage_difficulty": 3,
          "estimated_reading_time": 180,
          "paragraphs": [
            "Traditional economic policy assumes that individuals make rational decisions when provided with accurate information. Under this framework, the role of government is to ensure transparency\u2014clear labeling, accessible data, fair markets\u2014and then step back, trusting citizens to act in their own best interest. Behavioral economics, drawing on decades of psychological research, challenges this assumption by documenting systematic cognitive biases that cause people to make choices inconsistent with their own stated preferences.",
            "The concept of 'nudging,' popularized by Richard Thaler and Cass Sunstein, proposes that policy designers can improve outcomes by structuring choice environments to account for these biases without restricting options. The most widely cited example is automatic enrollment in retirement savings plans: when employees must opt out rather than opt in, participation rates increase dramatically, from roughly 50 percent to over 90 percent in many organizations. The choice to save remains entirely voluntary, but the default option is changed to align with what most employees say they want.",
            "Critics of nudging raise both practical and philosophical concerns. On the practical side, nudges that work in laboratory settings may produce smaller effects in complex real-world environments. On the philosophical side, some argue that nudging represents a form of paternalism that undermines individual autonomy, even when the intent is benevolent. Who determines what constitutes a 'better' choice, and by what criteria? These questions become particularly contentious when governments apply nudging to sensitive domains such as healthcare decisions or dietary choices.",
            "Despite these critiques, nudge-based policies have proliferated globally. The UK's Behavioural Insights Team, established in 2010, has implemented nudges across tax compliance, energy conservation, and public health. The approach's appeal lies in its cost-effectiveness: nudges typically require minimal expenditure compared to traditional regulatory or incentive-based interventions, while producing measurable behavioral change."
          ]
        },
        {
          "id": "rc-q-018",
          "passage_id": "rc-passage-006",
          "section": "verbal",
          "subsection": "reading_comprehension",
          "question_type": "detail",
          "topic": "social_science",
          "difficulty": 2,
          "target_solving_time": 75,
          "evidence_paragraphs": [
            2
          ],
          "question_text": "According to the passage, automatic enrollment in retirement savings plans is an effective nudge because",
          "options": [
            "it forces employees to save a minimum percentage of their salary",
            "it provides financial incentives for retirement saving",
            "it changes the default option to align with what most employees say they want",
            "it restricts employees' ability to withdraw their savings early",
            "it requires employers to match employee contributions"
          ],
          "correct_option_index": 2,
          "explanation": "P2 states that 'the default option is changed to align with what most employees say they want' while keeping the choice 'entirely voluntary.'",
          "option_explanations": [
            "Contradicted: The passage says the choice remains voluntary.",
            "Not stated: Financial incentives are not mentioned.",
            "Correct: Directly stated in paragraph 2.",
            "Not stated: Withdrawal restrictions are not discussed.",
            "Not stated: Employer matching is not mentioned."
          ],
          "trap_type": "distortion",
          "skills": [
            "detail_retrieval"
          ],
          "passage_text": "Traditional economic policy assumes that individuals make rational decisions when provided with accurate information. Under this framework, the role of government is to ensure transparency\u2014clear labeling, accessible data, fair markets\u2014and then step back, trusting citizens to act in their own best interest. Behavioral economics, drawing on decades of psychological research, challenges this assumption by documenting systematic cognitive biases that cause people to make choices inconsistent with their own stated preferences.\n\nThe concept of 'nudging,' popularized by Richard Thaler and Cass Sunstein, proposes that policy designers can improve outcomes by structuring choice environments to account for these biases without restricting options. The most widely cited example is automatic enrollment in retirement savings plans: when employees must opt out rather than opt in, participation rates increase dramatically, from roughly 50 percent to over 90 percent in many organizations. The choice to save remains entirely voluntary, but the default option is changed to align with what most employees say they want.\n\nCritics of nudging raise both practical and philosophical concerns. On the practical side, nudges that work in laboratory settings may produce smaller effects in complex real-world environments. On the philosophical side, some argue that nudging represents a form of paternalism that undermines individual autonomy, even when the intent is benevolent. Who determines what constitutes a 'better' choice, and by what criteria? These questions become particularly contentious when governments apply nudging to sensitive domains such as healthcare decisions or dietary choices.\n\nDespite these critiques, nudge-based policies have proliferated globally. The UK's Behavioural Insights Team, established in 2010, has implemented nudges across tax compliance, energy conservation, and public health. The approach's appeal lies in its cost-effectiveness: nudges typically require minimal expenditure compared to traditional regulatory or incentive-based interventions, while producing measurable behavioral change.",
          "passage_title": "Behavioral Nudges and Public Policy Design",
          "passage_category": "social_science",
          "passage_difficulty": 3,
          "estimated_reading_time": 180,
          "paragraphs": [
            "Traditional economic policy assumes that individuals make rational decisions when provided with accurate information. Under this framework, the role of government is to ensure transparency\u2014clear labeling, accessible data, fair markets\u2014and then step back, trusting citizens to act in their own best interest. Behavioral economics, drawing on decades of psychological research, challenges this assumption by documenting systematic cognitive biases that cause people to make choices inconsistent with their own stated preferences.",
            "The concept of 'nudging,' popularized by Richard Thaler and Cass Sunstein, proposes that policy designers can improve outcomes by structuring choice environments to account for these biases without restricting options. The most widely cited example is automatic enrollment in retirement savings plans: when employees must opt out rather than opt in, participation rates increase dramatically, from roughly 50 percent to over 90 percent in many organizations. The choice to save remains entirely voluntary, but the default option is changed to align with what most employees say they want.",
            "Critics of nudging raise both practical and philosophical concerns. On the practical side, nudges that work in laboratory settings may produce smaller effects in complex real-world environments. On the philosophical side, some argue that nudging represents a form of paternalism that undermines individual autonomy, even when the intent is benevolent. Who determines what constitutes a 'better' choice, and by what criteria? These questions become particularly contentious when governments apply nudging to sensitive domains such as healthcare decisions or dietary choices.",
            "Despite these critiques, nudge-based policies have proliferated globally. The UK's Behavioural Insights Team, established in 2010, has implemented nudges across tax compliance, energy conservation, and public health. The approach's appeal lies in its cost-effectiveness: nudges typically require minimal expenditure compared to traditional regulatory or incentive-based interventions, while producing measurable behavioral change."
          ]
        }
      ]
    },
    {
      "id": "rc-passage-007",
      "title": "Ocean Acidification and Marine Ecosystems",
      "category": "environment",
      "difficulty": 4,
      "estimated_reading_time": 190,
      "paragraphs": [
        "The world's oceans absorb approximately 30 percent of the carbon dioxide released into the atmosphere by human activities. While this absorption has moderated the pace of atmospheric warming, it has come at a significant cost to marine chemistry. When carbon dioxide dissolves in seawater, it forms carbonic acid, which releases hydrogen ions that lower the water's pH. Since the beginning of the industrial era, ocean surface pH has decreased by approximately 0.1 units, representing a 26 percent increase in acidity.",
        "This shift in ocean chemistry poses a direct threat to marine organisms that build shells or skeletons from calcium carbonate, including corals, mollusks, and certain plankton species. As acidity increases, the concentration of carbonate ions\u2014essential building blocks for these structures\u2014decreases, making it progressively more difficult and energetically costly for organisms to form and maintain their protective shells. Laboratory experiments have demonstrated that many calcifying species exhibit reduced growth rates, thinner shells, and higher mortality when exposed to projected future pH levels.",
        "The ecological implications extend far beyond calcifying organisms. Coral reefs, which support an estimated 25 percent of all marine species despite covering less than 1 percent of the ocean floor, are particularly vulnerable. Reef degradation threatens the complex food webs and biodiversity hotspots that depend on coral structures. Pteropods, tiny swimming snails that form a critical component of polar food chains, have already shown signs of shell dissolution in Antarctic waters where acidification is most advanced.",
        "Addressing ocean acidification ultimately requires reducing atmospheric carbon dioxide concentrations, as the ocean's chemistry will continue to shift as long as excess CO2 persists in the atmosphere. Some researchers have proposed local interventions, such as adding alkaline minerals to coastal waters, but the scale of the ocean makes such approaches impractical as a global solution. International agreements to limit carbon emissions remain the most scientifically credible path to slowing ocean acidification, though the ocean's response to reduced emissions will be measured in decades, not years."
      ],
      "questions": [
        {
          "id": "rc-q-019",
          "passage_id": "rc-passage-007",
          "section": "verbal",
          "subsection": "reading_comprehension",
          "question_type": "main_idea",
          "topic": "environment",
          "difficulty": 3,
          "target_solving_time": 90,
          "evidence_paragraphs": [
            1,
            2,
            3,
            4
          ],
          "question_text": "Which of the following best expresses the main idea of the passage?",
          "options": [
            "Ocean acidification is caused by industrial pollution of waterways.",
            "Human CO2 emissions are causing ocean acidification that threatens marine ecosystems, and meaningful solutions require global emissions reductions.",
            "Coral reefs will be completely destroyed within the next decade.",
            "Local interventions such as adding alkaline minerals are the best solution to ocean acidification.",
            "The ocean's ability to absorb carbon dioxide will eliminate the threat of atmospheric warming."
          ],
          "correct_option_index": 1,
          "explanation": "The passage explains the mechanism (P1), impacts (P2-P3), and solutions (P4) of ocean acidification, emphasizing that global CO2 reduction is the credible path forward.",
          "option_explanations": [
            "Inaccurate: The cause is atmospheric CO2 absorption, not direct pollution.",
            "Correct: Captures the cause, threat, and solution arc of the passage.",
            "Too extreme and unsupported: No timeline for complete destruction is given.",
            "Contradicted: P4 says such approaches are 'impractical as a global solution.'",
            "Contradicted: P1 notes that absorption comes 'at a significant cost' to marine chemistry."
          ],
          "trap_type": "distortion",
          "skills": [
            "main_idea",
            "synthesis"
          ],
          "passage_text": "The world's oceans absorb approximately 30 percent of the carbon dioxide released into the atmosphere by human activities. While this absorption has moderated the pace of atmospheric warming, it has come at a significant cost to marine chemistry. When carbon dioxide dissolves in seawater, it forms carbonic acid, which releases hydrogen ions that lower the water's pH. Since the beginning of the industrial era, ocean surface pH has decreased by approximately 0.1 units, representing a 26 percent increase in acidity.\n\nThis shift in ocean chemistry poses a direct threat to marine organisms that build shells or skeletons from calcium carbonate, including corals, mollusks, and certain plankton species. As acidity increases, the concentration of carbonate ions\u2014essential building blocks for these structures\u2014decreases, making it progressively more difficult and energetically costly for organisms to form and maintain their protective shells. Laboratory experiments have demonstrated that many calcifying species exhibit reduced growth rates, thinner shells, and higher mortality when exposed to projected future pH levels.\n\nThe ecological implications extend far beyond calcifying organisms. Coral reefs, which support an estimated 25 percent of all marine species despite covering less than 1 percent of the ocean floor, are particularly vulnerable. Reef degradation threatens the complex food webs and biodiversity hotspots that depend on coral structures. Pteropods, tiny swimming snails that form a critical component of polar food chains, have already shown signs of shell dissolution in Antarctic waters where acidification is most advanced.\n\nAddressing ocean acidification ultimately requires reducing atmospheric carbon dioxide concentrations, as the ocean's chemistry will continue to shift as long as excess CO2 persists in the atmosphere. Some researchers have proposed local interventions, such as adding alkaline minerals to coastal waters, but the scale of the ocean makes such approaches impractical as a global solution. International agreements to limit carbon emissions remain the most scientifically credible path to slowing ocean acidification, though the ocean's response to reduced emissions will be measured in decades, not years.",
          "passage_title": "Ocean Acidification and Marine Ecosystems",
          "passage_category": "environment",
          "passage_difficulty": 4,
          "estimated_reading_time": 190,
          "paragraphs": [
            "The world's oceans absorb approximately 30 percent of the carbon dioxide released into the atmosphere by human activities. While this absorption has moderated the pace of atmospheric warming, it has come at a significant cost to marine chemistry. When carbon dioxide dissolves in seawater, it forms carbonic acid, which releases hydrogen ions that lower the water's pH. Since the beginning of the industrial era, ocean surface pH has decreased by approximately 0.1 units, representing a 26 percent increase in acidity.",
            "This shift in ocean chemistry poses a direct threat to marine organisms that build shells or skeletons from calcium carbonate, including corals, mollusks, and certain plankton species. As acidity increases, the concentration of carbonate ions\u2014essential building blocks for these structures\u2014decreases, making it progressively more difficult and energetically costly for organisms to form and maintain their protective shells. Laboratory experiments have demonstrated that many calcifying species exhibit reduced growth rates, thinner shells, and higher mortality when exposed to projected future pH levels.",
            "The ecological implications extend far beyond calcifying organisms. Coral reefs, which support an estimated 25 percent of all marine species despite covering less than 1 percent of the ocean floor, are particularly vulnerable. Reef degradation threatens the complex food webs and biodiversity hotspots that depend on coral structures. Pteropods, tiny swimming snails that form a critical component of polar food chains, have already shown signs of shell dissolution in Antarctic waters where acidification is most advanced.",
            "Addressing ocean acidification ultimately requires reducing atmospheric carbon dioxide concentrations, as the ocean's chemistry will continue to shift as long as excess CO2 persists in the atmosphere. Some researchers have proposed local interventions, such as adding alkaline minerals to coastal waters, but the scale of the ocean makes such approaches impractical as a global solution. International agreements to limit carbon emissions remain the most scientifically credible path to slowing ocean acidification, though the ocean's response to reduced emissions will be measured in decades, not years."
          ]
        },
        {
          "id": "rc-q-020",
          "passage_id": "rc-passage-007",
          "section": "verbal",
          "subsection": "reading_comprehension",
          "question_type": "strengthen_weaken",
          "topic": "environment",
          "difficulty": 4,
          "target_solving_time": 100,
          "evidence_paragraphs": [
            2,
            3
          ],
          "question_text": "Which of the following, if true, would most strengthen the passage's claim about the threat to marine ecosystems?",
          "options": [
            "Some fish species have shown the ability to adapt to slightly lower pH levels over multiple generations.",
            "A recent study found that reduced carbonate ion availability has already caused a measurable decline in commercial shellfish populations along several coastlines.",
            "Ocean temperatures have also increased significantly over the past century.",
            "The tourism industry generates significant revenue from coral reef destinations.",
            "Some species of algae actually benefit from increased carbon dioxide levels."
          ],
          "correct_option_index": 1,
          "explanation": "The passage discusses threats to calcifying organisms. Real-world evidence of actual shellfish population decline directly strengthens the claim that acidification threatens marine ecosystems.",
          "option_explanations": [
            "Weakens: Fish adaptation would reduce the severity of the threat.",
            "Correct: Direct real-world evidence supporting the threat claim.",
            "Relevant but doesn't specifically address acidification's impact on marine ecosystems.",
            "Irrelevant: Tourism revenue doesn't strengthen the ecological threat claim.",
            "Weakens: Algae benefits would partially offset the threat."
          ],
          "trap_type": "out_of_scope",
          "skills": [
            "strengthen_weaken",
            "evidence_evaluation"
          ],
          "passage_text": "The world's oceans absorb approximately 30 percent of the carbon dioxide released into the atmosphere by human activities. While this absorption has moderated the pace of atmospheric warming, it has come at a significant cost to marine chemistry. When carbon dioxide dissolves in seawater, it forms carbonic acid, which releases hydrogen ions that lower the water's pH. Since the beginning of the industrial era, ocean surface pH has decreased by approximately 0.1 units, representing a 26 percent increase in acidity.\n\nThis shift in ocean chemistry poses a direct threat to marine organisms that build shells or skeletons from calcium carbonate, including corals, mollusks, and certain plankton species. As acidity increases, the concentration of carbonate ions\u2014essential building blocks for these structures\u2014decreases, making it progressively more difficult and energetically costly for organisms to form and maintain their protective shells. Laboratory experiments have demonstrated that many calcifying species exhibit reduced growth rates, thinner shells, and higher mortality when exposed to projected future pH levels.\n\nThe ecological implications extend far beyond calcifying organisms. Coral reefs, which support an estimated 25 percent of all marine species despite covering less than 1 percent of the ocean floor, are particularly vulnerable. Reef degradation threatens the complex food webs and biodiversity hotspots that depend on coral structures. Pteropods, tiny swimming snails that form a critical component of polar food chains, have already shown signs of shell dissolution in Antarctic waters where acidification is most advanced.\n\nAddressing ocean acidification ultimately requires reducing atmospheric carbon dioxide concentrations, as the ocean's chemistry will continue to shift as long as excess CO2 persists in the atmosphere. Some researchers have proposed local interventions, such as adding alkaline minerals to coastal waters, but the scale of the ocean makes such approaches impractical as a global solution. International agreements to limit carbon emissions remain the most scientifically credible path to slowing ocean acidification, though the ocean's response to reduced emissions will be measured in decades, not years.",
          "passage_title": "Ocean Acidification and Marine Ecosystems",
          "passage_category": "environment",
          "passage_difficulty": 4,
          "estimated_reading_time": 190,
          "paragraphs": [
            "The world's oceans absorb approximately 30 percent of the carbon dioxide released into the atmosphere by human activities. While this absorption has moderated the pace of atmospheric warming, it has come at a significant cost to marine chemistry. When carbon dioxide dissolves in seawater, it forms carbonic acid, which releases hydrogen ions that lower the water's pH. Since the beginning of the industrial era, ocean surface pH has decreased by approximately 0.1 units, representing a 26 percent increase in acidity.",
            "This shift in ocean chemistry poses a direct threat to marine organisms that build shells or skeletons from calcium carbonate, including corals, mollusks, and certain plankton species. As acidity increases, the concentration of carbonate ions\u2014essential building blocks for these structures\u2014decreases, making it progressively more difficult and energetically costly for organisms to form and maintain their protective shells. Laboratory experiments have demonstrated that many calcifying species exhibit reduced growth rates, thinner shells, and higher mortality when exposed to projected future pH levels.",
            "The ecological implications extend far beyond calcifying organisms. Coral reefs, which support an estimated 25 percent of all marine species despite covering less than 1 percent of the ocean floor, are particularly vulnerable. Reef degradation threatens the complex food webs and biodiversity hotspots that depend on coral structures. Pteropods, tiny swimming snails that form a critical component of polar food chains, have already shown signs of shell dissolution in Antarctic waters where acidification is most advanced.",
            "Addressing ocean acidification ultimately requires reducing atmospheric carbon dioxide concentrations, as the ocean's chemistry will continue to shift as long as excess CO2 persists in the atmosphere. Some researchers have proposed local interventions, such as adding alkaline minerals to coastal waters, but the scale of the ocean makes such approaches impractical as a global solution. International agreements to limit carbon emissions remain the most scientifically credible path to slowing ocean acidification, though the ocean's response to reduced emissions will be measured in decades, not years."
          ]
        },
        {
          "id": "rc-q-021",
          "passage_id": "rc-passage-007",
          "section": "verbal",
          "subsection": "reading_comprehension",
          "question_type": "detail",
          "topic": "environment",
          "difficulty": 2,
          "target_solving_time": 75,
          "evidence_paragraphs": [
            1
          ],
          "question_text": "According to the passage, since the industrial era, ocean surface pH has",
          "options": [
            "increased by 0.1 units",
            "decreased by 0.1 units, representing a 26 percent increase in acidity",
            "remained essentially stable despite increased CO2 emissions",
            "decreased by 26 percent",
            "fluctuated unpredictably due to ocean currents"
          ],
          "correct_option_index": 1,
          "explanation": "Paragraph 1 directly states: 'ocean surface pH has decreased by approximately 0.1 units, representing a 26 percent increase in acidity.'",
          "option_explanations": [
            "Reversed: pH decreased, not increased.",
            "Correct: Directly stated in paragraph 1.",
            "Contradicted: Significant change is documented.",
            "Distortion: pH decreased by 0.1 units; acidity increased 26%.",
            "Not stated: Unpredictable fluctuation is not discussed."
          ],
          "trap_type": "distortion",
          "skills": [
            "detail_retrieval"
          ],
          "passage_text": "The world's oceans absorb approximately 30 percent of the carbon dioxide released into the atmosphere by human activities. While this absorption has moderated the pace of atmospheric warming, it has come at a significant cost to marine chemistry. When carbon dioxide dissolves in seawater, it forms carbonic acid, which releases hydrogen ions that lower the water's pH. Since the beginning of the industrial era, ocean surface pH has decreased by approximately 0.1 units, representing a 26 percent increase in acidity.\n\nThis shift in ocean chemistry poses a direct threat to marine organisms that build shells or skeletons from calcium carbonate, including corals, mollusks, and certain plankton species. As acidity increases, the concentration of carbonate ions\u2014essential building blocks for these structures\u2014decreases, making it progressively more difficult and energetically costly for organisms to form and maintain their protective shells. Laboratory experiments have demonstrated that many calcifying species exhibit reduced growth rates, thinner shells, and higher mortality when exposed to projected future pH levels.\n\nThe ecological implications extend far beyond calcifying organisms. Coral reefs, which support an estimated 25 percent of all marine species despite covering less than 1 percent of the ocean floor, are particularly vulnerable. Reef degradation threatens the complex food webs and biodiversity hotspots that depend on coral structures. Pteropods, tiny swimming snails that form a critical component of polar food chains, have already shown signs of shell dissolution in Antarctic waters where acidification is most advanced.\n\nAddressing ocean acidification ultimately requires reducing atmospheric carbon dioxide concentrations, as the ocean's chemistry will continue to shift as long as excess CO2 persists in the atmosphere. Some researchers have proposed local interventions, such as adding alkaline minerals to coastal waters, but the scale of the ocean makes such approaches impractical as a global solution. International agreements to limit carbon emissions remain the most scientifically credible path to slowing ocean acidification, though the ocean's response to reduced emissions will be measured in decades, not years.",
          "passage_title": "Ocean Acidification and Marine Ecosystems",
          "passage_category": "environment",
          "passage_difficulty": 4,
          "estimated_reading_time": 190,
          "paragraphs": [
            "The world's oceans absorb approximately 30 percent of the carbon dioxide released into the atmosphere by human activities. While this absorption has moderated the pace of atmospheric warming, it has come at a significant cost to marine chemistry. When carbon dioxide dissolves in seawater, it forms carbonic acid, which releases hydrogen ions that lower the water's pH. Since the beginning of the industrial era, ocean surface pH has decreased by approximately 0.1 units, representing a 26 percent increase in acidity.",
            "This shift in ocean chemistry poses a direct threat to marine organisms that build shells or skeletons from calcium carbonate, including corals, mollusks, and certain plankton species. As acidity increases, the concentration of carbonate ions\u2014essential building blocks for these structures\u2014decreases, making it progressively more difficult and energetically costly for organisms to form and maintain their protective shells. Laboratory experiments have demonstrated that many calcifying species exhibit reduced growth rates, thinner shells, and higher mortality when exposed to projected future pH levels.",
            "The ecological implications extend far beyond calcifying organisms. Coral reefs, which support an estimated 25 percent of all marine species despite covering less than 1 percent of the ocean floor, are particularly vulnerable. Reef degradation threatens the complex food webs and biodiversity hotspots that depend on coral structures. Pteropods, tiny swimming snails that form a critical component of polar food chains, have already shown signs of shell dissolution in Antarctic waters where acidification is most advanced.",
            "Addressing ocean acidification ultimately requires reducing atmospheric carbon dioxide concentrations, as the ocean's chemistry will continue to shift as long as excess CO2 persists in the atmosphere. Some researchers have proposed local interventions, such as adding alkaline minerals to coastal waters, but the scale of the ocean makes such approaches impractical as a global solution. International agreements to limit carbon emissions remain the most scientifically credible path to slowing ocean acidification, though the ocean's response to reduced emissions will be measured in decades, not years."
          ]
        }
      ]
    },
    {
      "id": "rc-passage-008",
      "title": "Modernism in Architecture and the Democratization of Space",
      "category": "arts_and_culture",
      "difficulty": 3,
      "estimated_reading_time": 180,
      "paragraphs": [
        "The modernist movement in architecture, which emerged in the early twentieth century, sought to break decisively with historical styles and embrace the possibilities of new materials and construction techniques. Architects such as Le Corbusier, Ludwig Mies van der Rohe, and Walter Gropius championed designs characterized by clean lines, open floor plans, and the honest expression of structural materials like steel, concrete, and glass. Their ambition extended beyond aesthetics: modernism aspired to solve social problems through design, creating functional, affordable housing and public spaces accessible to all social classes.",
        "This democratic impulse was perhaps most clearly expressed in social housing projects of the mid-twentieth century. Le Corbusier's Unit\u00e9 d'Habitation in Marseille, completed in 1952, was designed as a self-contained community providing apartments, shops, recreational facilities, and a rooftop kindergarten within a single concrete structure. The building embodied the modernist belief that thoughtful design could improve quality of life for working-class residents by integrating housing with community services.",
        "However, the social ambitions of modernist architecture frequently collided with the realities of implementation. Large-scale housing projects, particularly in the United States and Britain, often suffered from poor construction quality, inadequate maintenance, and a failure to account for residents' social and cultural needs. The Pruitt-Igoe housing complex in St. Louis, designed according to modernist principles and demolished just two decades after its construction, became an emblem of modernism's perceived failure to deliver on its social promises.",
        "Contemporary architecture has largely moved beyond the rigid doctrines of high modernism while preserving its democratic aspirations. Architects increasingly engage with communities in the design process, incorporate cultural and contextual considerations, and blend modern materials with local building traditions. This evolution suggests that modernism's most enduring contribution may not be a specific aesthetic but rather the conviction that architecture bears social responsibility."
      ],
      "questions": [
        {
          "id": "rc-q-022",
          "passage_id": "rc-passage-008",
          "section": "verbal",
          "subsection": "reading_comprehension",
          "question_type": "authors_attitude",
          "topic": "arts_and_culture",
          "difficulty": 3,
          "target_solving_time": 90,
          "evidence_paragraphs": [
            1,
            2,
            3,
            4
          ],
          "question_text": "The author's attitude toward modernist architecture's social ambitions can best be described as",
          "options": [
            "wholly admiring and uncritical",
            "contemptuous and dismissive",
            "appreciative of the underlying ideals while acknowledging significant failures in execution",
            "indifferent to both the ideals and their outcomes",
            "primarily focused on the aesthetic achievements rather than social goals"
          ],
          "correct_option_index": 2,
          "explanation": "The author describes modernism's democratic aspirations positively (P1-P2) but honestly acknowledges implementation failures (P3) and notes that contemporary architecture has evolved while preserving the core ideal (P4). This is balanced appreciation with acknowledged shortcomings.",
          "option_explanations": [
            "Contradicted: P3 discusses significant failures.",
            "Contradicted: P4 affirms modernism's enduring contribution.",
            "Correct: Balanced appreciation of ideals with honest assessment of failures.",
            "Contradicted: The passage engages substantively with both ideals and outcomes.",
            "Contradicted: The passage focuses primarily on social goals, not aesthetics."
          ],
          "trap_type": "too_broad",
          "skills": [
            "authorial_attitude",
            "tone_analysis"
          ],
          "passage_text": "The modernist movement in architecture, which emerged in the early twentieth century, sought to break decisively with historical styles and embrace the possibilities of new materials and construction techniques. Architects such as Le Corbusier, Ludwig Mies van der Rohe, and Walter Gropius championed designs characterized by clean lines, open floor plans, and the honest expression of structural materials like steel, concrete, and glass. Their ambition extended beyond aesthetics: modernism aspired to solve social problems through design, creating functional, affordable housing and public spaces accessible to all social classes.\n\nThis democratic impulse was perhaps most clearly expressed in social housing projects of the mid-twentieth century. Le Corbusier's Unit\u00e9 d'Habitation in Marseille, completed in 1952, was designed as a self-contained community providing apartments, shops, recreational facilities, and a rooftop kindergarten within a single concrete structure. The building embodied the modernist belief that thoughtful design could improve quality of life for working-class residents by integrating housing with community services.\n\nHowever, the social ambitions of modernist architecture frequently collided with the realities of implementation. Large-scale housing projects, particularly in the United States and Britain, often suffered from poor construction quality, inadequate maintenance, and a failure to account for residents' social and cultural needs. The Pruitt-Igoe housing complex in St. Louis, designed according to modernist principles and demolished just two decades after its construction, became an emblem of modernism's perceived failure to deliver on its social promises.\n\nContemporary architecture has largely moved beyond the rigid doctrines of high modernism while preserving its democratic aspirations. Architects increasingly engage with communities in the design process, incorporate cultural and contextual considerations, and blend modern materials with local building traditions. This evolution suggests that modernism's most enduring contribution may not be a specific aesthetic but rather the conviction that architecture bears social responsibility.",
          "passage_title": "Modernism in Architecture and the Democratization of Space",
          "passage_category": "arts_and_culture",
          "passage_difficulty": 3,
          "estimated_reading_time": 180,
          "paragraphs": [
            "The modernist movement in architecture, which emerged in the early twentieth century, sought to break decisively with historical styles and embrace the possibilities of new materials and construction techniques. Architects such as Le Corbusier, Ludwig Mies van der Rohe, and Walter Gropius championed designs characterized by clean lines, open floor plans, and the honest expression of structural materials like steel, concrete, and glass. Their ambition extended beyond aesthetics: modernism aspired to solve social problems through design, creating functional, affordable housing and public spaces accessible to all social classes.",
            "This democratic impulse was perhaps most clearly expressed in social housing projects of the mid-twentieth century. Le Corbusier's Unit\u00e9 d'Habitation in Marseille, completed in 1952, was designed as a self-contained community providing apartments, shops, recreational facilities, and a rooftop kindergarten within a single concrete structure. The building embodied the modernist belief that thoughtful design could improve quality of life for working-class residents by integrating housing with community services.",
            "However, the social ambitions of modernist architecture frequently collided with the realities of implementation. Large-scale housing projects, particularly in the United States and Britain, often suffered from poor construction quality, inadequate maintenance, and a failure to account for residents' social and cultural needs. The Pruitt-Igoe housing complex in St. Louis, designed according to modernist principles and demolished just two decades after its construction, became an emblem of modernism's perceived failure to deliver on its social promises.",
            "Contemporary architecture has largely moved beyond the rigid doctrines of high modernism while preserving its democratic aspirations. Architects increasingly engage with communities in the design process, incorporate cultural and contextual considerations, and blend modern materials with local building traditions. This evolution suggests that modernism's most enduring contribution may not be a specific aesthetic but rather the conviction that architecture bears social responsibility."
          ]
        },
        {
          "id": "rc-q-023",
          "passage_id": "rc-passage-008",
          "section": "verbal",
          "subsection": "reading_comprehension",
          "question_type": "function_of_paragraph",
          "topic": "arts_and_culture",
          "difficulty": 3,
          "target_solving_time": 90,
          "evidence_paragraphs": [
            3
          ],
          "question_text": "Paragraph 3 primarily serves to",
          "options": [
            "celebrate the architectural achievements of the modernist movement",
            "argue that all modernist housing projects were unsuccessful",
            "present the gap between modernist social ambitions and implementation realities",
            "compare American and British approaches to social housing",
            "explain the engineering reasons why modernist buildings failed structurally"
          ],
          "correct_option_index": 2,
          "explanation": "P3 discusses how modernism's social ambitions 'collided with the realities of implementation,' using Pruitt-Igoe as an example of perceived failure. It presents the gap between vision and reality.",
          "option_explanations": [
            "Contradicted: P3 discusses failures, not celebrations.",
            "Too extreme: 'All' is not stated; specific failures are cited.",
            "Correct: Captures the paragraph's focus on the ambition-reality gap.",
            "Not the purpose: Both countries are mentioned briefly but not compared.",
            "Not discussed: Engineering failure reasons are not explained."
          ],
          "trap_type": "too_broad",
          "skills": [
            "paragraph_function",
            "critical_reading"
          ],
          "passage_text": "The modernist movement in architecture, which emerged in the early twentieth century, sought to break decisively with historical styles and embrace the possibilities of new materials and construction techniques. Architects such as Le Corbusier, Ludwig Mies van der Rohe, and Walter Gropius championed designs characterized by clean lines, open floor plans, and the honest expression of structural materials like steel, concrete, and glass. Their ambition extended beyond aesthetics: modernism aspired to solve social problems through design, creating functional, affordable housing and public spaces accessible to all social classes.\n\nThis democratic impulse was perhaps most clearly expressed in social housing projects of the mid-twentieth century. Le Corbusier's Unit\u00e9 d'Habitation in Marseille, completed in 1952, was designed as a self-contained community providing apartments, shops, recreational facilities, and a rooftop kindergarten within a single concrete structure. The building embodied the modernist belief that thoughtful design could improve quality of life for working-class residents by integrating housing with community services.\n\nHowever, the social ambitions of modernist architecture frequently collided with the realities of implementation. Large-scale housing projects, particularly in the United States and Britain, often suffered from poor construction quality, inadequate maintenance, and a failure to account for residents' social and cultural needs. The Pruitt-Igoe housing complex in St. Louis, designed according to modernist principles and demolished just two decades after its construction, became an emblem of modernism's perceived failure to deliver on its social promises.\n\nContemporary architecture has largely moved beyond the rigid doctrines of high modernism while preserving its democratic aspirations. Architects increasingly engage with communities in the design process, incorporate cultural and contextual considerations, and blend modern materials with local building traditions. This evolution suggests that modernism's most enduring contribution may not be a specific aesthetic but rather the conviction that architecture bears social responsibility.",
          "passage_title": "Modernism in Architecture and the Democratization of Space",
          "passage_category": "arts_and_culture",
          "passage_difficulty": 3,
          "estimated_reading_time": 180,
          "paragraphs": [
            "The modernist movement in architecture, which emerged in the early twentieth century, sought to break decisively with historical styles and embrace the possibilities of new materials and construction techniques. Architects such as Le Corbusier, Ludwig Mies van der Rohe, and Walter Gropius championed designs characterized by clean lines, open floor plans, and the honest expression of structural materials like steel, concrete, and glass. Their ambition extended beyond aesthetics: modernism aspired to solve social problems through design, creating functional, affordable housing and public spaces accessible to all social classes.",
            "This democratic impulse was perhaps most clearly expressed in social housing projects of the mid-twentieth century. Le Corbusier's Unit\u00e9 d'Habitation in Marseille, completed in 1952, was designed as a self-contained community providing apartments, shops, recreational facilities, and a rooftop kindergarten within a single concrete structure. The building embodied the modernist belief that thoughtful design could improve quality of life for working-class residents by integrating housing with community services.",
            "However, the social ambitions of modernist architecture frequently collided with the realities of implementation. Large-scale housing projects, particularly in the United States and Britain, often suffered from poor construction quality, inadequate maintenance, and a failure to account for residents' social and cultural needs. The Pruitt-Igoe housing complex in St. Louis, designed according to modernist principles and demolished just two decades after its construction, became an emblem of modernism's perceived failure to deliver on its social promises.",
            "Contemporary architecture has largely moved beyond the rigid doctrines of high modernism while preserving its democratic aspirations. Architects increasingly engage with communities in the design process, incorporate cultural and contextual considerations, and blend modern materials with local building traditions. This evolution suggests that modernism's most enduring contribution may not be a specific aesthetic but rather the conviction that architecture bears social responsibility."
          ]
        },
        {
          "id": "rc-q-024",
          "passage_id": "rc-passage-008",
          "section": "verbal",
          "subsection": "reading_comprehension",
          "question_type": "inference",
          "topic": "arts_and_culture",
          "difficulty": 3,
          "target_solving_time": 90,
          "evidence_paragraphs": [
            4
          ],
          "question_text": "The passage implies that contemporary architecture's approach to community engagement differs from high modernism's approach in that contemporary architects",
          "options": [
            "reject all modernist design principles as outdated",
            "prioritize aesthetics over functionality in their designs",
            "involve residents in the design process rather than imposing predetermined solutions",
            "focus exclusively on luxury developments rather than social housing",
            "use only traditional building materials and techniques"
          ],
          "correct_option_index": 2,
          "explanation": "P4 states that architects 'increasingly engage with communities in the design process,' implying a shift from modernism's top-down approach to participatory design.",
          "option_explanations": [
            "Too extreme: P4 says they preserve democratic aspirations from modernism.",
            "Not stated: The focus is on social responsibility, not aesthetics over function.",
            "Correct: Community engagement represents the key difference.",
            "Not stated: Social responsibility is maintained.",
            "Contradicted: P4 says they 'blend modern materials with local building traditions.'"
          ],
          "trap_type": "distortion",
          "skills": [
            "inference",
            "contrast"
          ],
          "passage_text": "The modernist movement in architecture, which emerged in the early twentieth century, sought to break decisively with historical styles and embrace the possibilities of new materials and construction techniques. Architects such as Le Corbusier, Ludwig Mies van der Rohe, and Walter Gropius championed designs characterized by clean lines, open floor plans, and the honest expression of structural materials like steel, concrete, and glass. Their ambition extended beyond aesthetics: modernism aspired to solve social problems through design, creating functional, affordable housing and public spaces accessible to all social classes.\n\nThis democratic impulse was perhaps most clearly expressed in social housing projects of the mid-twentieth century. Le Corbusier's Unit\u00e9 d'Habitation in Marseille, completed in 1952, was designed as a self-contained community providing apartments, shops, recreational facilities, and a rooftop kindergarten within a single concrete structure. The building embodied the modernist belief that thoughtful design could improve quality of life for working-class residents by integrating housing with community services.\n\nHowever, the social ambitions of modernist architecture frequently collided with the realities of implementation. Large-scale housing projects, particularly in the United States and Britain, often suffered from poor construction quality, inadequate maintenance, and a failure to account for residents' social and cultural needs. The Pruitt-Igoe housing complex in St. Louis, designed according to modernist principles and demolished just two decades after its construction, became an emblem of modernism's perceived failure to deliver on its social promises.\n\nContemporary architecture has largely moved beyond the rigid doctrines of high modernism while preserving its democratic aspirations. Architects increasingly engage with communities in the design process, incorporate cultural and contextual considerations, and blend modern materials with local building traditions. This evolution suggests that modernism's most enduring contribution may not be a specific aesthetic but rather the conviction that architecture bears social responsibility.",
          "passage_title": "Modernism in Architecture and the Democratization of Space",
          "passage_category": "arts_and_culture",
          "passage_difficulty": 3,
          "estimated_reading_time": 180,
          "paragraphs": [
            "The modernist movement in architecture, which emerged in the early twentieth century, sought to break decisively with historical styles and embrace the possibilities of new materials and construction techniques. Architects such as Le Corbusier, Ludwig Mies van der Rohe, and Walter Gropius championed designs characterized by clean lines, open floor plans, and the honest expression of structural materials like steel, concrete, and glass. Their ambition extended beyond aesthetics: modernism aspired to solve social problems through design, creating functional, affordable housing and public spaces accessible to all social classes.",
            "This democratic impulse was perhaps most clearly expressed in social housing projects of the mid-twentieth century. Le Corbusier's Unit\u00e9 d'Habitation in Marseille, completed in 1952, was designed as a self-contained community providing apartments, shops, recreational facilities, and a rooftop kindergarten within a single concrete structure. The building embodied the modernist belief that thoughtful design could improve quality of life for working-class residents by integrating housing with community services.",
            "However, the social ambitions of modernist architecture frequently collided with the realities of implementation. Large-scale housing projects, particularly in the United States and Britain, often suffered from poor construction quality, inadequate maintenance, and a failure to account for residents' social and cultural needs. The Pruitt-Igoe housing complex in St. Louis, designed according to modernist principles and demolished just two decades after its construction, became an emblem of modernism's perceived failure to deliver on its social promises.",
            "Contemporary architecture has largely moved beyond the rigid doctrines of high modernism while preserving its democratic aspirations. Architects increasingly engage with communities in the design process, incorporate cultural and contextual considerations, and blend modern materials with local building traditions. This evolution suggests that modernism's most enduring contribution may not be a specific aesthetic but rather the conviction that architecture bears social responsibility."
          ]
        }
      ]
    }
  ],
  "RC_QUESTIONS": [
    {
      "id": "rc-q-001",
      "passage_id": "rc-passage-001",
      "section": "verbal",
      "subsection": "reading_comprehension",
      "question_type": "primary_purpose",
      "topic": "business",
      "difficulty": 3,
      "target_solving_time": 90,
      "evidence_paragraphs": [
        1,
        2,
        3,
        4
      ],
      "question_text": "The primary purpose of the passage is to",
      "options": [
        "advocate for the adoption of stakeholder capitalism over shareholder primacy",
        "present the evolution, arguments, evidence, and challenges related to stakeholder capitalism",
        "demonstrate that ESG practices lead to superior financial performance",
        "criticize Milton Friedman's theory of shareholder primacy",
        "propose regulatory reforms to enforce stakeholder accountability"
      ],
      "correct_option_index": 1,
      "explanation": "The passage traces the historical shift from shareholder primacy to stakeholder capitalism, presents arguments from both sides, reviews mixed empirical evidence, and discusses implementation challenges. It is balanced and informational, not advocating a single position.",
      "option_explanations": [
        "Too one-sided: The passage presents both sides without advocating for stakeholder capitalism.",
        "Correct: Captures the passage's balanced, informational approach covering evolution, debate, evidence, and challenges.",
        "Too narrow and inaccurate: The passage notes mixed evidence, not conclusive outperformance.",
        "Too narrow: Friedman is mentioned as context, not as the target of criticism.",
        "Too narrow: Regulatory reform is mentioned in one paragraph as one possible solution, not the passage's main purpose."
      ],
      "trap_type": "too_broad",
      "skills": [
        "primary_purpose",
        "passage_structure"
      ],
      "passage_text": "For much of the twentieth century, the dominant paradigm in corporate governance was shareholder primacy\u2014the idea that a corporation's primary obligation is to maximize returns for its shareholders. This view, championed by economist Milton Friedman in his 1970 essay, held that social responsibility beyond profit maximization was tantamount to taxation without representation, as it involved spending shareholders' money on goals they had not endorsed.\n\nIn recent decades, however, stakeholder capitalism has gained significant traction. Proponents argue that corporations have obligations not only to shareholders but also to employees, customers, communities, and the environment. The Business Roundtable's 2019 statement, signed by 181 CEOs, redefined the purpose of a corporation to include commitment to all stakeholders. Critics counter that without a single measurable objective, managers lack accountability and can justify virtually any decision as serving some stakeholder interest.\n\nEmpirical evidence on the performance implications of stakeholder capitalism remains mixed. Some studies suggest that companies with strong environmental, social, and governance (ESG) practices outperform their peers over the long term, while others find no statistically significant relationship between ESG scores and financial returns. The methodological challenge lies in isolating the causal effect of stakeholder orientation from the many confounding variables that influence corporate performance.\n\nThe practical implementation of stakeholder capitalism also presents challenges. Balancing competing stakeholder interests\u2014for example, when wage increases for employees reduce short-term returns for shareholders\u2014requires judgment calls that existing governance frameworks are not designed to adjudicate. Some scholars propose that regulatory reform, rather than voluntary corporate pledges, is the most effective path toward stakeholder accountability.",
      "passage_title": "Stakeholder Capitalism and Corporate Governance",
      "passage_category": "business",
      "passage_difficulty": 3,
      "estimated_reading_time": 180,
      "paragraphs": [
        "For much of the twentieth century, the dominant paradigm in corporate governance was shareholder primacy\u2014the idea that a corporation's primary obligation is to maximize returns for its shareholders. This view, championed by economist Milton Friedman in his 1970 essay, held that social responsibility beyond profit maximization was tantamount to taxation without representation, as it involved spending shareholders' money on goals they had not endorsed.",
        "In recent decades, however, stakeholder capitalism has gained significant traction. Proponents argue that corporations have obligations not only to shareholders but also to employees, customers, communities, and the environment. The Business Roundtable's 2019 statement, signed by 181 CEOs, redefined the purpose of a corporation to include commitment to all stakeholders. Critics counter that without a single measurable objective, managers lack accountability and can justify virtually any decision as serving some stakeholder interest.",
        "Empirical evidence on the performance implications of stakeholder capitalism remains mixed. Some studies suggest that companies with strong environmental, social, and governance (ESG) practices outperform their peers over the long term, while others find no statistically significant relationship between ESG scores and financial returns. The methodological challenge lies in isolating the causal effect of stakeholder orientation from the many confounding variables that influence corporate performance.",
        "The practical implementation of stakeholder capitalism also presents challenges. Balancing competing stakeholder interests\u2014for example, when wage increases for employees reduce short-term returns for shareholders\u2014requires judgment calls that existing governance frameworks are not designed to adjudicate. Some scholars propose that regulatory reform, rather than voluntary corporate pledges, is the most effective path toward stakeholder accountability."
      ]
    },
    {
      "id": "rc-q-002",
      "passage_id": "rc-passage-001",
      "section": "verbal",
      "subsection": "reading_comprehension",
      "question_type": "detail",
      "topic": "business",
      "difficulty": 2,
      "target_solving_time": 75,
      "evidence_paragraphs": [
        2
      ],
      "question_text": "According to the passage, critics of stakeholder capitalism argue that",
      "options": [
        "corporations should never consider environmental impacts in decision-making",
        "the stakeholder model reduces corporate profitability",
        "without a single measurable objective, managers lack accountability",
        "the Business Roundtable statement was signed by too few CEOs to be meaningful",
        "shareholder primacy leads to better employee satisfaction"
      ],
      "correct_option_index": 2,
      "explanation": "Paragraph 2 explicitly states that critics argue 'without a single measurable objective, managers lack accountability and can justify virtually any decision as serving some stakeholder interest.'",
      "option_explanations": [
        "Distortion: Critics argue about accountability, not a complete ban on environmental consideration.",
        "Not stated: The passage doesn't attribute a profitability claim to the critics.",
        "Correct: Directly stated in paragraph 2.",
        "Not stated: The passage mentions 181 CEOs but critics don't challenge the number.",
        "Not stated: Critics don't make claims about employee satisfaction under shareholder primacy."
      ],
      "trap_type": "distortion",
      "skills": [
        "detail_retrieval",
        "careful_reading"
      ],
      "passage_text": "For much of the twentieth century, the dominant paradigm in corporate governance was shareholder primacy\u2014the idea that a corporation's primary obligation is to maximize returns for its shareholders. This view, championed by economist Milton Friedman in his 1970 essay, held that social responsibility beyond profit maximization was tantamount to taxation without representation, as it involved spending shareholders' money on goals they had not endorsed.\n\nIn recent decades, however, stakeholder capitalism has gained significant traction. Proponents argue that corporations have obligations not only to shareholders but also to employees, customers, communities, and the environment. The Business Roundtable's 2019 statement, signed by 181 CEOs, redefined the purpose of a corporation to include commitment to all stakeholders. Critics counter that without a single measurable objective, managers lack accountability and can justify virtually any decision as serving some stakeholder interest.\n\nEmpirical evidence on the performance implications of stakeholder capitalism remains mixed. Some studies suggest that companies with strong environmental, social, and governance (ESG) practices outperform their peers over the long term, while others find no statistically significant relationship between ESG scores and financial returns. The methodological challenge lies in isolating the causal effect of stakeholder orientation from the many confounding variables that influence corporate performance.\n\nThe practical implementation of stakeholder capitalism also presents challenges. Balancing competing stakeholder interests\u2014for example, when wage increases for employees reduce short-term returns for shareholders\u2014requires judgment calls that existing governance frameworks are not designed to adjudicate. Some scholars propose that regulatory reform, rather than voluntary corporate pledges, is the most effective path toward stakeholder accountability.",
      "passage_title": "Stakeholder Capitalism and Corporate Governance",
      "passage_category": "business",
      "passage_difficulty": 3,
      "estimated_reading_time": 180,
      "paragraphs": [
        "For much of the twentieth century, the dominant paradigm in corporate governance was shareholder primacy\u2014the idea that a corporation's primary obligation is to maximize returns for its shareholders. This view, championed by economist Milton Friedman in his 1970 essay, held that social responsibility beyond profit maximization was tantamount to taxation without representation, as it involved spending shareholders' money on goals they had not endorsed.",
        "In recent decades, however, stakeholder capitalism has gained significant traction. Proponents argue that corporations have obligations not only to shareholders but also to employees, customers, communities, and the environment. The Business Roundtable's 2019 statement, signed by 181 CEOs, redefined the purpose of a corporation to include commitment to all stakeholders. Critics counter that without a single measurable objective, managers lack accountability and can justify virtually any decision as serving some stakeholder interest.",
        "Empirical evidence on the performance implications of stakeholder capitalism remains mixed. Some studies suggest that companies with strong environmental, social, and governance (ESG) practices outperform their peers over the long term, while others find no statistically significant relationship between ESG scores and financial returns. The methodological challenge lies in isolating the causal effect of stakeholder orientation from the many confounding variables that influence corporate performance.",
        "The practical implementation of stakeholder capitalism also presents challenges. Balancing competing stakeholder interests\u2014for example, when wage increases for employees reduce short-term returns for shareholders\u2014requires judgment calls that existing governance frameworks are not designed to adjudicate. Some scholars propose that regulatory reform, rather than voluntary corporate pledges, is the most effective path toward stakeholder accountability."
      ]
    },
    {
      "id": "rc-q-003",
      "passage_id": "rc-passage-001",
      "section": "verbal",
      "subsection": "reading_comprehension",
      "question_type": "inference",
      "topic": "business",
      "difficulty": 4,
      "target_solving_time": 100,
      "evidence_paragraphs": [
        3
      ],
      "question_text": "The passage suggests that the relationship between ESG practices and financial performance is difficult to establish because",
      "options": [
        "most companies with strong ESG scores are relatively new and lack sufficient financial history",
        "ESG scoring methodologies are inconsistent across rating agencies",
        "many variables besides ESG practices affect corporate performance, making it hard to isolate ESG's specific impact",
        "shareholders consistently oppose ESG initiatives, biasing performance data",
        "companies manipulate their ESG scores to attract investors"
      ],
      "correct_option_index": 2,
      "explanation": "Paragraph 3 states 'The methodological challenge lies in isolating the causal effect of stakeholder orientation from the many confounding variables that influence corporate performance.' This directly supports option C.",
      "option_explanations": [
        "Not stated: The passage doesn't mention company age or financial history.",
        "Not stated: Rating methodology inconsistency is not mentioned in the passage.",
        "Correct: Directly supported by the passage's discussion of confounding variables.",
        "Not stated: Shareholder opposition to ESG is not mentioned.",
        "Not stated: ESG score manipulation is not discussed."
      ],
      "trap_type": "unsupported_inference",
      "skills": [
        "inference",
        "causal_reasoning"
      ],
      "passage_text": "For much of the twentieth century, the dominant paradigm in corporate governance was shareholder primacy\u2014the idea that a corporation's primary obligation is to maximize returns for its shareholders. This view, championed by economist Milton Friedman in his 1970 essay, held that social responsibility beyond profit maximization was tantamount to taxation without representation, as it involved spending shareholders' money on goals they had not endorsed.\n\nIn recent decades, however, stakeholder capitalism has gained significant traction. Proponents argue that corporations have obligations not only to shareholders but also to employees, customers, communities, and the environment. The Business Roundtable's 2019 statement, signed by 181 CEOs, redefined the purpose of a corporation to include commitment to all stakeholders. Critics counter that without a single measurable objective, managers lack accountability and can justify virtually any decision as serving some stakeholder interest.\n\nEmpirical evidence on the performance implications of stakeholder capitalism remains mixed. Some studies suggest that companies with strong environmental, social, and governance (ESG) practices outperform their peers over the long term, while others find no statistically significant relationship between ESG scores and financial returns. The methodological challenge lies in isolating the causal effect of stakeholder orientation from the many confounding variables that influence corporate performance.\n\nThe practical implementation of stakeholder capitalism also presents challenges. Balancing competing stakeholder interests\u2014for example, when wage increases for employees reduce short-term returns for shareholders\u2014requires judgment calls that existing governance frameworks are not designed to adjudicate. Some scholars propose that regulatory reform, rather than voluntary corporate pledges, is the most effective path toward stakeholder accountability.",
      "passage_title": "Stakeholder Capitalism and Corporate Governance",
      "passage_category": "business",
      "passage_difficulty": 3,
      "estimated_reading_time": 180,
      "paragraphs": [
        "For much of the twentieth century, the dominant paradigm in corporate governance was shareholder primacy\u2014the idea that a corporation's primary obligation is to maximize returns for its shareholders. This view, championed by economist Milton Friedman in his 1970 essay, held that social responsibility beyond profit maximization was tantamount to taxation without representation, as it involved spending shareholders' money on goals they had not endorsed.",
        "In recent decades, however, stakeholder capitalism has gained significant traction. Proponents argue that corporations have obligations not only to shareholders but also to employees, customers, communities, and the environment. The Business Roundtable's 2019 statement, signed by 181 CEOs, redefined the purpose of a corporation to include commitment to all stakeholders. Critics counter that without a single measurable objective, managers lack accountability and can justify virtually any decision as serving some stakeholder interest.",
        "Empirical evidence on the performance implications of stakeholder capitalism remains mixed. Some studies suggest that companies with strong environmental, social, and governance (ESG) practices outperform their peers over the long term, while others find no statistically significant relationship between ESG scores and financial returns. The methodological challenge lies in isolating the causal effect of stakeholder orientation from the many confounding variables that influence corporate performance.",
        "The practical implementation of stakeholder capitalism also presents challenges. Balancing competing stakeholder interests\u2014for example, when wage increases for employees reduce short-term returns for shareholders\u2014requires judgment calls that existing governance frameworks are not designed to adjudicate. Some scholars propose that regulatory reform, rather than voluntary corporate pledges, is the most effective path toward stakeholder accountability."
      ]
    },
    {
      "id": "rc-q-004",
      "passage_id": "rc-passage-001",
      "section": "verbal",
      "subsection": "reading_comprehension",
      "question_type": "function_of_paragraph",
      "topic": "business",
      "difficulty": 3,
      "target_solving_time": 90,
      "evidence_paragraphs": [
        4
      ],
      "question_text": "The fourth paragraph primarily serves to",
      "options": [
        "summarize the arguments presented in the first three paragraphs",
        "present counterevidence against the claims made in paragraph 3",
        "discuss practical difficulties in implementing stakeholder capitalism and suggest a possible solution",
        "argue that regulatory reform is the only viable approach to corporate governance",
        "provide examples of successful stakeholder capitalism implementations"
      ],
      "correct_option_index": 2,
      "explanation": "Paragraph 4 discusses practical challenges (balancing competing interests, inadequate governance frameworks) and mentions regulatory reform as a possible path forward. It addresses implementation, not theory.",
      "option_explanations": [
        "Incorrect: It introduces new content about implementation, not a summary.",
        "Incorrect: It does not counter paragraph 3's evidence discussion.",
        "Correct: Identifies implementation challenges and suggests regulatory reform.",
        "Too extreme: It mentions regulatory reform as one proposal, not the 'only viable approach.'",
        "Incorrect: No specific success examples are given."
      ],
      "trap_type": "too_narrow",
      "skills": [
        "paragraph_function",
        "passage_structure"
      ],
      "passage_text": "For much of the twentieth century, the dominant paradigm in corporate governance was shareholder primacy\u2014the idea that a corporation's primary obligation is to maximize returns for its shareholders. This view, championed by economist Milton Friedman in his 1970 essay, held that social responsibility beyond profit maximization was tantamount to taxation without representation, as it involved spending shareholders' money on goals they had not endorsed.\n\nIn recent decades, however, stakeholder capitalism has gained significant traction. Proponents argue that corporations have obligations not only to shareholders but also to employees, customers, communities, and the environment. The Business Roundtable's 2019 statement, signed by 181 CEOs, redefined the purpose of a corporation to include commitment to all stakeholders. Critics counter that without a single measurable objective, managers lack accountability and can justify virtually any decision as serving some stakeholder interest.\n\nEmpirical evidence on the performance implications of stakeholder capitalism remains mixed. Some studies suggest that companies with strong environmental, social, and governance (ESG) practices outperform their peers over the long term, while others find no statistically significant relationship between ESG scores and financial returns. The methodological challenge lies in isolating the causal effect of stakeholder orientation from the many confounding variables that influence corporate performance.\n\nThe practical implementation of stakeholder capitalism also presents challenges. Balancing competing stakeholder interests\u2014for example, when wage increases for employees reduce short-term returns for shareholders\u2014requires judgment calls that existing governance frameworks are not designed to adjudicate. Some scholars propose that regulatory reform, rather than voluntary corporate pledges, is the most effective path toward stakeholder accountability.",
      "passage_title": "Stakeholder Capitalism and Corporate Governance",
      "passage_category": "business",
      "passage_difficulty": 3,
      "estimated_reading_time": 180,
      "paragraphs": [
        "For much of the twentieth century, the dominant paradigm in corporate governance was shareholder primacy\u2014the idea that a corporation's primary obligation is to maximize returns for its shareholders. This view, championed by economist Milton Friedman in his 1970 essay, held that social responsibility beyond profit maximization was tantamount to taxation without representation, as it involved spending shareholders' money on goals they had not endorsed.",
        "In recent decades, however, stakeholder capitalism has gained significant traction. Proponents argue that corporations have obligations not only to shareholders but also to employees, customers, communities, and the environment. The Business Roundtable's 2019 statement, signed by 181 CEOs, redefined the purpose of a corporation to include commitment to all stakeholders. Critics counter that without a single measurable objective, managers lack accountability and can justify virtually any decision as serving some stakeholder interest.",
        "Empirical evidence on the performance implications of stakeholder capitalism remains mixed. Some studies suggest that companies with strong environmental, social, and governance (ESG) practices outperform their peers over the long term, while others find no statistically significant relationship between ESG scores and financial returns. The methodological challenge lies in isolating the causal effect of stakeholder orientation from the many confounding variables that influence corporate performance.",
        "The practical implementation of stakeholder capitalism also presents challenges. Balancing competing stakeholder interests\u2014for example, when wage increases for employees reduce short-term returns for shareholders\u2014requires judgment calls that existing governance frameworks are not designed to adjudicate. Some scholars propose that regulatory reform, rather than voluntary corporate pledges, is the most effective path toward stakeholder accountability."
      ]
    },
    {
      "id": "rc-q-005",
      "passage_id": "rc-passage-002",
      "section": "verbal",
      "subsection": "reading_comprehension",
      "question_type": "main_idea",
      "topic": "economics",
      "difficulty": 3,
      "target_solving_time": 90,
      "evidence_paragraphs": [
        1,
        2,
        3,
        4
      ],
      "question_text": "Which of the following best describes the main idea of the passage?",
      "options": [
        "Central bank digital currencies are superior to decentralized cryptocurrencies.",
        "Digital currencies pose challenges to traditional monetary policy, and CBDCs present both opportunities and risks as a response.",
        "The traditional instruments of monetary policy are no longer effective in the modern economy.",
        "China and Europe are leading the development of central bank digital currencies.",
        "Decentralized cryptocurrencies will inevitably replace traditional banking systems."
      ],
      "correct_option_index": 1,
      "explanation": "The passage explains how digital currencies challenge monetary policy (P1-P2), introduces CBDCs as a response with benefits (P3), and discusses their risks (P4). Option B captures this balanced arc.",
      "option_explanations": [
        "Too one-sided: The passage presents benefits and concerns of CBDCs.",
        "Correct: Captures the challenge, response, and balanced evaluation.",
        "Too extreme: The passage says tools may be weakened, not that they are no longer effective.",
        "Too narrow: Specific CBDC projects are details, not the main idea.",
        "Too extreme: 'Inevitably replace' is not supported by the passage."
      ],
      "trap_type": "too_broad",
      "skills": [
        "main_idea",
        "passage_comprehension"
      ],
      "passage_text": "Central banks have traditionally managed monetary policy through three primary instruments: setting benchmark interest rates, conducting open market operations, and adjusting reserve requirements for commercial banks. These tools operate through the banking system, influencing the cost and availability of credit to shape economic activity. The effectiveness of these instruments depends on the assumption that the vast majority of economic transactions flow through regulated financial institutions.\n\nThe emergence of decentralized digital currencies, particularly those built on blockchain technology, threatens to undermine this assumption. If a significant share of transactions migrates to cryptocurrency networks that operate outside the traditional banking system, central banks may find their monetary policy transmission mechanisms weakened. A consumer who holds savings in Bitcoin rather than a bank deposit is not directly affected by changes in the central bank's interest rate.\n\nCentral bank digital currencies (CBDCs) represent one response to this challenge. By issuing their own digital currencies, central banks could maintain direct influence over the money supply even in an increasingly digital economy. China's digital yuan and the European Central Bank's digital euro project are among the most advanced CBDC initiatives. Proponents argue that CBDCs could enhance financial inclusion, reduce transaction costs, and strengthen monetary policy transmission.\n\nHowever, CBDCs also raise significant concerns. A CBDC that allows the central bank to monitor all transactions could compromise financial privacy. Furthermore, if consumers can hold CBDC balances directly with the central bank, commercial banks could face deposit outflows during periods of financial stress, potentially amplifying bank runs rather than preventing them. Designing a CBDC that balances innovation with stability remains an open challenge for policymakers.",
      "passage_title": "Monetary Policy in the Age of Digital Currencies",
      "passage_category": "economics",
      "passage_difficulty": 4,
      "estimated_reading_time": 190,
      "paragraphs": [
        "Central banks have traditionally managed monetary policy through three primary instruments: setting benchmark interest rates, conducting open market operations, and adjusting reserve requirements for commercial banks. These tools operate through the banking system, influencing the cost and availability of credit to shape economic activity. The effectiveness of these instruments depends on the assumption that the vast majority of economic transactions flow through regulated financial institutions.",
        "The emergence of decentralized digital currencies, particularly those built on blockchain technology, threatens to undermine this assumption. If a significant share of transactions migrates to cryptocurrency networks that operate outside the traditional banking system, central banks may find their monetary policy transmission mechanisms weakened. A consumer who holds savings in Bitcoin rather than a bank deposit is not directly affected by changes in the central bank's interest rate.",
        "Central bank digital currencies (CBDCs) represent one response to this challenge. By issuing their own digital currencies, central banks could maintain direct influence over the money supply even in an increasingly digital economy. China's digital yuan and the European Central Bank's digital euro project are among the most advanced CBDC initiatives. Proponents argue that CBDCs could enhance financial inclusion, reduce transaction costs, and strengthen monetary policy transmission.",
        "However, CBDCs also raise significant concerns. A CBDC that allows the central bank to monitor all transactions could compromise financial privacy. Furthermore, if consumers can hold CBDC balances directly with the central bank, commercial banks could face deposit outflows during periods of financial stress, potentially amplifying bank runs rather than preventing them. Designing a CBDC that balances innovation with stability remains an open challenge for policymakers."
      ]
    },
    {
      "id": "rc-q-006",
      "passage_id": "rc-passage-002",
      "section": "verbal",
      "subsection": "reading_comprehension",
      "question_type": "authors_tone",
      "topic": "economics",
      "difficulty": 3,
      "target_solving_time": 80,
      "evidence_paragraphs": [
        1,
        2,
        3,
        4
      ],
      "question_text": "The author's tone in discussing CBDCs can best be described as",
      "options": [
        "enthusiastically supportive",
        "dismissive and skeptical",
        "analytically balanced, acknowledging both potential and concerns",
        "cautiously optimistic about their inevitable success",
        "deeply alarmed about privacy implications"
      ],
      "correct_option_index": 2,
      "explanation": "The author presents CBDC benefits (P3) and concerns (P4) without advocating for or against them. The tone is analytical and balanced throughout.",
      "option_explanations": [
        "Too positive: The author also raises significant concerns.",
        "Too negative: The author acknowledges potential benefits.",
        "Correct: Balanced analytical tone presenting both sides.",
        "Contradicted: The author does not suggest CBDCs are inevitable.",
        "Too extreme: Privacy is one concern mentioned, not the author's dominant attitude."
      ],
      "trap_type": "distortion",
      "skills": [
        "tone_identification",
        "authorial_perspective"
      ],
      "passage_text": "Central banks have traditionally managed monetary policy through three primary instruments: setting benchmark interest rates, conducting open market operations, and adjusting reserve requirements for commercial banks. These tools operate through the banking system, influencing the cost and availability of credit to shape economic activity. The effectiveness of these instruments depends on the assumption that the vast majority of economic transactions flow through regulated financial institutions.\n\nThe emergence of decentralized digital currencies, particularly those built on blockchain technology, threatens to undermine this assumption. If a significant share of transactions migrates to cryptocurrency networks that operate outside the traditional banking system, central banks may find their monetary policy transmission mechanisms weakened. A consumer who holds savings in Bitcoin rather than a bank deposit is not directly affected by changes in the central bank's interest rate.\n\nCentral bank digital currencies (CBDCs) represent one response to this challenge. By issuing their own digital currencies, central banks could maintain direct influence over the money supply even in an increasingly digital economy. China's digital yuan and the European Central Bank's digital euro project are among the most advanced CBDC initiatives. Proponents argue that CBDCs could enhance financial inclusion, reduce transaction costs, and strengthen monetary policy transmission.\n\nHowever, CBDCs also raise significant concerns. A CBDC that allows the central bank to monitor all transactions could compromise financial privacy. Furthermore, if consumers can hold CBDC balances directly with the central bank, commercial banks could face deposit outflows during periods of financial stress, potentially amplifying bank runs rather than preventing them. Designing a CBDC that balances innovation with stability remains an open challenge for policymakers.",
      "passage_title": "Monetary Policy in the Age of Digital Currencies",
      "passage_category": "economics",
      "passage_difficulty": 4,
      "estimated_reading_time": 190,
      "paragraphs": [
        "Central banks have traditionally managed monetary policy through three primary instruments: setting benchmark interest rates, conducting open market operations, and adjusting reserve requirements for commercial banks. These tools operate through the banking system, influencing the cost and availability of credit to shape economic activity. The effectiveness of these instruments depends on the assumption that the vast majority of economic transactions flow through regulated financial institutions.",
        "The emergence of decentralized digital currencies, particularly those built on blockchain technology, threatens to undermine this assumption. If a significant share of transactions migrates to cryptocurrency networks that operate outside the traditional banking system, central banks may find their monetary policy transmission mechanisms weakened. A consumer who holds savings in Bitcoin rather than a bank deposit is not directly affected by changes in the central bank's interest rate.",
        "Central bank digital currencies (CBDCs) represent one response to this challenge. By issuing their own digital currencies, central banks could maintain direct influence over the money supply even in an increasingly digital economy. China's digital yuan and the European Central Bank's digital euro project are among the most advanced CBDC initiatives. Proponents argue that CBDCs could enhance financial inclusion, reduce transaction costs, and strengthen monetary policy transmission.",
        "However, CBDCs also raise significant concerns. A CBDC that allows the central bank to monitor all transactions could compromise financial privacy. Furthermore, if consumers can hold CBDC balances directly with the central bank, commercial banks could face deposit outflows during periods of financial stress, potentially amplifying bank runs rather than preventing them. Designing a CBDC that balances innovation with stability remains an open challenge for policymakers."
      ]
    },
    {
      "id": "rc-q-007",
      "passage_id": "rc-passage-002",
      "section": "verbal",
      "subsection": "reading_comprehension",
      "question_type": "detail",
      "topic": "economics",
      "difficulty": 2,
      "target_solving_time": 75,
      "evidence_paragraphs": [
        1
      ],
      "question_text": "According to paragraph 1, the effectiveness of traditional monetary policy instruments depends on",
      "options": [
        "the central bank's ability to set negative interest rates",
        "the majority of economic transactions flowing through regulated financial institutions",
        "government fiscal policy working in coordination with monetary policy",
        "commercial banks voluntarily cooperating with central bank directives",
        "consumer confidence in the stability of the national currency"
      ],
      "correct_option_index": 1,
      "explanation": "Paragraph 1 explicitly states: 'The effectiveness of these instruments depends on the assumption that the vast majority of economic transactions flow through regulated financial institutions.'",
      "option_explanations": [
        "Not stated: Negative rates are not mentioned.",
        "Correct: Directly stated in paragraph 1.",
        "Not stated: Fiscal policy coordination is not discussed.",
        "Not stated: Voluntary cooperation is not the stated dependency.",
        "Not stated: Consumer confidence is not mentioned as a dependency."
      ],
      "trap_type": "out_of_scope",
      "skills": [
        "detail_retrieval"
      ],
      "passage_text": "Central banks have traditionally managed monetary policy through three primary instruments: setting benchmark interest rates, conducting open market operations, and adjusting reserve requirements for commercial banks. These tools operate through the banking system, influencing the cost and availability of credit to shape economic activity. The effectiveness of these instruments depends on the assumption that the vast majority of economic transactions flow through regulated financial institutions.\n\nThe emergence of decentralized digital currencies, particularly those built on blockchain technology, threatens to undermine this assumption. If a significant share of transactions migrates to cryptocurrency networks that operate outside the traditional banking system, central banks may find their monetary policy transmission mechanisms weakened. A consumer who holds savings in Bitcoin rather than a bank deposit is not directly affected by changes in the central bank's interest rate.\n\nCentral bank digital currencies (CBDCs) represent one response to this challenge. By issuing their own digital currencies, central banks could maintain direct influence over the money supply even in an increasingly digital economy. China's digital yuan and the European Central Bank's digital euro project are among the most advanced CBDC initiatives. Proponents argue that CBDCs could enhance financial inclusion, reduce transaction costs, and strengthen monetary policy transmission.\n\nHowever, CBDCs also raise significant concerns. A CBDC that allows the central bank to monitor all transactions could compromise financial privacy. Furthermore, if consumers can hold CBDC balances directly with the central bank, commercial banks could face deposit outflows during periods of financial stress, potentially amplifying bank runs rather than preventing them. Designing a CBDC that balances innovation with stability remains an open challenge for policymakers.",
      "passage_title": "Monetary Policy in the Age of Digital Currencies",
      "passage_category": "economics",
      "passage_difficulty": 4,
      "estimated_reading_time": 190,
      "paragraphs": [
        "Central banks have traditionally managed monetary policy through three primary instruments: setting benchmark interest rates, conducting open market operations, and adjusting reserve requirements for commercial banks. These tools operate through the banking system, influencing the cost and availability of credit to shape economic activity. The effectiveness of these instruments depends on the assumption that the vast majority of economic transactions flow through regulated financial institutions.",
        "The emergence of decentralized digital currencies, particularly those built on blockchain technology, threatens to undermine this assumption. If a significant share of transactions migrates to cryptocurrency networks that operate outside the traditional banking system, central banks may find their monetary policy transmission mechanisms weakened. A consumer who holds savings in Bitcoin rather than a bank deposit is not directly affected by changes in the central bank's interest rate.",
        "Central bank digital currencies (CBDCs) represent one response to this challenge. By issuing their own digital currencies, central banks could maintain direct influence over the money supply even in an increasingly digital economy. China's digital yuan and the European Central Bank's digital euro project are among the most advanced CBDC initiatives. Proponents argue that CBDCs could enhance financial inclusion, reduce transaction costs, and strengthen monetary policy transmission.",
        "However, CBDCs also raise significant concerns. A CBDC that allows the central bank to monitor all transactions could compromise financial privacy. Furthermore, if consumers can hold CBDC balances directly with the central bank, commercial banks could face deposit outflows during periods of financial stress, potentially amplifying bank runs rather than preventing them. Designing a CBDC that balances innovation with stability remains an open challenge for policymakers."
      ]
    },
    {
      "id": "rc-q-008",
      "passage_id": "rc-passage-003",
      "section": "verbal",
      "subsection": "reading_comprehension",
      "question_type": "main_idea",
      "topic": "science",
      "difficulty": 3,
      "target_solving_time": 90,
      "evidence_paragraphs": [
        1,
        2,
        3,
        4
      ],
      "question_text": "The passage is primarily concerned with",
      "options": [
        "disproving the central dogma of molecular biology",
        "describing how epigenetic mechanisms challenge traditional views of genetic determinism while noting ongoing scientific debates",
        "advocating for increased funding for epigenetic research",
        "explaining the molecular mechanism of DNA methylation in detail",
        "comparing the Dutch famine study with rodent epigenetic studies"
      ],
      "correct_option_index": 1,
      "explanation": "The passage introduces traditional genetics, explains how epigenetics challenges it, discusses transgenerational inheritance, and presents the scientific debate. This balanced overview matches option B.",
      "option_explanations": [
        "Too strong: The passage says epigenetics 'complicated' the picture, not disproved the dogma.",
        "Correct: Captures the challenge to traditional views and the ongoing debates.",
        "Not the purpose: Funding advocacy is not mentioned.",
        "Too narrow: DNA methylation details are supporting evidence, not the main concern.",
        "Too narrow: The studies are examples, not the central comparison."
      ],
      "trap_type": "too_broad",
      "skills": [
        "main_idea",
        "scientific_reasoning"
      ],
      "passage_text": "The central dogma of molecular biology\u2014that genetic information flows from DNA to RNA to protein\u2014long suggested that an organism's traits are determined primarily by the nucleotide sequences it inherits. Under this view, environmental factors could select among organisms with different genotypes but could not alter the genetic instructions themselves. The discovery of epigenetic mechanisms has fundamentally complicated this picture.\n\nEpigenetic modifications, such as DNA methylation and histone acetylation, can alter gene expression without changing the underlying DNA sequence. These chemical markers act as molecular switches, turning genes on or off in response to environmental signals. A landmark study of Dutch famine survivors demonstrated that individuals exposed to severe caloric restriction in utero exhibited distinct methylation patterns decades later, with corresponding increases in rates of cardiovascular disease and metabolic disorders.\n\nPerhaps most provocatively, some research suggests that epigenetic changes can be transmitted across generations. Studies in rodents have shown that environmental stressors experienced by parents can produce epigenetic alterations that appear in offspring who were never directly exposed to those stressors. If confirmed in humans, transgenerational epigenetic inheritance would imply that environmental experiences can shape the biology of descendants in ways that neither classical genetics nor Darwinian natural selection fully anticipated.\n\nHowever, the field remains contentious. Critics argue that many transgenerational studies suffer from small sample sizes and fail to rule out confounding factors such as shared environments, maternal behavior, and microbiome transmission. Distinguishing genuine epigenetic inheritance from these alternative mechanisms remains a significant methodological challenge. Nonetheless, the growing body of evidence has prompted a reexamination of the boundary between nature and nurture.",
      "passage_title": "Epigenetics and Environmental Influence on Gene Expression",
      "passage_category": "science",
      "passage_difficulty": 4,
      "estimated_reading_time": 200,
      "paragraphs": [
        "The central dogma of molecular biology\u2014that genetic information flows from DNA to RNA to protein\u2014long suggested that an organism's traits are determined primarily by the nucleotide sequences it inherits. Under this view, environmental factors could select among organisms with different genotypes but could not alter the genetic instructions themselves. The discovery of epigenetic mechanisms has fundamentally complicated this picture.",
        "Epigenetic modifications, such as DNA methylation and histone acetylation, can alter gene expression without changing the underlying DNA sequence. These chemical markers act as molecular switches, turning genes on or off in response to environmental signals. A landmark study of Dutch famine survivors demonstrated that individuals exposed to severe caloric restriction in utero exhibited distinct methylation patterns decades later, with corresponding increases in rates of cardiovascular disease and metabolic disorders.",
        "Perhaps most provocatively, some research suggests that epigenetic changes can be transmitted across generations. Studies in rodents have shown that environmental stressors experienced by parents can produce epigenetic alterations that appear in offspring who were never directly exposed to those stressors. If confirmed in humans, transgenerational epigenetic inheritance would imply that environmental experiences can shape the biology of descendants in ways that neither classical genetics nor Darwinian natural selection fully anticipated.",
        "However, the field remains contentious. Critics argue that many transgenerational studies suffer from small sample sizes and fail to rule out confounding factors such as shared environments, maternal behavior, and microbiome transmission. Distinguishing genuine epigenetic inheritance from these alternative mechanisms remains a significant methodological challenge. Nonetheless, the growing body of evidence has prompted a reexamination of the boundary between nature and nurture."
      ]
    },
    {
      "id": "rc-q-009",
      "passage_id": "rc-passage-003",
      "section": "verbal",
      "subsection": "reading_comprehension",
      "question_type": "function_of_sentence",
      "topic": "science",
      "difficulty": 4,
      "target_solving_time": 100,
      "evidence_paragraphs": [
        2
      ],
      "question_text": "The reference to the Dutch famine survivors primarily serves to",
      "options": [
        "argue that famine conditions are the primary cause of cardiovascular disease",
        "provide concrete evidence that environmental conditions can produce lasting epigenetic changes in humans",
        "contrast European and Asian epigenetic research methodologies",
        "suggest that epigenetic changes are always harmful",
        "demonstrate that DNA methylation is the only epigenetic mechanism"
      ],
      "correct_option_index": 1,
      "explanation": "The Dutch famine study is cited as 'a landmark study' providing concrete evidence that environmental conditions (caloric restriction in utero) produce measurable epigenetic changes (distinct methylation patterns) decades later.",
      "option_explanations": [
        "Too extreme: The passage does not claim famine is the primary cause.",
        "Correct: Concrete evidence linking environment to lasting epigenetic changes.",
        "Not stated: No methodology comparison is made.",
        "Too broad: The passage discusses one harmful example but doesn't generalize.",
        "Not stated: DNA methylation is one mechanism; the passage also mentions histone acetylation."
      ],
      "trap_type": "too_broad",
      "skills": [
        "function_identification",
        "evidence_evaluation"
      ],
      "passage_text": "The central dogma of molecular biology\u2014that genetic information flows from DNA to RNA to protein\u2014long suggested that an organism's traits are determined primarily by the nucleotide sequences it inherits. Under this view, environmental factors could select among organisms with different genotypes but could not alter the genetic instructions themselves. The discovery of epigenetic mechanisms has fundamentally complicated this picture.\n\nEpigenetic modifications, such as DNA methylation and histone acetylation, can alter gene expression without changing the underlying DNA sequence. These chemical markers act as molecular switches, turning genes on or off in response to environmental signals. A landmark study of Dutch famine survivors demonstrated that individuals exposed to severe caloric restriction in utero exhibited distinct methylation patterns decades later, with corresponding increases in rates of cardiovascular disease and metabolic disorders.\n\nPerhaps most provocatively, some research suggests that epigenetic changes can be transmitted across generations. Studies in rodents have shown that environmental stressors experienced by parents can produce epigenetic alterations that appear in offspring who were never directly exposed to those stressors. If confirmed in humans, transgenerational epigenetic inheritance would imply that environmental experiences can shape the biology of descendants in ways that neither classical genetics nor Darwinian natural selection fully anticipated.\n\nHowever, the field remains contentious. Critics argue that many transgenerational studies suffer from small sample sizes and fail to rule out confounding factors such as shared environments, maternal behavior, and microbiome transmission. Distinguishing genuine epigenetic inheritance from these alternative mechanisms remains a significant methodological challenge. Nonetheless, the growing body of evidence has prompted a reexamination of the boundary between nature and nurture.",
      "passage_title": "Epigenetics and Environmental Influence on Gene Expression",
      "passage_category": "science",
      "passage_difficulty": 4,
      "estimated_reading_time": 200,
      "paragraphs": [
        "The central dogma of molecular biology\u2014that genetic information flows from DNA to RNA to protein\u2014long suggested that an organism's traits are determined primarily by the nucleotide sequences it inherits. Under this view, environmental factors could select among organisms with different genotypes but could not alter the genetic instructions themselves. The discovery of epigenetic mechanisms has fundamentally complicated this picture.",
        "Epigenetic modifications, such as DNA methylation and histone acetylation, can alter gene expression without changing the underlying DNA sequence. These chemical markers act as molecular switches, turning genes on or off in response to environmental signals. A landmark study of Dutch famine survivors demonstrated that individuals exposed to severe caloric restriction in utero exhibited distinct methylation patterns decades later, with corresponding increases in rates of cardiovascular disease and metabolic disorders.",
        "Perhaps most provocatively, some research suggests that epigenetic changes can be transmitted across generations. Studies in rodents have shown that environmental stressors experienced by parents can produce epigenetic alterations that appear in offspring who were never directly exposed to those stressors. If confirmed in humans, transgenerational epigenetic inheritance would imply that environmental experiences can shape the biology of descendants in ways that neither classical genetics nor Darwinian natural selection fully anticipated.",
        "However, the field remains contentious. Critics argue that many transgenerational studies suffer from small sample sizes and fail to rule out confounding factors such as shared environments, maternal behavior, and microbiome transmission. Distinguishing genuine epigenetic inheritance from these alternative mechanisms remains a significant methodological challenge. Nonetheless, the growing body of evidence has prompted a reexamination of the boundary between nature and nurture."
      ]
    },
    {
      "id": "rc-q-010",
      "passage_id": "rc-passage-003",
      "section": "verbal",
      "subsection": "reading_comprehension",
      "question_type": "inference",
      "topic": "science",
      "difficulty": 4,
      "target_solving_time": 100,
      "evidence_paragraphs": [
        3,
        4
      ],
      "question_text": "It can be inferred from the passage that the author views transgenerational epigenetic inheritance in humans as",
      "options": [
        "definitively proven by existing research",
        "an intriguing possibility that has not yet been conclusively established",
        "impossible given the current understanding of molecular biology",
        "relevant only to rodent models and not applicable to humans",
        "a theory that has been thoroughly refuted by recent studies"
      ],
      "correct_option_index": 1,
      "explanation": "Paragraph 3 uses 'if confirmed in humans' and 'would imply,' indicating it's a possibility, not established fact. Paragraph 4 notes the field is 'contentious' with methodological challenges. This supports option B.",
      "option_explanations": [
        "Contradicted: 'If confirmed' indicates it's not yet proven.",
        "Correct: The conditional language and ongoing debates support this characterization.",
        "Contradicted: The author presents it as plausible, not impossible.",
        "Contradicted: The author speculates about human implications ('if confirmed in humans').",
        "Contradicted: Critics raise concerns but the theory has not been refuted."
      ],
      "trap_type": "distortion",
      "skills": [
        "inference",
        "authorial_stance"
      ],
      "passage_text": "The central dogma of molecular biology\u2014that genetic information flows from DNA to RNA to protein\u2014long suggested that an organism's traits are determined primarily by the nucleotide sequences it inherits. Under this view, environmental factors could select among organisms with different genotypes but could not alter the genetic instructions themselves. The discovery of epigenetic mechanisms has fundamentally complicated this picture.\n\nEpigenetic modifications, such as DNA methylation and histone acetylation, can alter gene expression without changing the underlying DNA sequence. These chemical markers act as molecular switches, turning genes on or off in response to environmental signals. A landmark study of Dutch famine survivors demonstrated that individuals exposed to severe caloric restriction in utero exhibited distinct methylation patterns decades later, with corresponding increases in rates of cardiovascular disease and metabolic disorders.\n\nPerhaps most provocatively, some research suggests that epigenetic changes can be transmitted across generations. Studies in rodents have shown that environmental stressors experienced by parents can produce epigenetic alterations that appear in offspring who were never directly exposed to those stressors. If confirmed in humans, transgenerational epigenetic inheritance would imply that environmental experiences can shape the biology of descendants in ways that neither classical genetics nor Darwinian natural selection fully anticipated.\n\nHowever, the field remains contentious. Critics argue that many transgenerational studies suffer from small sample sizes and fail to rule out confounding factors such as shared environments, maternal behavior, and microbiome transmission. Distinguishing genuine epigenetic inheritance from these alternative mechanisms remains a significant methodological challenge. Nonetheless, the growing body of evidence has prompted a reexamination of the boundary between nature and nurture.",
      "passage_title": "Epigenetics and Environmental Influence on Gene Expression",
      "passage_category": "science",
      "passage_difficulty": 4,
      "estimated_reading_time": 200,
      "paragraphs": [
        "The central dogma of molecular biology\u2014that genetic information flows from DNA to RNA to protein\u2014long suggested that an organism's traits are determined primarily by the nucleotide sequences it inherits. Under this view, environmental factors could select among organisms with different genotypes but could not alter the genetic instructions themselves. The discovery of epigenetic mechanisms has fundamentally complicated this picture.",
        "Epigenetic modifications, such as DNA methylation and histone acetylation, can alter gene expression without changing the underlying DNA sequence. These chemical markers act as molecular switches, turning genes on or off in response to environmental signals. A landmark study of Dutch famine survivors demonstrated that individuals exposed to severe caloric restriction in utero exhibited distinct methylation patterns decades later, with corresponding increases in rates of cardiovascular disease and metabolic disorders.",
        "Perhaps most provocatively, some research suggests that epigenetic changes can be transmitted across generations. Studies in rodents have shown that environmental stressors experienced by parents can produce epigenetic alterations that appear in offspring who were never directly exposed to those stressors. If confirmed in humans, transgenerational epigenetic inheritance would imply that environmental experiences can shape the biology of descendants in ways that neither classical genetics nor Darwinian natural selection fully anticipated.",
        "However, the field remains contentious. Critics argue that many transgenerational studies suffer from small sample sizes and fail to rule out confounding factors such as shared environments, maternal behavior, and microbiome transmission. Distinguishing genuine epigenetic inheritance from these alternative mechanisms remains a significant methodological challenge. Nonetheless, the growing body of evidence has prompted a reexamination of the boundary between nature and nurture."
      ]
    },
    {
      "id": "rc-q-011",
      "passage_id": "rc-passage-004",
      "section": "verbal",
      "subsection": "reading_comprehension",
      "question_type": "primary_purpose",
      "topic": "technology",
      "difficulty": 3,
      "target_solving_time": 90,
      "evidence_paragraphs": [
        1,
        2,
        3,
        4
      ],
      "question_text": "The primary purpose of the passage is to",
      "options": [
        "argue that AI will inevitably replace radiologists within a decade",
        "examine the promise, obstacles, and practical considerations surrounding AI in medical diagnostics",
        "warn healthcare providers against adopting AI diagnostic tools",
        "compare the accuracy of AI systems with that of human physicians",
        "propose specific regulatory frameworks for AI medical devices"
      ],
      "correct_option_index": 1,
      "explanation": "The passage presents AI diagnostic capabilities (P1), deployment obstacles (P2), liability issues (P3), and future potential (P4). This balanced examination matches option B.",
      "option_explanations": [
        "Too extreme: The passage discusses augmentation, not replacement.",
        "Correct: Balanced coverage of promise, obstacles, and practical considerations.",
        "Too negative: The passage acknowledges significant promise alongside challenges.",
        "Too narrow: Accuracy comparison is one element of P1, not the primary purpose.",
        "Not done: The passage identifies regulatory challenges but doesn't propose frameworks."
      ],
      "trap_type": "too_broad",
      "skills": [
        "primary_purpose",
        "passage_structure"
      ],
      "passage_text": "The application of artificial intelligence to medical diagnostics has generated considerable excitement in the healthcare community. Deep learning algorithms, particularly convolutional neural networks, have demonstrated remarkable accuracy in identifying certain conditions from medical images. In some controlled studies, these systems have matched or exceeded the diagnostic accuracy of experienced radiologists in detecting specific cancers from mammograms and identifying diabetic retinopathy from fundus photographs.\n\nDespite these impressive results, significant obstacles remain before AI diagnostics can be widely deployed in clinical settings. Most AI systems are trained on datasets from specific populations and imaging equipment, raising concerns about performance when applied to patients with different demographic characteristics or when using different hardware. Additionally, the 'black box' nature of deep learning models\u2014where the reasoning behind a diagnosis is not transparent\u2014creates challenges for regulatory approval and physician trust.\n\nThe integration of AI into clinical workflows also requires careful consideration of liability and professional responsibility. If an AI system makes an incorrect diagnosis, the question of whether the physician, the hospital, or the software developer bears responsibility remains legally unsettled. Some healthcare systems have adopted AI as a 'second reader' that flags potential concerns for physician review, rather than as an autonomous diagnostic tool, thereby preserving physician authority and responsibility.\n\nLooking forward, the most promising applications of AI in diagnostics may not be in replacing physicians but in augmenting their capabilities. AI systems that can rapidly screen large volumes of images, prioritize urgent cases, and reduce diagnostic backlogs could improve healthcare access, particularly in underserved regions where specialist physicians are scarce.",
      "passage_title": "Artificial Intelligence in Medical Diagnostics",
      "passage_category": "technology",
      "passage_difficulty": 3,
      "estimated_reading_time": 180,
      "paragraphs": [
        "The application of artificial intelligence to medical diagnostics has generated considerable excitement in the healthcare community. Deep learning algorithms, particularly convolutional neural networks, have demonstrated remarkable accuracy in identifying certain conditions from medical images. In some controlled studies, these systems have matched or exceeded the diagnostic accuracy of experienced radiologists in detecting specific cancers from mammograms and identifying diabetic retinopathy from fundus photographs.",
        "Despite these impressive results, significant obstacles remain before AI diagnostics can be widely deployed in clinical settings. Most AI systems are trained on datasets from specific populations and imaging equipment, raising concerns about performance when applied to patients with different demographic characteristics or when using different hardware. Additionally, the 'black box' nature of deep learning models\u2014where the reasoning behind a diagnosis is not transparent\u2014creates challenges for regulatory approval and physician trust.",
        "The integration of AI into clinical workflows also requires careful consideration of liability and professional responsibility. If an AI system makes an incorrect diagnosis, the question of whether the physician, the hospital, or the software developer bears responsibility remains legally unsettled. Some healthcare systems have adopted AI as a 'second reader' that flags potential concerns for physician review, rather than as an autonomous diagnostic tool, thereby preserving physician authority and responsibility.",
        "Looking forward, the most promising applications of AI in diagnostics may not be in replacing physicians but in augmenting their capabilities. AI systems that can rapidly screen large volumes of images, prioritize urgent cases, and reduce diagnostic backlogs could improve healthcare access, particularly in underserved regions where specialist physicians are scarce."
      ]
    },
    {
      "id": "rc-q-012",
      "passage_id": "rc-passage-004",
      "section": "verbal",
      "subsection": "reading_comprehension",
      "question_type": "detail",
      "topic": "technology",
      "difficulty": 2,
      "target_solving_time": 75,
      "evidence_paragraphs": [
        3
      ],
      "question_text": "According to paragraph 3, some healthcare systems use AI as a 'second reader' in order to",
      "options": [
        "reduce the number of radiologists needed in the department",
        "ensure that the AI system receives adequate training data",
        "preserve physician authority and responsibility while benefiting from AI capabilities",
        "demonstrate to regulators that AI is safe for autonomous deployment",
        "lower the cost of medical malpractice insurance"
      ],
      "correct_option_index": 2,
      "explanation": "Paragraph 3 explains that the 'second reader' approach 'preserv[es] physician authority and responsibility,' using AI to flag concerns for physician review rather than making autonomous diagnoses.",
      "option_explanations": [
        "Not stated: Reducing radiologist numbers is not mentioned as the purpose.",
        "Not stated: Training data collection is not discussed in this context.",
        "Correct: Directly supported by the passage's explanation of the second-reader model.",
        "Not stated: Autonomous deployment is contrasted with, not supported by, this approach.",
        "Not stated: Insurance costs are not discussed."
      ],
      "trap_type": "out_of_scope",
      "skills": [
        "detail_retrieval",
        "purpose_identification"
      ],
      "passage_text": "The application of artificial intelligence to medical diagnostics has generated considerable excitement in the healthcare community. Deep learning algorithms, particularly convolutional neural networks, have demonstrated remarkable accuracy in identifying certain conditions from medical images. In some controlled studies, these systems have matched or exceeded the diagnostic accuracy of experienced radiologists in detecting specific cancers from mammograms and identifying diabetic retinopathy from fundus photographs.\n\nDespite these impressive results, significant obstacles remain before AI diagnostics can be widely deployed in clinical settings. Most AI systems are trained on datasets from specific populations and imaging equipment, raising concerns about performance when applied to patients with different demographic characteristics or when using different hardware. Additionally, the 'black box' nature of deep learning models\u2014where the reasoning behind a diagnosis is not transparent\u2014creates challenges for regulatory approval and physician trust.\n\nThe integration of AI into clinical workflows also requires careful consideration of liability and professional responsibility. If an AI system makes an incorrect diagnosis, the question of whether the physician, the hospital, or the software developer bears responsibility remains legally unsettled. Some healthcare systems have adopted AI as a 'second reader' that flags potential concerns for physician review, rather than as an autonomous diagnostic tool, thereby preserving physician authority and responsibility.\n\nLooking forward, the most promising applications of AI in diagnostics may not be in replacing physicians but in augmenting their capabilities. AI systems that can rapidly screen large volumes of images, prioritize urgent cases, and reduce diagnostic backlogs could improve healthcare access, particularly in underserved regions where specialist physicians are scarce.",
      "passage_title": "Artificial Intelligence in Medical Diagnostics",
      "passage_category": "technology",
      "passage_difficulty": 3,
      "estimated_reading_time": 180,
      "paragraphs": [
        "The application of artificial intelligence to medical diagnostics has generated considerable excitement in the healthcare community. Deep learning algorithms, particularly convolutional neural networks, have demonstrated remarkable accuracy in identifying certain conditions from medical images. In some controlled studies, these systems have matched or exceeded the diagnostic accuracy of experienced radiologists in detecting specific cancers from mammograms and identifying diabetic retinopathy from fundus photographs.",
        "Despite these impressive results, significant obstacles remain before AI diagnostics can be widely deployed in clinical settings. Most AI systems are trained on datasets from specific populations and imaging equipment, raising concerns about performance when applied to patients with different demographic characteristics or when using different hardware. Additionally, the 'black box' nature of deep learning models\u2014where the reasoning behind a diagnosis is not transparent\u2014creates challenges for regulatory approval and physician trust.",
        "The integration of AI into clinical workflows also requires careful consideration of liability and professional responsibility. If an AI system makes an incorrect diagnosis, the question of whether the physician, the hospital, or the software developer bears responsibility remains legally unsettled. Some healthcare systems have adopted AI as a 'second reader' that flags potential concerns for physician review, rather than as an autonomous diagnostic tool, thereby preserving physician authority and responsibility.",
        "Looking forward, the most promising applications of AI in diagnostics may not be in replacing physicians but in augmenting their capabilities. AI systems that can rapidly screen large volumes of images, prioritize urgent cases, and reduce diagnostic backlogs could improve healthcare access, particularly in underserved regions where specialist physicians are scarce."
      ]
    },
    {
      "id": "rc-q-013",
      "passage_id": "rc-passage-004",
      "section": "verbal",
      "subsection": "reading_comprehension",
      "question_type": "inference",
      "topic": "technology",
      "difficulty": 3,
      "target_solving_time": 90,
      "evidence_paragraphs": [
        4
      ],
      "question_text": "The author would most likely agree that AI diagnostic tools",
      "options": [
        "should not be used in any clinical setting until all regulatory questions are resolved",
        "are most valuable when used to complement physician expertise rather than replace it",
        "have already demonstrated sufficient reliability for autonomous clinical use",
        "are primarily beneficial for wealthy healthcare systems with advanced technology",
        "will be rendered obsolete by future medical breakthroughs"
      ],
      "correct_option_index": 1,
      "explanation": "Paragraph 4 states 'the most promising applications may not be in replacing physicians but in augmenting their capabilities,' directly supporting the view that AI should complement, not replace, physicians.",
      "option_explanations": [
        "Too restrictive: The author doesn't suggest waiting until all issues are resolved.",
        "Correct: Directly aligned with the passage's concluding perspective.",
        "Contradicted: P2 discusses obstacles to autonomous use.",
        "Contradicted: P4 specifically mentions benefits for 'underserved regions.'",
        "Unsupported: No such prediction is made."
      ],
      "trap_type": "distortion",
      "skills": [
        "inference",
        "authorial_perspective"
      ],
      "passage_text": "The application of artificial intelligence to medical diagnostics has generated considerable excitement in the healthcare community. Deep learning algorithms, particularly convolutional neural networks, have demonstrated remarkable accuracy in identifying certain conditions from medical images. In some controlled studies, these systems have matched or exceeded the diagnostic accuracy of experienced radiologists in detecting specific cancers from mammograms and identifying diabetic retinopathy from fundus photographs.\n\nDespite these impressive results, significant obstacles remain before AI diagnostics can be widely deployed in clinical settings. Most AI systems are trained on datasets from specific populations and imaging equipment, raising concerns about performance when applied to patients with different demographic characteristics or when using different hardware. Additionally, the 'black box' nature of deep learning models\u2014where the reasoning behind a diagnosis is not transparent\u2014creates challenges for regulatory approval and physician trust.\n\nThe integration of AI into clinical workflows also requires careful consideration of liability and professional responsibility. If an AI system makes an incorrect diagnosis, the question of whether the physician, the hospital, or the software developer bears responsibility remains legally unsettled. Some healthcare systems have adopted AI as a 'second reader' that flags potential concerns for physician review, rather than as an autonomous diagnostic tool, thereby preserving physician authority and responsibility.\n\nLooking forward, the most promising applications of AI in diagnostics may not be in replacing physicians but in augmenting their capabilities. AI systems that can rapidly screen large volumes of images, prioritize urgent cases, and reduce diagnostic backlogs could improve healthcare access, particularly in underserved regions where specialist physicians are scarce.",
      "passage_title": "Artificial Intelligence in Medical Diagnostics",
      "passage_category": "technology",
      "passage_difficulty": 3,
      "estimated_reading_time": 180,
      "paragraphs": [
        "The application of artificial intelligence to medical diagnostics has generated considerable excitement in the healthcare community. Deep learning algorithms, particularly convolutional neural networks, have demonstrated remarkable accuracy in identifying certain conditions from medical images. In some controlled studies, these systems have matched or exceeded the diagnostic accuracy of experienced radiologists in detecting specific cancers from mammograms and identifying diabetic retinopathy from fundus photographs.",
        "Despite these impressive results, significant obstacles remain before AI diagnostics can be widely deployed in clinical settings. Most AI systems are trained on datasets from specific populations and imaging equipment, raising concerns about performance when applied to patients with different demographic characteristics or when using different hardware. Additionally, the 'black box' nature of deep learning models\u2014where the reasoning behind a diagnosis is not transparent\u2014creates challenges for regulatory approval and physician trust.",
        "The integration of AI into clinical workflows also requires careful consideration of liability and professional responsibility. If an AI system makes an incorrect diagnosis, the question of whether the physician, the hospital, or the software developer bears responsibility remains legally unsettled. Some healthcare systems have adopted AI as a 'second reader' that flags potential concerns for physician review, rather than as an autonomous diagnostic tool, thereby preserving physician authority and responsibility.",
        "Looking forward, the most promising applications of AI in diagnostics may not be in replacing physicians but in augmenting their capabilities. AI systems that can rapidly screen large volumes of images, prioritize urgent cases, and reduce diagnostic backlogs could improve healthcare access, particularly in underserved regions where specialist physicians are scarce."
      ]
    },
    {
      "id": "rc-q-014",
      "passage_id": "rc-passage-005",
      "section": "verbal",
      "subsection": "reading_comprehension",
      "question_type": "structure_of_passage",
      "topic": "history",
      "difficulty": 3,
      "target_solving_time": 90,
      "evidence_paragraphs": [
        1,
        2,
        3,
        4
      ],
      "question_text": "Which of the following best describes the organization of the passage?",
      "options": [
        "A problem is identified, a solution is proposed, and the solution's limitations are discussed.",
        "A historical context is established, key developments are traced chronologically, outcomes are assessed, and contemporary relevance is noted.",
        "Two competing theories are presented, evidence for each is evaluated, and one is endorsed.",
        "A phenomenon is described, its causes are analyzed, and future predictions are made.",
        "A controversial claim is stated, objections are raised, and the claim is modified."
      ],
      "correct_option_index": 1,
      "explanation": "P1 establishes context (Industrial Revolution conditions), P2 traces the development of labor movements, P3 assesses legislative outcomes and debates their causes, P4 connects to contemporary relevance. This is a chronological historical narrative.",
      "option_explanations": [
        "Doesn't match: No single solution is proposed.",
        "Correct: Matches the passage's chronological structure from context to contemporary relevance.",
        "Doesn't match: While a debate is mentioned in P3, the passage doesn't endorse one theory.",
        "Doesn't match: The passage discusses historical outcomes, not future predictions.",
        "Doesn't match: No single controversial claim drives the passage."
      ],
      "trap_type": "distortion",
      "skills": [
        "passage_structure",
        "organization"
      ],
      "passage_text": "The Industrial Revolution, which began in Britain in the late eighteenth century, transformed economic production from agrarian and artisan-based systems to factory-centered manufacturing. This shift brought unprecedented economic growth but also created harsh working conditions: twelve- to sixteen-hour workdays, dangerous machinery, child labor, and wages barely sufficient for subsistence. Workers had little bargaining power as individuals, and early attempts at collective action were often met with legal prosecution under laws that treated labor organizing as criminal conspiracy.\n\nThe emergence of organized labor movements in the nineteenth century represented a fundamental shift in the balance of power between workers and employers. Trade unions, initially formed among skilled craftsmen, gradually expanded to include unskilled factory workers. The legal landscape evolved as well: Britain's repeal of the Combination Acts in 1824 and the passage of the Trade Union Act in 1871 progressively legitimized labor organizing. In the United States, the American Federation of Labor, founded in 1886, pursued a strategy of 'pure and simple unionism' focused on wages, hours, and working conditions.\n\nLabor movements achieved significant legislative victories in the early twentieth century, including restrictions on child labor, the establishment of maximum working hours, workplace safety regulations, and the right to collective bargaining. These reforms fundamentally altered the social contract between capital and labor. However, historians debate whether these changes resulted primarily from organized labor's political pressure or from broader social and economic forces, including industrialists' recognition that better-treated workers were more productive.\n\nThe legacy of industrial-era labor movements continues to shape contemporary debates about workers' rights. Issues such as minimum wage levels, workplace automation, and the gig economy echo the fundamental tensions between economic efficiency and worker welfare that defined the original labor struggles. Understanding this history provides essential context for evaluating modern proposals to reform labor markets.",
      "passage_title": "The Industrial Revolution and Labor Movements",
      "passage_category": "history",
      "passage_difficulty": 3,
      "estimated_reading_time": 180,
      "paragraphs": [
        "The Industrial Revolution, which began in Britain in the late eighteenth century, transformed economic production from agrarian and artisan-based systems to factory-centered manufacturing. This shift brought unprecedented economic growth but also created harsh working conditions: twelve- to sixteen-hour workdays, dangerous machinery, child labor, and wages barely sufficient for subsistence. Workers had little bargaining power as individuals, and early attempts at collective action were often met with legal prosecution under laws that treated labor organizing as criminal conspiracy.",
        "The emergence of organized labor movements in the nineteenth century represented a fundamental shift in the balance of power between workers and employers. Trade unions, initially formed among skilled craftsmen, gradually expanded to include unskilled factory workers. The legal landscape evolved as well: Britain's repeal of the Combination Acts in 1824 and the passage of the Trade Union Act in 1871 progressively legitimized labor organizing. In the United States, the American Federation of Labor, founded in 1886, pursued a strategy of 'pure and simple unionism' focused on wages, hours, and working conditions.",
        "Labor movements achieved significant legislative victories in the early twentieth century, including restrictions on child labor, the establishment of maximum working hours, workplace safety regulations, and the right to collective bargaining. These reforms fundamentally altered the social contract between capital and labor. However, historians debate whether these changes resulted primarily from organized labor's political pressure or from broader social and economic forces, including industrialists' recognition that better-treated workers were more productive.",
        "The legacy of industrial-era labor movements continues to shape contemporary debates about workers' rights. Issues such as minimum wage levels, workplace automation, and the gig economy echo the fundamental tensions between economic efficiency and worker welfare that defined the original labor struggles. Understanding this history provides essential context for evaluating modern proposals to reform labor markets."
      ]
    },
    {
      "id": "rc-q-015",
      "passage_id": "rc-passage-005",
      "section": "verbal",
      "subsection": "reading_comprehension",
      "question_type": "relationship_between_ideas",
      "topic": "history",
      "difficulty": 4,
      "target_solving_time": 100,
      "evidence_paragraphs": [
        3
      ],
      "question_text": "The passage presents the debate described in paragraph 3 in order to",
      "options": [
        "argue that industrialists deserve more credit than unions for labor reforms",
        "suggest that the causes of labor reforms are complex and not attributable to a single factor",
        "demonstrate that organized labor was ultimately ineffective in achieving reforms",
        "criticize historians who downplay the role of labor unions",
        "propose a new theory of labor reform based on economic efficiency"
      ],
      "correct_option_index": 1,
      "explanation": "The passage presents the debate between labor pressure and broader forces as an open question, suggesting that the causes are complex and multifaceted rather than attributable to one factor.",
      "option_explanations": [
        "Too one-sided: The passage presents both perspectives without favoring either.",
        "Correct: Captures the nuanced presentation of multiple contributing factors.",
        "Contradicted: The passage credits labor movements with significant victories.",
        "Not the purpose: The passage presents the debate neutrally.",
        "Not done: No new theory is proposed."
      ],
      "trap_type": "too_narrow",
      "skills": [
        "relationship_analysis",
        "authorial_intent"
      ],
      "passage_text": "The Industrial Revolution, which began in Britain in the late eighteenth century, transformed economic production from agrarian and artisan-based systems to factory-centered manufacturing. This shift brought unprecedented economic growth but also created harsh working conditions: twelve- to sixteen-hour workdays, dangerous machinery, child labor, and wages barely sufficient for subsistence. Workers had little bargaining power as individuals, and early attempts at collective action were often met with legal prosecution under laws that treated labor organizing as criminal conspiracy.\n\nThe emergence of organized labor movements in the nineteenth century represented a fundamental shift in the balance of power between workers and employers. Trade unions, initially formed among skilled craftsmen, gradually expanded to include unskilled factory workers. The legal landscape evolved as well: Britain's repeal of the Combination Acts in 1824 and the passage of the Trade Union Act in 1871 progressively legitimized labor organizing. In the United States, the American Federation of Labor, founded in 1886, pursued a strategy of 'pure and simple unionism' focused on wages, hours, and working conditions.\n\nLabor movements achieved significant legislative victories in the early twentieth century, including restrictions on child labor, the establishment of maximum working hours, workplace safety regulations, and the right to collective bargaining. These reforms fundamentally altered the social contract between capital and labor. However, historians debate whether these changes resulted primarily from organized labor's political pressure or from broader social and economic forces, including industrialists' recognition that better-treated workers were more productive.\n\nThe legacy of industrial-era labor movements continues to shape contemporary debates about workers' rights. Issues such as minimum wage levels, workplace automation, and the gig economy echo the fundamental tensions between economic efficiency and worker welfare that defined the original labor struggles. Understanding this history provides essential context for evaluating modern proposals to reform labor markets.",
      "passage_title": "The Industrial Revolution and Labor Movements",
      "passage_category": "history",
      "passage_difficulty": 3,
      "estimated_reading_time": 180,
      "paragraphs": [
        "The Industrial Revolution, which began in Britain in the late eighteenth century, transformed economic production from agrarian and artisan-based systems to factory-centered manufacturing. This shift brought unprecedented economic growth but also created harsh working conditions: twelve- to sixteen-hour workdays, dangerous machinery, child labor, and wages barely sufficient for subsistence. Workers had little bargaining power as individuals, and early attempts at collective action were often met with legal prosecution under laws that treated labor organizing as criminal conspiracy.",
        "The emergence of organized labor movements in the nineteenth century represented a fundamental shift in the balance of power between workers and employers. Trade unions, initially formed among skilled craftsmen, gradually expanded to include unskilled factory workers. The legal landscape evolved as well: Britain's repeal of the Combination Acts in 1824 and the passage of the Trade Union Act in 1871 progressively legitimized labor organizing. In the United States, the American Federation of Labor, founded in 1886, pursued a strategy of 'pure and simple unionism' focused on wages, hours, and working conditions.",
        "Labor movements achieved significant legislative victories in the early twentieth century, including restrictions on child labor, the establishment of maximum working hours, workplace safety regulations, and the right to collective bargaining. These reforms fundamentally altered the social contract between capital and labor. However, historians debate whether these changes resulted primarily from organized labor's political pressure or from broader social and economic forces, including industrialists' recognition that better-treated workers were more productive.",
        "The legacy of industrial-era labor movements continues to shape contemporary debates about workers' rights. Issues such as minimum wage levels, workplace automation, and the gig economy echo the fundamental tensions between economic efficiency and worker welfare that defined the original labor struggles. Understanding this history provides essential context for evaluating modern proposals to reform labor markets."
      ]
    },
    {
      "id": "rc-q-016",
      "passage_id": "rc-passage-005",
      "section": "verbal",
      "subsection": "reading_comprehension",
      "question_type": "application_of_idea",
      "topic": "history",
      "difficulty": 4,
      "target_solving_time": 100,
      "evidence_paragraphs": [
        4
      ],
      "question_text": "Based on the passage, the author would most likely view a contemporary debate about gig economy workers' rights as",
      "options": [
        "irrelevant to the historical labor struggles described in the passage",
        "a modern manifestation of the enduring tension between economic efficiency and worker welfare",
        "evidence that labor movements have completely failed in their mission",
        "a problem that can be solved solely through market forces",
        "a temporary issue that will resolve itself as technology improves"
      ],
      "correct_option_index": 1,
      "explanation": "Paragraph 4 explicitly identifies 'the gig economy' as echoing 'the fundamental tensions between economic efficiency and worker welfare that defined the original labor struggles,' directly supporting option B.",
      "option_explanations": [
        "Contradicted: P4 explicitly connects modern issues to historical struggles.",
        "Correct: Directly supported by P4's identification of contemporary echoes.",
        "Too extreme: The passage notes significant achievements, not complete failure.",
        "Not supported: The passage does not suggest market forces alone are sufficient.",
        "Not supported: No such optimistic prediction is made."
      ],
      "trap_type": "out_of_scope",
      "skills": [
        "application",
        "historical_analogy"
      ],
      "passage_text": "The Industrial Revolution, which began in Britain in the late eighteenth century, transformed economic production from agrarian and artisan-based systems to factory-centered manufacturing. This shift brought unprecedented economic growth but also created harsh working conditions: twelve- to sixteen-hour workdays, dangerous machinery, child labor, and wages barely sufficient for subsistence. Workers had little bargaining power as individuals, and early attempts at collective action were often met with legal prosecution under laws that treated labor organizing as criminal conspiracy.\n\nThe emergence of organized labor movements in the nineteenth century represented a fundamental shift in the balance of power between workers and employers. Trade unions, initially formed among skilled craftsmen, gradually expanded to include unskilled factory workers. The legal landscape evolved as well: Britain's repeal of the Combination Acts in 1824 and the passage of the Trade Union Act in 1871 progressively legitimized labor organizing. In the United States, the American Federation of Labor, founded in 1886, pursued a strategy of 'pure and simple unionism' focused on wages, hours, and working conditions.\n\nLabor movements achieved significant legislative victories in the early twentieth century, including restrictions on child labor, the establishment of maximum working hours, workplace safety regulations, and the right to collective bargaining. These reforms fundamentally altered the social contract between capital and labor. However, historians debate whether these changes resulted primarily from organized labor's political pressure or from broader social and economic forces, including industrialists' recognition that better-treated workers were more productive.\n\nThe legacy of industrial-era labor movements continues to shape contemporary debates about workers' rights. Issues such as minimum wage levels, workplace automation, and the gig economy echo the fundamental tensions between economic efficiency and worker welfare that defined the original labor struggles. Understanding this history provides essential context for evaluating modern proposals to reform labor markets.",
      "passage_title": "The Industrial Revolution and Labor Movements",
      "passage_category": "history",
      "passage_difficulty": 3,
      "estimated_reading_time": 180,
      "paragraphs": [
        "The Industrial Revolution, which began in Britain in the late eighteenth century, transformed economic production from agrarian and artisan-based systems to factory-centered manufacturing. This shift brought unprecedented economic growth but also created harsh working conditions: twelve- to sixteen-hour workdays, dangerous machinery, child labor, and wages barely sufficient for subsistence. Workers had little bargaining power as individuals, and early attempts at collective action were often met with legal prosecution under laws that treated labor organizing as criminal conspiracy.",
        "The emergence of organized labor movements in the nineteenth century represented a fundamental shift in the balance of power between workers and employers. Trade unions, initially formed among skilled craftsmen, gradually expanded to include unskilled factory workers. The legal landscape evolved as well: Britain's repeal of the Combination Acts in 1824 and the passage of the Trade Union Act in 1871 progressively legitimized labor organizing. In the United States, the American Federation of Labor, founded in 1886, pursued a strategy of 'pure and simple unionism' focused on wages, hours, and working conditions.",
        "Labor movements achieved significant legislative victories in the early twentieth century, including restrictions on child labor, the establishment of maximum working hours, workplace safety regulations, and the right to collective bargaining. These reforms fundamentally altered the social contract between capital and labor. However, historians debate whether these changes resulted primarily from organized labor's political pressure or from broader social and economic forces, including industrialists' recognition that better-treated workers were more productive.",
        "The legacy of industrial-era labor movements continues to shape contemporary debates about workers' rights. Issues such as minimum wage levels, workplace automation, and the gig economy echo the fundamental tensions between economic efficiency and worker welfare that defined the original labor struggles. Understanding this history provides essential context for evaluating modern proposals to reform labor markets."
      ]
    },
    {
      "id": "rc-q-017",
      "passage_id": "rc-passage-006",
      "section": "verbal",
      "subsection": "reading_comprehension",
      "question_type": "primary_purpose",
      "topic": "social_science",
      "difficulty": 3,
      "target_solving_time": 90,
      "evidence_paragraphs": [
        1,
        2,
        3,
        4
      ],
      "question_text": "The primary purpose of the passage is to",
      "options": [
        "argue that nudging is the most effective public policy tool available to governments",
        "provide an overview of nudge-based policy design, including its theoretical basis, applications, criticisms, and growing adoption",
        "contrast behavioral economics with classical economic theory",
        "demonstrate that automatic enrollment in retirement plans is the best nudge ever designed",
        "warn governments against the unintended consequences of nudge policies"
      ],
      "correct_option_index": 1,
      "explanation": "The passage provides a balanced overview: theoretical background (P1-P2), criticisms (P3), and global adoption (P4). It neither advocates exclusively nor warns against nudging.",
      "option_explanations": [
        "Too one-sided: The passage presents criticisms as well.",
        "Correct: Captures the balanced, comprehensive overview.",
        "Too narrow: The contrast is context, not the primary purpose.",
        "Too narrow: Retirement enrollment is one example, not the focus.",
        "Too negative: The passage also discusses benefits and adoption."
      ],
      "trap_type": "too_narrow",
      "skills": [
        "primary_purpose",
        "balanced_assessment"
      ],
      "passage_text": "Traditional economic policy assumes that individuals make rational decisions when provided with accurate information. Under this framework, the role of government is to ensure transparency\u2014clear labeling, accessible data, fair markets\u2014and then step back, trusting citizens to act in their own best interest. Behavioral economics, drawing on decades of psychological research, challenges this assumption by documenting systematic cognitive biases that cause people to make choices inconsistent with their own stated preferences.\n\nThe concept of 'nudging,' popularized by Richard Thaler and Cass Sunstein, proposes that policy designers can improve outcomes by structuring choice environments to account for these biases without restricting options. The most widely cited example is automatic enrollment in retirement savings plans: when employees must opt out rather than opt in, participation rates increase dramatically, from roughly 50 percent to over 90 percent in many organizations. The choice to save remains entirely voluntary, but the default option is changed to align with what most employees say they want.\n\nCritics of nudging raise both practical and philosophical concerns. On the practical side, nudges that work in laboratory settings may produce smaller effects in complex real-world environments. On the philosophical side, some argue that nudging represents a form of paternalism that undermines individual autonomy, even when the intent is benevolent. Who determines what constitutes a 'better' choice, and by what criteria? These questions become particularly contentious when governments apply nudging to sensitive domains such as healthcare decisions or dietary choices.\n\nDespite these critiques, nudge-based policies have proliferated globally. The UK's Behavioural Insights Team, established in 2010, has implemented nudges across tax compliance, energy conservation, and public health. The approach's appeal lies in its cost-effectiveness: nudges typically require minimal expenditure compared to traditional regulatory or incentive-based interventions, while producing measurable behavioral change.",
      "passage_title": "Behavioral Nudges and Public Policy Design",
      "passage_category": "social_science",
      "passage_difficulty": 3,
      "estimated_reading_time": 180,
      "paragraphs": [
        "Traditional economic policy assumes that individuals make rational decisions when provided with accurate information. Under this framework, the role of government is to ensure transparency\u2014clear labeling, accessible data, fair markets\u2014and then step back, trusting citizens to act in their own best interest. Behavioral economics, drawing on decades of psychological research, challenges this assumption by documenting systematic cognitive biases that cause people to make choices inconsistent with their own stated preferences.",
        "The concept of 'nudging,' popularized by Richard Thaler and Cass Sunstein, proposes that policy designers can improve outcomes by structuring choice environments to account for these biases without restricting options. The most widely cited example is automatic enrollment in retirement savings plans: when employees must opt out rather than opt in, participation rates increase dramatically, from roughly 50 percent to over 90 percent in many organizations. The choice to save remains entirely voluntary, but the default option is changed to align with what most employees say they want.",
        "Critics of nudging raise both practical and philosophical concerns. On the practical side, nudges that work in laboratory settings may produce smaller effects in complex real-world environments. On the philosophical side, some argue that nudging represents a form of paternalism that undermines individual autonomy, even when the intent is benevolent. Who determines what constitutes a 'better' choice, and by what criteria? These questions become particularly contentious when governments apply nudging to sensitive domains such as healthcare decisions or dietary choices.",
        "Despite these critiques, nudge-based policies have proliferated globally. The UK's Behavioural Insights Team, established in 2010, has implemented nudges across tax compliance, energy conservation, and public health. The approach's appeal lies in its cost-effectiveness: nudges typically require minimal expenditure compared to traditional regulatory or incentive-based interventions, while producing measurable behavioral change."
      ]
    },
    {
      "id": "rc-q-018",
      "passage_id": "rc-passage-006",
      "section": "verbal",
      "subsection": "reading_comprehension",
      "question_type": "detail",
      "topic": "social_science",
      "difficulty": 2,
      "target_solving_time": 75,
      "evidence_paragraphs": [
        2
      ],
      "question_text": "According to the passage, automatic enrollment in retirement savings plans is an effective nudge because",
      "options": [
        "it forces employees to save a minimum percentage of their salary",
        "it provides financial incentives for retirement saving",
        "it changes the default option to align with what most employees say they want",
        "it restricts employees' ability to withdraw their savings early",
        "it requires employers to match employee contributions"
      ],
      "correct_option_index": 2,
      "explanation": "P2 states that 'the default option is changed to align with what most employees say they want' while keeping the choice 'entirely voluntary.'",
      "option_explanations": [
        "Contradicted: The passage says the choice remains voluntary.",
        "Not stated: Financial incentives are not mentioned.",
        "Correct: Directly stated in paragraph 2.",
        "Not stated: Withdrawal restrictions are not discussed.",
        "Not stated: Employer matching is not mentioned."
      ],
      "trap_type": "distortion",
      "skills": [
        "detail_retrieval"
      ],
      "passage_text": "Traditional economic policy assumes that individuals make rational decisions when provided with accurate information. Under this framework, the role of government is to ensure transparency\u2014clear labeling, accessible data, fair markets\u2014and then step back, trusting citizens to act in their own best interest. Behavioral economics, drawing on decades of psychological research, challenges this assumption by documenting systematic cognitive biases that cause people to make choices inconsistent with their own stated preferences.\n\nThe concept of 'nudging,' popularized by Richard Thaler and Cass Sunstein, proposes that policy designers can improve outcomes by structuring choice environments to account for these biases without restricting options. The most widely cited example is automatic enrollment in retirement savings plans: when employees must opt out rather than opt in, participation rates increase dramatically, from roughly 50 percent to over 90 percent in many organizations. The choice to save remains entirely voluntary, but the default option is changed to align with what most employees say they want.\n\nCritics of nudging raise both practical and philosophical concerns. On the practical side, nudges that work in laboratory settings may produce smaller effects in complex real-world environments. On the philosophical side, some argue that nudging represents a form of paternalism that undermines individual autonomy, even when the intent is benevolent. Who determines what constitutes a 'better' choice, and by what criteria? These questions become particularly contentious when governments apply nudging to sensitive domains such as healthcare decisions or dietary choices.\n\nDespite these critiques, nudge-based policies have proliferated globally. The UK's Behavioural Insights Team, established in 2010, has implemented nudges across tax compliance, energy conservation, and public health. The approach's appeal lies in its cost-effectiveness: nudges typically require minimal expenditure compared to traditional regulatory or incentive-based interventions, while producing measurable behavioral change.",
      "passage_title": "Behavioral Nudges and Public Policy Design",
      "passage_category": "social_science",
      "passage_difficulty": 3,
      "estimated_reading_time": 180,
      "paragraphs": [
        "Traditional economic policy assumes that individuals make rational decisions when provided with accurate information. Under this framework, the role of government is to ensure transparency\u2014clear labeling, accessible data, fair markets\u2014and then step back, trusting citizens to act in their own best interest. Behavioral economics, drawing on decades of psychological research, challenges this assumption by documenting systematic cognitive biases that cause people to make choices inconsistent with their own stated preferences.",
        "The concept of 'nudging,' popularized by Richard Thaler and Cass Sunstein, proposes that policy designers can improve outcomes by structuring choice environments to account for these biases without restricting options. The most widely cited example is automatic enrollment in retirement savings plans: when employees must opt out rather than opt in, participation rates increase dramatically, from roughly 50 percent to over 90 percent in many organizations. The choice to save remains entirely voluntary, but the default option is changed to align with what most employees say they want.",
        "Critics of nudging raise both practical and philosophical concerns. On the practical side, nudges that work in laboratory settings may produce smaller effects in complex real-world environments. On the philosophical side, some argue that nudging represents a form of paternalism that undermines individual autonomy, even when the intent is benevolent. Who determines what constitutes a 'better' choice, and by what criteria? These questions become particularly contentious when governments apply nudging to sensitive domains such as healthcare decisions or dietary choices.",
        "Despite these critiques, nudge-based policies have proliferated globally. The UK's Behavioural Insights Team, established in 2010, has implemented nudges across tax compliance, energy conservation, and public health. The approach's appeal lies in its cost-effectiveness: nudges typically require minimal expenditure compared to traditional regulatory or incentive-based interventions, while producing measurable behavioral change."
      ]
    },
    {
      "id": "rc-q-019",
      "passage_id": "rc-passage-007",
      "section": "verbal",
      "subsection": "reading_comprehension",
      "question_type": "main_idea",
      "topic": "environment",
      "difficulty": 3,
      "target_solving_time": 90,
      "evidence_paragraphs": [
        1,
        2,
        3,
        4
      ],
      "question_text": "Which of the following best expresses the main idea of the passage?",
      "options": [
        "Ocean acidification is caused by industrial pollution of waterways.",
        "Human CO2 emissions are causing ocean acidification that threatens marine ecosystems, and meaningful solutions require global emissions reductions.",
        "Coral reefs will be completely destroyed within the next decade.",
        "Local interventions such as adding alkaline minerals are the best solution to ocean acidification.",
        "The ocean's ability to absorb carbon dioxide will eliminate the threat of atmospheric warming."
      ],
      "correct_option_index": 1,
      "explanation": "The passage explains the mechanism (P1), impacts (P2-P3), and solutions (P4) of ocean acidification, emphasizing that global CO2 reduction is the credible path forward.",
      "option_explanations": [
        "Inaccurate: The cause is atmospheric CO2 absorption, not direct pollution.",
        "Correct: Captures the cause, threat, and solution arc of the passage.",
        "Too extreme and unsupported: No timeline for complete destruction is given.",
        "Contradicted: P4 says such approaches are 'impractical as a global solution.'",
        "Contradicted: P1 notes that absorption comes 'at a significant cost' to marine chemistry."
      ],
      "trap_type": "distortion",
      "skills": [
        "main_idea",
        "synthesis"
      ],
      "passage_text": "The world's oceans absorb approximately 30 percent of the carbon dioxide released into the atmosphere by human activities. While this absorption has moderated the pace of atmospheric warming, it has come at a significant cost to marine chemistry. When carbon dioxide dissolves in seawater, it forms carbonic acid, which releases hydrogen ions that lower the water's pH. Since the beginning of the industrial era, ocean surface pH has decreased by approximately 0.1 units, representing a 26 percent increase in acidity.\n\nThis shift in ocean chemistry poses a direct threat to marine organisms that build shells or skeletons from calcium carbonate, including corals, mollusks, and certain plankton species. As acidity increases, the concentration of carbonate ions\u2014essential building blocks for these structures\u2014decreases, making it progressively more difficult and energetically costly for organisms to form and maintain their protective shells. Laboratory experiments have demonstrated that many calcifying species exhibit reduced growth rates, thinner shells, and higher mortality when exposed to projected future pH levels.\n\nThe ecological implications extend far beyond calcifying organisms. Coral reefs, which support an estimated 25 percent of all marine species despite covering less than 1 percent of the ocean floor, are particularly vulnerable. Reef degradation threatens the complex food webs and biodiversity hotspots that depend on coral structures. Pteropods, tiny swimming snails that form a critical component of polar food chains, have already shown signs of shell dissolution in Antarctic waters where acidification is most advanced.\n\nAddressing ocean acidification ultimately requires reducing atmospheric carbon dioxide concentrations, as the ocean's chemistry will continue to shift as long as excess CO2 persists in the atmosphere. Some researchers have proposed local interventions, such as adding alkaline minerals to coastal waters, but the scale of the ocean makes such approaches impractical as a global solution. International agreements to limit carbon emissions remain the most scientifically credible path to slowing ocean acidification, though the ocean's response to reduced emissions will be measured in decades, not years.",
      "passage_title": "Ocean Acidification and Marine Ecosystems",
      "passage_category": "environment",
      "passage_difficulty": 4,
      "estimated_reading_time": 190,
      "paragraphs": [
        "The world's oceans absorb approximately 30 percent of the carbon dioxide released into the atmosphere by human activities. While this absorption has moderated the pace of atmospheric warming, it has come at a significant cost to marine chemistry. When carbon dioxide dissolves in seawater, it forms carbonic acid, which releases hydrogen ions that lower the water's pH. Since the beginning of the industrial era, ocean surface pH has decreased by approximately 0.1 units, representing a 26 percent increase in acidity.",
        "This shift in ocean chemistry poses a direct threat to marine organisms that build shells or skeletons from calcium carbonate, including corals, mollusks, and certain plankton species. As acidity increases, the concentration of carbonate ions\u2014essential building blocks for these structures\u2014decreases, making it progressively more difficult and energetically costly for organisms to form and maintain their protective shells. Laboratory experiments have demonstrated that many calcifying species exhibit reduced growth rates, thinner shells, and higher mortality when exposed to projected future pH levels.",
        "The ecological implications extend far beyond calcifying organisms. Coral reefs, which support an estimated 25 percent of all marine species despite covering less than 1 percent of the ocean floor, are particularly vulnerable. Reef degradation threatens the complex food webs and biodiversity hotspots that depend on coral structures. Pteropods, tiny swimming snails that form a critical component of polar food chains, have already shown signs of shell dissolution in Antarctic waters where acidification is most advanced.",
        "Addressing ocean acidification ultimately requires reducing atmospheric carbon dioxide concentrations, as the ocean's chemistry will continue to shift as long as excess CO2 persists in the atmosphere. Some researchers have proposed local interventions, such as adding alkaline minerals to coastal waters, but the scale of the ocean makes such approaches impractical as a global solution. International agreements to limit carbon emissions remain the most scientifically credible path to slowing ocean acidification, though the ocean's response to reduced emissions will be measured in decades, not years."
      ]
    },
    {
      "id": "rc-q-020",
      "passage_id": "rc-passage-007",
      "section": "verbal",
      "subsection": "reading_comprehension",
      "question_type": "strengthen_weaken",
      "topic": "environment",
      "difficulty": 4,
      "target_solving_time": 100,
      "evidence_paragraphs": [
        2,
        3
      ],
      "question_text": "Which of the following, if true, would most strengthen the passage's claim about the threat to marine ecosystems?",
      "options": [
        "Some fish species have shown the ability to adapt to slightly lower pH levels over multiple generations.",
        "A recent study found that reduced carbonate ion availability has already caused a measurable decline in commercial shellfish populations along several coastlines.",
        "Ocean temperatures have also increased significantly over the past century.",
        "The tourism industry generates significant revenue from coral reef destinations.",
        "Some species of algae actually benefit from increased carbon dioxide levels."
      ],
      "correct_option_index": 1,
      "explanation": "The passage discusses threats to calcifying organisms. Real-world evidence of actual shellfish population decline directly strengthens the claim that acidification threatens marine ecosystems.",
      "option_explanations": [
        "Weakens: Fish adaptation would reduce the severity of the threat.",
        "Correct: Direct real-world evidence supporting the threat claim.",
        "Relevant but doesn't specifically address acidification's impact on marine ecosystems.",
        "Irrelevant: Tourism revenue doesn't strengthen the ecological threat claim.",
        "Weakens: Algae benefits would partially offset the threat."
      ],
      "trap_type": "out_of_scope",
      "skills": [
        "strengthen_weaken",
        "evidence_evaluation"
      ],
      "passage_text": "The world's oceans absorb approximately 30 percent of the carbon dioxide released into the atmosphere by human activities. While this absorption has moderated the pace of atmospheric warming, it has come at a significant cost to marine chemistry. When carbon dioxide dissolves in seawater, it forms carbonic acid, which releases hydrogen ions that lower the water's pH. Since the beginning of the industrial era, ocean surface pH has decreased by approximately 0.1 units, representing a 26 percent increase in acidity.\n\nThis shift in ocean chemistry poses a direct threat to marine organisms that build shells or skeletons from calcium carbonate, including corals, mollusks, and certain plankton species. As acidity increases, the concentration of carbonate ions\u2014essential building blocks for these structures\u2014decreases, making it progressively more difficult and energetically costly for organisms to form and maintain their protective shells. Laboratory experiments have demonstrated that many calcifying species exhibit reduced growth rates, thinner shells, and higher mortality when exposed to projected future pH levels.\n\nThe ecological implications extend far beyond calcifying organisms. Coral reefs, which support an estimated 25 percent of all marine species despite covering less than 1 percent of the ocean floor, are particularly vulnerable. Reef degradation threatens the complex food webs and biodiversity hotspots that depend on coral structures. Pteropods, tiny swimming snails that form a critical component of polar food chains, have already shown signs of shell dissolution in Antarctic waters where acidification is most advanced.\n\nAddressing ocean acidification ultimately requires reducing atmospheric carbon dioxide concentrations, as the ocean's chemistry will continue to shift as long as excess CO2 persists in the atmosphere. Some researchers have proposed local interventions, such as adding alkaline minerals to coastal waters, but the scale of the ocean makes such approaches impractical as a global solution. International agreements to limit carbon emissions remain the most scientifically credible path to slowing ocean acidification, though the ocean's response to reduced emissions will be measured in decades, not years.",
      "passage_title": "Ocean Acidification and Marine Ecosystems",
      "passage_category": "environment",
      "passage_difficulty": 4,
      "estimated_reading_time": 190,
      "paragraphs": [
        "The world's oceans absorb approximately 30 percent of the carbon dioxide released into the atmosphere by human activities. While this absorption has moderated the pace of atmospheric warming, it has come at a significant cost to marine chemistry. When carbon dioxide dissolves in seawater, it forms carbonic acid, which releases hydrogen ions that lower the water's pH. Since the beginning of the industrial era, ocean surface pH has decreased by approximately 0.1 units, representing a 26 percent increase in acidity.",
        "This shift in ocean chemistry poses a direct threat to marine organisms that build shells or skeletons from calcium carbonate, including corals, mollusks, and certain plankton species. As acidity increases, the concentration of carbonate ions\u2014essential building blocks for these structures\u2014decreases, making it progressively more difficult and energetically costly for organisms to form and maintain their protective shells. Laboratory experiments have demonstrated that many calcifying species exhibit reduced growth rates, thinner shells, and higher mortality when exposed to projected future pH levels.",
        "The ecological implications extend far beyond calcifying organisms. Coral reefs, which support an estimated 25 percent of all marine species despite covering less than 1 percent of the ocean floor, are particularly vulnerable. Reef degradation threatens the complex food webs and biodiversity hotspots that depend on coral structures. Pteropods, tiny swimming snails that form a critical component of polar food chains, have already shown signs of shell dissolution in Antarctic waters where acidification is most advanced.",
        "Addressing ocean acidification ultimately requires reducing atmospheric carbon dioxide concentrations, as the ocean's chemistry will continue to shift as long as excess CO2 persists in the atmosphere. Some researchers have proposed local interventions, such as adding alkaline minerals to coastal waters, but the scale of the ocean makes such approaches impractical as a global solution. International agreements to limit carbon emissions remain the most scientifically credible path to slowing ocean acidification, though the ocean's response to reduced emissions will be measured in decades, not years."
      ]
    },
    {
      "id": "rc-q-021",
      "passage_id": "rc-passage-007",
      "section": "verbal",
      "subsection": "reading_comprehension",
      "question_type": "detail",
      "topic": "environment",
      "difficulty": 2,
      "target_solving_time": 75,
      "evidence_paragraphs": [
        1
      ],
      "question_text": "According to the passage, since the industrial era, ocean surface pH has",
      "options": [
        "increased by 0.1 units",
        "decreased by 0.1 units, representing a 26 percent increase in acidity",
        "remained essentially stable despite increased CO2 emissions",
        "decreased by 26 percent",
        "fluctuated unpredictably due to ocean currents"
      ],
      "correct_option_index": 1,
      "explanation": "Paragraph 1 directly states: 'ocean surface pH has decreased by approximately 0.1 units, representing a 26 percent increase in acidity.'",
      "option_explanations": [
        "Reversed: pH decreased, not increased.",
        "Correct: Directly stated in paragraph 1.",
        "Contradicted: Significant change is documented.",
        "Distortion: pH decreased by 0.1 units; acidity increased 26%.",
        "Not stated: Unpredictable fluctuation is not discussed."
      ],
      "trap_type": "distortion",
      "skills": [
        "detail_retrieval"
      ],
      "passage_text": "The world's oceans absorb approximately 30 percent of the carbon dioxide released into the atmosphere by human activities. While this absorption has moderated the pace of atmospheric warming, it has come at a significant cost to marine chemistry. When carbon dioxide dissolves in seawater, it forms carbonic acid, which releases hydrogen ions that lower the water's pH. Since the beginning of the industrial era, ocean surface pH has decreased by approximately 0.1 units, representing a 26 percent increase in acidity.\n\nThis shift in ocean chemistry poses a direct threat to marine organisms that build shells or skeletons from calcium carbonate, including corals, mollusks, and certain plankton species. As acidity increases, the concentration of carbonate ions\u2014essential building blocks for these structures\u2014decreases, making it progressively more difficult and energetically costly for organisms to form and maintain their protective shells. Laboratory experiments have demonstrated that many calcifying species exhibit reduced growth rates, thinner shells, and higher mortality when exposed to projected future pH levels.\n\nThe ecological implications extend far beyond calcifying organisms. Coral reefs, which support an estimated 25 percent of all marine species despite covering less than 1 percent of the ocean floor, are particularly vulnerable. Reef degradation threatens the complex food webs and biodiversity hotspots that depend on coral structures. Pteropods, tiny swimming snails that form a critical component of polar food chains, have already shown signs of shell dissolution in Antarctic waters where acidification is most advanced.\n\nAddressing ocean acidification ultimately requires reducing atmospheric carbon dioxide concentrations, as the ocean's chemistry will continue to shift as long as excess CO2 persists in the atmosphere. Some researchers have proposed local interventions, such as adding alkaline minerals to coastal waters, but the scale of the ocean makes such approaches impractical as a global solution. International agreements to limit carbon emissions remain the most scientifically credible path to slowing ocean acidification, though the ocean's response to reduced emissions will be measured in decades, not years.",
      "passage_title": "Ocean Acidification and Marine Ecosystems",
      "passage_category": "environment",
      "passage_difficulty": 4,
      "estimated_reading_time": 190,
      "paragraphs": [
        "The world's oceans absorb approximately 30 percent of the carbon dioxide released into the atmosphere by human activities. While this absorption has moderated the pace of atmospheric warming, it has come at a significant cost to marine chemistry. When carbon dioxide dissolves in seawater, it forms carbonic acid, which releases hydrogen ions that lower the water's pH. Since the beginning of the industrial era, ocean surface pH has decreased by approximately 0.1 units, representing a 26 percent increase in acidity.",
        "This shift in ocean chemistry poses a direct threat to marine organisms that build shells or skeletons from calcium carbonate, including corals, mollusks, and certain plankton species. As acidity increases, the concentration of carbonate ions\u2014essential building blocks for these structures\u2014decreases, making it progressively more difficult and energetically costly for organisms to form and maintain their protective shells. Laboratory experiments have demonstrated that many calcifying species exhibit reduced growth rates, thinner shells, and higher mortality when exposed to projected future pH levels.",
        "The ecological implications extend far beyond calcifying organisms. Coral reefs, which support an estimated 25 percent of all marine species despite covering less than 1 percent of the ocean floor, are particularly vulnerable. Reef degradation threatens the complex food webs and biodiversity hotspots that depend on coral structures. Pteropods, tiny swimming snails that form a critical component of polar food chains, have already shown signs of shell dissolution in Antarctic waters where acidification is most advanced.",
        "Addressing ocean acidification ultimately requires reducing atmospheric carbon dioxide concentrations, as the ocean's chemistry will continue to shift as long as excess CO2 persists in the atmosphere. Some researchers have proposed local interventions, such as adding alkaline minerals to coastal waters, but the scale of the ocean makes such approaches impractical as a global solution. International agreements to limit carbon emissions remain the most scientifically credible path to slowing ocean acidification, though the ocean's response to reduced emissions will be measured in decades, not years."
      ]
    },
    {
      "id": "rc-q-022",
      "passage_id": "rc-passage-008",
      "section": "verbal",
      "subsection": "reading_comprehension",
      "question_type": "authors_attitude",
      "topic": "arts_and_culture",
      "difficulty": 3,
      "target_solving_time": 90,
      "evidence_paragraphs": [
        1,
        2,
        3,
        4
      ],
      "question_text": "The author's attitude toward modernist architecture's social ambitions can best be described as",
      "options": [
        "wholly admiring and uncritical",
        "contemptuous and dismissive",
        "appreciative of the underlying ideals while acknowledging significant failures in execution",
        "indifferent to both the ideals and their outcomes",
        "primarily focused on the aesthetic achievements rather than social goals"
      ],
      "correct_option_index": 2,
      "explanation": "The author describes modernism's democratic aspirations positively (P1-P2) but honestly acknowledges implementation failures (P3) and notes that contemporary architecture has evolved while preserving the core ideal (P4). This is balanced appreciation with acknowledged shortcomings.",
      "option_explanations": [
        "Contradicted: P3 discusses significant failures.",
        "Contradicted: P4 affirms modernism's enduring contribution.",
        "Correct: Balanced appreciation of ideals with honest assessment of failures.",
        "Contradicted: The passage engages substantively with both ideals and outcomes.",
        "Contradicted: The passage focuses primarily on social goals, not aesthetics."
      ],
      "trap_type": "too_broad",
      "skills": [
        "authorial_attitude",
        "tone_analysis"
      ],
      "passage_text": "The modernist movement in architecture, which emerged in the early twentieth century, sought to break decisively with historical styles and embrace the possibilities of new materials and construction techniques. Architects such as Le Corbusier, Ludwig Mies van der Rohe, and Walter Gropius championed designs characterized by clean lines, open floor plans, and the honest expression of structural materials like steel, concrete, and glass. Their ambition extended beyond aesthetics: modernism aspired to solve social problems through design, creating functional, affordable housing and public spaces accessible to all social classes.\n\nThis democratic impulse was perhaps most clearly expressed in social housing projects of the mid-twentieth century. Le Corbusier's Unit\u00e9 d'Habitation in Marseille, completed in 1952, was designed as a self-contained community providing apartments, shops, recreational facilities, and a rooftop kindergarten within a single concrete structure. The building embodied the modernist belief that thoughtful design could improve quality of life for working-class residents by integrating housing with community services.\n\nHowever, the social ambitions of modernist architecture frequently collided with the realities of implementation. Large-scale housing projects, particularly in the United States and Britain, often suffered from poor construction quality, inadequate maintenance, and a failure to account for residents' social and cultural needs. The Pruitt-Igoe housing complex in St. Louis, designed according to modernist principles and demolished just two decades after its construction, became an emblem of modernism's perceived failure to deliver on its social promises.\n\nContemporary architecture has largely moved beyond the rigid doctrines of high modernism while preserving its democratic aspirations. Architects increasingly engage with communities in the design process, incorporate cultural and contextual considerations, and blend modern materials with local building traditions. This evolution suggests that modernism's most enduring contribution may not be a specific aesthetic but rather the conviction that architecture bears social responsibility.",
      "passage_title": "Modernism in Architecture and the Democratization of Space",
      "passage_category": "arts_and_culture",
      "passage_difficulty": 3,
      "estimated_reading_time": 180,
      "paragraphs": [
        "The modernist movement in architecture, which emerged in the early twentieth century, sought to break decisively with historical styles and embrace the possibilities of new materials and construction techniques. Architects such as Le Corbusier, Ludwig Mies van der Rohe, and Walter Gropius championed designs characterized by clean lines, open floor plans, and the honest expression of structural materials like steel, concrete, and glass. Their ambition extended beyond aesthetics: modernism aspired to solve social problems through design, creating functional, affordable housing and public spaces accessible to all social classes.",
        "This democratic impulse was perhaps most clearly expressed in social housing projects of the mid-twentieth century. Le Corbusier's Unit\u00e9 d'Habitation in Marseille, completed in 1952, was designed as a self-contained community providing apartments, shops, recreational facilities, and a rooftop kindergarten within a single concrete structure. The building embodied the modernist belief that thoughtful design could improve quality of life for working-class residents by integrating housing with community services.",
        "However, the social ambitions of modernist architecture frequently collided with the realities of implementation. Large-scale housing projects, particularly in the United States and Britain, often suffered from poor construction quality, inadequate maintenance, and a failure to account for residents' social and cultural needs. The Pruitt-Igoe housing complex in St. Louis, designed according to modernist principles and demolished just two decades after its construction, became an emblem of modernism's perceived failure to deliver on its social promises.",
        "Contemporary architecture has largely moved beyond the rigid doctrines of high modernism while preserving its democratic aspirations. Architects increasingly engage with communities in the design process, incorporate cultural and contextual considerations, and blend modern materials with local building traditions. This evolution suggests that modernism's most enduring contribution may not be a specific aesthetic but rather the conviction that architecture bears social responsibility."
      ]
    },
    {
      "id": "rc-q-023",
      "passage_id": "rc-passage-008",
      "section": "verbal",
      "subsection": "reading_comprehension",
      "question_type": "function_of_paragraph",
      "topic": "arts_and_culture",
      "difficulty": 3,
      "target_solving_time": 90,
      "evidence_paragraphs": [
        3
      ],
      "question_text": "Paragraph 3 primarily serves to",
      "options": [
        "celebrate the architectural achievements of the modernist movement",
        "argue that all modernist housing projects were unsuccessful",
        "present the gap between modernist social ambitions and implementation realities",
        "compare American and British approaches to social housing",
        "explain the engineering reasons why modernist buildings failed structurally"
      ],
      "correct_option_index": 2,
      "explanation": "P3 discusses how modernism's social ambitions 'collided with the realities of implementation,' using Pruitt-Igoe as an example of perceived failure. It presents the gap between vision and reality.",
      "option_explanations": [
        "Contradicted: P3 discusses failures, not celebrations.",
        "Too extreme: 'All' is not stated; specific failures are cited.",
        "Correct: Captures the paragraph's focus on the ambition-reality gap.",
        "Not the purpose: Both countries are mentioned briefly but not compared.",
        "Not discussed: Engineering failure reasons are not explained."
      ],
      "trap_type": "too_broad",
      "skills": [
        "paragraph_function",
        "critical_reading"
      ],
      "passage_text": "The modernist movement in architecture, which emerged in the early twentieth century, sought to break decisively with historical styles and embrace the possibilities of new materials and construction techniques. Architects such as Le Corbusier, Ludwig Mies van der Rohe, and Walter Gropius championed designs characterized by clean lines, open floor plans, and the honest expression of structural materials like steel, concrete, and glass. Their ambition extended beyond aesthetics: modernism aspired to solve social problems through design, creating functional, affordable housing and public spaces accessible to all social classes.\n\nThis democratic impulse was perhaps most clearly expressed in social housing projects of the mid-twentieth century. Le Corbusier's Unit\u00e9 d'Habitation in Marseille, completed in 1952, was designed as a self-contained community providing apartments, shops, recreational facilities, and a rooftop kindergarten within a single concrete structure. The building embodied the modernist belief that thoughtful design could improve quality of life for working-class residents by integrating housing with community services.\n\nHowever, the social ambitions of modernist architecture frequently collided with the realities of implementation. Large-scale housing projects, particularly in the United States and Britain, often suffered from poor construction quality, inadequate maintenance, and a failure to account for residents' social and cultural needs. The Pruitt-Igoe housing complex in St. Louis, designed according to modernist principles and demolished just two decades after its construction, became an emblem of modernism's perceived failure to deliver on its social promises.\n\nContemporary architecture has largely moved beyond the rigid doctrines of high modernism while preserving its democratic aspirations. Architects increasingly engage with communities in the design process, incorporate cultural and contextual considerations, and blend modern materials with local building traditions. This evolution suggests that modernism's most enduring contribution may not be a specific aesthetic but rather the conviction that architecture bears social responsibility.",
      "passage_title": "Modernism in Architecture and the Democratization of Space",
      "passage_category": "arts_and_culture",
      "passage_difficulty": 3,
      "estimated_reading_time": 180,
      "paragraphs": [
        "The modernist movement in architecture, which emerged in the early twentieth century, sought to break decisively with historical styles and embrace the possibilities of new materials and construction techniques. Architects such as Le Corbusier, Ludwig Mies van der Rohe, and Walter Gropius championed designs characterized by clean lines, open floor plans, and the honest expression of structural materials like steel, concrete, and glass. Their ambition extended beyond aesthetics: modernism aspired to solve social problems through design, creating functional, affordable housing and public spaces accessible to all social classes.",
        "This democratic impulse was perhaps most clearly expressed in social housing projects of the mid-twentieth century. Le Corbusier's Unit\u00e9 d'Habitation in Marseille, completed in 1952, was designed as a self-contained community providing apartments, shops, recreational facilities, and a rooftop kindergarten within a single concrete structure. The building embodied the modernist belief that thoughtful design could improve quality of life for working-class residents by integrating housing with community services.",
        "However, the social ambitions of modernist architecture frequently collided with the realities of implementation. Large-scale housing projects, particularly in the United States and Britain, often suffered from poor construction quality, inadequate maintenance, and a failure to account for residents' social and cultural needs. The Pruitt-Igoe housing complex in St. Louis, designed according to modernist principles and demolished just two decades after its construction, became an emblem of modernism's perceived failure to deliver on its social promises.",
        "Contemporary architecture has largely moved beyond the rigid doctrines of high modernism while preserving its democratic aspirations. Architects increasingly engage with communities in the design process, incorporate cultural and contextual considerations, and blend modern materials with local building traditions. This evolution suggests that modernism's most enduring contribution may not be a specific aesthetic but rather the conviction that architecture bears social responsibility."
      ]
    },
    {
      "id": "rc-q-024",
      "passage_id": "rc-passage-008",
      "section": "verbal",
      "subsection": "reading_comprehension",
      "question_type": "inference",
      "topic": "arts_and_culture",
      "difficulty": 3,
      "target_solving_time": 90,
      "evidence_paragraphs": [
        4
      ],
      "question_text": "The passage implies that contemporary architecture's approach to community engagement differs from high modernism's approach in that contemporary architects",
      "options": [
        "reject all modernist design principles as outdated",
        "prioritize aesthetics over functionality in their designs",
        "involve residents in the design process rather than imposing predetermined solutions",
        "focus exclusively on luxury developments rather than social housing",
        "use only traditional building materials and techniques"
      ],
      "correct_option_index": 2,
      "explanation": "P4 states that architects 'increasingly engage with communities in the design process,' implying a shift from modernism's top-down approach to participatory design.",
      "option_explanations": [
        "Too extreme: P4 says they preserve democratic aspirations from modernism.",
        "Not stated: The focus is on social responsibility, not aesthetics over function.",
        "Correct: Community engagement represents the key difference.",
        "Not stated: Social responsibility is maintained.",
        "Contradicted: P4 says they 'blend modern materials with local building traditions.'"
      ],
      "trap_type": "distortion",
      "skills": [
        "inference",
        "contrast"
      ],
      "passage_text": "The modernist movement in architecture, which emerged in the early twentieth century, sought to break decisively with historical styles and embrace the possibilities of new materials and construction techniques. Architects such as Le Corbusier, Ludwig Mies van der Rohe, and Walter Gropius championed designs characterized by clean lines, open floor plans, and the honest expression of structural materials like steel, concrete, and glass. Their ambition extended beyond aesthetics: modernism aspired to solve social problems through design, creating functional, affordable housing and public spaces accessible to all social classes.\n\nThis democratic impulse was perhaps most clearly expressed in social housing projects of the mid-twentieth century. Le Corbusier's Unit\u00e9 d'Habitation in Marseille, completed in 1952, was designed as a self-contained community providing apartments, shops, recreational facilities, and a rooftop kindergarten within a single concrete structure. The building embodied the modernist belief that thoughtful design could improve quality of life for working-class residents by integrating housing with community services.\n\nHowever, the social ambitions of modernist architecture frequently collided with the realities of implementation. Large-scale housing projects, particularly in the United States and Britain, often suffered from poor construction quality, inadequate maintenance, and a failure to account for residents' social and cultural needs. The Pruitt-Igoe housing complex in St. Louis, designed according to modernist principles and demolished just two decades after its construction, became an emblem of modernism's perceived failure to deliver on its social promises.\n\nContemporary architecture has largely moved beyond the rigid doctrines of high modernism while preserving its democratic aspirations. Architects increasingly engage with communities in the design process, incorporate cultural and contextual considerations, and blend modern materials with local building traditions. This evolution suggests that modernism's most enduring contribution may not be a specific aesthetic but rather the conviction that architecture bears social responsibility.",
      "passage_title": "Modernism in Architecture and the Democratization of Space",
      "passage_category": "arts_and_culture",
      "passage_difficulty": 3,
      "estimated_reading_time": 180,
      "paragraphs": [
        "The modernist movement in architecture, which emerged in the early twentieth century, sought to break decisively with historical styles and embrace the possibilities of new materials and construction techniques. Architects such as Le Corbusier, Ludwig Mies van der Rohe, and Walter Gropius championed designs characterized by clean lines, open floor plans, and the honest expression of structural materials like steel, concrete, and glass. Their ambition extended beyond aesthetics: modernism aspired to solve social problems through design, creating functional, affordable housing and public spaces accessible to all social classes.",
        "This democratic impulse was perhaps most clearly expressed in social housing projects of the mid-twentieth century. Le Corbusier's Unit\u00e9 d'Habitation in Marseille, completed in 1952, was designed as a self-contained community providing apartments, shops, recreational facilities, and a rooftop kindergarten within a single concrete structure. The building embodied the modernist belief that thoughtful design could improve quality of life for working-class residents by integrating housing with community services.",
        "However, the social ambitions of modernist architecture frequently collided with the realities of implementation. Large-scale housing projects, particularly in the United States and Britain, often suffered from poor construction quality, inadequate maintenance, and a failure to account for residents' social and cultural needs. The Pruitt-Igoe housing complex in St. Louis, designed according to modernist principles and demolished just two decades after its construction, became an emblem of modernism's perceived failure to deliver on its social promises.",
        "Contemporary architecture has largely moved beyond the rigid doctrines of high modernism while preserving its democratic aspirations. Architects increasingly engage with communities in the design process, incorporate cultural and contextual considerations, and blend modern materials with local building traditions. This evolution suggests that modernism's most enduring contribution may not be a specific aesthetic but rather the conviction that architecture bears social responsibility."
      ]
    }
  ],
  "GRAMMAR_QUESTIONS": [
    {
      "id": "gr-001",
      "mode": "foundation",
      "foundation_type": "grammar",
      "subtopic": "subject_verb_agreement",
      "level": 1,
      "difficulty": 1,
      "question_text": "Choose the correct sentence:",
      "options": [
        "The team of researchers have published their findings.",
        "The team of researchers has published its findings.",
        "The team of researchers have published its findings.",
        "The team of researchers has published their findings."
      ],
      "correct_option_index": 1,
      "grammar_rule": "A collective noun (team) is singular when the group acts as a unit.",
      "why_it_works": "'The team' is a singular collective noun, so it takes the singular verb 'has' and pronoun 'its.'",
      "why_incorrect_fail": [
        "Uses plural verb 'have' with singular subject 'team.'",
        "\u2014",
        "Uses plural 'have' with singular 'team.'",
        "'Has' is correct but 'their' is informal; 'its' is the standard match for a collective noun acting as a unit."
      ],
      "simple_example": "The committee has reached its decision.",
      "gmat_example": "The board of directors has approved the merger.",
      "common_trap": "The prepositional phrase 'of researchers' can mislead you into matching the verb with 'researchers' instead of 'team.'",
      "memory_rule": "Ignore phrases between subject and verb\u2014match the verb to the actual subject.",
      "target_time_seconds": 45
    },
    {
      "id": "gr-002",
      "mode": "foundation",
      "foundation_type": "grammar",
      "subtopic": "verb_tenses",
      "level": 1,
      "difficulty": 2,
      "question_text": "Select the correct verb form: By the time the manager arrives, the team ______ the presentation.",
      "options": [
        "will complete",
        "will have completed",
        "completed",
        "has completed"
      ],
      "correct_option_index": 1,
      "grammar_rule": "Future perfect tense (will have + past participle) is used for an action that will be completed before a specific future time.",
      "why_it_works": "The action (completing) will be finished before the manager's arrival, requiring future perfect.",
      "why_incorrect_fail": [
        "Simple future doesn't convey completion before a specific future event.",
        "\u2014",
        "Past tense is wrong for a future scenario.",
        "Present perfect doesn't fit a future context."
      ],
      "simple_example": "By next Friday, I will have finished the report.",
      "gmat_example": "By the end of the fiscal year, the company will have generated record revenue.",
      "common_trap": "Confusing 'will complete' (simple future) with 'will have completed' (future perfect).",
      "memory_rule": "'By the time X happens' \u2192 future perfect (will have done).",
      "target_time_seconds": 45
    },
    {
      "id": "gr-003",
      "mode": "foundation",
      "foundation_type": "grammar",
      "subtopic": "modifiers",
      "level": 2,
      "difficulty": 3,
      "question_text": "Identify the sentence with a correctly placed modifier:",
      "options": [
        "Running quickly through the park, the finish line was crossed by the athlete.",
        "The athlete crossed the finish line, running quickly through the park.",
        "Running quickly through the park, the athlete crossed the finish line.",
        "The finish line, running quickly through the park, was crossed by the athlete."
      ],
      "correct_option_index": 2,
      "grammar_rule": "A participial phrase must be placed next to the noun it modifies (the doer of the action).",
      "why_it_works": "'Running quickly' modifies 'the athlete,' who immediately follows the phrase.",
      "why_incorrect_fail": [
        "Dangling modifier: 'the finish line' cannot be 'running.'",
        "Misplaced modifier: Placement after the main clause creates ambiguity.",
        "\u2014",
        "Absurd: The finish line cannot be running."
      ],
      "simple_example": "Walking to school, Maria found a coin.",
      "gmat_example": "Seeking to increase market share, the company launched an aggressive advertising campaign.",
      "common_trap": "Dangling modifiers: the phrase seems to modify whatever noun follows it, even if illogical.",
      "memory_rule": "Participial phrase \u2192 the doer must be the very next noun.",
      "target_time_seconds": 50
    },
    {
      "id": "gr-004",
      "mode": "foundation",
      "foundation_type": "grammar",
      "subtopic": "parallelism",
      "level": 2,
      "difficulty": 3,
      "question_text": "Which sentence demonstrates correct parallel structure?",
      "options": [
        "The CEO plans to cut costs, increase revenue, and hiring more staff.",
        "The CEO plans to cut costs, to increase revenue, and hiring more staff.",
        "The CEO plans to cut costs, increase revenue, and hire more staff.",
        "The CEO plans cutting costs, increasing revenue, and to hire more staff."
      ],
      "correct_option_index": 2,
      "grammar_rule": "Items in a series must follow the same grammatical pattern (all infinitives, all gerunds, etc.).",
      "why_it_works": "All three items are base infinitives after 'to': cut, increase, hire.",
      "why_incorrect_fail": [
        "Breaks parallelism: 'hiring' is a gerund; the others are infinitives.",
        "Inconsistent: mixes 'to + verb' with gerund 'hiring.'",
        "\u2014",
        "Mixes gerunds with infinitive 'to hire.'"
      ],
      "simple_example": "She likes reading, writing, and running.",
      "gmat_example": "The strategy involves reducing overhead, streamlining operations, and increasing employee productivity.",
      "common_trap": "Mixing verb forms in a list (gerunds with infinitives).",
      "memory_rule": "In a list, all items must match in form: verb, verb, verb.",
      "target_time_seconds": 45
    },
    {
      "id": "gr-005",
      "mode": "foundation",
      "foundation_type": "grammar",
      "subtopic": "comparisons",
      "level": 2,
      "difficulty": 3,
      "question_text": "Select the grammatically correct comparison:",
      "options": [
        "The profits of Company A are higher than Company B.",
        "The profits of Company A are higher than those of Company B.",
        "Company A's profits are higher than Company B.",
        "The profits of Company A are more higher than those of Company B."
      ],
      "correct_option_index": 1,
      "grammar_rule": "Comparisons must be between like items. Use 'those of' to compare parallel categories.",
      "why_it_works": "'Profits' are compared to 'those [profits] of Company B'\u2014parallel comparison.",
      "why_incorrect_fail": [
        "Faulty comparison: compares profits to a company, not profits to profits.",
        "\u2014",
        "Faulty comparison: compares profits to Company B itself.",
        "Double comparative: 'more higher' is grammatically incorrect."
      ],
      "simple_example": "The population of Tokyo is greater than that of Paris.",
      "gmat_example": "The revenue growth of the acquiring firm exceeded that of its competitors.",
      "common_trap": "Comparing an attribute (profits) to an entity (company) instead of comparing like to like.",
      "memory_rule": "Compare apples to apples: profits to profits, not profits to companies.",
      "target_time_seconds": 45
    },
    {
      "id": "gr-006",
      "mode": "foundation",
      "foundation_type": "grammar",
      "subtopic": "pronoun_reference",
      "level": 1,
      "difficulty": 2,
      "question_text": "Which sentence has a clear pronoun reference?",
      "options": [
        "When the manager spoke to the client, he was confused.",
        "The manager spoke to the client and clarified the client's concerns.",
        "The manager and the client discussed the project, and he approved it.",
        "He told him that he needed more time."
      ],
      "correct_option_index": 1,
      "grammar_rule": "Pronouns must clearly refer to a single, unambiguous antecedent.",
      "why_it_works": "No ambiguous pronouns; 'the client's' clearly identifies whose concerns.",
      "why_incorrect_fail": [
        "Ambiguous: 'he' could refer to either the manager or the client.",
        "\u2014",
        "Ambiguous: 'he' could be either person.",
        "Completely ambiguous: three 'he/him' pronouns with no clear referents."
      ],
      "simple_example": "John told Mark that Mark's report was excellent.",
      "gmat_example": "The auditor informed the CFO that the CFO's division had exceeded budget projections.",
      "common_trap": "Using a pronoun when two nouns of the same gender precede it.",
      "memory_rule": "If 'he' or 'she' could refer to more than one person, use the name instead.",
      "target_time_seconds": 40
    },
    {
      "id": "gr-007",
      "mode": "foundation",
      "foundation_type": "grammar",
      "subtopic": "articles",
      "level": 1,
      "difficulty": 1,
      "question_text": "Choose the correct article usage:",
      "options": [
        "She is a honest person.",
        "She is an honest person.",
        "She is the honest person.",
        "She is honest person."
      ],
      "correct_option_index": 1,
      "grammar_rule": "'An' is used before words that begin with a vowel sound, regardless of spelling.",
      "why_it_works": "'Honest' starts with a vowel sound (the 'h' is silent), so 'an' is correct.",
      "why_incorrect_fail": [
        "'A' is used before consonant sounds, but 'honest' starts with a vowel sound.",
        "\u2014",
        "'The' implies a specific person, which changes the meaning.",
        "Missing article: 'a/an' is needed before a singular countable noun."
      ],
      "simple_example": "He waited for an hour.",
      "gmat_example": "The proposal presents an honest assessment of the company's risks.",
      "common_trap": "Matching 'a/an' to the first letter rather than the first sound.",
      "memory_rule": "Listen to the sound, not the letter: 'an hour' (silent h), 'a university' (yoo- sound).",
      "target_time_seconds": 30
    },
    {
      "id": "gr-008",
      "mode": "foundation",
      "foundation_type": "grammar",
      "subtopic": "active_passive_voice",
      "level": 2,
      "difficulty": 2,
      "question_text": "Which sentence is in active voice?",
      "options": [
        "The report was completed by the analyst.",
        "The analyst completed the report.",
        "The report has been completed by the analyst.",
        "The completion of the report was done by the analyst."
      ],
      "correct_option_index": 1,
      "grammar_rule": "In active voice, the subject performs the action. In passive voice, the subject receives it.",
      "why_it_works": "'The analyst' (subject) performs the action 'completed.'",
      "why_incorrect_fail": [
        "Passive: subject 'report' receives the action.",
        "\u2014",
        "Passive: 'has been completed' signals passive construction.",
        "Passive and wordy: Nominalization with passive voice."
      ],
      "simple_example": "The dog chased the cat. (Active) vs. The cat was chased by the dog. (Passive)",
      "gmat_example": "The board approved the acquisition. (Active, preferred in GMAT writing)",
      "common_trap": "Nominalizations disguise passive voice: 'the completion was done' instead of 'completed.'",
      "memory_rule": "If you can add 'by [someone]' at the end, it's likely passive.",
      "target_time_seconds": 40
    },
    {
      "id": "gr-009",
      "mode": "foundation",
      "foundation_type": "grammar",
      "subtopic": "concision",
      "level": 3,
      "difficulty": 3,
      "question_text": "Which version is the most concise without losing meaning?",
      "options": [
        "Due to the fact that the weather was bad, the event was cancelled.",
        "The event was cancelled because of bad weather.",
        "Because the weather was bad, the event was cancelled.",
        "The event was cancelled due to the weather being bad."
      ],
      "correct_option_index": 1,
      "grammar_rule": "Eliminate wordy phrases. Replace 'due to the fact that' with 'because' or 'because of.'",
      "why_it_works": "Shortest version that retains full meaning without unnecessary words.",
      "why_incorrect_fail": [
        "Wordy: 'Due to the fact that' should be 'because.'",
        "\u2014",
        "Acceptable but slightly less concise than B.",
        "Wordy: 'the weather being bad' adds unnecessary gerund construction."
      ],
      "simple_example": "'In order to succeed' \u2192 'To succeed'",
      "gmat_example": "'The reason why profits declined is that costs increased' \u2192 'Profits declined because costs increased.'",
      "common_trap": "Using 'due to the fact that,' 'in order to,' 'for the purpose of' instead of simpler alternatives.",
      "memory_rule": "If you can say it in fewer words without losing meaning, do it.",
      "target_time_seconds": 45
    },
    {
      "id": "gr-010",
      "mode": "foundation",
      "foundation_type": "grammar",
      "subtopic": "conditional_sentences",
      "level": 2,
      "difficulty": 3,
      "question_text": "Choose the correct conditional sentence:",
      "options": [
        "If the company would have invested earlier, it would have captured more market share.",
        "If the company had invested earlier, it would have captured more market share.",
        "If the company invested earlier, it would have captured more market share.",
        "If the company has invested earlier, it will have captured more market share."
      ],
      "correct_option_index": 1,
      "grammar_rule": "Third conditional (past unreal): If + past perfect, would have + past participle.",
      "why_it_works": "'Had invested' (past perfect) pairs with 'would have captured' for an unreal past condition.",
      "why_incorrect_fail": [
        "Error: 'would have' cannot appear in the if-clause of a conditional.",
        "\u2014",
        "Mixed conditional: Simple past in if-clause doesn't match third conditional.",
        "Incorrect tense pairing: present perfect with future perfect."
      ],
      "simple_example": "If I had studied harder, I would have passed the exam.",
      "gmat_example": "If the firm had diversified its portfolio, it would have mitigated the losses.",
      "common_trap": "Using 'would have' in the if-clause instead of 'had.'",
      "memory_rule": "If HAD \u2192 WOULD HAVE. Never 'if would have.'",
      "target_time_seconds": 45
    },
    {
      "id": "gr-011",
      "mode": "foundation",
      "foundation_type": "grammar",
      "subtopic": "punctuation",
      "level": 2,
      "difficulty": 2,
      "question_text": "Which sentence uses the semicolon correctly?",
      "options": [
        "The company expanded; because it secured new funding.",
        "The company expanded; it secured new funding last quarter.",
        "The company; expanded after securing new funding.",
        "The company expanded; and it secured new funding."
      ],
      "correct_option_index": 1,
      "grammar_rule": "A semicolon connects two independent clauses that are closely related in meaning.",
      "why_it_works": "Both clauses are complete sentences, and they are logically connected.",
      "why_incorrect_fail": [
        "'Because' makes the second part a dependent clause\u2014use a comma, not a semicolon.",
        "\u2014",
        "Semicolon splits a subject from its verb.",
        "Don't use both a semicolon and a conjunction\u2014use one or the other."
      ],
      "simple_example": "It was raining; we stayed indoors.",
      "gmat_example": "Revenue increased 12 percent; however, net income declined due to rising costs.",
      "common_trap": "Using a semicolon before 'because' or splitting subject from verb.",
      "memory_rule": "Semicolon = period power. Both sides must be able to stand alone as sentences.",
      "target_time_seconds": 40
    },
    {
      "id": "gr-012",
      "mode": "foundation",
      "foundation_type": "grammar",
      "subtopic": "conjunctions",
      "level": 1,
      "difficulty": 2,
      "question_text": "Select the sentence with the correct conjunction:",
      "options": [
        "The project was delayed, so the team worked overtime.",
        "The project was delayed, but the team worked overtime.",
        "The project was delayed, or the team worked overtime.",
        "The project was delayed, for the team worked overtime."
      ],
      "correct_option_index": 0,
      "grammar_rule": "'So' indicates a cause-effect relationship (result). 'But' indicates contrast.",
      "why_it_works": "Working overtime is a logical result of the delay, so 'so' (cause-effect) fits.",
      "why_incorrect_fail": [
        "\u2014",
        "'But' implies contrast\u2014overtime is not contrasted with delay here.",
        "'Or' implies an alternative, which doesn't fit the logical relationship.",
        "'For' means 'because'\u2014overtime is the result, not the cause, of the delay."
      ],
      "simple_example": "It was cold, so I wore a jacket.",
      "gmat_example": "Demand exceeded supply, so the company raised prices.",
      "common_trap": "Using 'but' when the relationship is cause-effect, not contrast.",
      "memory_rule": "FANBOYS: For (because), And (addition), Nor (neither), But (contrast), Or (alternative), Yet (contrast), So (result).",
      "target_time_seconds": 40
    },
    {
      "id": "gr-013",
      "mode": "foundation",
      "foundation_type": "grammar",
      "subtopic": "countable_uncountable",
      "level": 1,
      "difficulty": 2,
      "question_text": "Choose the correct quantifier:",
      "options": [
        "The company has less employees than its competitor.",
        "The company has fewer employees than its competitor.",
        "The company has a fewer number of employees than its competitor.",
        "The company has lesser employees than its competitor."
      ],
      "correct_option_index": 1,
      "grammar_rule": "'Fewer' is used with countable nouns; 'less' is used with uncountable nouns.",
      "why_it_works": "'Employees' are countable, so 'fewer' is correct.",
      "why_incorrect_fail": [
        "'Less' is for uncountable nouns (less water, less time), not countable (employees).",
        "\u2014",
        "'A fewer number' is redundant and non-standard.",
        "'Lesser' means 'of smaller importance,' not 'a smaller quantity.'"
      ],
      "simple_example": "Fewer apples, less juice.",
      "gmat_example": "Fewer companies reported losses this quarter than in the previous year.",
      "common_trap": "Using 'less' with countable nouns (less people, less items).",
      "memory_rule": "Can you count it? Use 'fewer.' Can't count it? Use 'less.'",
      "target_time_seconds": 35
    },
    {
      "id": "gr-014",
      "mode": "foundation",
      "foundation_type": "grammar",
      "subtopic": "sentence_structure",
      "level": 2,
      "difficulty": 3,
      "question_text": "Which sentence avoids a run-on or comma splice?",
      "options": [
        "The merger was approved, the shareholders were satisfied.",
        "The merger was approved the shareholders were satisfied.",
        "The merger was approved, and the shareholders were satisfied.",
        "The merger was approved, so, the shareholders were satisfied."
      ],
      "correct_option_index": 2,
      "grammar_rule": "Two independent clauses need a conjunction with a comma, a semicolon, or a period\u2014not just a comma.",
      "why_it_works": "A comma followed by 'and' correctly connects two independent clauses.",
      "why_incorrect_fail": [
        "Comma splice: two independent clauses joined only by a comma.",
        "Run-on: two independent clauses with no punctuation.",
        "\u2014",
        "Incorrect punctuation: extra comma after 'so' is non-standard."
      ],
      "simple_example": "I studied hard, and I passed the exam.",
      "gmat_example": "The acquisition was completed in June, and integration began the following month.",
      "common_trap": "Joining two sentences with only a comma (comma splice).",
      "memory_rule": "Two complete sentences + just a comma = error. Add a conjunction or use a semicolon.",
      "target_time_seconds": 45
    },
    {
      "id": "gr-015",
      "mode": "foundation",
      "foundation_type": "grammar",
      "subtopic": "redundancy",
      "level": 3,
      "difficulty": 3,
      "question_text": "Which sentence eliminates the redundancy?",
      "options": [
        "The CEO gave a brief summary of the annual yearly report.",
        "The CEO summarized the annual report.",
        "The CEO gave a summary that was brief of the annual yearly report.",
        "The CEO briefly summarized the annual yearly report."
      ],
      "correct_option_index": 1,
      "grammar_rule": "Eliminate redundant words: 'brief summary' is redundant (summaries are brief by nature); 'annual yearly' repeats the same idea.",
      "why_it_works": "'Summarized' includes the idea of brevity; 'annual' alone conveys yearly.",
      "why_incorrect_fail": [
        "'Brief summary' and 'annual yearly' are both redundant.",
        "\u2014",
        "Awkward and still contains 'annual yearly.'",
        "'Annual yearly' is still redundant."
      ],
      "simple_example": "'Return back' \u2192 'Return.' 'End result' \u2192 'Result.'",
      "gmat_example": "The consensus among analysts is... (not 'the general consensus of opinion among analysts')",
      "common_trap": "Common redundancies: 'past history,' 'future plans,' 'completely eliminate,' 'free gift.'",
      "memory_rule": "If removing a word doesn't change the meaning, remove it.",
      "target_time_seconds": 45
    },
    {
      "id": "gr-016",
      "mode": "foundation",
      "foundation_type": "grammar",
      "subtopic": "prepositions",
      "level": 1,
      "difficulty": 2,
      "question_text": "Choose the correct preposition:",
      "options": [
        "The report is different than the previous version.",
        "The report is different from the previous version.",
        "The report is different to the previous version.",
        "The report is different of the previous version."
      ],
      "correct_option_index": 1,
      "grammar_rule": "In standard American English and GMAT usage, 'different from' is preferred.",
      "why_it_works": "'Different from' is the standard prepositional pairing in formal writing.",
      "why_incorrect_fail": [
        "'Different than' is informal and not preferred in GMAT style.",
        "\u2014",
        "'Different to' is British English and non-standard in GMAT context.",
        "'Different of' is not idiomatic in any English dialect."
      ],
      "simple_example": "This book is different from that one.",
      "gmat_example": "The company's strategy is fundamentally different from that of its competitors.",
      "common_trap": "Using 'different than' (common in speech but not in formal GMAT writing).",
      "memory_rule": "Different FROM (formal/GMAT). Differ FROM. Similar TO.",
      "target_time_seconds": 35
    },
    {
      "id": "gr-017",
      "mode": "foundation",
      "foundation_type": "grammar",
      "subtopic": "word_order",
      "level": 2,
      "difficulty": 2,
      "question_text": "Which sentence has correct word order?",
      "options": [
        "Only the manager can approve expenditures exceeding ten thousand dollars.",
        "The manager only can approve expenditures exceeding ten thousand dollars.",
        "The manager can only approve expenditures exceeding ten thousand dollars.",
        "The manager can approve only expenditures exceeding ten thousand dollars."
      ],
      "correct_option_index": 0,
      "grammar_rule": "'Only' should be placed immediately before the word or phrase it modifies.",
      "why_it_works": "'Only the manager' = nobody else can approve. This is the intended meaning.",
      "why_incorrect_fail": [
        "\u2014",
        "Awkward placement: 'only can' is ambiguous.",
        "Changes meaning: implies the manager can only approve (not reject or review).",
        "Changes meaning: implies only expenditures (not other items) over $10K."
      ],
      "simple_example": "Only she passed the test. (Nobody else passed.)",
      "gmat_example": "Only companies with revenue exceeding five million dollars are eligible for the tax credit.",
      "common_trap": "Placing 'only' in the wrong position changes the sentence's meaning.",
      "memory_rule": "'Only' modifies whatever comes right after it. Place it carefully.",
      "target_time_seconds": 45
    },
    {
      "id": "gr-018",
      "mode": "foundation",
      "foundation_type": "grammar",
      "subtopic": "clauses",
      "level": 2,
      "difficulty": 3,
      "question_text": "Identify the sentence with correct use of a restrictive clause:",
      "options": [
        "The employees, who completed the training, received a bonus.",
        "The employees who completed the training received a bonus.",
        "The employees, that completed the training, received a bonus.",
        "The employees, which completed the training, received a bonus."
      ],
      "correct_option_index": 1,
      "grammar_rule": "Restrictive (essential) clauses use 'who/that' without commas. Non-restrictive clauses use commas.",
      "why_it_works": "No commas = restrictive: only employees who completed training got bonuses, not all employees.",
      "why_incorrect_fail": [
        "Commas make it non-restrictive, implying ALL employees completed training and got bonuses.",
        "\u2014",
        "'That' should not be used with commas; 'that' is always restrictive.",
        "'Which' refers to things, not people."
      ],
      "simple_example": "The car that I bought is red. (Restrictive: specifies which car.)",
      "gmat_example": "The firms that invested in technology outperformed those that did not.",
      "common_trap": "Adding commas to restrictive clauses changes the meaning from 'some' to 'all.'",
      "memory_rule": "No commas = essential info (restrictive). Commas = extra info (non-restrictive).",
      "target_time_seconds": 50
    },
    {
      "id": "gr-019",
      "mode": "foundation",
      "foundation_type": "grammar",
      "subtopic": "logical_sentence_construction",
      "level": 3,
      "difficulty": 4,
      "question_text": "Which sentence correctly expresses the intended logical relationship?",
      "options": [
        "Despite increasing revenue, the company hired more staff.",
        "Despite declining revenue, the company hired more staff.",
        "Because of declining revenue, the company hired more staff.",
        "Due to increasing revenue, the company hired fewer staff."
      ],
      "correct_option_index": 1,
      "grammar_rule": "'Despite' signals a contrast between expectation and action. The action should be surprising given the condition.",
      "why_it_works": "Hiring more staff despite declining revenue is a surprising contrast\u2014this is logically coherent.",
      "why_incorrect_fail": [
        "No real contrast: hiring more staff when revenue increases is expected, not surprising.",
        "\u2014",
        "Illogical: 'because of' implies causation, but declining revenue wouldn't logically cause more hiring.",
        "No contrast and illogical: increasing revenue causing fewer hires is unexpected but uses 'due to' (cause), not 'despite.'"
      ],
      "simple_example": "Despite the rain, she went jogging. (Surprise: rain should discourage jogging.)",
      "gmat_example": "Despite a 15% decline in market share, the company increased its advertising budget.",
      "common_trap": "Using contrast words (despite, although) when there is no actual contrast.",
      "memory_rule": "'Despite' = 'You'd expect X, but Y happened instead.'",
      "target_time_seconds": 50
    },
    {
      "id": "gr-020",
      "mode": "foundation",
      "foundation_type": "grammar",
      "subtopic": "common_errors",
      "level": 1,
      "difficulty": 2,
      "question_text": "Which sentence is free of grammatical errors?",
      "options": [
        "Each of the candidates have submitted their application.",
        "Each of the candidates has submitted his or her application.",
        "Each of the candidates have submitted his or her applications.",
        "Every candidates has submitted their application."
      ],
      "correct_option_index": 1,
      "grammar_rule": "'Each' is singular and takes a singular verb and singular pronoun.",
      "why_it_works": "'Each' \u2192 singular verb 'has' \u2192 singular pronoun 'his or her.'",
      "why_incorrect_fail": [
        "'Each' is singular but 'have' and 'their' are plural.",
        "\u2014",
        "'Each' is singular but 'have' is plural.",
        "'Every' takes a singular noun ('every candidate'), not plural."
      ],
      "simple_example": "Each student has his or her own desk.",
      "gmat_example": "Each of the divisions has submitted its quarterly report.",
      "common_trap": "'Each of the [plural noun]' tricks you into using a plural verb.",
      "memory_rule": "Each = one at a time = singular verb.",
      "target_time_seconds": 40
    },
    {
      "id": "gr-021",
      "mode": "foundation",
      "foundation_type": "grammar",
      "subtopic": "sentence_structure",
      "level": 3,
      "difficulty": 4,
      "question_text": "Which sentence correctly combines the two ideas?",
      "options": [
        "The company expanded internationally, it also increased domestic production.",
        "Not only did the company expand internationally, but it also increased domestic production.",
        "The company expanded internationally and it also increased domestic production too.",
        "The company not only expanded internationally, but it increased domestic production also."
      ],
      "correct_option_index": 1,
      "grammar_rule": "'Not only...but also' is a correlative conjunction pair requiring parallel structure.",
      "why_it_works": "'Not only did...expand' parallels 'but...also increased'\u2014correct correlative structure.",
      "why_incorrect_fail": [
        "Comma splice: two independent clauses joined by a comma.",
        "\u2014",
        "Redundant: 'also' and 'too' repeat the same idea.",
        "Incorrect placement: 'also' should follow 'but,' not come at the end."
      ],
      "simple_example": "Not only is she smart, but she is also hardworking.",
      "gmat_example": "Not only did the merger reduce costs, but it also improved market position.",
      "common_trap": "Misplacing 'also' or breaking the parallel structure of correlative conjunctions.",
      "memory_rule": "Not only X, but also Y. X and Y must be parallel in form.",
      "target_time_seconds": 50
    },
    {
      "id": "gr-022",
      "mode": "foundation",
      "foundation_type": "grammar",
      "subtopic": "parts_of_speech",
      "level": 1,
      "difficulty": 1,
      "question_text": "In the sentence 'The rapid growth of the company surprised investors,' which word is an adjective?",
      "options": [
        "growth",
        "rapid",
        "company",
        "surprised"
      ],
      "correct_option_index": 1,
      "grammar_rule": "An adjective modifies a noun, describing its quality, quantity, or state.",
      "why_it_works": "'Rapid' modifies the noun 'growth,' describing how fast the growth was.",
      "why_incorrect_fail": [
        "'Growth' is a noun (the thing being described).",
        "\u2014",
        "'Company' is a noun.",
        "'Surprised' is a verb (the action in the sentence)."
      ],
      "simple_example": "The tall building (tall = adjective modifying building).",
      "gmat_example": "The unprecedented decline in consumer confidence alarmed economists.",
      "common_trap": "Confusing adjectives with adverbs. Adjectives modify nouns; adverbs modify verbs.",
      "memory_rule": "Ask 'what kind?' or 'which one?' \u2192 the answer is the adjective.",
      "target_time_seconds": 30
    },
    {
      "id": "gr-023",
      "mode": "foundation",
      "foundation_type": "grammar",
      "subtopic": "singular_plural",
      "level": 1,
      "difficulty": 2,
      "question_text": "Choose the correct form:",
      "options": [
        "The data shows a clear trend.",
        "The data show a clear trend.",
        "The datas show a clear trend.",
        "The data is showing a clear trend."
      ],
      "correct_option_index": 1,
      "grammar_rule": "In formal and GMAT usage, 'data' is plural (singular: datum). It takes a plural verb.",
      "why_it_works": "'Data' is formally plural, so 'show' (plural verb) is correct in GMAT style.",
      "why_incorrect_fail": [
        "'Shows' is a singular verb; 'data' is plural in formal usage.",
        "\u2014",
        "'Datas' is not a word.",
        "'Is showing' treats 'data' as singular."
      ],
      "simple_example": "The data indicate a rising trend. (Plural verb 'indicate')",
      "gmat_example": "The data from the study suggest that the hypothesis is correct.",
      "common_trap": "Treating 'data' as singular. In everyday English it's often singular, but GMAT uses formal plural.",
      "memory_rule": "GMAT formal: data ARE, criteria ARE, phenomena ARE.",
      "target_time_seconds": 35
    },
    {
      "id": "gr-024",
      "mode": "foundation",
      "foundation_type": "grammar",
      "subtopic": "gmat_bridge_argument_language",
      "level": 4,
      "difficulty": 4,
      "question_text": "Which sentence correctly uses argument transition language?",
      "options": [
        "The study supports the hypothesis; conversely, the sample size was adequate.",
        "The study supports the hypothesis; moreover, the sample size was large enough to ensure statistical significance.",
        "The study supports the hypothesis; however, the sample size was large enough to ensure statistical significance.",
        "The study supports the hypothesis; nevertheless, the sample size was adequate."
      ],
      "correct_option_index": 1,
      "grammar_rule": "'Moreover' adds supporting information. 'However/conversely/nevertheless' signal contrast or concession.",
      "why_it_works": "Adequate sample size adds support to the hypothesis, so 'moreover' (addition) is correct.",
      "why_incorrect_fail": [
        "'Conversely' signals opposition, but adequate sample size supports the hypothesis.",
        "\u2014",
        "'However' signals contrast, but both clauses point in the same direction.",
        "'Nevertheless' signals concession despite opposition, which doesn't fit here."
      ],
      "simple_example": "The product is affordable; moreover, it comes with a two-year warranty.",
      "gmat_example": "Revenue increased 20 percent; moreover, operating margins expanded by 5 percentage points.",
      "common_trap": "Using contrast transitions (however, nevertheless) when adding supporting information.",
      "memory_rule": "Moreover/Furthermore = same direction. However/Nevertheless = opposite direction.",
      "target_time_seconds": 50
    },
    {
      "id": "gr-025",
      "mode": "foundation",
      "foundation_type": "grammar",
      "subtopic": "gmat_bridge_cause_effect",
      "level": 4,
      "difficulty": 4,
      "question_text": "Which sentence correctly expresses cause and effect?",
      "options": [
        "The decline in sales was a result from the economic recession.",
        "The decline in sales resulted from the economic recession.",
        "The decline in sales resulted of the economic recession.",
        "The decline in sales was resulted by the economic recession."
      ],
      "correct_option_index": 1,
      "grammar_rule": "'Result from' means 'caused by.' 'Result in' means 'lead to.'",
      "why_it_works": "The decline was caused by the recession, so 'resulted from' is correct.",
      "why_incorrect_fail": [
        "'A result from' is not standard; use 'a result of' or 'resulted from.'",
        "\u2014",
        "'Resulted of' is not idiomatic English.",
        "'Was resulted by' is not a valid construction."
      ],
      "simple_example": "The accident resulted from poor visibility.",
      "gmat_example": "The merger resulted in significant cost savings for both companies.",
      "common_trap": "Confusing 'result from' (effect from cause) with 'result in' (cause leads to effect).",
      "memory_rule": "Result FROM = caused by. Result IN = leads to.",
      "target_time_seconds": 45
    }
  ],
  "VOCABULARY_ITEMS": [
    {
      "id": "v-001",
      "word": "mitigate",
      "part_of_speech": "verb",
      "definition": "To make less severe or intense; to moderate.",
      "contextual_meaning": "To reduce the impact of a negative outcome.",
      "example_sentence": "The company implemented controls to mitigate financial risk.",
      "business_example": "Diversification can mitigate portfolio volatility.",
      "synonyms": [
        "alleviate",
        "reduce",
        "lessen",
        "diminish"
      ],
      "antonyms": [
        "aggravate",
        "intensify",
        "worsen"
      ],
      "root_prefix_suffix": "Latin 'mitigare' (to soften)",
      "common_confusion": "Mitigate does not mean to eliminate completely.",
      "memory_aid": "MITIgate \u2192 MITI(gation) makes things MILDER.",
      "level": 2,
      "difficulty": 3
    },
    {
      "id": "v-002",
      "word": "proliferate",
      "part_of_speech": "verb",
      "definition": "To increase rapidly in number; to multiply.",
      "contextual_meaning": "To spread or grow quickly.",
      "example_sentence": "Startups have proliferated in the technology sector.",
      "business_example": "Digital payment methods have proliferated across developing economies.",
      "synonyms": [
        "multiply",
        "spread",
        "expand",
        "burgeon"
      ],
      "antonyms": [
        "decline",
        "decrease",
        "diminish"
      ],
      "root_prefix_suffix": "Latin 'proles' (offspring) + 'ferre' (to bear)",
      "common_confusion": "Proliferate implies rapid, widespread increase, not just gradual growth.",
      "memory_aid": "PROLIFIC + RATE = things appearing at a prolific rate.",
      "level": 2,
      "difficulty": 3
    },
    {
      "id": "v-003",
      "word": "exacerbate",
      "part_of_speech": "verb",
      "definition": "To make a problem, situation, or negative feeling worse.",
      "contextual_meaning": "To intensify or aggravate an existing issue.",
      "example_sentence": "The drought exacerbated the water shortage.",
      "business_example": "Supply chain disruptions exacerbated inflationary pressures.",
      "synonyms": [
        "worsen",
        "aggravate",
        "intensify",
        "compound"
      ],
      "antonyms": [
        "alleviate",
        "mitigate",
        "ameliorate"
      ],
      "root_prefix_suffix": "Latin 'exacerbare' (to irritate)",
      "common_confusion": "Exacerbate means to make worse, not to cause; the problem must already exist.",
      "memory_aid": "EX-AGGRAVATE \u2192 makes things WORSE.",
      "level": 2,
      "difficulty": 3
    },
    {
      "id": "v-004",
      "word": "ubiquitous",
      "part_of_speech": "adjective",
      "definition": "Present, appearing, or found everywhere.",
      "contextual_meaning": "So common that it seems to be everywhere.",
      "example_sentence": "Smartphones have become ubiquitous in modern society.",
      "business_example": "Cloud computing has become ubiquitous in enterprise infrastructure.",
      "synonyms": [
        "omnipresent",
        "pervasive",
        "universal",
        "widespread"
      ],
      "antonyms": [
        "rare",
        "scarce",
        "uncommon"
      ],
      "root_prefix_suffix": "Latin 'ubique' (everywhere)",
      "common_confusion": "Ubiquitous implies presence everywhere, not just common.",
      "memory_aid": "U-BIG-uitous: so BIG it's everywhere.",
      "level": 3,
      "difficulty": 4
    },
    {
      "id": "v-005",
      "word": "pragmatic",
      "part_of_speech": "adjective",
      "definition": "Dealing with things sensibly and realistically; practical rather than theoretical.",
      "contextual_meaning": "Focused on practical outcomes rather than ideals.",
      "example_sentence": "The CEO took a pragmatic approach to the restructuring.",
      "business_example": "A pragmatic negotiation strategy focuses on achievable concessions.",
      "synonyms": [
        "practical",
        "realistic",
        "sensible",
        "utilitarian"
      ],
      "antonyms": [
        "idealistic",
        "theoretical",
        "impractical"
      ],
      "root_prefix_suffix": "Greek 'pragma' (deed, act)",
      "common_confusion": "Pragmatic is not negative\u2014it simply means practical, not cynical.",
      "memory_aid": "PRAGmatic \u2192 PRACTical.",
      "level": 2,
      "difficulty": 2
    },
    {
      "id": "v-006",
      "word": "dichotomy",
      "part_of_speech": "noun",
      "definition": "A division or contrast between two things that are opposed or entirely different.",
      "contextual_meaning": "A clear division into two contradictory groups or ideas.",
      "example_sentence": "The dichotomy between rich and poor is growing.",
      "business_example": "The dichotomy between short-term profits and long-term sustainability presents a governance challenge.",
      "synonyms": [
        "divide",
        "split",
        "contrast",
        "polarity"
      ],
      "antonyms": [
        "unity",
        "convergence",
        "similarity"
      ],
      "root_prefix_suffix": "Greek 'dicha' (in two) + 'tomos' (cutting)",
      "common_confusion": "A dichotomy is a sharp division, not a mild difference.",
      "memory_aid": "DI (two) + CUT = cutting into TWO.",
      "level": 3,
      "difficulty": 4
    },
    {
      "id": "v-007",
      "word": "inherent",
      "part_of_speech": "adjective",
      "definition": "Existing as a permanent, essential, or characteristic attribute.",
      "contextual_meaning": "Built-in or natural; not added from outside.",
      "example_sentence": "There are inherent risks in any investment.",
      "business_example": "The inherent volatility of emerging markets requires careful risk management.",
      "synonyms": [
        "intrinsic",
        "innate",
        "built-in",
        "fundamental"
      ],
      "antonyms": [
        "extrinsic",
        "acquired",
        "external"
      ],
      "root_prefix_suffix": "Latin 'inhaerere' (to stick in)",
      "common_confusion": "Inherent means naturally part of something, not just associated with it.",
      "memory_aid": "IN-HERE-nt: the quality is IN HERE, built right in.",
      "level": 2,
      "difficulty": 3
    },
    {
      "id": "v-008",
      "word": "empirical",
      "part_of_speech": "adjective",
      "definition": "Based on observation or experience rather than theory or pure logic.",
      "contextual_meaning": "Derived from real-world data and evidence.",
      "example_sentence": "The theory lacks empirical support.",
      "business_example": "Empirical evidence suggests that diverse teams outperform homogeneous ones.",
      "synonyms": [
        "observational",
        "experiential",
        "evidence-based",
        "practical"
      ],
      "antonyms": [
        "theoretical",
        "hypothetical",
        "speculative"
      ],
      "root_prefix_suffix": "Greek 'empeiria' (experience)",
      "common_confusion": "Empirical does not mean 'proven'\u2014it means based on observation.",
      "memory_aid": "EMPIRical \u2192 like an EMPIRE built on real experience.",
      "level": 3,
      "difficulty": 3
    },
    {
      "id": "v-009",
      "word": "corroborate",
      "part_of_speech": "verb",
      "definition": "To confirm or give support to a statement, theory, or finding.",
      "contextual_meaning": "To provide additional evidence that supports a claim.",
      "example_sentence": "The witness corroborated the defendant's alibi.",
      "business_example": "Independent auditors corroborated the company's financial statements.",
      "synonyms": [
        "confirm",
        "verify",
        "substantiate",
        "validate"
      ],
      "antonyms": [
        "contradict",
        "refute",
        "disprove"
      ],
      "root_prefix_suffix": "Latin 'corroborare' (to strengthen)",
      "common_confusion": "Corroborate means to support with additional evidence, not to originate the claim.",
      "memory_aid": "CO-ROBUST-ate: make an argument more ROBUST.",
      "level": 3,
      "difficulty": 4
    },
    {
      "id": "v-010",
      "word": "anomaly",
      "part_of_speech": "noun",
      "definition": "Something that deviates from what is standard, normal, or expected.",
      "contextual_meaning": "An unusual occurrence or irregularity.",
      "example_sentence": "The warm winter was an anomaly in the region's weather patterns.",
      "business_example": "The quarterly earnings spike was an anomaly driven by a one-time asset sale.",
      "synonyms": [
        "irregularity",
        "deviation",
        "aberration",
        "outlier"
      ],
      "antonyms": [
        "norm",
        "regularity",
        "standard"
      ],
      "root_prefix_suffix": "Greek 'anomalos' (uneven, irregular)",
      "common_confusion": "An anomaly is not necessarily negative; it simply deviates from the norm.",
      "memory_aid": "A-NORMAL-y: NOT normal.",
      "level": 2,
      "difficulty": 2
    },
    {
      "id": "v-011",
      "word": "precipitate",
      "part_of_speech": "verb",
      "definition": "To cause something to happen suddenly, unexpectedly, or prematurely.",
      "contextual_meaning": "To trigger or bring about rapidly.",
      "example_sentence": "The scandal precipitated the CEO's resignation.",
      "business_example": "A credit downgrade can precipitate a liquidity crisis.",
      "synonyms": [
        "trigger",
        "spark",
        "hasten",
        "accelerate"
      ],
      "antonyms": [
        "prevent",
        "delay",
        "hinder"
      ],
      "root_prefix_suffix": "Latin 'praecipitare' (to throw headlong)",
      "common_confusion": "Precipitate (verb) means to cause suddenly; precipitate (adjective) means hasty.",
      "memory_aid": "PRECIPICE + ATE: like falling off a precipice\u2014sudden and dramatic.",
      "level": 3,
      "difficulty": 4
    },
    {
      "id": "v-012",
      "word": "commensurate",
      "part_of_speech": "adjective",
      "definition": "Corresponding in size, extent, or degree; proportionate.",
      "contextual_meaning": "Matching or in proportion to something.",
      "example_sentence": "The salary is commensurate with experience.",
      "business_example": "Returns should be commensurate with the level of risk assumed.",
      "synonyms": [
        "proportionate",
        "corresponding",
        "equivalent",
        "appropriate"
      ],
      "antonyms": [
        "disproportionate",
        "inadequate",
        "excessive"
      ],
      "root_prefix_suffix": "Latin 'com-' (together) + 'mensurare' (to measure)",
      "common_confusion": "Commensurate means proportional, not equal.",
      "memory_aid": "CO-MEASURE-ate: measured TOGETHER to match.",
      "level": 3,
      "difficulty": 4
    },
    {
      "id": "v-013",
      "word": "disparate",
      "part_of_speech": "adjective",
      "definition": "Essentially different in kind; not able to be compared.",
      "contextual_meaning": "So different that comparison is difficult or inappropriate.",
      "example_sentence": "The two proposals address disparate issues.",
      "business_example": "The merger brought together disparate corporate cultures.",
      "synonyms": [
        "different",
        "dissimilar",
        "distinct",
        "divergent"
      ],
      "antonyms": [
        "similar",
        "comparable",
        "alike"
      ],
      "root_prefix_suffix": "Latin 'disparatus' (separated)",
      "common_confusion": "Disparate means fundamentally different, not just slightly different. Do not confuse with 'desperate.'",
      "memory_aid": "DIS-PAIR-ate: things that don't PAIR well because they're too different.",
      "level": 3,
      "difficulty": 3
    },
    {
      "id": "v-014",
      "word": "paradigm",
      "part_of_speech": "noun",
      "definition": "A typical example or pattern of something; a model or framework.",
      "contextual_meaning": "A dominant way of thinking or a standard framework.",
      "example_sentence": "The shift from print to digital represented a paradigm shift in media.",
      "business_example": "Agile development represents a new paradigm for software engineering.",
      "synonyms": [
        "model",
        "framework",
        "pattern",
        "archetype"
      ],
      "antonyms": [
        "anomaly",
        "deviation"
      ],
      "root_prefix_suffix": "Greek 'paradeigma' (pattern, example)",
      "common_confusion": "A paradigm is the entire framework of assumptions, not just a single example.",
      "memory_aid": "PARA-DIME: a dime is a model coin\u2014paradigm is the model framework.",
      "level": 3,
      "difficulty": 3
    },
    {
      "id": "v-015",
      "word": "catalyst",
      "part_of_speech": "noun",
      "definition": "A person or thing that precipitates an event or change.",
      "contextual_meaning": "Something that triggers or accelerates change without being consumed by it.",
      "example_sentence": "The new CEO served as a catalyst for organizational transformation.",
      "business_example": "Low interest rates acted as a catalyst for the housing market boom.",
      "synonyms": [
        "trigger",
        "stimulus",
        "impetus",
        "spark"
      ],
      "antonyms": [
        "inhibitor",
        "deterrent",
        "obstacle"
      ],
      "root_prefix_suffix": "Greek 'katalysis' (dissolution)",
      "common_confusion": "In business context, a catalyst initiates change; in chemistry, it speeds up a reaction.",
      "memory_aid": "CAT-a-LYST: the CAT knocked something over and started a chain reaction.",
      "level": 2,
      "difficulty": 2
    },
    {
      "id": "v-016",
      "word": "tenuous",
      "part_of_speech": "adjective",
      "definition": "Very weak or slight; lacking substance or firmness.",
      "contextual_meaning": "Barely adequate or supported; fragile.",
      "example_sentence": "The connection between the two events is tenuous at best.",
      "business_example": "The company's claim to market leadership rests on tenuous evidence.",
      "synonyms": [
        "weak",
        "flimsy",
        "fragile",
        "insubstantial"
      ],
      "antonyms": [
        "strong",
        "substantial",
        "robust"
      ],
      "root_prefix_suffix": "Latin 'tenuis' (thin, slight)",
      "common_confusion": "Tenuous implies weakness or fragility, not necessarily falsity.",
      "memory_aid": "TEN-U-ous: as thin as a TENDON stretched too far.",
      "level": 3,
      "difficulty": 3
    },
    {
      "id": "v-017",
      "word": "pertinent",
      "part_of_speech": "adjective",
      "definition": "Relevant or applicable to a particular matter; apposite.",
      "contextual_meaning": "Directly related and useful to the topic at hand.",
      "example_sentence": "The lawyer raised several pertinent objections.",
      "business_example": "The consultant focused on the most pertinent market data.",
      "synonyms": [
        "relevant",
        "applicable",
        "appropriate",
        "germane"
      ],
      "antonyms": [
        "irrelevant",
        "immaterial",
        "extraneous"
      ],
      "root_prefix_suffix": "Latin 'pertinere' (to pertain to)",
      "common_confusion": "Pertinent is stronger than 'related'\u2014it means directly relevant and important.",
      "memory_aid": "PERTAIN-ent: it PERTAINS to the topic.",
      "level": 2,
      "difficulty": 2
    },
    {
      "id": "v-018",
      "word": "ambiguous",
      "part_of_speech": "adjective",
      "definition": "Open to more than one interpretation; unclear or inexact.",
      "contextual_meaning": "Having multiple possible meanings; not definitive.",
      "example_sentence": "The contract language was deliberately ambiguous.",
      "business_example": "Ambiguous regulatory guidelines create compliance uncertainty.",
      "synonyms": [
        "vague",
        "unclear",
        "equivocal",
        "indeterminate"
      ],
      "antonyms": [
        "clear",
        "unambiguous",
        "definitive",
        "explicit"
      ],
      "root_prefix_suffix": "Latin 'ambiguus' (having two meanings, from 'ambi-' = both)",
      "common_confusion": "Ambiguous (multiple meanings) vs. Ambivalent (mixed feelings).",
      "memory_aid": "AMBI (both) + GUOUS: going BOTH ways in meaning.",
      "level": 2,
      "difficulty": 2
    },
    {
      "id": "v-019",
      "word": "circumvent",
      "part_of_speech": "verb",
      "definition": "To find a way around an obstacle or restriction.",
      "contextual_meaning": "To avoid or bypass, especially cleverly.",
      "example_sentence": "The company found ways to circumvent the trade restrictions.",
      "business_example": "Some firms attempt to circumvent regulations through offshore subsidiaries.",
      "synonyms": [
        "bypass",
        "evade",
        "sidestep",
        "avoid"
      ],
      "antonyms": [
        "confront",
        "comply",
        "face"
      ],
      "root_prefix_suffix": "Latin 'circum' (around) + 'venire' (to come)",
      "common_confusion": "Circumvent implies clever avoidance, not direct confrontation.",
      "memory_aid": "CIRCUM (circle around) + VENT: go AROUND the obstacle.",
      "level": 3,
      "difficulty": 3
    },
    {
      "id": "v-020",
      "word": "substantiate",
      "part_of_speech": "verb",
      "definition": "To provide evidence to support or prove the truth of a claim.",
      "contextual_meaning": "To back up with concrete proof.",
      "example_sentence": "The researcher could not substantiate her claims with data.",
      "business_example": "The plaintiff must substantiate damages with financial documentation.",
      "synonyms": [
        "verify",
        "confirm",
        "corroborate",
        "validate"
      ],
      "antonyms": [
        "disprove",
        "refute",
        "invalidate"
      ],
      "root_prefix_suffix": "Latin 'substantia' (substance, essence)",
      "common_confusion": "Substantiate means to provide proof, not just to believe something.",
      "memory_aid": "SUBSTANCE + ATE: give SUBSTANCE (proof) to a claim.",
      "level": 3,
      "difficulty": 3
    },
    {
      "id": "v-021",
      "word": "analogous",
      "part_of_speech": "adjective",
      "definition": "Comparable in certain respects; similar enough to allow comparison.",
      "contextual_meaning": "Similar in relevant ways, allowing a useful comparison.",
      "example_sentence": "The CEO drew an analogous comparison between the two market downturns.",
      "business_example": "The current supply chain crisis is analogous to the disruptions of 2020.",
      "synonyms": [
        "comparable",
        "similar",
        "parallel",
        "equivalent"
      ],
      "antonyms": [
        "dissimilar",
        "different",
        "unrelated"
      ],
      "root_prefix_suffix": "Greek 'analogia' (proportion)",
      "common_confusion": "Analogous means similar in certain respects, not identical.",
      "memory_aid": "ANALOG-ous: like an ANALOGY\u2014similar but not the same.",
      "level": 3,
      "difficulty": 3
    },
    {
      "id": "v-022",
      "word": "preclude",
      "part_of_speech": "verb",
      "definition": "To prevent from happening; to make impossible.",
      "contextual_meaning": "To rule out or make something impossible in advance.",
      "example_sentence": "The heavy snowfall precluded any outdoor activities.",
      "business_example": "The non-compete clause precludes former employees from joining rival firms.",
      "synonyms": [
        "prevent",
        "rule out",
        "exclude",
        "prohibit"
      ],
      "antonyms": [
        "allow",
        "permit",
        "enable"
      ],
      "root_prefix_suffix": "Latin 'praecludere' (to close off)",
      "common_confusion": "Preclude means to make impossible, not just to discourage.",
      "memory_aid": "PRE-CLUDE (close): CLOSE the door BEFORE something can happen.",
      "level": 3,
      "difficulty": 3
    },
    {
      "id": "v-023",
      "word": "volatile",
      "part_of_speech": "adjective",
      "definition": "Liable to change rapidly and unpredictably, especially for the worse.",
      "contextual_meaning": "Subject to sudden, dramatic fluctuations.",
      "example_sentence": "The stock market has been particularly volatile this quarter.",
      "business_example": "Volatile commodity prices make budget forecasting challenging.",
      "synonyms": [
        "unstable",
        "unpredictable",
        "fluctuating",
        "erratic"
      ],
      "antonyms": [
        "stable",
        "steady",
        "predictable"
      ],
      "root_prefix_suffix": "Latin 'volatilis' (fleeting, from volare = to fly)",
      "common_confusion": "Volatile doesn't always mean dangerous\u2014it means prone to rapid change.",
      "memory_aid": "VOLATILE = VOL (fly) = changes that FLY up and down.",
      "level": 2,
      "difficulty": 2
    },
    {
      "id": "v-024",
      "word": "alleviate",
      "part_of_speech": "verb",
      "definition": "To make suffering, a problem, or a deficiency less severe.",
      "contextual_meaning": "To partially reduce or relieve a negative condition.",
      "example_sentence": "The new policy aims to alleviate poverty in rural areas.",
      "business_example": "Automation can alleviate bottlenecks in the production process.",
      "synonyms": [
        "relieve",
        "ease",
        "mitigate",
        "reduce"
      ],
      "antonyms": [
        "aggravate",
        "worsen",
        "exacerbate"
      ],
      "root_prefix_suffix": "Latin 'alleviare' (to lighten)",
      "common_confusion": "Alleviate means to reduce, not to eliminate completely.",
      "memory_aid": "A-LEVER-iate: use a LEVER to LIGHTEN the burden.",
      "level": 2,
      "difficulty": 2
    },
    {
      "id": "v-025",
      "word": "conjecture",
      "part_of_speech": "noun/verb",
      "definition": "An opinion or conclusion formed on the basis of incomplete information; a guess.",
      "contextual_meaning": "An educated guess without full evidence.",
      "example_sentence": "The report is based on conjecture rather than facts.",
      "business_example": "Analysts' earnings estimates are often conjecture disguised as precision.",
      "synonyms": [
        "speculation",
        "hypothesis",
        "supposition",
        "guess"
      ],
      "antonyms": [
        "fact",
        "certainty",
        "proof"
      ],
      "root_prefix_suffix": "Latin 'conjectura' (interpretation, from con- + jacere = to throw together)",
      "common_confusion": "Conjecture is weaker than hypothesis\u2014it has even less evidence.",
      "memory_aid": "CON-JECT-ure: THROW (ject) ideas TOGETHER to guess.",
      "level": 3,
      "difficulty": 3
    },
    {
      "id": "v-026",
      "word": "feasible",
      "part_of_speech": "adjective",
      "definition": "Possible and practical to do easily or conveniently.",
      "contextual_meaning": "Capable of being accomplished; workable.",
      "example_sentence": "The plan is technically feasible but financially challenging.",
      "business_example": "A feasibility study determines whether the proposed expansion is feasible.",
      "synonyms": [
        "possible",
        "practicable",
        "viable",
        "achievable"
      ],
      "antonyms": [
        "impossible",
        "impracticable",
        "unfeasible"
      ],
      "root_prefix_suffix": "Latin 'facere' (to do, make)",
      "common_confusion": "Feasible means possible and practical, not just theoretically possible.",
      "memory_aid": "FEAS-ible = able to be DONE (facere).",
      "level": 2,
      "difficulty": 2
    },
    {
      "id": "v-027",
      "word": "scrutinize",
      "part_of_speech": "verb",
      "definition": "To examine or inspect closely and thoroughly.",
      "contextual_meaning": "To look at something with intense, critical attention.",
      "example_sentence": "Investors scrutinized the company's quarterly earnings report.",
      "business_example": "Regulators scrutinize merger proposals for antitrust concerns.",
      "synonyms": [
        "examine",
        "inspect",
        "analyze",
        "investigate"
      ],
      "antonyms": [
        "overlook",
        "ignore",
        "neglect"
      ],
      "root_prefix_suffix": "Latin 'scrutinium' (close search)",
      "common_confusion": "Scrutinize implies careful, detailed examination\u2014not a casual glance.",
      "memory_aid": "SCRUT-inize: look at something under a SCREW-tiny lens.",
      "level": 2,
      "difficulty": 2
    },
    {
      "id": "v-028",
      "word": "unprecedented",
      "part_of_speech": "adjective",
      "definition": "Never done or known before; without previous example.",
      "contextual_meaning": "Completely new; no historical precedent exists.",
      "example_sentence": "The pandemic caused unprecedented disruption to global supply chains.",
      "business_example": "The central bank took unprecedented measures to stabilize markets.",
      "synonyms": [
        "unparalleled",
        "unmatched",
        "novel",
        "extraordinary"
      ],
      "antonyms": [
        "common",
        "ordinary",
        "precedented"
      ],
      "root_prefix_suffix": "un- (not) + precedent (previous example)",
      "common_confusion": "Unprecedented means truly first-time, not just unusual or severe.",
      "memory_aid": "UN-PRECEDENT-ed: no PRECEDENT (previous case) exists.",
      "level": 2,
      "difficulty": 2
    },
    {
      "id": "v-029",
      "word": "ameliorate",
      "part_of_speech": "verb",
      "definition": "To make something bad or unsatisfactory better; to improve.",
      "contextual_meaning": "To improve a negative situation or condition.",
      "example_sentence": "The new legislation aims to ameliorate working conditions in factories.",
      "business_example": "The restructuring plan is designed to ameliorate the company's financial position.",
      "synonyms": [
        "improve",
        "better",
        "enhance",
        "upgrade"
      ],
      "antonyms": [
        "worsen",
        "deteriorate",
        "degrade"
      ],
      "root_prefix_suffix": "Latin 'melior' (better)",
      "common_confusion": "Ameliorate specifically means to improve a bad situation, not just any improvement.",
      "memory_aid": "A-MELIORATE = make things MELLOW (better).",
      "level": 3,
      "difficulty": 4
    },
    {
      "id": "v-030",
      "word": "cogent",
      "part_of_speech": "adjective",
      "definition": "Clear, logical, and convincing.",
      "contextual_meaning": "Persuasive through clarity and strength of reasoning.",
      "example_sentence": "She presented a cogent argument for increasing the marketing budget.",
      "business_example": "The consultant delivered a cogent analysis that convinced the board to proceed.",
      "synonyms": [
        "convincing",
        "compelling",
        "persuasive",
        "logical"
      ],
      "antonyms": [
        "unconvincing",
        "weak",
        "illogical",
        "vague"
      ],
      "root_prefix_suffix": "Latin 'cogere' (to compel, drive together)",
      "common_confusion": "Cogent implies logical persuasiveness, not emotional appeal.",
      "memory_aid": "CO-GENT: a GENT (gentleman) who argues with compelling logic.",
      "level": 3,
      "difficulty": 3
    }
  ],
  "CATALOG": {
    "critical_reasoning": {
      "total_questions": 20,
      "question_types": [
        "must_be_true",
        "flaw_in_reasoning",
        "sufficient_assumption",
        "resolve_paradox",
        "assumption",
        "principle",
        "method_of_reasoning",
        "explain_discrepancy",
        "main_conclusion",
        "boldface",
        "necessary_assumption",
        "weaken",
        "evaluate",
        "inference",
        "strengthen"
      ],
      "topics": [
        "scientific_study",
        "environmental_policy",
        "economics",
        "public_health",
        "business_strategy",
        "ethics",
        "technology",
        "business_operations",
        "education",
        "public_policy"
      ],
      "difficulties": [
        2,
        3,
        4,
        5
      ]
    },
    "reading_comprehension": {
      "total_passages": 8,
      "total_questions": 24,
      "categories": [
        "science",
        "business",
        "environment",
        "history",
        "economics",
        "arts_and_culture",
        "technology",
        "social_science"
      ],
      "difficulties": [
        3,
        4
      ]
    },
    "foundation_grammar": {
      "total_questions": 25,
      "subtopics": [
        "comparisons",
        "common_errors",
        "countable_uncountable",
        "parts_of_speech",
        "singular_plural",
        "modifiers",
        "parallelism",
        "punctuation",
        "active_passive_voice",
        "sentence_structure",
        "prepositions",
        "clauses",
        "word_order",
        "pronoun_reference",
        "verb_tenses",
        "conjunctions",
        "articles",
        "gmat_bridge_cause_effect",
        "conditional_sentences",
        "redundancy",
        "concision",
        "subject_verb_agreement",
        "gmat_bridge_argument_language",
        "logical_sentence_construction"
      ],
      "levels": [
        1,
        2,
        3,
        4
      ]
    },
    "foundation_vocabulary": {
      "total_items": 30,
      "levels": [
        2,
        3
      ]
    }
  }
};
