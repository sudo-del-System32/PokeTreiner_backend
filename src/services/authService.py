from src import ALGORITHM_TO_HASH
from datetime import datetime, timedelta, timezone
from jose import jwt


def create_tolkien(user_id: str, expire_time: timedelta, SECRET: str):
    payload = {
        "id": user_id,
        "exp": datetime.now(timezone.utc) + expire_time
    }
    return jwt.encode(claims=payload, key=SECRET, algorithm=ALGORITHM_TO_HASH)