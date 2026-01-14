import os
from dotenv import load_dotenv
from openai import OpenAI
from prompt import SYSTEM_PROMPT

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY missing")

client = OpenAI(api_key=api_key)

def ask_ai(conversation):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]
    messages.extend(conversation)

    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=messages,
            max_output_tokens=800,
            temperature=0.85,
            timeout=10
        )

        if response and response.output_text:
            return response.output_text.strip()

        return None

    except Exception as e:
        print("OPENAI ERROR:", e)
        return None
