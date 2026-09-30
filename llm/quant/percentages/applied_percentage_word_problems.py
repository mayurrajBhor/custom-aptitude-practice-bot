import math
import random
from fractions import Fraction


class AppliedPercentageWordProblemsMixin:
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
