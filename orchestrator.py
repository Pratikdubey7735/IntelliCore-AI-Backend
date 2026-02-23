import time
from agents.intent_agent import classify_intent
from agents.table_selection_agent import select_table
from agents.column_selection_agent import select_columns
from agents.pseudo_code_agent import generate_pseudo_code
from agents.sql_agent import generate_sql
from agents.sql_executor import execute_sql
from agents.final_answer_agent import generate_final_answer

def run_pipeline(user_question: str, user_id: int = None) -> dict:
    
    start_time = time.time()
    steps = []

    try:
        # Step 1 - Intent
        intent_result = classify_intent(user_question)
        steps.append({"step": "intent", "status": "done", "result": intent_result})

        if intent_result["intent"] == "unknown":
            return {
                "success": False,
                "question": user_question,
                "answer": "I'm sorry, I don't have data to answer this question. Please ask something related to Students, Cricket players, or Employees.",
                "steps": steps,
                "sql": None,
                "data": [],
                "columns": [],
                "row_count": 0,
                "time_taken_ms": int((time.time() - start_time) * 1000)
            }

        # Step 2 - Table Selection
        table_result = select_table(user_question, intent_result["intent"])
        steps.append({"step": "table_selection", "status": "done", "result": table_result})

        if table_result["table"] == "none":
            return {
                "success": False,
                "question": user_question,
                "answer": "I could not identify which data table to use for your question. Please rephrase your question.",
                "steps": steps,
                "sql": None,
                "data": [],
                "columns": [],
                "row_count": 0,
                "time_taken_ms": int((time.time() - start_time) * 1000)
            }

        # Step 3 - Column Selection
        column_result = select_columns(user_question, intent_result["intent"], table_result["table"])
        steps.append({"step": "column_selection", "status": "done", "result": column_result})

        # Step 4 - Pseudo Code
        pseudo_result = generate_pseudo_code(user_question, intent_result["intent"], table_result["table"], column_result)
        steps.append({"step": "pseudo_code", "status": "done", "result": pseudo_result})

        # Step 5 - SQL Generation
        sql_result = generate_sql(user_question, intent_result["intent"], table_result["table"], column_result, pseudo_result)
        steps.append({"step": "sql_generation", "status": "done", "result": sql_result})

        if not sql_result["sql"]:
            return {
                "success": False,
                "question": user_question,
                "answer": "I was unable to generate a valid SQL query for your question. Please try rephrasing.",
                "steps": steps,
                "sql": None,
                "data": [],
                "columns": [],
                "row_count": 0,
                "time_taken_ms": int((time.time() - start_time) * 1000)
            }

        # Step 6 - Execute SQL
        execution_result = execute_sql(sql_result["sql"])
        steps.append({"step": "sql_execution", "status": "done", "result": {"row_count": execution_result["row_count"], "success": execution_result["success"]}})

        # Step 7 - Final Answer
        final_answer = generate_final_answer(user_question, execution_result)
        steps.append({"step": "final_answer", "status": "done"})

        time_taken = int((time.time() - start_time) * 1000)

        return {
            "success": execution_result["success"],
            "question": user_question,
            "answer": final_answer,
            "steps": steps,
            "sql": sql_result["sql"],
            "data": execution_result["data"],
            "columns": execution_result.get("columns", []),
            "row_count": execution_result["row_count"],
            "intent": intent_result["intent"],
            "table_used": table_result["table"],
            "time_taken_ms": time_taken
        }

    except Exception as e:
        return {
            "success": False,
            "question": user_question,
            "answer": f"An unexpected error occurred: {str(e)}",
            "steps": steps,
            "sql": None,
            "data": [],
            "columns": [],
            "row_count": 0,
            "time_taken_ms": int((time.time() - start_time) * 1000)
        }