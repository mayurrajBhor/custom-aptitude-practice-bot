import sys
sys.path.append('.')
from llm.hybrid_gen import hybrid_generator

print("=== Testing Income Expenditure ===")
for _ in range(3):
    res = hybrid_generator.generate_income_expenditure()
    print("Q:", res['question_text'][:120])
    print("Ans:", res['options'][res['correct_option_index']])
    print()

print("=== Testing Pass Fail ===")
for _ in range(3):
    res = hybrid_generator.generate_pass_fail_aggregates()
    print("Q:", res['question_text'][:120])
    print("Ans:", res['options'][res['correct_option_index']])
    print()
