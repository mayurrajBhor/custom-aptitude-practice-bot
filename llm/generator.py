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
        return None

    def generate_mcq(self, topic_name, pattern_name, pattern_description, difficulty, avoid_questions=None):
        # Check for Hybrid Patterns first
        hybrid_type = self._get_hybrid_type(pattern_name)
        if hybrid_type == "mixed_fraction":
            return hybrid_generator.generate_mixed_fraction(), None
        elif hybrid_type == "fraction_subtraction":
            return hybrid_generator.generate_fraction_subtraction(), None
        elif hybrid_type == "random_conv":
            return hybrid_generator.generate_random_conv(), None
        elif hybrid_type == "benchmark_conv":
            return hybrid_generator.generate_benchmark_conv(), None
        elif hybrid_type == "find_original_number":
            return hybrid_generator.generate_find_original_number(), None
        elif hybrid_type == "fraction_to_decimal":
            return hybrid_generator.generate_fraction_to_decimal(), None
        elif hybrid_type == "swap_percentage":
            return hybrid_generator.generate_swap_percentage(), None
        elif hybrid_type == "breakdown_percentage":
            return hybrid_generator.generate_breakdown_percentage(), None
        elif hybrid_type == "percentage_equations":
            return hybrid_generator.generate_percentage_equations(), None
        elif hybrid_type == "base_comparisons":
            return hybrid_generator.generate_base_comparisons(), None
        elif hybrid_type == "applied_percentages":
            return hybrid_generator.generate_applied_percentages(), None

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
        for p in patterns_info:
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
