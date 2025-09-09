import os
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_text(text, max_chars=400):
    prompt = f"Summarize this text in 3-4 concise bullet points:\n\n{text[:max_chars]}"
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=120,   # smaller response
        timeout=20        # fail fast instead of hanging forever
    )
    return response.choices[0].message["content"]

