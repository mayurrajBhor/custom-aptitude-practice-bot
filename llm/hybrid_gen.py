import random
import math
from fractions import Fraction

class HybridGenerator:
    def __init__(self):
        # Master list of GMAT benchmark fractions requested by user
        self.benchmarks = [
            (1, 2, "50%"), (1, 3, "33.33%"), (1, 4, "25%"), (1, 5, "20%"),
            (1, 6, "16.67%"), (1, 7, "14.28%"), (1, 8, "12.5%"), (1, 9, "11.11%"), 
            (1, 10, "10%"), (1, 11, "9.09%"), (1, 12, "8.33%"), (1, 13, "7.69%"), 
            (1, 14, "7.14%"), (1, 15, "6.67%"), (1, 16, "6.25%"), (1, 17, "5.88%"), 
            (1, 18, "5.55%"), (1, 19, "5.26%"), (1, 20, "5%"),
            (1, 25, "4%"), (1, 30, "3.33%"), (1, 40, "2.5%"), (1, 50, "2%"),
            (3, 8, "37.5%"), (5, 8, "62.5%"), 
            (4, 7, "57.14%"), (5, 7, "71.42%"), 
            (5, 6, "83.33%")
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

    def generate_alligation_shifts(self):
        """Phase 19 Category: Alligation & Shift Applications"""
        sub_type = random.choice(['double_shift_nested', 'simple_pop_split', 'qty_value_overlap'])
        
        if sub_type == 'double_shift_nested':
            # Q1: Total Pop = M + F. M grows by X%, F grows by Y%. New Total = N. 
            # Sub-question: P% of M are boys, Q% of F are girls. Diff between boys and girls?
            # To ensure clean numbers, pick M and F first.
            M = random.randint(30, 80) * 100
            F = random.randint(30, 80) * 100
            while M == F: F = random.randint(30, 80) * 100
            Total1 = M + F
            
            p_m = random.choice([5, 8, 10, 12, 14, 15, 20])
            p_f = random.choice([4, 6, 8, 10, 15, 16, 25])
            while p_m == p_f: p_f = random.choice([4, 6, 8, 10, 15, 16, 25])
            
            # Allow decimal percentages in the prompt for "trickiness" (e.g. 14.2%, 17.7%) but just calculate exact integer growths
            # Actually, generating exact matching decimals is tricky, let's stick to fractional percentage strings if needed, 
            # but standard integers are safest. Let's add decimals like +0.2% and +0.7% if M/F are multiples of 1000
            if M % 1000 == 0 and F % 1000 == 0:
                p_m_dec = p_m + random.choice([0.2, 0.4, 0.5])
                p_f_dec = p_f + random.choice([0.5, 0.7, 0.8])
            else:
                p_m_dec, p_f_dec = float(p_m), float(p_f)
                
            growth_m = int(M * (p_m_dec / 100.0))
            growth_f = int(F * (p_f_dec / 100.0))
            Total2 = Total1 + growth_m + growth_f
            
            b_perc = random.choice([10, 15, 20, 25, 30])
            g_perc = random.choice([10, 12, 15, 18, 20, 25])
            
            boys = int(M * (b_perc / 100.0))
            girls = int(F * (g_perc / 100.0))
            ans = abs(boys - girls)
            
            p_m_str = f"{p_m_dec}%" if p_m_dec != int(p_m_dec) else f"{int(p_m_dec)}%"
            p_f_str = f"{p_f_dec}%" if p_f_dec != int(p_f_dec) else f"{int(p_f_dec)}%"
            
            question = f"The total population of a city is {Total1}. The male population is increased by {p_m_str} and the female population by {p_f_str}, making the total population {Total2}. If {b_perc}% of the total original male population are boys and {g_perc}% of the total original female population are girls, find the difference between the number of boys and girls."
            correct = str(ans)
            
            # Using alligation / shift logic for explanation
            shift = min(p_m_dec, p_f_dec)
            extra = max(p_m_dec, p_f_dec) - shift
            larger_group_is_male = p_m_dec > p_f_dec
            base_growth = int(Total1 * (shift / 100.0))
            actual_growth = Total2 - Total1
            difference = actual_growth - base_growth
            larger_pop = int((difference * 100.0) / extra)
            
            if larger_group_is_male:
                calc_M = larger_pop
                calc_F = Total1 - calc_M
            else:
                calc_F = larger_pop
                calc_M = Total1 - calc_F
                
            explanation = f"Use the shifting method:\nAssume both grew by {shift}%. Growth would be {shift}% of {Total1} = {base_growth}.\nActual growth = {Total2} - {Total1} = {actual_growth}.\nExtra growth = {actual_growth} - {base_growth} = {difference}.\nThis extra growth comes from the extra {extra}% of the {'male' if larger_group_is_male else 'female'} population.\nSo, {extra}% of {'Males' if larger_group_is_male else 'Females'} = {difference} => {'Males' if larger_group_is_male else 'Females'} = {larger_pop}.\nThus, Males = {calc_M} and Females = {calc_F}.\nBoys = {b_perc}% of {calc_M} = {boys}.\nGirls = {g_perc}% of {calc_F} = {girls}.\nDifference = |{boys} - {girls}| = {ans}."
            
        elif sub_type == 'simple_pop_split':
            # Q2: simpler variation of Q1. Find current M & F.
            M = random.randint(20, 60) * 100
            F = random.randint(20, 60) * 100
            while M == F: F = random.randint(20, 60) * 100
            Total1 = M + F
            
            p_m = random.choice([4, 5, 8, 10, 12, 15])
            p_f = random.choice([6, 9, 11, 14, 18, 20])
            while p_m == p_f: p_f = random.choice([6, 9, 11, 14, 18, 20])
            
            Total2 = Total1 + int(M * (p_m/100.0)) + int(F * (p_f/100.0))
            
            ask_current = random.choice([True, False])
            if ask_current:
                question = f"The population of a town is {Total1}. If males increase by {p_m}% and females increase by {p_f}%, then after a year the population becomes {Total2}. Find the CURRENT (increased) male and female population."
                ans_M = M + int(M * (p_m/100.0))
                ans_F = F + int(F * (p_f/100.0))
                term = "current (increased)"
            else:
                question = f"The population of a town is {Total1}. If males increase by {p_m}% and females increase by {p_f}%, then after a year the population becomes {Total2}. Find the ORIGINAL male and female population."
                ans_M = M
                ans_F = F
                term = "original"
                
            correct = f"{ans_M} Males, {ans_F} Females"
            
            shift = min(p_m, p_f)
            extra = max(p_m, p_f) - shift
            larger_group_is_male = p_m > p_f
            base_growth = int(Total1 * (shift / 100.0))
            actual_growth = Total2 - Total1
            difference = actual_growth - base_growth
            larger_pop = int((difference * 100.0) / extra)
            
            if larger_group_is_male:
                calc_M = larger_pop
                calc_F = Total1 - calc_M
            else:
                calc_F = larger_pop
                calc_M = Total1 - calc_F
                
            explanation = f"Use Alligation or Shifting:\nMinimum growth is {shift}%. If all {Total1} grew by {shift}%, growth = {base_growth}.\nActual growth = {actual_growth}. Difference = {difference}.\nThis {difference} is due to the extra {round(extra, 2)}% of {'Males' if larger_group_is_male else 'Females'}.\nSo, Original {'Males' if larger_group_is_male else 'Females'} = {larger_pop}.\nOriginal Males = {calc_M}, Original Females = {calc_F}.\nThe {term} values are {ans_M} Males and {ans_F} Females."

        else: # qty_value_overlap
            # Q3: Cats and dogs, biscuits.
            # Group 1 = G1, Group 2 = G2
            G1 = random.randint(15, 30)
            G2 = random.randint(15, 30)
            while G1 == G2: G2 = random.randint(15, 30)
            
            T_animals = G1 + G2
            
            V1 = random.randint(3, 8)
            V2 = V1 + random.randint(2, 5)
            
            T_biscuits = G1 * V1 + G2 * V2
            
            themes = [
                ("cats", "dogs", "biscuits", "eats"),
                ("boys", "girls", "candies", "gets"),
                ("cars", "bikes", "tires", "has"),
                ("adults", "children", "tickets", "buys")
            ]
            t_A, t_B, t_item, t_verb = random.choice(themes)
            
            question = f"There are two types of groups in a room: {t_A} and {t_B}. Each {t_A[:-1]} {t_verb} {V1} {t_item} and each {t_B[:-1]} {t_verb} {V2} {t_item}. If {T_biscuits} {t_item} are distributed among {T_animals} individuals, find the number of {t_A} and {t_B}."
            correct = f"{G1} {t_A}, {G2} {t_B}"
            
            shift = V1
            extra = V2 - V1
            base_items = T_animals * shift
            diff = T_biscuits - base_items
            calc_G2 = diff // extra
            calc_G1 = T_animals - calc_G2
            
            explanation = f"Use the shifting method:\nAssume EVERY individual {t_verb} the minimum amount ({V1} {t_item}).\nTotal {t_item} used = {T_animals} * {V1} = {base_items}.\nRemaining {t_item} = {T_biscuits} - {base_items} = {diff}.\nThese {diff} {t_item} belong to the {t_B} because each {t_B[:-1]} gets {extra} extra {t_item} ({V2} - {V1}).\nNumber of {t_B} = {diff} / {extra} = {calc_G2}.\nNumber of {t_A} = {T_animals} - {calc_G2} = {calc_G1}.\nThus, {G1} {t_A} and {G2} {t_B}."

        options = [correct]
        while len(options) < 4:
            if "," in correct and "Males" in correct:
                M_alt = max(100, int(correct.split(" ")[0]) + random.choice([-200, -100, 100, 200]))
                F_alt = max(100, int(correct.split(", ")[1].split(" ")[0]) + random.choice([-200, -100, 100, 200]))
                alt = f"{M_alt} Males, {F_alt} Females"
                if alt not in options: options.append(alt)
            elif "," in correct:
                # the cats/dogs version
                p1 = int(correct.split(" ")[0])
                p2 = int(correct.split(", ")[1].split(" ")[0])
                n1 = correct.split(" ")[1].replace(",", "")
                n2 = correct.split(", ")[1].split(" ")[1]
                
                alt_p1 = max(1, p1 + random.choice([-5, -3, 2, 4, 5]))
                alt_p2 = (p1 + p2) - alt_p1 # sum remains same
                if alt_p2 > 0:
                    alt = f"{alt_p1} {n1}, {alt_p2} {n2}"
                    if alt not in options: options.append(alt)
                else:
                    alt = f"{p2} {n1}, {p1} {n2}" # swab
                    if alt not in options: options.append(alt)
            else:
                val = int(correct)
                alt_val = max(1, val + random.choice([-50, -20, 20, 50, 100, -100]))
                if str(alt_val) not in options: options.append(str(alt_val))
                
        random.shuffle(options)
        return {
            "question_text": question,
            "options": options,
            "correct_option_index": options.index(correct),
            "explanation": explanation,
            "difficulty": 4
        }

    def generate_percentage_comparisons(self):
        """Phase 20 Cat 1: Percentage Comparisons
        Covers Q2, Q3, Q4, Q5, Q6, Q9, Q12, Q13, Q16 style questions.
        Uses Python for math, varied wording for context.
        """
        sub = random.choice([
            'nested_variable_chain',  # Q6, Q13 A>B>C>D style
            'sum_relativity',         # Q2 C is X% less than sum(A+B), A is Y% more than B
            'basic_diff_equation',    # Q4, Q12  X% less than Y% by Z
            'ratio_equalization',     # Q5 ratios / volumes
            'weight_fraction',        # Q9 sum of weights, X% of A = Y*B
            'multi_person_donations', # Q3 salary same, different donation%, find C's salary
            'fractional_population',  # Q16 4/9 males, 50% married, etc.
        ])

        def make_options(correct_val, step=None):
            opts = [str(correct_val)]
            step = step or max(5, abs(correct_val) // 5)
            while len(opts) < 4:
                alt = correct_val + random.choice([-3,-2,-1,1,2,3]) * step
                s = str(alt)
                if s not in opts: opts.append(s)
            random.shuffle(opts)
            return opts, opts.index(str(correct_val))

        if sub == 'nested_variable_chain':
            # A is P% more than B, B is Q% more than C, C is R% less than D
            # Given A - C = Z, find B
            templates = [
                ("A obtained {p}% more marks than B, B obtained {q}% more marks than C, C obtained {r}% less marks than D. If A obtained {diff} more marks than C, how much did B score?", "marks"),
                ("Store A's sales are {p}% higher than store B's. Store B's sales are {q}% higher than store C's. Store C's sales are {r}% less than store D's. If A sells {diff} more units than C, find B's sales.", "units"),
                ("Ravi earns {p}% more than Suresh. Suresh earns {q}% more than Mohan. Mohan earns {r}% less than Kiran. If Ravi earns Rs.{diff} more than Mohan, find Suresh's salary.", "Rs."),
            ]
            # pick clean numbers
            # let C = base, B = C*(1+q/100), A = B*(1+p/100)
            C = random.randint(4, 20) * 100
            q = random.choice([10, 20, 25, 50])
            p = random.choice([10, 20, 25, 50])
            B = int(C * (1 + q/100))
            A = int(B * (1 + p/100))
            diff = A - C
            r = random.choice([10, 20, 25])
            tmpl, unit = random.choice(templates)
            question = tmpl.format(p=p, q=q, r=r, diff=diff)
            correct = B
            explanation = (f"Let C = {C}.\nB = C × (1 + {q}/100) = {C} × {1+q/100} = {B}.\n"
                           f"A = B × (1 + {p}/100) = {B} × {1+p/100} = {A}.\n"
                           f"A - C = {A} - {C} = {diff}. ✓\nSo B = {B} {unit}.")

        elif sub == 'sum_relativity':
            # A is P% more than B; C is Q% less than (A+B). How much % is C less than A?
            templates = [
                ("A is {p}% more than B, and C is {q}% less than the sum of A and B. By what percent is C less than A?", ""),
                ("Product X is {p}% more expensive than product Y. Product Z costs {q}% less than the combined price of X and Y. By what percent is Z cheaper than X?", ""),
                ("Raj's score is {p}% more than Priya's. Kiran's score is {q}% less than the total of Raj and Priya. By what percent is Kiran's score less than Raj's?", ""),
            ]
            B = 100  # normalise
            p = random.choice([80, 50, 25, 20, 10])
            A = B * (1 + p/100)
            q_choices = [round(100 * x / 14, 2) for x in [1]] + [10, 20, 25, 40, 48, 50]
            # use a clean fraction: 48(4/7)% = 340/7 % is from original question
            q_str = random.choice(['48(4/7)', '25', '20', '40', '10'])
            q_map = {'48(4/7)': 340/7, '25': 25, '20': 20, '40': 40, '10': 10}
            q_val = q_map[q_str]
            S = A + B
            C = S * (1 - q_val/100)
            pct_less_than_A = round((A - C) / A * 100, 2)
            # round to clean
            pct_less_than_A_display = round(pct_less_than_A, 2)
            tmpl, _ = random.choice(templates)
            question = tmpl.format(p=p, q=q_str)
            correct = f"{pct_less_than_A_display}%"
            explanation = (f"Let B = 100. A = B × (1+{p}/100) = {A}.\n"
                           f"Sum A+B = {S}. C = {S} × (1 - {q_val:.2f}/100) = {C:.2f}.\n"
                           f"C is less than A by: ({A} - {C:.2f})/{A} × 100 = {pct_less_than_A_display}%.")
            opts = [correct]
            alts = [f"{round(pct_less_than_A_display + d, 2)}%" for d in [-10, -5, 5, 10, 15, -15] if d != 0]
            random.shuffle(alts)
            for a in alts:
                if a not in opts: opts.append(a)
                if len(opts) == 4: break
            random.shuffle(opts)
            return {
                "question_text": question,
                "options": opts,
                "correct_option_index": opts.index(correct),
                "explanation": explanation,
                "difficulty": 5
            }

        elif sub == 'basic_diff_equation':
            # X% of N < Y% of N by Z; find W% of N
            templates = [
                ("If {y}% of a number is more than its {x}% by {z}, then {w}% of that number is:", ""),
                ("A number's {y}% exceeds its {x}% by {z}. What is {w}% of the number?", ""),
                ("{y}% of a certain number is {z} more than {x}% of the same number. Find {w}% of that number.", ""),
            ]
            x, y = sorted(random.sample([20, 30, 40, 60, 70, 80], 2))
            N = random.randint(5, 20) * 10
            z = int((y - x) * N / 100)
            w = random.choice([5, 10, 20, 25, 50])
            ans = int(w * N / 100)
            tmpl, _ = random.choice(templates)
            question = tmpl.format(x=x, y=y, z=z, w=w)
            correct = ans
            explanation = (f"({y}% - {x}%) of N = {z}.\n{y-x}% of N = {z}.\nN = {z} × 100 / {y-x} = {N}.\n{w}% of {N} = {ans}.")

        elif sub == 'ratio_equalization':
            # Tank A:B = P:Q. A increases by X%. What % must B increase so A=B?
            templates = [
                ("The volume of water in two tanks A and B is in the ratio {p}:{q}. The volume in tank A is increased by {x}%. By what percent must the volume in tank B be increased so that both tanks become equal?", ""),
                ("Two factories A and B produce in ratio {p}:{q}. Factory A increases output by {x}%. By what percent should factory B increase to match A?", ""),
                ("Two cities have population in ratio {p}:{q}. City A's population rises by {x}%. What percentage increase does city B need to have the same population as city A?", ""),
            ]
            p, q = random.choice([(6,5),(4,3),(3,2),(5,4),(7,5)])
            x = random.choice([20, 25, 30, 40, 50])
            # A_new = p*(1+x/100), need B_new = A_new, so %inc = (A_new - q)/q * 100
            A_new = p * (1 + x/100)
            pct_B = round((A_new - q) / q * 100, 2)
            tmpl, _ = random.choice(templates)
            question = tmpl.format(p=p, q=q, x=x)
            correct = f"{pct_B}%"
            explanation = (f"A_new = {p} × (1 + {x}/100) = {A_new}.\n"
                           f"We need B_new = {A_new}. B original = {q}.\n"
                           f"% increase in B = ({A_new} - {q})/{q} × 100 = {pct_B}%.")
            opts = [correct]
            alts = [f"{round(pct_B + d, 2)}%" for d in [-10,-5,5,10,15,-15]]
            random.shuffle(alts)
            for a in alts:
                if a not in opts: opts.append(a)
                if len(opts) == 4: break
            random.shuffle(opts)
            return {
                "question_text": question, "options": opts,
                "correct_option_index": opts.index(correct),
                "explanation": explanation, "difficulty": 4
            }

        elif sub == 'weight_fraction':
            # Sum of A+B = S. P% of A = (m/n) * B. Find diff.
            templates = [
                ("The sum of weights of A and B is {s} kg. {p}% of A's weight is {frac} times the weight of B. Find the difference between their weights.", "kg"),
                ("The combined salary of X and Y is Rs.{s}. {p}% of X's salary equals {frac} of Y's salary. What is the difference in their salaries?", "Rs."),
                ("The total score of P and Q in an exam is {s}. {p}% of P's score is {frac} of Q's score. Find the difference in their scores.", "marks"),
            ]
            # pick m/n from benchmarks
            num, den = random.choice([(5,6),(2,3),(3,4),(4,5),(1,2),(5,8)])
            frac_str = f"{num}/{den}"
            # p% of A = (num/den) * B:  (p/100)*A = (num/den)*B => A/B = 100*num/(den*p)
            p = random.choice([25, 50, 40, 60, 75, 20])
            # ratio A/B = (100*num)/(den*p)
            A_part = 100 * num
            B_part = den * p
            from math import gcd
            g = gcd(A_part, B_part)
            Ar, Br = A_part // g, B_part // g
            total_parts = Ar + Br
            S = random.randint(3, 10) * total_parts
            A = S * Ar // total_parts
            B = S * Br // total_parts
            diff = abs(A - B)
            tmpl, unit = random.choice(templates)
            question = tmpl.format(s=S, p=p, frac=frac_str)
            correct = diff
            explanation = (f"{p}% of A = {frac_str} × B => A/B = (100×{num})/(100×{den}×{p}/100) = wait:\n"
                           f"(p/100)·A = ({num}/{den})·B => A/B = {num}×100/({den}×{p}) = {Ar}/{Br}.\n"
                           f"A = {S}×{Ar}/{total_parts} = {A}. B = {S}×{Br}/{total_parts} = {B}.\n"
                           f"Difference = |{A}-{B}| = {diff} {unit}.")

        elif sub == 'multi_person_donations':
            # A and B same salary S. A donates a%, B donates b%, C donates c%.
            # |donation_A - donation_B| = D1. TotalDon_A+B - Don_C = D2. Find C's salary.
            templates = [
                ("The monthly salaries of A and B are equal. A donates {a}%, B donates {b}%, and C donates {c}% of their salaries to charity. The difference between A's and B's donations is Rs.{d1}. The total donation by A and B is Rs.{d2} more than C's donation. What is C's monthly salary?", "Rs."),
                ("Workers P and Q earn the same monthly wage. P contributes {a}%, Q contributes {b}%, and R contributes {c}% to a welfare fund. |P's - Q's contribution| = Rs.{d1}. P+Q's total contribution exceeds R's by Rs.{d2}. Find R's salary.", "Rs."),
            ]
            a, b = sorted(random.sample([8, 9, 10, 12, 15, 6], 2), reverse=True)
            c = random.choice([7, 8, 9, 10, 12, 14])
            S_AB = random.randint(5, 20) * 1000   # same salary for A,B
            d1 = abs(a - b) * S_AB // 100
            don_A = a * S_AB // 100
            don_B = b * S_AB // 100
            total_AB = don_A + don_B
            d2 = random.randint(1, 5) * 100
            don_C = total_AB - d2
            S_C = don_C * 100 // c
            # round to nearest hundred for clean answer
            S_C = (S_C // 100) * 100
            don_C_actual = c * S_C // 100
            d2_actual = total_AB - don_C_actual
            tmpl, unit = random.choice(templates)
            question = tmpl.format(a=a, b=b, c=c, d1=d1, d2=d2_actual)
            correct = S_C
            explanation = (f"Since A and B have same salary S.\n"
                           f"({a}% - {b}%) of S = {d1} => {a-b}% of S = {d1} => S = {S_AB}.\n"
                           f"A donates {don_A}, B donates {don_B}. Total A+B = {total_AB}.\n"
                           f"Total A+B - C's donation = {d2_actual} => C's donation = {don_C_actual}.\n"
                           f"C salary = {don_C_actual} × 100 / {c} = {S_C}.")

        elif sub == 'fractional_population':
            # Total = T. M/N are men, rest women. P% men are married. Q% women are married.
            # Find % married population OR % married women
            templates_dbl = [
                ("The population of a town is {t}. {num}/{den} of them are males and the rest are females. {p}% of the males are married. Find (i) the percentage of married population, and (ii) the percentage of married females if the total married population is {mp}.", ""),
                ("A school has {t} students. {num}/{den} are boys and the rest are girls. {p}% of the boys are prefects. If total prefects are {mp}, find the percent of prefects among all students and percent of girl prefects.", ""),
            ]
            den = random.choice([3, 4, 5, 7, 9])
            num = random.randint(1, den-1)
            T = random.randint(10, 40) * den * 1000 // 1000 * 1000  # multiple of den*1000
            while T % den != 0: T += 1
            males = T * num // den
            females = T - males
            p = random.choice([40, 50, 60, 75, 80, 25])
            married_males = males * p // 100
            q = random.choice([20, 30, 40, 50, 60])  # % married females
            married_females = females * q // 100
            total_married = married_males + married_females
            pct_married_total = round(total_married / T * 100, 2)
            pct_married_female = round(married_females / females * 100, 2)
            question = (f"The population of a town is {T}. {num}/{den} of them are males and the rest are females. "
                        f"{p}% of males are married and {q}% of females are married. Find: "
                        f"(i) % of the total population that is married, and (ii) % of married females out of all females.")
            correct = f"{pct_married_total}% total married; {pct_married_female}% females married"
            explanation = (f"Males = {T}×{num}/{den} = {males}. Females = {T}-{males} = {females}.\n"
                           f"Married males = {p}% of {males} = {married_males}.\n"
                           f"Married females = {q}% of {females} = {married_females}.\n"
                           f"Total married = {total_married}. % of total = {total_married}/{T}×100 = {pct_married_total}%.\n"
                           f"% of females married = {married_females}/{females}×100 = {pct_married_female}%.")
            opts = [correct]
            alts_total = [round(pct_married_total + d, 2) for d in [-10,-5,5,10]]
            alts_fem   = [round(pct_married_female + d, 2) for d in [-10,-5,5,10]]
            for dt, df in zip(alts_total, alts_fem):
                alt = f"{dt}% total married; {df}% females married"
                if alt not in opts: opts.append(alt)
                if len(opts) == 4: break
            random.shuffle(opts)
            return {
                "question_text": question, "options": opts,
                "correct_option_index": opts.index(correct),
                "explanation": explanation, "difficulty": 5
            }

        # Build options for integer answers
        opts, idx = make_options(correct)
        return {
            "question_text": question,
            "options": opts,
            "correct_option_index": idx,
            "explanation": explanation,
            "difficulty": 4
        }

    def generate_percentage_calculations(self):
        """Phase 20 Cat 2: Percentage Calculations
        Covers Q1, Q7, Q8, Q10, Q11, Q14, Q15, Q17 style questions.
        Uses Python math for exact calculations.
        """
        sub = random.choice([
            'product_constancy',      # Q7, Q15 rate/hours, price/consumption
            'work_productivity',      # Q8 work increase + productivity increase
            'geometry_scaling',       # Q17 cube/square/circle edge % increase => area/volume
            'error_multiplier',       # Q14 multiply by wrong fraction
            'salary_remainder',       # Q11 spend X% on A, Y% on B, borrows Z, find salary
            'property_value_chain',   # Q1 owns X% of property, Y% of that = Z, find W% total
            'spoiled_fruit_subsets',  # Q10 1 per N, X% sold, total sold = Z, find total
        ])

        def make_options(correct_val, step=None):
            opts = [str(correct_val)]
            step = step or max(5, abs(correct_val) // 5)
            while len(opts) < 4:
                alt = correct_val + random.choice([-3,-2,-1,1,2,3]) * step
                if alt > 0:
                    s = str(alt)
                    if s not in opts: opts.append(s)
            random.shuffle(opts)
            return opts, opts.index(str(correct_val))

        if sub == 'product_constancy':
            # Factor A increases by X%, Factor B changes by Y%. Net change = ?
            # contexts: wages/hours, price/consumption, speed/time
            contexts = [
                ("A labour works {h} hr/week and earns Rs.{w} as wages. His hourly rate is increased by {x}% and his work duration is reduced by {y}%. Find the percentage change in his income.",
                 "wages", "hours"),
                ("The price of a commodity is increased by {x}%. A family reduces its consumption by {y}%. Find the percentage change in their expenditure.",
                 "price", "consumption"),
                ("A car's speed is increased by {x}%. The driver reduces travel time by {y}%. By what percent does total distance change?",
                 "speed", "time"),
                ("A factory worker's rate per unit is hiked by {x}%. The worker reduces output by {y}%. Find the net % change in earnings.",
                 "rate", "output"),
            ]
            x = random.choice([20, 25, 30, 40, 50])
            # y is such that reduction = 1/(n+1) style
            y_choices = {
                'clean': [10, 20, 25, 50],
                'fraction': [16, 11, 33]
            }
            y_frac_str_map = {
                16: '16(2/3)', 11: '11(1/9)', 33: '33(1/3)'
            }
            y = random.choice([10, 20, 25])
            # Net change = (1 + x/100)(1 - y/100) - 1
            net = round(((1 + x/100) * (1 - y/100) - 1) * 100, 2)
            direction = "increase" if net > 0 else "decrease"
            abs_net = abs(net)
            tmpl, f1, f2 = random.choice(contexts)
            h = random.choice([40, 48, 50, 60])
            rate = random.randint(25, 80)
            w = h * rate
            question = tmpl.format(h=h, w=w, x=x, y=y)
            correct = f"{abs_net}% {direction}"
            explanation = (f"Let original {f1} = 1, {f2} = 1. Original value = 1.\n"
                           f"New {f1} = 1 + {x}/100 = {1+x/100:.3f}.\n"
                           f"New {f2} = 1 - {y}/100 = {1-y/100:.3f}.\n"
                           f"New value = {(1+x/100)*(1-y/100):.4f}.\n"
                           f"Change = {net:.2f}% => {abs_net}% {direction}.")
            opts = [correct]
            alts = [f"{round(abs_net+d,2)}% {direction}" for d in [-5,-2,3,8] if round(abs_net+d,2)!=abs_net]
            for a in alts:
                if a not in opts: opts.append(a)
                if len(opts) == 4: break
            opp = "decrease" if direction == "increase" else "increase"
            if len(opts) < 4: opts.append(f"{abs_net}% {opp}")
            random.shuffle(opts)
            return {
                "question_text": question, "options": opts,
                "correct_option_index": opts.index(correct),
                "explanation": explanation, "difficulty": 4
            }

        elif sub == 'work_productivity':
            templates = [
                ("The amount of work in a factory is increased by {w}%. By what percent must the number of workers be increased to complete the work in the same time, if the productivity of new workers is {p}% more than the existing workers?", ""),
                ("A company's total tasks increased by {w}%. New hires are {p}% more efficient than existing staff. By what percent must the headcount be increased to finish all tasks on time?", ""),
                ("A project's scope increased by {w}%. Newly recruited engineers are {p}% more productive. What percent increase in team size is needed to meet the same deadline?", ""),
            ]
            w = random.choice([25, 50, 60, 75, 100])
            p = random.choice([20, 25, 50])
            # Required workers_new = (1+w/100) / (1+p/100).  % increase from 1:
            new_W = (1 + w/100) / (1 + p/100)
            pct_inc = round((new_W - 1) * 100, 2)
            tmpl, _ = random.choice(templates)
            question = tmpl.format(w=w, p=p)
            correct = f"{pct_inc}%"
            explanation = (f"New work = (1+{w}/100) = {1+w/100:.3f} times.\n"
                           f"Each new worker does (1+{p}/100) = {1+p/100:.3f} times.\n"
                           f"Workers needed = {1+w/100:.3f}/{1+p/100:.3f} = {new_W:.4f}.\n"
                           f"% increase = ({new_W:.4f}-1)×100 = {pct_inc}%.")
            opts = [correct]
            alts = [f"{round(pct_inc+d,2)}%" for d in [-10,-5,5,10,15] if d!=0]
            for a in alts:
                if a not in opts: opts.append(a)
                if len(opts) == 4: break
            random.shuffle(opts)
            return {"question_text": question, "options": opts,
                    "correct_option_index": opts.index(correct),
                    "explanation": explanation, "difficulty": 4}

        elif sub == 'geometry_scaling':
            shapes = [
                ("cube", "surface area",  lambda x: round((1+x/100)**2 * 6 - 6, 4), "6a²", "all 4 faces are squares: SA = 6a²"),
                ("square", "area",        lambda x: round((1+x/100)**2 - 1, 4)*100, "a²", "Area = a²"),
                ("circle", "area",        lambda x: round((1+x/100)**2 - 1, 4)*100, "πr²", "Area = πr²"),
                ("sphere", "surface area",lambda x: round((1+x/100)**2 - 1, 4)*100, "4πr²", "SA = 4πr²"),
                ("cube", "volume",        lambda x: round((1+x/100)**3 - 1, 4)*100, "a³", "Volume = a³"),
            ]
            shape, measure, formula, formula_str, note = random.choice(shapes)
            x = random.choice([10, 20, 25, 50])
            pct_change = round(formula(x), 2)
            templates = [
                f"If each edge of a {shape} is increased by {x}%, find the percentage increase in its {measure}.",
                f"Every dimension of a {shape} increases by {x}%. What is the % change in {measure}?",
                f"The side of a {shape} is increased by {x}%. By what % does the {measure} change?",
            ]
            question = random.choice(templates)
            correct = f"{pct_change}%"
            explanation = (f"Formula: {measure} ∝ {formula_str} ({note}).\n"
                           f"If side increases by {x}%, new {measure} = original × (1+{x}/100)² = original × {(1+x/100)**2:.4f}.\n"
                           f"% increase = ({(1+x/100)**2:.4f} - 1) × 100 = {pct_change}%.")
            opts = [correct]
            alts = [f"{round(pct_change+d,2)}%" for d in [-5,-2,3,10] if d!=0]
            for a in alts:
                if a not in opts: opts.append(a)
                if len(opts) == 4: break
            random.shuffle(opts)
            return {"question_text": question, "options": opts,
                    "correct_option_index": opts.index(correct),
                    "explanation": explanation, "difficulty": 4}

        elif sub == 'error_multiplier':
            # multiply by a/b instead of c/d, find % error
            templates = [
                ("A man multiplied a number by {a}/{b} instead of {c}/{d}. What is the percentage error in the result?", ""),
                ("Instead of multiplying by {c}/{d}, a student multiplied by {a}/{b}. Find the % error.", ""),
                ("A calculation required multiplying by {c}/{d}, but {a}/{b} was used instead. What is the % change in the result?", ""),
            ]
            # make sure a/b != c/d. Use benchmarks
            pairs = [(7,4,3,5),(3,2,4,7),(5,3,2,5),(5,4,4,5),(9,4,3,4)]
            a,b,c,d = random.choice(pairs)
            # correct result = N * c/d, actual = N * a/b
            # error % = (actual - correct)/correct * 100 = (a/b - c/d)/(c/d)*100 = (a*d - b*c)/(b*c)*100
            num = a*d - b*c
            den = b*c
            from fractions import Fraction
            frac = Fraction(num, den)
            pct = round(float(frac) * 100, 2)
            direction = "increase" if pct > 0 else "decrease"
            tmpl, _ = random.choice(templates)
            question = tmpl.format(a=a, b=b, c=c, d=d)
            correct = f"{abs(pct)}% {direction}"
            explanation = (f"Correct multiplier = {c}/{d}. Used = {a}/{b}.\n"
                           f"% change = ({a}/{b} - {c}/{d}) / ({c}/{d}) × 100\n"
                           f"= ({a*d} - {b*c}) / {b*c} × 100 = {num}/{den} × 100 = {pct}%.\n"
                           f"So the result is {abs(pct)}% {'more' if pct>0 else 'less'} than correct.")
            opts = [correct]
            alts = [f"{round(abs(pct)+d,2)}% {direction}" for d in [-10,-5,5,10] if d!=0]
            for a_ in alts:
                if a_ not in opts: opts.append(a_)
                if len(opts) == 4: break
            random.shuffle(opts)
            return {"question_text": question, "options": opts,
                    "correct_option_index": opts.index(correct),
                    "explanation": explanation, "difficulty": 4}

        elif sub == 'salary_remainder':
            # Ramesh spends a%, b%, c%, d% of salary. Borrows E to meet an expense of F. Find salary.
            spend_items = [
                ("food", "house rent", "entertainment", "conveyance"),
                ("groceries", "transport", "clothing", "utilities"),
                ("education", "medical", "travel", "dining"),
            ]
            items = random.choice(spend_items)
            a = random.choice([30, 35, 40, 45])
            b = random.choice([15, 18, 20])
            c = random.choice([10, 12, 15])
            d = random.choice([5, 6, 8])
            total_spent_pct = a + b + c + d
            saved_pct = 100 - total_spent_pct
            # Family function expense = F, borrows E
            E = random.choice([8000, 10000, 12000, 16000])
            F = E + random.choice([2000, 4000, 5000, 8000])
            # savings - available = F - E => salary * saved_pct/100 = F - E... wait
            # He borrowed E to meet TOTAL expense of F.
            # So from salary S, he spent on items: total_spent_pct% .
            # Remaining = (100-total_spent_pct)% = saved_pct%.
            # He uses ALL remaining for the function BUT still needs MORE = borrows E.
            # So: S*saved_pct/100 + E = F => S = (F-E)*100/saved_pct
            S = (F - E) * 100 // saved_pct
            templates = [
                (f"{{name}} spends {a}% of monthly salary on {items[0]}, {b}% on {items[1]}, {c}% on {items[2]}, and {d}% on {items[3]}. Due to a family function, he borrows Rs.{E} to meet an expense of Rs.{F}. What is his monthly salary?", "Rs."),
                (f"{{name}} allocates {a}% of income to {items[0]}, {b}% to {items[1]}, {c}% to {items[2]}, {d}% to {items[3]}. For a special event costing Rs.{F}, she borrows Rs.{E}. What is her monthly income?", "Rs."),
            ]
            names = ["Ramesh", "Priya", "Amit", "Neha", "Suresh"]
            name = random.choice(names)
            tmpl, unit = random.choice(templates)
            question = tmpl.format(name=name)
            correct = S
            explanation = (f"Total spent = {a}+{b}+{c}+{d} = {total_spent_pct}%.\n"
                           f"Remaining (savings) = 100-{total_spent_pct} = {saved_pct}%.\n"
                           f"He uses savings + borrows {E} to pay {F}.\n"
                           f"Savings from salary = {F} - {E} = {F-E}.\n"
                           f"{saved_pct}% of S = {F-E} => S = {F-E}×100/{saved_pct} = {S}.")

        elif sub == 'property_value_chain':
            # Anuja owns X% of property. Y% of her share = Z. Find W% of total.
            templates = [
                ("{name} owns {x}% of a property. {y}% of the property she owns is worth Rs.{z}. What is {w}% of the total value of the property?", "Rs."),
                ("A company holds {x}% of a real estate. {y}% of its share is valued at Rs.{z}. Find {w}% of the total property value.", "Rs."),
                ("{name} has {x}% stake in a business. {y}% of her stake is worth Rs.{z}. What is {w}% of the total business value?", "Rs."),
            ]
            x = random.choice([50, 60, 75, 66])  # including 66(2/3)%
            x_str = "66(2/3)" if x == 66 else str(x)
            x_val = 200/3 if x == 66 else x
            y = random.choice([20, 25, 30, 40, 50])
            w = random.choice([40, 45, 50, 60, 75])
            # y% of (x_val% of T) = Z => T = Z*100*100/(y*x_val)
            Z = random.choice([10000, 25000, 50000, 75000, 100000, 125000])
            T = Z * 100 * 100 / (y * x_val)
            ans = round(w * T / 100)
            names = ["Anuja", "Priya", "Meena", "Sunita"]
            name = random.choice(names)
            tmpl, unit = random.choice(templates)
            question = tmpl.format(name=name, x=x_str, y=y, z=Z, w=w)
            correct = ans
            explanation = (f"{name} owns {x_str}% of T = {x_val:.2f}% × T.\n"
                           f"{y}% of ({x_val:.2f}% of T) = {Z}.\n"
                           f"T = {Z}×100×100/({y}×{x_val:.2f}) = {T:.2f}.\n"
                           f"{w}% of T = {w}×{T:.2f}/100 = {ans}.")

        elif sub == 'spoiled_fruit_subsets':
            templates = [
                ("A crate of fruits contains 1 spoiled fruit for every {n} fruits. {p}% of the spoiled fruits were sold. If the seller sold {k} spoiled fruits, how many fruits were there in total?", "fruits"),
                ("A warehouse has 1 defective item for every {n} items. {p}% of defective items are shipped. If {k} defective items were shipped, how many items are in the warehouse?", "items"),
                ("In a shipment, 1 in every {n} apples is rotten. {p}% of rotten apples were dispatched. If {k} rotten apples were dispatched, find the total number of apples.", "apples"),
            ]
            n = random.choice([10, 20, 25, 50])
            p = random.choice([30, 40, 50, 60, 80])
            k = random.choice([24, 36, 48, 60, 72, 90])
            # spoiled = k / (p/100) = k*100/p
            spoiled = k * 100 // p
            total = spoiled * n
            tmpl, unit = random.choice(templates)
            question = tmpl.format(n=n, p=p, k=k)
            correct = total
            explanation = (f"1 spoiled per {n} fruits => spoiled fraction = 1/{n}.\n"
                           f"{p}% of spoiled = {k}.\n"
                           f"Total spoiled = {k}×100/{p} = {spoiled}.\n"
                           f"Total {unit} = {spoiled}×{n} = {total}.")

        # Build integer options
        def make_options_int(v, step=None):
            opts = [str(v)]
            step = step or max(100, abs(v)//5)
            while len(opts) < 4:
                alt = v + random.choice([-3,-2,-1,1,2,3]) * step
                if alt > 0:
                    s = str(alt)
                    if s not in opts: opts.append(s)
            random.shuffle(opts)
            return opts, opts.index(str(v))

        opts, idx = make_options_int(correct)
        return {
            "question_text": question,
            "options": opts,
            "correct_option_index": idx,
            "explanation": explanation,
            "difficulty": 4
        }

    def generate_income_expenditure(self):
        """Phase 21 Cat 1: Income, Expenditure, and Savings Chains
        Covers successive changes tracking back/forth via I = E + S.
        """
        sub = random.choice([
            'direct_savings_pct',         # Q1, Q2, Q3, Q10
            'net_decimal_variation',      # Q5
            'backtrack_target_amt_str',   # Q4
            'missing_savings_rate'        # Q11
        ])
        
        def make_options(correct_val, step=None):
            opts = [str(correct_val)]
            step = step or max(5, abs(correct_val) // 5)
            while len(opts) < 4:
                alt = correct_val + random.choice([-3, -2, -1, 1, 2, 3]) * step
                if alt > 0:
                    s = str(alt)
                    if s not in opts: opts.append(s)
            random.shuffle(opts)
            return opts, opts.index(str(correct_val))

        if sub == 'direct_savings_pct' or sub == 'net_decimal_variation':
            # Sub types based on Q1,2,3,5,10.
            # Base logic: I = E + S. dI, dE -> find dS
            names = ["A", "Rahul", "Priya", "Amit"]
            name = random.choice(names)
            e_pct = random.choice([60, 65, 75, 80]) # percent spent
            s_pct = 100 - e_pct                     # percent saved
            i_inc = random.choice([15, 19, 20, 25, 29, 20.1])
            e_inc = random.choice([10, 13, 15, 20, 25])
            
            # Using base Income = 1000 for standard % equations.
            I0 = 1000
            E0 = I0 * e_pct / 100
            S0 = I0 - E0
            
            I1 = I0 * (1 + i_inc / 100)
            E1 = E0 * (1 + e_inc / 100)
            S1 = I1 - E1
            
            s_change_pct = round(( (S1 - S0) / S0 ) * 100, 1)
            diff = abs(s_change_pct)
            direction = "increase" if s_change_pct > 0 else "decrease"

            # Formatting
            if sub == 'net_decimal_variation':
                question = f"{name} saves {s_pct}% of his income. If his income increases by {i_inc}% and his expenditure increases by {e_inc}%, then by what percentage do his savings restrictively {direction}? (round to 1 decimal point)"
                correct = f"{diff}% {direction}"
            else:
                question = f"{name} spends {e_pct}% of his income. His income is increased by {i_inc}% and his expenditure is increased by {e_inc}%. Find the % change in his savings."
                correct_val = int(diff) if diff.is_integer() else diff
                correct = f"{correct_val}% {direction}"

            explanation = (f"Let Income = 1000. Expenditure = {e_pct}% = {E0}. Savings = {S0}.\n"
                           f"New Income = 1000 × {1 + i_inc/100:.3f} = {I1:.1f}.\n"
                           f"New Expenditure = {E0} × {1 + e_inc/100:.3f} = {E1:.1f}.\n"
                           f"New Savings = {I1:.1f} - {E1:.1f} = {S1:.1f}.\n"
                           f"{direction.title()} in savings = ({S1:.1f} - {S0}) / {S0} × 100 = {s_change_pct}%")
                           
            opts = [correct]
            alts = [round(diff + d, 1) for d in [-5.5, -2.1, 3.0, 5.0, 8.5] if round(diff + d, 1) > 0]
            for a in alts:
                a_str = f"{int(a) if a.is_integer() else a}% {direction}"
                if a_str not in opts: opts.append(a_str)
                if len(opts) >= 4: break
            random.shuffle(opts)
            
            return {"question_text": question, "options": opts,
                    "correct_option_index": opts.index(correct),
                    "explanation": explanation, "difficulty": 4}

        elif sub == 'backtrack_target_amt_str': 
            # Q4: Expenses = I * (1 + x%). Income + A%, Expenses + B% -> Savings + Z -> Find Init Expense 
            e_base = 100
            templates = [
                "The monthly expenses of a person are {p}% OF her monthly income. If her monthly income increases by {i_inc}% and her monthly expenses increase by {e_inc}%, there is an increase of Rs. {z} in her monthly savings. What is the initial expenditure?",
            ]
            
            fraction_str = random.choice([("66(2/3)", 200/3), ("75", 75), ("80", 80), ("60", 60)])
            p_str, p_val = fraction_str
            
            i_inc = random.choice([20, 25, 40, 44, 50])
            e_inc = random.choice([30, 40, 50, 60, 80])
            
            # Use base 300 to clear 66(2/3)% cleanly
            base = 300
            # Scale
            I_b = base
            E_b = I_b * p_val / 100
            S_b = I_b - E_b
            
            I_n = I_b * (1 + i_inc/100)
            E_n = E_b * (1 + e_inc/100)
            S_n = I_n - E_n
            
            unit_change = S_n - S_b
            
            # Scale total up to target amount logically
            mult = random.choice([4, 5, 10, 20])
            Z = int(unit_change * mult)
            
            # Calculate target
            Target_Exp = int(E_b * mult)
            
            question = templates[0].format(p=p_str, i_inc=i_inc, e_inc=e_inc, z=Z)
            correct = Target_Exp
            explanation = (f"Let Income = {base} units. Expenses = {p_str}% of {base} = {E_b} units. Savings = {S_b} units.\n"
                           f"New Income = {base} × 1.{i_inc} = {I_n}. New Expenses = {E_b} × 1.{e_inc} = {E_n}.\n"
                           f"New Savings = {I_n} - {E_n} = {S_n} units.\n"
                           f"Increase in savings = {unit_change:.2f} units.\n"
                           f"Given increase = Rs. {Z}. Therefore 1 unit = {Z} / {unit_change:.2f} = {mult}.\n"
                           f"Initial expenditure = {E_b} × {mult} = Rs. {Target_Exp}.")
            
            opts, idx = make_options(correct, step=Target_Exp//4)
            return {"question_text": question, "options": opts,
                    "correct_option_index": idx,
                    "explanation": explanation, "difficulty": 5}

        elif sub == 'missing_savings_rate':
            # Q11: saves x%, income + i%, exp + e% -> savings + s%
            i_inc = random.choice([20, 26, 30])
            e_inc = random.choice([15, 20, 25])
            s_inc_target = random.choice([40, 50, 60])
            
            # Equation: 
            # I1 = I0(1 + i/100), E1 = (I0 - S0)*(1 + e/100)
            # S1 = I1 - E1
            # We want (S1 - S0)/S0 = s_target/100
            # S1 = S0 * (1 + s_target/100)
            # I0(1+i) - (I0-S0)(1+e) = S0(1+s)
            # I0(1+i) - I0(1+e) + S0(1+e) = S0(1+s)
            # I0(i - e) = S0(s - e)
            # S0/I0 = (i - e) / (s - e) => x / 100
            # Needs clean divisions:
            while True:
                num = i_inc - e_inc
                den = s_inc_target - e_inc
                if den > 0 and num > 0 and (num * 100 % den == 0):
                    x_target = (num * 100) // den
                    break
                else:
                    i_inc = random.choice([20, 26, 30, 40, 50])
                    e_inc = random.choice([10, 15, 20, 25])
                    s_inc_target = random.choice([40, 50, 60, 75])

            question = f"Rishu saves x% of her income. If her income increases by {i_inc}% and her expenditure increases by {e_inc}%, her savings increase by {s_inc_target}%. What is the value of x?"
            correct = f"{x_target}%"
            explanation = (f"Let Income = I and Savings = S. Expenditure E = I - S.\n"
                           f"S0/I0 = (Income % increase - Expense % increase) / (Savings % increase - Expense % increase)\n"
                           f"S/I = ({i_inc} - {e_inc}) / ({s_inc_target} - {e_inc}) = {num}/{den}.\n"
                           f"Value of x = ({num}/{den}) × 100 = {x_target}%.")
            
            opts = [correct]
            alts = [f"{x_target + d}%" for d in [-10, -5, 5, 10, 15] if x_target+d > 0]
            for a in alts:
                if a not in opts: opts.append(a)
                if len(opts) == 4: break
            random.shuffle(opts)
            
            return {"question_text": question, "options": opts,
                    "correct_option_index": opts.index(correct),
                    "explanation": explanation, "difficulty": 5}

    def generate_pass_fail_aggregates(self):
        """Phase 21 Cat 2: Pass/Fail and Aggregate Scaling distributions
        """
        sub = random.choice([
            'split_pass_fail_ratios',     # Q6
            'weighted_pass_fail',         # Q7, Q8
            'missing_weighted_component', # Q13
            'margin_work_scaling',        # Q9
            'absentee_splits'             # Q12
        ])
        
        def make_options(correct_val, step=None):
            opts = [str(correct_val)]
            step = step or max(5, abs(int(correct_val)) // 5)
            while len(opts) < 4:
                alt = correct_val + random.choice([-3, -2, -1, 1, 2, 3]) * step
                if alt > 0:
                    s = str(alt)
                    if s not in opts: opts.append(s)
            random.shuffle(opts)
            return opts, opts.index(str(correct_val))

        if sub == 'split_pass_fail_ratios':
            # Q6: Y has P% more students than X. X has F1% fail. Total pass is P_tot%. Find Y's fail %.
            P = random.choice([20, 50, 100, 150])
            F1 = random.choice([20, 25, 30, 40])
            
            # X passes
            P1 = 100 - F1
            
            # Build valid Y fail rate and calculate P_tot
            while True:
                F2 = random.choice([10, 15, 20, 25, 30])
                P2 = 100 - F2
                
                # Math: X students = 100, Y students = 100 * (1 + P/100)
                nx = 100
                ny = int(100 * (1 + P / 100))
                
                total_students = nx + ny
                total_pass = nx * P1 / 100 + ny * P2 / 100
                P_tot = (total_pass / total_students) * 100
                
                if P_tot.is_integer() and P_tot > 0 and P_tot < 100:
                    P_tot = int(P_tot)
                    break 

            question = f"A certain number of students from school X appeared in an examination and {F1}% of the students failed. {P}% more students than school X appeared in school Y. If {P_tot}% of the total number of students who appeared from X and Y passed, then what is the percentage of students who failed from Y?"
            correct = f"{F2}%"
            explanation = (f"Let students from X = 100. Fail = {F1}%, so Pass from X = {P1}.\n"
                           f"Students from Y = 100 + {P}% = {ny}.\n"
                           f"Total students = 100 + {ny} = {nx + ny}.\n"
                           f"Total passed = {P_tot}% of {nx + ny} = {int(total_pass)}.\n"
                           f"Pass from Y = Total pass - Pass from X = {int(total_pass)} - {P1} = {int(total_pass - P1)}.\n"
                           f"Fail from Y = Total from Y - Pass from Y = {ny} - {int(total_pass - P1)} = {int(ny - (total_pass - P1))}.\n"
                           f"Fail % from Y = ({int(ny - (total_pass - P1))} / {ny}) * 100 = {F2}%.")
            
            opts = [correct]
            alts = [f"{F2 + d}%" for d in [-10, -5, 5, 8, 10, 15] if F2+d > 0]
            for a in alts:
                if a not in opts: opts.append(a)
                if len(opts) == 4: break
            random.shuffle(opts)
            
            return {"question_text": question, "options": opts,
                    "correct_option_index": opts.index(correct),
                    "explanation": explanation, "difficulty": 5}

        elif sub == 'weighted_pass_fail':
            # Q7/8: Weighted average pass rates. 
            # Sub-variation: raw numbers vs maximum marks.
            v = random.choice([1, 2])
            if v == 1:
                # Q7 style (raw numbers)
                n1 = random.choice([40, 60, 80, 100])
                n2 = random.choice([40, 60, 80, 120])
                p1 = random.choice([50, 60, 75, 80])
                p2 = random.choice([50, 60, 75, 80])
                
                tot_passed = (n1 * p1 / 100) + (n2 * p2 / 100)
                tot_students = n1 + n2
                avg_rate = (tot_passed / tot_students) * 100
                
                question = f"In two successive years, {n1} and {n2} students of a school appeared at the final examination, of which {p1}% and {p2}% passed respectively. The average rate of students passed is:"
                correct = f"{round(avg_rate, 2)}%"
                explanation = (f"Total students = {n1} + {n2} = {tot_students}.\n"
                               f"Total passed = ({p1}% of {n1}) + ({p2}% of {n2}) = {int(n1 * p1 / 100)} + {int(n2 * p2 / 100)} = {int(tot_passed)}.\n"
                               f"Average pass rate = ({int(tot_passed)} / {tot_students}) * 100 = {round(avg_rate, 2)}%.")
                diff = round(avg_rate, 2)
                
            else:
                # Q8 style (max marks)
                n1 = random.choice([500, 600, 800, 900])
                n2 = random.choice([400, 600, 700])
                p1 = random.choice([60, 70, 72, 80])
                p2 = random.choice([70, 80, 85, 90])
                
                tot_scored = (n1 * p1 / 100) + (n2 * p2 / 100)
                tot_max = n1 + n2
                avg_rate = (tot_scored / tot_max) * 100
                
                question = f"A scored {p1}% in a paper with maximum marks of {n1} and {p2}% in another paper with maximum marks of {n2}. If the result is based on the combined percentage of the two papers, the combined percentage is:"
                correct = f"{round(avg_rate, 2)}%"
                explanation = (f"Marks obtained = ({p1}% of {n1}) + ({p2}% of {n2}) = {int(n1 * p1 / 100)} + {int(n2 * p2 / 100)} = {int(tot_scored)}.\n"
                               f"Total maximum marks = {n1} + {n2} = {tot_max}.\n"
                               f"Combined percentage = ({int(tot_scored)} / {tot_max}) * 100 = {round(avg_rate, 2)}%.")
                diff = round(avg_rate, 2)

            opts = [correct]
            alts = [round(diff + d, 2) for d in [-3.5, -2.0, 1.5, 3.0, 5.0]]
            for a in alts:
                a_str = f"{a}%"
                if a_str not in opts: opts.append(a_str)
                if len(opts) >= 4: break
            random.shuffle(opts)
            
            return {"question_text": question, "options": opts,
                    "correct_option_index": opts.index(correct),
                    "explanation": explanation, "difficulty": 4}

        elif sub == 'missing_weighted_component':
            # Q13: A student scored P1% in S1 out of M1. Needs P_tot% overall of M_tot. Find P2%.
            M1 = random.choice([200, 300, 400])
            M2 = random.choice([100, 200, 300])
            M_tot = M1 + M2
            
            P1 = random.choice([32, 40, 50, 60])
            P_tot = random.choice([46, 55, 65, 75])
            
            marks1 = (P1 * M1) / 100
            marks_target = (P_tot * M_tot) / 100
            
            marks2_needed = marks_target - marks1
            P2_req = (marks2_needed / M2) * 100
            
            question = f"A student scored {P1}% marks in science subjects out of {M1}. How much percentage should he score in language papers out of {M2} if he is to get an overall {P_tot}% marks?"
            correct = f"{round(P2_req, 1)}%"
            explanation = (f"Marks in Science = {P1}% of {M1} = {int(marks1)}.\n"
                           f"Target marks overall = {P_tot}% of {M_tot} = {int(marks_target)}.\n"
                           f"Marks needed in Language = {int(marks_target)} - {int(marks1)} = {int(marks2_needed)}.\n"
                           f"Required % = ({int(marks2_needed)} / {M2}) * 100 = {round(P2_req, 1)}%.")

            opts = [correct]
            alts = [round(P2_req + d, 1) for d in [-10, -5, 5, 10, 15] if P2_req+d > 0]
            for a in alts:
                a_str = f"{a}%"
                if a_str not in opts: opts.append(a_str)
                if len(opts) >= 4: break
            random.shuffle(opts)
            
            return {"question_text": question, "options": opts,
                    "correct_option_index": opts.index(correct),
                    "explanation": explanation, "difficulty": 4}

        elif sub == 'margin_work_scaling':
            # Q9: T1 mins for L1 lines, M1% margin. Time T2 for N pages of L2 lines, M2% = M1*(1+X%).
            # Actually, "25% MORE margin of before" means M2 = M1 * 1.25. (e.g. 8% * 1.25 = 10%)
            M1 = random.choice([8, 10, 12, 16])
            margin_increase = random.choice([20, 25, 50])
            M2 = int(M1 * (1 + margin_increase / 100))
            
            T1 = random.choice([10, 15, 20])
            L1 = random.choice([20, 30, 40])
            
            Pages = random.choice([23, 30, 40])
            L2_per_page = random.choice([40, 50, 60])
            L2_total = Pages * L2_per_page
            
            # Rate of typing raw text: Raw = L1 * (100 - M1) / 100 in T1 mins.
            raw_text_1 = L1 * (100 - M1)
            raw_rate = raw_text_1 / T1 
            
            # Needed raw text to type: Raw_2 = L2_total * (100 - M2)
            raw_text_2 = L2_total * (100 - M2)
            T2 = raw_text_2 / raw_rate
            
            question = f"A man can type {L1} lines in {T1} minutes, but he leaves an {M1}% margin on each line. In how much time will he type {Pages} pages, each containing {L2_per_page} lines, on which he leaves {margin_increase}% more margin than before?"
            correct = f"{round(T2)} minutes"
            explanation = (f"Actual text per line typed initially = {(100 - M1)}% of a full line.\n"
                           f"Work rate = {L1} × {(100 - M1)} / {T1} = {raw_rate} units/min.\n"
                           f"New margin = {M1} + ({margin_increase}% of {M1}) = {M2}%.\n"
                           f"Actual text per new line = {(100 - M2)}% of a full line.\n"
                           f"Total lines = {Pages} × {L2_per_page} = {L2_total} lines.\n"
                           f"Total work needed = {L2_total} × {(100 - M2)} = {raw_text_2} units.\n"
                           f"Time = {raw_text_2} / {raw_rate} = {round(T2)} minutes.")
                           
            opts = [correct]
            alts = [round(T2 + d) for d in [-30, -10, 10, 20, 30]]
            for a in alts:
                a_str = f"{a} minutes"
                if a_str not in opts: opts.append(a_str)
                if len(opts) >= 4: break
            random.shuffle(opts)
            
            return {"question_text": question, "options": opts,
                    "correct_option_index": opts.index(correct),
                    "explanation": explanation, "difficulty": 5}

        elif sub == 'absentee_splits':
            # Q12: 88(1/3)% of students are girls & rest boys. 60% boys & 80% girls present. Find % absent overall.
            frac_str = random.choice([("83(1/3)", 250/3), ("66(2/3)", 200/3), ("75", 75), ("80", 80), ("87.5", 87.5)])
            p_str, p_val = frac_str
            
            boys_val = 100 - p_val
            
            b_present = random.choice([60, 70, 75, 80])
            g_present = random.choice([70, 75, 80, 90])
            
            absent_pct = (boys_val * (100 - b_present) / 100) + (p_val * (100 - g_present) / 100)
            
            question = f"In a class, {p_str}% of the number of students are girls and the rest are boys. If {b_present}% of the number of boys and {g_present}% of the girls are present, then what percentage of the total number of students in the class is absent?"
            correct = f"{round(absent_pct, 2)}%"
            
            explanation = (f"Let total students = 100.\n"
                           f"Girls = {p_str}% of 100 = {round(p_val, 2)}. Boys = 100 - {round(p_val, 2)} = {round(boys_val, 2)}.\n"
                           f"Absent boys = (100 - {b_present})% of {round(boys_val, 2)} = {round(boys_val * (100 - b_present)/100, 2)}.\n"
                           f"Absent girls = (100 - {g_present})% of {round(p_val, 2)} = {round(p_val * (100 - g_present)/100, 2)}.\n"
                           f"Total absent = {round(boys_val * (100 - b_present)/100, 2)} + {round(p_val * (100 - g_present)/100, 2)} = {round(absent_pct, 2)}%.")
            
            opts = [correct]
            alts = [round(absent_pct + d, 2) for d in [-5.5, -2.0, 2.0, 5.0, 10.0] if absent_pct+d > 0]
            for a in alts:
                a_str = f"{a}%"
                if a_str not in opts: opts.append(a_str)
                if len(opts) >= 4: break
            random.shuffle(opts)
            
            return {"question_text": question, "options": opts,
                    "correct_option_index": opts.index(correct),
                    "explanation": explanation, "difficulty": 4}

hybrid_generator = HybridGenerator()
