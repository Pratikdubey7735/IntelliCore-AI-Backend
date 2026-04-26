from fastapi import APIRouter, Depends, HTTPException
from auth.auth_bearer import JWTBearer
from db.db_connection import get_connection
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

def is_admin(token: dict = Depends(JWTBearer())):
    if token.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return token

# ─────────────────────────────────────────────
# BROADCAST ANNOUNCEMENT
# ─────────────────────────────────────────────
class AnnouncementRequest(BaseModel):
    message: str
    type: str = "info"

@router.post("/admin/announcement")
def set_announcement(data: AnnouncementRequest, token: dict = Depends(is_admin)):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS announcements (
            id SERIAL PRIMARY KEY,
            message TEXT NOT NULL,
            type VARCHAR(20) DEFAULT 'info',
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT NOW()
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS announcement_reads (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL,
            announcement_id INTEGER NOT NULL,
            UNIQUE(user_id, announcement_id)
        )
    """)
    cur.execute("UPDATE announcements SET is_active = FALSE")
    cur.execute("""
        INSERT INTO announcements (message, type, is_active)
        VALUES (%s, %s, TRUE) RETURNING id
    """, (data.message, data.type))
    conn.commit()
    cur.close()
    conn.close()
    return {"message": "Announcement broadcasted"}

@router.get("/announcement")
def get_announcement(token: dict = Depends(JWTBearer())):
    # Support both "user_id" and "id" key in token
    user_id = token.get("user_id") or token.get("id")
    role = token.get("role")

    # Admin never gets announcements
    if role == "admin":
        return {"message": None, "id": None, "type": "info", "unread": False}

    if not user_id:
        return {"message": None, "id": None, "type": "info", "unread": False}

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS announcements (
                id SERIAL PRIMARY KEY,
                message TEXT NOT NULL,
                type VARCHAR(20) DEFAULT 'info',
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT NOW()
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS announcement_reads (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL,
                announcement_id INTEGER NOT NULL,
                UNIQUE(user_id, announcement_id)
            )
        """)
        conn.commit()

        cur.execute("""
            SELECT id, message, type FROM announcements
            WHERE is_active = TRUE
            ORDER BY created_at DESC LIMIT 1
        """)
        row = cur.fetchone()
        if not row:
            return {"message": None, "id": None, "type": "info", "unread": False}

        ann_id, message, ann_type = row

        cur.execute("""
            SELECT id FROM announcement_reads
            WHERE user_id = %s AND announcement_id = %s
        """, (user_id, ann_id))
        already_read = cur.fetchone() is not None

        return {
            "id": ann_id,
            "message": message,
            "type": ann_type,
            "unread": not already_read
        }
    except Exception as e:
        print(f"Announcement error: {e}")
        return {"message": None, "id": None, "type": "info", "unread": False}
    finally:
        cur.close()
        conn.close()


@router.post("/announcement/{ann_id}/read")
def mark_announcement_read(ann_id: int, token: dict = Depends(JWTBearer())):
    user_id = token.get("user_id") or token.get("id")
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID missing from token")

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO announcement_reads (user_id, announcement_id)
            VALUES (%s, %s)
            ON CONFLICT (user_id, announcement_id) DO NOTHING
        """, (user_id, ann_id))
        conn.commit()
        return {"message": "Marked as read"}
    except Exception as e:
        print(f"Mark read error: {e}")
        raise HTTPException(status_code=500, detail="Failed to mark as read")
    finally:
        cur.close()
        conn.close()
        
@router.delete("/admin/announcement")
def clear_announcement(token: dict = Depends(is_admin)):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE announcements SET is_active = FALSE")
    conn.commit()
    cur.close()
    conn.close()
    return {"message": "Cleared"}
# ─────────────────────────────────────────────
# SYSTEM ANALYTICS DASHBOARD
# ─────────────────────────────────────────────

@router.get("/admin/analytics")
def get_system_analytics(token: dict = Depends(is_admin)):
    conn = get_connection()
    cur = conn.cursor()

    # Total users
    cur.execute("SELECT COUNT(*) FROM users")
    total_users = cur.fetchone()[0]

    # New users today
    cur.execute("SELECT COUNT(*) FROM users WHERE DATE(created_at) = CURRENT_DATE")
    users_today = cur.fetchone()[0]

    # Total queries
    cur.execute("SELECT COUNT(*) FROM query_logs")
    total_queries = cur.fetchone()[0]

    # Queries today
    cur.execute("SELECT COUNT(*) FROM query_logs WHERE DATE(created_at) = CURRENT_DATE")
    queries_today = cur.fetchone()[0]

    # Success vs failure
    cur.execute("SELECT status, COUNT(*) FROM query_logs GROUP BY status")
    status_counts = {row[0]: row[1] for row in cur.fetchall()}
    success = status_counts.get("success", 0)
    failure = status_counts.get("failed", 0)

    # Average response time
    cur.execute("SELECT ROUND(AVG(time_taken_ms)::numeric, 0) FROM query_logs WHERE status = 'success'")
    avg_time = cur.fetchone()[0] or 0

    # Most active user
    cur.execute("""
        SELECT u.name, COUNT(q.id) as cnt
        FROM query_logs q
        JOIN users u ON q.user_id = u.id
        GROUP BY u.name
        ORDER BY cnt DESC LIMIT 1
    """)
    row = cur.fetchone()
    most_active_user = {"name": row[0], "count": row[1]} if row else None

    # Most queried table
    cur.execute("""
        SELECT table_used, COUNT(*) as cnt
        FROM query_logs
        WHERE table_used IS NOT NULL
        GROUP BY table_used
        ORDER BY cnt DESC LIMIT 1
    """)
    row = cur.fetchone()
    most_queried_table = {"table": row[0], "count": row[1]} if row else None

    # Queries per day last 7 days
    cur.execute("""
        SELECT DATE(created_at) as day, COUNT(*) as cnt
        FROM query_logs
        WHERE created_at >= NOW() - INTERVAL '7 days'
        GROUP BY day
        ORDER BY day
    """)
    queries_per_day = [{"date": str(row[0]), "count": row[1]} for row in cur.fetchall()]

    # Queries by table
    cur.execute("""
        SELECT table_used, COUNT(*) as cnt
        FROM query_logs
        WHERE table_used IS NOT NULL
        GROUP BY table_used
        ORDER BY cnt DESC
    """)
    queries_by_table = [{"table": row[0], "count": row[1]} for row in cur.fetchall()]

    # Queries by intent
    cur.execute("""
        SELECT intent, COUNT(*) as cnt
        FROM query_logs
        WHERE intent IS NOT NULL
        GROUP BY intent
        ORDER BY cnt DESC
    """)
    queries_by_intent = [{"intent": row[0], "count": row[1]} for row in cur.fetchall()]

    # Peak hour
    cur.execute("""
        SELECT EXTRACT(HOUR FROM created_at) as hour, COUNT(*) as cnt
        FROM query_logs
        GROUP BY hour
        ORDER BY cnt DESC LIMIT 1
    """)
    row = cur.fetchone()
    peak_hour = f"{int(row[0])}:00 - {int(row[0])+1}:00" if row else "N/A"

    # Top 5 slowest queries
    cur.execute("""
        SELECT question, table_used, time_taken_ms
        FROM query_logs
        WHERE status = 'success'
        ORDER BY time_taken_ms DESC LIMIT 5
    """)
    slowest = [{"question": r[0][:60], "table": r[1], "ms": r[2]} for r in cur.fetchall()]

    cur.close()
    conn.close()

    return {
        "total_users": total_users,
        "users_today": users_today,
        "total_queries": total_queries,
        "queries_today": queries_today,
        "success_count": success,
        "failure_count": failure,
        "avg_response_ms": float(avg_time),
        "most_active_user": most_active_user,
        "most_queried_table": most_queried_table,
        "queries_per_day": queries_per_day,
        "queries_by_table": queries_by_table,
        "queries_by_intent": queries_by_intent,
        "peak_hour": peak_hour,
        "slowest_queries": slowest,
    }

# ─────────────────────────────────────────────
# QUERY MONITOR
# ─────────────────────────────────────────────

@router.get("/admin/query-monitor")
def get_query_monitor(token: dict = Depends(is_admin)):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT q.id, u.name, q.question, q.table_used,
               q.intent, q.status, q.time_taken_ms, q.created_at
        FROM query_logs q
        JOIN users u ON q.user_id = u.id
        ORDER BY q.created_at DESC
        LIMIT 100
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [
        {
            "id": r[0],
            "user": r[1],
            "question": r[2],
            "table": r[3],
            "intent": r[4],
            "status": r[5],
            "time_ms": r[6],
            "created_at": str(r[7])
        }
        for r in rows
    ]

# ─────────────────────────────────────────────
# BONUS 1 — FAILED QUERY LOG
# ─────────────────────────────────────────────

@router.get("/admin/failed-queries")
def get_failed_queries(token: dict = Depends(is_admin)):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT q.id, u.name, q.question, q.table_used, q.created_at
        FROM query_logs q
        JOIN users u ON q.user_id = u.id
        WHERE q.status = 'failed'
        ORDER BY q.created_at DESC
        LIMIT 50
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [
        {
            "id": r[0],
            "user": r[1],
            "question": r[2],
            "table": r[3],
            "created_at": str(r[4])
        }
        for r in rows
    ]

# ─────────────────────────────────────────────
# BONUS 2 — USER DETAIL / QUERY HISTORY
# ─────────────────────────────────────────────

@router.get("/admin/users/{user_id}/queries")
def get_user_queries(user_id: int, token: dict = Depends(is_admin)):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT question, table_used, intent, status, time_taken_ms, created_at
        FROM query_logs
        WHERE user_id = %s
        ORDER BY created_at DESC
        LIMIT 50
    """, (user_id,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [
        {
            "question": r[0],
            "table": r[1],
            "intent": r[2],
            "status": r[3],
            "time_ms": r[4],
            "created_at": str(r[5])
        }
        for r in rows
    ]

# ─────────────────────────────────────────────
# BONUS 3 — BAN / UNBAN USER
# ─────────────────────────────────────────────

class BanRequest(BaseModel):
    is_active: bool

@router.put("/admin/users/{user_id}/ban")
def ban_user(user_id: int, data: BanRequest, token: dict = Depends(is_admin)):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE users SET is_active = %s WHERE id = %s", (data.is_active, user_id))
    conn.commit()
    cur.close()
    conn.close()
    action = "unbanned" if data.is_active else "banned"
    return {"message": f"User {action} successfully"}