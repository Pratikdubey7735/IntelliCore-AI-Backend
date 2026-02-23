import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "llama-3.3-70b-versatile"

def generate_pseudo_code(user_question: str, intent: str, table_name: str, columns: dict) -> dict:

    prompt = f"""You are a SQL query planner for a PostgreSQL database.

User Question: "{user_question}"
Intent: "{intent}"
Table: "{table_name}"
Selected Columns: {json.dumps(columns)}

Write a plain English step-by-step plan describing exactly what SQL query should do.
Do NOT write actual SQL. Write the logical steps only.

Also identify:
- needs_casting: true if any numeric column is stored as VARCHAR and needs CAST
- needs_having: true if query needs a HAVING clause
- needs_subquery: true if query needs a subquery

Respond ONLY in this exact JSON format:
{{
  "pseudo_code": "<plain english description of what the query should do>",
  "needs_casting": <true_or_false>,
  "needs_having": <true_or_false>,
  "needs_subquery": <true_or_false>
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
            "pseudo_code": "Could not generate pseudo code",
            "needs_casting": False,
            "needs_having": False,
            "needs_subquery": False
        }

    return result