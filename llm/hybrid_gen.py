import random
import math
from fractions import Fraction

class HybridGenerator:
    def __init__(self):
        # Master list of GMAT benchmark fractions
        self.benchmarks = [
            (1, 2, "50%"), (1, 3, "33.33%"), (2, 3, "66.67%"),
            (1, 4, "25%"), (3, 4, "75%"),
            (1, 5, "20%"), (2, 5, "40%"), (3, 5, "60%"), (4, 5, "80%"),
            (1, 6, "16.67%"), (5, 6, "83.33%"),
            (1, 8, "12.5%"), (3, 8, "37.5%"), (5, 8, "62.5%"), (7, 8, "87.5%"),
            (1, 10, "10%"), (1, 12, "8.33%"), (1, 16, "6.25%"), (1, 20, "5%"),
            (1, 24, "4.17%"), (1, 25, "4%"), (1, 30, "3.33%"), (1, 40, "2.5%"),
            (1, 50, "2%")
        ]

    def generate_mixed_fraction(self):
        """Pattern 1: Improper Fraction to Mixed Fraction"""
        denom = random.randint(2, 50)
        whole = random.randint(1, 12)
        rem = random.randint(1, denom - 1)
        
        improper_num = (whole * denom) + rem
        question = f"Convert the improper fraction {improper_num}/{denom} into a mixed fraction."
        
        correct = f"{whole}({rem}/{denom})"
        
        # Distractors
        options = [correct]
        while len(options) < 4:
            w = max(1, whole + random.randint(-2, 2))
            r = max(1, rem + random.randint(-3, 3)) % denom
            if r == 0: r = 1
            opt = f"{w}({r}/{denom})"
            if opt not in options:
                options.append(opt)
        
        random.shuffle(options)
        return {
            "question_text": question,
            "options": options,
            "correct_option_index": options.index(correct),
            "explanation": f"{improper_num} divided by {denom} gives {whole} with a remainder of {rem}. So, it's {whole} and {rem}/{denom}.",
            "difficulty": 2
        }

    def generate_fraction_subtraction(self):
        """Pattern 2: Fraction Subtraction (Meaningful numbers)"""
        # Pick denominators that are likely to have a clean LCM
        denoms = [2, 3, 4, 5, 6, 8, 10, 12, 15, 20, 24, 30]
        d1 = random.choice(denoms)
        d2 = random.choice(denoms)
        
        f1 = Fraction(random.randint(1, d1*2), d1)
        f2 = Fraction(random.randint(1, d2), d2)
        
        # Ensure f1 > f2
        if f1 <= f2:
            f1, f2 = f2, f1
            if f1 == f2: f1 += Fraction(1, d1)

        question = f"What is the value of {f1} - {f2}?"
        correct_frac = f1 - f2
        correct = str(correct_frac)
        
        options = [correct]
        while len(options) < 4:
            # Common errors: subtracting numerators and denominators
            if len(options) == 1:
                alt = f"{abs(f1.numerator - f2.numerator)}/{abs(f1.denominator - f2.denominator)}" if f1.denominator != f2.denominator else "Error"
                if alt != correct and "/" in alt: options.append(alt)
                
            w_num = max(1, correct_frac.numerator + random.randint(-5, 5))
            w_den = correct_frac.denominator # often students get denom right but num wrong
            opt = str(Fraction(w_num, w_den))
            if opt not in options:
                options.append(opt)
                
        random.shuffle(options)
        return {
            "question_text": question,
            "options": options,
            "correct_option_index": options.index(correct),
            "explanation": f"To subtract fractions, find a common denominator. {f1} - {f2} = {correct}.",
            "difficulty": 3
        }

    def generate_random_conv(self):
        """Pattern 3: Per to fraction and vice versa (Random numbers)"""
        den = random.choice([20, 25, 40, 50, 80, 100])
        num = random.randint(1, den - 1)
        f = Fraction(num, den)
        p = f"{float(f)*100:.1f}%".replace(".0%", "%")
        
        to_percentage = random.random() > 0.5
        if to_percentage:
            question = f"Convert the fraction {f} to its percentage form."
            correct = p
        else:
            question = f"Convert {p} to its simplified fraction form."
            correct = str(f)
            
        options = [correct]
        while len(options) < 4:
            if to_percentage:
                val = f"{random.randint(5, 95)}%"
            else:
                val = f"{random.randint(1, 19)}/{random.choice([20, 25, 40, 50])}"
            if val not in options:
                options.append(val)
                
        random.shuffle(options)
        return {
            "question_text": question,
            "options": options,
            "correct_option_index": options.index(correct),
            "explanation": f"To convert fraction to percent, multiply by 100: ({f} * 100)% = {p}. To convert percent to fraction, divide by 100: {p}/100 = {f}.",
            "difficulty": 2
        }

    def generate_benchmark_conv(self):
        """Pattern 4: basic fraction to per (Common GMAT Benchmarks)"""
        num, den, perc = random.choice(self.benchmarks)
        
        # Focus heavily on Fraction -> Percentage as it's more common for memory
        question = f"What is the percentage value for the benchmark fraction {num}/{den}?"
        correct = perc
                
        options = [correct]
        # Distractors from other benchmarks to make it challenging
        while len(options) < 4:
            _, _, p_alt = random.choice(self.benchmarks)
            if p_alt not in options:
                options.append(p_alt)
                
        random.shuffle(options)
        return {
            "question_text": question,
            "options": options,
            "correct_option_index": options.index(correct),
            "explanation": f"This is a common GMAT benchmark: {num}/{den} is exactly {perc}. Memorizing this will save you significant time on the exam.",
            "difficulty": 2
        }

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

    def generate_fraction_to_decimal(self):
        """Pattern Q5: Drills for benchmark fraction-to-decimal."""
        num, den, perc = random.choice(self.benchmarks)
        # Use more "trap" benchmarks for this drill
        traps = [(1, 6, 0.1667), (1, 12, 0.0833), (1, 16, 0.0625), (1, 24, 0.0417), (1, 30, 0.0333)]
        if random.random() > 0.4:
            num, den, decimal = random.choice(traps)
        else:
            decimal = round(num / den, 4)

        to_decimal = random.random() > 0.5
        if to_decimal:
            question = f"Convert the fraction {num}/{den} to its decimal form."
            correct = str(decimal)
        else:
            question = f"Convert the decimal {decimal} to its simplest fraction form."
            correct = f"{num}/{den}"
            
        options = [correct]
        while len(options) < 4:
            if to_decimal:
                alt = str(round(decimal + random.uniform(-0.02, 0.02), 4))
            else:
                n_alt = max(1, num + random.randint(-2, 2))
                d_alt = den if random.random() > 0.5 else den + random.randint(-5, 5)
                alt = f"{n_alt}/{d_alt}"
            if alt not in options:
                options.append(alt)
                
        random.shuffle(options)
        return {
            "question_text": question,
            "options": options,
            "correct_option_index": options.index(correct),
            "explanation": f"{num}/{den} is exactly {decimal}. (Note: {perc} in percentage form).",
            "difficulty": 2
        }

    def generate_swap_percentage(self):
        """Patterns Q6, Q7, Q10: Swapping and Scaling properties."""
        sub_type = random.choice(['swap', 'scale', 'composite'])
        
        if sub_type == 'swap':
            # a% of b = b% of a
            a = random.randint(11, 99)
            b = random.choice([20, 25, 50, 75, 100, 200, 250, 500])
            question = f"What is {a}% of {b}?"
            # Solution uses b% of a
            correct = (a * b) / 100
            explanation = f"Using the property a% of b = b% of a, we can calculate {b}% of {a}. \n{b}% of {a} is {b/100} * {a} = {correct}."
        
        elif sub_type == 'scale':
            # Doubling/Halving (Q7)
            # ex: 48% of 82 = 96% of 41
            a = random.randint(10, 49) * 2
            b = random.randint(10, 50) 
            question = f"Find the value of {a}% of {b}."
            correct = (a * b) / 100
            explanation = f"Using scaling: {a}% of {b} is the same as {(a*2)}% of {b/2} or {(a/2)}% of {b*2}. \nIf we use {(a*2)}% of {b/2}, it might be easier. Result: {correct}."

        else: # composite (Q10)
            # 45% of 280 + 28% of 450
            a = random.choice([15, 25, 35, 45, 55])
            b = random.choice([120, 180, 240, 280, 360])
            # Second part: b/10 % of a*10
            # 45% of 280 = 28% of 450
            question = f"Calculate the value of: {a}% of {b} + {b//10}% of {a*10}"
            correct = 2 * (a * b / 100)
            explanation = f"Notice that {b//10}% of {a*10} is the same as {b}% of {a} (by moving the 0 and %). \nSince a% of b = b% of a, the expression is just 2 * ({a}% of {b}) = 2 * {a*b/100} = {correct}."

        correct_str = str(int(correct)) if correct == int(correct) else str(round(correct, 2))
        options = [correct_str]
        while len(options) < 4:
            alt = float(correct_str) + random.randint(-10, 10) * (2 if float(correct_str) > 50 else 0.5)
            alt_str = str(int(alt)) if alt == int(alt) else str(round(alt, 2))
            if alt_str not in options:
                options.append(alt_str)
        random.shuffle(options)
        return {
            "question_text": question,
            "options": options,
            "correct_option_index": options.index(correct_str),
            "explanation": explanation,
            "difficulty": 3
        }

    def generate_breakdown_percentage(self):
        """Patterns Q8, Q9, Q11: Decomposition and Repeating decimals."""
        sub_type = random.choice(['place_value', 'breakdown', 'repeating'])
        
        if sub_type == 'place_value':
            # Q8: 10%, 1%, 0.1%
            num = random.randint(1000, 9999)
            target = random.choice([10, 1, 0.1, 0.01])
            question = f"What is {target}% of {num}?"
            correct = (target * num) / 100
            explanation = f"To find {target}%, move the decimal point of {num} towards the left. \n100% = {num} \n10% = {num/10} \n1% = {num/100} \n0.1% = {num/1000} \nResult: {correct}."
        
        elif sub_type == 'breakdown':
            # Q9: 43.75% = 50% - 6.25%
            # Or 37.5% = 25% + 12.5%
            val, breakdown_text, fraction = random.choice([
                (43.75, "50% - 6.25%", "1/2 - 1/16 = 7/16"),
                (37.5, "25% + 12.5%", "1/4 + 1/8 = 3/8"),
                (62.5, "50% + 12.5%", "1/2 + 1/8 = 5/8"),
                (87.5, "100% - 12.5%", "1 - 1/8 = 7/8"),
                (18.75, "12.5% + 6.25%", "1/8 + 1/16 = 3/16")
            ])
            # Pick a multiple of 16 to keep it clean
            x = random.randint(5, 50) * 16
            question = f"Calculate {val}% of {x} using the breakdown method."
            correct = (val * x) / 100
            explanation = f"{val}% can be broken down into {breakdown_text}. \nIn fractions, this is {fraction}. \nResult: {fraction} of {x} = {correct}."

        else: # repeating (Q11)
            # 55.55% = 5/9, 72.72% = 8/11
            num, den, perc_str, factor = random.choice([
                (1, 9, "11.11%", 1), (5, 9, "55.55%", 5), (7, 9, "77.77%", 7),
                (1, 11, "09.09%", 1), (8, 11, "72.72%", 8), (4, 11, "36.36%", 4)
            ])
            x = den * random.randint(10, 100)
            question = f"What is {perc_str} of {x}?"
            correct = (x * num) // den
            explanation = f"Notice the repeating pattern {perc_str}. \nIf it's digits repeating (like 55.55), it's a multiple of 1/9 (11.11%). \nIf it's pairs repeating (like 72.72), it's a multiple of 1/11 (09.09%). \n{perc_str} = {num}/{den}. \n{num}/{den} of {x} = {correct}."

        correct_str = str(int(correct)) if correct == int(correct) else str(round(correct, 3))
        options = [correct_str]
        while len(options) < 4:
            alt = float(correct_str) + random.randint(-10, 10) * (2 if float(correct_str) > 50 else 0.5)
            alt_str = str(int(alt)) if alt == int(alt) else str(round(alt, 3))
            if alt_str not in options:
                options.append(alt_str)
        random.shuffle(options)
        return {
            "question_text": question,
            "options": options,
            "correct_option_index": options.index(correct_str),
            "explanation": explanation,
            "difficulty": 4
        }

    def generate_percentage_equations(self):
        """Phase 18 Category 1: Percentage Equations & Ratios"""
        sub_type = random.choice(['sum_diff', 'direct_eq', 'multi_var', 'third_anchor', 'sum_constraint'])
        
        if sub_type == 'sum_diff':
            # e.g., 40% (a+b) = 60% (a-b), find ratio or expression like a/b
            p1 = random.choice([10, 15, 20, 25, 30, 40])
            p2 = random.choice([50, 60, 70, 75, 80])
            f = Fraction(p1 + p2, p2 - p1)
            
            expr_type = random.choice(['ratio', 'percentage'])
            if expr_type == 'ratio':
                question = f"If {p1}% of (A + B) = {p2}% of (A - B), then what is the ratio of A to B?"
                correct = f"{f.numerator}:{f.denominator}"
                explanation = f"{p1}(A + B) = {p2}(A - B)\n=> {p1}A + {p1}B = {p2}A - {p2}B\n=> ({p1} + {p2})B = ({p2} - {p1})A\n=> {p1+p2}B = {p2-p1}A\n=> A/B = {p1+p2}/{p2-p1} = {f.numerator}/{f.denominator}."
            else:
                question = f"If {p1}% of (A + B) = {p2}% of (A - B), then A is what percent of B?"
                val = float(f) * 100
                correct = f"{int(val)}%" if val.is_integer() else f"{round(val, 2)}%"
                explanation = f"{p1}(A + B) = {p2}(A - B)\n=> {p1+p2}B = {p2-p1}A\n=> A/B = {f.numerator}/{f.denominator}.\nAs a percentage: ({f.numerator}/{f.denominator}) * 100 = {correct}."
                
        elif sub_type == 'direct_eq':
            # e.g., 80% A = 50% B. Find B as x% of A.
            p1 = random.choice([40, 50, 60, 75, 80])
            p2 = random.choice([10, 20, 25, 30])
            f = Fraction(p1, p2)
            val = float(f) * 100
            correct = f"{int(val)}" if val.is_integer() else f"{round(val, 2)}"
            question = f"If {p1}% of A = {p2}% of B, and B = x% of A, then find the value of x."
            explanation = f"{p1}% of A = {p2}% of B\n=> {p1}A = {p2}B\n=> B/A = {p1}/{p2} = {f.numerator}/{f.denominator}.\nSo B is ({f.numerator}/{f.denominator}) * 100% of A = {correct}% of A. Thus x = {correct}."
            
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
        while len(options) < 4:
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
                alt = f"{int(alt_val)}%" if alt_val.is_integer() else f"{round(alt_val, 2)}%"
                if alt not in options and alt_val > 0: options.append(alt)
            else:
                val = float(correct)
                alt_val = val + random.choice([-20, -10, 10, 20])
                alt = str(int(alt_val)) if alt_val.is_integer() else str(round(alt_val, 2))
                if alt not in options and alt_val > 0: options.append(alt)
        
        random.shuffle(options)
        return {
            "question_text": question,
            "options": options,
            "correct_option_index": options.index(correct),
            "explanation": explanation,
            "difficulty": 4
        }

    def generate_base_comparisons(self):
        """Phase 18 Category 2: Base Comparisons & Successive Chains"""
        sub_type = random.choice(['direct_base', 'missing_val', 'chain', 'successive', 'var_chain'])
        
        if sub_type == 'direct_base':
            t = random.choice(['of', 'less_than'])
            if t == 'of':
                p = random.choice([5, 10, 15, 20, 25, 30, 40, 50, 60, 75, 80])
                Y = random.randint(10, 100) * 10
                X = (p * Y) // 100
                if random.random() > 0.5: 
                    X, Y = X / 10, Y / 10
                question = f"{X} is what percent of {Y}?"
                correct = f"{p}%"
                explanation = f"Percent = (Part / Whole) * 100\n= ({X} / {Y}) * 100 = {p}%."
            else:
                p = random.choice([10, 20, 25, 30, 40, 50, 60, 75, 80])
                Y = random.randint(10, 100) * 10
                X = Y - (p * Y) // 100
                if random.random() > 0.5: 
                    X, Y = X / 10, Y / 10
                question = f"{X} is what percent less than {Y}?"
                correct = f"{p}%"
                explanation = f"Percent less = (Difference / Original Base) * 100\nDifference = {Y} - {X} = {Y-X}.\n({Y-X} / {Y}) * 100 = {p}%."
                
        elif sub_type == 'missing_val':
            if random.random() > 0.5:
                p1, X1 = random.choice([10, 15, 20, 25, 30]), random.randint(10, 50) * 10
                p2, X2 = random.choice([15, 20, 25, 30, 40, 50]), random.randint(20, 60) * 10
                val1 = (p1 * X1) // 100
                val2 = (p2 * X2) // 100
                if val1 >= val2: val2 = val1 + random.randint(10, 50)
                ans = val2 - val1
                question = f"What must be added to {p1}% of {X1} so that the sum is equal to {p2}% of {X2}?"
                correct = str(ans)
                explanation = f"Calculate both parts:\n{p1}% of {X1} = {val1}\n{p2}% of {X2} = {val2}\nDifference = {val2} - {val1} = {ans}. You must add {ans}."
            else:
                p1 = random.choice([12, 15, 18, 20, 24, 25])
                p2 = random.choice([10, 12, 16, 20, 25, 30])
                num2 = random.randint(20, 100) * 5
                num2 = (num2 // p1) * p1
                if num2 == 0: num2 = p1 * 5
                ans = (p2 * num2) // p1
                question = f"{p1}% of which number is equal to {p2}% of {num2}?"
                correct = str(ans)
                explanation = f"Let the number be x.\n{p1}% of x = {p2}% of {num2}\n({p1}/100) * x = {p2 * num2 / 100}\n{p1}x = {p2 * num2}\nx = {p2 * num2} / {p1} = {ans}."
                
        elif sub_type == 'chain':
            p1 = random.choice([12, 15, 18, 20, 24]) 
            p2 = random.choice([10, 15, 20, 25])     
            num = random.choice([20, 25, 30, 40, 50]) 
            den = random.choice([3, 4, 6, 8, 9, 12])  
            
            d_total = 10000 * den
            n_total = p1 * p2 * num
            g = math.gcd(d_total, n_total)
            base_total = d_total // g
            
            Total = base_total * random.randint(1, 10) * 100
            ans = (p1 * p2 * num * Total) // (10000 * den)
            
            question = f"The value of {p1}% of {p2}% of {num}/{den} of {Total} is:"
            correct = str(ans)
            explanation = f"Convert percentages to fractions and multiply out:\n({p1}/100) * ({p2}/100) * ({num}/{den}) * {Total}\n= ({p1*p2}/{10000}) * ({num}/{den}) * {Total}\n= {ans}."
            
        elif sub_type == 'successive':
            p1 = random.choice([10, 20, 25])
            p2 = random.choice([10, 20, 25])
            Z = random.choice([100, 125, 150, 200, 250])
            t1 = random.choice(['more', 'less'])
            t2 = random.choice(['more', 'less'])
            
            m1 = (100 + p1) / 100 if t1 == 'more' else (100 - p1) / 100
            m2 = (100 + p2) / 100 if t2 == 'more' else (100 - p2) / 100
            
            val_y = Z * m2
            val_x = val_y * m1
            
            question = f"If a number x is {p1}% {t1} than another number y, and y is {p2}% {t2} than {Z}, then x is equal to:"
            correct = str(int(val_x)) if val_x.is_integer() else str(round(val_x, 2))
            explanation = f"Step 1: Find y. y is {p2}% {t2} than {Z}.\ny = {Z} * {m2} = {val_y}\nStep 2: Find x. x is {p1}% {t1} than y.\nx = {val_y} * {m1} = {correct}."
            
        else: # var_chain
            A_val = random.choice([5, 10, 20, 25, 40, 50])
            val1 = random.choice([5, 10, 20, 40, 50, 100])
            val2 = random.choice([10, 20, 25, 40, 50])
            ans = (val2 * val1) / 100
            
            question = f"If b = A% of {val1}, then {val2}% of 'b' is the same as:"
            correct = f"{int(ans)}% of A" if ans.is_integer() else f"{round(ans, 2)}% of A"
            explanation = f"b = (A / 100) * {val1}\n{val2}% of b = ({val2} / 100) * b\nSubstitute b: ({val2} / 100) * (A / 100) * {val1}\nRearranging: A * ({val2} * {val1} / 10000)\n= ({ans} / 100) * A\n= {correct}."

        options = [correct]
        while len(options) < 4:
            if "% of A" in correct:
                val = float(correct.split("%")[0])
                alt_val = val * random.choice([0.5, 2, 10, 0.1, 5])
                alt = f"{int(alt_val)}% of A" if alt_val.is_integer() else f"{round(alt_val, 2)}% of A"
                if alt not in options and alt_val > 0: options.append(alt)
            elif "%" in correct:
                val = float(correct.replace("%", ""))
                alt_val = val + random.choice([-10, -5, 5, 10, 20])
                alt = f"{int(alt_val)}%" if alt_val.is_integer() else f"{round(alt_val, 2)}%"
                if alt not in options and alt_val > 0: options.append(alt)
            else:
                val = float(correct)
                alt_val = val + random.choice([-20, -10, 10, 20, -val*0.1, val*0.1])
                alt_val = max(1, alt_val)
                alt = str(int(alt_val)) if alt_val.is_integer() else str(round(alt_val, 2))
                if alt not in options: options.append(alt)
        
        random.shuffle(options)
        return {
            "question_text": question,
            "options": options,
            "correct_option_index": options.index(correct),
            "explanation": explanation,
            "difficulty": 4
        }

    def generate_applied_percentages(self):
        """Phase 18 Category 3: Applied Scenarios & Complex Calculations"""
        sub_type = random.choice(['fraction_shift', 'weighted_avg', 'population_split', 'calc_trick_add', 'calc_trick_sub'])
        
        if sub_type == 'fraction_shift':
            p_num = random.choice([100, 150, 200, 250, 300]) 
            p_den = random.choice([100, 200, 300, 400, 500]) 
            num = random.randint(1, 10)
            den = random.randint(2, 12)
            orig_f = Fraction(num, den) 
            
            m_num = Fraction(100 + p_num, 100)
            m_den = Fraction(100 + p_den, 100)
            
            new_f = orig_f * (m_num / m_den)
            
            question = f"If the numerator of a fraction is increased by {p_num}% and the denominator is increased by {p_den}%, the resultant fraction is {new_f.numerator}/{new_f.denominator}. What was the original fraction?"
            correct = f"{orig_f.numerator}/{orig_f.denominator}"
            explanation = f"Let original fraction be x/y.\nNew numerator = {100+p_num}% of x = {(100+p_num)/100}x\nNew denominator = {100+p_den}% of y = {(100+p_den)/100}y\nSo, ({(100+p_num)/100}x) / ({(100+p_den)/100}y) = {new_f.numerator}/{new_f.denominator}\nx/y = ({new_f.numerator}/{new_f.denominator}) * ({(100+p_den)/100} / {(100+p_num)/100}) = {correct}."
            
        elif sub_type == 'weighted_avg':
            half = random.choice([30, 40, 50, 60, 80])
            total = half * 2
            
            p_first = random.choice([55, 60, 65, 70])
            p_target = p_first + random.choice([5, 10, 15])
            
            p_second = 2 * p_target - p_first
            
            scenario = random.choice([
                f"In a test consisting of {total} questions carrying one mark each, a student answers {p_first}% of the first {half} questions correctly. What percent of the other {half} questions does she need to answer correctly to score {p_target}% on the entire test?",
                f"A company has {total} employees. {p_first}% of the first {half} interviewed support a new policy. What percentage of the remaining {half} must support it so the overall approval rating is {p_target}%?"
            ])
            question = scenario
            correct = f"{p_second}%"
            explanation = f"Total target score = {p_target}% of {total}. Since the two groups are of equal size ({half}), the overall percentage is just the simple average of the two percentages.\n({p_first}% + x%) / 2 = {p_target}%\n{p_first} + x = {p_target * 2}\nx = {p_second}%."
            
        elif sub_type == 'population_split':
            p_b = random.choice([40, 45, 55, 60, 65, 70])
            p_g = 100 - p_b
            
            total = random.randint(50, 500) * 20
            b_val = int(total * p_b / 100)
            g_val = int(total * p_g / 100)
            
            scenarios = [
                (f"If {p_b}% of the students in a school are boys and the number of girls is {g_val}. How many boys are there?", f"{b_val}", "boys"),
                (f"In a factory, {p_b}% of the manufactured cars are black. If {g_val} cars are not black, how many black cars are produced?", f"{b_val}", "black cars"),
                (f"A fruit basket contains apples and oranges. If {p_b}% of the fruits are apples and there are {g_val} oranges, how many apples are there?", f"{b_val}", "apples")
            ]
            q_text, correct, label = random.choice(scenarios)
            question = q_text
            explanation = f"Since {p_b}% are {label}, the remaining {p_g}% represent the other group.\n{p_g}% of Total = {g_val}\nTotal = {g_val} / {p_g/100} = {total}\nNumber of {label} = {total} - {g_val} = {correct}."
            
        elif sub_type == 'calc_trick_add':
            A = random.choice([45.5, 62.5, 78.5, 82.5, 94.5])
            B = random.choice([36, 42, 64, 84])
            
            term1 = (A * B * 10) / 100
            term2 = (B * A * 10) / 100 
            total_sum = term1 + term2
            
            target_diff = random.randint(10, 50) * 10
            rhs = total_sum - target_diff
            
            question = f"Calculate the missing value (?): {A}% of {B*10} + {B}% of {int(A*10)} - ? = {int(rhs)}"
            correct = str(int(target_diff))
            explanation = f"Notice the trick: {B}% of {int(A*10)} is exactly the same as {B*10}% of {A}, which is also equal to {A}% of {B*10}!\nSo the left side is 2 * ({A}% of {B*10}).\n2 * {term1} = {total_sum}.\n{total_sum} - ? = {int(rhs)}\n? = {target_diff}."
            
        else: # calc_trick_sub
            a = random.choice([6.4, 4.5, 8.2, 5.5])
            b = random.randint(100, 1500)
            c = random.choice([3.5, 2.5, 4.2, 1.5])
            d = random.randint(100, 500)
            
            t1 = (a * b) / 100
            t2 = (c * d) / 100
            ans = round(t1 - t2, 4)
            
            question = f"Find the exact value of ({a}% of {b}) - ({c}% of {d}):"
            correct = f"{int(ans)}" if ans.is_integer() else f"{round(ans, 4)}"
            explanation = f"Calculate each term separately. Multiply the decimal out:\n{a}% of {b} = {a/100} * {b} = {t1}\n{c}% of {d} = {c/100} * {d} = {t2}\nDifference = {t1} - {t2} = {correct}."

        options = [correct]
        while len(options) < 4:
            if "/" in correct: 
                n, d = map(int, correct.split('/'))
                alt_n = n + random.choice([-2, -1, 1, 2])
                alt_d = d + random.choice([-2, 0, 2])
                if alt_n > 0 and alt_d > 0:
                    alt = f"{alt_n}/{alt_d}"
                    if alt not in options: options.append(alt)
            elif "%" in correct:
                val = float(correct.replace("%", ""))
                alt_val = val + random.choice([-10, -5, 5, 10, 20])
                alt = f"{int(alt_val)}%" if alt_val.is_integer() else f"{round(alt_val, 2)}%"
                if alt not in options and alt_val > 0: options.append(alt)
            else:
                val = float(correct)
                alt_val = val + random.choice([-20, -10, 10, 20, -min(10, val*0.1), min(10, val*0.1), 1, -1])
                alt_val = max(0, alt_val)
                alt = str(int(alt_val)) if alt_val.is_integer() else str(round(alt_val, 4))
                if alt not in options: options.append(alt)
        
        random.shuffle(options)
        return {
            "question_text": question,
            "options": options,
            "correct_option_index": options.index(correct),
            "explanation": explanation,
            "difficulty": 4
        }

hybrid_generator = HybridGenerator()
