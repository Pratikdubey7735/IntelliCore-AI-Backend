import os
import json
from groq import Groq
from dotenv import load_dotenv
from db.schema_db import get_cast_columns

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "llama-3.3-70b-versatile"

def generate_sql(user_question: str, intent: str, table_name: str, columns: dict, pseudo_code: dict) -> dict:

    cast_columns = get_cast_columns(table_name)
    cast_info = json.dumps(cast_columns)

    cricket_note = ""
    if table_name == "cricket":
        cricket_note = """
IMPORTANT - Cricket table special rules:
- ALL numeric columns in cricket table are stored as VARCHAR
- To sort or calculate on runs: CAST(runs AS INTEGER)
- Always filter bad rows first using: WHERE runs ~ '^[0-9]+$'
- Example correct query for top 5 by runs:
  SELECT player_name, runs FROM cricket WHERE runs ~ '^[0-9]+$' ORDER BY CAST(runs AS INTEGER) DESC LIMIT 5;
- Follow this exact pattern for any numeric operation on cricket table
"""

    prompt = f"""You are a PostgreSQL SQL query generator.

User Question: "{user_question}"
Intent: "{intent}"
Table: "{table_name}"
Columns to use: {json.dumps(columns)}
Query Plan: "{pseudo_code['pseudo_code']}"
Columns that need CAST: {cast_info}
{cricket_note}

Rules:
1. Only use the exact table name and column names provided
2. Use proper PostgreSQL syntax
3. End query with semicolon
4. Return ONLY the JSON below, no extra text

Respond in this exact JSON format:
{{
  "sql": "<the complete postgresql query here>",
  "explanation": "<one line explanation>"
}}"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = response.choices[0].message.content

    try:
        start = raw.find("{")
        end = raw.rfind("}") + 1
        result = json.loads(raw[start:end])
    except Exception:
        result = {
            "sql": "",
            "explanation": "Could not generate SQL"
        }

    return result