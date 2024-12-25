from uuid import uuid4
import redis.asyncio as aioredis  # type: ignore

from fastapi import Depends

from yo.application.redis.redis_conn import get_redis_async_conn
from yo.application.exceptions import UknownSessionIdError


class AsyncSessionManager:
    def __init__(self, *, redis: aioredis.Redis, session_expiry: int = 3600):
        self._redis = redis
        self._session_expiry = session_expiry

    async def create_session(self, user_id: int) -> str:
        session_id = str(uuid4())
        await self._redis.set(session_id, user_id, ex=self._session_expiry)
        return session_id

    async def get_user_id(self, session_id: str) -> int:
        user_id = await self._redis.get(session_id)

        if not user_id:
            raise UknownSessionIdError(message="Session expired or unknown")

        return int(user_id)

    async def delete_session(self, session_id: str) -> None:
        await self._redis.delete(session_id)


def get_session_manager(
    redis: aioredis.Redis = Depends(get_redis_async_conn),
) -> AsyncSessionManager:
    return AsyncSessionManager(redis=redis)
