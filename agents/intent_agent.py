import os
import json
from groq import Groq
from dotenv import load_dotenv
from db.schema_db import get_all_table_descriptions

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "llama-3.3-70b-versatile"

def classify_intent(user_question: str) -> dict:

    table_context = get_all_table_descriptions()
    table_info = json.dumps(table_context, indent=2)

    prompt = f"""You are an intent classification expert for a SQL-based question answering system.

You have access to the following database tables:
{table_info}

Classify the user's question into exactly one of these intent types:
- aggregation : questions asking for sum, average, max, min, count
- filtering   : questions asking to find records matching a condition
- ranking     : questions asking for top N or bottom N records
- comparison  : questions comparing two or more entities
- lookup      : questions asking for details of a specific record
- unknown     : question is not related to any of the available tables

Also give a confidence score between 0.0 and 1.0.
Also detect if the question is ambiguous (true/false).

User Question: {user_question}

Respond ONLY in this exact JSON format with no explanation:
{{
  "intent": "<intent_type>",
  "confidence": <score>,
  "ambiguous": <true_or_false>,
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
            "intent": "unknown",
            "confidence": 0.0,
            "ambiguous": True,
            "reason": "Could not parse model response"
        }

    return result