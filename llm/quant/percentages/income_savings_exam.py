import math
import random
from fractions import Fraction


class IncomeSavingsExamMixin:
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
