import os
from dotenv import load_dotenv
from openai import OpenAI
import requests

load_dotenv()
openai_api_key = (os.getenv("OPENAI_API_KEY") or "").strip()
gemini_api_key = (os.getenv("GEMINI_API_KEY") or "").strip()

if not openai_api_key:
    raise ValueError("OPENAI_API_KEY is not set")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set")


def chat_completion_api():
    headers = {"Authorization": f"Bearer {openai_api_key}", "Content-Type": "application/json"}
    payload = {
        "model": "gpt-5-nano",
        "messages": [{"role": "user", "content": "Tell me a fun fact"}],
    }
    url = "https://api.openai.com/v1/chat/completions"
    response = requests.post(url, headers=headers, json=payload, timeout=60)
    response.raise_for_status()
    print(response.json()["choices"][0]["message"]["content"])


def complete_chat_openai_client():
    client = OpenAI(api_key=openai_api_key)
    response = client.chat.completions.create(
        model="gpt-5-nano",
        messages=[{"role": "user", "content": "Tell me a fun fact"}],
    )
    print(response.choices[0].message.content)
    return response.choices[0].message.content


def complete_chat_gemini_client():
    gemini_base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
    gemini = OpenAI(base_url=gemini_base_url, api_key=gemini_api_key)
    response = gemini.chat.completions.create(
        model="gemini-3.1-pro-preview",
        messages=[{"role": "user", "content": "Tell me a fun fact"}],
    )
    print(response.choices[0].message.content)
    return response.choices[0].message.content

def complete_chat_ollama_client():
    ollama_base_url = "http://localhost:11434/v1"
    ollama=OpenAI(base_url=ollama_base_url, api_key="ollama")
    response=ollama.chat.completions.create(
        model="llama3.2",
        messages=[{"role":'user',"content":"Tell me a fun fact"}],
    )
    print(response.choices[0].message.content)
    return response.choices[0].message.content

if __name__ == "__main__":
    chat_completion_api()
    complete_chat_openai_client()
    complete_chat_gemini_client()
    complete_chat_ollama_client()
