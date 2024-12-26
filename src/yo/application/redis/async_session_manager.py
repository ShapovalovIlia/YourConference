from uuid import uuid4, UUID

import redis.asyncio as aioredis  # type: ignore

from fastapi import Depends

from yo.application.redis.redis_conn import get_redis_async_conn
from yo.application.exceptions import UknownSessionIdError
from yo.application.user_type import UserType


class AsyncSessionManager:
    def __init__(self, *, redis: aioredis.Redis, session_expiry: int = 3600):
        self._redis = redis
        self._session_expiry = session_expiry

    async def create_session(
        self, user_id: UUID, user_type: UserType = UserType.USER
    ) -> str:
        session_id = str(uuid4())
        key = f"{user_type.value}:{session_id}"

        await self._redis.set(key, str(user_id), ex=self._session_expiry)
        return session_id

    async def get_id(
        self, session_id: str, user_type: UserType = UserType.USER
    ) -> UUID:
        key = f"{user_type.value}:{session_id}"
        user_id = await self._redis.get(key)

        if not user_id:
            raise UknownSessionIdError(
                message=f"Session expired or unknown for {user_type}"
            )

        return UUID(user_id.decode("utf-8"))

    async def delete_session(
        self, session_id: str, user_type: UserType = UserType.USER
    ) -> None:
        key = f"{user_type.value}:{session_id}"
        await self._redis.delete(key)


def get_session_manager(
    redis: aioredis.Redis = Depends(get_redis_async_conn),
) -> AsyncSessionManager:
    return AsyncSessionManager(redis=redis)
