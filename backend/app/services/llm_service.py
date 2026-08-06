import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

DEFAULT_MODEL = os.getenv("DEFAULT_MODEL")
FALLBACK_MODELS = os.getenv("FALLBACK_MODELS", "").split(",")

print("Default Model:", DEFAULT_MODEL)
print("Fallback Models:", FALLBACK_MODELS)

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)


# -----------------------------
# Decide whether web search is needed
# -----------------------------
def should_search(query: str) -> bool:

    query = query.lower()

    keywords = [
        "weather",
        "today",
        "latest",
        "current",
        "live",
        "news",
        "gold",
        "silver",
        "price",
        "stock",
        "share",
        "bitcoin",
        "crypto",
        "ipl",
        "score",
        "match",
        "temperature",
        "forecast",
        "rain",
        "earthquake",
        "election",
        "traffic",
        "petrol",
        "diesel",
        "currency",
        "exchange rate"
    ]

    decision = any(word in query for word in keywords)

    print(f"🔍 Search Decision: {decision}")

    return decision


# -----------------------------
# Generate AI Response
# -----------------------------
def generate_response(messages: list):

    system_prompt = {
        "role": "system",
        "content": """
You are ChatGPT.

Rules:

- Give concise answers.
- Maximum 4 bullet points.
- Keep answers under 150 words unless the user asks for details.
- Use bullet points whenever possible.
- Never use markdown headings(#, ##, ###).
- Do not repeat information.
- If live web search results are provided,
  always trust and use them.
- Never say:
  "I don't have internet access."
- Never ignore search results.
- Highlight important words using **bold** only when necessary.
"""
    }

    messages = [system_prompt] + messages

    models = [
        model.strip()
        for model in FALLBACK_MODELS
        if model.strip()
    ]

    if DEFAULT_MODEL not in models:
        models.append(DEFAULT_MODEL)

    last_error = None

    for model in models:

        try:

            print(f"🤖 Trying Model: {model}")

            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.2,
                max_tokens=1000
            )

            print(f"✅ Using Model: {model}")

            return response.choices[0].message.content

        except Exception as e:

            print(f"❌ {model} failed")
            print(e)

            last_error = e

    raise Exception(
        f"All models failed.\n{last_error}"
    )