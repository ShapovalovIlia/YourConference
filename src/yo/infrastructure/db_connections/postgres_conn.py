from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from yo.infrastructure.postgres.config import async_postgres_config_from_env


_engine = create_async_engine(
    async_postgres_config_from_env().url, echo=True
)  # TODO: убрать глобальную переменную
_AsyncSessionLocal = async_sessionmaker(
    bind=_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_postgres_async_conn():
    async with _AsyncSessionLocal() as session:
        yield session
