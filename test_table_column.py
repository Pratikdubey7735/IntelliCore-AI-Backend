from agents.intent_agent import classify_intent
from agents.table_selection_agent import select_table
from agents.column_selection_agent import select_columns

questions = [
    "Who scored the highest marks in Python?",
    "What is the average salary in R&D department?",
    "Show top 5 cricket players by runs"
]

for q in questions:
    print(f"\n{'='*60}")
    print(f"Question: {q}")
    
    intent_result = classify_intent(q)
    print(f"Intent: {intent_result['intent']}")
    
    table_result = select_table(q, intent_result['intent'])
    print(f"Table: {table_result['table']}")
    
    column_result = select_columns(q, intent_result['intent'], table_result['table'])
    print(f"Columns: {column_result}")