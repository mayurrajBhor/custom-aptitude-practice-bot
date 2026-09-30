import math
import random


class SpeedAdditionMixin:
    def generate_vedic_addition(self, difficulty=1):
        """Speed addition drills using left-to-right addition and complements."""
        level = self._level(difficulty)
        sub_type = random.choice(["left_to_right", "complements", "single_digit","two_digit_add_single_digit","two_digit_add_lessthan_100","two_digit_add_morethan_100","three_to_four_digit","three_digit_near_base", "missing_addend"])

        if sub_type == "left_to_right":
            if level == 1:
                a = random.randint(10, 60)
                b = random.randint(5, 40)
                correct = a + b
                question = f"Add mentally: {a} + {b}."
                explanation = f"Add the tens and ones: {a} + {b} = {correct}."
                return self._mcq(question, correct, explanation, 1, [correct + 1, correct - 1, correct + 10, correct - 10])

            a = random.randint(60, 180) if level == 2 else random.randint(240, 890)
            b = random.randint(30, 160) if level == 2 else random.randint(120, 760)
            c = random.randint(10, 90) if level == 2 else random.randint(80, 490)
            correct = a + b + c
            question = f"Add mentally from left to right: {a} + {b} + {c}."
            explanation = f"Add in chunks: {a} + {b} = {a + b}, then {a + b} + {c} = {correct}."
            return self._mcq(question, correct, explanation, min(level, 3), [correct + 10, correct - 10, correct + 100, correct - 1])

        if sub_type == "complements":
            base = 100 if level <= 2 else random.choice([1000, 10000])
            gap_limit = 20 if level == 1 else min(87, base // 5)
            gap_a = random.randint(1, gap_limit)
            gap_b = random.randint(1, gap_limit)
            a = base - gap_a
            b = base - gap_b
            correct = a + b
            question = f"Using complements to {base}, find {a} + {b}."
            explanation = f"{a} is {gap_a} below {base} and {b} is {gap_b} below {base}. So {a} + {b} = 2 x {base} - ({gap_a} + {gap_b}) = {correct}."
            return self._mcq(question, correct, explanation, min(level, 3), [correct + gap_a, correct + gap_b, correct - 10, correct + 100])
        
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

        if sub_type == "two_digit_add_lessthan_100":
            a = random.randint(10,49)
            b = random.randint(10,99 - a)
            correct = a + b
            question = f"Add mentally: {a} + {b}"
            explanation = f"Add the two digits: {a} + {b} = {correct}."
            return self._mcq(question, correct, explanation, min(level, 3), [correct + 9, correct +4, correct-10, correct-5])

        if sub_type == "two_digit_add_morethan_100":
            a = random.randint(50,99)
            b = random.randint(50,99)
            correct = a + b
            question = f"Add mentally: {a} + {b}"
            explanation = f"Add the two digits: {a} + {b} = {correct}."
            return self._mcq(question, correct, explanation, min(level, 3), [correct + 12, correct +2, correct-17, correct-7])

        if sub_type =="three_to_four_digit":
            a = random.randint(100,999)
            b = random.randint(100,9999)
            correct = a + b
            question = f"Add mentally: {a} + {b}"
            explanation = f"Add the two numbers: {a} + {b} = {correct}."
            return self._mcq(question, correct, explanation, min(level, 3), [correct + 100, correct +20, correct-150, correct-50])

        if sub_type == "three_digit_near_base":
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
            
        if sub_type == "missing_addend":
            a = random.randint(10, 80) if level == 1 else random.randint(180, 760)
            b = random.randint(10, 70) if level == 1 else random.randint(140, 620)
            missing = random.randint(5, 60) if level == 1 else random.randint(90, 540)
            total = a + b + missing
            question = f"What number should replace x if {a} + x + {b} = {total}?"
            explanation = f"Combine known terms: {a} + {b} = {a + b}. Then x = {total} - {a + b} = {missing}."
            return self._mcq(question, missing, explanation, min(level, 3), [missing + 10, missing - 10, total - a, total - b])
