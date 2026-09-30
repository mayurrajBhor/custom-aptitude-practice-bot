import math
import random


class PrimeCompositeMixin:
    def generate_prime_composite(self, difficulty=2):
        """Pattern: Prime/Composite Properties"""
        level = self._level(difficulty)
        sub_type = random.choice([
            "prime_identification",
            "coprime_pairs",
            "prime_ranges_and_counting",
            "composite_properties",
            "twin_primes_and_triplets",
        ])

        if sub_type == "prime_identification":
            primes_pool = [53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173]
            composites_pool = [
                (91, "7 * 13"),
                (119, "7 * 17"),
                (133, "7 * 19"),
                (143, "11 * 13"),
                (161, "7 * 23"),
                (209, "11 * 19"),
                (217, "7 * 31"),
                (221, "13 * 17"),
                (247, "13 * 19"),
                (323, "17 * 19"),
            ]
            prime_val = random.choice(primes_pool)
            chosen_comp = random.sample(composites_pool, 3)
            comp_vals = [c[0] for c in chosen_comp]

            question = "Which of the following numbers is a PRIME number?"
            correct = str(prime_val)
            distractors = [str(v) for v in comp_vals]
            comp_breakdown = ", ".join(f"{c[0]} = {c[1]}" for c in chosen_comp)
            explanation = (
                f"- The composite choices have factors: {comp_breakdown}.\n"
                f"- {prime_val} has no divisors other than 1 and itself (tested up to sqrt({prime_val}) ≈ {round(math.isqrt(prime_val), 1)}). "
                f"Hence, {prime_val} is a prime number."
            )
            return self._mcq(question, correct, explanation, level, distractors)

        if sub_type == "coprime_pairs":
            variant = random.choice(["find_coprime_pair", "totient_count"])
            if variant == "find_coprime_pair":
                coprime_candidates = [
                    ((15, 28), "15 = 3 * 5, 28 = 2^2 * 7 => gcd = 1"),
                    ((21, 55), "21 = 3 * 7, 55 = 5 * 11 => gcd = 1"),
                    ((14, 33), "14 = 2 * 7, 33 = 3 * 11 => gcd = 1"),
                    ((25, 36), "25 = 5^2, 36 = 2^2 * 3^2 => gcd = 1"),
                    ((35, 48), "35 = 5 * 7, 48 = 2^4 * 3 => gcd = 1"),
                ]
                non_coprime_candidates = [
                    "(14, 35) [gcd = 7]",
                    "(21, 57) [gcd = 3]",
                    "(26, 65) [gcd = 13]",
                    "(22, 55) [gcd = 11]",
                    "(18, 51) [gcd = 3]",
                ]
                pair, why = random.choice(coprime_candidates)
                correct = f"({pair[0]}, {pair[1]})"
                distractors = random.sample(non_coprime_candidates, 3)
                question = "Which of the following pairs of numbers is COPRIME (relatively prime)?"
                explanation = (
                    f"Two numbers are coprime if their greatest common divisor (GCD) is 1.\n"
                    f"- {correct}: {why}.\n"
                    "The other pairs share common prime factors > 1."
                )
                return self._mcq(question, correct, explanation, level, distractors)
            else:
                n = random.choice([12, 18, 20, 24, 30])
                factors = self._prime_factors(n)
                phi = n
                for p in factors:
                    phi = phi * (p - 1) // p
                question = f"How many positive integers less than {n} are coprime (relatively prime) to {n}?"
                correct = str(phi)
                distractors = [str(phi - 2), str(phi + 2), str(phi + 4)]
                factor_str = " * ".join(f"{p}^{factors[p]}" if factors[p] > 1 else str(p) for p in factors)
                totient_str = " * ".join(f"(1 - 1/{p})" for p in factors)
                explanation = (
                    f"By Euler's Totient Function phi(n) = n * Product(1 - 1/p) for each distinct prime factor p.\n"
                    f"Prime factorization of {n} = {factor_str}.\n"
                    f"phi({n}) = {n} * {totient_str} = {phi} numbers."
                )
                return self._mcq(question, correct, explanation, level, distractors)

        if sub_type == "prime_ranges_and_counting":
            ranges = [
                (10, 30, [11, 13, 17, 19, 23, 29]),
                (20, 45, [23, 29, 31, 37, 41, 43]),
                (30, 55, [31, 37, 41, 43, 47, 53]),
                (50, 75, [53, 59, 61, 67, 71, 73]),
            ]
            low, high, primes_in_range = random.choice(ranges)
            q_type = random.choice(["count", "sum"])
            if q_type == "count":
                count = len(primes_in_range)
                question = f"How many prime numbers are there strictly between {low} and {high}?"
                correct = str(count)
                distractors = [str(count - 1), str(count + 1), str(count + 2)]
                explanation = (
                    f"The prime numbers between {low} and {high} are: {', '.join(map(str, primes_in_range))}.\n"
                    f"Total count = {count}."
                )
            else:
                total_sum = sum(primes_in_range)
                question = f"What is the sum of all prime numbers strictly between {low} and {high}?"
                correct = str(total_sum)
                distractors = [str(total_sum - 6), str(total_sum + 6), str(total_sum + 10)]
                explanation = (
                    f"The prime numbers between {low} and {high} are: {', '.join(map(str, primes_in_range))}.\n"
                    f"Sum = {' + '.join(map(str, primes_in_range))} = {total_sum}."
                )
            return self._mcq(question, correct, explanation, level, distractors)

        if sub_type == "composite_properties":
            variant = random.choice(["three_factors_square_prime", "p_squared_mod_24"])
            if variant == "three_factors_square_prime":
                question = "A positive integer N has exactly 3 distinct positive factors. Which of the following MUST be true about N?"
                correct = "N is the square of a prime number (N = p^2)"
                distractors = [
                    "N is the product of two distinct prime numbers",
                    "N must be an even integer",
                    "N is the cube of a prime number (N = p^3)",
                ]
                explanation = (
                    "The number of factors of an integer with prime factorization p1^a * p2^b * ... is (a + 1)(b + 1)... \n"
                    "For the product to equal 3 (which is prime), there can only be a single prime factor with a + 1 = 3, so a = 2. \n"
                    "Therefore, N = p^2 where p is a prime number (e.g., 4, 9, 25, 49). Its only factors are 1, p, and p^2."
                )
            else:
                question = "If p is a prime number greater than 3, what is the remainder when p^2 is divided by 24?"
                correct = "1"
                distractors = ["0", "5", "7"]
                explanation = (
                    "Every prime p > 3 can be expressed in the form 6k ± 1.\n"
                    "Then p^2 - 1 = (6k ± 1)^2 - 1 = 36k^2 ± 12k = 12k(3k ± 1).\n"
                    "Since one of k or (3k ± 1) is always even, 12k(3k ± 1) is always divisible by 12 * 2 = 24.\n"
                    "Thus, p^2 leaves a remainder of 1 when divided by 24."
                )
            return self._mcq(question, correct, explanation, level, distractors)

        # twin_primes_and_triplets
        variant = random.choice(["identify_twin_prime", "prime_triplet_count"])
        if variant == "identify_twin_prime":
            twin_pair = random.choice(["(41, 43)", "(59, 61)", "(71, 73)", "(29, 31)", "(17, 19)"])
            question = "Two prime numbers are called twin primes if they differ by exactly 2. Which of the following is a pair of twin primes?"
            correct = twin_pair
            distractors = ["(51, 53)", "(87, 89)", "(91, 93)"]
            explanation = (
                f"- {correct} consists of two valid prime numbers whose difference is 2.\n"
                "- In the distractors: 51 is composite (3 * 17), 87 is composite (3 * 29), and 91 is composite (7 * 13)."
            )
        else:
            question = "How many sets of three prime numbers exist in the form of a prime triplet (p, p + 2, p + 4)?"
            correct = "Exactly 1 set: (3, 5, 7)"
            distractors = [
                "0 sets",
                "Infinitely many sets",
                "Exactly 2 sets: (3, 5, 7) and (5, 7, 9)",
            ]
            explanation = (
                "For any integer p, the numbers p, p + 2, and p + 4 leave remainders 0, 1, and 2 in some order when divided by 3. "
                "Therefore, exactly one of the three numbers must be divisible by 3. "
                "The only prime divisible by 3 is 3 itself. Thus p must be 3, giving the unique prime triplet (3, 5, 7). "
                "(Note: 9 is not prime, so (5, 7, 9) is invalid)."
            )
        return self._mcq(question, correct, explanation, level, distractors)
