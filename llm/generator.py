import os
import random
import json
import threading
from groq import Groq
from dotenv import load_dotenv
from llm.hybrid_gen import hybrid_generator

load_dotenv()

class QuestionGenerator:
    HYBRID_GROUPS = {
        "group_fraction_foundations": [
            "mixed_fraction",
            "fraction_subtraction",
            "random_conv",
            "benchmark_conv",
            "fraction_to_decimal",
        ],
        "group_core_percentage_equations": [
            "find_original_number",
            "percentage_equations",
        ],
        "group_percentage_calculation_tricks": [
            "swap_percentage",
            "breakdown_percentage",
            "base_comparisons",
            "percentage_calculations",
        ],
        "group_applied_percentage_word_problems": [
            "applied_percentages",
            "percentage_comparisons",
        ],
        "group_mixtures_alligation_shifts": [
            "alligation_shifts",
        ],
        "group_income_savings_exam_aggregates": [
            "income_expenditure",
            "pass_fail_aggregates",
            "exam_scoring",
        ],
        "group_successive_changes_discounts": [
            "successive_changes",
            "successive_discount",
        ],
    }

    HYBRID_SUBTYPES = {
        "random_conv": [
            "fraction_to_percent",
            "percent_to_fraction",
        ],
        "find_original_number": [
            "add_self",
            "sub_self",
            "add_abs",
            "sub_abs",
        ],
        "fraction_to_decimal": [
            "fraction_to_decimal",
            "decimal_to_fraction",
        ],
        "swap_percentage": [
            "swap",
            "scale",
            "composite",
        ],
        "breakdown_percentage": [
            "place_value",
            "breakdown",
            "repeating",
        ],
        "percentage_equations": [
            "sum_diff_ratio",
            "sum_diff_percent",
            "direct_eq_find_x",
            "direct_eq_two_var",
            "multi_var",
            "third_anchor",
            "sum_constraint",
        ],
        "base_comparisons": [
            "direct_of",
            "direct_less",
            "missing_add",
            "missing_num",
            "chain",
            "successive",
            "var_chain",
        ],
        "applied_percentages": [
            "fraction_shift",
            "weighted_avg",
            "population_split",
            "calc_trick_symmetric",
            "calc_trick_find_val",
            "calc_trick_sub",
        ],
        "alligation_shifts": [
            "double_shift_nested",
            "simple_pop_split",
            "qty_value_overlap",
        ],
        "percentage_comparisons": [
            "nested_variable_chain",
            "sum_relativity",
            "basic_diff_equation",
            "ratio_equalization",
            "weight_fraction",
            "multi_person_donations",
            "fractional_population",
        ],
        "percentage_calculations": [
            "product_constancy",
            "work_productivity",
            "geometry_scaling",
            "error_multiplier",
            "salary_remainder",
            "property_value_chain",
            "spoiled_fruit_subsets",
        ],
        "income_expenditure": [
            "direct_savings_pct",
            "net_decimal_variation",
            "backtrack_target_amt_str",
            "missing_savings_rate",
            "fixed_savings_find_income",
            "compare_two_persons",
            "exp_as_pct_of_savings",
            "savings_absolute_change",
        ],
        "pass_fail_aggregates": [
            "split_pass_fail_ratios",
            "weighted_pass_fail",
            "missing_weighted_component",
            "margin_work_scaling",
            "absentee_splits",
            "fail_by_marks",
            "pass_by_marks",
            "two_students_fail_pass",
            "pass_pct_given_marks",
            "find_max_marks",
        ],
        "exam_scoring": [
            "sum_difference_pct",
            "avg_candidates",
            "student_chain",
            "ratio_shift_pass_fail",
            "score_comparison_chain",
            "fail_pass_offsets",
            "fail_pass_simple",
        ],
        "successive_discount": [
            "selling_price",
            "marked_price",
            "equivalent_discount",
        ],
        "vedic_addition": [
            "left_to_right",
            "complements",
            "missing_addend",
        ],
        "vedic_subtraction": [
            "left_to_right",
            "base_complement",
            "near_base_difference",
            "missing_minuend",
        ],
        "vedic_multiplication": [
            "vertical_crosswise",
            "near_base_100",
            "multiply_by_11",
            "split_multiplier",
            "multiply_by_25_125",
        ],
        "vedic_division": [
            "short_division",
            "remainder",
            "divide_by_25_125",
            "missing_dividend",
        ],
        "vedic_tables_multiples": [
            "table_product",
            "missing_factor",
            "next_multiple",
            "factor_split",
        ],
        "vedic_squares_roots": [
            "square_ending_5",
            "near_base_square",
            "two_digit_square",
            "perfect_square_root",
            "integer_square_root",
        ],
        "vedic_cubes_roots": [
            "cube_value",
            "perfect_cube_root",
            "nearest_cube",
            "cube_unit_digit",
        ],
        "vedic_divisibility": [
            "rules_3_9",
            "rules_4_8",
            "rule_11",
            "combined_rules",
        ],
        "vedic_approximation": [
            "compatible_sum",
            "estimate_product",
            "estimate_division",
            "quick_percent",
        ],
    }

    HYBRID_RANDOM_VALUES = {
        ("random_conv", "fraction_to_percent"): [0.99],
        ("random_conv", "percent_to_fraction"): [0.0],
        ("fraction_to_decimal", "fraction_to_decimal"): [0.99, 0.99],
        ("fraction_to_decimal", "decimal_to_fraction"): [0.99, 0.0],
    }

    _forced_variant_lock = threading.RLock()

    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = "openai/gpt-oss-120b" # Latest model

    def _select_hybrid_type(self, hybrid_type):
        return random.choice(self.HYBRID_GROUPS.get(hybrid_type, [hybrid_type]))

    def get_hybrid_variants(self, pattern_name):
        hybrid_type = self._get_hybrid_type(pattern_name)
        if not hybrid_type:
            return []
        return self._expand_hybrid_type(hybrid_type)

    def _expand_hybrid_type(self, hybrid_type):
        variants = []
        for base_type in self.HYBRID_GROUPS.get(hybrid_type, [hybrid_type]):
            subtypes = self.HYBRID_SUBTYPES.get(base_type)
            if subtypes:
                variants.extend(f"{base_type}::{subtype}" for subtype in subtypes)
            else:
                variants.append(base_type)
        return variants

    @staticmethod
    def _split_hybrid_variant(hybrid_type):
        base_type, separator, forced_variant = hybrid_type.partition("::")
        return base_type, forced_variant if separator else None

    @staticmethod
    def _is_difficulty_aware_hybrid(base_type):
        return str(base_type or "").startswith("vedic_")

    def _call_hybrid_generator(self, generator_fn, base_type, forced_variant=None, difficulty=None):
        def call_generator():
            if not generator_fn:
                return None
            if self._is_difficulty_aware_hybrid(base_type):
                return generator_fn(difficulty=difficulty)
            return generator_fn()

        if not generator_fn or not forced_variant:
            return call_generator()

        subtype_list = self.HYBRID_SUBTYPES.get(base_type, [])
        forced_random_values = list(self.HYBRID_RANDOM_VALUES.get((base_type, forced_variant), []))

        real_choice = random.choice
        real_random = random.random

        def choice_with_forced_subtype(seq):
            values = list(seq)
            if forced_variant in values:
                return forced_variant
            return real_choice(seq)

        def random_with_forced_values():
            if forced_random_values:
                return forced_random_values.pop(0)
            return real_random()

        should_patch_choice = forced_variant in subtype_list
        should_patch_random = bool(forced_random_values)

        if not should_patch_choice and not should_patch_random:
            return call_generator()

        with self._forced_variant_lock:
            try:
                if should_patch_choice:
                    random.choice = choice_with_forced_subtype
                if should_patch_random:
                    random.random = random_with_forced_values
                return call_generator()
            finally:
                random.choice = real_choice
                random.random = real_random

    def _generate_hybrid(self, hybrid_type, difficulty=None):
        dispatch = {
            "mixed_fraction": hybrid_generator.generate_mixed_fraction,
            "fraction_subtraction": hybrid_generator.generate_fraction_subtraction,
            "random_conv": hybrid_generator.generate_random_conv,
            "benchmark_conv": hybrid_generator.generate_benchmark_conv,
            "find_original_number": hybrid_generator.generate_find_original_number,
            "fraction_to_decimal": hybrid_generator.generate_fraction_to_decimal,
            "swap_percentage": hybrid_generator.generate_swap_percentage,
            "breakdown_percentage": hybrid_generator.generate_breakdown_percentage,
            "percentage_equations": hybrid_generator.generate_percentage_equations,
            "base_comparisons": hybrid_generator.generate_base_comparisons,
            "applied_percentages": hybrid_generator.generate_applied_percentages,
            "alligation_shifts": hybrid_generator.generate_alligation_shifts,
            "percentage_comparisons": hybrid_generator.generate_percentage_comparisons,
            "percentage_calculations": hybrid_generator.generate_percentage_calculations,
            "income_expenditure": hybrid_generator.generate_income_expenditure,
            "pass_fail_aggregates": hybrid_generator.generate_pass_fail_aggregates,
            "exam_scoring": hybrid_generator.generate_exam_scoring,
            "successive_changes": hybrid_generator.generate_successive_net_change,
            "successive_discount": hybrid_generator.generate_successive_discount,
            "vedic_addition": hybrid_generator.generate_vedic_addition,
            "vedic_subtraction": hybrid_generator.generate_vedic_subtraction,
            "vedic_multiplication": hybrid_generator.generate_vedic_multiplication,
            "vedic_division": hybrid_generator.generate_vedic_division,
            "vedic_tables_multiples": hybrid_generator.generate_vedic_tables_multiples,
            "vedic_squares_roots": hybrid_generator.generate_vedic_squares_roots,
            "vedic_cubes_roots": hybrid_generator.generate_vedic_cubes_roots,
            "vedic_divisibility": hybrid_generator.generate_vedic_divisibility,
            "vedic_approximation": hybrid_generator.generate_vedic_approximation,
            "clockwise_anticlockwise": hybrid_generator.generate_clockwise_anticlockwise,
            "pythagoras_theorem": hybrid_generator.generate_pythagoras_theorem,
            "starting_without_direction": hybrid_generator.generate_starting_without_direction,
            "moving_towards_direction": hybrid_generator.generate_moving_towards_direction,
            "interchange_direction": hybrid_generator.generate_interchange_direction,
            "find_direction_in_respect_to_another": hybrid_generator.generate_find_direction_in_respect_to_another,
            "coded_direction": hybrid_generator.generate_coded_direction,
            "shadow_based": hybrid_generator.generate_shadow_based,
            "headstand": hybrid_generator.generate_headstand,
            "final_facing": hybrid_generator.generate_final_facing,
            "side_movement": hybrid_generator.generate_side_movement,
            "direction_of_smoke": hybrid_generator.generate_direction_of_smoke,
            "playing_cards": hybrid_generator.generate_playing_cards,
            "seating_arrangement": hybrid_generator.generate_seating_arrangement,
            "based_on_turns": hybrid_generator.generate_based_on_turns,
            "one_direction_only": hybrid_generator.generate_one_direction_only,
        }
        selected_type = self._select_hybrid_type(hybrid_type)
        base_type, forced_variant = self._split_hybrid_variant(selected_type)
        generator_fn = dispatch.get(base_type)
        return self._call_hybrid_generator(generator_fn, base_type, forced_variant, difficulty=difficulty)

    def _get_hybrid_type(self, pattern_name):
        """Map exact pattern names to hybrid generator methods (case-insensitive)."""
        pn = pattern_name.strip().lower()
        if pn == "fraction, decimal and percent foundations":
            return "group_fraction_foundations"
        if pn == "core percentage equations":
            return "group_core_percentage_equations"
        if pn == "percentage calculation tricks":
            return "group_percentage_calculation_tricks"
        if pn == "applied percentage word problems":
            return "group_applied_percentage_word_problems"
        if pn == "mixtures, alligation and shifts":
            return "group_mixtures_alligation_shifts"
        if pn == "income, savings and exam aggregates":
            return "group_income_savings_exam_aggregates"
        if pn == "successive changes and discounts":
            return "group_successive_changes_discounts"
        if pn == "mix fraction":
            return "mixed_fraction"
        if pn == "fraction subtraction":
            return "fraction_subtraction"
        if pn == "per to fraction and vice versa":
            return "random_conv"
        if pn == "basic fraction to per":
            return "benchmark_conv"
        if pn == "find original number":
            return "find_original_number"
        if pn in ("fraction to decimal and vice versa", "fraction to decimal"):
            return "fraction_to_decimal"
        if pn == "swap of percentage":
            return "swap_percentage"
        if pn == "breakdown percentage":
            return "breakdown_percentage"
        if pn == "percentage equations and ratios":
            return "percentage_equations"
        if pn == "base comparisons and successive chains":
            return "base_comparisons"
        if pn == "applied scenarios and complex calculations":
            return "applied_percentages"
        if pn == "alligation and shift applications":
            return "alligation_shifts"
        if pn == "percentage comparisons":
            return "percentage_comparisons"
        if pn == "percentage calculations":
            return "percentage_calculations"
        if pn == "income expenditure saving":
            return "income_expenditure"
        if pn == "pass fail aggregates":
            return "pass_fail_aggregates"
        if pn == "examination scoring":
            return "exam_scoring"
        if pn == "successive percentage changes":
            return "successive_changes"
        if pn == "successive discounts":
            return "successive_discount"
        if pn == "speed addition and complements":
            return "vedic_addition"
        if pn == "speed subtraction and complements":
            return "vedic_subtraction"
        if pn == "mental multiplication":
            return "vedic_multiplication"
        if pn == "fast division and remainders":
            return "vedic_division"
        if pn == "tables and multiples mastery":
            return "vedic_tables_multiples"
        if pn == "squares and square roots":
            return "vedic_squares_roots"
        if pn == "cubes and cube roots":
            return "vedic_cubes_roots"
        if pn == "divisibility rules":
            return "vedic_divisibility"
        if pn == "approximation and number sense":
            return "vedic_approximation"
        if pn == "clockwise and anti clockwise":
            return "clockwise_anticlockwise"
        if pn == "pythagoras theorem":
            return "pythagoras_theorem"
        if pn == "starting without direction":
            return "starting_without_direction"
        if pn in ("moving towards different direction", "moving towards different directions"):
            return "moving_towards_direction"
        if pn == "interchange direction":
            return "interchange_direction"
        if pn in ("find direction with respect to another point", "find direction in respect to another"):
            return "find_direction_in_respect_to_another"
        if pn == "coded direction":
            return "coded_direction"
        if pn in ("shadow-based questions", "shadow based"):
            return "shadow_based"
        if pn == "headstand questions":
            return "headstand"
        if pn == "final facing":
            return "final_facing"
        if pn == "side movement":
            return "side_movement"
        if pn == "direction of smoke":
            return "direction_of_smoke"
        if pn == "playing cards":
            return "playing_cards"
        if pn == "seating arrangement":
            return "seating_arrangement"
        if pn == "based on turns":
            return "based_on_turns"
        if pn in ("when only one direction is given", "only one direction given"):
            return "one_direction_only"
        if pn == "instructions based":
            return "moving_towards_direction"
        return None

    def generate_mcq(self, topic_name, pattern_name, pattern_description, difficulty, avoid_questions=None):
        # Check for Hybrid Patterns first
        hybrid_type = self._get_hybrid_type(pattern_name)
        if hybrid_type:
            hybrid_result = self._generate_hybrid(hybrid_type, difficulty=difficulty)

            if hybrid_result:
                # Intercept the hybrid math and pass through LLM for rephrasing
                rephrased, err = self._rephrase_hybrid_question(hybrid_result)
                if err:
                    return None, f"Rephrasing Error: {err}"
                return rephrased, None

        if not os.getenv("GROQ_API_KEY"):
            return None, "Groq API key is missing. Please check your .env file."

        avoid_text = ""
        if avoid_questions:
            avoid_text = "\n\nCRITICAL: Avoid generating these exact scenarios or questions. I have already used them:\n" + "\n".join([f"- {q[:500]}" for q in avoid_questions])

        prompt = f"""
        You are a GMAT and CAT (Common Admission Test) Master Tutor. 
        Your task is to generate a high-quality, exam-standard Multiple Choice Question (MCQ).
        
        Topic: {topic_name}
        Pattern: {pattern_name}
        Description: {pattern_description}
        Target Difficulty: {difficulty}/5

        EXAM STANDARDS:
        1. Use complex, multi-step reasoning similar to official GMAT/CAT questions.
        2. Ensure distractors (wrong options) are plausible and based on common student errors.
        3. The explanation MUST be deep, covering the logic of the correct answer and a refutation of all wrong answers.
        
        RULES:
        1. Always provide exactly 4 options (A, B, C, D).
        2. Output format MUST be a valid JSON object with the following keys:
            "question_text": "text",
            "options": ["A", "B", "C", "D"],
            "correct_option_index": 0-3,
            "explanation": "detailed reasoning",
            "difficulty": integer 1-5

        IMPORTANT: Generate a UNIQUE, varied scenario each time. Choose a distinct real‑world domain (e.g., finance, logistics, sports, health, engineering) and ensure the story context, numbers, and units differ from all previous questions. Use the avoid_questions list to avoid repeating similar wording or values.
        
        {avoid_text}
        
        Response should ONLY be the JSON object.
        """
        
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional GMAT tutor assistant. You output only structured JSON.",
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model=self.model,
                response_format={"type": "json_object"},
            )
            
            content = chat_completion.choices[0].message.content
            try:
                result = json.loads(content)
                return result, None
            except json.JSONDecodeError:
                return None, f"LLM returned invalid JSON logic. Content: {content[:200]}..."

        except Exception as e:
            error_msg = f"Groq API Error: {str(e)}"
            if hasattr(e, 'response') and hasattr(e.response, 'text'):
                error_msg += f" | Details: {e.response.text}"
            return None, error_msg

    def generate_batch(self, patterns_info, count=5, rephrase_hybrids=True):
        results = []
        ai_patterns = []
        random.shuffle(patterns_info)
        
        # Split into Hybrid and AI
        hybrid_results = []
        for p in patterns_info:
            ht = p.get('hybrid_type') or self._get_hybrid_type(p['name'])
            if ht:
                hybrid_result = self._generate_hybrid(ht, difficulty=p.get('difficulty'))
                
                if hybrid_result:
                    hybrid_results.append({**hybrid_result, "pattern_id": p['id']})
            else:
                ai_patterns.append(p)
                
        # Batch rephrase all hybrid results at once
        if hybrid_results and rephrase_hybrids:
            rephrased_hybrids, err = self._batch_rephrase_hybrid(hybrid_results)
            if err:
                print(f"Batch Rephrasing Error: {err}. Using original hybrid questions.")
                results.extend(hybrid_results)
            else:
                results.extend(rephrased_hybrids)
        elif hybrid_results:
            results.extend(hybrid_results)

        # Randomize AI pattern order to increase variety
        random.shuffle(ai_patterns)

        if not ai_patterns:
            return results, None

        if not os.getenv("GROQ_API_KEY"):
            return results, "Groq API key is missing."

        patterns_text = ""
        for p in ai_patterns:
            avoid_text = ""
            if p.get('avoid_questions'):
                avoid_text = "\n   - Avoid these previous scenarios: " + ", ".join([q[:200] for q in p['avoid_questions']])
            
            patterns_text += f"""
--- PATTERN ID: {p['id']} ---
Topic: {p['topic_name']}
Pattern: {p['name']}
Description: {p['description']}
Difficulty: {p['difficulty']}/5{avoid_text}
"""

        prompt = f"""
        You are a GMAT and CAT (Common Admission Test) Master Tutor. 
        Your task is to generate exactly {len(ai_patterns)} unique, high-quality, exam-standard MCQs.
        
        CRITICAL INSTRUCTIONS:
        1. For EACH Pattern ID listed below, you must generate EXACTLY ONE original question.
        2. EXAM STANDARDS: Use complex, multi-step reasoning. Ensure distractors are plausible and based on common student errors.
        3. EXPLANATIONS: Provide deep reasoning for the correct answer and clear refutations for all wrong options.

        PATTERNS TO USE:
        {patterns_text}

        Rules:
        1. Always provide 4 options (A, B, C, D).
        2. Output format MUST be a valid JSON object with a key "questions" containing an array of objects.
        
        Each object should have:
           "question_text": "text",
           "options": ["A", "B", "C", "D"],
           "correct_option_index": 0-3 Integer,
           "explanation": "detailed reasoning",
           "difficulty": integer 1-5,
           "pattern_id": integer (MUST MATCH THE PATTERN ID FROM THE LIST ABOVE)
        """
        
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a professional GMAT tutor assistant. You output only structured JSON arrays."},
                    {"role": "user", "content": prompt}
                ],
                model=self.model,
                response_format={"type": "json_object"}, 
            )
            content = chat_completion.choices[0].message.content
            batch_res = json.loads(content)
            
            if isinstance(batch_res, dict) and "questions" in batch_res:
                q_list = batch_res["questions"]
                if isinstance(q_list, list):
                    results.extend([q for q in q_list if isinstance(q, dict)])
            elif isinstance(batch_res, list):
                results.extend([q for q in batch_res if isinstance(q, dict)])
            
            return results, None
        except Exception as e:
            return results, str(e)

    def _rephrase_hybrid_question(self, hybrid_data):
        """Takes a math-generated question dict and uses the LLM to rewrite the linguistic framing with a retry loop."""
        if not os.getenv("GROQ_API_KEY"):
            return hybrid_data, None 
            
        original_text = hybrid_data['question_text']
        original_explanation = hybrid_data['explanation']
        
        last_err = "Unknown error"
        for attempt in range(2): # Up to 2 retries
            prompt = f"""
            You are a GMAT Question Rephraser.
            Take the following functionally correct math question and rewrite the storyline/context completely.
            Use a professional GMAT/CAT theme (e.g. corporate finance, global trade, industrial production, university admissions, salary negotiations, investment portfolios, market research, or logistics).
            
            Original Question: {original_text}
            Original Explanation: {original_explanation}
            
            CRITICAL RULES:
            1. KEEP ALL NUMERICAL VALUES EXACTLY THE SAME. If the original says 50, use 50. 
            2. DO NOT introduce any new numbers, dates, or quantitative values that were not in the original text (e.g. don't add "in 2024" or "budget of 10,000" if not present).
            3. You MAY change units (e.g., from "dollars" to "galactic credits" or "km" to "light years") if it fits the new theme, but the raw numbers must be invariant.
            4. DO NOT change or reorder the multiple choice options.
            5. You must output a JSON object with strictly these keys:
               "question_text": "your new unique rewritten question",
               "explanation": "the original explanation, altered ONLY to fit the new names/themes. Keep the formulas identical."
            """
            try:
                chat = self.client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": "You are a math tutor assistant. Output strictly valid JSON."},
                        {"role": "user", "content": prompt}
                    ],
                    model=self.model,
                    response_format={"type": "json_object"}
                )
                rephrased_json = json.loads(chat.choices[0].message.content)
                new_text = rephrased_json.get("question_text", original_text)
                new_explanation = rephrased_json.get("explanation", original_explanation)
                
                # Double-LLM Verification
                is_valid, reason = self._verify_rephrased_content(original_text, new_text)
                if is_valid:
                    return {
                        **hybrid_data,
                        "question_text": new_text,
                        "explanation": new_explanation
                    }, None
                else:
                    last_err = f"Verification failed: {reason}"
                    print(f"Rephrase Verification Failed (Attempt {attempt+1}). Reason: {reason}")
            except Exception as e:
                last_err = str(e)
                print(f"Hybrid Rephrase Error (Attempt {attempt+1}): {e}")
        
        return hybrid_data, last_err # Fallback to original instead of returning None

    def _verify_rephrased_content(self, original, rephrased):
        """Second LLM call to verify that the math remains identical."""
        prompt = f"""
        You are a Math Content Verifier. 
        Compare these two versions of a math question. 
        The second version (REPHRASED) should be a stylistic rewrite of the first (ORIGINAL).
        
        ORIGINAL: {original}
        REPHRASED: {rephrased}
        
        RULES:
        1. All numerical values in the ORIGINAL must be present and identical in the REPHRASED version.
        2. Units may change (e.g., $ to credits) but the digits must be invariant.
        3. The mathematical logic as defined by the constraints must be identical.
        4. The question goal (what is being asked for) must be identical.
        
        Output strictly a JSON object: {{"is_valid": true/false, "reason": "short explanation if false"}}
        """
        try:
            chat = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a Match Consistency Checker. YOUR ONLY JOB is to ensure that the DIGITS and NUMBERS (like 20, 10, 50%) are the same in both versions. Ignore commas, dollar signs, or unit symbols (e.g., '29,000' and '29000' are IDENTICAL). IF THE NUMBERS MATCH, IS_VALID IS TRUE."},
                    {"role": "user", "content": prompt}
                ],
                model=self.model, # Can use same or faster model
                response_format={"type": "json_object"}
            )
            try:
                content = chat.choices[0].message.content
                res = json.loads(content)
                if not isinstance(res, dict):
                    return False, f"LLM returned {type(res).__name__} instead of dict"
                return res.get("is_valid", False), res.get("reason", "No reason provided")
            except json.JSONDecodeError:
                return False, "LLM returned invalid JSON"
        except Exception as e:
            return True, f"Error in verification call: {e}" # Fallback to true to avoid infinite retry blocking on minor API errors

    def _batch_rephrase_hybrid(self, hybrid_list):
        """Takes a list of hybrid question dicts and rewrites them all in one LLM call with verification."""
        if not hybrid_list or not os.getenv("GROQ_API_KEY"):
            return hybrid_list, None
            
        last_err = "Unknown batch error"
        for attempt in range(2): 
            original_texts = ""
            for i, h in enumerate(hybrid_list):
                original_texts += f"\\n--- ITEM {i} ---\\nQuestion: {h['question_text']}\\nExplanation: {h['explanation']}"
                
            prompt = f"""
            You are a GMAT Question Rephraser.
            I will give you {len(hybrid_list)} mathematically correct word problems.
            For EACH one, rewrite the storyline/context completely using a professional GMAT/CAT theme (e.g. business operations, economics, social sciences, or corporate management).
            
            CRITICAL RULES:
            1. DO NOT change any numbers or mathematical relationships.
            2. DO NOT add any new numbers, quantities, or dates that were not in the original items.
            3. DO NOT change the multiple choice options.
            4. Output a single JSON object with a "replacements" array.
            
            Format:
            {{
                "replacements": [
                    {{
                        "question_text": "new rewritten text for ITEM 0",
                        "explanation": "explanation adapted to new theme"
                    }},
                    ...
                ]
            }}
            
            INPUT ITEMS:
            {original_texts}
            """
            try:
                chat = self.client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": "You output only valid JSON arrays."},
                        {"role": "user", "content": prompt}
                    ],
                    model=self.model,
                    response_format={"type": "json_object"}
                )
                content = chat.choices[0].message.content
                res = json.loads(content)
                if isinstance(res, list):
                    replacements = res
                elif isinstance(res, dict):
                    replacements = res.get("replacements", [])
                else:
                    print(f"Batch Rephrase Error: Expected dict or list, got {type(res).__name__}")
                    continue
                if not isinstance(replacements, list):
                    print(f"Batch Rephrase Error: 'replacements' should be a list, got {type(replacements).__name__}")
                    continue

                if len(replacements) == len(hybrid_list):
                    for i in range(len(hybrid_list)):
                        rep_item = replacements[i]
                        if not isinstance(rep_item, dict):
                            continue
                            
                        # Verify each one individually
                        is_valid, reason = self._verify_rephrased_content(hybrid_list[i]['question_text'], rep_item.get('question_text', ''))
                        if is_valid:
                            hybrid_list[i]["question_text"] = rep_item.get("question_text", hybrid_list[i]["question_text"])
                            hybrid_list[i]["explanation"] = rep_item.get("explanation", hybrid_list[i]["explanation"])
                        else:
                            print(f"Batch Item {i} Verification Failed: {reason}. Keeping original.")
                    
                    return hybrid_list, None
                
            except Exception as e:
                last_err = str(e)
                print(f"Hybrid Batch Rephrase Error (Attempt {attempt+1}): {e}")
                
        return None, last_err

    def restructure_pattern(self, raw_text):
        prompt = f"""
        A student wants to add a new GMAT practice pattern, but their description is messy.
        Restructure it into a professional GMAT pattern name and a concise description.
        Also, estimate the difficulty level from 1 to 5.
        
        User Input: "{raw_text}"
        
        Rules:
        1. "name": Professional, short name for the concept.
        2. "description": 1-2 sentences explaining what the pattern covers.
        3. "difficulty": 1-5 integer.
        
        Output format: JSON object with keys "name", "description", "difficulty".
        """
        
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a GMAT curriculum expert. Output only structured JSON."},
                    {"role": "user", "content": prompt}
                ],
                model=self.model,
                response_format={"type": "json_object"},
            )
            content = chat_completion.choices[0].message.content
            return json.loads(content), None
        except Exception as e:
            return None, str(e)

generator = QuestionGenerator()
