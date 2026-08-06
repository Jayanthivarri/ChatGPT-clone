from app.services.llm_service import client, DEFAULT_MODEL


def route_tool(query: str):

    router_messages = [
        {
            "role": "system",
            "content": """
You are a tool classifier.

Choose exactly ONE label from this list:

weather
calculator
memory
web_search
llm

Rules:
- Current weather, forecast, temperature → weather
- Math, calculations → calculator
- User profile or previous conversation → memory
- Latest news, live data, gold price, sports, stocks → web_search
- Everything else → llm

Output MUST be exactly one label.
Do not explain.
Do not use punctuation.
Do not write a sentence.
"""
        },
        {
            "role": "user",
            "content": query
        }
    ]

    response = client.chat.completions.create(
        model=DEFAULT_MODEL,
        messages=router_messages,
        temperature=0,
        max_tokens=5
    )

    content = response.choices[0].message.content

    print("🛠 Router Response:", content)

    if content is None:
        tool = "llm"
    else:
        tool = content.strip().lower()

    # -----------------------
    # Memory Fallback
    # -----------------------
    query_lower = query.lower()

    memory_keywords = [
        "my name",
        "who am i",
        "remember",
        "what did i tell you",
        "where do i live",
        "my age",
        "my email",
        "my phone"
    ]

    

    if tool == "llm" and any(keyword in query_lower for keyword in memory_keywords):
        return "memory"

    
    # Web Search Fallback
    web_keywords = [
        "latest",
        "today",
        "current",
        "live",
        "news",
        "gold price",
        "stock price",
        "bitcoin",
        "ipl",
        "score",
        "weather",
        "temperature",
        "forecast",
        "chief minister",
        "who is cm",
        "cm of",
        "prime minister",
        "president",
        "governor"
    ]

    return tool