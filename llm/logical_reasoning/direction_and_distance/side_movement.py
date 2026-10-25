import math
import random


class SideMovementMixin:
    def generate_side_movement(self):
        """Pattern: Side movement"""
        # Walking along edges of a square/rectangle
        l, b = random.randint(10, 50), random.randint(10, 50)
        sides = ["length", "width", "length", "width"]
        question = f"A person walks along the boundary of a rectangular field of {l}m x {b}m. He starts from one corner and walks {l}m along the length, then turns left and walks {b}m, then turns left and walks {l}m. How far and in which direction is he from the starting point?"
        
        correct_dist = f"{b}m"
        # Start at (0,0). Move l East -> (l, 0). Left(North) b -> (l, b). Left(West) l -> (0, b).
        # From (0,0) to (0,b) is b meters North.
        correct_dir = "North"
        
        options = ["North", "South", "East", "West"]
        random.shuffle(options)
        opts = [f"{b}m {d}" for d in options]
        correct = f"{b}m {correct_dir}"
        
        return {
            "question_text": question,
            "options": opts,
            "correct_option_index": opts.index(correct),
            "explanation": f"The path forms three sides of a rectangle. He is now at the last corner, which is {b}m away in the perpendicular direction ({correct_dir}).",
            "difficulty": 2
        }
