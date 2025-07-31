# agents/research_agent.py

import os
import time
from dotenv import load_dotenv
from openai import OpenAI, RateLimitError

# Load .env
load_dotenv()

# Use same OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def research_agent(topic: str) -> str:
    """
    Gathers factual details about 'topic'.
    Returns a block of researched information.
    """
    model_name = "gpt-3.5-turbo"
    max_tokens = 300

    print(f"[DEBUG] research_agent → researching: {topic}")
    prompt = (
        f"You are an expert aviation researcher.\n"
        f"Provide concise, factual, and up-to-date details about: {topic}.\n"
        "Structure as 3–5 bullet points, each with a clear fact or statistic."
    )

    for attempt in range(3):
        try:
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": "You produce factual research bullets."},
                    {"role": "user",   "content": prompt}
                ],
                max_tokens=max_tokens
            )
            return response.choices[0].message.content.strip()
        except RateLimitError:
            wait = 2 ** attempt
            print(f"[WARN] research_agent rate-limited. Retrying in {wait}s…")
            time.sleep(wait)

    raise RuntimeError("research_agent: Rate limit exceeded after 3 retries")
