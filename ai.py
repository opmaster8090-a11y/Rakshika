import os
from dotenv import load_dotenv
from openai import OpenAI
from prompt import SYSTEM_PROMPT

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask_ai(user_msg: str) -> str:
    response = client.responses.create(
        model="gpt-4o-mini",
        input=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_msg}
        ],
        max_output_tokens=1000   # 🔥 BADHA DIYA (200 → 600)
    )

    return response.output_text
