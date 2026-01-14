import os
from dotenv import load_dotenv
from openai import OpenAI
from prompt import SYSTEM_PROMPT

# ---------- LOAD ENV ----------
load_dotenv()

# ---------- API KEY GUARD ----------
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY missing")

# ---------- OPENAI CLIENT ----------
client = OpenAI(api_key=api_key)

# ---------- AI FUNCTION ----------
def ask_ai(conversation):
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    # user + assistant memory add
    messages.extend(conversation)

    # ---------- OPENAI CALL ----------
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=messages,
        max_output_tokens=1200,
        temperature=1.05,
        presence_penalty=0.6,
        frequency_penalty=0.6
    )

    # ---------- SAFE OUTPUT ----------
    if not response.output_text:
        return None

    return response.output_text.strip()
