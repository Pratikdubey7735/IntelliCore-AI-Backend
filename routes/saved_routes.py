from fastapi import APIRouter, Depends
from pydantic import BaseModel
from auth.auth_bearer import JWTBearer
from db.db_connection import get_connection

router = APIRouter()

class SaveQueryRequest(BaseModel):
    label: str
    question: str
    table_used: str
    sql_generated: str

@router.post("/saved")
def save_query(data: SaveQueryRequest, token: dict = Depends(JWTBearer())):
    user_id = token.get("id")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO saved_queries (user_id, label, question, table_used, sql_generated)
        VALUES (%s, %s, %s, %s, %s)
    """, (user_id, data.label, data.question, data.table_used, data.sql_generated))
    conn.commit()
    cur.close()
    conn.close()
    return {"message": "Query saved successfully"}

@router.get("/saved")
def get_saved(token: dict = Depends(JWTBearer())):
    user_id = token.get("id")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, label, question, table_used, sql_generated, created_at
        FROM saved_queries WHERE user_id = %s
        ORDER BY created_at DESC
    """, (user_id,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [
        {
            "id": r[0],
            "label": r[1],
            "question": r[2],
            "table_used": r[3],
            "sql_generated": r[4],
            "created_at": str(r[5])
        }
        for r in rows
    ]

@router.delete("/saved/{id}")
def delete_saved(id: int, token: dict = Depends(JWTBearer())):
    user_id = token.get("id")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM saved_queries WHERE id = %s AND user_id = %s", (id, user_id))
    conn.commit()
    cur.close()
    conn.close()
    return {"message": "Deleted successfully"}