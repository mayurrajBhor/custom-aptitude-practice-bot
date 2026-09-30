import math
import random


class OddEvenMixin:
    def generate_odd_even(self, difficulty=2):
        """Pattern: Odd/Even Properties"""
        level = self._level(difficulty)
        sub_type = random.choice([
            "parity_arithmetic",
            "algebraic_parity",
            "consecutive_integers",
            "power_and_exponents",
            "word_problem_parity",
        ])

        if sub_type == "parity_arithmetic":
            var_state = random.choice(["x_odd_y_even", "x_odd_y_odd", "x_even_y_even"])
            if var_state == "x_odd_y_even":
                q_ask = random.choice(["must be ODD", "must be EVEN"])
                if q_ask == "must be ODD":
                    question = "If x is an odd integer and y is an even integer, which of the following expressions MUST be odd?"
                    correct = "x + 2y"
                    distractors = ["2x + y", "xy", "x + y + 1"]
                    explanation = (
                        "Given: x is Odd, y is Even.\n"
                        "- 2y is Even, so x + 2y = Odd + Even = Odd (Always True).\n"
                        "- 2x is Even, so 2x + y = Even + Even = Even.\n"
                        "- xy = Odd * Even = Even.\n"
                        "- x + y + 1 = Odd + Even + 1 = Odd + 1 = Even."
                    )
                else:
                    question = "If x is an odd integer and y is an even integer, which of the following expressions MUST be even?"
                    correct = "xy + 2x"
                    distractors = ["x + y", "3x + y", "x^2 + y"]
                    explanation = (
                        "Given: x is Odd, y is Even.\n"
                        "- xy = Odd * Even = Even, and 2x is Even. Thus xy + 2x = Even + Even = Even (Always True).\n"
                        "- x + y = Odd + Even = Odd.\n"
                        "- 3x + y = Odd + Even = Odd.\n"
                        "- x^2 + y = Odd + Even = Odd."
                    )
            elif var_state == "x_odd_y_odd":
                question = "If both a and b are odd integers, which of the following expressions MUST be an even integer?"
                correct = "a + b"
                distractors = ["ab", "2a + b", "ab + 2"]
                explanation = (
                    "Given: a is Odd, b is Odd.\n"
                    "- a + b = Odd + Odd = Even (Always True).\n"
                    "- ab = Odd * Odd = Odd.\n"
                    "- 2a + b = Even + Odd = Odd.\n"
                    "- ab + 2 = Odd + Even = Odd."
                )
            else:
                question = "If m is an even integer and n is an odd integer, what is the parity of 3m + 5n + 1?"
                correct = "Even"
                distractors = ["Odd", "Could be Odd or Even", "Cannot be determined"]
                explanation = (
                    "Given: m is Even, n is Odd.\n"
                    "- 3m = Odd * Even = Even.\n"
                    "- 5n = Odd * Odd = Odd.\n"
                    "- 3m + 5n = Even + Odd = Odd.\n"
                    "- 3m + 5n + 1 = Odd + 1 = Even."
                )
            return self._mcq(question, correct, explanation, level, distractors)

        if sub_type == "algebraic_parity":
            variant = random.choice(["product_three", "sum_chain", "linear_equation"])
            if variant == "product_three":
                question = "If a, b, and c are positive integers such that the product a * b * c is an odd integer, which of the following MUST be true?"
                correct = "All three of a, b, and c are odd"
                distractors = [
                    "At least one of a, b, or c is even",
                    "Exactly two of a, b, and c are odd",
                    "a + b + c must be an even integer",
                ]
                explanation = (
                    "A product of integers is odd if and only if EVERY factor in the product is odd. "
                    "If even a single factor were even, the entire product would become even. "
                    "Therefore, all three integers a, b, and c must be odd. (Note: a + b + c = Odd + Odd + Odd = Odd)."
                )
            elif variant == "sum_chain":
                question = "If x + y is an even integer and y + z is an odd integer, what is the parity of x + z?"
                correct = "Always Odd"
                distractors = ["Always Even", "Could be Odd or Even depending on y", "Cannot be determined"]
                explanation = (
                    "- x + y is Even implies x and y have the SAME parity (both odd or both even).\n"
                    "- y + z is Odd implies y and z have OPPOSITE parity.\n"
                    "- Since x has the same parity as y, and z has the opposite parity of y, x and z must have OPPOSITE parity.\n"
                    "- The sum of two integers with opposite parity is ALWAYS Odd."
                )
            else:
                k = random.choice([25, 31, 37, 43, 49])
                question = f"If 3x + 5y = {k}, where x and y are positive integers, which of the following statements must be true regarding the parities of x and y?"
                correct = "One of x and y is even, and the other is odd"
                distractors = [
                    "Both x and y must be odd integers",
                    "Both x and y must be even integers",
                    "x must be even and y must be even",
                ]
                explanation = (
                    f"3x + 5y = {k} (an odd number).\n"
                    "For the sum of two terms (3x and 5y) to be odd, exactly one term must be even and the other must be odd.\n"
                    "- If 3x is even, then x is even, which forces 5y to be odd, so y is odd.\n"
                    "- If 3x is odd, then x is odd, which forces 5y to be even, so y is even.\n"
                    "Hence, x and y must have opposite parities (one even, one odd)."
                )
            return self._mcq(question, correct, explanation, level, distractors)

        if sub_type == "consecutive_integers":
            variant = random.choice(["sum_four", "product_two", "sum_n_value"])
            if variant == "sum_four":
                question = "For any integer n, the sum of four consecutive integers n + (n + 1) + (n + 2) + (n + 3) is:"
                correct = "Always Even"
                distractors = ["Always Odd", "Even only when n is even", "Odd only when n is odd"]
                explanation = (
                    "Sum = n + (n + 1) + (n + 2) + (n + 3) = 4n + 6 = 2(2n + 3).\n"
                    "Because 2 is a factor of 2(2n + 3), the sum is divisible by 2 for EVERY integer n. "
                    "Thus, the sum is always even."
                )
            elif variant == "product_two":
                question = "If k is any integer, what is the parity of the product k(k + 1)?"
                correct = "Always Even"
                distractors = ["Always Odd", "Even only if k is positive", "Odd only if k is odd"]
                explanation = (
                    "Out of any two consecutive integers k and k + 1, exactly one must be even and one must be odd. "
                    "Since Even * Odd = Even, the product of any two consecutive integers is ALWAYS Even."
                )
            else:
                n_start = random.randint(11, 29)
                total_sum = sum(n_start + i for i in range(5))
                largest = n_start + 4
                question = f"The sum of 5 consecutive integers is {total_sum}. What is the value of the largest of these integers, and is it odd or even?"
                correct = f"{largest} (which is {'even' if largest % 2 == 0 else 'odd'})"
                distractors = [
                    f"{largest - 1} (which is {'even' if (largest - 1) % 2 == 0 else 'odd'})",
                    f"{largest + 1} (which is {'even' if (largest + 1) % 2 == 0 else 'odd'})",
                    f"{largest + 2} (which is {'even' if (largest + 2) % 2 == 0 else 'odd'})",
                ]
                explanation = (
                    f"Let the integers be n, n+1, n+2, n+3, n+4. Their sum is 5n + 10 = {total_sum}.\n"
                    f"5n = {total_sum - 10} => n = {(total_sum - 10) // 5}.\n"
                    f"The largest integer is n + 4 = {largest}, which is {'even' if largest % 2 == 0 else 'odd'}."
                )
            return self._mcq(question, correct, explanation, level, distractors)

        if sub_type == "power_and_exponents":
            variant = random.choice(["x3_minus_x", "power_parity_rule", "base_exponent_parity"])
            if variant == "x3_minus_x":
                question = "If x is any positive integer, the expression x^3 - x is ALWAYS:"
                correct = "Divisible by 6 and always Even"
                distractors = [
                    "Always Odd",
                    "Even only when x is a multiple of 4",
                    "Divisible by 8 for all values of x",
                ]
                explanation = (
                    "x^3 - x = x(x^2 - 1) = (x - 1) * x * (x + 1).\n"
                    "This is the product of three consecutive integers. Any three consecutive integers contain "
                    "at least one multiple of 2 and exactly one multiple of 3. Therefore, the expression is always "
                    "divisible by 2 * 3 = 6, and is always Even."
                )
            elif variant == "power_parity_rule":
                question = "If a is an odd integer and b is a positive integer, what is the parity of a^b + (a + 1)^b?"
                correct = "Always Odd"
                distractors = ["Always Even", "Even if b is even", "Odd only if b is odd"]
                explanation = (
                    "1. An odd integer raised to any positive integer power is always Odd (Odd^b = Odd).\n"
                    "2. Since a is odd, (a + 1) is even. An even integer raised to any positive integer power is always Even (Even^b = Even).\n"
                    "3. Odd + Even = Odd. Hence, the expression is always Odd regardless of b."
                )
            else:
                question = "If m^n is an even integer, where m and n are positive integers, which of the following MUST be true?"
                correct = "m must be an even integer"
                distractors = [
                    "n must be an even integer",
                    "Both m and n must be even integers",
                    "m must be odd and n must be even",
                ]
                explanation = (
                    "The parity of a power m^n (with positive integer exponent n) is determined entirely by its base m. "
                    "If m were odd, m^n would be the product of n odd numbers, which is always odd. "
                    "Thus, for m^n to be even, m MUST be even. The exponent n can be any positive integer (e.g., 2^1=2, 2^2=4)."
                )
            return self._mcq(question, correct, explanation, level, distractors)

        # word_problem_parity
        variant = random.choice(["coin_partition", "handshake_lemma"])
        if variant == "coin_partition":
            odd_coins = random.choice([25, 27, 33, 35, 41])
            question = f"Can {odd_coins} gold coins be distributed among 4 treasure chests such that each chest contains an odd number of coins?"
            correct = "No, because the sum of 4 odd integers is always even"
            distractors = [
                f"Yes, by placing {odd_coins // 4} or {(odd_coins // 4) + 1} coins in each chest",
                f"Yes, because {odd_coins} is an odd number",
                "Cannot be determined without knowing the size of each chest",
            ]
            explanation = (
                f"Let the coins in each of the 4 chests be o1, o2, o3, o4 (all odd integers).\n"
                "Sum = (Odd + Odd) + (Odd + Odd) = Even + Even = Even.\n"
                f"However, the total number of coins is {odd_coins}, which is ODD. "
                "An even sum can never equal an odd number. Thus, such a distribution is mathematically impossible."
            )
        else:
            n_people = random.choice([15, 17, 19, 21])
            k_hands = random.choice([3, 5])
            question = f"In an executive committee of {n_people} members, is it possible for every member to have had meetings with exactly {k_hands} other members?"
            correct = "No, because the sum of all individual meetings must be an even number"
            distractors = [
                f"Yes, the total number of pairwise meetings would be {n_people * k_hands}",
                f"Yes, because both {n_people} and {k_hands} are odd numbers",
                "Cannot be determined without a seating arrangement",
            ]
            explanation = (
                f"Each meeting involves 2 people. Thus, 2 * (Total Meetings) = Sum of degrees = {n_people} * {k_hands} = {n_people * k_hands}.\n"
                f"Since {n_people} and {k_hands} are both odd, their product {n_people * k_hands} is ODD. "
                "However, 2 * (Total Meetings) must be EVEN. An odd number cannot equal an even number. "
                "By the Handshake Lemma, this scenario is impossible."
            )
        return self._mcq(question, correct, explanation, level, distractors)
