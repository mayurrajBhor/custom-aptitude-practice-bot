import math
import random
from fractions import Fraction


class CorePercentageEquationsMixin:
    def generate_find_original_number(self):
        """Patterns Q1-Q4: Solving for x in percentage equations."""
        sub_type = random.choice(['add_self', 'sub_self', 'add_abs', 'sub_abs'])
        
        # Benchmarks for Q1/Q2
        num, den, perc = random.choice(self.benchmarks)
        frac = Fraction(num, den)

        if sub_type == 'add_self':
            # x + (num/den)x = result
            # result = x * (1 + num/den) = x * (den + num) / den
            # Pick x as a multiple of den to keep result an integer
            multiplier = random.randint(50, 500)
            x = den * multiplier
            result = x + (x * num // den)
            question = f"If {perc} of a number is added to itself, the result becomes {result}. Find the original number."
            explanation = f"{perc} is {num}/{den}. If we add {num}/{den} of a number to itself, we get (1 + {num}/{den}) = {(den+num)}/{den} of the number. \nSo, {(den+num)}/{den} * x = {result} => x = ({result} * {den}) / {den+num} = {x}."
            correct = str(x)
        
        elif sub_type == 'sub_self':
            # x - (num/den)x = result
            multiplier = random.randint(50, 500)
            x = den * multiplier
            result = x - (x * num // den)
            question = f"If {perc} of a number is subtracted from itself, the result becomes {result}. Find the original number."
            explanation = f"{perc} is {num}/{den}. Subtracting {num}/{den} from the number gives (1 - {num}/{den}) = {(den-num)}/{den} of the number. \nSo, {(den-num)}/{den} * x = {result} => x = ({result} * {den}) / {den-num} = {x}."
            correct = str(x)

        elif sub_type == 'add_abs':
            # x + delta = target_perc * x
            # delta = x * (target_perc - 1)
            # Pick target_perc from benchmarks like 157% (11/7 if we use 157.14% or similar, but let's stick to easy ones)
            # Example Q3: 157%... let's use 150% or 125% for simplicity or pick a delta and target_perc
            target_perc_val = random.choice([125, 150, 175, 200, 250])
            target_frac = Fraction(target_perc_val, 100)
            x = random.randint(4, 25) * 4
            delta = int(x * (target_frac - 1))
            question = f"If {delta} is added to a number, the number becomes {target_perc_val}% of itself. Find the number."
            explanation = f"{target_perc_val}% of a number means the number has increased by {target_perc_val - 100}%. \nSo, {target_perc_val - 100}% of x = {delta} => ({target_perc_val - 100}/100) * x = {delta} => x = {x}."
            correct = str(x)
        
        else: # sub_abs
            # x - delta = target_perc * x
            target_perc_val = random.choice([25, 40, 50, 60, 75, 80])
            target_frac = Fraction(target_perc_val, 100)
            x = random.randint(10, 50) * 10
            delta = int(x * (1 - target_frac))
            question = f"If {delta} is subtracted from a number, the number becomes {target_perc_val}% of itself. Find the number."
            explanation = f"If the number becomes {target_perc_val}%, it means {100 - target_perc_val}% was subtracted. \nSo, {100 - target_perc_val}% of x = {delta} => ({100 - target_perc_val}/100) * x = {delta} => x = {x}."
            correct = str(x)

        options = [correct]
        while len(options) < 4:
            val = str(int(correct) + random.randint(-10, 10) * (5 if int(correct) > 100 else 1))
            if val not in options and int(val) > 0:
                options.append(val)
        random.shuffle(options)
        return {
            "question_text": question,
            "options": options,
            "correct_option_index": options.index(correct),
            "explanation": explanation,
            "difficulty": 3
        }

    def generate_percentage_equations(self):
        """Phase 18 Category 1: Percentage Equations & Ratios"""
        sub_type = random.choice([
            'sum_diff_ratio',       # Q12: P%(A+B)=Q%(A-B), find A:B ratio
            'sum_diff_percent',     # Q23: P%(A+B)=Q%(A-B), find A as % of B
            'direct_eq_find_x',    # Q21: P% of A = Q% of B, find x% (B as % of A)
            'direct_eq_two_var',   # Q22/Q26: two equalities, find combined expression
            'multi_var',           # Q27: 30%A = 0.25B = 1/5C, find A:B:C
            'third_anchor',        # Q20: first is X% of C, second is Y% less than C
            'sum_constraint',      # Q29: sum + ratio constraint
        ])
        
        if sub_type == 'sum_diff_ratio':
            # Q12: P%(A+B) = Q%(A-B), find A:B ratio
            p1 = random.choice([10, 15, 20, 25, 30, 40])
            p2 = random.choice([50, 60, 70, 75, 80])
            f = Fraction(p1 + p2, p2 - p1)
            templates = [
                f"If {p1}% of (A + B) = {p2}% of (A - B), then what is the ratio of A to B?",
                f"Two numbers A and B satisfy {p1}(A + B) = {p2}(A - B). What is A : B?",
                f"The sum of two numbers is related to their difference such that {p1}% of their sum equals {p2}% of their difference. Find A:B.",
            ]
            question = random.choice(templates)
            correct = f"{f.numerator}:{f.denominator}"
            explanation = f"{p1}(A + B) = {p2}(A - B)\n=> {p1}A + {p1}B = {p2}A - {p2}B\n=> ({p1} + {p2})B = ({p2} - {p1})A\n=> {p1+p2}B = {p2-p1}A\n=> A/B = {p1+p2}/{p2-p1} = {f.numerator}/{f.denominator}."

        elif sub_type == 'sum_diff_percent':
            # Q23: P%(A+B) = Q%(A-B), find A as % of B
            p1 = random.choice([10, 15, 20, 25, 30, 40])
            p2 = random.choice([50, 60, 70, 75, 80])
            f = Fraction(p1 + p2, p2 - p1)
            val = float(f) * 100
            templates = [
                f"If {p1}% of (A + B) = {p2}% of (A - B), then A is what percent of B?",
                f"Given {p1}(A+B) = {p2}(A-B), express A as a percentage of B.",
                f"Two numbers A and B satisfy {p1}% of (A+B) = {p2}% of (A–B). What percent of B is A?",
            ]
            question = random.choice(templates)
            correct = f"{int(val)}%" if val.is_integer() else f"{round(val, 2)}%"
            explanation = f"{p1}(A + B) = {p2}(A - B)\n=> {p1+p2}B = {p2-p1}A\n=> A/B = {f.numerator}/{f.denominator}.\nAs a percentage: ({f.numerator}/{f.denominator}) * 100 = {correct}."

        elif sub_type == 'direct_eq_find_x':
            # Q21: P% of A = Q% of B, and B = x% of A. Find x.
            p1 = random.choice([40, 50, 60, 75, 80])
            p2 = random.choice([10, 20, 25, 30])
            f = Fraction(p1, p2)
            val = float(f) * 100
            correct = f"{int(val)}" if val.is_integer() else f"{round(val, 2)}"
            templates = [
                f"If {p1}% of A = {p2}% of B, and B = x% of A, then find the value of x.",
                f"Given that {p1}% of A equals {p2}% of B, what percentage of A is B?",
                f"Two quantities A and B satisfy {p1}% of A = {p2}% of B. If B = x% of A, find x.",
            ]
            question = random.choice(templates)
            explanation = f"{p1}% of A = {p2}% of B\n=> {p1}A = {p2}B\n=> B/A = {p1}/{p2} = {f.numerator}/{f.denominator}.\nSo B is ({f.numerator}/{f.denominator}) * 100% of A = {correct}% of A. Thus x = {correct}."

        elif sub_type == 'direct_eq_two_var':
            # Q22/Q26: A is X% of C, B is Y% of C. Find B as % of A, or A+B as % of C.
            p_A = random.choice([30, 40, 50, 60, 75])
            p_B = random.choice([20, 25, 40, 50, 80])
            t = random.choice(['b_pct_a', 'sum_pct_c'])
            if t == 'b_pct_a':
                val = round(p_B / p_A * 100, 2)
                correct = f"{int(val)}%" if float(val).is_integer() else f"{val}%"
                templates = [
                    f"If A = {p_A}% of C and B = {p_B}% of C, then B is what percent of A?",
                    f"A and B are {p_A}% and {p_B}% of C respectively. Express B as a percentage of A.",
                ]
                explanation = f"A = {p_A}% of C => A = {p_A}.\nB = {p_B}% of C => B = {p_B}.\nB as % of A = ({p_B}/{p_A}) * 100 = {correct}."
            else:
                val = p_A + p_B
                correct = f"{val}%"
                templates = [
                    f"If A = {p_A}% of C and B = {p_B}% of C, then (A + B) is what percent of C?",
                    f"A is {p_A}% of C and B is {p_B}% of C. What percentage of C is (A+B)?",
                ]
                explanation = f"A + B = {p_A}% of C + {p_B}% of C = ({p_A} + {p_B})% of C = {val}% of C."
            question = random.choice(templates)
            
        elif sub_type == 'multi_var':
            b1 = random.choice([(1, 4, "25%"), (1, 5, "20%"), (3, 10, "30%")])
            b2 = random.choice([(1, 2, "0.5"), (1, 4, "0.25"), (1, 5, "0.2")])
            b3 = random.choice([(1, 3, "1/3"), (1, 5, "1/5"), (1, 6, "1/6")])
            
            n1, d1, s1 = b1
            n2, d2, s2 = b2
            n3, d3, s3 = b3
            
            def lcm(a, b): return abs(a*b) // math.gcd(a, b)
            num_lcm = lcm(n1, lcm(n2, n3))
            
            ra = (d1 * num_lcm) // n1
            rb = (d2 * num_lcm) // n2
            rc = (d3 * num_lcm) // n3
            
            g = math.gcd(ra, math.gcd(rb, rc))
            ra, rb, rc = ra//g, rb//g, rc//g
            
            question = f"If {s1} of A = {s2} of B = {s3} of C, then what is the ratio A : B : C?"
            correct = f"{ra}:{rb}:{rc}"
            explanation = f"Convert all to fractions: {n1}/{d1} A = {n2}/{d2} B = {n3}/{d3} C = k.\nSo A = {d1}/{n1} k, B = {d2}/{n2} k, C = {d3}/{n3} k.\nRatio A : B : C = {d1}/{n1} : {d2}/{n2} : {d3}/{n3}.\nMultiply by LCM of numerators to get integers: {correct}."
            
        elif sub_type == 'third_anchor':
            p1 = random.choice([20, 30, 40, 50])
            p2 = random.choice([40, 50, 60, 75])
            
            t = random.choice(['of_and_less', 'less_and_less'])
            if t == 'of_and_less':
                question = f"Two numbers are {p1}% of and {p2}% less than a third number respectively. The first number as a percentage of the second is:"
                num1 = p1
                num2 = 100 - p2
                exp_text = f"First number is {p1}% of C = {p1}. Second number is {p2}% less than C = 100 - {p2} = {100-p2}."
            else:
                question = f"Two numbers are {p1}% less than and {p2}% less than a third number respectively. What percent is the first of the second?"
                num1 = 100 - p1
                num2 = 100 - p2
                exp_text = f"First number is 100 - {p1} = {100-p1}. Second number is 100 - {p2} = {100-p2}."
            
            val = (num1 / num2) * 100
            correct = f"{int(val)}%" if val.is_integer() else f"{round(val, 2)}%"
            explanation = f"Let the third number be 100.\n{exp_text}\nThe percentage is ({num1} / {num2}) * 100 = {correct}."
            
        else: # sum_constraint
            p1 = random.choice([20, 30, 40, 50])
            p2 = random.choice([60, 70, 75, 80])
            f = Fraction(p2, p1)
            parts = f.numerator + f.denominator
            multiplier = random.randint(2, 10) * 10
            total_sum = parts * multiplier
            
            question = f"Out of two numbers, {p1}% of the greater number is equal to {p2}% of the smaller. If the sum of the numbers is {total_sum}, then the greater number is:"
            greater_val = f.numerator * multiplier
            correct = str(greater_val)
            explanation = f"Let G be greater, S be smaller.\n{p1}% of G = {p2}% of S => G/S = {p2}/{p1} = {f.numerator}/{f.denominator}.\nThe sum of the ratio parts is {f.numerator} + {f.denominator} = {parts}.\nThe actual sum is {total_sum}, so each part is {total_sum}/{parts} = {multiplier}.\nThe greater number G is {f.numerator} * {multiplier} = {correct}."

        options = [correct]
        attempts = 0
        while len(options) < 4 and attempts < 50:
            attempts += 1
            if ":" in correct: # Ratio
                parts = list(map(int, correct.split(':')))
                random.shuffle(parts)
                alt = ":".join(map(str, parts))
                if alt not in options: options.append(alt)
                else: 
                    alt = f"{parts[0]+1}:{parts[1]+1}" + (f":{parts[2]+1}" if len(parts)>2 else "")
                    if alt not in options: options.append(alt)
            elif "%" in correct:
                val = float(correct.replace("%", ""))
                alt_val = val + random.choice([-10, -5, 5, 10, 20])
                alt = f"{int(alt_val)}%" if float(alt_val).is_integer() else f"{round(alt_val, 2)}%"
                if alt not in options and alt_val > 0: options.append(alt)
            else:
                val = float(correct)
                alt_val = val + random.choice([-20, -10, 10, 20])
                alt = str(int(alt_val)) if float(alt_val).is_integer() else str(round(alt_val, 2))
                if alt not in options and alt_val > 0: options.append(alt)

        if len(options) < 4:
            if ":" in correct:
                parts = list(map(int, correct.split(':')))
                candidates = []
                for delta in range(1, 20):
                    candidates.append(":".join(str(max(1, p + delta)) for p in parts))
                    candidates.append(":".join(str(max(1, p + (delta if i == 0 else 0))) for i, p in enumerate(parts)))
                    candidates.append(":".join(str(max(1, p + (delta if i == len(parts) - 1 else 0))) for i, p in enumerate(parts)))
            elif "%" in correct:
                val = float(correct.replace("%", ""))
                candidates = [f"{int(v)}%" if float(v).is_integer() else f"{round(v, 2)}%" for v in (val + d for d in [-20, -15, -10, -5, 5, 10, 15, 20]) if v > 0]
            else:
                val = float(correct)
                candidates = [str(int(v)) if float(v).is_integer() else str(round(v, 2)) for v in (val + d for d in [-40, -30, -20, -10, 10, 20, 30, 40]) if v > 0]

            for candidate in candidates:
                if candidate not in options:
                    options.append(candidate)
                    if len(options) == 4:
                        break
        
        random.shuffle(options)
        return {
            "question_text": question,
            "options": options,
            "correct_option_index": options.index(correct),
            "explanation": explanation,
            "difficulty": 4
        }
