import math
import random


class ShadowBasedMixin:
    def generate_shadow_based(self):
        """Pattern: Shadow-based questions"""
        times = ["Morning", "Evening"]
        time = random.choice(times)
        
        # Morning: Sun is East, Shadow is West
        # Evening: Sun is West, Shadow is East
        sun_dir = "East" if time == "Morning" else "West"
        shadow_dir = "West" if time == "Morning" else "East"
        
        # Two people A and B are talking face to face.
        # A's shadow falls to the right of B.
        # If shadow is West, and it is to the right of B, then B is facing North.
        # (Facing North -> Right is East, Left is West. Wait. Facing North: Right is East? No.
        # N: L=W, R=E.
        # S: L=E, R=W.
        # So if shadow(West) is to the Right of B, B must be facing South.)
        
        facing_options = ["North", "South", "East", "West"]
        b_facing = random.choice(["North", "South"])
        
        if b_facing == "North":
            # Right is East, Left is West
            rel_side = "Left" if shadow_dir == "West" else "Right"
        else:
            # South: Right is West, Left is East
            rel_side = "Right" if shadow_dir == "West" else "Left"
            
        question = f"One {time}, Amit and Sunil were talking to each other face to face. Amit's shadow fell exactly to the {rel_side} of Sunil. Which direction was Amit facing?"
        
        # If Amit and Sunil are face to face, Amit faces opposite of Sunil.
        amit_facing = "South" if b_facing == "North" else "North"
        
        correct = amit_facing
        options = ["North", "South", "East", "West"]
        random.shuffle(options)
        
        return {
            "question_text": question,
            "options": options,
            "correct_option_index": options.index(correct),
            "explanation": f"In the {time}, the sun is in the {sun_dir}, so shadows fall to the {shadow_dir}. Since the shadow is to the {rel_side} of Sunil, Sunil must be facing {b_facing}. Amit is face-to-face with Sunil, so Amit faces {amit_facing}.",
            "difficulty": 4
        }
