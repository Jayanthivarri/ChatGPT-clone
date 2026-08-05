from fastapi import HTTPException
from sqlalchemy.orm import Session
from concurrent.futures import ThreadPoolExecutor

from app.database.models import ChatSession, Message
from app.services.llm_service import (
    generate_response,
    should_search
)
from app.tools.web_search import web_search

executor = ThreadPoolExecutor(max_workers=5)


def process_chat(
    session_id: int | None,
    user_message: str,
    db: Session,
    current_user
):

    # Create new session if it's the first message
    if session_id is None:

        session = ChatSession(
            title=user_message[:30],
            user_id=current_user.id
        )

        db.add(session)
        db.commit()
        db.refresh(session)

        session_id = session.id

    else:

        # Check existing session
        session = db.query(ChatSession).filter(
            ChatSession.id == session_id,
            ChatSession.user_id == current_user.id
        ).first()

        if session is None:
            raise HTTPException(
                status_code=404,
                detail="Chat session not found"
            )

    # Save user message
    user_msg = Message(
        session_id=session_id,
        role="user",
        content=user_message
    )

    db.add(user_msg)
    db.commit()

    # Load previous conversation
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
    # Web Search (Only if required)
    # -----------------------------
    if should_search(user_message):

        print("🌐 Performing Web Search...")

        search_results = web_search(user_message)

        formatted_results = ""

        for result in search_results:

            formatted_results += f"""
Title: {result['title']}
Snippet: {result['snippet']}
Link: {result['link']}

"""

        conversation.append(
            {
                "role": "system",
                "content": f"""
Use the following web search results while answering the user.

{formatted_results}

If the search results are useful, use them.
Otherwise answer normally.
"""
            }
        )

    # Generate AI response
    future = executor.submit(
        generate_response,
        conversation
    )

    ai_response = future.result()

    # Save AI response
    ai_msg = Message(
        session_id=session_id,
        role="assistant",
        content=ai_response
    )

    db.add(ai_msg)
    db.commit()

    return {
        "session_id": session_id,
        "response": ai_response
    }