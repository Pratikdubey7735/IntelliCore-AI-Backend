import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "llama-3.3-70b-versatile"

def generate_final_answer(user_question: str, sql_result: dict) -> str:

    if not sql_result["success"]:
        return f"I encountered an error while fetching your data: {sql_result.get('error', 'Unknown error')}"

    if sql_result["row_count"] == 0:
        return "No records were found matching your query in the database."

    data_preview = sql_result["data"][:10]

    prompt = f"""You are a helpful data analyst assistant.

The user asked: "{user_question}"

The database returned these results:
{json.dumps(data_preview, indent=2)}

Total rows returned: {sql_result['row_count']}

Write a clear, concise, natural language answer to the user's question based on the data above.
- Be conversational and friendly
- Highlight the key finding directly
- If there are multiple rows, summarize the pattern
- Do not mention SQL or database internals
- Keep it under 3 sentences"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content