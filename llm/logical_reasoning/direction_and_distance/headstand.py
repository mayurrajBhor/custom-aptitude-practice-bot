import math
import random


class HeadstandMixin:
    def generate_headstand(self):
        """Pattern: Headstand questions"""
        directions = ["North", "South", "East", "West"]
        facing = random.choice(directions)
        
        # Normal facing:
        # North -> L=West, R=East
        # South -> L=East, R=West
        # East -> L=North, R=South
        # West -> L=South, R=North
        
        # Headstand: Left and Right are SWAPPED relative to normal facing.
        # (A person facing North: Head is down, Feet are up. Eyes still face North.
        # But 'left' hand is now where 'right' used to be?)
        # Let's verify: Stand facing North. Left is West. Now flip upside down but keep facing North.
        # Your left hand is now on the East side.
        
        mapping = {
            "North": {"Left": "East", "Right": "West"},
            "South": {"Left": "West", "Right": "East"},
            "East": {"Left": "South", "Right": "North"},
            "West": {"Left": "North", "Right": "South"}
        }
        
        hand = random.choice(["Left", "Right"])
        correct = mapping[facing][hand]
        
        question = f"A person is performing headstand with his face towards the {facing}. In which direction will his {hand.lower()} hand be?"
        
        options = ["North", "South", "East", "West"]
        random.shuffle(options)
        
        return {
            "question_text": question,
            "options": options,
            "correct_option_index": options.index(correct),
            "explanation": f"When performing a headstand facing {facing}, the left and right positions are reversed compared to normal standing. Normally facing {facing}, the {hand.lower()} hand would be { 'West' if (facing=='North' and hand=='Left') else '...' }. In headstand, it is {correct}.",
            "difficulty": 3
        }
