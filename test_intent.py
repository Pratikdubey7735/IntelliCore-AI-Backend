from agents.intent_agent import classify_intent

questions = [
    "Who scored the highest marks in Python?",
    "What is the average salary in R&D department?",
    "Show top 5 cricket players by runs",
    "How many employees are in the Sales department?",
    "What is the weather today?"
]

for q in questions:
    print(f"\nQuestion: {q}")
    result = classify_intent(q)
    print(f"Result: {result}")