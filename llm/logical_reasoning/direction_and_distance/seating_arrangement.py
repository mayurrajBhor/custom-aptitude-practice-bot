import math
import random


class SeatingArrangementMixin:
    def generate_seating_arrangement(self):
        """Pattern: Seating arrangement"""
        # 5 people in a row or circle
        question = "Five boys P, Q, R, S, T are sitting in a row. P is to the right of Q, S is to the left of Q but to the right of R. P is to the left of T. Who is sitting in the middle?"
        # R - S - Q - P - T
        correct = "Q"
        options = ["P", "Q", "R", "S"]
        random.shuffle(options)
        
        return {
            "question_text": question,
            "options": options,
            "correct_option_index": options.index(correct),
            "explanation": "The arrangement from left to right is R, S, Q, P, T. Q is in the center.",
            "difficulty": 3
        }
