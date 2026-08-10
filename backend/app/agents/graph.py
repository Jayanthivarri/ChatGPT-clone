from langgraph.graph import StateGraph, START, END

from app.agents.state import ChatState
from app.router.tool_router import route_tool
from app.agents.tool_executor import execute_tool
from app.services.llm_service import generate_response


# ============================================
# 1. ROUTE NODE
# ============================================

def route_node(state: ChatState):

    user_message = state["user_message"]

    tools = route_tool(user_message)

    print("🛠 LangGraph Selected Tools:", tools)

    return {
        "tools_used": tools
    }


# ============================================
# 2. EXECUTE MULTIPLE TOOLS
# ============================================

def execute_node(state: ChatState):

    tools = state.get("tools_used", [])

    # Normal LLM
    if not tools or tools == ["llm"]:

        return {
            "tool_results": {}
        }

    tool_results = {}

    for tool in tools:

        if tool == "llm":
            continue

        print(f"🔧 Executing Tool: {tool}")

        result = execute_tool(
            tool,
            state["user_message"],
            state["current_user"],
            state["db"]
        )

        tool_results[tool] = result

        print(f"✅ {tool} Result:", result)

    return {
        "tool_results": tool_results
    }


# ============================================
# 3. PREPARE CONVERSATION
# ============================================

def prepare_node(state: ChatState):

    conversation = list(state["conversation"])

    tools = state.get("tools_used", [])
    tool_results = state.get("tool_results", {})

    print("\n================ TOOL DEBUG ================")
    print("TOOLS:", tools)
    print("TOOL RESULTS:", tool_results)
    print("============================================\n")

    # ----------------------------------------
    # Normal LLM
    # ----------------------------------------

    if not tools or tools == ["llm"]:

        return {
            "conversation": conversation
        }

    # ----------------------------------------
    # Build ONE combined tool result
    # ----------------------------------------

    tool_information = ""

    # ----------------------------------------
    # Calculator
    # ----------------------------------------

    if "calculator" in tools:

        result = tool_results.get("calculator")

        tool_information += f"""
CALCULATOR RESULT:
{result}

Use this exact calculation result.
"""

    # ----------------------------------------
    # Memory
    # ----------------------------------------

    if "memory" in tools:

        result = tool_results.get("memory")

        tool_information += f"""
USER MEMORY:
{result}

Use the stored memory to answer the user's question.
Do not invent personal information.
"""

    # ----------------------------------------
    # Time
    # ----------------------------------------

    if "time" in tools:

        result = tool_results.get("time")

        print("🕐 TIME RESULT =", result)

        if isinstance(result, dict):

            time_text = result.get(
                "snippet",
                str(result)
            )

        else:

            time_text = str(result)

        tool_information += f"""
CURRENT TIME TOOL RESULT:
{time_text}

IMPORTANT:
- This is the actual result returned by the time tool.
- Use this exact time in the answer.
- Do not calculate or invent another time.
"""

    # ----------------------------------------
    # Weather
    # ----------------------------------------

    if "weather" in tools:

        result = tool_results.get("weather")

        print("🌦 WEATHER RESULT =", result)

        if isinstance(result, dict):

            weather_text = result.get(
                "snippet",
                str(result)
            )

            weather_link = result.get(
                "link",
                ""
            )

        else:

            weather_text = str(result)
            weather_link = ""

        tool_information += f"""
CURRENT WEATHER TOOL RESULT:
{weather_text}

Weather Source:
{weather_link}

IMPORTANT:
- This is the actual result returned by the weather tool.
- Use this weather information in the answer.
- Do not invent temperature or weather conditions.
- Do not say real-time weather is unavailable when valid weather data is provided.
"""

    # ----------------------------------------
    # Web Search
    # ----------------------------------------

    if "web_search" in tools:

        results = tool_results.get(
            "web_search",
            []
        )

        formatted_results = ""

        for result in results:

            formatted_results += f"""
Title: {result.get('title', '')}
Snippet: {result.get('snippet', '')}
Link: {result.get('link', '')}
"""

        tool_information += f"""
LIVE WEB SEARCH RESULTS:

{formatted_results}

IMPORTANT:
- Use the search results when answering.
- Do not replace current information with general knowledge.
"""

    # ----------------------------------------
    # Add tool information to conversation
    # ----------------------------------------

    if tool_information:

        conversation.append(
            {
                "role": "system",
                "content": f"""
TOOL RESULTS FOR THE CURRENT USER QUESTION

The following information was obtained by executing the required tools.

{tool_information}

FINAL INSTRUCTIONS:

1. Use the tool results to answer the user's question.
2. If multiple tools were executed, combine ALL relevant results.
3. Do not ignore any tool result.
4. Do not invent values.
5. Do not say that real-time data is unavailable when a tool has returned valid current data.
6. Answer only what the user asked.
"""
            }
        )

    return {
        "conversation": conversation
    }


# ============================================
# 4. GENERATE AI RESPONSE
# ============================================

def generate_node(state: ChatState):

    conversation = state["conversation"]

    response = generate_response(
        conversation
    )

    return {
        "ai_response": response
    }


# ============================================
# 5. ROUTING AFTER ROUTE NODE
# ============================================

def route_after_node(state: ChatState):

    tools = state.get("tools_used", [])

    if not tools or tools == ["llm"]:

        return "prepare"

    return "execute_tool"


# ============================================
# 6. BUILD LANGGRAPH
# ============================================

builder = StateGraph(ChatState)

builder.add_node(
    "route",
    route_node
)

builder.add_node(
    "execute_tool",
    execute_node
)

builder.add_node(
    "prepare",
    prepare_node
)

builder.add_node(
    "generate",
    generate_node
)


# ============================================
# GRAPH FLOW
# ============================================

builder.add_edge(
    START,
    "route"
)

builder.add_conditional_edges(
    "route",
    route_after_node,
    {
        "execute_tool": "execute_tool",
        "prepare": "prepare"
    }
)

builder.add_edge(
    "execute_tool",
    "prepare"
)

builder.add_edge(
    "prepare",
    "generate"
)

builder.add_edge(
    "generate",
    END
)


# ============================================
# COMPILE
# ============================================

chat_graph = builder.compile()