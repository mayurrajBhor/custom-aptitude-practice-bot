import math
import random


class SpeedAdditionMixin:
    def generate_vedic_addition(self, difficulty=1):
        """Speed addition drills using left-to-right addition and complements."""
        level = self._level(difficulty)
        sub_type = random.choice(["single_digit","two_digit_add_single_digit","Multi_type"])

        if sub_type == "single_digit":
            a = random.randint(3,9)
            b = random.randint(3,9)
            correct = a + b
            question = f"Add mentally: {a} + {b}"
            explanation = f"Add the single digits: {a} + {b} = {correct}."
            return self._mcq(question, correct, explanation, min(level, 3), [correct + 1, correct +3, correct-2, correct-1])

        if sub_type == "two_digit_add_single_digit":
            a = random.randint(10,99)
            b = random.randint(3,9)
            correct = a + b
            question = f"Add mentally: {a} + {b}"
            explanation = f"Add the two digits: {a} + {b} = {correct}."
            return self._mcq(question, correct, explanation, min(level, 3), [correct + 9, correct +4, correct-10, correct-5])
        if sub_type == "Multi_type":
            sub_type = random.choice([
                "two_digit_add_lessthan_100",
                "two_digit_add_morethan_100",
                "three_to_four_digit",
                "three_digit_near_base",
                "missing_addend",])
            if sub_type == "two_digit_add_lessthan_100":
                a = random.randint(10,49)
                b = random.randint(10,99 - a)
                correct = a + b
                question = f"Add mentally: {a} + {b}"
                explanation = f"Add the two digits: {a} + {b} = {correct}."
                return self._mcq(question, correct, explanation, min(level, 3), [correct + 9, correct +4, correct-10, correct-5])

            elif sub_type == "two_digit_add_morethan_100":
                a = random.randint(50,99)
                b = random.randint(50,99)
                correct = a + b
                question = f"Add mentally: {a} + {b}"
                explanation = f"Add the two digits: {a} + {b} = {correct}."
                return self._mcq(question, correct, explanation, min(level, 3), [correct + 12, correct +2, correct-17, correct-7])

            elif sub_type =="three_to_four_digit":
                a = random.randint(100,999)
                b = random.randint(100,9999)
                correct = a + b
                question = f"Add mentally: {a} + {b}"
                explanation = f"Add the two numbers: {a} + {b} = {correct}."
                return self._mcq(question, correct, explanation, min(level, 3), [correct + 100, correct +20, correct-150, correct-50])

            elif sub_type == "three_digit_near_base":
                # One number near a base (like 399, 495, 651, 745, 854, 990)
                base = random.choice([100, 200, 300, 400, 500, 600, 700, 800, 900, 1000])
                deviation = random.randint(-50, 50)
                while deviation == 0:
                    deviation = random.randint(-50, 50)
                
                a = base + deviation
                b = random.randint(100, 999)
                
                # Ensure both are 3-digit or above 99
                while a < 100 or b < 100:
                    a = base + random.randint(-50, 50)
                    b = random.randint(100, 999)
                
                correct = a + b
                question = f"Add mentally: {a} + {b}"
                explanation = f"{a} is near base {base} (deviation {deviation:+d}). So {a} + {b} = {correct}."
                return self._mcq(question, correct, explanation, min(level, 3), [correct + 10, correct - 10, correct + 50, correct - 50])
                
            elif sub_type == "missing_addend":
                a = random.randint(10, 80) if level == 1 else random.randint(180, 760)
                b = random.randint(10, 70) if level == 1 else random.randint(140, 620)
                missing = random.randint(5, 60) if level == 1 else random.randint(90, 540)
                total = a + b + missing
                question = f"What number should replace x if {a} + x + {b} = {total}?"
                explanation = f"Combine known terms: {a} + {b} = {a + b}. Then x = {total} - {a + b} = {missing}."
                return self._mcq(question, missing, explanation, min(level, 3), [missing + 10, missing - 10, total - a, total - b])
