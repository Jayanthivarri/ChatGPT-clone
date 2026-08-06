from sqlalchemy.orm import Session

from app.tools.calculator import calculator
from app.tools.weather_tool import get_weather
from app.tools.web_search import web_search
from app.tools.memory_tool import get_memory


def execute_tool(
    tool: str,
    query: str,
    current_user,
    db: Session
):

    if tool == "calculator":

        return calculator(query)

    elif tool == "weather":

        return get_weather(query)

    elif tool == "memory":

        return get_memory(
            current_user.id,
            db
        )

    elif tool == "web_search":

        return web_search(query)

    return None