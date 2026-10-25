import math
import random


class PlayingCardsMixin:
    def generate_playing_cards(self):
        """Pattern: Playing cards"""
        # P, Q, R, S playing cards. Partners face each other.
        # P and R are partners, Q and S are partners.
        # S is to the right of P who faces North.
        
        p_facing = "North"
        # P faces North. S is to the right of P. In a circle, 'right' of P (facing North/Center) is East.
        # Wait, if they face center:
        # P(South side, faces North). S(West side, faces East) is to P's left. 
        # R(North side, faces South). Q(East side, faces West) is to P's right.
        # Let's use simple cardinal mapping.
        
        question = f"P, Q, R and S are playing a game of carrom/cards. P and R are partners; S and Q are partners. S is to the right of R who faces West. Which direction is Q facing?"
        
        # R faces West (stands on East side).
        # Partners R and P: P faces East (stands on West side).
        # To the right of R (facing West): Right is North.
        # So S is at North.
        # Partners S and Q: Q is at South.
        # Q faces North.
        
        correct = "North"
        options = ["North", "South", "East", "West"]
        random.shuffle(options)
        
        return {
            "question_text": question,
            "options": options,
            "correct_option_index": options.index(correct),
            "explanation": f"R faces West. R's partner P faces East. To the right of R (West) is North, where S sits. S's partner Q must sit at South, facing North.",
            "difficulty": 4
        }
