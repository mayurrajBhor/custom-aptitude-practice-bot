import math
import random
from fractions import Fraction


class PercentageCalculationTricksMixin:
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
