import math
import random
from fractions import Fraction


class BaseGenerator:
    def __init__(self):
        # Master list of GMAT benchmark fractions requested by user
        self.benchmarks = [
            (1, 2, "50%"), (1, 3, "33.33%"), (1, 4, "25%"), (1, 5, "20%"),
            (1, 6, "16.67%"), (1, 7, "14.28%"), (1, 8, "12.5%"), (1, 9, "11.11%"), 
            (1, 10, "10%"), (1, 11, "9.09%"), (1, 12, "8.33%"), (1, 13, "7.69%"), 
            (1, 14, "7.14%"), (1, 15, "6.67%"), (1, 16, "6.25%"), (1, 17, "5.88%"), 
            (1, 18, "5.55%"), (1, 19, "5.26%"), (1, 20, "5%"),
            (1, 25, "4%"), (1, 30, "3.33%"), (1, 40, "2.5%"), (1, 50, "2%"),
            (3, 8, "37.5%"), (5, 8, "62.5%"), 
            (4, 7, "57.14%"), (5, 7, "71.42%"), 
            (5, 6, "83.33%")
        ]

    def _options(self, correct, distractors):
        correct = str(correct)
        options = [correct]
        for value in distractors:
            option = str(value)
            if option != correct and option not in options:
                options.append(option)
            if len(options) == 4:
                break

        delta = 1
        while len(options) < 4:
            try:
                option = str(int(float(correct)) + delta)
            except ValueError:
                option = f"{correct} + {delta}"
            if option not in options:
                options.append(option)
            delta += 1

        random.shuffle(options)
        return options, options.index(correct)

    def _mcq(self, question, correct, explanation, difficulty=2, distractors=None):
        options, index = self._options(correct, distractors or [])
        return {
            "question_text": question,
            "options": options,
            "correct_option_index": index,
            "explanation": explanation,
            "difficulty": difficulty,
        }

    def _level(self, difficulty):
        try:
            level = int(round(float(difficulty)))
        except (TypeError, ValueError):
            level = 1
        return max(1, min(5, level))

    def _is_prime(self, n):
        if n < 2:
            return False
        if n in (2, 3):
            return True
        if n % 2 == 0 or n % 3 == 0:
            return False
        i = 5
        while i * i <= n:
            if n % i == 0 or n % (i + 2) == 0:
                return False
            i += 6
        return True

    def _prime_factors(self, n):
        factors = {}
        d = 2
        while d * d <= n:
            while n % d == 0:
                factors[d] = factors.get(d, 0) + 1
                n //= d
            d += 1
        if n > 1:
            factors[n] = factors.get(n, 0) + 1
        return factors

    def _lcm(self, a, b):
        return (a * b) // math.gcd(a, b)

    def _lcm_list(self, nums):
        res = nums[0]
        for n in nums[1:]:
            res = self._lcm(res, n)
        return res
