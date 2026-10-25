import math
import random


class InterchangeDirectionMixin:
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
