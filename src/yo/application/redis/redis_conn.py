from dataclasses import dataclass
import os

import redis.asyncio as aioredis  # type: ignore


@dataclass(frozen=True, slots=True)
class RedisConfig:
    url: str


def env_var_by_key(key: str) -> str:
    """
    Returns value from env vars by key
    if value exists, otherwise raises
    Exception.
    """
    value = os.getenv(key)
    if not value:
        message = f"Env var {key} doesn't exist"
        raise Exception(message)
    return value


def get_redis_config() -> RedisConfig:
    redis_host = env_var_by_key("REDIS_HOST")
    redis_port = env_var_by_key("REDIS_PORT")

    return RedisConfig(f"redis://{redis_host}:{redis_port}")


async def get_redis_async_conn():
    async with aioredis.from_url(
        get_redis_config().url, encoding="utf-8", decode_responses=True
    ) as session:  # TODO: сделать логику через диренв
        yield session
