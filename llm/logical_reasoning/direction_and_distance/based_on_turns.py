import math
import random


class BasedOnTurnsMixin:
    def generate_based_on_turns(self):
        """Pattern: Based on turns"""
        return self.generate_moving_towards_direction()
