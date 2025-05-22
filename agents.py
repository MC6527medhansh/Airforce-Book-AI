import os
import openai

# Load your OpenAI key from the .env file
from dotenv import load_dotenv
load_dotenv()  
openai.api_key = os.getenv("OPENAI_API_KEY")


def writer_agent(title, outline):
    """
    Given a title and an outline (list of bullet points),
    returns a detailed draft section from GPT-4o.
    """
    prompt = (
        f"You are an aerospace historian. Write a detailed, engaging section titled '{title}'.\n"
        f"Follow this outline:\n" + "\n".join(f"- {item}" for item in outline)
    )
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role":"system","content":"You write textbook chapters."},
                  {"role":"user","content":prompt}],
        max_tokens=1500
    )
    return response.choices[0].message.content
