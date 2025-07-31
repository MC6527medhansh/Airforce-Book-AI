import os
import time
from dotenv import load_dotenv
from openai import OpenAI, RateLimitError

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def writer_agent(title: str, outline: list[str]) -> str:
    """
    Calls the OpenAI API to generate a draft for the given title
    and outline. Returns the AI-generated text.
    """
    model_name = "gpt-3.5-turbo"  
    max_tokens = 500               

    print(f"[DEBUG] Using model: {model_name}, max_tokens={max_tokens}")
    prompt = (
        f"You are an aerospace historian. Write a detailed, engaging section titled '{title}'.\n"
        "Follow this outline:\n" +
        "\n".join(f"- {item}" for item in outline)
    )

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
            print(f"[WARN] Rate limited. Retrying in {wait}s…")
            time.sleep(wait)

    raise RuntimeError("OpenAI API rate limit exceeded after 3 retries")
