import os
import json
from groq import Groq
from dotenv import load_dotenv
from db.schema_db import get_all_table_descriptions

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "llama-3.3-70b-versatile"

def select_table(user_question: str, intent: str) -> dict:

    table_context = get_all_table_descriptions()
    table_info = json.dumps(table_context, indent=2)

    prompt = f"""You are a table selection expert for a SQL question answering system.

You have these database tables available:
{table_info}

The user asked: "{user_question}"
The detected intent is: "{intent}"

Your job is to select which table is most relevant to answer this question.
Only select from these exact table names: student, cricket, employee

If the question is unrelated to any table, return "none".

Respond ONLY in this exact JSON format with no explanation:
{{
  "table": "<table_name>",
  "confidence": <score between 0.0 and 1.0>,
  "reason": "<one line explanation>"
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
            "table": "none",
            "confidence": 0.0,
            "reason": "Could not parse model response"
        }

    return result