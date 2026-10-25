import math
import random


class DivisibilityRulesMixin:
    def generate_vedic_divisibility(self, difficulty=1):
        """Divisibility-rule drills across common aptitude divisors."""
        level = self._level(difficulty)
        sub_type = random.choice(["rules_3_9", "rules_4_8", "rule_11", "combined_rules"])

        if sub_type == "rules_3_9":
            n = random.randint(100, 999) if level == 1 else random.randint(1000, 99999)
            digit_sum = sum(int(d) for d in str(n))
            divisible_by_3 = digit_sum % 3 == 0
            divisible_by_9 = digit_sum % 9 == 0
            if divisible_by_9:
                correct = "3 and 9"
            elif divisible_by_3:
                correct = "3 only"
            else:
                correct = "neither 3 nor 9"
            question = f"The digit sum of {n} is {digit_sum}. By divisibility rules, {n} is divisible by which option?"
            explanation = f"A number is divisible by 3 or 9 when its digit sum is divisible by 3 or 9. Here the digit sum is {digit_sum}, so the answer is {correct}."
            return self._mcq(question, correct, explanation, min(level, 3), ["3 only", "9 only", "3 and 9", "neither 3 nor 9"])

        if sub_type == "rules_4_8":
            n = random.randint(100, 999) if level == 1 else random.randint(1000, 99999)
            last_two = n % 100
            last_three = n % 1000
            div4 = last_two % 4 == 0
            div8 = last_three % 8 == 0
            if div8:
                correct = "4 and 8"
            elif div4:
                correct = "4 only"
            else:
                correct = "neither 4 nor 8"
            question = f"Using the last digits, decide whether {n} is divisible by 4, 8, both, or neither."
            explanation = f"For 4, check the last two digits: {last_two}. For 8, check the last three digits: {last_three}. Therefore the answer is {correct}."
            return self._mcq(question, correct, explanation, min(level, 3), ["4 only", "8 only", "4 and 8", "neither 4 nor 8"])

        if sub_type == "rule_11":
            n = random.randint(100, 999) if level == 1 else random.randint(10000, 999999)
            digits = [int(d) for d in str(n)]
            alternating = abs(sum(digits[::2]) - sum(digits[1::2]))
            correct = alternating % 11
            question = f"For the divisibility-by-11 test on {n}, what is the remainder when the alternating digit-sum difference is divided by 11?"
            explanation = f"Alternating digit sums give |{sum(digits[::2])} - {sum(digits[1::2])}| = {alternating}. {alternating} mod 11 = {correct}."
            return self._mcq(question, correct, explanation, max(1, min(level, 3)), [(correct + 1) % 11, (correct + 2) % 11, alternating, 11 - correct if correct else 11])

        divisors = [2, 3, 5, 10] if level == 1 else [3, 4, 5, 6, 8, 9, 10, 11, 12, 15]
        n = random.randint(100, 999) if level == 1 else random.randint(1000, 99999)
        correct = sum(1 for divisor in divisors if n % divisor == 0)
        question = f"How many numbers in this list divide {n}: {', '.join(map(str, divisors))}?"
        explanation = f"Test each divisor using its rule. The count of divisors from the list that divide {n} exactly is {correct}."
        return self._mcq(question, correct, explanation, max(1, min(level, 3)), [correct + 1, max(0, correct - 1), correct + 2, max(0, correct - 2)])
