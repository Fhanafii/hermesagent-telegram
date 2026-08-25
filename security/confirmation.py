import secrets
import time


CONFIRMATION_TIMEOUT = 60


class ConfirmationManager:
    def __init__(self):
        self.pending = {}

    def create(
        self,
        user_id: int,
        tool_name: str,
        arguments: dict,
    ) -> str:

        token = secrets.token_urlsafe(16)

        self.pending[token] = {
            "user_id": user_id,
            "tool": tool_name,
            "arguments": arguments,
            "created_at": time.time(),
        }

        return token

    def get(
        self,
        token: str,
    ) -> dict | None:

        request = self.pending.get(token)

        if request is None:
            return None

        if time.time() - request["created_at"] > CONFIRMATION_TIMEOUT:
            del self.pending[token]
            return None

        return request

    def consume(
        self,
        token: str,
    ) -> dict | None:

        request = self.get(token)

        if request is None:
            return None

        del self.pending[token]

        return request

    def cancel(
        self,
        token: str,
    ) -> bool:

        if token not in self.pending:
            return False

        del self.pending[token]

        return True