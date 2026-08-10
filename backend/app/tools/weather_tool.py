from app.tools.web_search import web_search


def get_weather(query: str):

    query_lower = query.lower()

    # --------------------------------
    # Detect Location
    # --------------------------------

    locations = [
        "london",
        "india",
        "hyderabad",
        "vizag",
        "visakhapatnam",
        "delhi",
        "new york",
        "chicago",
        "los angeles",
        "tokyo",
        "singapore",
    ]

    location = None

    for place in locations:
        if place in query_lower:
            location = place
            break

    # Default location
    if location is None:
        location = "India"

    # --------------------------------
    # Create Weather-Specific Query
    # --------------------------------

    weather_query = f"current weather in {location}"

    print("🌦 Weather Search Query:", weather_query)

    results = web_search(weather_query)

    # --------------------------------
    # Find useful weather result
    # --------------------------------

    for result in results:

        title = result.get("title", "")
        snippet = result.get("snippet", "")

        text = f"{title} {snippet}".lower()

        if any(word in text for word in [
            "temperature",
            "weather",
            "humidity",
            "wind",
            "degrees",
            "°c",
            "°f"
        ]):

            return {
                "title": f"Current Weather - {location.title()}",
                "snippet": snippet,
                "link": result.get("link", "")
            }

    # --------------------------------
    # No weather result
    # --------------------------------

    return {
        "title": f"Weather - {location.title()}",
        "snippet": f"Weather information for {location.title()} was not found.",
        "link": ""
    }