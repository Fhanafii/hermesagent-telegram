import os

from dotenv import load_dotenv

load_dotenv()


ALLOWED_USER_IDS = {
    int(user_id.strip())
    for user_id in os.getenv("ALLOWED_USER_IDS", "").split(",")
    if user_id.strip()
}


def is_authorized(user_id: int) -> bool:
    return user_id in ALLOWED_USER_IDS