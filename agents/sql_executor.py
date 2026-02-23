from db.db_connection import get_connection

def execute_sql(sql: str) -> dict:
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]

        # Limit to 50 rows to avoid context overflow
        limited_rows = rows[:50]

        result = []
        for row in limited_rows:
            result.append(dict(zip(columns, row)))

        cur.close()
        return {
            "success": True,
            "data": result,
            "row_count": len(rows),
            "columns": columns
        }

    except Exception as e:
        return {
            "success": False,
            "data": [],
            "row_count": 0,
            "error": str(e)
        }
    finally:
        if conn:
            conn.close()