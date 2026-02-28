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

hybrid_generator = HybridGenerator()
