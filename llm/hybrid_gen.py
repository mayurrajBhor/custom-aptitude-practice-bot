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

    def _options(self, correct, distractors):
        correct = str(correct)
        options = [correct]
        for value in distractors:
            option = str(value)
            if option != correct and option not in options:
                options.append(option)
            if len(options) == 4:
                break

        delta = 1
        while len(options) < 4:
            try:
                option = str(int(float(correct)) + delta)
            except ValueError:
                option = f"{correct} + {delta}"
            if option not in options:
                options.append(option)
            delta += 1

        random.shuffle(options)
        return options, options.index(correct)

    def _mcq(self, question, correct, explanation, difficulty=2, distractors=None):
        options, index = self._options(correct, distractors or [])
        return {
            "question_text": question,
            "options": options,
            "correct_option_index": index,
            "explanation": explanation,
            "difficulty": difficulty,
        }

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
        for delta in [-2, -1, 1, 2, 3, 4]:
            w = max(1, whole + delta)
            r = rem
            opt = f"{w}({r}/{denom})"
            if opt not in options:
                options.append(opt)
            if len(options) == 4:
                break

        next_whole = whole + 5
        while len(options) < 4:
            opt = f"{next_whole}({rem}/{denom})"
            if opt not in options:
                options.append(opt)
            next_whole += 1
        
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

    def generate_base_comparisons(self):
        """Phase 18 Category 2: Base Comparisons & Successive Chains"""
        sub_type = random.choice([
            'direct_of',      # Q18: X is what % of Y
            'direct_less',    # Q19/Q28: X is what % less than Y
            'missing_add',    # Q11: what to add to X to equal Y
            'missing_num',    # Q24: P% of which number = Q% of Z
            'chain',          # Q14: chain multiplication a% of b% of c/d of N
            'successive',     # Q25: x is P% more than y, y is Q% more than Z
            'var_chain',      # Q13: b = A% of N, find Q% of b
        ])
        
        if sub_type == 'direct_of':
            # Q18: X is what percent of Y?
            p = random.choice([5, 10, 15, 20, 25, 30, 40, 50, 60, 75, 80])
            Y = random.randint(10, 100) * 10
            X = (p * Y) // 100
            if random.random() > 0.5:
                X, Y = X / 10, Y / 10
            templates = [
                f"{X} is what percent of {Y}?",
                f"What percentage of {Y} is {X}?",
                f"Express {X} as a percentage of {Y}.",
            ]
            question = random.choice(templates)
            correct = f"{p}%"
            explanation = f"Percent = (Part / Whole) * 100\n= ({X} / {Y}) * 100 = {p}%."

        elif sub_type == 'direct_less':
            # Q19/Q28: X is what % less/more than Y?
            p = random.choice([10, 20, 25, 30, 40, 50, 60, 75, 80])
            Y = random.randint(10, 100) * 10
            direction = random.choice(['less', 'more'])
            if direction == 'less':
                X = Y - (p * Y) // 100
                templates = [
                    f"{X} is what percent less than {Y}?",
                    f"By what percent is {X} less than {Y}?",
                    f"{X} is less than {Y} by what percentage?",
                ]
                explanation = f"Percent less = (Difference / Original) * 100\nDifference = {Y} - {X} = {Y-X}.\n({Y-X} / {Y}) * 100 = {p}%."
            else:
                X = Y + (p * Y) // 100
                templates = [
                    f"{X} is what percent more than {Y}?",
                    f"By what percent is {X} more than {Y}?",
                ]
                explanation = f"Percent more = (Difference / Base) * 100\nDifference = {X} - {Y} = {X-Y}.\n({X-Y} / {Y}) * 100 = {p}%."
            if random.random() > 0.5:
                X, Y = X / 10, Y / 10
            question = random.choice(templates)
            correct = f"{p}%"

        elif sub_type == 'missing_add':
            # Q11: What must be added to P% of X so sum equals Q% of Y?
            p1 = random.choice([10, 15, 20, 25, 30])
            X1 = random.randint(10, 50) * 10
            p2 = random.choice([15, 20, 25, 30, 40, 50])
            X2 = random.randint(20, 60) * 10
            val1 = (p1 * X1) // 100
            val2 = (p2 * X2) // 100
            if val1 >= val2: val2 = val1 + random.randint(10, 50)
            ans = val2 - val1
            templates = [
                f"What must be added to {p1}% of {X1} so that the sum is equal to {p2}% of {X2}?",
                f"Find what should be added to {p1}% of {X1} to make it equal to {p2}% of {X2}.",
                f"How much should be added to {p1}% of {X1} to bring it to the level of {p2}% of {X2}?",
            ]
            question = random.choice(templates)
            correct = str(ans)
            explanation = f"Calculate both parts:\n{p1}% of {X1} = {val1}\n{p2}% of {X2} = {val2}\nDifference = {val2} - {val1} = {ans}. You must add {ans}."

        elif sub_type == 'missing_num':
            # Q24: P% of which number equals Q% of Z?
            p1 = random.choice([12, 15, 18, 20, 24, 25])
            p2 = random.choice([10, 12, 16, 20, 25, 30])
            num2 = random.randint(20, 100) * 5
            num2 = (num2 // p1) * p1
            if num2 == 0: num2 = p1 * 5
            ans = (p2 * num2) // p1
            templates = [
                f"{p1}% of which number is equal to {p2}% of {num2}?",
                f"Find a number such that {p1}% of it equals {p2}% of {num2}.",
                f"What number, when {p1}% is taken, gives the same result as {p2}% of {num2}?",
            ]
            question = random.choice(templates)
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
            correct = str(int(val_x)) if float(val_x).is_integer() else str(round(val_x, 2))
            explanation = f"Step 1: Find y. y is {p2}% {t2} than {Z}.\ny = {Z} * {m2} = {val_y}\nStep 2: Find x. x is {p1}% {t1} than y.\nx = {val_y} * {m1} = {correct}."
            
        else: # var_chain
            A_val = random.choice([5, 10, 20, 25, 40, 50])
            val1 = random.choice([5, 10, 20, 40, 50, 100])
            val2 = random.choice([10, 20, 25, 40, 50])
            ans = (val2 * val1) / 100
            
            question = f"If b = A% of {val1}, then {val2}% of 'b' is the same as:"
            correct = f"{int(ans)}% of A" if float(ans).is_integer() else f"{round(ans, 2)}% of A"
            explanation = f"b = (A / 100) * {val1}\n{val2}% of b = ({val2} / 100) * b\nSubstitute b: ({val2} / 100) * (A / 100) * {val1}\nRearranging: A * ({val2} * {val1} / 10000)\n= ({ans} / 100) * A\n= {correct}."

        options = [correct]
        while len(options) < 4:
            if "% of A" in correct:
                val = float(correct.split("%")[0])
                alt_val = val * random.choice([0.5, 2, 10, 0.1, 5])
                alt = f"{int(alt_val)}% of A" if float(alt_val).is_integer() else f"{round(alt_val, 2)}% of A"
                if alt not in options and alt_val > 0: options.append(alt)
            elif "%" in correct:
                val = float(correct.replace("%", ""))
                alt_val = val + random.choice([-10, -5, 5, 10, 20])
                alt = f"{int(alt_val)}%" if float(alt_val).is_integer() else f"{round(alt_val, 2)}%"
                if alt not in options and alt_val > 0: options.append(alt)
            else:
                val = float(correct)
                alt_val = val + random.choice([-20, -10, 10, 20, -val*0.1, val*0.1])
                alt_val = max(1, alt_val)
                alt = str(int(alt_val)) if float(alt_val).is_integer() else str(round(alt_val, 2))
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
        sub_type = random.choice([
            'fraction_shift',       # Q30: numerator/denominator each % increased, find original
            'weighted_avg',         # Q31: two equal groups, find needed % on second half
            'population_split',     # Q32: P% boys, girls count given, find boys count
            'calc_trick_symmetric', # Q16: a% of b + b% of a = 2*(a% of b), find missing
            'calc_trick_find_val',  # Q17: same trick but asked as direct calculation
            'calc_trick_sub',       # Extra: precise decimal subtraction
        ])
        
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
            
        elif sub_type == 'calc_trick_symmetric':
            # Q16: a% of (b*10) + b% of (a*10) = 2 * (a% of b*10). Find missing value.
            A = random.choice([45.5, 62.5, 78.5, 82.5, 94.5])
            B = random.choice([36, 42, 64, 84])
            term1 = (A * B * 10) / 100
            term2 = (B * A * 10) / 100
            total_sum = term1 + term2
            target_diff = random.randint(10, 50) * 10
            rhs = total_sum - target_diff
            templates = [
                f"Calculate the missing value (?): {A}% of {B*10} + {B}% of {int(A*10)} - ? = {int(rhs)}",
                f"Find the unknown (?) in: {A}% of {int(B*10)} + {B}% of {int(A*10)} = {int(rhs)} + ?",
                f"What is the value of ?: {A}% of {B*10} + {B}% of {int(A*10)} - {int(rhs)} = ?",
            ]
            question = random.choice(templates)
            correct = str(int(target_diff))
            explanation = (
                f"Notice the trick: {B}% of {int(A*10)} = {A}% of {int(B*10)} (swap property).\n"
                f"So the expression = 2 × ({A}% of {int(B*10)}) = 2 × {term1} = {total_sum}.\n"
                f"{total_sum} - ? = {int(rhs)} => ? = {int(target_diff)}."
            )

        elif sub_type == 'calc_trick_find_val':
            # Q17: Direct calculation using symmetry. a% of X + X% of a = 2*(a% of X). 
            # Ask for the direct total.
            a = random.choice([25, 30, 40, 45, 50, 60])
            X = random.choice([80, 120, 150, 200, 240, 300])
            ans = 2 * (a * X / 100)
            templates = [
                f"Calculate: {a}% of {X} + {X}% of {a}",
                f"Find the value of ({a}% of {X}) + ({X}% of {a}).",
                f"What is the sum of {a}% of {X} and {X}% of {a}?",
            ]
            question = random.choice(templates)
            correct = str(int(ans)) if ans == int(ans) else str(round(ans, 2))
            explanation = (
                f"Using the property: a% of b = b% of a.\n"
                f"So {X}% of {a} = {a}% of {X} = {a * X / 100}.\n"
                f"Sum = {a}% of {X} + {a}% of {X} = 2 × {a * X / 100} = {ans}."
            )

        else:  # calc_trick_sub
            a = random.choice([6.4, 4.5, 8.2, 5.5])
            b = random.randint(100, 1500)
            c = random.choice([3.5, 2.5, 4.2, 1.5])
            d = random.randint(100, 500)
            t1 = (a * b) / 100
            t2 = (c * d) / 100
            ans = round(t1 - t2, 4)
            templates = [
                f"Find the exact value of ({a}% of {b}) - ({c}% of {d}):",
                f"Calculate: {a}% of {b} minus {c}% of {d}.",
                f"What is ({a}% of {b}) − ({c}% of {d})?",
            ]
            question = random.choice(templates)
            correct = f"{int(ans)}" if float(ans).is_integer() else f"{round(ans, 4)}"
            explanation = (
                f"Calculate each term:\n{a}% of {b} = {a/100} × {b} = {t1}\n"
                f"{c}% of {d} = {c/100} × {d} = {t2}\nDifference = {t1} - {t2} = {correct}."
            )

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
                alt = f"{int(alt_val)}%" if float(alt_val).is_integer() else f"{round(alt_val, 2)}%"
                if alt not in options and alt_val > 0: options.append(alt)
            else:
                val = float(correct)
                alt_val = val + random.choice([-20, -10, 10, 20, -min(10, val*0.1), min(10, val*0.1), 1, -1])
                alt_val = max(0, alt_val)
                alt = str(int(alt_val)) if float(alt_val).is_integer() else str(round(alt_val, 4))
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
            'direct_savings_pct',           # Q1: spends X%, income +A%, exp +B% -> savings change
            'net_decimal_variation',        # Q2: saves X%, income +A%, exp +B% -> savings change (decimal)
            'backtrack_target_amt_str',     # Q3: savings increase by Rs.Z, find initial expenditure
            'missing_savings_rate',         # Q4: saves x%, i+A%, e+B%, s+C% -> find x
            'fixed_savings_find_income',    # Q5: spends fixed Rs.X, saves Rs.Y, income + P% -> new savings
            'compare_two_persons',          # Q6: A earns more than B by P%, A spends more than B by Q% -> compare savings
            'exp_as_pct_of_savings',        # Q7: income + A%, exp unchanged -> expenditure is now X% of savings
            'savings_absolute_change',      # Q8: income + A%, exp + B%, savings change by Rs.Z -> find income
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

        elif sub == 'fixed_savings_find_income':
            # Q5: Person spends Rs.A exactly and saves Rs.B. Income increases by P%. Find new savings.
            spend_abs = random.choice([800, 1200, 1500, 2000, 2500])
            save_abs = random.choice([200, 400, 500, 600, 800])
            i_inc = random.choice([10, 15, 20, 25, 30])
            income_orig = spend_abs + save_abs
            new_income = income_orig * (1 + i_inc / 100)
            new_savings = new_income - spend_abs  # expenditure stays fixed
            
            names = ["Asha", "Ramesh", "David", "Pooja"]
            name = random.choice(names)
            question = (
                f"{name} spends Rs.{spend_abs} and saves Rs.{save_abs} per month. "
                f"If the income increases by {i_inc}%, what will be the new monthly savings?"
            )
            correct = f"Rs.{int(new_savings)}"
            explanation = (
                f"Original Income = Spend + Save = {spend_abs} + {save_abs} = Rs.{income_orig}.\n"
                f"New Income = {income_orig} × {1 + i_inc/100} = Rs.{new_income}.\n"
                f"Expenditure remains fixed at Rs.{spend_abs}.\n"
                f"New Savings = {new_income} - {spend_abs} = Rs.{int(new_savings)}."
            )
            opts = [correct]
            alts = [f"Rs.{int(new_savings) + d}" for d in [-200, -100, 100, 200, 300] if new_savings + d > 0]
            for a in alts:
                if a not in opts: opts.append(a)
                if len(opts) == 4: break
            random.shuffle(opts)
            return {"question_text": question, "options": opts,
                    "correct_option_index": opts.index(correct),
                    "explanation": explanation, "difficulty": 3}

        elif sub == 'compare_two_persons':
            # Q6: A's income is P% more than B's. A spends Q% more than B. Find ratio of savings or who saves more.
            p_more_income = random.choice([10, 20, 25, 50])
            q_more_spend = random.choice([5, 10, 20, 30])
            spend_B = random.choice([600, 800, 1000, 1200])
            income_B = random.choice([1000, 1200, 1500, 2000])
            while income_B <= spend_B:
                income_B = spend_B + random.choice([200, 400, 500])
            income_A = income_B * (1 + p_more_income / 100)
            spend_A = spend_B * (1 + q_more_spend / 100)
            save_A = income_A - spend_A
            save_B = income_B - spend_B
            from fractions import Fraction
            r = Fraction(int(save_A * 100), int(save_B * 100))
            names_pair = random.choice([("Ravi", "Suresh"), ("Meena", "Tina"), ("Ankit", "Vikas")])
            question = (
                f"The monthly income of {names_pair[0]} is {p_more_income}% more than that of {names_pair[1]}. "
                f"{names_pair[0]}'s monthly expenditure is {q_more_spend}% more than {names_pair[1]}'s. "
                f"If {names_pair[1]}'s monthly income is Rs.{income_B} and expenditure is Rs.{spend_B}, "
                f"what is the ratio of {names_pair[0]}'s to {names_pair[1]}'s monthly savings?"
            )
            correct = f"{r.numerator}:{r.denominator}"
            explanation = (
                f"{names_pair[0]}'s income = {income_B} × {1 + p_more_income/100} = Rs.{income_A}.\n"
                f"{names_pair[0]}'s expenditure = {spend_B} × {1 + q_more_spend/100} = Rs.{spend_A}.\n"
                f"{names_pair[0]}'s savings = {income_A} - {spend_A} = Rs.{save_A}.\n"
                f"{names_pair[1]}'s savings = {income_B} - {spend_B} = Rs.{save_B}.\n"
                f"Ratio = {save_A}:{save_B} = {r.numerator}:{r.denominator}."
            )
            opts = [correct]
            parts = [r.numerator, r.denominator]
            for d in [1, -1, 2]:
                alt = f"{parts[0]+d}:{parts[1]+d}"
                if alt not in opts: opts.append(alt)
                if len(opts) == 4: break
            random.shuffle(opts)
            return {"question_text": question, "options": opts,
                    "correct_option_index": opts.index(correct),
                    "explanation": explanation, "difficulty": 4}

        elif sub == 'exp_as_pct_of_savings':
            # Q7: Expenditure is E% of income. Income increases by I%. Expenditure unchanged. What % is exp of new savings?
            e_pct = random.choice([60, 64, 70, 75, 80])
            i_inc = random.choice([15, 20, 25, 30])
            I0 = 100
            E0 = e_pct
            S0 = 100 - e_pct
            I1 = 100 * (1 + i_inc / 100)
            S1 = I1 - E0
            exp_as_pct_savings = round((E0 / S1) * 100, 2)
            question = (
                f"A person's expenditure is {e_pct}% of his income. If his income is increased by {i_inc}% "
                f"while his expenditure remains unchanged, then his expenditure is what percent of his savings?"
            )
            correct = f"{exp_as_pct_savings}%"
            explanation = (
                f"Let Income = 100. Expenditure = {e_pct}. Savings = {S0}.\n"
                f"New Income = 100 × {1 + i_inc/100} = {I1}.\n"
                f"Expenditure unchanged = {e_pct}.\n"
                f"New Savings = {I1} - {e_pct} = {S1}.\n"
                f"Exp as % of Savings = ({e_pct} / {S1}) × 100 = {exp_as_pct_savings}%."
            )
            opts = [correct]
            alts = [round(exp_as_pct_savings + d, 2) for d in [-10, -5, 5, 10, 15] if exp_as_pct_savings + d > 0]
            for a in alts:
                a_str = f"{a}%"
                if a_str not in opts: opts.append(a_str)
                if len(opts) == 4: break
            random.shuffle(opts)
            return {"question_text": question, "options": opts,
                    "correct_option_index": opts.index(correct),
                    "explanation": explanation, "difficulty": 4}

        elif sub == 'savings_absolute_change':
            # Q8: Income + I%, Expenditure + E%, Savings increases by Rs.Z -> Find original income
            i_inc = random.choice([20, 25, 30, 40])
            e_inc = random.choice([10, 15, 20, 25])
            e_pct = random.choice([50, 60, 70, 75, 80])
            I0 = 1000  # base
            E0 = I0 * e_pct / 100
            S0 = I0 - E0
            I1 = I0 * (1 + i_inc / 100)
            E1 = E0 * (1 + e_inc / 100)
            S1 = I1 - E1
            unit_change = S1 - S0
            mult = random.choice([2, 3, 4, 5, 10])
            Z = int(unit_change * mult)
            Income_actual = int(I0 * mult)
            question = (
                f"A person spends {e_pct}% of his income. If his income increases by {i_inc}% "
                f"and expenditure increases by {e_inc}%, his savings increase by Rs.{Z}. "
                f"What is his original income?"
            )
            correct = f"Rs.{Income_actual}"
            explanation = (
                f"Let Income = {I0}. Expenditure = {e_pct}% = {E0}. Savings = {S0}.\n"
                f"New Income = {I1}. New Expenditure = {E1}. New Savings = {S1}.\n"
                f"Increase in savings = {unit_change} per {I0} of income.\n"
                f"Given increase = Rs.{Z}, so multiplier = {Z}/{int(unit_change)} = {mult}.\n"
                f"Original Income = {I0} × {mult} = Rs.{Income_actual}."
            )
            opts, idx = make_options(Income_actual, step=Income_actual // 4)
            return {"question_text": question, "options": opts,
                    "correct_option_index": idx,
                    "explanation": explanation, "difficulty": 5}

    def generate_pass_fail_aggregates(self):
        """Phase 21 Cat 2: Pass/Fail and Aggregate Scaling distributions
        """
        sub = random.choice([
            'split_pass_fail_ratios',     # Q1: school X/Y ratio with total pass%
            'weighted_pass_fail',         # Q2: weighted avg of pass% across two years
            'missing_weighted_component', # Q3: find required % in second paper for overall target
            'margin_work_scaling',        # Q4: typing lines with margin calculation
            'absentee_splits',            # Q5: % absent given boys/girls present%
            'fail_by_marks',              # Q6: student fails by N marks, find pass marks
            'pass_by_marks',              # Q7: student passes by N marks, find max marks
            'two_students_fail_pass',     # Q8: A fails by X, B passes by Y, find pass marks
            'pass_pct_given_marks',       # Q9: find pass% given marks scored and pass mark
            'find_max_marks',             # Q10: student scores X%, gets Y more than pass marks, find max
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
            valid_cases = []
            for P in [20, 50, 100, 150]:
                for F1 in [20, 25, 30, 40]:
                    for F2 in [10, 15, 20, 25, 30]:
                        P1 = 100 - F1
                        P2 = 100 - F2
                        nx = 100
                        ny = int(100 * (1 + P / 100))
                        total_students = nx + ny
                        total_pass = nx * P1 / 100 + ny * P2 / 100
                        P_tot = (total_pass / total_students) * 100

                        if P_tot.is_integer() and 0 < P_tot < 100:
                            valid_cases.append((P, F1, F2, P1, nx, ny, total_pass, int(P_tot)))

            P, F1, F2, P1, nx, ny, total_pass, P_tot = random.choice(valid_cases)

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
            valid_cases = []
            for M1 in [200, 300, 400]:
                for M2 in [100, 200, 300]:
                    for P1 in [32, 40, 50, 60]:
                        for P_tot in [46, 55, 65, 75]:
                            M_tot = M1 + M2
                            marks1 = (P1 * M1) / 100
                            marks_target = (P_tot * M_tot) / 100
                            marks2_needed = marks_target - marks1
                            P2_req = (marks2_needed / M2) * 100

                            if 0 < P2_req <= 100:
                                valid_cases.append((M1, M2, M_tot, P1, P_tot, marks1, marks_target, marks2_needed, P2_req))

            M1, M2, M_tot, P1, P_tot, marks1, marks_target, marks2_needed, P2_req = random.choice(valid_cases)
            
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

        elif sub == 'fail_by_marks':
            # Q6: Student scores X marks and fails by Y marks. Find pass marks.
            pass_marks = random.choice([150, 200, 240, 250, 300, 360])
            fail_by = random.choice([10, 15, 20, 25, 30, 40])
            scored = pass_marks - fail_by
            templates = [
                f"A student scores {scored} marks in an examination and fails by {fail_by} marks. What are the pass marks?",
                f"In an exam, a candidate obtained {scored} marks but failed by {fail_by} marks. What is the minimum marks required to pass?",
                f"Rohan got {scored} marks in an examination but could not pass. He fell short by {fail_by} marks. Find the pass mark.",
            ]
            question = random.choice(templates)
            correct = str(pass_marks)
            explanation = (
                f"Pass marks = Marks scored + Marks short of passing\n"
                f"= {scored} + {fail_by} = {pass_marks}."
            )
            opts = [correct]
            for d in [-fail_by * 2, -fail_by, fail_by, fail_by * 2]:
                alt = str(pass_marks + d)
                if alt not in opts and int(alt) > 0: opts.append(alt)
                if len(opts) == 4: break
            random.shuffle(opts)
            return {"question_text": question, "options": opts,
                    "correct_option_index": opts.index(correct),
                    "explanation": explanation, "difficulty": 2}

        elif sub == 'pass_by_marks':
            # Q7: Student passes by Y marks, scored is given, find pass marks or max marks.
            pass_pct = random.choice([33, 40, 50, 60])
            max_marks = random.choice([300, 400, 500, 600, 800])
            pass_marks = (pass_pct * max_marks) // 100
            pass_by = random.choice([10, 15, 20, 30, 40])
            scored = pass_marks + pass_by
            find_what = random.choice(['pass_marks', 'max_marks'])
            if find_what == 'pass_marks':
                templates = [
                    f"A candidate scored {scored} marks in an exam with maximum marks of {max_marks} and passed by {pass_by} marks. What are the passing marks?",
                    f"Sunita scored {scored} marks in an exam of {max_marks} marks. She passed by {pass_by} marks. What is the minimum marks required to pass?",
                ]
                question = random.choice(templates)
                correct = str(pass_marks)
                explanation = (
                    f"Pass marks = Scored - Excess over pass marks\n"
                    f"= {scored} - {pass_by} = {pass_marks}."
                )
            else:
                templates = [
                    f"A student scored {scored} marks in an exam and passed by {pass_by} marks. The pass percentage is {pass_pct}%. Find the maximum marks.",
                    f"Vikram got {scored} marks in an exam. He passed by {pass_by} marks. If the pass percentage is {pass_pct}%, what are the total marks?",
                ]
                question = random.choice(templates)
                correct = str(max_marks)
                explanation = (
                    f"Pass marks = Scored - Excess = {scored} - {pass_by} = {pass_marks}.\n"
                    f"{pass_pct}% of Max = {pass_marks}\n"
                    f"Max = {pass_marks} × 100 / {pass_pct} = {max_marks}."
                )
            opts = [correct]
            step = int(correct) // 5
            for d in [-2, -1, 1, 2]:
                alt = str(int(correct) + d * step)
                if alt not in opts and int(alt) > 0: opts.append(alt)
                if len(opts) == 4: break
            random.shuffle(opts)
            return {"question_text": question, "options": opts,
                    "correct_option_index": opts.index(correct),
                    "explanation": explanation, "difficulty": 3}

        elif sub == 'two_students_fail_pass':
            # Q8: A fails by X marks. B passes by Y marks. A scored N more/less than B. Find pass marks.
            pass_marks = random.choice([200, 240, 300, 360, 400])
            fail_A_by = random.choice([10, 15, 20, 25])
            pass_B_by = random.choice([10, 15, 20, 25])
            scored_A = pass_marks - fail_A_by
            scored_B = pass_marks + pass_B_by
            diff = scored_B - scored_A
            templates = [
                (f"A student A fails by {fail_A_by} marks in an exam. Another student B passes by {pass_B_by} marks. "
                 f"If B scored {diff} marks more than A, find the pass marks.", pass_marks),
                (f"In an examination, Ramesh fails by {fail_A_by} marks while Suresh passes by {pass_B_by} marks. "
                 f"Suresh got {diff} more marks than Ramesh. What are the pass marks?", pass_marks),
            ]
            tmpl, correct_val = random.choice(templates)
            question = tmpl
            correct = str(correct_val)
            explanation = (
                f"A scored = Pass - {fail_A_by} = Pass - {fail_A_by}.\n"
                f"B scored = Pass + {pass_B_by} = Pass + {pass_B_by}.\n"
                f"Difference = B - A = {pass_B_by} + {fail_A_by} = {diff}.\n"
                f"But given difference is {diff}, which matches. Pass marks = {pass_marks}."
            )
            opts = [correct]
            for d in [-fail_A_by * 2, -fail_A_by, pass_B_by, pass_B_by * 2]:
                alt = str(pass_marks + d)
                if alt not in opts and int(alt) > 0: opts.append(alt)
                if len(opts) == 4: break
            random.shuffle(opts)
            return {"question_text": question, "options": opts,
                    "correct_option_index": opts.index(correct),
                    "explanation": explanation, "difficulty": 3}

        elif sub == 'pass_pct_given_marks':
            # Q9: A student scored N marks out of M. Pass marks are P. Find pass percentage.
            max_marks = random.choice([300, 400, 500, 600])
            pass_marks = random.choice([120, 150, 200, 240])
            while pass_marks >= max_marks:
                pass_marks = random.randint(max_marks // 3, max_marks // 2)
            pass_pct = round((pass_marks / max_marks) * 100, 2)
            scored = pass_marks + random.choice([10, 20, 30, 40])
            templates = [
                f"In an examination with {max_marks} maximum marks and {pass_marks} pass marks, what is the pass percentage?",
                f"To pass an examination, a student needs to score {pass_marks} out of {max_marks}. What is the minimum pass percentage?",
                f"An exam has a maximum of {max_marks} marks. The minimum required to pass is {pass_marks} marks. What percentage is the pass mark?",
            ]
            question = random.choice(templates)
            correct = f"{pass_pct}%"
            explanation = (
                f"Pass percentage = (Pass marks / Max marks) × 100\n"
                f"= ({pass_marks} / {max_marks}) × 100 = {pass_pct}%."
            )
            opts = [correct]
            alts = [round(pass_pct + d, 2) for d in [-10, -5, 5, 10] if pass_pct + d > 0]
            for a in alts:
                a_str = f"{a}%"
                if a_str not in opts: opts.append(a_str)
                if len(opts) == 4: break
            random.shuffle(opts)
            return {"question_text": question, "options": opts,
                    "correct_option_index": opts.index(correct),
                    "explanation": explanation, "difficulty": 2}

        elif sub == 'find_max_marks':
            # Q10: Student scores P% and gets Y more marks than passing. Passing % is Q. Find max marks.
            pass_pct = random.choice([33, 40, 50])
            score_pct = random.choice([50, 60, 70, 75, 80])
            while score_pct <= pass_pct:
                score_pct = pass_pct + random.choice([10, 15, 20, 25])
            max_marks = random.choice([200, 300, 400, 500, 600])
            pass_marks = (pass_pct * max_marks) // 100
            score_marks = (score_pct * max_marks) // 100
            excess = score_marks - pass_marks
            templates = [
                f"By scoring {score_pct}% marks, a student passes by {excess} marks. If the pass percentage is {pass_pct}%, what are the maximum marks?",
                f"A candidate scores {score_pct}% in an exam and exceeds the pass mark by {excess}. If the pass percentage is {pass_pct}%, find the total marks.",
                f"Geeta scores {score_pct}% in her exam and passes by {excess} marks. The pass percentage is {pass_pct}%. What is the maximum marks in the exam?",
            ]
            question = random.choice(templates)
            correct = str(max_marks)
            explanation = (
                f"Score = {score_pct}% of M. Pass marks = {pass_pct}% of M.\n"
                f"Excess = ({score_pct} - {pass_pct})% of M = {excess}.\n"
                f"{score_pct - pass_pct}% of M = {excess}.\n"
                f"M = {excess} × 100 / {score_pct - pass_pct} = {max_marks}."
            )
            opts, idx = make_options(max_marks, step=max_marks // 4)
            return {"question_text": question, "options": opts,
                    "correct_option_index": opts.index(correct),
                    "explanation": explanation, "difficulty": 4}

    def generate_exam_scoring(self):
        """Phase 22 Cat 1: Examination Scoring & Cut-offs
        Covers pass/fail marks, max marks, and shifts.
        """
        sub = random.choice([
            'sum_difference_pct',         # Q1, Q4
            'avg_candidates',             # Q2
            'student_chain',              # Q3
            'ratio_shift_pass_fail',      # Q5
            'score_comparison_chain',     # Q6
            'fail_pass_offsets',          # Q7
            'fail_pass_simple'            # Q8
        ])

        def make_options_int(correct_val):
            opts = [str(correct_val)]
            step = max(5, correct_val // 10)
            while len(opts) < 4:
                alt = correct_val + random.choice([-3, -2, -1, 1, 2, 3]) * step
                if alt > 0 and str(alt) not in opts:
                    opts.append(str(alt))
            random.shuffle(opts)
            return opts, opts.index(str(correct_val))

        if sub == 'sum_difference_pct':
            # Q1, Q4: A got X marks more than B. A's marks were P% of sum.
            diff = random.choice([9, 10, 15, 20, 30])
            p = random.choice([55, 56, 60, 62.5])
            
            # A = p/100 * (A + B)
            # A = p/100 * (A + A - diff) = p/100 * (2A - diff)
            # 100A = p * 2A - p * diff
            # A * (100 - 2p) = -p * diff
            # A = p * diff / (2p - 100)
            
            while True:
                num = p * diff
                den = 2 * p - 100
                if den > 0 and num % den == 0:
                    a_marks = num // den
                    b_marks = a_marks - diff
                    break
                else:
                    diff = random.randint(5, 40)
                    p = random.choice([52, 54, 55, 56, 58, 60])

            names = ["Ram", "Shyam", "Rahul", "Pranita", "Amit"]
            objs = ["Math", "Science", "English"]
            n1, n2 = random.sample(names, 2)
            o1, o2 = random.sample(objs, 2)
            
            if random.random() > 0.5:
                question = f"In an entrance exam, {n1} secured {diff} marks more than {n2}, and his marks were {p}% of the sum of their marks. What were the marks obtained by them?"
                correct = f"{a_marks} and {b_marks}"
                explanation = (f"Let {n1} = A, {n2} = B. A = B + {diff} => B = A - {diff}.\n"
                               f"A = {p}% of (A + B) = {p}/100 * (A + A - {diff})\n"
                               f"100A = {p}(2A - {diff}) => 100A = {2*p}A - {p*diff}\n"
                               f"{2*p - 100}A = {p*diff} => A = {num}/{den} = {a_marks}.\n"
                               f"B = {a_marks} - {diff} = {b_marks}.")
            else:
                question = f"{n1} got {diff} marks more in {o1} than what she got in {o2}. Her {o1} marks are {p}% of the sum of her {o1} and {o2} marks. What are her {o2} marks?"
                correct = str(b_marks)
                explanation = (f"Let {o1} = M, {o2} = S. M = S + {diff}.\n"
                               f"M = {p}% of (M + S) => M = {p}/100 * (M + M - {diff})\n"
                               f"M = {a_marks}, S = {b_marks}.")

            opts = [correct]
            if "and" in correct:
                alts = [f"{a_marks+10} and {b_marks+10}", f"{a_marks-5} and {b_marks-5}", f"{a_marks+20} and {b_marks+20}"]
            else:
                alts = [str(b_marks+10), str(b_marks-10), str(b_marks+15)]
            for a in alts:
                if a not in opts: opts.append(a)
            random.shuffle(opts)
            return {"question_text": question, "options": opts, "correct_option_index": opts.index(correct), "explanation": explanation, "difficulty": 4}

        elif sub == 'avg_candidates':
            # Q2: Average marks of N candidates is A_tot. Avg of passed is A_p, avg of failed is A_f. Find passed count.
            n_tot = random.choice([100, 120, 150, 200])
            while True:
                a_tot = random.randint(25, 45)
                a_passed = random.randint(a_tot + 5, 60)
                a_failed = random.randint(10, a_tot - 5)
                
                # Equation: x * a_p + (n_tot - x) * a_f = n_tot * a_tot
                # x(a_p - a_f) = n_tot(a_tot - a_f)
                num = n_tot * (a_tot - a_failed)
                den = a_passed - a_failed
                if num % den == 0:
                    x = num // den
                    break

            question = f"The average marks obtained by {n_tot} candidates in a certain examination is {a_tot}. If the average marks of passed candidates is {a_passed} and failed candidates is {a_failed}, what is the number of candidates who passed the exam?"
            correct = str(x)
            explanation = (f"Let passed = x. Failed = {n_tot} - x.\n"
                           f"Total Marks = {n_tot} * {a_tot} = {n_tot * a_tot}.\n"
                           f"x * {a_passed} + ({n_tot} - x) * {a_failed} = {n_tot * a_tot}.\n"
                           f"x({a_passed} - {a_failed}) = {n_tot*a_tot} - {n_tot*a_failed} = {num}.\n"
                           f"x = {num} / {den} = {x}.")
            opts, idx = make_options_int(x)
            return {"question_text": question, "options": opts, "correct_option_index": idx, "explanation": explanation, "difficulty": 4}

        elif sub == 'student_chain':
            # Q3: Chain percentage. A = B*(1+x%), A = C*(1-y%). Given B find C.
            b_marks = random.choice([200, 220, 250, 300])
            p_ab = random.randint(10, 25)
            p_ac_less = random.randint(5, 15)
            
            a_marks = b_marks * (1 + p_ab / 100)
            c_marks = a_marks / (1 - p_ac_less / 100)
            
            while not c_marks.is_integer():
                b_marks += 10
                p_ab = random.randint(10, 25)
                p_ac_less = random.randint(5, 15)
                a_marks = b_marks * (1 + p_ab / 100)
                c_marks = a_marks / (1 - p_ac_less / 100)

            c_marks = int(c_marks)
            question = f"A, B, and C are three students. A got {p_ab}% more marks than B and {p_ac_less}% less marks than C. If B got {b_marks} marks, then how many marks has C got?"
            correct = str(c_marks)
            explanation = (f"B = {b_marks}.\n"
                           f"A = B + {p_ab}% of B = {b_marks} * {1 + p_ab/100} = {int(a_marks)}.\n"
                           f"A is {p_ac_less}% less than C => A = C * (100 - {p_ac_less})/100 = C * {100-p_ac_less}/100.\n"
                           f"C = ({int(a_marks)} * 100) / {100-p_ac_less} = {c_marks}.")
            opts, idx = make_options_int(c_marks)
            return {"question_text": question, "options": opts, "correct_option_index": idx, "explanation": explanation, "difficulty": 4}

        elif sub == 'ratio_shift_pass_fail':
            # Q5: Initial ratio P:F = a:b. If 1 more passed & appeared (so total +1), and 3 less failed...
            # Wait, "If one more students had appeared & passed & the number of failed students was 3 less than earlier"
            # This means: New Pass = P + 1, New Fail = F - 3. Total students = (P+1)+(F-3) = P+F-2.
            # Initial: P = 25k, F = 4k.
            # New: (25k + 1) / (4k - 3) = 22 / 3.
            # 3(25k + 1) = 22(4k - 3)
            # 75k + 3 = 88k - 66
            # 13k = 69 -> k = 69/13 (not nice).
            
            # Let's generalize: (ak + m) / (bk - n) = c / d
            # d(ak + m) = c(bk - n)
            # dak + dm = cbk - cn
            # k(cb - da) = dm + cn
            # k = (dm + cn) / (cb - da)
            
            while True:
                a, b = 25, 4
                c, d = random.randint(5, 30), random.randint(1, 10)
                m, n = random.randint(1, 5), random.randint(1, 5)
                
                num = d * m + c * n
                den = c * b - d * a
                if den != 0 and num % den == 0 and num // den > 0:
                    k = num // den
                    init_pass = a * k
                    init_fail = b * k
                    diff = init_pass - init_fail
                    break
                else:
                    a, b = random.choice([(25, 4), (5, 2), (7, 3)])
                    c, d = random.choice([(22, 3), (4, 1), (3, 1)])
                    m, n = random.randint(1, 5), random.randint(1, 10)

            question = f"In an exam, the number of students who passed and the number of students who failed were in the ratio of {a}:{b}. If {m} more student(s) had appeared and passed and the number of failed students was {n} less than earlier, the ratio of passed students to failed students would have become {c}:{d}. What is the difference between the number of students who initially passed and the number who failed?"
            correct = str(abs(diff))
            explanation = (f"Initial ratio {a}:{b} => Pass = {a}k, Fail = {b}k.\n"
                           f"New Pass = {a}k + {m}, New Fail = {b}k - {n}.\n"
                           f"({a}k + {m})/({b}k - {n}) = {c}/{d}.\n"
                           f"Solving for k: {d}({a}k + {m}) = {c}({b}k - {n}) => {k*den}k = {num} => k = {k}.\n"
                           f"Initial Pass = {a}*{k} = {init_pass}, Initial Fail = {b}*{k} = {init_fail}.\n"
                           f"Difference = {init_pass} - {init_fail} = {diff}.")
            opts, idx = make_options_int(abs(diff))
            return {"question_text": question, "options": opts, "correct_option_index": idx, "explanation": explanation, "difficulty": 5}

        elif sub == 'score_comparison_chain':
            # Q6 style: Chain of relative scores. A < B, B > C, C relative to D...
            # Ram scored 25 less than Rohit. Rohit 45 more than Sam. Rohan 75 (10 more than Sam). Ravi 34 more than Ram. Max-Ravi = 50. Find Ravi %.
            
            sam = random.randint(50, 80)
            rohan_diff = random.randint(5, 15)
            rohan = sam + rohan_diff
            
            rohit_diff = random.randint(30, 60)
            rohit = sam + rohit_diff
            
            ram_diff = random.randint(10, 30)
            ram = rohit - ram_diff
            
            ravi_diff = random.randint(20, 40)
            ravi = ram + ravi_diff
            
            max_offset = random.randint(40, 60)
            max_marks = ravi + max_offset
            
            pct = round((ravi / max_marks) * 100, 1)

            question = f"In an examination Ram scored {ram_diff} marks less than Rohit. Rohit scored {rohit_diff} more marks than Sam. Rohan scored {rohan} marks which is {rohan_diff} more than Sam. Ravi's score is {max_offset} less than the maximum marks of the test. What approximate percentage of marks did Ravi score if he gets {ravi_diff} more than Ram?"
            correct = f"{pct}%"
            explanation = (f"Rohan = {rohan}. Rohan = Sam + {rohan_diff} => Sam = {rohan} - {rohan_diff} = {sam}.\n"
                           f"Rohit = Sam + {rohit_diff} = {sam} + {rohit_diff} = {rohit}.\n"
                           f"Ram = Rohit - {ram_diff} = {rohit} - {ram_diff} = {ram}.\n"
                           f"Ravi = Ram + {ravi_diff} = {ram} + {ravi_diff} = {ravi}.\n"
                           f"Max Marks = Ravi + {max_offset} = {ravi} + {max_offset} = {max_marks}.\n"
                           f"Ravi % = ({ravi} / {max_marks}) * 100 = {pct}%.")
            
            opts = [correct]
            for d in [-3.2, 2.5, 5.0]:
                alt = f"{round(pct + d, 1)}%"
                if alt not in opts: opts.append(alt)
            random.shuffle(opts)
            return {"question_text": question, "options": opts, "correct_option_index": opts.index(correct), "explanation": explanation, "difficulty": 5}

        elif sub == 'fail_pass_offsets':
            # Q7: gets X% fail by M. gets Y% gets N more than pass. Find max marks.
            # Pass Mark = X% Max + M = Y% Max - N
            # (Y - X)% Max = M + N
            # Max = (M + N) / ((Y - X)/100)
            
            while True:
                x = random.randint(25, 35)
                y = random.randint(x + 5, 45)
                m = random.randint(10, 30)
                n = random.randint(10, 30)
                
                num = (m + n) * 100
                den = y - x
                if num % den == 0:
                    max_marks = num // den
                    pass_marks = (x * max_marks // 100) + m
                    break
            
            question = f"In a test, a student got {x}% marks and failed by {m} marks. In the same test, another student got {y}% marks and secured {n} marks more than the essential minimum pass marks. What is the maximum pass marks (maximum marks) of the test?"
            correct = str(max_marks)
            explanation = (f"Let Max Marks = T.\n"
                           f"Passing Marks P = {x}% of T + {m}.\n"
                           f"Passing Marks P = {y}% of T - {n}.\n"
                           f"{y}% of T - {x}% of T = {m} + {n}.\n"
                           f"({y-x})% of T = {m+n} => T = ({m+n} * 100) / {y-x} = {max_marks}.")
            opts, idx = make_options_int(max_marks)
            return {"question_text": question, "options": opts, "correct_option_index": idx, "explanation": explanation, "difficulty": 4}

        elif sub == 'fail_pass_simple':
            # Q8: Need P% to pass. Gets M, fails by N. Find Max.
            while True:
                p = random.choice([25, 30, 33, 35, 40])
                m = random.randint(40, 150)
                n = random.randint(10, 50)
                
                num = (m + n) * 100
                if num % p == 0:
                    max_marks = num // p
                    break

            question = f"For a student to pass an exam, he has to secure {p}% marks. If he gets {m} marks and fails by {n}, then what are the maximum marks of the exam?"
            correct = str(max_marks)
            explanation = (f"Passing Marks = {m} + {n} = {m+n}.\n"
                           f"{p}% of Max = {m+n} => Max = ({m+n} * 100) / {p} = {max_marks}.")
            opts, idx = make_options_int(max_marks)
            return {"question_text": question, "options": opts, "correct_option_index": idx, "explanation": explanation, "difficulty": 3}

    def generate_successive_net_change(self):
        """Phase 22 Cat 2: Successive Percentage Net Change
        Calculates equivalent single change for multiple random changes.
        """
        n_changes = random.choice([2, 3])
        has_decimal = random.random() < 0.3 # 30% chance have one decimal
        decimal_idx = random.randint(0, n_changes - 1) if has_decimal else -1
        changes = []
        for i in range(n_changes):
            if i == decimal_idx:
                # Generate a decimal (e.g., 12.5)
                val = round(random.uniform(2.5, 15.5), 1)
                if int(val) == val: val += 0.5 # Force it to be a decimal
            else:
                # Generate an integer
                val = random.randint(2, 20)
            changes.append(val)
        
        # Net multiplier: (1 - d1)(1 - d2)... for discounts (based on user examples 1, 2 -> 2.98)
        multiplier = 1.0
        for d in changes:
            multiplier *= (1 - d/100)
        
        net_change = round((1 - multiplier) * 100, 3)
        
        change_str = ", ".join([f"{c}%" for c in changes])
        question = f"Calculate the single equivalent discount percentage for successive discounts of {change_str}."
        correct = f"{net_change}%"
        
        if n_changes == 2:
            d1, d2 = changes
            explanation = (f"Formula: d1 + d2 - (d1*d2)/100\n"
                           f"Net = {d1} + {d2} - ({d1}*{d2})/100 = {d1+d2} - {round(d1*d2/100, 4)} = {net_change}%.")
        else:
            d1, d2, d3 = changes
            r1 = (1 - d1/100)
            r2 = (1 - d2/100)
            r3 = (1 - d3/100)
            explanation = (f"Equivalent multiplier = (1 - d1/100)(1 - d2/100)(1 - d3/100)\n"
                           f"M = {r1:.4f} * {r2:.4f} * {r3:.4f} = {multiplier:.6f}\n"
                           f"Net Discount = (1 - {multiplier:.6f}) * 100 = {net_change}%.")

        opts = [correct]
        while len(opts) < 4:
            alt = round(net_change + random.choice([-1.5, -0.5, 0.5, 1.5, 2.0]), 3)
            if alt > 0:
                alt_str = f"{alt}%"
                if alt_str not in opts: opts.append(alt_str)
        random.shuffle(opts)
        
        return {"question_text": question, "options": opts, "correct_option_index": opts.index(correct), "explanation": explanation, "difficulty": 4}

    def generate_successive_discount(self):
        """Successive discount applications with marked price and selling price."""
        d1 = random.choice([5, 10, 12.5, 15, 20, 25, 30])
        d2 = random.choice([5, 10, 12.5, 15, 20, 25])
        marked_price = random.choice([800, 1000, 1200, 1500, 2000, 2500, 4000, 5000])
        multiplier = (1 - d1 / 100) * (1 - d2 / 100)
        selling_price = round(marked_price * multiplier, 2)
        net_discount = round((1 - multiplier) * 100, 2)
        subtype = random.choice(["selling_price", "marked_price", "equivalent_discount"])

        def money(value):
            return str(int(value)) if float(value).is_integer() else str(round(value, 2))

        if subtype == "selling_price":
            question = f"A product marked at {marked_price} is sold after two successive discounts of {d1}% and {d2}%. What is the final selling price?"
            correct = money(selling_price)
            explanation = (
                f"Successive discounts multiply the remaining price, not the discount rates.\n"
                f"Final price = {marked_price} * (1 - {d1}/100) * (1 - {d2}/100)\n"
                f"= {marked_price} * {1 - d1 / 100:.4f} * {1 - d2 / 100:.4f} = {correct}."
            )
            numeric_correct = selling_price
        elif subtype == "marked_price":
            question = f"After successive discounts of {d1}% and {d2}%, an item sells for {money(selling_price)}. What was its marked price?"
            correct = money(marked_price)
            explanation = (
                f"Selling price = Marked price * (1 - {d1}/100) * (1 - {d2}/100).\n"
                f"Marked price = {money(selling_price)} / ({1 - d1 / 100:.4f} * {1 - d2 / 100:.4f}) = {correct}."
            )
            numeric_correct = marked_price
        else:
            question = f"What single discount is equivalent to two successive discounts of {d1}% and {d2}%?"
            correct = f"{money(net_discount)}%"
            explanation = (
                f"Equivalent discount = d1 + d2 - (d1*d2)/100.\n"
                f"= {d1} + {d2} - ({d1}*{d2})/100 = {correct}."
            )
            numeric_correct = net_discount

        opts = [correct]
        for delta in [-10, -5, 5, 10, 15, -15]:
            alt_val = numeric_correct + delta if subtype == "equivalent_discount" else numeric_correct * (1 + delta / 100)
            if alt_val <= 0:
                continue

            alt = f"{money(round(alt_val, 2))}%" if subtype == "equivalent_discount" else money(round(alt_val, 2))
            if alt not in opts:
                opts.append(alt)
            if len(opts) == 4:
                break

        random.shuffle(opts)
        return {
            "question_text": question,
            "options": opts,
            "correct_option_index": opts.index(correct),
            "explanation": explanation,
            "difficulty": 3
        }

    def generate_vedic_addition(self):
        """Speed addition drills using left-to-right addition and complements."""
        sub_type = random.choice(["left_to_right", "complements", "missing_addend"])

        if sub_type == "left_to_right":
            a = random.randint(240, 890)
            b = random.randint(120, 760)
            c = random.randint(80, 490)
            correct = a + b + c
            question = f"Add mentally from left to right: {a} + {b} + {c}."
            explanation = f"Add in chunks: {a} + {b} = {a + b}, then {a + b} + {c} = {correct}."
            return self._mcq(question, correct, explanation, 2, [correct + 10, correct - 10, correct + 100, correct - 1])

        if sub_type == "complements":
            base = random.choice([100, 1000, 10000])
            gap_a = random.randint(3, min(87, base // 5))
            gap_b = random.randint(4, min(94, base // 5))
            a = base - gap_a
            b = base - gap_b
            correct = a + b
            question = f"Using complements to {base}, find {a} + {b}."
            explanation = f"{a} is {gap_a} below {base} and {b} is {gap_b} below {base}. So {a} + {b} = 2 x {base} - ({gap_a} + {gap_b}) = {correct}."
            return self._mcq(question, correct, explanation, 2, [correct + gap_a, correct + gap_b, correct - 10, correct + 100])

        a = random.randint(180, 760)
        b = random.randint(140, 620)
        missing = random.randint(90, 540)
        total = a + b + missing
        question = f"What number should replace x if {a} + x + {b} = {total}?"
        explanation = f"Combine known terms: {a} + {b} = {a + b}. Then x = {total} - {a + b} = {missing}."
        return self._mcq(question, missing, explanation, 2, [missing + 10, missing - 10, total - a, total - b])

    def generate_vedic_subtraction(self):
        """Speed subtraction drills using borrowing, complements, and near-base differences."""
        sub_type = random.choice(["left_to_right", "base_complement", "near_base_difference", "missing_minuend"])

        if sub_type == "left_to_right":
            b = random.randint(180, 790)
            correct = random.randint(140, 860)
            a = b + correct
            question = f"Subtract mentally: {a} - {b}."
            explanation = f"Break {b} into easy parts and subtract left to right. {a} - {b} = {correct}."
            return self._mcq(question, correct, explanation, 2, [correct + 10, correct - 10, correct + 100, abs(correct - 100)])

        if sub_type == "base_complement":
            base = random.choice([1000, 10000])
            n = random.randint(base // 5, base - 17)
            correct = base - n
            question = f"Using the all-from-9-and-last-from-10 idea, find {base} - {n}."
            explanation = f"Subtract each leading digit from 9 and the last non-zero digit from 10. Directly, {base} - {n} = {correct}."
            return self._mcq(question, correct, explanation, 2, [correct + 1, correct - 1, correct + 10, correct + 100])

        if sub_type == "near_base_difference":
            base = random.choice([100, 1000])
            above = random.randint(3, 48)
            below = random.randint(4, 57)
            a = base + above
            b = base - below
            correct = above + below
            question = f"Find the difference quickly: {a} - {b}."
            explanation = f"{a} is {above} above {base}, while {b} is {below} below {base}. The difference is {above} + {below} = {correct}."
            return self._mcq(question, correct, explanation, 2, [abs(above - below), correct + 10, correct - 1, correct + 1])

        subtrahend = random.randint(260, 880)
        difference = random.randint(120, 760)
        minuend = subtrahend + difference
        question = f"If x - {subtrahend} = {difference}, what is x?"
        explanation = f"Add the subtrahend back to the difference: x = {difference} + {subtrahend} = {minuend}."
        return self._mcq(question, minuend, explanation, 2, [minuend + 10, minuend - 10, abs(subtrahend - difference), minuend + 100])

    def generate_vedic_multiplication(self):
        """Mental multiplication drills: near-base, by 11, split products, and 25/125 shortcuts."""
        sub_type = random.choice(["vertical_crosswise", "near_base_100", "multiply_by_11", "split_multiplier", "multiply_by_25_125"])

        if sub_type == "vertical_crosswise":
            a = random.randint(12, 98)
            b = random.randint(12, 98)
            correct = a * b
            question = f"Use vertical-and-crosswise multiplication to calculate {a} x {b}."
            explanation = f"For two-digit multiplication, combine units, cross-products, and tens. Directly, {a} x {b} = {correct}."
            return self._mcq(question, correct, explanation, 3, [correct + a, correct - b, correct + 10, correct - 10])

        if sub_type == "near_base_100":
            gap_a = random.choice([x for x in range(-18, 19) if x != 0])
            gap_b = random.choice([x for x in range(-18, 19) if x != 0])
            a = 100 + gap_a
            b = 100 + gap_b
            correct = a * b
            left = 100 + gap_a + gap_b
            question = f"Using the base-100 method, calculate {a} x {b}."
            explanation = f"Cross-adjust around 100: left part is 100 + ({gap_a}) + ({gap_b}) = {left}. The deviation product is {gap_a} x {gap_b} = {gap_a * gap_b}. Therefore {a} x {b} = {correct}."
            return self._mcq(question, correct, explanation, 3, [left * 100 + abs(gap_a * gap_b), correct + 100, correct - 100, correct + gap_a * gap_b])

        if sub_type == "multiply_by_11":
            tens = random.randint(2, 8)
            ones = random.randint(1, 8 - tens)
            n = 10 * tens + ones
            correct = n * 11
            question = f"Find {n} x 11 using the insert-the-sum shortcut."
            explanation = f"For {n} x 11, keep the outer digits {tens} and {ones}, and insert their sum {tens + ones}. So {n} x 11 = {correct}."
            return self._mcq(question, correct, explanation, 2, [n * 10, correct + 11, correct - 11, int(f"{tens}{ones}{tens + ones}")])

        if sub_type == "split_multiplier":
            a = random.randint(24, 89)
            tens = random.choice([20, 30, 40, 50, 60, 70, 80])
            ones = random.randint(2, 9)
            b = tens + ones
            correct = a * b
            question = f"Use splitting to calculate {a} x {b}."
            explanation = f"Split {b} as {tens} + {ones}. Then {a} x {b} = {a} x {tens} + {a} x {ones} = {a * tens} + {a * ones} = {correct}."
            return self._mcq(question, correct, explanation, 2, [a * tens, a * ones, correct + a, correct - a])

        multiplier = random.choice([25, 125])
        n = random.randint(12, 96)
        correct = n * multiplier
        question = f"Calculate {n} x {multiplier} using the shortcut."
        if multiplier == 25:
            explanation = f"Multiplying by 25 is the same as multiplying by 100 and dividing by 4: {n} x 25 = {n * 100} / 4 = {correct}."
        else:
            explanation = f"Multiplying by 125 is the same as multiplying by 1000 and dividing by 8: {n} x 125 = {n * 1000} / 8 = {correct}."
        return self._mcq(question, correct, explanation, 2, [correct + multiplier, correct - multiplier, n * 100, n * 10])

    def generate_vedic_division(self):
        """Fast division drills with exact division, remainders, and special divisors."""
        sub_type = random.choice(["short_division", "remainder", "divide_by_25_125", "missing_dividend"])

        if sub_type == "short_division":
            divisor = random.randint(6, 19)
            quotient = random.randint(24, 140)
            dividend = divisor * quotient
            question = f"Divide quickly: {dividend} / {divisor}."
            explanation = f"Since {divisor} x {quotient} = {dividend}, the quotient is {quotient}."
            return self._mcq(question, quotient, explanation, 2, [quotient + 1, quotient - 1, quotient + divisor, quotient - divisor])

        if sub_type == "remainder":
            divisor = random.randint(7, 23)
            quotient = random.randint(20, 120)
            remainder = random.randint(1, divisor - 1)
            dividend = divisor * quotient + remainder
            question = f"What is the remainder when {dividend} is divided by {divisor}?"
            explanation = f"{dividend} = {divisor} x {quotient} + {remainder}. Therefore the remainder is {remainder}."
            return self._mcq(question, remainder, explanation, 2, [divisor - remainder, remainder + 1, quotient, divisor])

        if sub_type == "divide_by_25_125":
            divisor = random.choice([25, 125])
            quotient = random.randint(12, 160)
            dividend = divisor * quotient
            question = f"Calculate {dividend} / {divisor} using a speed division shortcut."
            if divisor == 25:
                explanation = f"Dividing by 25 is the same as multiplying by 4 and dividing by 100: {dividend} x 4 / 100 = {quotient}."
            else:
                explanation = f"Dividing by 125 is the same as multiplying by 8 and dividing by 1000: {dividend} x 8 / 1000 = {quotient}."
            return self._mcq(question, quotient, explanation, 2, [quotient + 4, quotient - 4, quotient * 2, max(1, quotient // 2)])

        divisor = random.randint(6, 19)
        quotient = random.randint(14, 90)
        remainder = random.randint(0, divisor - 1)
        dividend = divisor * quotient + remainder
        question = f"A number divided by {divisor} gives quotient {quotient} and remainder {remainder}. Find the number."
        explanation = f"Dividend = divisor x quotient + remainder = {divisor} x {quotient} + {remainder} = {dividend}."
        return self._mcq(question, dividend, explanation, 2, [divisor + quotient + remainder, dividend + divisor, dividend - divisor, quotient * max(1, remainder)])

    def generate_vedic_tables_multiples(self):
        """Tables, missing factors, and multiple recognition drills."""
        sub_type = random.choice(["table_product", "missing_factor", "next_multiple", "factor_split"])

        if sub_type == "table_product":
            a = random.randint(12, 25)
            b = random.randint(6, 20)
            correct = a * b
            question = f"Recall the table value: {a} x {b} = ?"
            explanation = f"{a} x {b} = {correct}. Table fluency reduces load in longer aptitude calculations."
            return self._mcq(question, correct, explanation, 1, [correct + a, correct - a, correct + b, correct - b])

        if sub_type == "missing_factor":
            factor = random.randint(12, 25)
            missing = random.randint(6, 20)
            product = factor * missing
            question = f"If {factor} x x = {product}, what is x?"
            explanation = f"Use the table of {factor}: {factor} x {missing} = {product}, so x = {missing}."
            return self._mcq(question, missing, explanation, 1, [missing + 1, missing - 1, factor, product // 10])

        if sub_type == "next_multiple":
            base = random.randint(12, 25)
            k = random.randint(8, 30)
            target = base * k + random.randint(1, base - 1)
            correct = base * (k + 1)
            question = f"What is the smallest multiple of {base} greater than {target}?"
            explanation = f"{base} x {k} = {base * k}, which is below {target}. The next multiple is {base} x {k + 1} = {correct}."
            return self._mcq(question, correct, explanation, 2, [base * k, correct + base, correct - 1, target + base])

        a = random.randint(12, 25)
        b = random.randint(2, 9)
        c = random.randint(2, 9)
        correct = a * (b + c)
        question = f"Use table splitting to calculate {a} x {b} + {a} x {c}."
        explanation = f"Factor out {a}: {a} x {b} + {a} x {c} = {a} x ({b} + {c}) = {a} x {b + c} = {correct}."
        return self._mcq(question, correct, explanation, 2, [a * b, a * c, correct + a, correct - a])

    def generate_vedic_squares_roots(self):
        """Squares and square-root recognition drills."""
        sub_type = random.choice(["square_ending_5", "near_base_square", "two_digit_square", "perfect_square_root", "integer_square_root"])

        if sub_type == "square_ending_5":
            tens = random.randint(2, 12)
            n = tens * 10 + 5
            correct = n * n
            question = f"Find {n}^2 using the ending-in-5 shortcut."
            explanation = f"For a number ending in 5, multiply {tens} by {tens + 1} and append 25: {tens} x {tens + 1} = {tens * (tens + 1)}, so {n}^2 = {correct}."
            return self._mcq(question, correct, explanation, 2, [correct + 100, correct - 100, int(f"{tens * tens}25"), correct + 25])

        if sub_type == "near_base_square":
            base = random.choice([50, 100])
            gap = random.choice([x for x in range(-15, 16) if x != 0])
            n = base + gap
            correct = n * n
            question = f"Estimate and calculate exactly using near-base squaring: {n}^2."
            explanation = f"Use (base + gap)^2. Here {n}^2 = {base}^2 + 2 x {base} x ({gap}) + ({gap})^2 = {correct}."
            return self._mcq(question, correct, explanation, 3, [correct + abs(gap) * 10, correct - abs(gap) * 10, base * base + gap * gap, correct + 100])

        if sub_type == "two_digit_square":
            n = random.randint(21, 99)
            correct = n * n
            question = f"Calculate {n}^2 mentally."
            explanation = f"Use (a + b)^2 or a nearby base. Directly, {n} x {n} = {correct}."
            return self._mcq(question, correct, explanation, 2, [correct + n, correct - n, correct + 100, correct - 100])

        if sub_type == "perfect_square_root":
            root = random.randint(12, 45)
            square = root * root
            question = f"Find the square root of {square}."
            explanation = f"{root} x {root} = {square}, so sqrt({square}) = {root}."
            return self._mcq(question, root, explanation, 2, [root + 1, root - 1, root + 2, max(1, root - 2)])

        root = random.randint(15, 50)
        n = root * root + random.randint(1, 2 * root)
        correct = math.isqrt(n)
        question = f"What is the greatest integer less than or equal to sqrt({n})?"
        explanation = f"{correct}^2 = {correct * correct} and {correct + 1}^2 = {(correct + 1) * (correct + 1)}. Since {n} lies between them, the integer square root is {correct}."
        return self._mcq(question, correct, explanation, 3, [correct + 1, correct - 1, correct + 2, max(1, correct - 2)])

    def generate_vedic_cubes_roots(self):
        """Cubes, cube roots, and unit digit drills."""
        sub_type = random.choice(["cube_value", "perfect_cube_root", "nearest_cube", "cube_unit_digit"])

        if sub_type == "cube_value":
            n = random.randint(3, 20)
            correct = n ** 3
            question = f"Recall or calculate quickly: {n}^3 = ?"
            explanation = f"{n}^3 means {n} x {n} x {n} = {correct}."
            return self._mcq(question, correct, explanation, 2, [n * n, correct + n, correct - n, (n + 1) ** 3])

        if sub_type == "perfect_cube_root":
            root = random.randint(3, 20)
            cube = root ** 3
            question = f"Find the cube root of {cube}."
            explanation = f"{root}^3 = {cube}, so the cube root of {cube} is {root}."
            return self._mcq(question, root, explanation, 2, [root + 1, root - 1, root + 2, max(1, root - 2)])

        if sub_type == "nearest_cube":
            root = random.randint(5, 20)
            n = root ** 3 + random.randint(1, 3 * root * root)
            correct = round(n ** (1 / 3))
            while (correct + 1) ** 3 <= n:
                correct += 1
            while correct ** 3 > n:
                correct -= 1
            question = f"What is the greatest integer less than or equal to the cube root of {n}?"
            explanation = f"{correct}^3 = {correct ** 3} and {correct + 1}^3 = {(correct + 1) ** 3}. So the integer cube root is {correct}."
            return self._mcq(question, correct, explanation, 3, [correct + 1, correct - 1, correct + 2, max(1, correct - 2)])

        n = random.randint(12, 99)
        correct = (n ** 3) % 10
        question = f"What is the units digit of {n}^3?"
        explanation = f"Only the units digit matters. The units digit of {n} is {n % 10}, and {(n % 10)}^3 has units digit {correct}."
        return self._mcq(question, correct, explanation, 2, [(correct + 1) % 10, (correct + 2) % 10, (10 - correct) % 10, n % 10])

    def generate_vedic_divisibility(self):
        """Divisibility-rule drills across common aptitude divisors."""
        sub_type = random.choice(["rules_3_9", "rules_4_8", "rule_11", "combined_rules"])

        if sub_type == "rules_3_9":
            n = random.randint(1000, 99999)
            digit_sum = sum(int(d) for d in str(n))
            divisible_by_3 = digit_sum % 3 == 0
            divisible_by_9 = digit_sum % 9 == 0
            if divisible_by_9:
                correct = "3 and 9"
            elif divisible_by_3:
                correct = "3 only"
            else:
                correct = "neither 3 nor 9"
            question = f"The digit sum of {n} is {digit_sum}. By divisibility rules, {n} is divisible by which option?"
            explanation = f"A number is divisible by 3 or 9 when its digit sum is divisible by 3 or 9. Here the digit sum is {digit_sum}, so the answer is {correct}."
            return self._mcq(question, correct, explanation, 2, ["3 only", "9 only", "3 and 9", "neither 3 nor 9"])

        if sub_type == "rules_4_8":
            n = random.randint(1000, 99999)
            last_two = n % 100
            last_three = n % 1000
            div4 = last_two % 4 == 0
            div8 = last_three % 8 == 0
            if div8:
                correct = "4 and 8"
            elif div4:
                correct = "4 only"
            else:
                correct = "neither 4 nor 8"
            question = f"Using the last digits, decide whether {n} is divisible by 4, 8, both, or neither."
            explanation = f"For 4, check the last two digits: {last_two}. For 8, check the last three digits: {last_three}. Therefore the answer is {correct}."
            return self._mcq(question, correct, explanation, 2, ["4 only", "8 only", "4 and 8", "neither 4 nor 8"])

        if sub_type == "rule_11":
            n = random.randint(10000, 999999)
            digits = [int(d) for d in str(n)]
            alternating = abs(sum(digits[::2]) - sum(digits[1::2]))
            correct = alternating % 11
            question = f"For the divisibility-by-11 test on {n}, what is the remainder when the alternating digit-sum difference is divided by 11?"
            explanation = f"Alternating digit sums give |{sum(digits[::2])} - {sum(digits[1::2])}| = {alternating}. {alternating} mod 11 = {correct}."
            return self._mcq(question, correct, explanation, 3, [(correct + 1) % 11, (correct + 2) % 11, alternating, 11 - correct if correct else 11])

        divisors = [3, 4, 5, 6, 8, 9, 10, 11, 12, 15]
        n = random.randint(1000, 99999)
        correct = sum(1 for divisor in divisors if n % divisor == 0)
        question = f"How many numbers in this list divide {n}: 3, 4, 5, 6, 8, 9, 10, 11, 12, 15?"
        explanation = f"Test each divisor using its rule. The count of divisors from the list that divide {n} exactly is {correct}."
        return self._mcq(question, correct, explanation, 3, [correct + 1, max(0, correct - 1), correct + 2, max(0, correct - 2)])

    def generate_vedic_approximation(self):
        """Approximation, compatible numbers, and quick percent drills."""
        sub_type = random.choice(["compatible_sum", "estimate_product", "estimate_division", "quick_percent"])

        if sub_type == "compatible_sum":
            values = [random.randint(120, 980) for _ in range(3)]
            rounded = [round(v, -2) for v in values]
            correct = sum(rounded)
            question = f"Estimate {values[0]} + {values[1]} + {values[2]} by rounding each number to the nearest hundred."
            explanation = f"The rounded values are {rounded[0]}, {rounded[1]}, and {rounded[2]}. Their sum is {correct}."
            return self._mcq(question, correct, explanation, 1, [sum(values), correct + 100, correct - 100, correct + 200])

        if sub_type == "estimate_product":
            a = random.randint(24, 96)
            b = random.randint(24, 96)
            ra = round(a, -1)
            rb = round(b, -1)
            correct = ra * rb
            question = f"Estimate {a} x {b} by rounding both numbers to the nearest ten."
            explanation = f"{a} rounds to {ra} and {b} rounds to {rb}. Estimated product = {ra} x {rb} = {correct}."
            return self._mcq(question, correct, explanation, 1, [a * b, correct + 100, correct - 100, ra + rb])

        if sub_type == "estimate_division":
            divisor = random.choice([12, 15, 20, 25, 30, 40, 50])
            quotient = random.randint(8, 40)
            compatible_dividend = divisor * quotient
            dividend = compatible_dividend + random.randint(-divisor // 2, divisor // 2)
            question = f"Estimate {dividend} / {divisor} using compatible numbers."
            explanation = f"{dividend} is close to {compatible_dividend}, and {compatible_dividend} / {divisor} = {quotient}. So the estimate is {quotient}."
            return self._mcq(question, quotient, explanation, 1, [quotient + 1, quotient - 1, quotient + 2, max(1, quotient - 2)])

        percent = random.choice([5, 10, 12.5, 15, 20, 25, 50, 75])
        base = random.randint(8, 80) * 20
        correct_value = base * percent / 100
        correct = int(correct_value) if correct_value.is_integer() else correct_value
        question = f"Find {percent}% of {base} quickly."
        explanation = f"Use benchmark percentages: {percent}% of {base} = ({percent}/100) x {base} = {correct}."
        distractors = [correct_value + 10, max(0, correct_value - 10), correct_value * 2, correct_value / 2]
        distractors = [int(x) if float(x).is_integer() else x for x in distractors]
        return self._mcq(question, correct, explanation, 1, distractors)

    def generate_clockwise_anticlockwise(self):
        """Pattern: Clockwise and anti clockwise"""
        directions = ["North", "North-East", "East", "South-East", "South", "South-West", "West", "North-West"]
        dir_angles = {d: i * 45 for i, d in enumerate(directions)}
        angles_to_dir = {v: k for k, v in dir_angles.items()}
        
        start_dir = random.choice(directions)
        current_angle = dir_angles[start_dir]
        
        # Scenario: Facing X, turns A cw, then B acw, etc.
        num_turns = random.randint(2, 3)
        turns = []
        for _ in range(num_turns):
            angle = random.choice([45, 90, 135, 180, 225, 270])
            is_clockwise = random.random() > 0.5
            turns.append((angle, is_clockwise))
            if is_clockwise:
                current_angle = (current_angle + angle) % 360
            else:
                current_angle = (current_angle - angle) % 360
        
        final_dir = angles_to_dir[current_angle]
        
        turn_texts = []
        for angle, cw in turns:
            turn_texts.append(f"{angle}° {'clockwise' if cw else 'anti-clockwise'}")
        
        question = f"Facing {start_dir}, a person turns {' and then '.join(turn_texts)}. What direction is the person facing now?"
        
        options = [final_dir]
        while len(options) < 4:
            opt = random.choice(directions)
            if opt not in options:
                options.append(opt)
        
        random.shuffle(options)
        
        # Simple explanation
        exp_steps = [f"Initial: {start_dir} ({dir_angles[start_dir]}°)"]
        temp_angle = dir_angles[start_dir]
        for angle, cw in turns:
            change = angle if cw else -angle
            temp_angle = (temp_angle + change) % 360
            dir_now = angles_to_dir[temp_angle]
            exp_steps.append(f"Turn {angle}° {'CW' if cw else 'ACW'} -> {dir_now} ({temp_angle}°)")
            
        return {
            "question_text": question,
            "options": options,
            "correct_option_index": options.index(final_dir),
            "explanation": " -> ".join(exp_steps) + f". Final direction is {final_dir}.",
            "difficulty": 2
        }

    def generate_pythagoras_theorem(self):
        """Pattern: Pythagoras theorem"""
        # A person starts from home, walks X east, Y north/left etc.
        # Shortest distance = sqrt(dx^2 + dy^2)
        
        # Pick a pythagorean triplet or clean pair
        triplets = [(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 15, 17), (7, 24, 25), (9, 40, 41), (12, 35, 37)]
        dx, dy, dist = random.choice(triplets)
        
        if random.random() > 0.5: dx, dy = dy, dx
        
        # Decompose dx and dy into segments
        x1 = dx + random.randint(5, 15)
        y1 = dy + random.randint(5, 15)
        x2 = x1 - dx
        y_seg1 = random.randint(1, dy - 1)
        y_seg2 = dy - y_seg1
        
        question = f"Ravi started from his house and walked {x1}m East, then he takes a left turn and walked {y_seg1}m. Then again he takes a left turn and walks {x2}m. He finally takes a right turn and walked {y_seg2}m. What is the shortest distance between his house and the final point?"
        
        correct = f"{dist}m"
        options = [correct]
        while len(options) < 4:
            opt = f"{dist + random.choice([-2, -1, 1, 2, 5])}m"
            if opt not in options:
                options.append(opt)
        random.shuffle(options)
        
        return {
            "question_text": question,
            "options": options,
            "correct_option_index": options.index(correct),
            "explanation": f"Net displacement: East = {x1}-{x2} = {dx}m; North = {y_seg1}+{y_seg2} = {dy}m. Shortest distance = √( {dx}² + {dy}² ) = √({dx**2} + {dy**2}) = √{dx**2 + dy**2} = {dist}m.",
            "difficulty": 3
        }

    def generate_starting_without_direction(self):
        """Pattern: Starting without direction"""
        directions = ["North", "East", "South", "West"]
        
        # Random initial (hidden)
        initial_hidden = random.choice(directions)
        current = initial_hidden
        
        turns = []
        num_turns = random.randint(2, 3)
        for _ in range(num_turns):
            turn = random.choice(["left", "right"])
            turns.append(turn)
            if turn == "left":
                idx = directions.index(current)
                current = directions[(idx - 1) % 4]
            else:
                idx = directions.index(current)
                current = directions[(idx + 1) % 4]
        
        final_facing = current
        
        turn_text = ", ".join(turns[:-1]) + " and then a " + turns[-1] if len(turns) > 1 else turns[0]
        
        question = f"Rakesh starts walking from his house and then takes {turn_text} turn to reach the market. If he is facing {final_facing} on reaching the market, in which direction was Rakesh facing when he started from his house?"
        
        correct = initial_hidden
        options = directions[:]
        random.shuffle(options)
        
        # Explanation: Reversing
        exp_steps = [f"Final facing: {final_facing}"]
        temp_facing = final_facing
        for turn in reversed(turns):
            if turn == "left":
                idx = directions.index(temp_facing)
                temp_facing = directions[(idx + 1) % 4]
                exp_steps.append(f"Reverse Left turn -> Facing {temp_facing}")
            else:
                idx = directions.index(temp_facing)
                temp_facing = directions[(idx - 1) % 4]
                exp_steps.append(f"Reverse Right turn -> Facing {temp_facing}")
        
        return {
            "question_text": question,
            "options": options,
            "correct_option_index": options.index(correct),
            "explanation": " -> ".join(exp_steps) + f". Thus, he started facing {correct}.",
            "difficulty": 3
        }

    def generate_moving_towards_direction(self):
        """Pattern: Moving towards different direction"""
        # Complex movements with multiple turns
        segments = []
        directions = ["North", "East", "South", "West"]
        
        start_dir = random.choice(directions)
        current_dir = start_dir
        
        num_moves = random.randint(3, 5)
        for i in range(num_moves):
            dist = random.randint(10, 100)
            segments.append((current_dir, dist))
            
            # Next turn
            turn = random.choice(["left", "right"])
            if turn == "left":
                current_dir = directions[(directions.index(current_dir) - 1) % 4]
            else:
                current_dir = directions[(directions.index(current_dir) + 1) % 4]
        
        # Final move
        dist = random.randint(10, 100)
        segments.append((current_dir, dist))
        
        question_steps = []
        for i, (d, dist) in enumerate(segments):
            if i == 0:
                question_steps.append(f"walks {dist}m towards {d}")
            else:
                # Describe turn relative to previous
                prev_d = segments[i-1][0]
                turn = "left" if directions[(directions.index(prev_d) - 1) % 4] == d else "right"
                question_steps.append(f"turns {turn} and walks {dist}m")
        
        question = f"Gopal starts from A and " + ", ".join(question_steps) + ". In which direction is he facing now?"
        
        correct = current_dir
        options = directions[:]
        random.shuffle(options)
        
        return {
            "question_text": question,
            "options": options,
            "correct_option_index": options.index(correct),
            "explanation": f"Sequence of moves ends with facing {correct}.",
            "difficulty": 3
        }

    def generate_interchange_direction(self):
        """Pattern: Interchange direction"""
        directions = ["North", "North-East", "East", "South-East", "South", "South-West", "West", "North-West"]
        dir_angles = {d: i * 45 for i, d in enumerate(directions)}
        angles_to_dir = {v: k for k, v in dir_angles.items()}
        
        # Example: If South-East becomes North...
        old_dir = random.choice(directions)
        new_name = random.choice(directions)
        
        rotation = (dir_angles[new_name] - dir_angles[old_dir]) % 360
        
        target_old = random.choice([d for d in directions if d != old_dir])
        target_new_angle = (dir_angles[target_old] + rotation) % 360
        target_new = angles_to_dir[target_new_angle]
        
        question = f"If {old_dir} becomes {new_name}, and {directions[(directions.index(old_dir)+1)%8]} becomes {directions[(dir_angles[new_name]//45 + 1)%8]}, and so on, what will {target_old} become?"
        
        correct = target_new
        distractors = [d for d in directions if d != correct]
        random.shuffle(distractors)
        options = [correct] + distractors[:3]
        random.shuffle(options)
        
        return {
            "question_text": question,
            "options": options,
            "correct_option_index": options.index(correct),
            "explanation": f"The entire direction map is rotated by {rotation}°. {old_dir} ({dir_angles[old_dir]}°) -> {new_name} ({dir_angles[new_name]}°). So {target_old} ({dir_angles[target_old]}°) becomes {(dir_angles[target_old] + rotation)%360}° which is {target_new}.",
            "difficulty": 3
        }

    def generate_find_direction_in_respect_to_another(self):
        """Pattern: Find direction in respect to another one"""
        # Relative positioning of points
        num_points = random.randint(3, 5)
        points = {'A': (0, 0)}
        used_names = ['A']
        avail_names = ['B', 'C', 'D', 'E', 'F']
        
        descriptions = []
        for i in range(num_points - 1):
            p1 = random.choice(used_names)
            p2 = avail_names.pop(0)
            used_names.append(p2)
            
            dist = random.randint(10, 100)
            direction = random.choice(["North", "East", "South", "West"])
            
            x1, y1 = points[p1]
            if direction == "North": points[p2] = (x1, y1 + dist)
            elif direction == "South": points[p2] = (x1, y1 - dist)
            elif direction == "East": points[p2] = (x1 + dist, y1)
            elif direction == "West": points[p2] = (x1 - dist, y1)
            
            descriptions.append(f"{p2} is {dist}m {direction} of {p1}")
        
        # Ask relative position
        p_q = random.choice(used_names)
        p_ref = random.choice([p for p in used_names if p != p_q])
        
        xq, yq = points[p_q]
        xr, yr = points[p_ref]
        
        dx = xq - xr
        dy = yq - yr
        
        if dx == 0 and dy > 0: rel_dir = "North"
        elif dx == 0 and dy < 0: rel_dir = "South"
        elif dx > 0 and dy == 0: rel_dir = "East"
        elif dx < 0 and dy == 0: rel_dir = "West"
        elif dx > 0 and dy > 0: rel_dir = "North-East"
        elif dx > 0 and dy < 0: rel_dir = "South-East"
        elif dx < 0 and dy > 0: rel_dir = "North-West"
        else: rel_dir = "South-West"
        
        question = f"Given the locations: {'. '.join(descriptions)}. Find the position of {p_q} with reference to {p_ref}."
        
        correct = rel_dir
        options = ["North", "South", "East", "West", "North-East", "South-East", "North-West", "South-West"]
        random.shuffle(options)
        options = options[:4]
        if correct not in options:
            options[0] = correct
            random.shuffle(options)
            
        return {
            "question_text": question,
            "options": options,
            "correct_option_index": options.index(correct),
            "explanation": f"Based on the coordinates relative to {p_ref}, {p_q} lies to the {rel_dir}.",
            "difficulty": 4
        }

    def generate_coded_direction(self):
        """Pattern: Coded direction"""
        symbols = {"@": "North", "#": "South", "$": "East", "%": "West"}
        sym_list = list(symbols.keys())
        random.shuffle(sym_list)
        
        # New mapping for this question
        mapping = {s: d for s, d in zip(sym_list, ["North", "South", "East", "West"])}
        code_desc = [f"P {s} Q means P is {d} of Q" for s, d in mapping.items()]
        
        # Scenario: 3 points
        p1, p2, p3 = "A", "B", "C"
        s1 = random.choice(sym_list)
        s2 = random.choice(sym_list)
        
        d1 = random.randint(5, 20)
        d2 = random.randint(5, 20)
        
        question = f"{'. '.join(code_desc)}. If {p1} {s1} {p2} ({d1}m) and {p2} {s2} {p3} ({d2}m), then in which direction is {p1} with respect to {p3}?"
        
        # Calculate relative position
        # P1 is dir1 of P2 -> P1 = P2 + vector(dir1)
        # P2 is dir2 of P3 -> P2 = P3 + vector(dir2)
        # P1 = P3 + vector(dir2) + vector(dir1)
        
        x, y = 0, 0
        dir2 = mapping[s2]
        if dir2 == "North": y += d2
        elif dir2 == "South": y -= d2
        elif dir2 == "East": x += d2
        elif dir2 == "West": x -= d2
        
        dir1 = mapping[s1]
        if dir1 == "North": y += d1
        elif dir1 == "South": y -= d1
        elif dir1 == "East": x += d1
        elif dir1 == "West": x -= d1
        
        # Find direction of (x,y) from (0,0)
        if x == 0 and y > 0: rel = "North"
        elif x == 0 and y < 0: rel = "South"
        elif x > 0 and y == 0: rel = "East"
        elif x < 0 and y == 0: rel = "West"
        elif x > 0 and y > 0: rel = "North-East"
        elif x > 0 and y < 0: rel = "South-East"
        elif x < 0 and y > 0: rel = "North-West"
        else: rel = "South-West"
        
        correct = rel
        options = ["North-East", "South-East", "North-West", "South-West", "North", "South", "East", "West"]
        random.shuffle(options)
        options = options[:4]
        if correct not in options:
            options[0] = correct
            random.shuffle(options)
            
        return {
            "question_text": question,
            "options": options,
            "correct_option_index": options.index(correct),
            "explanation": f"{p2} is {dir2} of {p3}. {p1} is {dir1} of {p2}. Thus {p1} is at ({x}, {y}) relative to {p3}, which is {rel}.",
            "difficulty": 4
        }

    def generate_shadow_based(self):
        """Pattern: Shadow-based questions"""
        times = ["Morning", "Evening"]
        time = random.choice(times)
        
        # Morning: Sun is East, Shadow is West
        # Evening: Sun is West, Shadow is East
        sun_dir = "East" if time == "Morning" else "West"
        shadow_dir = "West" if time == "Morning" else "East"
        
        # Two people A and B are talking face to face.
        # A's shadow falls to the right of B.
        # If shadow is West, and it is to the right of B, then B is facing North.
        # (Facing North -> Right is East, Left is West. Wait. Facing North: Right is East? No.
        # N: L=W, R=E.
        # S: L=E, R=W.
        # So if shadow(West) is to the Right of B, B must be facing South.)
        
        facing_options = ["North", "South", "East", "West"]
        b_facing = random.choice(["North", "South"])
        
        if b_facing == "North":
            # Right is East, Left is West
            rel_side = "Left" if shadow_dir == "West" else "Right"
        else:
            # South: Right is West, Left is East
            rel_side = "Right" if shadow_dir == "West" else "Left"
            
        question = f"One {time}, Amit and Sunil were talking to each other face to face. Amit's shadow fell exactly to the {rel_side} of Sunil. Which direction was Amit facing?"
        
        # If Amit and Sunil are face to face, Amit faces opposite of Sunil.
        amit_facing = "South" if b_facing == "North" else "North"
        
        correct = amit_facing
        options = ["North", "South", "East", "West"]
        random.shuffle(options)
        
        return {
            "question_text": question,
            "options": options,
            "correct_option_index": options.index(correct),
            "explanation": f"In the {time}, the sun is in the {sun_dir}, so shadows fall to the {shadow_dir}. Since the shadow is to the {rel_side} of Sunil, Sunil must be facing {b_facing}. Amit is face-to-face with Sunil, so Amit faces {amit_facing}.",
            "difficulty": 4
        }

    def generate_headstand(self):
        """Pattern: Headstand questions"""
        directions = ["North", "South", "East", "West"]
        facing = random.choice(directions)
        
        # Normal facing:
        # North -> L=West, R=East
        # South -> L=East, R=West
        # East -> L=North, R=South
        # West -> L=South, R=North
        
        # Headstand: Left and Right are SWAPPED relative to normal facing.
        # (A person facing North: Head is down, Feet are up. Eyes still face North.
        # But 'left' hand is now where 'right' used to be?)
        # Let's verify: Stand facing North. Left is West. Now flip upside down but keep facing North.
        # Your left hand is now on the East side.
        
        mapping = {
            "North": {"Left": "East", "Right": "West"},
            "South": {"Left": "West", "Right": "East"},
            "East": {"Left": "South", "Right": "North"},
            "West": {"Left": "North", "Right": "South"}
        }
        
        hand = random.choice(["Left", "Right"])
        correct = mapping[facing][hand]
        
        question = f"A person is performing headstand with his face towards the {facing}. In which direction will his {hand.lower()} hand be?"
        
        options = ["North", "South", "East", "West"]
        random.shuffle(options)
        
        return {
            "question_text": question,
            "options": options,
            "correct_option_index": options.index(correct),
            "explanation": f"When performing a headstand facing {facing}, the left and right positions are reversed compared to normal standing. Normally facing {facing}, the {hand.lower()} hand would be { 'West' if (facing=='North' and hand=='Left') else '...' }. In headstand, it is {correct}.",
            "difficulty": 3
        }

    def generate_final_facing(self):
        """Pattern: Final facing"""
        return self.generate_moving_towards_direction()

    def generate_side_movement(self):
        """Pattern: Side movement"""
        # Walking along edges of a square/rectangle
        l, b = random.randint(10, 50), random.randint(10, 50)
        sides = ["length", "width", "length", "width"]
        question = f"A person walks along the boundary of a rectangular field of {l}m x {b}m. He starts from one corner and walks {l}m along the length, then turns left and walks {b}m, then turns left and walks {l}m. How far and in which direction is he from the starting point?"
        
        correct_dist = f"{b}m"
        # Start at (0,0). Move l East -> (l, 0). Left(North) b -> (l, b). Left(West) l -> (0, b).
        # From (0,0) to (0,b) is b meters North.
        correct_dir = "North"
        
        options = ["North", "South", "East", "West"]
        random.shuffle(options)
        opts = [f"{b}m {d}" for d in options]
        correct = f"{b}m {correct_dir}"
        
        return {
            "question_text": question,
            "options": opts,
            "correct_option_index": opts.index(correct),
            "explanation": f"The path forms three sides of a rectangle. He is now at the last corner, which is {b}m away in the perpendicular direction ({correct_dir}).",
            "difficulty": 2
        }

    def generate_direction_of_smoke(self):
        """Pattern: Direction of smoke"""
        # Train vs Wind
        directions = ["North", "South", "East", "West"]
        train_dir = random.choice(directions)
        wind_dir = random.choice([d for d in directions if d != train_dir])
        
        # Smoke goes opposite to train + with wind.
        # Opposite of North is South. Wind is East. Smoke goes South-East.
        opp = {"North": "South", "South": "North", "East": "West", "West": "East"}
        smoke_vector_1 = opp[train_dir]
        smoke_vector_2 = wind_dir
        
        correct = f"{smoke_vector_1}-{smoke_vector_2}"
        
        question = f"A train is moving towards {train_dir} and the wind is blowing towards {wind_dir}. In which direction will the smoke of the train go?"
        
        options = ["North-East", "South-East", "North-West", "South-West", "North", "South", "East", "West"]
        random.shuffle(options)
        options = options[:4]
        if correct not in options: options[0] = correct
        random.shuffle(options)
        
        return {
            "question_text": question,
            "options": options,
            "correct_option_index": options.index(correct),
            "explanation": f"Smoke is pushed back by the train's motion ({smoke_vector_1}) and carried by the wind ({smoke_vector_2}), resulting in {correct}.",
            "difficulty": 3
        }

    def generate_playing_cards(self):
        """Pattern: Playing cards"""
        # P, Q, R, S playing cards. Partners face each other.
        # P and R are partners, Q and S are partners.
        # S is to the right of P who faces North.
        
        p_facing = "North"
        # P faces North. S is to the right of P. In a circle, 'right' of P (facing North/Center) is East.
        # Wait, if they face center:
        # P(South side, faces North). S(West side, faces East) is to P's left. 
        # R(North side, faces South). Q(East side, faces West) is to P's right.
        # Let's use simple cardinal mapping.
        
        question = f"P, Q, R and S are playing a game of carrom/cards. P and R are partners; S and Q are partners. S is to the right of R who faces West. Which direction is Q facing?"
        
        # R faces West (stands on East side).
        # Partners R and P: P faces East (stands on West side).
        # To the right of R (facing West): Right is North.
        # So S is at North.
        # Partners S and Q: Q is at South.
        # Q faces North.
        
        correct = "North"
        options = ["North", "South", "East", "West"]
        random.shuffle(options)
        
        return {
            "question_text": question,
            "options": options,
            "correct_option_index": options.index(correct),
            "explanation": f"R faces West. R's partner P faces East. To the right of R (West) is North, where S sits. S's partner Q must sit at South, facing North.",
            "difficulty": 4
        }

    def generate_seating_arrangement(self):
        """Pattern: Seating arrangement"""
        # 5 people in a row or circle
        question = "Five boys P, Q, R, S, T are sitting in a row. P is to the right of Q, S is to the left of Q but to the right of R. P is to the left of T. Who is sitting in the middle?"
        # R - S - Q - P - T
        correct = "Q"
        options = ["P", "Q", "R", "S"]
        random.shuffle(options)
        
        return {
            "question_text": question,
            "options": options,
            "correct_option_index": options.index(correct),
            "explanation": "The arrangement from left to right is R, S, Q, P, T. Q is in the center.",
            "difficulty": 3
        }

    def generate_based_on_turns(self):
        """Pattern: Based on turns"""
        return self.generate_moving_towards_direction()

    def generate_one_direction_only(self):
        """Pattern: When only one direction is given"""
        # Traditional logic puzzle
        question = "To reach his school, Rahul goes 5km towards North, then turns left and goes 10km, then turns left again and goes 5km. In which direction is the school from his starting point?"
        # N 5, L(W) 10, L(S) 5 -> Net West 10.
        correct = "West"
        options = ["North", "South", "East", "West"]
        random.shuffle(options)
        return {
            "question_text": question,
            "options": options,
            "correct_option_index": options.index(correct),
            "explanation": "He moved 5km North and 5km South, cancelling the vertical movement. He is 10km West of the start.",
            "difficulty": 2
        }

hybrid_generator = HybridGenerator()
