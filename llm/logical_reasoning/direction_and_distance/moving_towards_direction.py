import math
import random


class MovingTowardsDirectionMixin:
    def generate_moving_towards_direction(self):
        """Pattern: Moving towards different direction"""
        # Complex movements with multiple turns
        segments = []
        directions = ["North", "East", "South", "West"]
        
        start_dir = random.choice(directions)
        current_dir = start_dir
        
        num_moves = random.randint(3, 5)
        for i in range(num_moves):
            dist = random.randint(10, 100)
            segments.append((current_dir, dist))
            
            # Next turn
            turn = random.choice(["left", "right"])
            if turn == "left":
                current_dir = directions[(directions.index(current_dir) - 1) % 4]
            else:
                current_dir = directions[(directions.index(current_dir) + 1) % 4]
        
        # Final move
        dist = random.randint(10, 100)
        segments.append((current_dir, dist))
        
        question_steps = []
        for i, (d, dist) in enumerate(segments):
            if i == 0:
                question_steps.append(f"walks {dist}m towards {d}")
            else:
                # Describe turn relative to previous
                prev_d = segments[i-1][0]
                turn = "left" if directions[(directions.index(prev_d) - 1) % 4] == d else "right"
                question_steps.append(f"turns {turn} and walks {dist}m")
        
        question = f"Gopal starts from A and " + ", ".join(question_steps) + ". In which direction is he facing now?"
        
        correct = current_dir
        options = directions[:]
        random.shuffle(options)
        
        return {
            "question_text": question,
            "options": options,
            "correct_option_index": options.index(correct),
            "explanation": f"Sequence of moves ends with facing {correct}.",
            "difficulty": 3
        }

    def generate_final_facing(self):
        """Pattern: Final facing"""
        return self.generate_moving_towards_direction()
