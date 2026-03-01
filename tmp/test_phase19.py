import sys
sys.path.append('.')
from llm.hybrid_gen import hybrid_generator

print("=== Testing Alligation & Shifts ===")
for _ in range(5):
    res = hybrid_generator.generate_alligation_shifts()
    print("-", res['question_text'])
    print("  Ans:", res['options'][res['correct_option_index']])
    print("  Exp:", res['explanation'])
    print()
