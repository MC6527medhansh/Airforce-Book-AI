# agents/writer_agent.py

import os
import time
from dotenv import load_dotenv
from openai import OpenAI, RateLimitError

# Load .env
load_dotenv()

# Instantiate OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def writer_agent(title: str, outline: list[str]) -> str:
    """
    Generates a first draft for 'title' following 'outline'.
    Returns raw AI-generated text.
    """
    model_name = "gpt-3.5-turbo"    # switch to gpt-4o once billing is live
    max_tokens = 500                # keep small during development

    print(f"[DEBUG] writer_agent → model={model_name}, max_tokens={max_tokens}")
    prompt = (
        f"You are an aerospace historian. Write a detailed section titled '{title}'.\n"
        "Follow this outline:\n" +
        "\n".join(f"- {item}" for item in outline)
    )

    # Retry on rate limits
    for attempt in range(3):
        try:
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": "You write textbook chapters."},
                    {"role": "user",   "content": prompt}
                ],
                max_tokens=max_tokens
            )
            return response.choices[0].message.content.strip()
        except RateLimitError:
            wait = 2 ** attempt
            print(f"[WARN] writer_agent rate-limited. Retrying in {wait}s…")
            time.sleep(wait)

    raise RuntimeError("writer_agent: Rate limit exceeded after 3 retries")
