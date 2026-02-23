from agents.intent_agent import classify_intent
from agents.table_selection_agent import select_table
from agents.column_selection_agent import select_columns
from agents.pseudo_code_agent import generate_pseudo_code
from agents.sql_agent import generate_sql
from agents.sql_executor import execute_sql
from agents.final_answer_agent import generate_final_answer

questions = [
    "Who scored the highest marks in Python?",
    "Which department has the highest average salary?",
    "Show top 5 cricket players by runs"
]

for q in questions:
    print(f"\n{'='*60}")
    print(f"Question: {q}")

    intent_result = classify_intent(q)
    print(f"1. Intent: {intent_result['intent']}")

    table_result = select_table(q, intent_result['intent'])
    print(f"2. Table: {table_result['table']}")

    column_result = select_columns(q, intent_result['intent'], table_result['table'])
    print(f"3. Columns: {column_result}")

    pseudo_result = generate_pseudo_code(q, intent_result['intent'], table_result['table'], column_result)
    print(f"4. Pseudo Code: {pseudo_result['pseudo_code']}")

    sql_result = generate_sql(q, intent_result['intent'], table_result['table'], column_result, pseudo_result)
    print(f"5. SQL: {sql_result['sql']}")

    execution_result = execute_sql(sql_result['sql'])
    print(f"6. Execution Success: {execution_result['success']}")
    print(f"   Rows returned: {execution_result['row_count']}")

    final_answer = generate_final_answer(q, execution_result)
    print(f"7. Final Answer: {final_answer}")