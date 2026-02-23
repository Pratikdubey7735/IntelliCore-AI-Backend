from fastapi import APIRouter, Depends
from pydantic import BaseModel
from auth.auth_bearer import JWTBearer
from orchestrator import run_pipeline
from db.db_connection import get_connection

router = APIRouter()

class QueryRequest(BaseModel):
    question: str

@router.post("/query")
def handle_query(data: QueryRequest, token: dict = Depends(JWTBearer())):
    user_id = token.get("id")
    result = run_pipeline(data.question, user_id)

    # Log to query_logs table
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO query_logs 
            (user_id, question, intent, table_used, sql_generated, result_count, time_taken_ms, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            user_id,
            data.question,
            result.get("intent"),
            result.get("table_used"),
            result.get("sql"),
            result.get("row_count"),
            result.get("time_taken_ms"),
            "success" if result["success"] else "failed"
        ))
        conn.commit()
        cur.close()
        conn.close()
    except Exception:
        pass

    return result

import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class ExplainRequest(BaseModel):
    sql: str

@router.post("/explain-sql")
def explain_sql(data: ExplainRequest, token: dict = Depends(JWTBearer())):
    prompt = f"""You are a SQL teacher explaining queries to beginners.

Explain this SQL query line by line in very simple plain English.
For each line or clause, explain what it does in one sentence.
Format your response as a numbered list.
Do not use technical jargon. Keep it simple and friendly.

SQL Query:
{data.sql}"""

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    return {"explanation": response.choices[0].message.content}