import math
import random


class CubesRootsMixin:
    def generate_vedic_cubes_roots(self, difficulty=1):
        """Cubes, cube roots, and unit digit drills."""
        level = self._level(difficulty)
        sub_type = random.choice(["cube_value", "perfect_cube_root", "nearest_cube", "cube_unit_digit"])

        if sub_type == "cube_value":
            # n = random.randint(2, 10) if level == 1 else random.randint(3, 20)
            n = random.randint(2, 10)
            correct = n ** 3
            question = f"Recall or calculate quickly: {n}^3 = ?"
            explanation = f"{n}^3 means {n} x {n} x {n} = {correct}."
            return self._mcq(question, correct, explanation, min(level, 3), [n * n, correct + n, correct - n, (n + 1) ** 3])

        if sub_type == "perfect_cube_root":
            root = random.randint(2, 10) if level == 1 else random.randint(3, 20)
            cube = root ** 3
            question = f"Find the cube root of {cube}."
            explanation = f"{root}^3 = {cube}, so the cube root of {cube} is {root}."
            return self._mcq(question, root, explanation, min(level, 3), [root + 1, root - 1, root + 2, max(1, root - 2)])

        if sub_type == "nearest_cube":
            root = random.randint(2, 10) if level == 1 else random.randint(5, 20)
            n = root ** 3 + random.randint(1, 3 * root * root)
            correct = round(n ** (1 / 3))
            while (correct + 1) ** 3 <= n:
                correct += 1
            while correct ** 3 > n:
                correct -= 1
            question = f"What is the greatest integer less than or equal to the cube root of {n}?"
            explanation = f"{correct}^3 = {correct ** 3} and {correct + 1}^3 = {(correct + 1) ** 3}. So the integer cube root is {correct}."
            return self._mcq(question, correct, explanation, max(1, min(level, 3)), [correct + 1, correct - 1, correct + 2, max(1, correct - 2)])

        n = random.randint(2, 20) if level == 1 else random.randint(12, 99)
        correct = (n ** 3) % 10
        question = f"What is the units digit of {n}^3?"
        explanation = f"Only the units digit matters. The units digit of {n} is {n % 10}, and {(n % 10)}^3 has units digit {correct}."
        return self._mcq(question, correct, explanation, min(level, 3), [(correct + 1) % 10, (correct + 2) % 10, (10 - correct) % 10, n % 10])
