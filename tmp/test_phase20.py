import sys
sys.path.append('.')
from llm.hybrid_gen import hybrid_generator

print("=== Testing Percentage Comparisons ===")
for _ in range(5):
    res = hybrid_generator.generate_percentage_comparisons()
    print("Q:", res['question_text'][:120])
    print("Ans:", res['options'][res['correct_option_index']])
    print()

print("=== Testing Percentage Calculations ===")
for _ in range(5):
    res = hybrid_generator.generate_percentage_calculations()
    print("Q:", res['question_text'][:120])
    print("Ans:", res['options'][res['correct_option_index']])
    print()
