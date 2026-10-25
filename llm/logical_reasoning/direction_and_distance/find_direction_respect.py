import math
import random


class FindDirectionRespectMixin:
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
