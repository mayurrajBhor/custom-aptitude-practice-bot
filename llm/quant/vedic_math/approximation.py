import math
import random


class ApproximationMixin:
    def generate_vedic_approximation(self, difficulty=1):
        """Approximation, compatible numbers, and quick percent drills."""
        level = self._level(difficulty)
        sub_type = random.choice(["compatible_sum", "estimate_product", "estimate_division", "quick_percent"])

        if sub_type == "compatible_sum":
            values = [random.randint(12, 98) for _ in range(2 if level == 1 else 3)]
            rounded = [round(v, -1 if level == 1 else -2) for v in values]
            correct = sum(rounded)
            question = f"Estimate {' + '.join(map(str, values))} by rounding each number to the nearest {'ten' if level == 1 else 'hundred'}."
            explanation = f"The rounded values are {', '.join(map(str, rounded))}. Their sum is {correct}."
            return self._mcq(question, correct, explanation, 1, [sum(values), correct + 100, correct - 100, correct + 200])

        if sub_type == "estimate_product":
            a = random.randint(11, 29) if level == 1 else random.randint(24, 96)
            b = random.randint(2, 9) if level == 1 else random.randint(24, 96)
            ra = round(a, -1)
            rb = round(b, -1)
            correct = ra * rb
            question = f"Estimate {a} x {b} by rounding both numbers to the nearest ten."
            explanation = f"{a} rounds to {ra} and {b} rounds to {rb}. Estimated product = {ra} x {rb} = {correct}."
            return self._mcq(question, correct, explanation, 1, [a * b, correct + 100, correct - 100, ra + rb])

        if sub_type == "estimate_division":
            divisor = random.choice([2, 5, 10]) if level == 1 else random.choice([12, 15, 20, 25, 30, 40, 50])
            quotient = random.randint(2, 12) if level == 1 else random.randint(8, 40)
            compatible_dividend = divisor * quotient
            dividend = compatible_dividend + random.randint(-divisor // 2, divisor // 2)
            question = f"Estimate {dividend} / {divisor} using compatible numbers."
            explanation = f"{dividend} is close to {compatible_dividend}, and {compatible_dividend} / {divisor} = {quotient}. So the estimate is {quotient}."
            return self._mcq(question, quotient, explanation, 1, [quotient + 1, quotient - 1, quotient + 2, max(1, quotient - 2)])

        percent = random.choice([10, 20, 25, 50]) if level == 1 else random.choice([5, 10, 12.5, 15, 20, 25, 50, 75])
        base = random.randint(2, 20) * 10 if level == 1 else random.randint(8, 80) * 20
        correct_value = base * percent / 100
        correct = int(correct_value) if correct_value.is_integer() else correct_value
        question = f"Find {percent}% of {base} quickly."
        explanation = f"Use benchmark percentages: {percent}% of {base} = ({percent}/100) x {base} = {correct}."
        distractors = [correct_value + 10, max(0, correct_value - 10), correct_value * 2, correct_value / 2]
        distractors = [int(x) if float(x).is_integer() else x for x in distractors]
        return self._mcq(question, correct, explanation, 1, distractors)
