import math
import random


class PythagorasTheoremMixin:
    def generate_pythagoras_theorem(self):
        """Pattern: Pythagoras theorem"""
        # A person starts from home, walks X east, Y north/left etc.
        # Shortest distance = sqrt(dx^2 + dy^2)
        
        # Pick a pythagorean triplet or clean pair
        triplets = [(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 15, 17), (7, 24, 25), (9, 40, 41), (12, 35, 37)]
        dx, dy, dist = random.choice(triplets)
        
        if random.random() > 0.5: dx, dy = dy, dx
        
        # Decompose dx and dy into segments
        x1 = dx + random.randint(5, 15)
        y1 = dy + random.randint(5, 15)
        x2 = x1 - dx
        y_seg1 = random.randint(1, dy - 1)
        y_seg2 = dy - y_seg1
        
        question = f"Ravi started from his house and walked {x1}m East, then he takes a left turn and walked {y_seg1}m. Then again he takes a left turn and walks {x2}m. He finally takes a right turn and walked {y_seg2}m. What is the shortest distance between his house and the final point?"
        
        correct = f"{dist}m"
        options = [correct]
        while len(options) < 4:
            opt = f"{dist + random.choice([-2, -1, 1, 2, 5])}m"
            if opt not in options:
                options.append(opt)
        random.shuffle(options)
        
        return {
            "question_text": question,
            "options": options,
            "correct_option_index": options.index(correct),
            "explanation": f"Net displacement: East = {x1}-{x2} = {dx}m; North = {y_seg1}+{y_seg2} = {dy}m. Shortest distance = √( {dx}² + {dy}² ) = √({dx**2} + {dy**2}) = √{dx**2 + dy**2} = {dist}m.",
            "difficulty": 3
        }
