import math
import random
from fractions import Fraction


class LcmMixin:
    def generate_lcm(self, difficulty=2):
        """Pattern: Least Common Multiple (LCM)"""
        level = self._level(difficulty)
        sub_type = random.choice([
            "prime_factorization_lcm",
            "fractions_lcm",
            "product_formula_relation",
            "smallest_number_with_remainders",
            "word_problems_bells",
        ])

        if sub_type == "prime_factorization_lcm":
            pool = [
                ([18, 24, 30], 360),
                ([24, 36, 60], 360),
                ([15, 25, 40], 600),
                ([16, 24, 36], 144),
                ([20, 30, 45], 180),
                ([28, 42, 56], 168),
            ]
            nums, lcm_val = random.choice(pool)
            nums_str = ", ".join(map(str, nums))
            question = f"Find the Least Common Multiple (LCM) of {nums_str}."
            correct = str(lcm_val)
            distractors = [str(lcm_val // 2), str(lcm_val * 2), str(lcm_val + nums[0])]
            explanation = (
                f"Using prime factor powers:\n"
                f"Take the highest power of each prime factor present across {nums_str}.\n"
                f"LCM = {lcm_val}."
            )
            return self._mcq(question, correct, explanation, level, distractors)

        if sub_type == "fractions_lcm":
            pool = [
                ([2, 3, 4], [5, 10, 15], 12, 5, "2/5, 3/10, 4/15"),
                ([1, 3, 5], [2, 4, 6], 15, 2, "1/2, 3/4, 5/6"),
                ([2, 4, 6], [3, 9, 27], 12, 3, "2/3, 4/9, 6/27"),
                ([5, 10, 15], [4, 8, 12], 30, 4, "5/4, 10/8, 15/12"),
            ]
            num_list, den_list, lcm_num, hcf_den, frac_str = random.choice(pool)
            frac_ans = Fraction(lcm_num, hcf_den)
            correct = f"{frac_ans.numerator}/{frac_ans.denominator}" if frac_ans.denominator != 1 else str(frac_ans.numerator)
            question = f"Find the LCM of the fractions: {frac_str}."
            distractors = [
                f"{lcm_num}/{hcf_den * 2}",
                f"{hcf_den}/{lcm_num}",
                f"{lcm_num * 2}/{hcf_den}",
            ]
            explanation = (
                "Formula: LCM of Fractions = LCM of Numerators / HCF of Denominators.\n"
                f"- LCM of Numerators ({num_list}) = {lcm_num}\n"
                f"- HCF of Denominators ({den_list}) = {hcf_den}\n"
                f"LCM = {lcm_num}/{hcf_den} = {correct}."
            )
            return self._mcq(question, correct, explanation, level, distractors)

        if sub_type == "product_formula_relation":
            variant = random.choice(["given_one_number", "ratio_and_hcf"])
            if variant == "given_one_number":
                hcf = random.choice([12, 15, 18, 20])
                k1, k2 = random.choice([(3, 4), (2, 5), (3, 5)])
                lcm_val = hcf * k1 * k2
                num1 = hcf * k1
                num2 = hcf * k2
                question = f"The HCF and LCM of two numbers are {hcf} and {lcm_val} respectively. If one of the numbers is {num1}, what is the other number?"
                correct = str(num2)
                distractors = [str(num2 - hcf), str(num2 + hcf), str(num1)]
                explanation = (
                    "Formula: Product of two numbers = HCF * LCM.\n"
                    f"Other Number = (HCF * LCM) / (Given Number) = ({hcf} * {lcm_val}) / {num1} = {num2}."
                )
            else:
                hcf = random.choice([8, 12, 14, 15])
                r1, r2 = random.choice([(3, 4), (3, 5), (4, 5), (5, 6)])
                lcm_val = hcf * r1 * r2
                question = f"Two numbers are in the ratio {r1}:{r2} and their HCF is {hcf}. What is their Least Common Multiple (LCM)?"
                correct = str(lcm_val)
                distractors = [str(lcm_val - hcf), str(lcm_val + hcf), str(hcf * (r1 + r2))]
                explanation = (
                    f"Let the numbers be {r1}x and {r2}x where x = HCF = {hcf}.\n"
                    f"The two numbers are {r1 * hcf} and {r2 * hcf}.\n"
                    f"LCM = HCF * r1 * r2 = {hcf} * {r1} * {r2} = {lcm_val}."
                )
            return self._mcq(question, correct, explanation, level, distractors)

        if sub_type == "smallest_number_with_remainders":
            variant = random.choice(["constant_remainder", "constant_difference"])
            if variant == "constant_remainder":
                divs = random.choice([(12, 15, 20), (15, 18, 24), (16, 20, 24)])
                rem = random.choice([3, 4, 5, 7])
                lcm_val = self._lcm_list(divs)
                ans = lcm_val + rem
                divs_str = ", ".join(map(str, divs))
                question = f"Find the smallest positive integer which when divided by {divs_str} leaves a remainder of {rem} in each case."
                correct = str(ans)
                distractors = [str(lcm_val), str(ans + divs[0]), str(ans - rem)]
                explanation = (
                    f"The required number is LCM({divs_str}) + remainder:\n"
                    f"LCM({divs_str}) = {lcm_val}\n"
                    f"Answer = {lcm_val} + {rem} = {ans}."
                )
            else:
                divs = (20, 25, 35)
                d = 6
                rems = tuple(div - d for div in divs)
                lcm_val = self._lcm_list(divs)
                ans = lcm_val - d
                question = f"Find the smallest positive integer which when divided by {divs[0]}, {divs[1]}, and {divs[2]} leaves remainders of {rems[0]}, {rems[1]}, and {rems[2]} respectively."
                correct = str(ans)
                distractors = [str(lcm_val), str(lcm_val + d), str(ans - 10)]
                explanation = (
                    f"Observe that the difference between each divisor and its remainder is constant:\n"
                    f"{divs[0]} - {rems[0]} = {d}, {divs[1]} - {rems[1]} = {d}, {divs[2]} - {rems[2]} = {d}.\n"
                    f"LCM({divs[0]}, {divs[1]}, {divs[2]}) = {lcm_val}.\n"
                    f"Answer = LCM - difference = {lcm_val} - {d} = {ans}."
                )
            return self._mcq(question, correct, explanation, level, distractors)

        # word_problems_bells
        bells = random.choice([(6, 8, 12, 18), (8, 12, 15, 20), (10, 15, 20, 25)])
        lcm_sec = self._lcm_list(bells)
        mins = random.choice([30, 36, 60])
        total_sec = mins * 60
        tolls = total_sec // lcm_sec
        bells_str = ", ".join(map(str, bells))
        question = f"Four electronic bells toll together at intervals of {bells_str} seconds respectively. In {mins} minutes, how many times will they toll together (excluding the toll at the start)?"
        correct = str(tolls)
        distractors = [str(tolls + 1), str(tolls - 1), str(tolls * 2)]
        explanation = (
            f"Step 1: All bells toll together every LCM({bells_str}) seconds = {lcm_sec} seconds.\n"
            f"Step 2: Total duration = {mins} minutes = {total_sec} seconds.\n"
            f"Number of times they toll together = {total_sec} / {lcm_sec} = {tolls} times."
        )
        return self._mcq(question, correct, explanation, level, distractors)
