import json
import logging
import os
import random
from typing import Any, Dict, List, Optional
from dotenv import load_dotenv

try:
    from groq import Groq
except ImportError:
    Groq = None

from database.english_data import (
    CR_QUESTIONS,
    RC_PASSAGES,
    RC_QUESTIONS,
    GRAMMAR_QUESTIONS,
    VOCABULARY_ITEMS,
)

load_dotenv()
logger = logging.getLogger(__name__)


class EnglishQuestionGenerator:
    """
    LLM-powered question generator for GMAT Verbal Reasoning and English Foundation.
    Uses Groq LLM with structured JSON output and falls back to curated database/english_data.py.
    """

    CR_QUESTION_TYPES = [
        "strengthen",
        "weaken",
        "assumption",
        "inference",
        "resolve_paradox",
        "flaw_in_reasoning",
        "evaluate",
        "method_of_reasoning",
        "boldface",
        "principle",
    ]

    RC_DOMAINS = [
        "business",
        "economics",
        "science",
        "technology",
        "history",
        "social_science",
        "environment",
        "arts_and_culture",
    ]

    GRAMMAR_TOPICS = [
        "subject_verb_agreement",
        "modifiers",
        "parallelism",
        "comparisons",
        "verb_tenses",
        "pronoun_reference",
        "concision",
        "clauses",
    ]

    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        self.client = None
        if api_key and Groq is not None:
            try:
                self.client = Groq(api_key=api_key)
            except Exception as e:
                logger.warning("Could not initialize Groq client: %s", e)
                self.client = None
        # Default model with high reasoning and structured JSON output
        self.model = "openai/gpt-oss-120b"

    def _has_llm(self) -> bool:
        return self.client is not None and bool(os.getenv("GROQ_API_KEY"))

    def generate_cr_question(
        self,
        question_type: Optional[str] = None,
        difficulty: int = 3,
        domain: Optional[str] = None,
        avoid_questions: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Generate an official-format GMAT Critical Reasoning question.
        """
        if not question_type:
            question_type = random.choice(self.CR_QUESTION_TYPES)
        if not domain:
            domain = random.choice(["business", "public_policy", "economics", "environment", "technology", "science"])

        if self._has_llm():
            try:
                avoid_text = ""
                if avoid_questions:
                    avoid_snippets = [f"- {q[:120]}..." for q in avoid_questions[:5]]
                    avoid_text = "\nDO NOT repeat or closely resemble these previous arguments:\n" + "\n".join(avoid_snippets)

                prompt = f"""You are a master GMAT Verbal Reasoning tutor. Generate an exam-grade Critical Reasoning question.
Target Question Type: {question_type.replace('_', ' ').title()}
Domain: {domain.title()}
Difficulty Level: {difficulty}/5 (1=Basic, 3=Standard GMAT 650, 5=Elite 700+ GMAT with subtle traps)

STRICT GMAT CR RULES:
1. Provide a realistic, logical scenario (~60-90 words).
2. Clearly demarcate the 'premise' (factual basis) and 'conclusion' (author's inference).
3. Exactly ONE option must be 100% correct, watertight, and logically bulletproof.
4. Exactly 4 options must be classic GMAT distractors with identifiable traps (e.g., 'scope_shift', 'extreme_language', 'opposite_effect', 'reversed_causality', 'irrelevant_comparison').
5. Output format MUST strictly be a JSON object with these keys:
{{
  "id": "cr-ai-{random.randint(1000, 9999)}",
  "section": "gmat_verbal",
  "subsection": "critical_reasoning",
  "type": "cr",
  "question_type": "{question_type}",
  "topic": "{domain}",
  "difficulty": {difficulty},
  "target_time": {120 if difficulty <= 3 else 140},
  "stimulus": {{
    "raw": "Full stimulus paragraph text",
    "premise": "Key supporting premises",
    "conclusion": "Author's main conclusion"
  }},
  "stem": "Question stem asking to {question_type.replace('_', ' ')} the argument",
  "options": [
    "Option A text",
    "Option B text",
    "Option C text",
    "Option D text",
    "Option E text"
  ],
  "correct_option_index": 0-4,
  "correct_letter": "A/B/C/D/E",
  "trap_type": "Primary trap in common incorrect choices",
  "reasoning": {{
    "premise": "Premise summary",
    "conclusion": "Conclusion summary",
    "assumption": "Unstated assumption or gap",
    "logical_gap": "Why the reasoning jump requires scrutiny",
    "why_correct": "Clear rationale for why the correct option satisfies the question stem",
    "choices_breakdown": [
      {{"letter": "A", "trap": "Trap Name or Correct", "text": "Why choice A is correct or wrong"}},
      {{"letter": "B", "trap": "Trap Name or Correct", "text": "Why choice B is correct or wrong"}},
      {{"letter": "C", "trap": "Trap Name or Correct", "text": "Why choice C is correct or wrong"}},
      {{"letter": "D", "trap": "Trap Name or Correct", "text": "Why choice D is correct or wrong"}},
      {{"letter": "E", "trap": "Trap Name or Correct", "text": "Why choice E is correct or wrong"}}
    ]
  }}
}}
{avoid_text}
Output ONLY the JSON object.
"""
                response = self.client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": "You are a professional GMAT Verbal test developer. You return only valid JSON."},
                        {"role": "user", "content": prompt},
                    ],
                    model=self.model,
                    response_format={"type": "json_object"},
                    temperature=0.7,
                )
                raw_json = response.choices[0].message.content
                data = json.loads(raw_json)
                if self._validate_cr_schema(data):
                    return data
            except Exception as exc:
                logger.warning("LLM CR generation failed, falling back to curated bank: %s", exc)

        # Fallback to curated question bank
        matching = [q for q in CR_QUESTIONS if q.get("question_type") == question_type]
        if not matching:
            matching = CR_QUESTIONS
        selected = random.choice(matching)
        return self._format_curated_cr(selected)

    def generate_rc_passage(
        self,
        category: Optional[str] = None,
        difficulty: int = 3,
        question_count: int = 3,
    ) -> Dict[str, Any]:
        """
        Generate a multi-paragraph GMAT Reading Comprehension passage with associated questions.
        """
        if not category:
            category = random.choice(self.RC_DOMAINS)

        if self._has_llm():
            try:
                prompt = f"""You are a master GMAT Verbal test creator. Generate an official-style Reading Comprehension passage with questions.
Domain: {category.replace('_', ' ').title()}
Target Difficulty: {difficulty}/5
Question Count: {question_count}

STRICT GMAT RC RULES:
1. Passage must be 3-4 structured paragraphs (~250-320 words). High scholastic density, professional prose.
2. Structure: Paragraph 1 introduces the concept/traditional viewpoint; Paragraph 2 presents complications or empirical counterevidence; Paragraph 3 synthesizes implications.
3. Provide exactly {question_count} questions:
   - Question 1: Primary Purpose / Main Idea
   - Question 2: Inference / Suggestion
   - Question 3: Specific Detail (citing specific paragraph evidence)
   ${"- Question 4: Function of a paragraph or phrase" if question_count >= 4 else ""}
4. Every question MUST have exactly 5 options (A-E).
5. Output format MUST be a valid JSON object:
{{
  "id": "rc-ai-pass-{random.randint(1000, 9999)}",
  "title": "Passage Title",
  "category": "{category}",
  "difficulty": {difficulty},
  "word_count": 280,
  "paragraphs": [
    "Paragraph 1 text...",
    "Paragraph 2 text...",
    "Paragraph 3 text..."
  ],
  "questions": [
    {{
      "id": "rc-ai-q-1",
      "question_type": "primary_purpose",
      "difficulty": {difficulty},
      "target_time": 90,
      "evidence_paragraphs": [1, 2, 3],
      "stem": "The primary purpose of the passage is to...",
      "options": ["A", "B", "C", "D", "E"],
      "correct_option_index": 0-4,
      "correct_letter": "A/B/C/D/E",
      "trap_type": "too_broad / out_of_scope",
      "explanation": "Why correct choice is right",
      "option_explanations": ["Why A is...", "Why B is...", "Why C is...", "Why D is...", "Why E is..."]
    }}
  ]
}}
Output ONLY the JSON object.
"""
                response = self.client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": "You are a professional GMAT test developer. Output only valid JSON."},
                        {"role": "user", "content": prompt},
                    ],
                    model=self.model,
                    response_format={"type": "json_object"},
                    temperature=0.7,
                )
                data = json.loads(response.choices[0].message.content)
                if self._validate_rc_schema(data):
                    return data
            except Exception as exc:
                logger.warning("LLM RC generation failed, falling back to curated bank: %s", exc)

        # Fallback to curated passage bank
        matching = [p for p in RC_PASSAGES if p.get("category") == category]
        if not matching:
            matching = RC_PASSAGES
        selected = random.choice(matching)
        return self._format_curated_rc(selected)

    def generate_grammar_question(
        self,
        subtopic: Optional[str] = None,
        level: int = 2,
        difficulty: int = 3,
    ) -> Dict[str, Any]:
        """
        Generate an English Foundation Grammar practice question.
        """
        if not subtopic:
            subtopic = random.choice(self.GRAMMAR_TOPICS)

        if self._has_llm():
            try:
                prompt = f"""Generate an English Foundation Grammar question for GMAT students.
Grammar Topic: {subtopic.replace('_', ' ').title()}
Proficiency Level: Level {level} of 4 (1=Basic, 2=Intermediate, 3=Advanced, 4=GMAT Bridge)
Difficulty: {difficulty}/5

RULES:
1. Provide a sentence with an underlined section or choice options testing {subtopic}.
2. Exactly 5 options (A, B, C, D, E). Option A should typically replicate the original sentence.
3. Provide comprehensive educational explanations:
   - grammar_rule
   - why_it_works
   - simple_example
   - gmat_example
   - common_trap
   - memory_rule
4. Output MUST be valid JSON:
{{
  "id": "gram-ai-{random.randint(1000, 9999)}",
  "section": "foundation",
  "subsection": "grammar",
  "foundation_type": "grammar",
  "topic": "{subtopic}",
  "level": {level},
  "difficulty": {difficulty},
  "question_text": "Sentence with underlined portion...",
  "options": ["A", "B", "C", "D", "E"],
  "correct_option_index": 0-4,
  "explanation": "Why correct answer is right",
  "option_explanations": ["A explanation", "B explanation", "C explanation", "D explanation", "E explanation"],
  "grammar_rule": "Rule name",
  "why_it_works": "Deep grammatical principle",
  "simple_example": "Everyday example",
  "gmat_example": "Formal academic example",
  "common_trap": "What students mistakenly pick",
  "memory_rule": "Quick mnemonic"
}}
Output ONLY the JSON object.
"""
                response = self.client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": "You are a professional English grammar instructor. Output only valid JSON."},
                        {"role": "user", "content": prompt},
                    ],
                    model=self.model,
                    response_format={"type": "json_object"},
                    temperature=0.6,
                )
                data = json.loads(response.choices[0].message.content)
                if self._validate_grammar_schema(data):
                    return data
            except Exception as exc:
                logger.warning("LLM Grammar generation failed, falling back to curated bank: %s", exc)

        # Fallback to curated grammar questions
        matching = [g for g in GRAMMAR_QUESTIONS if g.get("topic") == subtopic or g.get("level") == level]
        if not matching:
            matching = GRAMMAR_QUESTIONS
        return random.choice(matching)

    def generate_drill_set(
        self,
        mode: str = "mixed",
        count: int = 5,
        target_difficulty: int = 3,
        avoid_questions: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Generate a complete adaptive drill set.
        Modes: 'cr', 'rc', 'grammar', 'mixed'
        """
        questions = []
        if mode == "cr":
            for _ in range(count):
                q = self.generate_cr_question(difficulty=target_difficulty, avoid_questions=avoid_questions)
                questions.append(q)
        elif mode == "rc":
            passage_data = self.generate_rc_passage(difficulty=target_difficulty, question_count=min(count, 4))
            for q in passage_data.get("questions", []):
                q["passage"] = {
                    "id": passage_data.get("id"),
                    "title": passage_data.get("title"),
                    "paragraphs": passage_data.get("paragraphs", []),
                    "word_count": passage_data.get("word_count", 280),
                }
                questions.append(q)
        elif mode == "grammar":
            for _ in range(count):
                q = self.generate_grammar_question(difficulty=target_difficulty)
                questions.append(q)
        else:
            # Mixed verbal drill (CR + RC)
            cr_count = max(1, count // 2)
            for _ in range(cr_count):
                questions.append(self.generate_cr_question(difficulty=target_difficulty, avoid_questions=avoid_questions))
            rc_needed = count - len(questions)
            if rc_needed > 0:
                passage_data = self.generate_rc_passage(difficulty=target_difficulty, question_count=rc_needed)
                for q in passage_data.get("questions", []):
                    q["passage"] = {
                        "id": passage_data.get("id"),
                        "title": passage_data.get("title"),
                        "paragraphs": passage_data.get("paragraphs", []),
                        "word_count": passage_data.get("word_count", 280),
                    }
                    questions.append(q)

        questions = questions[:count]
        return {
            "mode": mode,
            "count": len(questions),
            "target_difficulty": target_difficulty,
            "is_ai_generated": self._has_llm(),
            "questions": questions,
        }

    # Validation & Formatting Helpers
    def _validate_cr_schema(self, data: Dict[str, Any]) -> bool:
        return (
            isinstance(data, dict)
            and "stimulus" in data
            and isinstance(data.get("options"), list)
            and len(data["options"]) == 5
            and isinstance(data.get("correct_option_index"), int)
            and 0 <= data["correct_option_index"] < 5
        )

    def _validate_rc_schema(self, data: Dict[str, Any]) -> bool:
        return (
            isinstance(data, dict)
            and isinstance(data.get("paragraphs"), list)
            and len(data["paragraphs"]) >= 2
            and isinstance(data.get("questions"), list)
            and len(data["questions"]) >= 1
        )

    def _validate_grammar_schema(self, data: Dict[str, Any]) -> bool:
        return (
            isinstance(data, dict)
            and isinstance(data.get("options"), list)
            and len(data["options"]) in (4, 5)
            and "correct_option_index" in data
        )

    def _format_curated_cr(self, q: Dict[str, Any]) -> Dict[str, Any]:
        res = dict(q)
        res["stem"] = res.get("question_text") or res.get("stem") or ""
        if isinstance(res.get("stimulus"), str):
            res["stimulus"] = {
                "raw": res["stimulus"],
                "premise": res.get("premise", ""),
                "conclusion": res.get("conclusion", ""),
            }
        return res

    def _format_curated_rc(self, p: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "id": p.get("id"),
            "title": p.get("title", "Reading Comprehension"),
            "category": p.get("category", "general"),
            "difficulty": p.get("difficulty", 3),
            "word_count": p.get("word_count", 280),
            "paragraphs": p.get("paragraphs", []),
            "questions": [
                {
                    **q,
                    "stem": q.get("question_text") or q.get("stem", ""),
                    "passage": {
                        "id": p.get("id"),
                        "title": p.get("title"),
                        "paragraphs": p.get("paragraphs"),
                    },
                }
                for q in p.get("questions", [])
            ],
        }


# Singleton instance
english_generator = EnglishQuestionGenerator()
