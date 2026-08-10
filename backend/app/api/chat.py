from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.models import (
    ChatSession,
    Message,
    User,
    Feedback
)

from app.database.schemas import (
    SessionCreate,
    SessionResponse,
    MessageResponse,
    ChatRequest,
    ChatResponse,
    FeedbackResponse,
    FeedbackCreate
)

from app.auth.dependencies import get_current_user
from app.services.chat_service import process_chat


router = APIRouter(tags=["Chat"])


# =========================================================
# CREATE CHAT SESSION
# =========================================================

@router.post(
    "/sessions",
    response_model=SessionResponse
)
def create_session(
    session: SessionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    new_session = ChatSession(
        title=session.title,
        user_id=current_user.id
    )

    db.add(new_session)
    db.commit()
    db.refresh(new_session)

    return new_session


# =========================================================
# GET ALL CHAT SESSIONS
# =========================================================

@router.get(
    "/sessions",
    response_model=list[SessionResponse]
)
def get_sessions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    sessions = (
        db.query(ChatSession)
        .filter(
            ChatSession.user_id == current_user.id
        )
        .order_by(ChatSession.id.desc())
        .all()
    )

    return sessions


# =========================================================
# GET MESSAGES OF A SESSION
# =========================================================

@router.get(
    "/sessions/{session_id}",
    response_model=list[MessageResponse]
)
def get_chat_messages(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    chat_session = (
        db.query(ChatSession)
        .filter(
            ChatSession.id == session_id,
            ChatSession.user_id == current_user.id
        )
        .first()
    )

    if chat_session is None:
        raise HTTPException(
            status_code=404,
            detail="Chat session not found"
        )

    messages = (
        db.query(Message)
        .filter(
            Message.session_id == session_id
        )
        .order_by(Message.id.asc())
        .all()
    )

    return messages


# =========================================================
# CHAT
# =========================================================

@router.post(
    "/chat",
    response_model=ChatResponse
)
def chat(
    chat: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    response = process_chat(
        session_id=chat.session_id,
        user_message=chat.message,
        db=db,
        current_user=current_user
    )

    return response


# =========================================================
# SUBMIT FEEDBACK
# =========================================================

@router.post(
    "/feedback",
    response_model=FeedbackResponse
)
def submit_feedback(
    feedback: FeedbackCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    message = (
        db.query(Message)
        .join(ChatSession)
        .filter(
            Message.id == feedback.message_id,
            ChatSession.user_id == current_user.id
        )
        .first()
    )

    if message is None:
        raise HTTPException(
            status_code=404,
            detail="Message not found"
        )

    new_feedback = Feedback(
        message_id=feedback.message_id,
        rating=feedback.rating,
        comment=feedback.comment
    )

    db.add(new_feedback)
    db.commit()
    db.refresh(new_feedback)

    return new_feedback


# =========================================================
# DELETE CHAT SESSION
# =========================================================

@router.delete(
    "/sessions/{session_id}"
)
def delete_session(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

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
            detail="Session not found"
        )

    # -----------------------------------------
    # Delete all messages
    # -----------------------------------------

    db.query(Message).filter(
        Message.session_id == session_id
    ).delete(
        synchronize_session=False
    )

    # -----------------------------------------
    # Delete session
    # -----------------------------------------

    db.delete(session)
    db.commit()

    return {
        "message": "Chat deleted successfully"
    }