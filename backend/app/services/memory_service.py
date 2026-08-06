import re
from sqlalchemy.orm import Session

from app.database.models import UserMemory


def save_memory(user_id: int, message: str, db: Session):

    patterns = [
        (
            r"my name is (.+)",
            "name"
        ),
        (
            r"i am (.+)",
            "profession"
        ),
        (
            r"i live in (.+)",
            "location"
        ),
        (
            r"my favourite food is (.+)",
            "favorite_food"
        ),
        (
            r"my favorite food is (.+)",
            "favorite_food"
        ),
    ]

    message = message.lower()

    for pattern, key in patterns:

        match = re.search(pattern, message)

        if match:

            value = match.group(1).strip()

            existing = (
                db.query(UserMemory)
                .filter(
                    UserMemory.user_id == user_id,
                    UserMemory.memory_key == key
                )
                .first()
            )

            if existing:

                existing.memory_value = value

            else:

                memory = UserMemory(
                    user_id=user_id,
                    memory_key=key,
                    memory_value=value
                )

                db.add(memory)

            db.commit()