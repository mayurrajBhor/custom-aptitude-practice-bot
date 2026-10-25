import math
import random
from fractions import Fraction


class MixturesAlligationShiftsMixin:
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
