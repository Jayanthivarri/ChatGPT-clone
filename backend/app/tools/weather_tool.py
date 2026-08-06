from app.tools.web_search import web_search


def get_weather(query: str):

    results = web_search(query)

    if not results:
        return "Unable to fetch weather."

    return results[0]