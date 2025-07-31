# agents/editor_agent.py

import os
import time
from dotenv import load_dotenv
from openai import OpenAI, RateLimitError

# Load .env
load_dotenv()

# Same client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def editor_agent(draft: str) -> str:
    """
    Polishes 'draft' text: improve flow, fix grammar,
    add simple citation placeholders like [1], [2].
    Returns the refined text.
    """
    model_name = "gpt-3.5-turbo"
    max_tokens = 400

    print("[DEBUG] editor_agent → polishing draft")
    prompt = (
        "You are a professional technical editor.\n"
        "Please refine the following text for clarity, coherence, and academic style.\n"
        "Add placeholder citations [1], [2], etc., where relevant.\n\n"
        f"Draft:\n{draft}"
    )

    for attempt in range(3):
        try:
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": "You refine and format technical writing."},
                    {"role": "user",   "content": prompt}
                ],
                max_tokens=max_tokens
            )
            return response.choices[0].message.content.strip()
        except RateLimitError:
            wait = 2 ** attempt
            print(f"[WARN] editor_agent rate-limited. Retrying in {wait}s…")
            time.sleep(wait)

    raise RuntimeError("editor_agent: Rate limit exceeded after 3 retries")
