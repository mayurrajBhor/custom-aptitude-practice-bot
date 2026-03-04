import sys
sys.path.append('.')
from llm.hybrid_gen import hybrid_generator

print("=== Testing Exam Scoring ===")
for _ in range(5):
    res = hybrid_generator.generate_exam_scoring()
    print("Q:", res['question_text'][:120])
    print("Ans:", res['options'][res['correct_option_index']])
    print()

print("=== Testing Successive Changes ===")
for _ in range(5):
    res = hybrid_generator.generate_successive_net_change()
    print("Q:", res['question_text'][:120])
    print("Ans:", res['options'][res['correct_option_index']])
    print()
