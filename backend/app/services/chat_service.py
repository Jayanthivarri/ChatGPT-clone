from fastapi import HTTPException
from sqlalchemy.orm import Session
from concurrent.futures import ThreadPoolExecutor

from app.database.models import ChatSession, Message, UserMemory
from app.services.llm_service import generate_response
from app.router.tool_router import route_tool
from app.services.memory_service import save_memory
from app.tools.web_search import web_search
from app.tools.calculator import calculator
from app.tools.weather_tool import get_weather
from app.tools.memory_tool import get_memory
from app.agents.tool_executor import execute_tool

executor = ThreadPoolExecutor(max_workers=5)


def process_chat(
    session_id: int | None,
    user_message: str,
    db: Session,
    current_user
):

    # -----------------------------
    # Create new session if needed
    # -----------------------------
    if session_id is None:

        session = ChatSession(
            title=user_message[:30],
            user_id=current_user.id
        )
        print("✅ New Session Created:", session.title)
        db.add(session)
        db.commit()
        db.refresh(session)

        session_id = session.id

    else:

        session = (
            db.query(ChatSession)
            .filter(
                ChatSession.id == session_id,
                ChatSession.user_id == current_user.id
            )
            .first()
        )

        if session is None:
            raise HTTPException(
                status_code=404,
                detail="Chat session not found"
            )

    # -----------------------------
    # Save User Message
    # -----------------------------
    user_msg = Message(
        session_id=session_id,
        role="user",
        content=user_message
    )

    db.add(user_msg)
    db.commit()

    # -----------------------------
    # Save User Memory
    # -----------------------------
    save_memory(
        current_user.id,
        user_message,
        db
    )

    # -----------------------------
    # Load Previous Conversation
    # -----------------------------
    messages = (
        db.query(Message)
        .filter(Message.session_id == session_id)
        .order_by(Message.id.asc())
        .all()
    )

    conversation = []

    for msg in messages:
        conversation.append(
            {
                "role": msg.role,
                "content": msg.content
            }
        )

    
    # -----------------------------
    # Route Tool
    # -----------------------------
    tool_used = route_tool(user_message)

    print("🛠 Selected Tool:", tool_used)
    tool_result = None
    if tool_used!="llm":
        tool_result = execute_tool(
            tool_used,
            user_message,
            current_user,
            db
       )

    if tool_used == "calculator":
        ai_msg = Message(
           session_id=session_id,
           role="assistant",
           content=tool_result
        )

        db.add(ai_msg)
        db.commit()

        return {
        "session_id": session_id,
        "response": tool_result,
        "tool": tool_used
    }

    elif tool_used == "memory":

       conversation.append(
        {
            "role": "system",
            "content": f"""
             User Memory:

            {tool_result}

            Answer using only the stored memory.
            """
        }
        )

    elif tool_used == "weather":
      print("🌦 WEATHER RESULT =", tool_result)

      conversation.append(
        {
            "role": "system",
            "content": f"""
            Current Weather Information:

            {tool_result["snippet"]}

            Answer naturally using this weather information.
            Do NOT say you don't have internet access.
            Do NOT say you don't have real-time weather.
             """
        }
        )
    elif tool_used == "web_search":

        formatted_results = ""

        for result in tool_result:

            formatted_results += f"""
               Title: {result['title']}
               Snippet: {result['snippet']}
               Link: {result['link']}"""

        conversation.append(
          {
            "role": "system",
            "content": f"""
You have LIVE web search results.

Use ONLY the search results below whenever they are relevant.

Search Results:

{formatted_results}
"""
        }
    )


    # -----------------------------
    # Generate AI Response
    # -----------------------------
    future = executor.submit(
        generate_response,
        conversation
    )

    ai_response = future.result()

    # -----------------------------
    # Save AI Response
    # -----------------------------
    ai_msg = Message(
        session_id=session_id,
        role="assistant",
        content=ai_response
    )

    db.add(ai_msg)
    db.commit()

    return {
        "session_id": session_id,
        "response": ai_response,
        "tool": tool_used
    }