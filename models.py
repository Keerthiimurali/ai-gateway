import os
import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

MODELS = {
    "fast": {
        "provider": "groq",
        "model": "llama-3.1-8b-instant",
        "api_key": GROQ_API_KEY,
        "url": "https://api.groq.com/openai/v1/chat/completions"
    },
   "capable": {
    "provider": "google",
    "model": "gemini-2.0-flash",
    "api_key": GOOGLE_API_KEY,
    "url": "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
}
}


def call_fast_model(prompt: str):

    # Handle very short prompts
    if len(prompt.split()) <= 2:
        return "Hello! How can I help you?", 5

    headers = {
        "Authorization": f"Bearer {MODELS['fast']['api_key']}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODELS["fast"]["model"],
        "messages": [
            {
                "role": "user",
                "content": f"Answer in 1 short sentence only:\n{prompt}"
            }
        ],
        "max_tokens": 25
    }

    response = requests.post(MODELS["fast"]["url"], headers=headers, json=payload)
    data = response.json()

    try:
        text = data["choices"][0]["message"]["content"]
    except Exception:
        text = data.get("error", {}).get("message", "No response from Groq")

    tokens = data.get(
        "usage", {}
    ).get(
        "total_tokens",
        len(prompt.split()) + len(text.split())
    )

    return text, tokens


def call_capable_model(prompt: str):

    url = f"{MODELS['capable']['url']}?key={MODELS['capable']['api_key']}"

    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": f"{prompt}\n\nGive a clear, well-structured answer."
                    }
                ]
            }
        ]
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, json=payload)
    data = response.json()

    try:
        if "candidates" in data:
            parts = data["candidates"][0]["content"]["parts"]
            text = parts[0].get("text", "No response")
        else:
            text = data.get("error", {}).get("message", "No response")
    except Exception as e:
        text = f"Error parsing response: {str(e)}"

    tokens = len(prompt.split()) + len(text.split())

    return text, tokens


