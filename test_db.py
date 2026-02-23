from db.db_connection import get_connection

conn = get_connection()
print("Connection successful")
conn.close()