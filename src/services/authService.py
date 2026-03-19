from src import SECRET_KEY, ALGORITHM_TO_HASH, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import datetime, timedelta, timezone
from jose import jwt


def create_tolkien(user_id: str, expire_time: timedelta, SECRET: str):
    payload = {
        "id": user_id,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    return jwt.encode(claims=payload, key=SECRET, algorithm=ALGORITHM_TO_HASH)