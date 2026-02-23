import os
import random
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class QuestionGenerator:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = "openai/gpt-oss-120b" # Latest model

    def generate_mcq(self, topic_name, pattern_name, pattern_description, difficulty, avoid_questions=None):
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
        1. Always provide exactly 5 options (A, B, C, D, E).
        2. Output format MUST be a valid JSON object with the following keys:
           "question_text": "text",
           "options": ["A", "B", "C", "D", "E"],
           "correct_option_index": 0-4,
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
        patterns_info: List of dicts with {topic_name, name, description, difficulty, avoid_questions}
        """
        if not os.getenv("GROQ_API_KEY"):
            return None, "Groq API key is missing."

        patterns_text = ""
        for i, p in enumerate(patterns_info):
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
        Your task is to generate exactly {count} unique, high-quality, exam-standard MCQs.
        
        CRITICAL INSTRUCTIONS:
        1. For EACH Pattern ID listed below, you must generate EXACTLY ONE original question.
        2. EXAM STANDARDS: Use complex, multi-step reasoning. Ensure distractors are plausible and based on common student errors.
        3. EXPLANATIONS: Provide deep reasoning for the correct answer and clear refutations for all wrong options.

        PATTERNS TO USE:
        {patterns_text}

        Rules:
        1. Always provide 5 options (A, B, C, D, E).
        2. Output format MUST be a valid JSON object with a key "questions" containing an array of objects.
        
        Each object should have:
           "question_text": "text",
           "options": ["A", "B", "C", "D", "E"],
           "correct_option_index": 0-4 Integer,
           "explanation": "detailed reasoning",
           "difficulty": integer 1-5,
           "pattern_id": integer (MUST MATCH THE PATTERN ID FROM THE LIST ABOVE)

        Example response format:
        {{
          "questions": [
            {{"pattern_id": 12, "question_text": "...", ...}},
            ...
          ]
        }}
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
            # Some models/proxies might need specific handling, but we rely on standard groq client here
            content = chat_completion.choices[0].message.content
            # Groq model 'openai/gpt-oss-120b' might require JSON mode via response_format
            # but usually it's better to just parse if the prompt is strong.
            
            result = json.loads(content)
            # If the model wraps it in a key like "questions", extract it
            if isinstance(result, dict) and "questions" in result:
                return result["questions"], None
            elif isinstance(result, list):
                return result, None
            return [result], None # Fallback if single object
        except Exception as e:
            return None, str(e)

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
