import math
import random


class TablesMultiplesMixin:
    def generate_vedic_tables_multiples(self, difficulty=1):
        """Tables, missing factors, and multiple recognition drills."""
        level = self._level(difficulty)
        sub_type = random.choice(["table_product", "missing_factor", "next_multiple", "factor_split"])
        table_max = 10 if level == 1 else 12 if level == 2 else 25

        if sub_type == "table_product":
            # a = random.randint(2, table_max)
            a = random.randint(4, 9)
            b = random.randint(3, 9)
            # b = random.randint(2, 10 if level == 1 else 20)
            correct = a * b
            question = f"Recall the table value: {a} x {b} = ?"
            explanation = f"{a} x {b} = {correct}. Table fluency reduces load in longer aptitude calculations."
            return self._mcq(question, correct, explanation, 1, [correct + a, correct - a, correct + b, correct - b])

        if sub_type == "missing_factor":
            factor = random.randint(2, table_max)
            missing = random.randint(2, 10 if level == 1 else 20)
            product = factor * missing
            question = f"If {factor} x x = {product}, what is x?"
            explanation = f"Use the table of {factor}: {factor} x {missing} = {product}, so x = {missing}."
            return self._mcq(question, missing, explanation, 1, [missing + 1, missing - 1, factor, product // 10])

        if sub_type == "next_multiple":
            base = random.randint(2, table_max)
            k = random.randint(3, 12 if level == 1 else 30)
            target = base * k + random.randint(1, base - 1)
            correct = base * (k + 1)
            question = f"What is the smallest multiple of {base} greater than {target}?"
            explanation = f"{base} x {k} = {base * k}, which is below {target}. The next multiple is {base} x {k + 1} = {correct}."
            return self._mcq(question, correct, explanation, 2, [base * k, correct + base, correct - 1, target + base])

        a = random.randint(2, table_max)
        b = random.randint(2, 5 if level == 1 else 9)
        c = random.randint(2, 5 if level == 1 else 9)
        correct = a * (b + c)
        question = f"Use table splitting to calculate {a} x {b} + {a} x {c}."
        explanation = f"Factor out {a}: {a} x {b} + {a} x {c} = {a} x ({b} + {c}) = {a} x {b + c} = {correct}."
        return self._mcq(question, correct, explanation, 2, [a * b, a * c, correct + a, correct - a])
