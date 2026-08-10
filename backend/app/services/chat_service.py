from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.database.models import ChatSession, Message
from app.services.memory_service import save_memory
from app.agents.graph import chat_graph


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
    # Run LangGraph
    # -----------------------------

    result = chat_graph.invoke(
        {
            "session_id": session_id,
            "user_message": user_message,
            "db": db,
            "current_user": current_user,
            "conversation": conversation
        }
    )

    # Multiple tools
    tools_used = result.get("tools_used", ["llm"])
    ai_response = result.get("ai_response", "")

    print("🤖 LangGraph Response:", ai_response)
    print("🛠 Tools Used:", tools_used)

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

    # -----------------------------
    # Return Response
    # -----------------------------

    return {
        "session_id": session_id,
        "response": ai_response,
        "tool": tools_used
    }