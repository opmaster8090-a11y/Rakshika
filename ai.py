import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY missing")

client = OpenAI(api_key=api_key)

def ask_ai(conversation):
    messages = []
    messages.extend(conversation)

    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=messages,
            max_output_tokens=1200,   # longer replies
            temperature=1.1,          # more natural / less robotic
            timeout=10
        )

        if response and response.output_text:
            return response.output_text.strip()

        return None

    except Exception as e:
        print("OPENAI ERROR:", e)
        return None
