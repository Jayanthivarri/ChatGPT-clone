import os
import requests

from dotenv import load_dotenv

load_dotenv()

SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")


def web_search(query: str):

    url = "https://serpapi.com/search"

    params = {
        "engine": "google",
        "q": query,
        "api_key": SERPAPI_API_KEY
    }

    response = requests.get(url, params=params)

    response.raise_for_status()

    data = response.json()

    results = []

    for item in data.get("organic_results", [])[:5]:

        results.append(
            {
                "title": item.get("title"),
                "snippet": item.get("snippet"),
                "link": item.get("link")
            }
        )

    return results