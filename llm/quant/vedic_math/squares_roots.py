import math
import random


class SquaresRootsMixin:
    def generate_vedic_squares_roots(self, difficulty=1):
        """Squares and square-root recognition drills."""
        level = self._level(difficulty)
        sub_type = random.choice(["squares","square_ending_5", "near_base_square", "perfect_square_root", "integer_square_root"])

        if sub_type == "squares":
            n = random.randint(7, 30)
            correct = n * n
            question = f"Calculate {n}^2."
            explanation = f"{n} x {n} = {correct}."
            return self._mcq(question, correct, explanation, min(level, 3), [correct + 10, correct - 10, correct + 100, correct - 100]) 

        if sub_type == "square_ending_5":
            tens = random.randint(1, 3) if level == 1 else random.randint(2, 12)
            n = tens * 10 + 5
            correct = n * n
            question = f"Find {n}^2 using the ending-in-5 shortcut."
            explanation = f"For a number ending in 5, multiply {tens} by {tens + 1} and append 25: {tens} x {tens + 1} = {tens * (tens + 1)}, so {n}^2 = {correct}."
            return self._mcq(question, correct, explanation, min(level, 3), [correct + 100, correct - 100, int(f"{tens * tens}25"), correct + 25])

        if sub_type == "near_base_square":
            base = 10 if level == 1 else random.choice([50, 100])
            span = 4 if level == 1 else 15
            gap = random.choice([x for x in range(-span, span + 1) if x != 0])
            n = base + gap
            correct = n * n
            question = f"Estimate and calculate exactly using near-base squaring: {n}^2."
            explanation = f"Use (base + gap)^2. Here {n}^2 = {base}^2 + 2 x {base} x ({gap}) + ({gap})^2 = {correct}."
            return self._mcq(question, correct, explanation, max(1, min(level, 3)), [correct + abs(gap) * 10, correct - abs(gap) * 10, base * base + gap * gap, correct + 100])

        if sub_type == "perfect_square_root":
            root = random.randint(2, 12) if level == 1 else random.randint(12, 45)
            square = root * root
            question = f"Find the square root of {square}."
            explanation = f"{root} x {root} = {square}, so sqrt({square}) = {root}."
            return self._mcq(question, root, explanation, min(level, 3), [root + 1, root - 1, root + 2, max(1, root - 2)])

        root = random.randint(2, 12) if level == 1 else random.randint(15, 50)
        n = root * root + random.randint(1, 2 * root)
        correct = math.isqrt(n)
        question = f"What is the greatest integer less than or equal to sqrt({n})?"
        explanation = f"{correct}^2 = {correct * correct} and {correct + 1}^2 = {(correct + 1) * (correct + 1)}. Since {n} lies between them, the integer square root is {correct}."
        return self._mcq(question, correct, explanation, max(1, min(level, 3)), [correct + 1, correct - 1, correct + 2, max(1, correct - 2)])
