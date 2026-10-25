import math
import random


class SpeedSubtractionMixin:
    def generate_vedic_subtraction(self, difficulty=1):
        """Speed subtraction drills using borrowing, complements, and near-base differences."""
        level = self._level(difficulty)
        sub_type = random.choice(["single_digit","two_digit_subtraction","Multi_type",])

        if sub_type == "two_digit_subtraction":
            b = random.randint(11, 79)
            diff = random.randint(11, 50)
            a = b + diff
            correct = diff
            question = f"Subtract mentally: {a} - {b}"
            tens = (b // 10) * 10
            units = b % 10
            explanation = (
                f"Subtract tens first, then units: "
                f"{a} - {tens} = {a - tens}, then {a - tens} - {units} = {correct}."
            )
            return self._mcq(question, correct,explanation,min(level, 3),[correct + 10, correct - 10, correct + 2, correct - 2],
            )
        
        if sub_type == "single_digit":
            b = random.randint(2, 9)
            a = random.randint(b, b + 9)  # guarantees positive result
            correct = a - b
            question = f"Subtract mentally: {a} - {b}"
            explanation = f"Subtract the single digits: {a} - {b} = {correct}."
            return self._mcq(
                question,
                correct,
                explanation,
                min(level, 3),
                [correct + 1, correct + 2, max(0, correct - 1), correct + 3],
            )

        if sub_type == "Multi_type":
            variant = random.choice([
                "round_and_adjust",
                "constant_difference",
                "base_complement",
                "near_base_difference",
                "reverse_digits_shortcut",
                "missing_term",
            ])
            # A. Round & Adjust: subtracting numbers ending in 8 or 9 (e.g. 345 - 98)
            if variant == "round_and_adjust":
                # Pick a subtrahend ending in 8 or 9 (like 19, 29, 48, 98, 199)
                round_base = random.choice(
                    [20, 30, 50, 100, 200]
                    if level <= 2
                    else [100, 200, 300, 500, 1000]
                )
                adjustment = random.choice([1, 2])
                b = round_base - adjustment
                a = round_base + random.randint(30, 150)
                correct = a - b
                question = f"Use Round & Adjust: {a} - {b}"
                explanation = (
                    f"Round {b} up to {round_base} (add {adjustment}):\n"
                    f"{a} - {round_base} = {a - round_base}.\n"
                    f"Add back the adjustment: {a - round_base} + {adjustment} = {correct}."
                )
                return self._mcq(
                    question,
                    correct,
                    explanation,
                    min(level, 3),
                    [correct + 10, correct - 10, correct + 2, correct - 2],
                )
            # B. Constant Difference Method (Equal Addition to eliminate borrowing)
            elif variant == "constant_difference":
                # Make subtrahend end in 7 or 8, so adding 2 or 3 makes it a round ten
                k = random.choice([1, 2, 3])
                base_ten = random.randint(2, 8) * 10
                b = base_ten - k
                a = b + random.randint(15, 65)
                correct = a - b
                question = f"Use Equal Addition: {a} - {b}"
                explanation = (
                    f"Add {k} to both numbers to avoid borrowing:\n"
                    f"({a} + {k}) - ({b} + {k}) = {a + k} - {base_ten} = {correct}."
                )
                return self._mcq(
                    question,
                    correct,
                    explanation,
                    min(level, 3),
                    [correct + 10, correct - 10, correct + k, correct - k],
                )
            # C. Base Complement (Nikhilam Sutra: All from 9, Last from 10)
            elif variant == "base_complement":
                base = 100 if level <= 2 else random.choice([1000, 10000])
                n = random.randint(base // 5, base - 17)
                correct = base - n
                question = f"Using All from 9 and Last from 10: {base} - {n} = ?"
                explanation = (
                    f"Subtract each leading digit from 9 and the last non-zero digit from 10.\n"
                    f"Directly: {base} - {n} = {correct}."
                )
                return self._mcq(
                    question,
                    correct,
                    explanation,
                    min(level, 3),
                    [correct + 1, correct - 1, correct + 10, correct + 100],
                )
            # D. Near Base Difference: (Base + x) - (Base - y) = x + y
            elif variant == "near_base_difference":
                base = 100 if level <= 2 else 1000
                above = random.randint(3, 25)
                below = random.randint(3, 25)
                a = base + above
                b = base - below
                correct = above + below
                question = f"Find the difference quickly: {a} - {b}"
                explanation = (
                    f"{a} is {above} above {base}, and {b} is {below} below {base}.\n"
                    f"The total distance is {above} + {below} = {correct}."
                )
                return self._mcq(
                    question,
                    correct,
                    explanation,
                    min(level, 3),
                    [
                        abs(above - below),
                        correct + 10,
                        correct - 10,
                        correct + 2,
                    ],
                )
            # E. Reverse Digits Shortcut: AB - BA = 9 * (A - B)
            elif variant == "reverse_digits_shortcut":
                d1 = random.randint(3, 9)
                d2 = random.randint(1, d1 - 1)
                a = d1 * 10 + d2
                b = d2 * 10 + d1
                diff_digits = d1 - d2
                correct = 9 * diff_digits
                question = f"Calculate mentally: {a} - {b}"
                explanation = (
                    f"For any two-digit number and its reverse, AB - BA = 9 × (A - B).\n"
                    f"Here, 9 × ({d1} - {d2}) = 9 × {diff_digits} = {correct}."
                )
                return self._mcq(
                    question,
                    correct,
                    explanation,
                    min(level, 3),
                    [
                        correct + 9,
                        correct - 9,
                        11 * diff_digits,
                        (d1 + d2) * 9,
                    ],
                )
            # F. Missing Term Equation (e.g. x - b = diff or a - x = diff)
            elif variant == "missing_term":
                subtrahend = random.randint(15, 75)
                difference = random.randint(15, 65)
                minuend = subtrahend + difference
                question = f"What number replaces x in: x - {subtrahend} = {difference}?"
                explanation = (
                    f"Add the subtrahend to the difference:\n"
                    f"x = {difference} + {subtrahend} = {minuend}."
                )
                return self._mcq(
                    question,
                    minuend,
                    explanation,
                    min(level, 3),
                    [
                        minuend + 10,
                        minuend - 10,
                        abs(subtrahend - difference),
                        minuend + 1,
                    ],
                )