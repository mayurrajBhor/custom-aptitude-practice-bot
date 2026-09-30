import math
import random


class FactorsMixin:
    def generate_factors(self, difficulty=2):
        """Pattern: Factors and Divisors"""
        level = self._level(difficulty)
        sub_type = random.choice([
            "total_number_of_factors",
            "sum_of_factors",
            "odd_and_even_factors",
            "factor_pairs_and_products",
            "perfect_square_factors",
        ])

        if sub_type == "total_number_of_factors":
            pool = [
                (72, {"2": 3, "3": 2}, 12),
                (120, {"2": 3, "3": 1, "5": 1}, 16),
                (180, {"2": 2, "3": 2, "5": 1}, 18),
                (240, {"2": 4, "3": 1, "5": 1}, 20),
                (360, {"2": 3, "3": 2, "5": 1}, 24),
                (720, {"2": 4, "3": 2, "5": 1}, 30),
                (1080, {"2": 3, "3": 3, "5": 1}, 32),
            ]
            num, factors_dict, total_factors = random.choice(pool)
            question = f"Find the total number of positive factors (divisors) of {num}."
            correct = str(total_factors)
            distractors = [str(total_factors - 4), str(total_factors + 4), str(total_factors + 6)]
            decomp_str = " * ".join(f"{p}^{exp}" for p, exp in factors_dict.items())
            formula_str = " * ".join(f"({exp} + 1)" for exp in factors_dict.values())
            explanation = (
                f"Step 1: Find the prime factorization of {num} = {decomp_str}.\n"
                f"Step 2: Apply the divisor formula: Total Factors = {formula_str} = {total_factors}."
            )
            return self._mcq(question, correct, explanation, level, distractors)

        if sub_type == "sum_of_factors":
            pool = [
                (48, {"2": 4, "3": 1}, 124),
                (60, {"2": 2, "3": 1, "5": 1}, 168),
                (72, {"2": 3, "3": 2}, 195),
                (96, {"2": 5, "3": 1}, 252),
                (108, {"2": 2, "3": 3}, 280),
                (120, {"2": 3, "3": 1, "5": 1}, 360),
            ]
            num, factors_dict, factor_sum = random.choice(pool)
            question = f"What is the sum of all positive factors (divisors) of {num}?"
            correct = str(factor_sum)
            distractors = [str(factor_sum - 20), str(factor_sum + 24), str(factor_sum + 36)]
            decomp_str = " * ".join(f"{p}^{exp}" for p, exp in factors_dict.items())
            parts = []
            for p, exp in factors_dict.items():
                p_int = int(p)
                p_sum = sum(p_int ** i for i in range(exp + 1))
                parts.append(str(p_sum))
            explanation = (
                f"Step 1: Prime factorization of {num} = {decomp_str}.\n"
                f"Step 2: Sum of divisors = {' * '.join(parts)} = {factor_sum}."
            )
            return self._mcq(question, correct, explanation, level, distractors)

        if sub_type == "odd_and_even_factors":
            pool = [
                (120, 4, 12, 16),
                (180, 6, 12, 18),
                (240, 4, 16, 20),
                (360, 6, 18, 24),
                (480, 4, 20, 24),
            ]
            num, odd_count, even_count, total = random.choice(pool)
            ask_even = random.choice([True, False])
            if ask_even:
                question = f"How many EVEN positive factors does the number {num} have?"
                correct = str(even_count)
                distractors = [str(odd_count), str(total), str(even_count - 2)]
                explanation = (
                    f"Total factors of {num} = {total}.\n"
                    f"To find odd factors, ignore all powers of 2. Number of odd factors = {odd_count}.\n"
                    f"Number of even factors = Total Factors - Odd Factors = {total} - {odd_count} = {even_count}."
                )
            else:
                question = f"How many ODD positive factors does the number {num} have?"
                correct = str(odd_count)
                distractors = [str(even_count), str(total), str(odd_count + 2)]
                explanation = (
                    f"To find the number of odd factors of {num}, completely exclude the prime factor 2 from the factorization.\n"
                    f"The remaining prime factors give {odd_count} odd factors."
                )
            return self._mcq(question, correct, explanation, level, distractors)

        if sub_type == "factor_pairs_and_products":
            pool = [
                (120, 16, 8, False),
                (144, 15, 8, True),
                (180, 18, 9, False),
                (225, 9, 5, True),
                (360, 24, 12, False),
            ]
            num, total_f, pairs, is_square = random.choice(pool)
            question = f"In how many ways can {num} be expressed as a product of two positive integer factors?"
            correct = str(pairs)
            distractors = [str(pairs - 2), str(pairs + 1), str(total_f)]
            if is_square:
                explanation = (
                    f"Total factors of {num} = {total_f} (since {num} is a perfect square, {math.isqrt(num)}^2).\n"
                    f"Ways to express as product of two factors = (Total Factors + 1) / 2 = ({total_f} + 1) / 2 = {pairs}."
                )
            else:
                explanation = (
                    f"Total factors of {num} = {total_f}.\n"
                    f"Each pair of factors (a, b) produces a * b = {num}.\n"
                    f"Number of factor pairs = Total Factors / 2 = {total_f} / 2 = {pairs}."
                )
            return self._mcq(question, correct, explanation, level, distractors)

        # perfect_square_factors
        pool = [
            ("2^4 * 3^2 * 5^1", 6),
            ("2^5 * 3^4 * 5^2", 18),
            ("2^6 * 3^3 * 5^2", 16),
            ("2^3 * 3^4 * 7^2", 12),
        ]
        decomp, count_val = random.choice(pool)
        question = f"How many positive factors of the number N = {decomp} are perfect squares?"
        correct = str(count_val)
        distractors = [str(count_val - 4), str(count_val + 4), str(count_val + 6)]
        explanation = (
            f"A factor is a perfect square if all the exponents in its prime factorization are even multiples of 2.\n"
            f"For each prime p^k, the available even exponents are 0, 2, 4, ... up to k.\n"
            f"Multiplying the choices of even exponents gives: {correct} perfect square factors."
        )
        return self._mcq(question, correct, explanation, level, distractors)
