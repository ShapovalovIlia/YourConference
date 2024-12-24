from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select

from fastapi import APIRouter, HTTPException, Depends, Cookie, Query

from yo.infrastructure import (
    get_postgres_async_conn,
    ConferencesOrm,
    AsyncSessionManager,
    RegistrationsOrm,
    AdminsOrm,
    get_session_manager,
)


conference_router = APIRouter(prefix="/conferences")


@conference_router.get("")  # type: ignore
async def get_conferences_list(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, gt=0),
    db_conn: AsyncSession = Depends(get_postgres_async_conn),
):
    query = select(ConferencesOrm).offset(skip).limit(limit)
    conferences = await db_conn.execute(query)
    return conferences
