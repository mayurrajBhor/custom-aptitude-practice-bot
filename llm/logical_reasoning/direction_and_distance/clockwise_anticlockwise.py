import math
import random


class ClockwiseAnticlockwiseMixin:
    def generate_clockwise_anticlockwise(self):
        """Pattern: Clockwise and anti clockwise"""
        directions = ["North", "North-East", "East", "South-East", "South", "South-West", "West", "North-West"]
        dir_angles = {d: i * 45 for i, d in enumerate(directions)}
        angles_to_dir = {v: k for k, v in dir_angles.items()}
        
        start_dir = random.choice(directions)
        current_angle = dir_angles[start_dir]
        
        # Scenario: Facing X, turns A cw, then B acw, etc.
        num_turns = random.randint(2, 3)
        turns = []
        for _ in range(num_turns):
            angle = random.choice([45, 90, 135, 180, 225, 270])
            is_clockwise = random.random() > 0.5
            turns.append((angle, is_clockwise))
            if is_clockwise:
                current_angle = (current_angle + angle) % 360
            else:
                current_angle = (current_angle - angle) % 360
        
        final_dir = angles_to_dir[current_angle]
        
        turn_texts = []
        for angle, cw in turns:
            turn_texts.append(f"{angle}° {'clockwise' if cw else 'anti-clockwise'}")
        
        question = f"Facing {start_dir}, a person turns {' and then '.join(turn_texts)}. What direction is the person facing now?"
        
        options = [final_dir]
        while len(options) < 4:
            opt = random.choice(directions)
            if opt not in options:
                options.append(opt)
        
        random.shuffle(options)
        
        # Simple explanation
        exp_steps = [f"Initial: {start_dir} ({dir_angles[start_dir]}°)"]
        temp_angle = dir_angles[start_dir]
        for angle, cw in turns:
            change = angle if cw else -angle
            temp_angle = (temp_angle + change) % 360
            dir_now = angles_to_dir[temp_angle]
            exp_steps.append(f"Turn {angle}° {'CW' if cw else 'ACW'} -> {dir_now} ({temp_angle}°)")
            
        return {
            "question_text": question,
            "options": options,
            "correct_option_index": options.index(final_dir),
            "explanation": " -> ".join(exp_steps) + f". Final direction is {final_dir}.",
            "difficulty": 2
        }
