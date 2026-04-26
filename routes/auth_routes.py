from fastapi import APIRouter, HTTPException
from auth.models import SignupModel, LoginModel
from auth.auth_handler import hash_password, verify_password, create_token
from db.db_connection import get_connection

router = APIRouter()

@router.post("/signup")
def signup(data: SignupModel):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE email = %s", (data.email,))
    if cur.fetchone():
        cur.close()
        conn.close()
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed = hash_password(data.password)
    cur.execute(
        "INSERT INTO users (name, email, password_hash, role) VALUES (%s, %s, %s, %s) RETURNING id",
        (data.name, data.email, hashed, data.role)
    )
    conn.commit()
    cur.close()
    conn.close()
    return {"message": "Account created successfully"}

@router.post("/login")
def login(data: LoginModel):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, password_hash, role, is_active FROM users WHERE email = %s", (data.email,))
    user = cur.fetchone()
    cur.close()
    conn.close()

    if not user or not verify_password(data.password, user[2]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # Check if user is banned
    if user[4] is False:
        raise HTTPException(status_code=403, detail="Your account has been suspended. Contact admin.")

    token = create_token({
        "id": user[0],
        "user_id": user[0],  # Add this explicitly
        "name": user[1],
        "role": user[3]
    })
    return {"token": token, "name": user[1], "role": user[3]}
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, password_hash, role FROM users WHERE email = %s", (data.email,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    if not user or not verify_password(data.password, user[2]):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    token = create_token({"id": user[0], "name": user[1], "role": user[3]})
    return {"token": token, "name": user[1], "role": user[3]}