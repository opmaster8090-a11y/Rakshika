import os
from dotenv import load_dotenv
from openai import OpenAI
from prompt import SYSTEM_PROMPT

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask_ai(conversation):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

    messages.extend(conversation)

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=messages,
        max_output_tokens=1200,
        temperature=1.05,
        presence_penalty=0.6,
        frequency_penalty=0.6,
    )

    return response.output_text.strip()
