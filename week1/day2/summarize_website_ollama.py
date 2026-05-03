from IPython.display import Markdown, display
from openai import OpenAI

from utils.scraper import fetch_website_contents_playwright


system_prompt = """
You are a snarky assistant that analyzes the contents of a website,
and provides a short, snarky, humorous summary, ignoring text that might be navigation related.
Respond in markdown. Do not wrap the markdown in a code block - respond just with the markdown.
"""

user_prompt_prefix = """
Here are the contents of a website.
Provide a short summary of this website.
If it includes news or announcements, then summarize these too.

"""
def summarize_website(url):
    ollama_base_url = "http://localhost:11434/v1"
    ollama = OpenAI(base_url=ollama_base_url, api_key="ollama")
    website_contents = fetch_website_contents_playwright(url)
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt_prefix + website_contents},
    ]
    response = ollama.chat.completions.create(model="llama3.2", messages=messages)
    print(response.choices[0].message.content)
    return response.choices[0].message.content

def display_summary(url):
    summary = summarize_website(url)
    display(Markdown(summary))

display_summary("https://www.cnn.com")