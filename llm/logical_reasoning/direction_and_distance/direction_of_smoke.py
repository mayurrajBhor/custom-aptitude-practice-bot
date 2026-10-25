import math
import random


class DirectionOfSmokeMixin:
    def generate_direction_of_smoke(self):
        """Pattern: Direction of smoke"""
        # Train vs Wind
        directions = ["North", "South", "East", "West"]
        train_dir = random.choice(directions)
        wind_dir = random.choice([d for d in directions if d != train_dir])
        
        # Smoke goes opposite to train + with wind.
        # Opposite of North is South. Wind is East. Smoke goes South-East.
        opp = {"North": "South", "South": "North", "East": "West", "West": "East"}
        smoke_vector_1 = opp[train_dir]
        smoke_vector_2 = wind_dir
        
        correct = f"{smoke_vector_1}-{smoke_vector_2}"
        
        question = f"A train is moving towards {train_dir} and the wind is blowing towards {wind_dir}. In which direction will the smoke of the train go?"
        
        options = ["North-East", "South-East", "North-West", "South-West", "North", "South", "East", "West"]
        random.shuffle(options)
        options = options[:4]
        if correct not in options: options[0] = correct
        random.shuffle(options)
        
        return {
            "question_text": question,
            "options": options,
            "correct_option_index": options.index(correct),
            "explanation": f"Smoke is pushed back by the train's motion ({smoke_vector_1}) and carried by the wind ({smoke_vector_2}), resulting in {correct}.",
            "difficulty": 3
        }
