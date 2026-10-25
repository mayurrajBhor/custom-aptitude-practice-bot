import math
import random


class PrimeFactorizationMixin:
    def generate_prime_factorization(self, difficulty=2):
        """Pattern: Prime Factorization and Exponents"""
        level = self._level(difficulty)
        sub_type = random.choice([
            "canonical_decomposition",
            "highest_power_in_factorial",
            "missing_factor_for_perfect_power",
            "distinct_prime_factors",
            "algebraic_factorization",
        ])

        if sub_type == "canonical_decomposition":
            pool = [
                (252, "2^2 * 3^2 * 7", ["2^3 * 3 * 7", "2^2 * 3^3 * 7", "2 * 3^2 * 7^2"]),
                (360, "2^3 * 3^2 * 5", ["2^2 * 3^3 * 5", "2^3 * 3 * 5^2", "2^4 * 3^2 * 5"]),
                (504, "2^3 * 3^2 * 7", ["2^2 * 3^3 * 7", "2^3 * 3 * 7^2", "2^4 * 3 * 7"]),
                (540, "2^2 * 3^3 * 5", ["2^3 * 3^2 * 5", "2^2 * 3^2 * 5^2", "2 * 3^3 * 5^2"]),
                (840, "2^3 * 3 * 5 * 7", ["2^2 * 3^2 * 5 * 7", "2^3 * 3 * 5^2 * 7", "2^4 * 3 * 5 * 7"]),
            ]
            num, correct_decomp, dist = random.choice(pool)
            question = f"What is the canonical prime factorization of {num}?"
            correct = correct_decomp
            distractors = dist
            explanation = (
                f"Prime factorization steps for {num}:\n"
                f"Repeated division by prime factors (2, 3, 5, 7...) yields {correct_decomp}."
            )
            return self._mcq(question, correct, explanation, level, distractors)

        if sub_type == "highest_power_in_factorial":
            n = random.choice([30, 40, 50, 60, 75, 100])
            p = random.choice([3, 5])
            count = 0
            k = p
            terms = []
            while k <= n:
                term = n // k
                count += term
                terms.append(f"floor({n}/{k}) = {term}")
                k *= p
            if p == 5 and random.choice([True, False]):
                question = f"How many trailing zeros does {n}! ({n} factorial) have?"
                correct = str(count)
                distractors = [str(count - 2), str(count + 2), str(count + 4)]
                explanation = (
                    f"Trailing zeros in {n}! are determined by the highest power of 5 dividing {n}! (Legendre's formula):\n"
                    f"{' + '.join(terms)} => Total = {count} trailing zeros."
                )
            else:
                question = f"What is the highest power of {p} that completely divides {n}! ({n} factorial)?"
                correct = str(count)
                distractors = [str(count - 2), str(count + 2), str(count + 3)]
                explanation = (
                    f"Using Legendre's Formula for prime {p} dividing {n}!:\n"
                    f"Sum = {' + '.join(terms)} = {count}."
                )
            return self._mcq(question, correct, explanation, level, distractors)

        if sub_type == "missing_factor_for_perfect_power":
            power_type = random.choice(["square", "cube"])
            if power_type == "square":
                pool = [
                    (108, "2^2 * 3^3", 3),
                    (180, "2^2 * 3^2 * 5^1", 5),
                    (250, "2^1 * 5^3", 10),
                    (392, "2^3 * 7^2", 2),
                    (675, "3^3 * 5^2", 3),
                ]
                num, decomp, mult = random.choice(pool)
                question = f"What is the smallest positive integer by which {num} must be multiplied so that the product is a perfect square?"
                correct = str(mult)
                distractors = [str(mult * 2), str(mult * 3), str(mult + 1)]
                explanation = (
                    f"Factorization: {num} = {decomp}.\n"
                    f"To form a perfect square, every prime exponent must be an even number. "
                    f"Multiplying by {mult} balances all odd exponents to the next even power."
                )
            else:
                pool = [
                    (72, "2^3 * 3^2", 3),
                    (144, "2^4 * 3^2", 12),
                    (200, "2^3 * 5^2", 5),
                    (500, "2^2 * 5^3", 2),
                    (720, "2^4 * 3^2 * 5^1", 300),
                ]
                num, decomp, mult = random.choice(pool)
                question = f"What is the smallest positive integer by which {num} must be multiplied so that the product is a perfect cube?"
                correct = str(mult)
                distractors = [str(mult // 2 if mult > 4 else mult + 2), str(mult * 2), str(mult + 6)]
                explanation = (
                    f"Factorization: {num} = {decomp}.\n"
                    f"To form a perfect cube, every prime exponent must be a multiple of 3. "
                    f"The required multiplier is {mult}."
                )
            return self._mcq(question, correct, explanation, level, distractors)

        if sub_type == "distinct_prime_factors":
            pool = [
                (210, [2, 3, 5, 7], 4, 17),
                (330, [2, 3, 5, 11], 4, 21),
                (2310, [2, 3, 5, 7, 11], 5, 28),
                (1155, [3, 5, 7, 11], 4, 26),
                (1001, [7, 11, 13], 3, 31),
            ]
            num, p_list, count, p_sum = random.choice(pool)
            ask_sum = random.choice([True, False])
            if ask_sum:
                question = f"What is the sum of all DISTINCT prime factors of {num}?"
                correct = str(p_sum)
                distractors = [str(p_sum - 4), str(p_sum + 4), str(p_sum + 6)]
                explanation = (
                    f"The distinct prime factors of {num} are: {', '.join(map(str, p_list))}.\n"
                    f"Sum = {' + '.join(map(str, p_list))} = {p_sum}."
                )
            else:
                question = f"How many DISTINCT prime factors does {num} have?"
                correct = str(count)
                distractors = [str(count - 1), str(count + 1), str(count + 2)]
                explanation = (
                    f"Prime factorization of {num} = {' * '.join(map(str, p_list))}.\n"
                    f"There are {count} distinct prime factors."
                )
            return self._mcq(question, correct, explanation, level, distractors)

        # algebraic_factorization
        variant = random.choice(["ten_power_4_minus_1", "two_power_16_minus_1"])
        if variant == "ten_power_4_minus_1":
            question = "What is the largest prime factor of 10^4 - 1 (which equals 9,999)?"
            correct = "101"
            distractors = ["11", "37", "333"]
            explanation = (
                "10^4 - 1 = (10^2 - 1)(10^2 + 1) = (99)(101) = (9 * 11) * 101 = 3^2 * 11 * 101.\n"
                "The prime factors are 3, 11, and 101. The largest prime factor is 101."
            )
        else:
            question = "What is the largest prime factor of 2^16 - 1?"
            correct = "257"
            distractors = ["17", "31", "127"]
            explanation = (
                "Using difference of squares repeatedly:\n"
                "2^16 - 1 = (2^8 - 1)(2^8 + 1) = (2^4 - 1)(2^4 + 1)(256 + 1) = (15)(17)(257) = (3 * 5 * 17 * 257).\n"
                "The prime factors are 3, 5, 17, and 257. The largest prime factor is 257."
            )
        return self._mcq(question, correct, explanation, level, distractors)
