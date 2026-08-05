import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

DEFAULT_MODEL = os.getenv("DEFAULT_MODEL")
FALLBACK_MODELS = os.getenv("FALLBACK_MODELS").split(",")

print("Default Model:", DEFAULT_MODEL)
print("Fallback Models:", FALLBACK_MODELS)

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)


def should_search(query: str) -> bool:
    """
    Decide whether the user's question requires web search.
    Returns True if web search is needed, otherwise False.
    """

    router_messages = [
        {
            "role": "system",
            "content": (
                "You are a routing assistant.\n"
                "If the user's question requires current, real-time, latest, live, "
                "breaking news, today's information, weather, stock prices, sports scores, "
                "or any information that changes over time, reply ONLY with YES.\n\n"
                "Otherwise reply ONLY with NO."
            )
        },
        {
            "role": "user",
            "content": query
        }
    ]

    try:

        response = client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=router_messages,
            temperature=0
        )

        decision = response.choices[0].message.content.strip().upper()

        print(f"🔍 Search Decision: {decision}")

        return decision == "YES"

    except Exception as e:

        print("❌ Router Failed:", e)

        return False


def generate_response(messages: list):

    last_error = None

    # Try all fallback models
    for model in FALLBACK_MODELS:

        try:

            response = client.chat.completions.create(
                model=model.strip(),
                messages=messages,
                temperature=0.3
            )

            print(f"✅ Using Fallback Model: {model.strip()}")

            return response.choices[0].message.content

        except Exception as e:

            print(f"❌ {model.strip()} failed")

            last_error = e

            continue

    # Final fallback -> OpenRouter Free Router
    try:

        print(f"🔄 Switching to Default Model: {DEFAULT_MODEL}")

        response = client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=messages,
            temperature=0.3
        )

        print(f"✅ Using Default Model: {DEFAULT_MODEL}")

        return response.choices[0].message.content

    except Exception as e:

        raise Exception(
            f"All fallback models failed.\n{e}"
        )