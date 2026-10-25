import math
import random


class OneDirectionOnlyMixin:
    def generate_one_direction_only(self):
        """Pattern: When only one direction is given"""
        # Traditional logic puzzle
        question = "To reach his school, Rahul goes 5km towards North, then turns left and goes 10km, then turns left again and goes 5km. In which direction is the school from his starting point?"
        # N 5, L(W) 10, L(S) 5 -> Net West 10.
        correct = "West"
        options = ["North", "South", "East", "West"]
        random.shuffle(options)
        return {
            "question_text": question,
            "options": options,
            "correct_option_index": options.index(correct),
            "explanation": "He moved 5km North and 5km South, cancelling the vertical movement. He is 10km West of the start.",
            "difficulty": 2
        }
