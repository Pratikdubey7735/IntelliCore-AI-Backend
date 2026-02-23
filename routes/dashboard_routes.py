from fastapi import APIRouter, Depends, HTTPException
from auth.auth_bearer import JWTBearer
from db.db_connection import get_connection

router = APIRouter()

@router.get("/dashboard/stats")
def get_dashboard_stats(token: dict = Depends(JWTBearer())):
    user_id = token.get("id")
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM query_logs WHERE user_id = %s", (user_id,))
    total_queries = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM query_logs WHERE user_id = %s AND DATE(created_at) = CURRENT_DATE", (user_id,))
    queries_today = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM saved_queries WHERE user_id = %s", (user_id,))
    saved_queries = cur.fetchone()[0]

    cur.execute("""
        SELECT table_used, COUNT(*) as cnt 
        FROM query_logs 
        WHERE user_id = %s AND table_used IS NOT NULL
        GROUP BY table_used 
        ORDER BY cnt DESC 
        LIMIT 1
    """, (user_id,))
    most_queried = cur.fetchone()
    most_queried_table = most_queried[0] if most_queried else "N/A"

    cur.execute("""
        SELECT table_used, COUNT(*) as cnt
        FROM query_logs
        WHERE user_id = %s 
        AND table_used IS NOT NULL
        AND created_at >= CURRENT_DATE - INTERVAL '7 days'
        GROUP BY table_used
    """, (user_id,))
    table_distribution = [{"table": r[0], "count": r[1]} for r in cur.fetchall()]

    cur.execute("""
        SELECT intent, COUNT(*) as cnt
        FROM query_logs
        WHERE user_id = %s AND intent IS NOT NULL
        GROUP BY intent
    """, (user_id,))
    intent_distribution = [{"intent": r[0], "count": r[1]} for r in cur.fetchall()]

    cur.execute("""
        SELECT question, table_used, intent, status, time_taken_ms, created_at
        FROM query_logs
        WHERE user_id = %s
        ORDER BY created_at DESC
        LIMIT 5
    """, (user_id,))
    recent = cur.fetchall()
    recent_queries = [
        {
            "question": r[0],
            "table_used": r[1],
            "intent": r[2],
            "status": r[3],
            "time_taken_ms": r[4],
            "created_at": str(r[5])
        }
        for r in recent
    ]

    cur.close()
    conn.close()

    return {
        "total_queries": total_queries,
        "queries_today": queries_today,
        "saved_queries": saved_queries,
        "most_queried_table": most_queried_table,
        "table_distribution": table_distribution,
        "intent_distribution": intent_distribution,
        "recent_queries": recent_queries
    }


@router.get("/admin/users")
def get_all_users(token: dict = Depends(JWTBearer())):
    if token.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT u.id, u.name, u.email, u.role, u.is_active, u.created_at,
               COUNT(q.id) as query_count
        FROM users u
        LEFT JOIN query_logs q ON q.user_id = u.id
        GROUP BY u.id, u.name, u.email, u.role, u.is_active, u.created_at
        ORDER BY u.created_at DESC
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [
        {
            "id": r[0],
            "name": r[1],
            "email": r[2],
            "role": r[3],
            "is_active": r[4],
            "created_at": str(r[5]),
            "query_count": r[6]
        }
        for r in rows
    ]


@router.put("/admin/users/{user_id}/role")
def update_user_role(user_id: int, token: dict = Depends(JWTBearer())):
    if token.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT role FROM users WHERE id = %s", (user_id,))
    user = cur.fetchone()
    new_role = "admin" if user[0] == "user" else "user"
    cur.execute("UPDATE users SET role = %s WHERE id = %s", (new_role, user_id))
    conn.commit()
    cur.close()
    conn.close()
    return {"message": f"Role updated to {new_role}"}

@router.get("/data-profile/{table_name}")
def get_data_profile(table_name: str, token: dict = Depends(JWTBearer())):
    if table_name not in ["student", "cricket", "employee"]:
        raise HTTPException(status_code=400, detail="Invalid table name")

    conn = get_connection()
    cur = conn.cursor()

    # Row count
    cur.execute(f"SELECT COUNT(*) FROM {table_name}")
    row_count = cur.fetchone()[0]

    # Column info
    cur.execute("""
        SELECT column_name, data_type 
        FROM information_schema.columns 
        WHERE table_name = %s
        ORDER BY ordinal_position
    """, (table_name,))
    columns = cur.fetchall()

    profile = []
    for col_name, data_type in columns:
        col_info = {
            "column": col_name,
            "type": data_type
        }

        if data_type in ("integer", "numeric", "double precision", "real"):
            cur.execute(f"""
                SELECT 
                    MIN({col_name}),
                    MAX({col_name}),
                    ROUND(AVG({col_name})::numeric, 2)
                FROM {table_name}
            """)
            stats = cur.fetchone()
            col_info["min"] = stats[0]
            col_info["max"] = stats[1]
            col_info["avg"] = float(stats[2]) if stats[2] else None

        else:
            cur.execute(f"""
                SELECT {col_name}, COUNT(*) as cnt
                FROM {table_name}
                WHERE {col_name} IS NOT NULL AND {col_name} != ''
                GROUP BY {col_name}
                ORDER BY cnt DESC
                LIMIT 5
            """)
            top_values = cur.fetchall()
            col_info["top_values"] = [{"value": r[0], "count": r[1]} for r in top_values]

        profile.append(col_info)

    cur.close()
    conn.close()

    return {
        "table": table_name,
        "row_count": row_count,
        "column_count": len(columns),
        "profile": profile
    }

@router.get("/report")
def generate_report(token: dict = Depends(JWTBearer())):
    conn = get_connection()
    cur = conn.cursor()

    report = {}

    # Student Stats
    cur.execute("SELECT COUNT(*) FROM student")
    report["student_total"] = cur.fetchone()[0]

    cur.execute("""
        SELECT student_name, python FROM student 
        ORDER BY python DESC LIMIT 3
    """)
    report["top_python_students"] = [
        {"name": r[0], "marks": r[1]} for r in cur.fetchall()
    ]

    cur.execute("""
        SELECT ROUND(AVG(python)::numeric,2), ROUND(AVG(data_structures)::numeric,2),
               ROUND(AVG(c)::numeric,2), ROUND(AVG(software_engineering)::numeric,2),
               ROUND(AVG(coa)::numeric,2)
        FROM student
    """)
    avgs = cur.fetchone()
    report["subject_averages"] = [
        {"subject": "Python", "avg": float(avgs[0])},
        {"subject": "Data Structures", "avg": float(avgs[1])},
        {"subject": "C", "avg": float(avgs[2])},
        {"subject": "Software Eng", "avg": float(avgs[3])},
        {"subject": "COA", "avg": float(avgs[4])},
    ]

    # Cricket Stats
    cur.execute("""
        SELECT player_name, runs FROM cricket
        WHERE runs ~ '^[0-9]+$'
        ORDER BY CAST(runs AS INTEGER) DESC LIMIT 5
    """)
    report["top_run_scorers"] = [
        {"player": r[0], "runs": r[1]} for r in cur.fetchall()
    ]

    cur.execute("""
        SELECT player_name, hundreds FROM cricket
        WHERE hundreds ~ '^[0-9]+$'
        ORDER BY CAST(hundreds AS INTEGER) DESC LIMIT 5
    """)
    report["top_century_scorers"] = [
        {"player": r[0], "hundreds": r[1]} for r in cur.fetchall()
    ]

    # Employee Stats
    cur.execute("""
        SELECT department, ROUND(AVG(monthly_income)::numeric, 2) as avg_salary
        FROM employee
        GROUP BY department
        ORDER BY avg_salary DESC
    """)
    report["dept_salaries"] = [
        {"department": r[0], "avg_salary": float(r[1])} for r in cur.fetchall()
    ]

    cur.execute("""
        SELECT education, COUNT(*) as count
        FROM employee
        GROUP BY education
        ORDER BY count DESC
    """)
    report["education_distribution"] = [
        {"education": r[0], "count": r[1]} for r in cur.fetchall()
    ]

    cur.execute("""
        SELECT ROUND(AVG(monthly_income)::numeric,2),
               ROUND(AVG(years_of_experience)::numeric,2),
               ROUND(AVG(performance_rating)::numeric,2)
        FROM employee
    """)
    emp_avgs = cur.fetchone()
    report["employee_averages"] = {
        "avg_salary": float(emp_avgs[0]),
        "avg_experience": float(emp_avgs[1]),
        "avg_performance": float(emp_avgs[2])
    }

    cur.close()
    conn.close()
    return report