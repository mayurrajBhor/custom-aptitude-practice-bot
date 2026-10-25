import math
import random


class FastDivisionMixin:
    def generate_vedic_division(self, difficulty=1):
        """Fast division drills with exact division, remainders, and special divisors."""
        level = self._level(difficulty)
        sub_type = random.choice(["short_division", "remainder", "divide_by_25_125", "missing_dividend"])

        if sub_type == "short_division":
            divisor = random.randint(2, 9) if level == 1 else random.randint(6, 19)
            quotient = random.randint(2, 12) if level == 1 else random.randint(24, 140)
            dividend = divisor * quotient
            question = f"Divide quickly: {dividend} / {divisor}."
            explanation = f"Since {divisor} x {quotient} = {dividend}, the quotient is {quotient}."
            return self._mcq(question, quotient, explanation, min(level, 3), [quotient + 1, quotient - 1, quotient + divisor, quotient - divisor])

        if sub_type == "remainder":
            divisor = random.randint(3, 9) if level == 1 else random.randint(7, 23)
            quotient = random.randint(2, 12) if level == 1 else random.randint(20, 120)
            remainder = random.randint(1, divisor - 1)
            dividend = divisor * quotient + remainder
            question = f"What is the remainder when {dividend} is divided by {divisor}?"
            explanation = f"{dividend} = {divisor} x {quotient} + {remainder}. Therefore the remainder is {remainder}."
            return self._mcq(question, remainder, explanation, min(level, 3), [divisor - remainder, remainder + 1, quotient, divisor])

        if sub_type == "divide_by_25_125":
            divisor = 25 if level <= 2 else random.choice([25, 125])
            quotient = random.randint(2, 20) if level == 1 else random.randint(12, 160)
            dividend = divisor * quotient
            question = f"Calculate {dividend} / {divisor} using a speed division shortcut."
            if divisor == 25:
                explanation = f"Dividing by 25 is the same as multiplying by 4 and dividing by 100: {dividend} x 4 / 100 = {quotient}."
            else:
                explanation = f"Dividing by 125 is the same as multiplying by 8 and dividing by 1000: {dividend} x 8 / 1000 = {quotient}."
            return self._mcq(question, quotient, explanation, min(level, 3), [quotient + 4, quotient - 4, quotient * 2, max(1, quotient // 2)])

        divisor = random.randint(2, 9) if level == 1 else random.randint(6, 19)
        quotient = random.randint(2, 12) if level == 1 else random.randint(14, 90)
        remainder = random.randint(0, divisor - 1)
        dividend = divisor * quotient + remainder
        question = f"A number divided by {divisor} gives quotient {quotient} and remainder {remainder}. Find the number."
        explanation = f"Dividend = divisor x quotient + remainder = {divisor} x {quotient} + {remainder} = {dividend}."
        return self._mcq(question, dividend, explanation, min(level, 3), [divisor + quotient + remainder, dividend + divisor, dividend - divisor, quotient * max(1, remainder)])
