from typing import Any, TypedDict
from sqlalchemy.orm import Session


class ChatState(TypedDict, total=False):

    session_id: int
    user_message: str

    db: Session
    current_user: Any

    conversation: list

    # Multiple tools
    tools_used: list[str]
    tool_results: dict[str, Any]

    ai_response: str