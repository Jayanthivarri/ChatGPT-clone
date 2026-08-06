from sqlalchemy.orm import Session

from app.database.models import UserMemory


def get_memory(user_id: int, db: Session):

    memories = (
        db.query(UserMemory)
        .filter(UserMemory.user_id == user_id)
        .all()
    )

    if not memories:
        return "No stored memory."

    memory_text = ""

    for memory in memories:

        memory_text += (
            f"{memory.memory_key}: "
            f"{memory.memory_value}\n"
        )

    return memory_text