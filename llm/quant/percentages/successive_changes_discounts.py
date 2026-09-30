import math
import random


class SuccessiveChangesDiscountsMixin:
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
