import math
import random


class StartingWithoutDirectionMixin:
    def generate_starting_without_direction(self):
        """Pattern: Starting without direction"""
        directions = ["North", "East", "South", "West"]
        
        # Random initial (hidden)
        initial_hidden = random.choice(directions)
        current = initial_hidden
        
        turns = []
        num_turns = random.randint(2, 3)
        for _ in range(num_turns):
            turn = random.choice(["left", "right"])
            turns.append(turn)
            if turn == "left":
                idx = directions.index(current)
                current = directions[(idx - 1) % 4]
            else:
                idx = directions.index(current)
                current = directions[(idx + 1) % 4]
        
        final_facing = current
        
        turn_text = ", ".join(turns[:-1]) + " and then a " + turns[-1] if len(turns) > 1 else turns[0]
        
        question = f"Rakesh starts walking from his house and then takes {turn_text} turn to reach the market. If he is facing {final_facing} on reaching the market, in which direction was Rakesh facing when he started from his house?"
        
        correct = initial_hidden
        options = directions[:]
        random.shuffle(options)
        
        # Explanation: Reversing
        exp_steps = [f"Final facing: {final_facing}"]
        temp_facing = final_facing
        for turn in reversed(turns):
            if turn == "left":
                idx = directions.index(temp_facing)
                temp_facing = directions[(idx + 1) % 4]
                exp_steps.append(f"Reverse Left turn -> Facing {temp_facing}")
            else:
                idx = directions.index(temp_facing)
                temp_facing = directions[(idx - 1) % 4]
                exp_steps.append(f"Reverse Right turn -> Facing {temp_facing}")
        
        return {
            "question_text": question,
            "options": options,
            "correct_option_index": options.index(correct),
            "explanation": " -> ".join(exp_steps) + f". Thus, he started facing {correct}.",
            "difficulty": 3
        }
