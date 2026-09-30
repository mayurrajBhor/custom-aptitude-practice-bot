import math
import random


class MentalMultiplicationMixin:
    def generate_vedic_multiplication(self, difficulty=1):
        """Mental multiplication drills: near-base, by 11, split products, and 25/125 shortcuts."""
        level = self._level(difficulty)
        sub_type = random.choice(["vertical_crosswise", "near_base_100", "multiply_by_11", "split_multiplier", "multiply_by_25_125"])

        if sub_type == "vertical_crosswise":
            a = random.randint(11, 19) if level == 1 else random.randint(12, 98)
            b = random.randint(2, 9) if level == 1 else random.randint(12, 98)
            correct = a * b
            question = f"Use vertical-and-crosswise multiplication to calculate {a} x {b}."
            explanation = f"For two-digit multiplication, combine units, cross-products, and tens. Directly, {a} x {b} = {correct}."
            return self._mcq(question, correct, explanation, max(1, min(level, 3)), [correct + a, correct - b, correct + 10, correct - 10])

        if sub_type == "near_base_100":
            base = 10 if level == 1 else 100
            span = 4 if level == 1 else 18
            gap_a = random.choice([x for x in range(-span, span + 1) if x != 0])
            gap_b = random.choice([x for x in range(-span, span + 1) if x != 0])
            a = base + gap_a
            b = base + gap_b
            correct = a * b
            left = base + gap_a + gap_b
            question = f"Using the base-{base} method, calculate {a} x {b}."
            explanation = f"Cross-adjust around {base}: left part is {base} + ({gap_a}) + ({gap_b}) = {left}. The deviation product is {gap_a} x {gap_b} = {gap_a * gap_b}. Therefore {a} x {b} = {correct}."
            return self._mcq(question, correct, explanation, max(1, min(level, 3)), [left * base + abs(gap_a * gap_b), correct + base, correct - base, correct + gap_a * gap_b])

        if sub_type == "multiply_by_11":
            tens = random.randint(2, 8)
            ones = random.randint(1, max(1, 8 - tens))
            n = 10 * tens + ones
            correct = n * 11
            question = f"Find {n} x 11 using the insert-the-sum shortcut."
            explanation = f"For {n} x 11, keep the outer digits {tens} and {ones}, and insert their sum {tens + ones}. So {n} x 11 = {correct}."
            return self._mcq(question, correct, explanation, min(level, 2), [n * 10, correct + 11, correct - 11, int(f"{tens}{ones}{tens + ones}")])

        if sub_type == "split_multiplier":
            a = random.randint(11, 25) if level == 1 else random.randint(24, 89)
            tens = random.choice([10, 20]) if level == 1 else random.choice([20, 30, 40, 50, 60, 70, 80])
            ones = random.randint(1, 5) if level == 1 else random.randint(2, 9)
            b = tens + ones
            correct = a * b
            question = f"Use splitting to calculate {a} x {b}."
            explanation = f"Split {b} as {tens} + {ones}. Then {a} x {b} = {a} x {tens} + {a} x {ones} = {a * tens} + {a * ones} = {correct}."
            return self._mcq(question, correct, explanation, min(level, 3), [a * tens, a * ones, correct + a, correct - a])

        multiplier = 25 if level <= 2 else random.choice([25, 125])
        n = random.choice([4, 8, 12, 16, 20, 24, 28, 32]) if level == 1 else random.randint(12, 96)
        correct = n * multiplier
        question = f"Calculate {n} x {multiplier} using the shortcut."
        if multiplier == 25:
            explanation = f"Multiplying by 25 is the same as multiplying by 100 and dividing by 4: {n} x 25 = {n * 100} / 4 = {correct}."
        else:
            explanation = f"Multiplying by 125 is the same as multiplying by 1000 and dividing by 8: {n} x 125 = {n * 1000} / 8 = {correct}."
        return self._mcq(question, correct, explanation, min(level, 3), [correct + multiplier, correct - multiplier, n * 100, n * 10])
