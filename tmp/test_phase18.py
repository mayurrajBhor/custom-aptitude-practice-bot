import sys
sys.path.append('.')
from llm.hybrid_gen import hybrid_generator
import json

print("=== Testing Percentage Equations ===")
for _ in range(5):
    res = hybrid_generator.generate_percentage_equations()
    print("-", res['question_text'])
    print("  Ans:", res['options'][res['correct_option_index']])

print("\n=== Testing Base Comparisons ===")
for _ in range(5):
    res = hybrid_generator.generate_base_comparisons()
    print("-", res['question_text'])
    print("  Ans:", res['options'][res['correct_option_index']])

print("\n=== Testing Applied Scenarios ===")
for _ in range(5):
    res = hybrid_generator.generate_applied_percentages()
    print("-", res['question_text'])
    print("  Ans:", res['options'][res['correct_option_index']])
