from fastapi import APIRouter, Depends
from auth.auth_bearer import JWTBearer
from db.db_connection import get_connection

router = APIRouter()

@router.get("/history")
def get_history(token: dict = Depends(JWTBearer())):
    user_id = token.get("id")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, question, intent, table_used, sql_generated, 
               result_count, time_taken_ms, status, created_at
        FROM query_logs 
        WHERE user_id = %s
        ORDER BY created_at DESC
    """, (user_id,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [
        {
            "id": r[0],
            "question": r[1],
            "intent": r[2],
            "table_used": r[3],
            "sql_generated": r[4],
            "result_count": r[5],
            "time_taken_ms": r[6],
            "status": r[7],
            "created_at": str(r[8])
        }
        for r in rows
    ]