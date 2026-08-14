import asyncio
from sqlalchemy.orm import Session

from app.tools.calculator import calculator
from app.tools.weather_tool import get_weather
from app.tools.web_search import web_search
from app.tools.memory_tool import get_memory
from app.tools.time_tool import get_time

from app.services.mcp_client import call_mcp_tool


def execute_tool(
    tool: str,
    query: str,
    current_user,
    db: Session
):

    # MCP tools
    if tool == "calculate":

        return asyncio.run(
            call_mcp_tool(
                "calculate",
                {"expression": query}
            )
        )

    elif tool == "get_project_info":

        return asyncio.run(
            call_mcp_tool(
                "get_project_info",
                {}
            )
        )

    elif tool == "greet":

        return asyncio.run(
            call_mcp_tool(
                "greet",
                {"name": query}
            )
        )

    # Existing local tools
    elif tool == "calculator":

        return calculator(query)

    elif tool == "weather":

        return get_weather(query)

    elif tool == "time":

        return get_time(query)

    elif tool == "memory":

        return get_memory(
            current_user.id,
            db
        )

    elif tool == "web_search":

        return web_search(query)

    return None