from uuid import uuid4
import redis.asyncio as aioredis  # type: ignore


class AsyncSessionManager:
    def __init__(self, *, redis: aioredis.Redis, session_expiry: int = 3600):
        self.redis = redis
        self.session_expiry = session_expiry

    async def create_session(self, user_id: int) -> str:
        session_id = str(uuid4())
        await self.redis.set(session_id, user_id, ex=self.session_expiry)
        return session_id

    async def get_user_id(self, session_id: str) -> int | None:
        user_id = await self.redis.get(session_id)
        return int(user_id) if user_id else None

    async def delete_session(self, session_id: str) -> None:
        await self.redis.delete(session_id)
