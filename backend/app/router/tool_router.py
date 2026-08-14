from app.services.llm_service import client, DEFAULT_MODEL


def route_tool(query: str):

    query_lower = query.lower().strip()

    tools = []

    # ============================================
    # 1. MEMORY
    # ============================================

    memory_keywords = [
        "my name",
        "who am i",
        "remember",
        "what did i tell you",
        "where do i live",
        "my age",
        "my email",
        "my phone",
        "my details",
        "what do you know about me"
    ]

    if any(keyword in query_lower for keyword in memory_keywords):
        tools.append("memory")

    # ============================================
    # 2. TIME
    # ============================================

    time_keywords = [
        "what time",
        "current time",
        "time in",
        "time at",
        "local time",
        "time now",
        "clock",
        "time and",
        "time &",
        "time plus",
        "today's time",
        "todays time",
        "time today"
    ]

    if any(keyword in query_lower for keyword in time_keywords):
        tools.append("time")

    # ============================================
    # 3. WEATHER
    # ============================================

    weather_keywords = [
        "weather",
        "temperature",
        "forecast",
        "rain",
        "raining",
        "humidity",
        "wind",
        "climate"
    ]

    if any(keyword in query_lower for keyword in weather_keywords):
        tools.append("weather")

    # ============================================
    # 4. CALCULATOR
    # ============================================

    calculator_keywords = [
        "calculate",
        "calculator",
        "how much is",
        "multiply",
        "divide",
        "percentage",
        "%",
        "+",
        "*",
        "/",
        "-",
        "**"
    ]

    if any(keyword in query_lower for keyword in calculator_keywords):
        tools.append("calculator")

    # ============================================
    # 5. MCP TOOLS
    # ============================================

    # ---- Project Information ----

    project_keywords = [
        "project information",
        "project info",
        "project details",
        "about the project",
        "tell me about this project",
        "information about the project"
    ]

    if any(keyword in query_lower for keyword in project_keywords):
        tools.append("get_project_info")

    # ---- Greeting ----

    greet_keywords = [
        "greet me",
        "say hello",
        "greet",
        "say hi"
    ]

    if any(keyword in query_lower for keyword in greet_keywords):
        tools.append("greet")

    # ============================================
    # 6. WEB SEARCH
    # ============================================

    web_keywords = [
        "latest",
        "news",
        "gold price",
        "gold rate",
        "silver price",
        "silver rate",
        "stock price",
        "share price",
        "bitcoin",
        "crypto",
        "ipl",
        "score",
        "match",
        "election",
        "traffic",
        "petrol",
        "diesel",
        "currency",
        "exchange rate",
        "chief minister",
        "who is cm",
        "cm of",
        "prime minister",
        "president",
        "governor"
    ]

    if any(keyword in query_lower for keyword in web_keywords):
        tools.append("web_search")

    # ============================================
    # REMOVE DUPLICATES
    # ============================================

    tools = list(dict.fromkeys(tools))

    # ============================================
    # DEBUG
    # ============================================

    if tools:
        print("🛠 Selected Tools:", tools)
        return tools

    # ============================================
    # 7. LLM CLASSIFIER
    # ============================================

    router_messages = [
        {
            "role": "system",
            "content": """
You are a tool classifier.

Choose exactly ONE label from this list:

weather
calculator
memory
time
web_search
get_project_info
greet
llm

Rules:

- Current weather, forecast, temperature → weather
- Math, calculations → calculator
- User profile or previous conversation → memory
- Current time or time in a location → time
- Latest news, live data, gold price, sports, stocks → web_search
- Questions about the ChatGPT Clone project → get_project_info
- Requests to greet someone or say hello → greet
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

    if not content:
        return ["llm"]

    tool = content.strip().lower()

    valid_tools = {
        "weather",
        "calculator",
        "memory",
        "time",
        "web_search",
        "get_project_info",
        "greet",
        "llm"
    }

    if tool not in valid_tools:
        return ["llm"]

    return [tool]