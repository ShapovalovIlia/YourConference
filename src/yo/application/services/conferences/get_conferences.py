from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from fastapi import Depends

from yo.application.postgres import Conference, get_postgres_async_conn


class GetConferencesProcessor:
    def __init__(self, db_conn: AsyncSession) -> None:
        self._db_conn = db_conn

    async def process(
        self,
        *,
        skip: int,
        limit: int,
    ) -> Sequence[Conference]:
        query = select(Conference).offset(skip).limit(limit)
        result = await self._db_conn.execute(query)
        confernces = result.scalars().all()

        return confernces


def get_get_conferences_processor(
    db_conn: AsyncSession = Depends(get_postgres_async_conn),
) -> GetConferencesProcessor:
    return GetConferencesProcessor(db_conn=db_conn)
