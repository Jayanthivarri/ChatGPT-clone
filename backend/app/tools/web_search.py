import os
import requests

from dotenv import load_dotenv

load_dotenv()

SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")


def web_search(query: str):

    url = "https://serpapi.com/search.json"

    params = {
        "engine": "google",
        "q": query,
        "api_key": SERPAPI_API_KEY,
        "num": 5,
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=60
        )

        response.raise_for_status()

        data = response.json()

    except requests.exceptions.Timeout:

        print("❌ SerpAPI request timed out")

        return [
            {
                "title": "Search Timeout",
                "snippet": "The web search took too long to respond. Please try again.",
                "link": ""
            }
        ]

    except requests.exceptions.RequestException as e:

        print("❌ SerpAPI Error:", e)

        return [
            {
                "title": "Search Error",
                "snippet": "Unable to fetch web search results right now.",
                "link": ""
            }
        ]

    # ----------------------------
    # Results
    # ----------------------------

    results = []

    # ----------------------------
    # Weather Results
    # ----------------------------

    if data.get("weather_result"):

        weather = data["weather_result"]

        results.append(
            {
                "title": "Current Weather",
                "snippet": f"""
Temperature: {weather.get('temperature', 'N/A')}
Condition: {weather.get('condition', 'N/A')}
Humidity: {weather.get('humidity', 'N/A')}
Wind: {weather.get('wind', 'N/A')}
""",
                "link": ""
            }
        )

    # ----------------------------
    # Google Answer Box
    # ----------------------------

    if data.get("answer_box"):

        answer = data["answer_box"]

        answer_text = (
            answer.get("answer")
            or answer.get("snippet")
            or answer.get("title")
            or ""
        )

        results.append(
            {
                "title": answer.get("title", "Answer"),
                "snippet": answer_text,
                "link": answer.get("link", "")
            }
        )

    # ----------------------------
    # Knowledge Graph
    # ----------------------------

    if data.get("knowledge_graph"):

        kg = data["knowledge_graph"]

        desc = kg.get("description", "")

        if desc:

            results.append(
                {
                    "title": kg.get("title", "Knowledge Graph"),
                    "snippet": desc,
                    "link": kg.get("website", "")
                }
            )

    # ----------------------------
    # Organic Results
    # ----------------------------

    for item in data.get("organic_results", [])[:5]:

        results.append(
            {
                "title": item.get("title", ""),
                "snippet": item.get("snippet", ""),
                "link": item.get("link", "")
            }
        )

    # ----------------------------
    # Fallback
    # ----------------------------

    if not results:

        results.append(
            {
                "title": "No Results",
                "snippet": "No search results found.",
                "link": ""
            }
        )

    return results