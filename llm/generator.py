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
        if pn == "fraction to decimal":
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

            if hybrid_result:
                # Intercept the hybrid math and pass through LLM for rephrasing
                rephrased = self._rephrase_hybrid_question(hybrid_result)
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
                
                if hybrid_result:
                    hybrid_results.append({**hybrid_result, "pattern_id": p['id']})
            else:
                ai_patterns.append(p)
                
        # Batch rephrase all hybrid results at once
        if hybrid_results:
            hybrid_results = self._batch_rephrase_hybrid(hybrid_results)
            results.extend(hybrid_results)
            ht = self._get_hybrid_type(p['name'])
            if ht == "mixed_fraction":
                results.append({**hybrid_generator.generate_mixed_fraction(), "pattern_id": p['id']})
            elif ht == "fraction_subtraction":
                results.append({**hybrid_generator.generate_fraction_subtraction(), "pattern_id": p['id']})
            elif ht == "random_conv":
                results.append({**hybrid_generator.generate_random_conv(), "pattern_id": p['id']})
            elif ht == "benchmark_conv":
                results.append({**hybrid_generator.generate_benchmark_conv(), "pattern_id": p['id']})
            elif ht == "find_original_number":
                results.append({**hybrid_generator.generate_find_original_number(), "pattern_id": p['id']})
            elif ht == "fraction_to_decimal":
                results.append({**hybrid_generator.generate_fraction_to_decimal(), "pattern_id": p['id']})
            elif ht == "swap_percentage":
                results.append({**hybrid_generator.generate_swap_percentage(), "pattern_id": p['id']})
            elif ht == "breakdown_percentage":
                results.append({**hybrid_generator.generate_breakdown_percentage(), "pattern_id": p['id']})
            elif ht == "percentage_equations":
                results.append({**hybrid_generator.generate_percentage_equations(), "pattern_id": p['id']})
            elif ht == "base_comparisons":
                results.append({**hybrid_generator.generate_base_comparisons(), "pattern_id": p['id']})
            elif ht == "applied_percentages":
                results.append({**hybrid_generator.generate_applied_percentages(), "pattern_id": p['id']})
            elif ht == "alligation_shifts":
                results.append({**hybrid_generator.generate_alligation_shifts(), "pattern_id": p['id']})
            elif ht == "percentage_comparisons":
                results.append({**hybrid_generator.generate_percentage_comparisons(), "pattern_id": p['id']})
            elif ht == "percentage_calculations":
                results.append({**hybrid_generator.generate_percentage_calculations(), "pattern_id": p['id']})
            elif ht == "income_expenditure":
                results.append({**hybrid_generator.generate_income_expenditure(), "pattern_id": p['id']})
            elif ht == "pass_fail_aggregates":
                results.append({**hybrid_generator.generate_pass_fail_aggregates(), "pattern_id": p['id']})
            else:
                ai_patterns.append(p)

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
                results.extend(batch_res["questions"])
            elif isinstance(batch_res, list):
                results.extend(batch_res)
            
            return results, None
        except Exception as e:
            return results, str(e)

    def _rephrase_hybrid_question(self, hybrid_data):
        """Takes a math-generated question dict and uses the LLM to rewrite the linguistic framing."""
        if not os.getenv("GROQ_API_KEY"):
            return hybrid_data # Graceful fallback if no key
            
        prompt = f"""
        You are a GMAT Question Rephraser.
        Take the following functionally correct math question and rewrite the storyline/context completely.
        Use a creative new theme (e.g. spaceships, business budgets, ancient kingdoms, racecars, obscure professions, etc).
        
        Original Question: {hybrid_data['question_text']}
        Original Explanation: {hybrid_data['explanation']}
        
        CRITICAL RULES:
        1. DO NOT change any numbers or mathematical relationships.
        2. DO NOT change or reorder the multiple choice options.
        3. You must output a JSON object with strictly these keys:
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
            val = json.loads(chat.choices[0].message.content)
            
            # Merge the new text over the original, preserving options/correct_index/difficulty/pattern_id
            return {
                **hybrid_data,
                "question_text": val.get("question_text", hybrid_data["question_text"]),
                "explanation": val.get("explanation", hybrid_data["explanation"])
            }
        except Exception as e:
            print(f"Hybrid Rephrase Error: {e}")
            return hybrid_data # Graceful fallback

    def _batch_rephrase_hybrid(self, hybrid_list):
        """Takes a list of hybrid question dicts and rewrites them all in one LLM call for speed."""
        if not hybrid_list or not os.getenv("GROQ_API_KEY"):
            return hybrid_list
            
        original_texts = ""
        for i, h in enumerate(hybrid_list):
            original_texts += f"\\n--- ITEM {i} ---\\nQuestion: {h['question_text']}\\nExplanation: {h['explanation']}"
            
        prompt = f"""
        You are a GMAT Question Rephraser.
        I will give you {len(hybrid_list)} mathematically correct word problems.
        For EACH one, rewrite the storyline/context completely using a creative new theme (e.g. spaceships, business budgets, ancient kingdoms, racecars).
        
        CRITICAL RULES:
        1. DO NOT change any numbers or mathematical relationships.
        2. DO NOT change the multiple choice options.
        3. Output a single JSON object with a "replacements" array. Each object in the array MUST correspond to the input items in order.
        
        Format:
        {{
            "replacements": [
                {{
                    "question_text": "new rewritten text for ITEM 0",
                    "explanation": "explanation adapted to new theme but keeping exact same math/formulas"
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
            res = json.loads(chat.choices[0].message.content)
            replacements = res.get("replacements", [])
            
            if len(replacements) == len(hybrid_list):
                for i in range(len(hybrid_list)):
                    hybrid_list[i]["question_text"] = replacements[i].get("question_text", hybrid_list[i]["question_text"])
                    hybrid_list[i]["explanation"] = replacements[i].get("explanation", hybrid_list[i]["explanation"])
        except Exception as e:
            print(f"Hybrid Batch Rephrase Error: {e}")
            
        return hybrid_list

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
