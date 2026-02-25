from llm.generator import generator

def test_hybrid():
    print("--- Testing Hybrid Dispatcher ---")
    
    # Test 1: Mixed Fraction
    res, err = generator.generate_mcq("Quant", "Mix fraction", "Desc", 2)
    print(f"\nMixed Fraction Test:\nQ: {res['question_text']}\nOptions: {res['options']}\nExplanation: {res['explanation']}")
    
    # Test 2: Fraction Subtraction
    res, err = generator.generate_mcq("Quant", "Fraction subtraction", "Desc", 3)
    print(f"\nFraction Subtraction Test:\nQ: {res['question_text']}\nOptions: {res['options']}\nExplanation: {res['explanation']}")
    
    # Test 3: Batch Generation (Mixed)
    patterns = [
        {"id": 1, "topic_name": "Quant", "name": "Mix fraction", "description": "desc", "difficulty": 2},
        {"id": 2, "topic_name": "Quant", "name": "Fraction subtraction", "description": "desc", "difficulty": 3},
        {"id": 3, "topic_name": "Quant", "name": "Per to fraction and vice versa", "description": "desc", "difficulty": 2},
        {"id": 4, "topic_name": "Quant", "name": "basic fraction to per", "description": "desc", "difficulty": 2}
    ]
    
    print("\n--- Testing Batch Despatch ---")
    results, err = generator.generate_batch(patterns, count=4)
    if err:
        print(f"Batch Error: {err}")
    
    for r in results:
        p_id = r.get('pattern_id')
        q_text = r.get('question_text')
        # Check if it's Hybrid or AI based on explanation brevity (hybrid has fixed explanations)
        source = "HYBRID" if "Memory" in r['explanation'] or "Divided by" in r['explanation'] or "find a common" in r['explanation'] else "AI"
        print(f"Pattern {p_id} ({source}): {q_text[:100]}...")

if __name__ == "__main__":
    test_hybrid()
