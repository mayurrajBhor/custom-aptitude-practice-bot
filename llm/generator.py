import os
import random
import json
from groq import Groq
from dotenv import load_dotenv
from llm.hybrid_gen import hybrid_generator

load_dotenv()

class QuestionGenerator:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = "openai/gpt-oss-120b" # Latest model

    def _get_hybrid_type(self, pattern_name):
        """Map exact pattern names to hybrid generator methods (case-insensitive)."""
        pn = pattern_name.strip().lower()
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
        if pn == "fraction to decimal and vice versa":
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
        if pn == "clockwise and anti clockwise":
            return "clockwise_anticlockwise"
        if pn == "pythagoras theorem":
            return "pythagoras_theorem"
        if pn == "starting without direction":
            return "starting_without_direction"
        if pn == "moving towards different directions":
            return "moving_towards_direction"
        if pn == "interchange direction":
            return "interchange_direction"
        if pn == "find direction with respect to another point":
            return "find_direction_in_respect_to_another"
        if pn == "coded direction":
            return "coded_direction"
        if pn == "shadow-based questions":
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
        if pn == "when only one direction is given":
            return "one_direction_only"
        return None

    def generate_mcq(self, topic_name, pattern_name, pattern_description, difficulty, avoid_questions=None):
        # Check for Hybrid Patterns first
        hybrid_type = self._get_hybrid_type(pattern_name)
        if hybrid_type:
            hybrid_result = None
            if hybrid_type == "mixed_fraction": hybrid_result = hybrid_generator.generate_mixed_fraction()
            elif hybrid_type == "fraction_subtraction": hybrid_result = hybrid_generator.generate_fraction_subtraction()
            elif hybrid_type == "random_conv": hybrid_result = hybrid_generator.generate_random_conv()
            elif hybrid_type == "benchmark_conv": hybrid_result = hybrid_generator.generate_benchmark_conv()
            elif hybrid_type == "find_original_number": hybrid_result = hybrid_generator.generate_find_original_number()
            elif hybrid_type == "fraction_to_decimal": hybrid_result = hybrid_generator.generate_fraction_to_decimal()
            elif hybrid_type == "swap_percentage": hybrid_result = hybrid_generator.generate_swap_percentage()
            elif hybrid_type == "breakdown_percentage": hybrid_result = hybrid_generator.generate_breakdown_percentage()
            elif hybrid_type == "percentage_equations": hybrid_result = hybrid_generator.generate_percentage_equations()
            elif hybrid_type == "base_comparisons": hybrid_result = hybrid_generator.generate_base_comparisons()
            elif hybrid_type == "applied_percentages": hybrid_result = hybrid_generator.generate_applied_percentages()
            elif hybrid_type == "alligation_shifts": hybrid_result = hybrid_generator.generate_alligation_shifts()
            elif hybrid_type == "percentage_comparisons": hybrid_result = hybrid_generator.generate_percentage_comparisons()
            elif hybrid_type == "percentage_calculations": hybrid_result = hybrid_generator.generate_percentage_calculations()
            elif hybrid_type == "income_expenditure": hybrid_result = hybrid_generator.generate_income_expenditure()
            elif hybrid_type == "pass_fail_aggregates": hybrid_result = hybrid_generator.generate_pass_fail_aggregates()
            elif hybrid_type == "exam_scoring": hybrid_result = hybrid_generator.generate_exam_scoring()
            elif hybrid_type == "successive_changes": hybrid_result = hybrid_generator.generate_successive_net_change()
            elif hybrid_type == "clockwise_anticlockwise": hybrid_result = hybrid_generator.generate_clockwise_anticlockwise()
            elif hybrid_type == "pythagoras_theorem": hybrid_result = hybrid_generator.generate_pythagoras_theorem()
            elif hybrid_type == "starting_without_direction": hybrid_result = hybrid_generator.generate_starting_without_direction()
            elif hybrid_type == "moving_towards_direction": hybrid_result = hybrid_generator.generate_moving_towards_direction()
            elif hybrid_type == "interchange_direction": hybrid_result = hybrid_generator.generate_interchange_direction()
            elif hybrid_type == "find_direction_in_respect_to_another": hybrid_result = hybrid_generator.generate_find_direction_in_respect_to_another()
            elif hybrid_type == "coded_direction": hybrid_result = hybrid_generator.generate_coded_direction()
            elif hybrid_type == "shadow_based": hybrid_result = hybrid_generator.generate_shadow_based()
            elif hybrid_type == "headstand": hybrid_result = hybrid_generator.generate_headstand()
            elif hybrid_type == "final_facing": hybrid_result = hybrid_generator.generate_final_facing()
            elif hybrid_type == "side_movement": hybrid_result = hybrid_generator.generate_side_movement()
            elif hybrid_type == "direction_of_smoke": hybrid_result = hybrid_generator.generate_direction_of_smoke()
            elif hybrid_type == "playing_cards": hybrid_result = hybrid_generator.generate_playing_cards()
            elif hybrid_type == "seating_arrangement": hybrid_result = hybrid_generator.generate_seating_arrangement()
            elif hybrid_type == "based_on_turns": hybrid_result = hybrid_generator.generate_based_on_turns()
            elif hybrid_type == "one_direction_only": hybrid_result = hybrid_generator.generate_one_direction_only()

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
        
        Rules:
        1. Always provide exactly 4 options (A, B, C, D).
        2. Output format MUST be a valid JSON object with the following keys:
           "question_text": "text",
           "options": ["A", "B", "C", "D"],
           "correct_option_index": 0-3,
           "explanation": "detailed reasoning",
           "difficulty": integer 1-5
        
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

    def generate_batch(self, patterns_info, count=5):
        """
        patterns_info: List of dicts with {topic_name, name, description, difficulty, avoid_questions, id}
        """
        results = []
        ai_patterns = []
        
        # Split into Hybrid and AI
        hybrid_results = []
        for p in patterns_info:
            ht = self._get_hybrid_type(p['name'])
            if ht:
                hybrid_result = None
                if ht == "mixed_fraction": hybrid_result = hybrid_generator.generate_mixed_fraction()
                elif ht == "fraction_subtraction": hybrid_result = hybrid_generator.generate_fraction_subtraction()
                elif ht == "random_conv": hybrid_result = hybrid_generator.generate_random_conv()
                elif ht == "benchmark_conv": hybrid_result = hybrid_generator.generate_benchmark_conv()
                elif ht == "find_original_number": hybrid_result = hybrid_generator.generate_find_original_number()
                elif ht == "fraction_to_decimal": hybrid_result = hybrid_generator.generate_fraction_to_decimal()
                elif ht == "swap_percentage": hybrid_result = hybrid_generator.generate_swap_percentage()
                elif ht == "breakdown_percentage": hybrid_result = hybrid_generator.generate_breakdown_percentage()
                elif ht == "percentage_equations": hybrid_result = hybrid_generator.generate_percentage_equations()
                elif ht == "base_comparisons": hybrid_result = hybrid_generator.generate_base_comparisons()
                elif ht == "applied_percentages": hybrid_result = hybrid_generator.generate_applied_percentages()
                elif ht == "alligation_shifts": hybrid_result = hybrid_generator.generate_alligation_shifts()
                elif ht == "percentage_comparisons": hybrid_result = hybrid_generator.generate_percentage_comparisons()
                elif ht == "percentage_calculations": hybrid_result = hybrid_generator.generate_percentage_calculations()
                elif ht == "income_expenditure": hybrid_result = hybrid_generator.generate_income_expenditure()
                elif ht == "pass_fail_aggregates": hybrid_result = hybrid_generator.generate_pass_fail_aggregates()
                elif ht == "exam_scoring": hybrid_result = hybrid_generator.generate_exam_scoring()
                elif ht == "successive_changes": hybrid_result = hybrid_generator.generate_successive_net_change()
                elif ht == "clockwise_anticlockwise": hybrid_result = hybrid_generator.generate_clockwise_anticlockwise()
                elif ht == "pythagoras_theorem": hybrid_result = hybrid_generator.generate_pythagoras_theorem()
                elif ht == "starting_without_direction": hybrid_result = hybrid_generator.generate_starting_without_direction()
                elif ht == "moving_towards_direction": hybrid_result = hybrid_generator.generate_moving_towards_direction()
                elif ht == "interchange_direction": hybrid_result = hybrid_generator.generate_interchange_direction()
                elif ht == "find_direction_in_respect_to_another": hybrid_result = hybrid_generator.generate_find_direction_in_respect_to_another()
                elif ht == "coded_direction": hybrid_result = hybrid_generator.generate_coded_direction()
                elif ht == "shadow_based": hybrid_result = hybrid_generator.generate_shadow_based()
                elif ht == "headstand": hybrid_result = hybrid_generator.generate_headstand()
                elif ht == "final_facing": hybrid_result = hybrid_generator.generate_final_facing()
                elif ht == "side_movement": hybrid_result = hybrid_generator.generate_side_movement()
                elif ht == "direction_of_smoke": hybrid_result = hybrid_generator.generate_direction_of_smoke()
                elif ht == "playing_cards": hybrid_result = hybrid_generator.generate_playing_cards()
                elif ht == "seating_arrangement": hybrid_result = hybrid_generator.generate_seating_arrangement()
                elif ht == "based_on_turns": hybrid_result = hybrid_generator.generate_based_on_turns()
                elif ht == "one_direction_only": hybrid_result = hybrid_generator.generate_one_direction_only()
                
                if hybrid_result:
                    hybrid_results.append({**hybrid_result, "pattern_id": p['id']})
            else:
                ai_patterns.append(p)
                
        # Batch rephrase all hybrid results at once
        if hybrid_results:
            hybrid_results, err = self._batch_rephrase_hybrid(hybrid_results)
            if err:
                return results, f"Batch Rephrasing Error: {err}"
            results.extend(hybrid_results)

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
            2. You MAY change units (e.g., from "dollars" to "galactic credits" or "km" to "light years") if it fits the new theme, but the raw numbers must be invariant.
            3. DO NOT change or reorder the multiple choice options.
            4. You must output a JSON object with strictly these keys:
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
        
        return None, last_err # Propagate the error instead of falling back

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
                    {"role": "system", "content": "You are a Match Consistency Checker. YOUR ONLY JOB is to ensure that the DIGITS and NUMBERS (like 20, 10, 50%) are the same in both versions. DO NOT care about currency, names, units, or themes. IF THE NUMBERS MATCH, IS_VALID IS TRUE."},
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
            2. DO NOT change the multiple choice options.
            3. Output a single JSON object with a "replacements" array. 
            
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
                if not isinstance(res, dict):
                    print(f"Batch Rephrase Error: Expected dict, got {type(res).__name__}")
                    continue
                    
                replacements = res.get("replacements", [])
                if not isinstance(replacements, list):
                    print(f"Batch Rephrase Error: 'replacements' should be a list, got {type(replacements).__name__}")
                    continue

                if len(replacements) == len(hybrid_list):
                    all_valid = True
                    reasons = []
                    for i in range(len(hybrid_list)):
                        # Ensure item is a dict
                        rep_item = replacements[i]
                        if not isinstance(rep_item, dict):
                            reasons.append(f"Item {i} is not a dictionary")
                            all_valid = False
                            break
                            
                        # Verify each one
                        is_valid, reason = self._verify_rephrased_content(hybrid_list[i]['question_text'], rep_item.get('question_text', ''))
                        if not is_valid:
                            reasons.append(f"Item {i}: {reason}")
                            all_valid = False
                            break
                    
                    if all_valid:
                        for i in range(len(hybrid_list)):
                            hybrid_list[i]["question_text"] = replacements[i].get("question_text", hybrid_list[i]["question_text"])
                            hybrid_list[i]["explanation"] = replacements[i].get("explanation", hybrid_list[i]["explanation"])
                        return hybrid_list, None
                    else:
                        last_err = "; ".join(reasons)
                        print(f"Batch Rephrase Verification Failed (Attempt {attempt+1}): {last_err}")
                
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
