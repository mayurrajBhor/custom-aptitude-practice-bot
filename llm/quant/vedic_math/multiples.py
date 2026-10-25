import math
import random


class MultiplesMixin:
    def generate_multiples(self, difficulty=2):
        """Pattern: Multiples and Divisibility Patterns"""
        level = self._level(difficulty)
        sub_type = random.choice([
            "counting_multiples_in_range",
            "common_multiples_and_intervals",
            "either_or_multiples",
            "consecutive_multiples_sum",
            "word_problems_multiples",
        ])

        if sub_type == "counting_multiples_in_range":
            m = random.choice([6, 7, 8, 9, 11, 13])
            start = random.choice([100, 120, 150, 200])
            end = random.choice([350, 400, 500, 600])
            count = (end // m) - ((start - 1) // m)
            question = f"How many positive multiples of {m} are there between {start} and {end} (inclusive)?"
            correct = str(count)
            distractors = [str(count - 1), str(count + 1), str(count + 2)]
            explanation = (
                f"Formula: Multiples in [A, B] = floor(B / m) - floor((A - 1) / m).\n"
                f"= floor({end} / {m}) - floor({start - 1} / {m}) = {end // m} - {(start - 1) // m} = {count}."
            )
            return self._mcq(question, correct, explanation, level, distractors)

        if sub_type == "common_multiples_and_intervals":
            a, b = random.choice([(6, 8), (8, 12), (9, 15), (12, 16), (15, 20)])
            lcm_ab = self._lcm(a, b)
            limit = random.choice([300, 400, 500, 600])
            count = limit // lcm_ab
            question = f"How many integers from 1 to {limit} (inclusive) are divisible by both {a} and {b}?"
            correct = str(count)
            distractors = [str(count - 2), str(count + 2), str(count + 5)]
            explanation = (
                f"Numbers divisible by both {a} and {b} must be multiples of LCM({a}, {b}).\n"
                f"LCM({a}, {b}) = {lcm_ab}.\n"
                f"Count of multiples up to {limit} = floor({limit} / {lcm_ab}) = {count}."
            )
            return self._mcq(question, correct, explanation, level, distractors)

        if sub_type == "either_or_multiples":
            a, b = random.choice([(4, 6), (6, 9), (4, 10), (6, 8)])
            lcm_ab = self._lcm(a, b)
            limit = random.choice([200, 300, 400])
            count_a = limit // a
            count_b = limit // b
            count_both = limit // lcm_ab
            total = count_a + count_b - count_both
            question = f"How many integers between 1 and {limit} (inclusive) are divisible by either {a} or {b} (or both)?"
            correct = str(total)
            distractors = [str(count_a + count_b), str(total - count_both), str(total + 5)]
            explanation = (
                f"Using the Principle of Inclusion-Exclusion: n(A or B) = n(A) + n(B) - n(A and B).\n"
                f"- Multiples of {a}: floor({limit} / {a}) = {count_a}\n"
                f"- Multiples of {b}: floor({limit} / {b}) = {count_b}\n"
                f"- Multiples of both (LCM {lcm_ab}): floor({limit} / {lcm_ab}) = {count_both}\n"
                f"Total = {count_a} + {count_b} - {count_both} = {total}."
            )
            return self._mcq(question, correct, explanation, level, distractors)

        if sub_type == "consecutive_multiples_sum":
            m = random.choice([6, 7, 8, 9, 12])
            n = random.choice([10, 12, 15, 20])
            total_sum = m * (n * (n + 1)) // 2
            question = f"What is the sum of the first {n} positive multiples of {m}?"
            correct = str(total_sum)
            distractors = [str(total_sum - m * 2), str(total_sum + m * 2), str(total_sum + m * 5)]
            explanation = (
                f"Sum = {m}(1 + 2 + 3 + ... + {n}) = {m} * [n(n + 1) / 2].\n"
                f"= {m} * [({n} * {n + 1}) / 2] = {m} * {(n * (n + 1)) // 2} = {total_sum}."
            )
            return self._mcq(question, correct, explanation, level, distractors)

        # word_problems_multiples
        intervals = random.choice([(12, 15), (15, 20), (20, 25), (18, 24)])
        t1, t2 = intervals
        lcm_val = self._lcm(t1, t2)
        question = f"Two automated safety drones patrol a perimeter: Drone A returns every {t1} minutes, and Drone B returns every {t2} minutes. If both drones depart together at 8:00 AM, after how many minutes will they next return to base at the same time?"
        correct = f"{lcm_val} minutes"
        distractors = [f"{t1 * t2} minutes", f"{lcm_val + t1} minutes", f"{lcm_val - t1} minutes"]
        explanation = (
            f"The drones will return to base together at intervals equal to the Least Common Multiple of their patrol periods.\n"
            f"LCM({t1}, {t2}) = {lcm_val} minutes."
        )
        return self._mcq(question, correct, explanation, level, distractors)
