import os
import json
from groq import Groq
from dotenv import load_dotenv
from db.schema_db import get_column_details

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "llama-3.3-70b-versatile"

def select_columns(user_question: str, intent: str, table_name: str) -> dict:

    columns = get_column_details(table_name)
    column_info = json.dumps(columns, indent=2)

    prompt = f"""You are a column selection expert for a SQL question answering system.

The selected table is: "{table_name}"
The columns available in this table are:
{column_info}

The user asked: "{user_question}"
The detected intent is: "{intent}"

Your job is to identify:
1. select_columns - columns to show in the result
2. filter_columns - columns used in WHERE condition
3. aggregate_columns - columns used in aggregation like AVG, SUM, MAX, MIN, COUNT
4. group_by_columns - columns used in GROUP BY

Only use exact column names from the list above. Return empty lists if not applicable.

Respond ONLY in this exact JSON format with no explanation:
{{
  "select_columns": ["<col1>", "<col2>"],
  "filter_columns": ["<col1>"],
  "aggregate_columns": ["<col1>"],
  "group_by_columns": ["<col1>"]
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
            "select_columns": [],
            "filter_columns": [],
            "aggregate_columns": [],
            "group_by_columns": []
        }

    return result