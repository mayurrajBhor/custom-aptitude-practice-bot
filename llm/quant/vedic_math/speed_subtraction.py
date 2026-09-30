import math
import random


class SpeedSubtractionMixin:
    def generate_vedic_subtraction(self, difficulty=1):
        """Speed subtraction drills using borrowing, complements, and near-base differences."""
        level = self._level(difficulty)
        sub_type = random.choice(["left_to_right", "base_complement", "near_base_difference", "missing_minuend"])

        if sub_type == "left_to_right":
            b = random.randint(5, 40) if level == 1 else random.randint(180, 790)
            correct = random.randint(10, 70) if level == 1 else random.randint(140, 860)
            a = b + correct
            question = f"Subtract mentally: {a} - {b}."
            explanation = f"Break {b} into easy parts and subtract left to right. {a} - {b} = {correct}."
            return self._mcq(question, correct, explanation, min(level, 3), [correct + 10, correct - 10, correct + 100, abs(correct - 100)])

        if sub_type == "base_complement":
            base = 100 if level <= 2 else random.choice([1000, 10000])
            n = random.randint(base // 5, base - (3 if level == 1 else 17))
            correct = base - n
            question = f"Using the all-from-9-and-last-from-10 idea, find {base} - {n}."
            explanation = f"Subtract each leading digit from 9 and the last non-zero digit from 10. Directly, {base} - {n} = {correct}."
            return self._mcq(question, correct, explanation, min(level, 3), [correct + 1, correct - 1, correct + 10, correct + 100])

        if sub_type == "near_base_difference":
            base = 100 if level <= 3 else 1000
            above = random.randint(1, 15) if level == 1 else random.randint(3, 48)
            below = random.randint(1, 15) if level == 1 else random.randint(4, 57)
            a = base + above
            b = base - below
            correct = above + below
            question = f"Find the difference quickly: {a} - {b}."
            explanation = f"{a} is {above} above {base}, while {b} is {below} below {base}. The difference is {above} + {below} = {correct}."
            return self._mcq(question, correct, explanation, min(level, 3), [abs(above - below), correct + 10, correct - 1, correct + 1])

        subtrahend = random.randint(10, 80) if level == 1 else random.randint(260, 880)
        difference = random.randint(10, 70) if level == 1 else random.randint(120, 760)
        minuend = subtrahend + difference
        question = f"If x - {subtrahend} = {difference}, what is x?"
        explanation = f"Add the subtrahend back to the difference: x = {difference} + {subtrahend} = {minuend}."
        return self._mcq(question, minuend, explanation, min(level, 3), [minuend + 10, minuend - 10, abs(subtrahend - difference), minuend + 100])
