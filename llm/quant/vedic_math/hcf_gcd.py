import math
import random


class HcfGcdMixin:
    def generate_hcf_gcd(self, difficulty=2):
        """Pattern: Highest Common Factor (HCF / GCD)"""
        level = self._level(difficulty)
        sub_type = random.choice([
            "euclidean_algorithm",
            "prime_factorization_hcf",
            "fractions_hcf",
            "largest_divisor_with_remainders",
            "word_problems_tiling",
        ])

        if sub_type == "euclidean_algorithm":
            pairs = [
                (198, 360, 18),
                (144, 216, 72),
                (168, 252, 84),
                (288, 432, 144),
                (210, 504, 42),
                (135, 225, 45),
            ]
            a, b, ans = random.choice(pairs)
            question = f"Find the Highest Common Factor (HCF / GCD) of {a} and {b}."
            correct = str(ans)
            distractors = [str(ans // 2 if ans > 20 else ans * 2), str(ans + 6), str(ans - 6)]
            explanation = (
                f"Using Euclidean Algorithm / Factorization:\n"
                f"{b} = {a} * {b // a} + {b % a}\n"
                f"Continuing division until remainder is 0 yields HCF({a}, {b}) = {ans}."
            )
            return self._mcq(question, correct, explanation, level, distractors)

        if sub_type == "prime_factorization_hcf":
            pool = [
                ("A = 2^3 * 3^4 * 5^2", "B = 2^2 * 3^5 * 5^1 * 7^1", "2^2 * 3^4 * 5^1", 1620),
                ("A = 2^4 * 3^2 * 5^3", "B = 2^3 * 3^3 * 5^1", "2^3 * 3^2 * 5^1", 360),
                ("A = 2^5 * 3^1 * 7^2", "B = 2^3 * 3^3 * 7^1", "2^3 * 3^1 * 7^1", 168),
                ("A = 3^3 * 5^2 * 11^1", "B = 3^2 * 5^3 * 11^2", "3^2 * 5^2 * 11^1", 2475),
            ]
            a_str, b_str, hcf_expr, hcf_val = random.choice(pool)
            question = f"Find the HCF of the two numbers given in prime factor form: {a_str} and {b_str}."
            correct = f"{hcf_expr} ({hcf_val})"
            distractors = [
                f"{hcf_expr.replace('^2', '^3')} ({hcf_val * 2})",
                f"{hcf_expr.replace('^1', '^2')} ({hcf_val * 3})",
                f"{hcf_expr.replace('2^', '2^1 * ')} ({hcf_val // 2})",
            ]
            explanation = (
                "The HCF of numbers in prime factor form is the product of the lowest power of each common prime factor:\n"
                f"HCF = {hcf_expr} = {hcf_val}."
            )
            return self._mcq(question, correct, explanation, level, distractors)

        if sub_type == "fractions_hcf":
            pool = [
                ([2, 8, 16], [3, 9, 27], 2, 27, "2/3, 8/9, 16/27"),
                ([3, 6, 9], [4, 8, 16], 3, 16, "3/4, 6/8, 9/16"),
                ([4, 6, 8], [5, 15, 25], 2, 75, "4/5, 6/15, 8/25"),
                ([5, 10, 25], [6, 12, 18], 5, 36, "5/6, 10/12, 25/18"),
            ]
            nums, dens, hcf_num, lcm_den, frac_str = random.choice(pool)
            question = f"Find the HCF of the fractions: {frac_str}."
            correct = f"{hcf_num}/{lcm_den}"
            distractors = [
                f"{hcf_num * 2}/{lcm_den}",
                f"{hcf_num}/{lcm_den // 2 if lcm_den % 2 == 0 else lcm_den * 2}",
                f"{lcm_den}/{hcf_num}",
            ]
            explanation = (
                "Formula: HCF of Fractions = HCF of Numerators / LCM of Denominators.\n"
                f"- Numerators: {nums} => HCF = {hcf_num}\n"
                f"- Denominators: {dens} => LCM = {lcm_den}\n"
                f"HCF = {correct}."
            )
            return self._mcq(question, correct, explanation, level, distractors)

        if sub_type == "largest_divisor_with_remainders":
            variant = random.choice(["diff_remainders", "same_remainder"])
            if variant == "diff_remainders":
                hcf_target = random.choice([24, 36, 48])
                k1, k2 = random.choice([(3, 5), (4, 7), (5, 6)])
                r1, r2 = 4, 6
                a = hcf_target * k1 + r1
                b = hcf_target * k2 + r2
                ans = math.gcd(a - r1, b - r2)
                question = f"What is the greatest number that divides {a} and {b} leaving remainders of {r1} and {r2} respectively?"
                correct = str(ans)
                distractors = [str(ans // 2), str(ans + 6), str(ans - 6)]
                explanation = (
                    f"The required number must exactly divide ({a} - {r1}) and ({b} - {r2}):\n"
                    f"{a} - {r1} = {a - r1}\n"
                    f"{b} - {r2} = {b - r2}\n"
                    f"HCF({a - r1}, {b - r2}) = {ans}."
                )
            else:
                d = random.choice([25, 30, 35, 40])
                r = 7
                a = d * 2 + r
                b = d * 4 + r
                c = d * 7 + r
                ans = math.gcd(b - a, c - b)
                question = f"What is the greatest positive integer that divides {a}, {b}, and {c} leaving the same remainder in each case?"
                correct = str(ans)
                distractors = [str(ans // 2), str(ans + 5), str(ans + 10)]
                explanation = (
                    f"When numbers leave the same remainder, the required divisor is the HCF of their absolute differences:\n"
                    f"|{b} - {a}| = {b - a}\n"
                    f"|{c} - {b}| = {c - b}\n"
                    f"|{c} - {a}| = {c - a}\n"
                    f"HCF({b - a}, {c - b}, {c - a}) = {ans}."
                )
            return self._mcq(question, correct, explanation, level, distractors)

        # word_problems_tiling
        pool = [
            (18, 15, 3, 30),
            (24, 18, 6, 12),
            (36, 28, 4, 63),
            (40, 25, 5, 40),
            (60, 48, 12, 20),
        ]
        length, width, side, count = random.choice(pool)
        question = f"A rectangular conference hall is {length} meters long and {width} meters wide. It is to be completely paved with identical square tiles of the largest possible size. What is the minimum number of tiles needed?"
        correct = str(count)
        distractors = [str(count + 5), str(count - 4), str(side * 4)]
        explanation = (
            f"Step 1: The side length of the largest square tile is HCF({length}, {width}) = {side} meters.\n"
            f"Step 2: Number of tiles = (Area of hall) / (Area of 1 tile) = ({length} * {width}) / ({side} * {side})\n"
            f"= ({length // side}) * ({width // side}) = {count} tiles."
        )
        return self._mcq(question, correct, explanation, level, distractors)
