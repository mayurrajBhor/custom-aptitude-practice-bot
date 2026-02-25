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
        while len(options) < 5:
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
        while len(options) < 5:
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
        while len(options) < 5:
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
        while len(options) < 5:
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

hybrid_generator = HybridGenerator()
