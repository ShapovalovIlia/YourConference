from uuid import uuid4

import redis.asyncio as aioredis # type: ignore

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse

from yo.infrastructure.di import get_postgres_async_conn, get_redis_async_conn
from yo.infrastructure.postgres.orm_models import AdminsOrm
from yo.presentation.validation_models import AdminForm


auth_router = APIRouter()


@auth_router.post("/login") # type: ignore
async def login(
    form_data: AdminForm = Depends(),
    db_conn: AsyncSession = Depends(get_postgres_async_conn),
    redis: aioredis.Redis = Depends(get_redis_async_conn),
):
    query = select(AdminsOrm).filter(AdminsOrm.username == form_data.username)
    result = await db_conn.execute(query)
    admin = result.scalar_one_or_none()

    if admin is None:
        raise HTTPException(
            status_code=401, detail="Incorrect username or password"
        )

    if form_data.password != admin.password:
        raise HTTPException(
            status_code=401, detail="Incorrect username or password"
        )

    session_id = str(uuid4())
    await redis.set(session_id, admin.id, ex=30)  # TODO поменять после тестов

    response = JSONResponse(
        content={"message": "Login successful", "username": admin.username},
        status_code=200,
    )

    response.set_cookie("session_id", session_id)
    return response
