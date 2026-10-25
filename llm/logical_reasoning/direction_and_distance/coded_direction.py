import math
import random


class CodedDirectionMixin:
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
